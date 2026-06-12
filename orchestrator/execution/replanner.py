#!/usr/bin/env python3
"""
DARIO Replanner — Dynamic re-planning on task failure.
=======================================================
When a task fails, don't stop the pipeline. Auto-reroute:
1. Check fallback_matrix for alternative skill/worker
2. Retry with different worker (sibling)
3. Decompose into smaller subtasks
4. Only escalate to human if all recovery paths exhausted

Usage:
    python replanner.py --task MNB-002 --failure "agent_timeout"
    python replanner.py --task MNB-002 --failure "quality_below_50" --score 42
    python replanner.py --task MNB-002 --failure "skill_not_found"
    python replanner.py --json

Exit codes:
    0 = recovery plan created (task rerouted or retried)
    1 = error
    2 = escalation required (no automatic recovery possible)
"""

import argparse
import json
import logging
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))  # script-mode runs need core.db importable

try:
    from ruamel.yaml import YAML
    yaml_engine = YAML()
    yaml_engine.preserve_quotes = True
    yaml_engine.width = 200
    def load_yaml(path):
        with open(path, encoding='utf-8') as f:
            return yaml_engine.load(f)
    def dump_yaml(data, path):
        with open(path, 'w', encoding='utf-8') as f:
            yaml_engine.dump(data, f)
except ImportError:
    import yaml
    def load_yaml(path):
        with open(path, encoding='utf-8') as f:
            return yaml.safe_load(f)
    def dump_yaml(data, path):
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


TASKS_DIR = ORCH_DIR / "tasks" / "active"
FALLBACK_FILE = ORCH_DIR / "fallback_matrix.yaml"
COMPANY_FILE = ORCH_DIR / "company.yaml"

# Max retries before escalation
MAX_RETRIES = 2

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("replanner")


FAILURE_STRATEGIES = {
    "agent_timeout": ["retry_same", "retry_sibling", "escalate"],
    "quality_below_50": ["retry_with_feedback", "retry_sibling", "escalate"],
    "skill_not_found": ["fallback_skill", "escalate"],
    "worker_busy": ["retry_sibling", "queue_for_next_pulse"],
    "budget_exceeded": ["escalate"],
    "dependency_failed": ["unblock_alternate", "escalate"],
    "parse_error": ["retry_same", "escalate"],
    "unknown": ["retry_same", "retry_sibling", "escalate"],
}


# ─── Persistence: DB-first with YAML mirror (DD finding A8, 2026-06-12) ─────
# The replanner was the last YAML-only task writer. Convention since Onda 2:
# SQLite (core/db.py) is the authority, tasks/active/*.yaml is a mirror kept
# for session tools. Every mutation must hit BOTH or the db_yaml_divergence
# tripwire reopens.

# DB columns the replanner mutates. revision_count / notes / watchers have no
# DB column (schema gap) — they live only in the YAML mirror, by design.
_DB_AUTHORITATIVE_COLUMNS = (
    "status", "assignee", "skill", "priority", "dispatch_reason", "blocked_reason",
)

_DB = None  # cached handle; tests inject a tmp-path DB here. False = unavailable.


def _get_db():
    global _DB
    if _DB is None:
        try:
            from core.db import DB
            _DB = DB()
        except Exception as e:  # degraded mode: YAML-only, same as orch CLI
            log.warning(f"DB unavailable ({e}) — YAML-only mode, run backfill to reconcile")
            _DB = False
    return _DB or None


def _db_fields(data: dict) -> dict:
    """Project a task dict onto DB-writable columns (JSON-encode containers)."""
    try:
        from core.db import ALLOWED_TASK_COLUMNS as allowed
    except Exception:
        allowed = set(_DB_AUTHORITATIVE_COLUMNS)
    out = {}
    for k, v in data.items():
        if k in allowed:
            out[k] = json.dumps(list(v) if isinstance(v, (list, tuple)) else dict(v)) \
                if isinstance(v, (list, tuple, dict)) else v
    return out


