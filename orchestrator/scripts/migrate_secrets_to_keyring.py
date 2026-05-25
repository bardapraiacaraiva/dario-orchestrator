#!/usr/bin/env python3
"""Migrate existing file-based secrets into the OS keyring.

Faixa 1 #2 (2026-05-25). One-shot migration tool.

Reads:
  - .master_secret           → keyring "MASTER_SECRET"
  - security/.audit_privkey  → keyring "AUDIT_PRIVKEY_PEM"
  - $ANTHROPIC_API_KEY (env) → keyring "ANTHROPIC_API_KEY" (if set)
  - $DARIO_GH_TOKEN (env)    → keyring "DARIO_GH_TOKEN" (if set)

After migration:
  - Source files renamed to *.migrated-YYYY-MM-DD (NOT deleted — manual review)
  - Keyring catalog updated
  - Audit log entry recorded for each migration

Usage:
  python scripts/migrate_secrets_to_keyring.py            # dry run
  python scripts/migrate_secrets_to_keyring.py --apply    # actually migrate
  python scripts/migrate_secrets_to_keyring.py --apply --delete-source  # also delete files

Safety:
  - Default is dry-run
  - --apply renames sources to .migrated-* (recoverable)
  - --delete-source actually removes (NOT recoverable — only after verifying)
  - Aborts if keyring backend unavailable
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from core.secrets import (
    get_secret,
    is_keyring_available,
    get_keyring_backend,
    set_secret,
)


# (env_var, keyring_name, fallback_file_relative_to_orch, description)
MIGRATIONS = [
    ("DARIO_MASTER_SECRET", "MASTER_SECRET", ".master_secret", "HMAC key for license signing"),
    (None,                  "AUDIT_PRIVKEY_PEM", "security/.audit_privkey", "Ed25519 audit signing key (PEM)"),
    ("ANTHROPIC_API_KEY",   "ANTHROPIC_API_KEY", None, "Anthropic Claude API key"),
    ("DARIO_GH_TOKEN",      "DARIO_GH_TOKEN", None, "GitHub PAT for VIP repo access"),
]


def _read_existing(env_var: str | None, fallback_file: str | None) -> tuple[str | None, str]:
    """Return (value, source_description). Value None if not found."""
    if env_var:
        v = os.environ.get(env_var)
        if v:
            return v, f"env:{env_var}"
    if fallback_file:
        p = ORCH_DIR / fallback_file
        if p.exists():
            content = p.read_text(encoding="utf-8").strip()
            if content:
                return content, f"file:{p}"
    return None, "(not found)"


def main():
    p = argparse.ArgumentParser(description="Migrate secrets to keyring (Faixa 1 #2)")
    p.add_argument("--apply", action="store_true", help="actually migrate (default: dry-run)")
    p.add_argument("--delete-source", action="store_true",
                   help="DELETE source files after migration (NOT recoverable)")
    p.add_argument("--force", action="store_true", help="overwrite existing keyring entries")
    args = p.parse_args()

    print("═══════════════════════════════════════════════════════")
    print(f" DARIO Secrets Migration — {datetime.now(UTC).isoformat()}")
    print("═══════════════════════════════════════════════════════")
    print(f" Backend:  {get_keyring_backend()}")
    print(f" Mode:     {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f" Delete:   {'YES' if args.delete_source else 'NO (rename to .migrated-*)'}")
    print()

    if not is_keyring_available():
        print("ABORT: keyring backend not available.")
        return 1

    today_tag = datetime.now(UTC).strftime("%Y-%m-%d")

    migrated = 0
    skipped = 0

    for env_var, keyring_name, fallback_file, desc in MIGRATIONS:
        print(f"── {keyring_name} ({desc})")
        existing_in_keyring = get_secret(keyring_name, caller="migrator")
        if existing_in_keyring and not args.force:
            print(f"   SKIP: already in keyring (use --force to overwrite)")
            skipped += 1
            continue

        value, source = _read_existing(env_var, fallback_file)
        if value is None:
            print(f"   SKIP: {source}")
            skipped += 1
            continue

        print(f"   Found in {source} ({len(value)} chars)")

        if not args.apply:
            print(f"   [dry-run] would store in keyring")
            continue

        set_secret(keyring_name, value, caller="migrator")
        print(f"   ✓ Stored in keyring")
        migrated += 1

        # Handle source file
        if fallback_file:
            source_path = ORCH_DIR / fallback_file
            if source_path.exists():
                if args.delete_source:
                    source_path.unlink()
                    print(f"   ✓ Deleted source file: {source_path}")
                else:
                    archived = source_path.with_suffix(source_path.suffix + f".migrated-{today_tag}")
                    source_path.rename(archived)
                    print(f"   ✓ Renamed source: {archived.name}")

    print()
    print("═══════════════════════════════════════════════════════")
    print(f" Migrated:  {migrated}")
    print(f" Skipped:   {skipped}")
    print(f" Total:     {len(MIGRATIONS)}")

    if not args.apply:
        print()
        print("This was a dry-run. Re-run with --apply to actually migrate.")
    else:
        print()
        print("Verify with: python core/secrets.py list")
        print("Roll back:   restore the .migrated-* files, then `secrets.py delete <name>`")

    return 0


if __name__ == "__main__":
    sys.exit(main())
