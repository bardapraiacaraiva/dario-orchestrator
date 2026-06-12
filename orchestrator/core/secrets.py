"""DARIO Secrets Manager — OS keyring wrapper with audit + namespacing.

Faixa 1 #2 (2026-05-25). Closes audit Risk #2: secret exfiltration.

Backend: Python `keyring` lib → OS-native vault
  - Windows: Credential Manager (DPAPI encrypted, per-user ACL)
  - macOS:   Keychain (encrypted, per-user, biometric optional)
  - Linux:   Secret Service (gnome-keyring, KWallet, etc.)

What it protects against
────────────────────────
- Casual file read attacks (.master_secret was world-readable plain text)
- Compromised skill processes that grep filesystem for secrets (keyring API
  requires explicit get + namespaced; secrets aren't enumerable from outside)
- Accidental git commit of secret files (no files = nothing to commit)
- Bash history leakage (secrets never in command args, only in keyring calls)

What it does NOT protect against
────────────────────────────────
- Skills running with full user privileges CAN still call `secrets.get(...)`
  if they know the name. Real isolation needs per-skill subprocess with
  env scoping (deferred to Faixa 2 — too invasive for v1).
- Skills can call any other Python (no sandboxing — Faixa 1 #1).
- Memory dump while DARIO is running exposes loaded secrets.
- Compromised OS user account = full access (use disk encryption + 2FA).

Threat model deltas vs file-based:
  Before: `cat ~/.claude/orchestrator/.master_secret` → secret printed
  After:  `cat ~/.claude/orchestrator/.master_secret` → file gone
          `python -c "import keyring; print(keyring.get_password('x','y'))"`
            → only works if attacker knows EXACTLY the service + key name
            → still logged via dario.audit if accessed through this wrapper

Usage:
    from core.secrets import set_secret, get_secret, delete_secret, list_secret_names

    set_secret("ANTHROPIC_API_KEY", "sk-ant-...", caller="my-skill")
    api_key = get_secret("ANTHROPIC_API_KEY", caller="my-skill")
    delete_secret("OLD_TOKEN", caller="rotation-script")
    names = list_secret_names()  # names only, never values

Namespacing:
  Every secret is stored under the service "dario-orchestrator". This
  prevents collision with non-DARIO apps using the same keyring.

Migration:
  See `scripts/migrate_secrets_to_keyring.py` for moving .master_secret
  and .audit_privkey out of files into keyring.
"""
from __future__ import annotations

import logging
import os

try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    keyring = None
    KEYRING_AVAILABLE = False


SERVICE_NAME = "dario-orchestrator"
_logger = logging.getLogger(__name__)


# ─── Audit hook ───────────────────────────────────────────────────────────


def _audit(action: str, secret_name: str, caller: str, ok: bool = True) -> None:
    """Log secret access to dario.audit. Fail-soft if audit_logger missing.

    Records: who accessed which secret, when, success/fail. Never logs
    the secret value itself. This lets you answer "what did skill X read
    in the last hour?" — critical for breach forensics.

    Reentrancy guard (Fase 1 fix, 2026-06-12): the audit logger signs every
    event, and signing loads the audit private key via get_secret(
    caller="audit_signing"). Auditing THAT access would recurse
    (get_secret → _audit → log_event → sign_entry → _ensure_keypair →
    get_secret …), which measured ~52s per signature. Reading the audit
    key for the purpose of signing the audit log cannot itself be audited —
    it is circular by definition — so we skip it.
    """
    if caller == "audit_signing":
        return
    try:
        from core.audit_logger import log_event
        log_event(
            actor=caller,
            action=f"secret_{action}",
            entity_type="secret",
            entity_id=secret_name,
            details=f"ok={ok}",
        )
    except Exception:
        # Don't let audit failures block secret operations
        _logger.debug("audit log unavailable for secret %s", action)


# ─── Public API ───────────────────────────────────────────────────────────


def is_keyring_available() -> bool:
    """Returns True if keyring backend is functional.

    Use this to decide whether to fall back to file-based storage.
    """
    if not KEYRING_AVAILABLE:
        return False
    try:
        backend = keyring.get_keyring()
        # FailingKeyring is what keyring returns when no backend works
        return "Failing" not in type(backend).__name__
    except Exception:
        return False


def get_keyring_backend() -> str:
    """Returns the backend class name (e.g. 'WinVaultKeyring')."""
    if not KEYRING_AVAILABLE:
        return "(keyring not installed)"
    try:
        return type(keyring.get_keyring()).__name__
    except Exception as e:
        return f"(error: {e})"


def set_secret(name: str, value: str, caller: str = "unknown") -> None:
    """Store a secret in the OS keyring.

    Args:
        name: identifier (e.g., "ANTHROPIC_API_KEY", "audit_privkey")
        value: secret content (never logged)
        caller: skill/script name for audit trail

    Raises:
        RuntimeError: if keyring backend unavailable
    """
    if not is_keyring_available():
        _audit("set", name, caller, ok=False)
        raise RuntimeError(
            f"Keyring backend not available ({get_keyring_backend()}). "
            "Install keyring + ensure OS vault accessible."
        )
    try:
        keyring.set_password(SERVICE_NAME, name, value)
        _audit("set", name, caller)
        _update_catalog(name, add=True)
    except Exception:
        _audit("set", name, caller, ok=False)
        raise


