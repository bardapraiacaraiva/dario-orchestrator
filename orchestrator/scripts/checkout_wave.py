"""
checkout_wave.py — Atomic checkout for autopilot wave.
Marks specified task IDs as in_progress in BOTH the SQLite DB and the
matching YAML file in tasks/active/. Logs audit entries.
"""
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

ORCH = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH))

from core.task_store import TaskStore

WAVE = ["CUI-001", "CUI-002", "CUI-003"]
NOW = datetime.now(UTC).isoformat()

ts = TaskStore()

for tid in WAVE:
    task = ts.get(tid)
    if not task:
        print(f"[ERR]  {tid} not found")
        continue
    if task.get("status") != "todo":
        print(f"[SKIP] {tid} status={task.get('status')}")
        continue

    ok = ts.update(tid, {
        "status": "in_progress",
        "checked_out_at": NOW,
    })
    print(f"[DB]   {tid} → in_progress (ok={ok})")

    yaml_path = ORCH / "tasks" / "active" / f"{tid}.yaml"
    if yaml_path.exists():
        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        data["status"] = "in_progress"
        data["checked_out_at"] = NOW
        if "notes" not in data or data["notes"] is None:
            data["notes"] = []
        data["notes"].append(f"[{NOW}] Wave 0 checkout — lucas-autopilot pulse")
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)
        print(f"[YAML] {tid} updated")

# Audit log
audit_file = ORCH / "audit" / f"{datetime.now().strftime('%Y-%m-%d')}.yaml"
audit_file.parent.mkdir(parents=True, exist_ok=True)
audit_entries = []
if audit_file.exists():
    with open(audit_file, encoding="utf-8") as f:
        audit_entries = yaml.safe_load(f) or []

audit_entries.append({
    "timestamp": NOW,
    "actor": "lucas-autopilot",
    "action": "wave_dispatched",
    "details": f"Wave 0 (Cuidaí): checked out {', '.join(WAVE)}. State=ACTIVE, max_parallel=3.",
})

with open(audit_file, "w", encoding="utf-8") as f:
    yaml.dump(audit_entries, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
print(f"[AUDIT] logged to {audit_file.name}")
print(f"\nFinal counts: {ts.counts()}")
