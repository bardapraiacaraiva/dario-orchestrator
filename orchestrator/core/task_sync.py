"""Surgical YAML -> DB sync for task files.

Closes the interactive-path gap (2026-06-12 self-audit, finding #12 residue):
the /dario-orchestrator skill and session tools write task YAML to
tasks/active|done/ without touching SQLite -- the exact writer pattern that
reopened the DB<->YAML divergence (61 invisible tasks reconciled in bulk by
scripts/backfill_yaml_tasks_to_db.py). This module is the per-file,
idempotent version meant to be called right after any YAML write:

    orch tasks sync <file.yaml>     # one file
    orch tasks sync --all           # every YAML in active/ + done/

Status is preserved on insert (db.create_task forces status='todo', so we
INSERT directly, same technique as the backfill).
"""

import json
import sys
from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
if str(ORCH_DIR) not in sys.path:
    sys.path.insert(0, str(ORCH_DIR))

# Same projection the backfill used: every column that exists in both the
# task YAML schema and the tasks table.
COLUMNS = [
    "id", "title", "description", "project", "skill", "priority", "status",
    "assignee", "execution_policy", "depends_on", "estimated_tokens",
    "actual_tokens", "quality_score", "completion_comment", "parent",
    "dispatch_reason", "blocked_reason", "created_at", "updated_at",
    "assigned_at", "checked_out_at", "completed_at",
]


def _row_from_yaml(task: dict) -> dict:
    row = {}
    for col in COLUMNS:
        v = task.get(col)
        if col == "depends_on" and isinstance(v, list):
            v = json.dumps(v)
        row[col] = v
    return row


def sync_file(path: Path, db=None) -> tuple[str, str]:
    """Upsert one task YAML into the DB.

    Returns (outcome, detail) where outcome is one of:
    inserted | updated | unchanged | skipped
    """
    try:
        task = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except Exception as e:
        return "skipped", f"parse error: {e}"
    if not isinstance(task, dict) or not task.get("id") or not task.get("title"):
        return "skipped", "not a task yaml (missing id/title)"

    if db is None:
        from core.db import DB
        db = DB()

    row = _row_from_yaml(task)
    task_id = row["id"]

    with db._conn() as conn:
        existing = conn.execute(
            f"SELECT {', '.join(COLUMNS)} FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

    if existing is None:
        with db._conn() as conn:
            conn.execute(
                f"INSERT OR IGNORE INTO tasks ({', '.join(COLUMNS)}) "
                f"VALUES ({', '.join('?' * len(COLUMNS))})",
                [row[c] for c in COLUMNS],
            )
            conn.execute(
                "INSERT INTO audit (timestamp, actor, action, details) "
                "VALUES (datetime('now'), ?, ?, ?)",
                ("task_sync", "task_inserted", f"{task_id} synced YAML->DB"),
            )
        return "inserted", f"{task_id} [{row['status']}]"

    current = dict(zip(COLUMNS, existing))
    # created_at is identity, not state -- never overwrite it on update.
    diff = {
        k: row[k]
        for k in COLUMNS
        if k not in ("id", "created_at") and row[k] is not None and row[k] != current[k]
    }
    if not diff:
        return "unchanged", task_id

    db.update_task(task_id, diff)  # whitelisted columns only
    with db._conn() as conn:
        conn.execute(
            "INSERT INTO audit (timestamp, actor, action, details) "
            "VALUES (datetime('now'), ?, ?, ?)",
            ("task_sync", "task_updated", f"{task_id} fields: {sorted(diff)}"),
        )
    return "updated", f"{task_id} {sorted(diff)}"


def sync_all() -> dict:
    """Sync every YAML in tasks/active/ and tasks/done/. Returns counts."""
    from core.db import DB
    db = DB()
    counts = {"inserted": 0, "updated": 0, "unchanged": 0, "skipped": 0}
    for sub in ("active", "done"):
        d = ORCH_DIR / "tasks" / sub
        if not d.exists():
            continue
        for f in sorted(d.glob("*.yaml")):
            outcome, _ = sync_file(f, db=db)
            counts[outcome] += 1
    return counts


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sync task YAML file(s) into the DB")
    parser.add_argument("path", nargs="?", help="task yaml file")
    parser.add_argument("--all", action="store_true", help="sync tasks/active + tasks/done")
    args = parser.parse_args()

    if args.all:
        print(json.dumps(sync_all()))
    elif args.path:
        outcome, detail = sync_file(Path(args.path))
        print(f"{outcome}: {detail}")
        sys.exit(0 if outcome != "skipped" else 1)
    else:
        parser.print_help()
        sys.exit(1)
