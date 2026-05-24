#!/usr/bin/env python3
"""
DARIO License Manager — Simplified per RFC_STRATEGIC_DECISIONS (Risk #4).

Was 1577 LOC with 3-layer fingerprint (orch dir + home obfuscated + Windows registry),
anti-debug checks, snapshot rollback detection, cert-pinned server revalidation.

Strategic decision 2026-05-24 (framing C consulting accelerator):
the obfuscation defended against zero real threats — anyone with
pyc-decompile + 30min broke it. Maintenance burden was disproportionate
to risk model.

This rewrite (~280 LOC) keeps the honest minimum:
  - License key generation + validation (HMAC against MASTER_SECRET)
  - File-based license storage (~/.claude/orchestrator/.license)
  - Trial init (7-day expiry, no fingerprint anti-snapshot)
  - Server-side check (optional, fail-soft, signal not security boundary)
  - Tier capabilities lookup

API surface preserved so license_guard.py + runtime.py don't break.

Key format: DARIO-XXXX-XXXX-XXXX-TIER (unchanged)
Tiers: trial / pro / enterprise (unchanged dict structure)

Usage:
    python license_manager.py --status
    python license_manager.py --activate DARIO-XXXX-XXXX-XXXX-PRO
    python license_manager.py --init-trial
    python license_manager.py --check
    python license_manager.py --generate-key TIER EMAIL  # admin only
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import logging
import os
import secrets
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

# Optional server client (fail-soft if not present)
try:
    from license_client import is_enabled as server_enabled
    from license_client import (
        init_trial_remote, report_activation, report_check, revalidate,
    )
except ImportError:
    def server_enabled() -> bool:
        return False

    def init_trial_remote(*a, **kw):
        return None

    def report_activation(*a, **kw):
        return None

    def report_check(*a, **kw):
        return None

    def revalidate(*a, **kw):
        return None


ORCH_DIR = Path.home() / ".claude" / "orchestrator"
LICENSE_FILE = ORCH_DIR / "license.json"

# MASTER_SECRET: env override or file fallback.
# Production deployment must set DARIO_MASTER_SECRET to a 32+ char random string.
MASTER_SECRET_FILE = ORCH_DIR / ".master_secret"
DEFAULT_INSECURE_SECRET = "dario-dev-secret-replace-in-production"

TIER_MAP = {"TRIAL": "trial", "PRO": "pro", "ENT": "enterprise"}

# Tier capabilities (unchanged from original — referenced by callers)
TIERS = {
    "trial": {
        "name": "Trial",
        "duration_days": 7,
        "price_brl_month": 0,
        "max_parallel": 3,
        "engines_allowed": "all",
        "features": {
            "api_execution": True, "evolution_engine": True, "llm_judge": True,
            "predictive_dispatch": True, "chain_executor": True,
            "multi_tenancy": True, "federation": True, "plugins": True,
            "adaptive_rubrics": True, "dashboard": True, "task_templates": True,
        },
    },
    "pro": {
        "name": "Professional",
        "duration_days": None,
        "price_brl_month": 297,
        "max_parallel": 3,
        "engines_allowed": "all",
        "features": {
            "api_execution": True, "evolution_engine": True, "llm_judge": True,
            "predictive_dispatch": True, "chain_executor": True,
            "multi_tenancy": False, "federation": False, "plugins": True,
            "adaptive_rubrics": True, "dashboard": True, "task_templates": True,
        },
    },
    "enterprise": {
        "name": "Enterprise",
        "duration_days": None,
        "price_brl_month": 997,
        "max_parallel": 5,
        "engines_allowed": "all",
        "features": {
            "api_execution": True, "evolution_engine": True, "llm_judge": True,
            "predictive_dispatch": True, "chain_executor": True,
            "multi_tenancy": True, "federation": True, "plugins": True,
            "adaptive_rubrics": True, "dashboard": True, "task_templates": True,
        },
    },
}


def _load_master_secret() -> bytes:
    """Load HMAC master secret from env or file. Returns insecure default
    if neither available (logs warning)."""
    env = os.getenv("DARIO_MASTER_SECRET", "").strip()
    if env:
        return env.encode("utf-8")
    if MASTER_SECRET_FILE.exists():
        return MASTER_SECRET_FILE.read_bytes().strip()
    logging.warning(
        "DARIO_MASTER_SECRET not set and no .master_secret file — "
        "using INSECURE default. Set env or write ~/.claude/orchestrator/.master_secret"
    )
    return DEFAULT_INSECURE_SECRET.encode("utf-8")


def _hmac_signature(payload: str) -> str:
    """Compute HMAC-SHA256 of payload, return uppercase hex."""
    return hmac.new(_load_master_secret(), payload.encode("utf-8"),
                    hashlib.sha256).hexdigest().upper()


def _machine_id() -> str:
    """Stable per-machine identifier — hash of hostname + user.

    Simplified from previous 3-layer fingerprint. Just enough to dedupe
    trial inits, NOT a security boundary.
    """
    import platform
    raw = f"{platform.node()}-{os.environ.get('USER') or os.environ.get('USERNAME', '')}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


# ─── KEY GENERATION + VALIDATION ─────────────────────────────────────────────

def generate_key(tier: str, email: str = "") -> str:
    """Generate a license key for the given tier. Admin/server use only."""
    tier_upper = next((k for k, v in TIER_MAP.items() if v == tier), None)
    if not tier_upper:
        raise ValueError(f"Unknown tier: {tier}. Use one of {list(TIERS.keys())}")
    nonce = secrets.token_hex(2).upper()  # 4 hex chars
    payload = f"{tier}:{nonce}"
    sig = _hmac_signature(payload)[:8]
    return f"DARIO-{nonce}-{sig[:4]}-{sig[4:8]}-{tier_upper}"


def validate_key(key: str) -> dict:
    """Validate a license key by recomputing HMAC against MASTER_SECRET.

    Returns {"valid": True, "tier": ...} if signature matches.
    Returns {"valid": False, "reason": ...} otherwise.
    """
    if not key or not key.startswith("DARIO-"):
        return {"valid": False, "reason": "Invalid key format"}
    parts = key.split("-")
    if len(parts) != 5:
        return {"valid": False, "reason": "Key must have 5 segments"}
    nonce, sig1, sig2, suffix = parts[1], parts[2], parts[3], parts[4].upper()
    if suffix not in TIER_MAP:
        return {"valid": False, "reason": f"Unknown tier suffix: {suffix}"}
    tier = TIER_MAP[suffix]
    payload = f"{tier}:{nonce}"
    expected = _hmac_signature(payload)
    presented = sig1.upper() + sig2.upper()
    if not hmac.compare_digest(presented, expected[:8]):
        return {"valid": False, "reason": "Signature mismatch"}
    return {"valid": True, "tier": tier}


# ─── LICENSE FILE I/O ────────────────────────────────────────────────────────

def load_license() -> dict:
    """Load license file or return empty dict."""
    if not LICENSE_FILE.exists():
        return {}
    try:
        return json.loads(LICENSE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_license(lic: dict) -> None:
    """Persist license dict to file."""
    LICENSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    LICENSE_FILE.write_text(json.dumps(lic, indent=2), encoding="utf-8")


# ─── TIER OPERATIONS ─────────────────────────────────────────────────────────

def init_trial(force: bool = False) -> dict:
    """Initialize a 7-day trial license. Idempotent unless force=True."""
    existing = load_license()
    if existing and not force:
        return {"status": "exists", "license": existing}
    now = datetime.now(UTC)
    expires = now + timedelta(days=TIERS["trial"]["duration_days"])
    lic = {
        "tier": "trial",
        "machine_id": _machine_id(),
        "activated_at": now.isoformat(timespec="seconds"),
        "expires_at": expires.isoformat(timespec="seconds"),
        "email": "",
        "key": "",
    }
    save_license(lic)
    if server_enabled():
        init_trial_remote(lic["machine_id"])
    return {"status": "initialized", "license": lic}


def activate_key(key: str) -> dict:
    """Activate a license key (PRO or ENT). Validates HMAC + saves."""
    result = validate_key(key)
    if not result.get("valid"):
        return {"status": "error", "reason": result.get("reason")}
    tier = result["tier"]
    if tier == "trial":
        return {"status": "error", "reason": "Cannot activate trial via key — use --init-trial"}
    now = datetime.now(UTC).isoformat(timespec="seconds")
    lic = {
        "tier": tier,
        "key": key,
        "machine_id": _machine_id(),
        "activated_at": now,
        "expires_at": None,  # PRO/ENT are permanent
        "email": "",
    }
    save_license(lic)
    if server_enabled():
        report_activation(key, lic["machine_id"], tier)
    return {"status": "activated", "license": lic}


def check_license() -> dict:
    """Check current license state. Returns status + tier + days remaining."""
    lic = load_license()
    if not lic:
        return {"valid": False, "reason": "No license — run --init-trial or --activate"}
    tier = lic.get("tier")
    if tier not in TIERS:
        return {"valid": False, "reason": f"Unknown tier in license: {tier}"}
    # Permanent tiers
    if tier in ("pro", "enterprise"):
        # Optional server revalidation (fail-soft)
        if server_enabled() and lic.get("key"):
            srv = revalidate(lic["key"], lic.get("machine_id", ""))
            if srv and srv.get("revoked"):
                return {"valid": False, "reason": "License revoked by server", "tier": tier}
        return {"valid": True, "tier": tier, "days_remaining": None}
    # Trial — check expiry
    expires_str = lic.get("expires_at")
    if not expires_str:
        return {"valid": False, "reason": "Trial license has no expires_at field"}
    try:
        expires = datetime.fromisoformat(expires_str)
    except ValueError:
        return {"valid": False, "reason": f"Invalid expires_at: {expires_str}"}
    now = datetime.now(UTC)
    if now >= expires:
        return {"valid": False, "reason": "Trial expired", "tier": "trial",
                "days_remaining": 0}
    return {"valid": True, "tier": "trial",
            "days_remaining": (expires - now).days}


def is_feature_allowed(feature: str) -> bool:
    """Check if a feature is allowed in the current tier."""
    lic = load_license()
    tier = lic.get("tier", "trial")
    return bool(TIERS.get(tier, {}).get("features", {}).get(feature, False))


def get_max_parallel() -> int:
    """Max parallel workers allowed by current tier."""
    lic = load_license()
    tier = lic.get("tier", "trial")
    return int(TIERS.get(tier, {}).get("max_parallel", 1))


def tier_caps_diff(from_tier: str = "trial", to_tier: str = "pro") -> dict:
    """Diff features between two tiers (used by activate UX)."""
    src = TIERS.get(from_tier, {})
    dst = TIERS.get(to_tier, {})
    src_features = {k for k, v in (src.get("features") or {}).items() if v}
    dst_features = {k for k, v in (dst.get("features") or {}).items() if v}
    return {
        "from": from_tier,
        "to": to_tier,
        "removed_features": sorted(src_features - dst_features),
        "added_features": sorted(dst_features - src_features),
        "parallel_delta": (dst.get("max_parallel", 0) - src.get("max_parallel", 0)),
    }


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="DARIO License Manager (simplified)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--status", action="store_true")
    g.add_argument("--check", action="store_true")
    g.add_argument("--init-trial", action="store_true")
    g.add_argument("--activate", metavar="KEY")
    g.add_argument("--generate-key", nargs=2, metavar=("TIER", "EMAIL"))
    ap.add_argument("--force", action="store_true",
                    help="With --init-trial: re-init even if license exists")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.status:
        result = {"license": load_license(), "tiers": list(TIERS.keys()),
                  "machine_id": _machine_id(), "server_enabled": server_enabled()}
    elif args.check:
        result = check_license()
        if args.json:
            print(json.dumps(result))
        else:
            print(f"valid={result['valid']} tier={result.get('tier', '?')} "
                  f"days_remaining={result.get('days_remaining', '?')}")
        return 0 if result["valid"] else 1
    elif args.init_trial:
        result = init_trial(force=args.force)
    elif args.activate:
        result = activate_key(args.activate)
    elif args.generate_key:
        tier, email = args.generate_key
        result = {"key": generate_key(tier, email)}

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
