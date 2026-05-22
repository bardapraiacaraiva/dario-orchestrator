"""FastAPI license server (Onda 8)."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
from datetime import UTC, datetime, timedelta

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from license_server.db import (
    DEFAULT_DB_PATH,
    db_connect,
    get_trial,
    insert_trial,
    log_event,
    mark_status,
    update_heartbeat,
    upgrade_to_vip,
)

# ─── Config ──────────────────────────────────────────────────────────────────

SERVER_SECRET = os.getenv("LICENSE_SERVER_SECRET", "").strip()
TRIAL_DAYS = int(os.getenv("LICENSE_TRIAL_DAYS", "7"))
ALLOW_SNAPSHOT_ROLLBACK_TOLERANCE_HOURS = int(
    os.getenv("LICENSE_ROLLBACK_TOLERANCE_HOURS", "1")
)


def _require_secret() -> str:
    """Fail-loud if the operator forgot to set the server secret."""
    if not SERVER_SECRET or len(SERVER_SECRET) < 32:
        raise RuntimeError(
            "LICENSE_SERVER_SECRET env var must be set (≥32 chars). "
            "Generate one with: python -c 'import secrets; "
            "print(secrets.token_hex(32))'"
        )
    return SERVER_SECRET


def _sign(payload: str) -> str:
    secret = _require_secret()
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


def _token_for(machine_id: str, first_init_at: str, expires_at: str) -> str:
    """Generate an opaque, HMAC-signed token clients can stash locally."""
    nonce = secrets.token_hex(8)
    payload = f"{machine_id}|{first_init_at}|{expires_at}|{nonce}"
    signature = _sign(payload)
    # Token format: base64-style "payload.signature" (we keep `|` for readability)
    return f"{payload}.{signature}"


def _verify_token(token: str, machine_id: str) -> dict:
    """Return {valid, payload?, reason?}."""
    if "." not in token:
        return {"valid": False, "reason": "malformed_token"}
    payload, signature = token.rsplit(".", 1)
    expected = _sign(payload)
    if not hmac.compare_digest(signature, expected):
        return {"valid": False, "reason": "bad_signature"}
    parts = payload.split("|")
    if len(parts) != 4:
        return {"valid": False, "reason": "malformed_payload"}
    if parts[0] != machine_id:
        return {"valid": False, "reason": "machine_mismatch"}
    return {
        "valid": True,
        "machine_id": parts[0],
        "first_init_at": parts[1],
        "expires_at": parts[2],
        "nonce": parts[3],
    }


# ─── Pydantic contracts ──────────────────────────────────────────────────────


class ActivateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    machine_id: str = Field(min_length=4, max_length=200)


class ValidateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    machine_id: str = Field(min_length=4, max_length=200)
    token: str = Field(min_length=16)
    client_first_init_at: str | None = None  # local belief, for rollback detection


class VipActivateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    machine_id: str = Field(min_length=4, max_length=200)
    vip_key: str = Field(min_length=8, max_length=64)


class TrialResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    machine_id: str
    tier: str
    status: str
    first_init_at: str
    expires_at: str | None
    days_remaining: int = 0
    token: str
    heartbeat_count: int = 0


class ValidationResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    valid: bool
    tier: str = "trial"
    status: str = "unknown"
    days_remaining: int = 0
    expires_at: str | None = None
    reason: str | None = None
    rollback_detected: bool = False
    heartbeat_count: int = 0


# ─── App ─────────────────────────────────────────────────────────────────────


app = FastAPI(
    title="DARIO License Server",
    version="1.0.0",
    description="Server-side trial enforcement with anti-snapshot rollback detection.",
)


def _trial_to_response(trial: dict, days_remaining: int) -> TrialResponse:
    return TrialResponse(
        machine_id=trial["machine_id"],
        tier=trial["tier"],
        status=trial["status"],
        first_init_at=trial["first_init_at"],
        expires_at=trial["expires_at"] or None,
        days_remaining=max(0, days_remaining),
        token=trial["token"],
        heartbeat_count=trial["heartbeat_count"],
    )


def _days_remaining(expires_at: str) -> int:
    if not expires_at:
        return 999999  # effectively unlimited (pro/enterprise)
    try:
        exp = datetime.fromisoformat(expires_at)
        now = datetime.now(UTC)
        delta = exp - now
        return max(0, delta.days + (1 if delta.seconds > 0 else 0))
    except Exception:
        return 0


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "dario-license-server", "version": "1.0.0"}


@app.post("/trial/activate", response_model=TrialResponse)
async def trial_activate(req: ActivateRequest) -> TrialResponse:
    """Activate (or return existing) trial for the given machine_id.

    Idempotent: re-calling with the same machine_id returns the same trial
    record. There is exactly one trial per machine, ever.
    """
    _require_secret()
    with db_connect() as conn:
        existing = get_trial(conn, req.machine_id)
        if existing:
            log_event(conn, req.machine_id, "activate_repeat",
                      json.dumps({"existing_status": existing["status"]}))
            return _trial_to_response(existing, _days_remaining(existing["expires_at"]))

        # New trial
        now = datetime.now(UTC)
        first_init = now.isoformat()
        expires = (now + timedelta(days=TRIAL_DAYS)).isoformat()
        token = _token_for(req.machine_id, first_init, expires)
        trial = insert_trial(conn, req.machine_id, first_init, expires, token)
        log_event(conn, req.machine_id, "activate_new",
                  json.dumps({"expires_at": expires}))
        return _trial_to_response(trial, TRIAL_DAYS)


@app.post("/trial/validate", response_model=ValidationResponse)
async def trial_validate(req: ValidateRequest) -> ValidationResponse:
    """Validate a client's token + record heartbeat.

    Performs three checks:
      1. Token signature (cryptographic — anyone tampering invalidates this)
      2. Server-side expiration (server clock is the source of truth)
      3. Snapshot-rollback detection: if client's local `client_first_init_at`
         is *later* than the server's `first_init_at`, the client clock or
         install is a VM snapshot rolled back to before the original activation.

    Records a heartbeat row in `audit_log` on every call so the server's
    `last_seen_at` stays current.
    """
    _require_secret()
    tok = _verify_token(req.token, req.machine_id)
    if not tok["valid"]:
        return ValidationResponse(valid=False, reason=tok["reason"])

    with db_connect() as conn:
        trial = get_trial(conn, req.machine_id)
        if not trial:
            log_event(conn, req.machine_id, "validate_no_record",
                      json.dumps({"reason": tok["reason"] if not tok["valid"] else "ok"}))
            return ValidationResponse(valid=False, reason="no_trial_record")

        # Token must match what we stored (defends against replay of a
        # forged-with-leaked-secret-but-old-payload token).
        if trial["token"] != req.token:
            log_event(conn, req.machine_id, "validate_token_mismatch", "{}")
            return ValidationResponse(valid=False, reason="token_replaced",
                                       status=trial["status"])

        # Server-side expiration (source of truth)
        rollback_detected = False
        if req.client_first_init_at:
            try:
                client_init = datetime.fromisoformat(req.client_first_init_at)
                server_init = datetime.fromisoformat(trial["first_init_at"])
                tolerance = timedelta(hours=ALLOW_SNAPSHOT_ROLLBACK_TOLERANCE_HOURS)
                # If client claims it started LATER than server records,
                # the install is a snapshot rolled forward in time.
                # If client claims it started EARLIER than server records
                # by more than the tolerance, the local files were tampered.
                drift = abs(client_init - server_init)
                if drift > tolerance:
                    rollback_detected = True
            except Exception:
                rollback_detected = False

        update_heartbeat(conn, req.machine_id)
        trial = get_trial(conn, req.machine_id)  # refresh after heartbeat
        assert trial is not None

        days_remaining = _days_remaining(trial["expires_at"]) if trial["tier"] == "trial" else 999999
        valid = (
            trial["status"] == "active"
            and (trial["tier"] != "trial" or days_remaining > 0)
            and not rollback_detected
        )

        # If expired, persist the new status so future checks are O(1)
        if trial["tier"] == "trial" and days_remaining == 0 and trial["status"] == "active":
            mark_status(conn, req.machine_id, "expired")
            trial["status"] = "expired"

        log_event(
            conn,
            req.machine_id,
            "validate",
            json.dumps({
                "valid": valid,
                "days_remaining": days_remaining,
                "rollback_detected": rollback_detected,
                "tier": trial["tier"],
            }),
        )

        return ValidationResponse(
            valid=valid,
            tier=trial["tier"],
            status=trial["status"],
            days_remaining=days_remaining,
            expires_at=trial["expires_at"] or None,
            rollback_detected=rollback_detected,
            heartbeat_count=trial["heartbeat_count"],
            reason=(
                None if valid else
                ("rollback_detected" if rollback_detected else
                 ("expired" if trial["status"] == "expired" else "invalid"))
            ),
        )


@app.post("/vip/activate", response_model=TrialResponse)
async def vip_activate(req: VipActivateRequest) -> TrialResponse:
    """Bind a VIP key to a machine. After this, /trial/validate returns
    tier=pro|enterprise and `days_remaining` is effectively unbounded.

    The VIP key itself is validated by the orchestrator's MASTER_SECRET on
    the client side (it must already pass `validate_key` before being sent
    here). The server is the canonical record of "which machine is bound
    to which key", not the issuer of keys.
    """
    _require_secret()

    # Trivial pattern check on the key shape — the heavy validation happens
    # on the client with MASTER_SECRET; here we just refuse obvious garbage.
    if not req.vip_key.startswith("DARIO-") or req.vip_key.count("-") < 4:
        raise HTTPException(400, "VIP key must match DARIO-XXXX-XXXX-XXXX-TIER format")

    tier = req.vip_key.split("-")[-1].lower()
    if tier not in ("pro", "ent", "enterprise"):
        raise HTTPException(400, "Unrecognised tier in VIP key")
    if tier == "ent":
        tier = "enterprise"

    with db_connect() as conn:
        existing = get_trial(conn, req.machine_id)
        now = datetime.now(UTC)
        if not existing:
            # Bootstrap a record so we have something to upgrade.
            first_init = now.isoformat()
            placeholder_token = _token_for(req.machine_id, first_init, "")
            insert_trial(conn, req.machine_id, first_init, "", placeholder_token)

        upgrade_to_vip(conn, req.machine_id, tier, req.vip_key)
        log_event(
            conn,
            req.machine_id,
            "upgrade",
            json.dumps({"vip_key_tail": req.vip_key[-4:], "tier": tier}),
        )
        trial = get_trial(conn, req.machine_id)
        assert trial is not None
        return _trial_to_response(trial, 999999)


def main():
    import argparse

    import uvicorn

    parser = argparse.ArgumentParser(description="DARIO License Server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8430)
    parser.add_argument("--db", help="SQLite DB path (overrides LICENSE_SERVER_DB env)")
    args = parser.parse_args()

    if args.db:
        os.environ["LICENSE_SERVER_DB"] = args.db

    # Fail loudly if the secret is not set, rather than serving requests
    # that produce useless tokens.
    _require_secret()
    print(f"DB path: {DEFAULT_DB_PATH}")
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
