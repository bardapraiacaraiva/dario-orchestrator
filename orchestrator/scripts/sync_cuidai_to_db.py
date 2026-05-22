"""
sync_cuidai_to_db.py
Imports the 40 CUI-* YAML tasks into the orchestrator SQLite DB so the
state machine can detect pending work and transition EXPANSION → ACTIVE.

Idempotent: skips tasks already present in DB. Sets blocked status correctly.
"""
import sys
from pathlib import Path

import yaml

ORCH = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH))

from db import DB

db = DB()
tasks_dir = ORCH / "tasks" / "active"

inserted = 0
skipped = 0
blocked_updated = 0
failed = []

# Get current DB IDs to skip duplicates
existing_ids = {t["id"] for t in db.get_tasks()}

for yaml_path in sorted(tasks_dir.glob("CUI-*.yaml")):
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data or not data.get("id"):
        failed.append((yaml_path.name, "missing_id"))
        continue

    tid = data["id"]
    if tid in existing_ids:
        skipped += 1
        continue

    try:
        db.create_task(data)
        inserted += 1

        # Update status to 'blocked' if the YAML had blocked_reason
        if data.get("blocked_reason"):
            from task_store import TaskStore
            ts = TaskStore()
            ts.update(tid, {
                "status": "blocked",
                "blocked_reason": data["blocked_reason"],
            })
            blocked_updated += 1
    except Exception as e:
        failed.append((tid, str(e)[:80]))

print("Sync complete:")
print(f"  inserted: {inserted}")
print(f"  skipped (already in DB): {skipped}")
print(f"  blocked status applied: {blocked_updated}")
print(f"  failed: {len(failed)}")
if failed:
    for tid, err in failed[:5]:
        print(f"    {tid}: {err}")

# Final DB state
print("\nDB state after sync:")
print(f"  task_counts: {db.get_task_counts()}")
