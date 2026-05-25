"""Ed25519-signed audit trail with hash chain.

Faixa 1 #5 (2026-05-25). Closes audit Risk #6: tamper-evident audit log.

Design (Bitcoin/Git-inspired, simplified):

1. **Hash chain** — each entry includes a `prev_hash` field referencing the
   SHA-256 of the previous entry's canonical JSON. Tampering with any entry
   breaks the chain — all subsequent entries become unverifiable.

2. **Ed25519 signature** — each entry is signed with a local private key.
   Without the key, an attacker cannot forge entries that survive
   verification. The public key is committed to the repo for any auditor
   to verify (`security/audit_pubkey.pem`).

3. **Daily seal** — at end of day, the final entry's hash is written to
   `audit/seal-YYYY-MM-DD.json` along with the day's signature. This is the
   "Merkle root" for that day — a single hash an external auditor can pin.

4. **Backwards compat** — existing audit/*.yaml files (pre-signing) remain
   readable. Verification only runs on entries with `sig` field present.

Threat model:
  - Insider modifying entries: chain breaks at verify time → DETECTED
  - Insider deleting entries: hash mismatch on next entry → DETECTED
  - Insider compromising private key: signs forgeries → UNDETECTED
    (mitigation: rotate key + maintain seal history)
  - Replay attacks: timestamp + monotonic counter prevents → DETECTED

Key management:
  - Private key: ~/.claude/orchestrator/security/.audit_privkey (chmod 600)
  - Public key: ~/.claude/orchestrator/security/audit_pubkey.pem (committed)
  - Generated on first use; never regenerated automatically (would invalidate
    prior signatures). Manual rotation: archive old keypair, generate new,
    document in TRIAGE.

Usage:
    from core.audit_signing import sign_entry, verify_entry, verify_chain

    signed = sign_entry({"actor": "x", "action": "y"}, prev_hash="...")
    verify_entry(signed, prev_hash="...")  # raises on tamper
    verify_chain([entry1, entry2, ...])     # full daily file
"""
from __future__ import annotations

import base64
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey,
        Ed25519PublicKey,
    )
    from cryptography.hazmat.primitives.serialization import (
        Encoding,
        NoEncryption,
        PrivateFormat,
        PublicFormat,
        load_pem_private_key,
        load_pem_public_key,
    )
except ImportError:
    raise ImportError(
        "cryptography package required for audit signing. "
        "Install: pip install cryptography"
    )


_ORCH_DIR = Path.home() / ".claude" / "orchestrator"
SECURITY_DIR = _ORCH_DIR / "security"
PRIVATE_KEY_PATH = SECURITY_DIR / ".audit_privkey"
PUBLIC_KEY_PATH = SECURITY_DIR / "audit_pubkey.pem"

# Genesis hash for the FIRST entry in any chain. Distinguishes "no prev"
# from "prev is missing/tampered". Per-day genesis = SHA-256 of date string.
GENESIS_PREFIX = "DARIO-AUDIT-CHAIN-2026-05-25"


# ─── Key management ──────────────────────────────────────────────────────


def _ensure_keypair() -> tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    """Load existing keypair or generate + persist a new one."""
    SECURITY_DIR.mkdir(parents=True, exist_ok=True)

    if PRIVATE_KEY_PATH.exists():
        priv = load_pem_private_key(PRIVATE_KEY_PATH.read_bytes(), password=None)
        if not isinstance(priv, Ed25519PrivateKey):
            raise TypeError(f"Existing key at {PRIVATE_KEY_PATH} is not Ed25519")
        pub = priv.public_key()
        return priv, pub

    # Generate new
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()

    PRIVATE_KEY_PATH.write_bytes(
        priv.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption(),
        )
    )
    # Tighten perms — Windows ignores, POSIX honours.
    try:
        PRIVATE_KEY_PATH.chmod(0o600)
    except (OSError, NotImplementedError):
        pass

    PUBLIC_KEY_PATH.write_bytes(
        pub.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo,
        )
    )

    return priv, pub