def get_secret(name: str, caller: str = "unknown",
               fallback_env: str | None = None,
               fallback_file: str | None = None) -> str | None:
    """Retrieve a secret from the keyring.

    Args:
        name: identifier
        caller: skill/script name for audit trail
        fallback_env: env var name to check if keyring returns None
            (back-compat with old env-based code)
        fallback_file: file path to read if keyring + env both empty
            (back-compat with .master_secret-style files)

    Returns:
        Secret value or None if not found in any source.
    """
    value: str | None = None

    if is_keyring_available():
        try:
            value = keyring.get_password(SERVICE_NAME, name)
        except Exception:
            _logger.debug("keyring read failed for %s", name)

    if value is None and fallback_env:
        value = os.environ.get(fallback_env)
        if value:
            _logger.debug("secret %s sourced from env %s (fallback)", name, fallback_env)

    if value is None and fallback_file:
        try:
            from pathlib import Path
            p = Path(fallback_file).expanduser()
            if p.exists():
                value = p.read_text(encoding="utf-8").strip()
                _logger.warning(
                    "secret %s sourced from file %s — consider migrating to keyring",
                    name, fallback_file
                )
        except Exception:
            pass

    _audit("get", name, caller, ok=(value is not None))
    return value


def delete_secret(name: str, caller: str = "unknown") -> bool:
    """Remove a secret from the keyring. Returns True if deleted."""
    if not is_keyring_available():
        _audit("delete", name, caller, ok=False)
        return False
    try:
        keyring.delete_password(SERVICE_NAME, name)
        _audit("delete", name, caller)
        _update_catalog(name, add=False)
        return True
    except keyring.errors.PasswordDeleteError:
        # Not present
        _audit("delete", name, caller, ok=False)
        return False
    except Exception:
        _audit("delete", name, caller, ok=False)
        return False


def list_secret_names() -> list[str]:
    """List names of known secrets. Never returns values.

    Most keyring backends don't natively support enumeration (security
    feature). We maintain a local catalog file under security/ that
    tracks known secret names — updated on set/delete.
    """
    from pathlib import Path
    catalog = Path.home() / ".claude" / "orchestrator" / "security" / "secret_catalog.txt"
    if not catalog.exists():
        return []
    return sorted(set(catalog.read_text(encoding="utf-8").strip().splitlines()))


def _update_catalog(name: str, add: bool = True) -> None:
    """Maintain the catalog file. Best-effort, non-blocking."""
    try:
        from pathlib import Path
        catalog = Path.home() / ".claude" / "orchestrator" / "security" / "secret_catalog.txt"
        catalog.parent.mkdir(parents=True, exist_ok=True)
        existing = set()
        if catalog.exists():
            existing = set(catalog.read_text(encoding="utf-8").strip().splitlines())
        if add:
            existing.add(name)
        else:
            existing.discard(name)
        catalog.write_text("\n".join(sorted(existing)) + "\n", encoding="utf-8")
    except Exception:
        pass


# Catalog maintenance is done inline in the primary set_secret/delete_secret
# above (post-mypy refactor 2026-05-25 — was double-defined which mypy flagged
# as `no-redef`).


# ─── CLI ──────────────────────────────────────────────────────────────────


def _cli() -> int:
    import argparse
    p = argparse.ArgumentParser(description="DARIO Secrets Manager (Faixa 1 #2)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Show keyring backend + catalog count")

    setp = sub.add_parser("set", help="Set a secret (value from stdin if --stdin)")
    setp.add_argument("name")
    setp.add_argument("value", nargs="?", help="value (or omit + use --stdin)")
    setp.add_argument("--stdin", action="store_true", help="read value from stdin (more secure)")
    setp.add_argument("--caller", default="cli")

    getp = sub.add_parser("get", help="Get a secret (prints value — use carefully)")
    getp.add_argument("name")
    getp.add_argument("--caller", default="cli")

    delp = sub.add_parser("delete", help="Delete a secret")
    delp.add_argument("name")
    delp.add_argument("--caller", default="cli")

    sub.add_parser("list", help="List secret names (catalog)")

    args = p.parse_args()

    if args.cmd == "status":
        print(f"Backend:      {get_keyring_backend()}")
        print(f"Available:    {is_keyring_available()}")
        print(f"Service:      {SERVICE_NAME}")
        print(f"Catalog size: {len(list_secret_names())}")

    elif args.cmd == "set":
        value = args.value
        if args.stdin or not value:
            import sys
            value = sys.stdin.read().strip()
        set_secret(args.name, value, caller=args.caller)
        print(f"Stored: {args.name}")

    elif args.cmd == "get":
        value = get_secret(args.name, caller=args.caller)
        if value is None:
            print(f"NOT FOUND: {args.name}")
            return 1
        print(value)

    elif args.cmd == "delete":
        ok = delete_secret(args.name, caller=args.caller)
        print(f"{'Deleted' if ok else 'Not found'}: {args.name}")
        return 0 if ok else 1

    elif args.cmd == "list":
        names = list_secret_names()
        if not names:
            print("(empty catalog)")
            return 0
        for n in names:
            print(n)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(_cli())