def load_task(task_id: str) -> dict:
    """DB-first read, merged over the YAML mirror.

    YAML keeps the rich fields the DB schema lacks (revision_count, notes,
    watchers); the DB overrides the columns it owns. YAML-only tasks (legacy)
    still load — save_task() heals them into the DB.
    """
    yaml_task = None
    task_file = TASKS_DIR / f"{task_id}.yaml"
    if task_file.exists():
        yaml_task = load_yaml(str(task_file))

    db_task = None
    db = _get_db()
    if db:
        try:
            db_task = db.get_task(task_id)
        except Exception as e:
            log.warning(f"DB read failed for {task_id} ({e}) — falling back to YAML")

    if db_task and isinstance(yaml_task, dict):
        for col in _DB_AUTHORITATIVE_COLUMNS:
            if col in db_task:
                yaml_task[col] = db_task[col]
        return yaml_task
    if db_task:
        return dict(db_task)
    return yaml_task if isinstance(yaml_task, dict) else None


def save_task(task_id: str, data: dict, dry_run: bool = False):
    """Dual-write: DB (authority) + YAML mirror, in the same operation."""
    if dry_run:
        log.info(f"[dry-run] {task_id}: skipping DB + YAML write")
        return

    db = _get_db()
    if db:
        try:
            fields = _db_fields(data)
            if not db.update_task(task_id, fields):
                # Legacy YAML-only task: create the row so DB-first readers
                # (dispatch/budget/dashboard) see it, then apply the mutation
                # (create_task forces status='todo').
                db.create_task({
                    "id": task_id,
                    "title": data.get("title") or task_id,
                    "description": data.get("description", ""),
                    "project": data.get("project", ""),
                    "skill": data.get("skill") or "",
                    "priority": data.get("priority", "medium"),
                    "assignee": data.get("assignee"),
                    "execution_policy": data.get("execution_policy", "default"),
                    "depends_on": data.get("depends_on") or [],
                    "estimated_tokens": data.get("estimated_tokens") or 0,
                    "parent": data.get("parent"),
                })
                if fields:
                    db.update_task(task_id, fields)
        except Exception as e:
            log.warning(f"DB write failed for {task_id} ({e}) — YAML-only, run backfill to reconcile")

    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    dump_yaml(data, str(TASKS_DIR / f"{task_id}.yaml"))


def get_fallback_skill(skill: str) -> str:
    """Check fallback_matrix for alternative skill."""
    if not FALLBACK_FILE.exists():
        return None
    matrix = load_yaml(str(FALLBACK_FILE))
    if not isinstance(matrix, dict):
        return None
    # Look for skill in matrix
    for entry in matrix.get("fallbacks", []):
        if isinstance(entry, dict) and entry.get("primary") == skill:
            return entry.get("fallback")
    return None


def get_sibling_worker(worker_id: str, skill: str) -> str:
    """Find a sibling worker that could handle the same skill."""
    if not COMPANY_FILE.exists():
        return None
    company = load_yaml(str(COMPANY_FILE))
    workers = company.get("workers", {})

    # Find current worker's director
    current = workers.get(worker_id, {})
    if not isinstance(current, dict):
        return None
    director = current.get("reports_to", "")

    # Find siblings under same director
    for wid, wdata in workers.items():
        if wid == worker_id:
            continue
        if not isinstance(wdata, dict):
            continue
        if wdata.get("reports_to") == director:
            # Check capability overlap
            caps = wdata.get("capabilities", [])
            if isinstance(caps, list) and skill in str(caps):
                return wid
    return None