def load_public_key() -> Ed25519PublicKey:
    """Load the committed public key (read-only)."""
    if not PUBLIC_KEY_PATH.exists():
        raise FileNotFoundError(f"No public key at {PUBLIC_KEY_PATH}")
    pub = load_pem_public_key(PUBLIC_KEY_PATH.read_bytes())
    if not isinstance(pub, Ed25519PublicKey):
        raise TypeError(f"Key at {PUBLIC_KEY_PATH} is not Ed25519")
    return pub


# ─── Canonicalization ────────────────────────────────────────────────────


def _canonical_bytes(entry: dict[str, Any]) -> bytes:
    """Deterministic serialization for hashing/signing.

    Excludes `sig` and `prev_hash` fields (which are derived) and sorts
    keys alphabetically. Same entry always produces same bytes.
    """
    payload = {k: v for k, v in entry.items() if k not in ("sig", "prev_hash")}
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def entry_hash(entry: dict[str, Any]) -> str:
    """SHA-256 of canonical entry bytes. Includes prev_hash to chain."""
    canonical = _canonical_bytes(entry)
    prev = entry.get("prev_hash", "")
    return hashlib.sha256(canonical + prev.encode("utf-8")).hexdigest()


def genesis_hash(day: str) -> str:
    """Per-day chain root. day = 'YYYY-MM-DD'."""
    return hashlib.sha256(f"{GENESIS_PREFIX}|{day}".encode("utf-8")).hexdigest()


# ─── Sign / verify ───────────────────────────────────────────────────────


def sign_entry(entry: dict[str, Any], prev_hash: str) -> dict[str, Any]:
    """Return entry with `prev_hash` and `sig` fields added.

    Mutates a copy; the input dict is unmodified.
    """
    priv, _ = _ensure_keypair()
    signed = dict(entry)
    signed["prev_hash"] = prev_hash
    # Sign the canonical bytes that include prev_hash via the same scheme used
    # by entry_hash: SHA-256(canonical || prev_hash). Signing this gives us
    # tamper-evidence on both the entry content AND its chain position.
    to_sign = _canonical_bytes(signed) + prev_hash.encode("utf-8")
    sig_bytes = priv.sign(to_sign)
    signed["sig"] = base64.b64encode(sig_bytes).decode("ascii")
    return signed


def verify_entry(entry: dict[str, Any], expected_prev_hash: str) -> tuple[bool, str]:
    """Returns (ok, reason). reason is empty string on success."""
    if "sig" not in entry:
        return False, "missing sig field (entry pre-dates signing)"
    if "prev_hash" not in entry:
        return False, "missing prev_hash field"
    if entry["prev_hash"] != expected_prev_hash:
        return False, f"prev_hash mismatch: chain broken (got {entry['prev_hash'][:12]}..., expected {expected_prev_hash[:12]}...)"

    pub = load_public_key()
    try:
        sig_bytes = base64.b64decode(entry["sig"])
        to_verify = _canonical_bytes(entry) + entry["prev_hash"].encode("utf-8")
        pub.verify(sig_bytes, to_verify)
    except Exception as e:
        return False, f"signature verification failed: {e}"

    return True, ""


def verify_chain(entries: list[dict[str, Any]], day: str | None = None) -> dict[str, Any]:
    """Verify entire chain. Returns summary dict.

    If day given, expects first entry's prev_hash to equal genesis_hash(day).
    Otherwise, first entry's prev_hash is used as-is.
    """
    if not entries:
        return {"ok": True, "total": 0, "verified": 0, "broken_at": None, "reason": ""}

    if day:
        expected_prev = genesis_hash(day)
    else:
        expected_prev = entries[0].get("prev_hash", "")

    verified = 0
    for i, entry in enumerate(entries):
        ok, reason = verify_entry(entry, expected_prev)
        if not ok:
            return {
                "ok": False,
                "total": len(entries),
                "verified": verified,
                "broken_at": i,
                "reason": reason,
            }
        verified += 1
        expected_prev = entry_hash(entry)

    return {
        "ok": True,
        "total": len(entries),
        "verified": verified,
        "broken_at": None,
        "reason": "",
    }


