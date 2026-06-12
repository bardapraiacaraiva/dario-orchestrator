#!/usr/bin/env python3
"""One-shot backfill: insert YAML-only tasks into the SQLite DB.

The 2026-06-01 fix made readers DB-first but left writers (orch, session
skills) writing YAML only — by 2026-06-12 there were 61 tasks invisible to
every DB-first reader (dispatch, budget, dashboard). This copies them in with
their REAL status/tokens/timestamps (db.create_task forces status='todo', so
we INSERT directly).

Usage:
  python scripts/backfill_yaml_tasks_to_db.py --dry-run
  python scripts/backfill_yaml_tasks_to_db.py
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
if str(ORCH_DIR) not in sys.path:
    sys.path.insert(0, str(ORCH_DIR))

COLUMNS = [
    "id", "title", "description", "project", "skill", "priority", "status",
    "assignee", "execution_policy", "depends_on", "estimated_tokens",
    "actual_tokens", "quality_score", "completion_comment", "parent",
    "dispatch_reason", "blocked_reason", "created_at", "updated_at",
    "assigned_at", "checked_out_at", "completed_at",
]


def load_yaml_tasks() -> list[dict]:
    tasks = []
    for sub in ("active", "done"):
        d = ORCH_DIR / "tasks" / sub
        if not d.exists():
            continue
        for f in sorted(d.glob("*.yaml")):
            try:
                t = yaml.safe_load(f.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"  SKIP {f.name}: parse error {e}")
                continue
            if isinstance(t, dict) and t.get("id") and t.get("title"):
                tasks.append(t)
    return tasks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    from core.db import DB
    db = DB()
    with db._conn() as conn:
        existing = {r[0] for r in conn.execute("SELECT id FROM tasks").fetchall()}

    yaml_tasks = load_yaml_tasks()
    missing = [t for t in yaml_tasks if t["id"] not in existing]
    print(f"YAML tasks: {len(yaml_tasks)} | already in DB: {len(yaml_tasks) - len(missing)} | to backfill: {len(missing)}")

    inserted = 0
    for t in missing:
        row = {}
        for col in COLUMNS:
            v = t.get(col)
            if col == "depends_on" and isinstance(v, list):
                v = json.dumps(v)
            row[col] = v
        if args.dry_run:
            print(f"  WOULD INSERT {row['id']} [{row['status']}] {str(row['title'])[:60]}")
            continue
        with db._conn() as conn:
            conn.execute(
                f"INSERT OR IGNORE INTO tasks ({', '.join(COLUMNS)}) VALUES ({', '.join('?' * len(COLUMNS))})",
                [row[c] for c in COLUMNS],
            )
        inserted += 1
        print(f"  INSERTED {row['id']} [{row['status']}]")

    if not args.dry_run and inserted:
        with db._conn() as conn:
            conn.execute(
                "INSERT INTO audit (timestamp, actor, action, details) VALUES (datetime('now'), ?, ?, ?)",
                ("backfill_yaml_tasks_to_db", "backfill",
                 f"{inserted} YAML-only tasks inserted into DB (audit 2026-06-12 Onda 2)"),
            )
    print(f"Done: {inserted} inserted" if not args.dry_run else "Dry-run only — nothing written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