def replan(task_id: str, failure_type: str, score: int = 0,
           error_msg: str = "", dry_run: bool = False) -> dict:
    """Create a recovery plan for a failed task.

    dry_run=True computes the plan without persisting (no DB, no YAML).
    """
    result = {
        "task_id": task_id,
        "failure": failure_type,
        "action": "escalate",
        "details": "",
        "applied": False,
        "dry_run": dry_run,
    }

    task = load_task(task_id)
    if not task:
        result["details"] = "Task not found"
        return result

    retry_count = int(task.get("revision_count", 0) or 0)
    skill = task.get("skill", "")
    worker = task.get("assignee", "")

    strategies = FAILURE_STRATEGIES.get(failure_type, FAILURE_STRATEGIES["unknown"])

    for strategy in strategies:
        if strategy == "retry_same" and retry_count < MAX_RETRIES:
            # Retry with same worker
            task["status"] = "todo"
            task["revision_count"] = retry_count + 1
            task["notes"] = task.get("notes") or []
            if isinstance(task["notes"], list):
                task["notes"].append(f"REPLAN: retry #{retry_count+1} after {failure_type}")
            save_task(task_id, task, dry_run=dry_run)
            result["action"] = "retry_same"
            result["details"] = f"Retry #{retry_count+1} with {worker}"
            result["applied"] = not dry_run
            return result

        elif strategy == "retry_with_feedback" and retry_count < MAX_RETRIES:
            # Retry with quality feedback injected
            task["status"] = "todo"
            task["revision_count"] = retry_count + 1
            task["notes"] = task.get("notes") or []
            if isinstance(task["notes"], list):
                task["notes"].append(
                    f"REPLAN: retry with feedback. Score was {score}. "
                    f"Improve specificity and accuracy. {error_msg}"
                )
            save_task(task_id, task, dry_run=dry_run)
            result["action"] = "retry_with_feedback"
            result["details"] = f"Retry with quality feedback (score was {score})"
            result["applied"] = not dry_run
            return result

        elif strategy == "retry_sibling":
            sibling = get_sibling_worker(worker, skill)
            if sibling:
                task["status"] = "todo"
                task["assignee"] = sibling
                task["dispatch_reason"] = f"rerouted from {worker} after {failure_type}"
                task["notes"] = task.get("notes") or []
                if isinstance(task["notes"], list):
                    task["notes"].append(f"REPLAN: rerouted to {sibling} (original: {worker})")
                save_task(task_id, task, dry_run=dry_run)
                result["action"] = "retry_sibling"
                result["details"] = f"Rerouted to {sibling}"
                result["applied"] = not dry_run
                return result

        elif strategy == "fallback_skill":
            fallback = get_fallback_skill(skill)
            if fallback:
                task["skill"] = fallback
                task["status"] = "todo"
                task["assignee"] = None  # Let dispatch find worker for new skill
                task["notes"] = task.get("notes") or []
                if isinstance(task["notes"], list):
                    task["notes"].append(f"REPLAN: skill fallback {skill} → {fallback}")
                save_task(task_id, task, dry_run=dry_run)
                result["action"] = "fallback_skill"
                result["details"] = f"Skill changed: {skill} → {fallback}"
                result["applied"] = not dry_run
                return result

        elif strategy == "queue_for_next_pulse":
            task["status"] = "todo"
            task["assignee"] = None
            save_task(task_id, task, dry_run=dry_run)
            result["action"] = "queue_for_next_pulse"
            result["details"] = "Released assignment, will be re-dispatched next pulse"
            result["applied"] = not dry_run
            return result

        elif strategy == "escalate":
            task["status"] = "blocked"
            task["blocked_reason"] = f"Auto-recovery exhausted after {failure_type}. Retries: {retry_count}. Needs human intervention."
            task["watchers"] = task.get("watchers") or []
            if isinstance(task["watchers"], list) and "dario-ceo" not in task["watchers"]:
                task["watchers"].append("dario-ceo")
            save_task(task_id, task, dry_run=dry_run)
            result["action"] = "escalate"
            result["details"] = f"Blocked + escalated to CEO (retries exhausted: {retry_count})"
            result["applied"] = not dry_run
            return result

    return result


def main():
    parser = argparse.ArgumentParser(description="DARIO Replanner — Auto-recovery on failure")
    parser.add_argument("--task", "-t", required=True, help="Task ID that failed")
    parser.add_argument("--failure", "-f", required=True,
                        help=f"Failure type: {list(FAILURE_STRATEGIES.keys())}")
    parser.add_argument("--score", type=int, default=0, help="Quality score (for quality failures)")
    parser.add_argument("--error", default="", help="Error message")
    parser.add_argument("--dry-run", action="store_true",
                        help="Compute the recovery plan without writing DB/YAML")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.json:
        logging.getLogger().setLevel(logging.ERROR)

    result = replan(args.task, args.failure, args.score, args.error,
                    dry_run=args.dry_run)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        symbol = "+" if result["applied"] and result["action"] != "escalate" else "!"
        print(f"[{symbol}] {args.task}: {result['action']}")
        print(f"    {result['details']}")

    return 0 if result["action"] != "escalate" else 2


if __name__ == "__main__":
    sys.exit(main())