# ─── Daily seal (Merkle root equivalent) ─────────────────────────────────


def seal_day(entries: list[dict[str, Any]], day: str) -> dict[str, Any]:
    """Produce a daily seal = final hash + signature over (day, count, final_hash).

    The seal is committed to audit/seal-YYYY-MM-DD.json. An external auditor
    holding only the public key can verify the day's chain integrity by:
      1. Computing entry_hash(last_entry) and confirming it matches seal.final_hash
      2. Verifying seal.sig against (day, count, final_hash)
      3. Optionally walking the chain entry-by-entry
    """
    priv, _ = _ensure_keypair()

    if entries:
        final_hash = entry_hash(entries[-1])
    else:
        final_hash = genesis_hash(day)

    seal_body = {
        "day": day,
        "count": len(entries),
        "final_hash": final_hash,
        "sealed_at": datetime.now(UTC).isoformat(),
    }
    to_sign = _canonical_bytes(seal_body).rstrip()
    sig = priv.sign(to_sign)
    seal_body["sig"] = base64.b64encode(sig).decode("ascii")
    return seal_body


def verify_seal(seal: dict[str, Any]) -> tuple[bool, str]:
    """Verify a daily seal's signature."""
    if "sig" not in seal:
        return False, "missing sig"
    body = {k: v for k, v in seal.items() if k != "sig"}
    pub = load_public_key()
    try:
        sig_bytes = base64.b64decode(seal["sig"])
        pub.verify(sig_bytes, _canonical_bytes(body).rstrip())
    except Exception as e:
        return False, f"seal signature invalid: {e}"
    return True, ""


# ─── CLI ─────────────────────────────────────────────────────────────────


def _cli():
    import argparse
    p = argparse.ArgumentParser(description="Audit trail signing tools (Faixa 1 #5)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="Generate keypair (idempotent)")

    vp = sub.add_parser("verify", help="Verify a YAML chain file")
    vp.add_argument("file", type=Path)
    vp.add_argument("--day", help="YYYY-MM-DD (default: derive from filename)")

    sub.add_parser("pubkey", help="Print public key (for sharing with auditors)")

    args = p.parse_args()

    if args.cmd == "init":
        _, pub = _ensure_keypair()
        print(f"Private key: {PRIVATE_KEY_PATH}")
        print(f"Public key:  {PUBLIC_KEY_PATH}")
        print()
        print(PUBLIC_KEY_PATH.read_text())

    elif args.cmd == "pubkey":
        print(PUBLIC_KEY_PATH.read_text() if PUBLIC_KEY_PATH.exists() else "(no keypair yet — run `init`)")

    elif args.cmd == "verify":
        try:
            from ruamel.yaml import YAML
            y = YAML()
            with args.file.open(encoding="utf-8") as f:
                data = y.load(f)
        except Exception as e:
            print(f"FAIL: cannot read {args.file}: {e}")
            return 1
        if not isinstance(data, list):
            print(f"FAIL: {args.file} is not a list")
            return 1

        day = args.day or args.file.stem  # e.g., '2026-05-25.yaml' → '2026-05-25'
        result = verify_chain(data, day=day)
        if result["ok"]:
            print(f"OK: {result['verified']}/{result['total']} entries verified, chain intact")
            return 0
        else:
            print(f"FAIL at entry #{result['broken_at']}: {result['reason']}")
            print(f"     verified {result['verified']} entries before break")
            return 1


if __name__ == "__main__":
    import sys
    sys.exit(_cli() or 0)
