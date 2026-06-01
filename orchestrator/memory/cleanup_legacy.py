"""Legacy workflow cleanup — auto-archive unused chains after a grace period.

Criteria (ALL must match):
  - discovered_from == "legacy_chains"
  - use_count == 0
  - workflow file mtime older than GRACE_DAYS (default 30)

Archived workflows are moved to procedural/.archive/ (non-destructive, reversible).

Self-gated by date — safe to call on every run, only acts when threshold reached.

Usage:
    python -m memory.cleanup_legacy             # archive if criteria met
    python -m memory.cleanup_legacy --dry-run
    python -m memory.cleanup_legacy --grace-days 60
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from memory import procedural

GRACE_DAYS_DEFAULT = 30
ARCHIVE_DIR = procedural.PROCEDURAL_DIR / ".archive"


def cleanup(grace_days: int = GRACE_DAYS_DEFAULT, dry_run: bool = False) -> dict:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(UTC).timestamp()
    cutoff = now - (grace_days * 86400)

    candidates = []
    archived = []

    for wf in procedural.list_workflows():
        if wf.discovered_from != "legacy_chains":
            continue
        if wf.use_count > 0:
            continue
        path = procedural.PROCEDURAL_DIR / f"{wf.workflow_id}.yaml"
        if not path.exists():
            continue
        mtime = path.stat().st_mtime
        if mtime > cutoff:
            candidates.append({
                "workflow_id": wf.workflow_id,
                "name": wf.name,
                "age_days": round((now - mtime) / 86400, 1),
                "status": "below_grace",
            })
            continue

        candidates.append({
            "workflow_id": wf.workflow_id,
            "name": wf.name,
            "age_days": round((now - mtime) / 86400, 1),
            "status": "archived" if not dry_run else "would_archive",
        })

        if not dry_run:
            path.rename(ARCHIVE_DIR / path.name)
            archived.append(wf.workflow_id)

    return {
        "grace_days": grace_days,
        "candidates_evaluated": len(candidates),
        "archived": len(archived),
        "archived_ids": archived,
        "details": candidates,
        "dry_run": dry_run,
    }


def main():
    parser = argparse.ArgumentParser(description="Archive unused legacy workflows")
    parser.add_argument("--grace-days", type=int, default=GRACE_DAYS_DEFAULT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = cleanup(grace_days=args.grace_days, dry_run=args.dry_run)

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print(f"\n[LEGACY CLEANUP] grace={args.grace_days}d  dry_run={args.dry_run}")
    print(f"  Candidates evaluated: {result['candidates_evaluated']}")
    print(f"  Archived: {result['archived']}")
    for d in result['details']:
        status_icon = {"archived": "[x]", "would_archive": "[ ]", "below_grace": "[-]"}.get(d["status"], "[?]")
        print(f"    {status_icon} {d['workflow_id']:50s}  age={d['age_days']}d  ({d['status']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
