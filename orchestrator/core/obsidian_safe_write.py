#!/usr/bin/env python3
"""
DARIO Obsidian Safe Write Utility
==================================
Companion utility for any module that writes markdown into the Obsidian vault.

The vault's .obsidian/app.json has:
    "newFileLocation": "folder"
    "newFileFolderPath": "00 - Inbox"

This makes Obsidian create empty shadow copies under "00 - Inbox/" whenever
a file appears in the vault from outside Obsidian (Python writes, etc.).
The shadows mirror the destination folder path (sometimes with "<name> 1.md"
auto-rename suffixes) and have size 0.

Call `safe_write_obsidian(path, content)` from any module instead of
`path.write_text(content)`. It writes the file AND removes shadow copies.

Or call `cleanup_inbox_shadows(filename_or_basename)` after a manual write.

CLI:
    python obsidian_safe_write.py --scan          List all empty shadows in vault
    python obsidian_safe_write.py --cleanup       Remove all empty shadows
    python obsidian_safe_write.py --cleanup-name "2026-W21 - Cognitive Weekly"
"""

import argparse
import sys
from pathlib import Path

DEFAULT_VAULT_ROOT = (Path.home() / "OneDrive" / "Documents" / "D.A.R.I.O")
DEFAULT_INBOX_DIRNAME = "00 - Inbox"


def find_vault_root(start: Path) -> Path:
    """Walk up from `start` looking for a `.obsidian` folder. Falls back to default."""
    p = start.resolve()
    for ancestor in [p] + list(p.parents):
        if (ancestor / ".obsidian").exists():
            return ancestor
    return DEFAULT_VAULT_ROOT


def cleanup_inbox_shadows(target_filename: str, vault_root: Path = None) -> int:
    """Remove 0-byte files in 00 - Inbox/ matching target_filename's basename
    (with optional `<name> N.md` auto-rename). Returns count removed.
    """
    vault = vault_root or DEFAULT_VAULT_ROOT
    inbox = vault / DEFAULT_INBOX_DIRNAME
    if not inbox.exists():
        return 0

    base = Path(target_filename).stem  # strip .md
    removed = 0
    for shadow in inbox.rglob("*.md"):
        try:
            if shadow.stat().st_size != 0:
                continue
            stem = shadow.stem
            if stem == base:
                shadow.unlink()
                removed += 1
                continue
            # Match Obsidian auto-rename: "<name> 1", "<name> 2", etc.
            if stem.startswith(base + " "):
                suffix = stem[len(base) + 1:].strip()
                if suffix.isdigit():
                    shadow.unlink()
                    removed += 1
        except Exception:
            continue
    return removed


def cleanup_all_empty_shadows(vault_root: Path = None) -> dict:
    """Find and remove ALL 0-byte files in `00 - Inbox/`. Returns stats."""
    vault = vault_root or DEFAULT_VAULT_ROOT
    inbox = vault / DEFAULT_INBOX_DIRNAME
    if not inbox.exists():
        return {"removed": 0, "found": 0, "files": []}

    files_removed = []
    found = 0
    for shadow in inbox.rglob("*.md"):
        try:
            if shadow.stat().st_size == 0:
                found += 1
                shadow.unlink()
                files_removed.append(str(shadow.relative_to(vault)))
        except Exception:
            continue
    return {"removed": len(files_removed), "found": found, "files": files_removed}


def scan_shadows(vault_root: Path = None) -> list:
    """Return list of empty markdown files in 00 - Inbox/ without removing them."""
    vault = vault_root or DEFAULT_VAULT_ROOT
    inbox = vault / DEFAULT_INBOX_DIRNAME
    if not inbox.exists():
        return []
    out = []
    for shadow in inbox.rglob("*.md"):
        try:
            if shadow.stat().st_size == 0:
                out.append(str(shadow.relative_to(vault)))
        except Exception:
            continue
    return out


def safe_write_obsidian(path: Path, content: str,
                         encoding: str = "utf-8") -> dict:
    """Write `content` to `path` (inside the Obsidian vault), then remove any
    shadow copies in the Inbox that match the filename.

    Returns: {"path": str, "written_bytes": int, "shadows_removed": int}
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding)
    written = path.stat().st_size

    # Determine vault root from the target path
    vault = find_vault_root(path.parent)
    removed = cleanup_inbox_shadows(path.name, vault_root=vault)

    return {
        "path": str(path),
        "written_bytes": written,
        "shadows_removed": removed,
    }


def main():
    p = argparse.ArgumentParser(description="DARIO Obsidian Safe Write Utility")
    p.add_argument("--scan", action="store_true",
                   help="List empty shadows in 00 - Inbox/ (no removal)")
    p.add_argument("--cleanup", action="store_true",
                   help="Remove ALL empty markdown files in 00 - Inbox/")
    p.add_argument("--cleanup-name",
                   help="Remove shadows matching a specific basename")
    p.add_argument("--vault", help="Override vault root path")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    vault = Path(args.vault) if args.vault else None

    if args.scan:
        out = scan_shadows(vault)
        if args.json:
            import json
            print(json.dumps(out, indent=2))
        else:
            print(f"Found {len(out)} empty shadow(s) in inbox:")
            for f in out:
                print(f"  - {f}")
        return 0

    if args.cleanup:
        r = cleanup_all_empty_shadows(vault)
        if args.json:
            import json
            print(json.dumps(r, indent=2))
        else:
            print(f"Removed {r['removed']} empty shadow(s).")
            for f in r["files"]:
                print(f"  - {f}")
        return 0

    if args.cleanup_name:
        count = cleanup_inbox_shadows(args.cleanup_name, vault_root=vault)
        print(f"Removed {count} shadow(s) matching '{args.cleanup_name}'")
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
