"""One-time migration: read existing taskboard + audit logs and create Episode records.

Two sources:
  1. `~/.claude/orchestrator/tasks/done/*.yaml` — completed task records (rich)
  2. `~/.claude/orchestrator/audit/YYYY-MM-DD.yaml` — audit events (fallback)

The done/ folder is the primary source — it has skill, project, score, tokens,
duration, completion comments. Audit logs are a fallback when done files are missing.

Usage:
    python -m memory.backfill_from_audit            # all done tasks + 30d audit
    python -m memory.backfill_from_audit --days 30
    python -m memory.backfill_from_audit --dry-run
    python -m memory.backfill_from_audit --source done|audit|both
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from memory import episodic
from memory.schemas import Episode, Outcome

AUDIT_DIR = ORCH_DIR / "audit"
DONE_DIR = ORCH_DIR / "tasks" / "done"


def _load_done_tasks() -> list:
    """DB-FIRST (2026-06-01): SQLite is the source of truth (CONVENTIONS.md).

    Previously this only globbed tasks/done/*.yaml, which is empty post-migration
    — so the episodic backfill silently did nothing. Read done tasks from the DB;
    fall back to YAML only when the DB is unavailable.
    """
    try:
        from core.task_store import TaskStore
        tasks = TaskStore().get_all(status="done")
        if tasks:
            return tasks
    except Exception:
        pass
    out = []
    for path in sorted(DONE_DIR.glob("*.yaml")):
        try:
            with open(path, encoding="utf-8") as f:
                t = yaml.safe_load(f) or {}
            if t:
                t.setdefault("id", path.stem)
                out.append(t)
        except Exception:
            continue
    return out


def backfill_from_done(dry_run: bool = False) -> dict:
    """Create one Episode per completed task (DB-first, YAML fallback).

    Idempotent: skips tasks that already have an Episode record.
    """
    written = 0
    skipped = 0
    skipped_existing = 0
    done_tasks = _load_done_tasks()
    for t in done_tasks:
        skill = t.get("skill", "")
        if not skill:
            skipped += 1
            continue

        task_id = t.get("id", "")
        if not task_id:
            skipped += 1
            continue
        if episodic.episode_exists_for_task(task_id):
            skipped_existing += 1
            continue

        timestamp = t.get("completed_at") or t.get("checked_out_at") or t.get("created_at")
        if not timestamp:
            skipped += 1
            continue

        outcome = Outcome.SUCCESS if t.get("status") == "done" else Outcome.FAILURE

        duration = 0.0
        if t.get("checked_out_at") and t.get("completed_at"):
            try:
                start = datetime.fromisoformat(t["checked_out_at"])
                end = datetime.fromisoformat(t["completed_at"])
                duration = (end - start).total_seconds()
            except Exception:
                pass

        ep = Episode(
            episode_id="",
            task_id=task_id,
            timestamp=timestamp,
            agent=t.get("assignee") or "",   # DB rows may have explicit None
            skill=skill,
            outcome=outcome,
            score=t.get("quality_score"),
            duration_seconds=duration,
            tokens_used=t.get("actual_tokens") or 0,
            model="opus",
            project=t.get("project") or "",  # DB rows may have explicit None
            output_summary=(t.get("completion_comment") or t.get("description") or "")[:500],
            tags=t.get("tags", []) if isinstance(t.get("tags"), list) else [],
        )
        if not dry_run:
            episodic.write_episode(ep)
        written += 1

    return {
        "source": "db:done (yaml fallback)",
        "files_processed": len(done_tasks),
        "episodes_written": written,
        "skipped_no_skill": skipped,
        "skipped_already_existed": skipped_existing,
    }

SCORE_RE = re.compile(r"[Ss]core\s+(\d+)")
TOKENS_RE = re.compile(r"[Tt]okens:?\s*([\d,]+)")
SKILL_RE = re.compile(r"[Ss]kill\s+([\w\-]+)")


def parse_audit_file(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f) or []
        except Exception:
            return []
    return data if isinstance(data, list) else []


def extract_episode_data(entry: dict, dispatch_map: dict) -> dict | None:
    if entry.get("action") != "task_completed":
        return None
    task_id = entry.get("entity_id", "")
    details = entry.get("details", "")
    timestamp = entry.get("timestamp", "")
    actor = entry.get("actor", "")

    score_m = SCORE_RE.search(details)
    tokens_m = TOKENS_RE.search(details)

    score = int(score_m.group(1)) if score_m else None
    tokens = int(tokens_m.group(1).replace(",", "")) if tokens_m else 0

    dispatch = dispatch_map.get(task_id, {})
    skill = dispatch.get("skill", "")
    if not skill:
        m = SKILL_RE.search(dispatch.get("details", ""))
        if m:
            skill = m.group(1)

    project = ""
    for proj in ("cuidai", "lucas", "vivenda", "atrium", "credito", "pupli", "cre", "atelier", "patudos"):
        if proj in task_id.lower() or proj in details.lower():
            project = proj
            break

    outcome = Outcome.SUCCESS
    if "fail" in details.lower() or "blocked" in details.lower():
        outcome = Outcome.FAILURE

    return {
        "task_id": task_id,
        "timestamp": timestamp,
        "agent": actor,
        "skill": skill,
        "outcome": outcome,
        "score": score,
        "tokens_used": tokens,
        "project": project,
        "output_summary": details[:300],
    }


def backfill(days: int = 0, dry_run: bool = False) -> dict:
    files = sorted(AUDIT_DIR.glob("*.yaml"))
    if days > 0:
        cutoff = datetime.now(UTC) - timedelta(days=days)
        files = [f for f in files if f.stem >= cutoff.strftime("%Y-%m-%d")]

    written = 0
    skipped = 0
    dispatch_map: dict[str, dict] = {}

    for path in files:
        entries = parse_audit_file(path)
        for e in entries:
            if e.get("action") == "task_dispatched":
                dispatch_map[e.get("entity_id", "")] = {
                    "skill": "",
                    "details": e.get("details", ""),
                }
                m = SKILL_RE.search(e.get("details", ""))
                if m:
                    dispatch_map[e["entity_id"]]["skill"] = m.group(1)

        for e in entries:
            data = extract_episode_data(e, dispatch_map)
            if not data:
                continue
            if not data["skill"]:
                skipped += 1
                continue
            ep = Episode(
                episode_id="",
                task_id=data["task_id"],
                timestamp=data["timestamp"],
                agent=data["agent"],
                skill=data["skill"],
                outcome=data["outcome"],
                score=data["score"],
                tokens_used=data["tokens_used"],
                project=data["project"],
                model="opus",
                output_summary=data["output_summary"],
            )
            if not dry_run:
                episodic.write_episode(ep)
            written += 1

    return {"files_processed": len(files), "episodes_written": written, "skipped_no_skill": skipped, "dry_run": dry_run}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=30, help="Audit lookback in days (0=all)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--source", choices=["done", "audit", "both"], default="both")
    args = parser.parse_args()

    import json
    results = {}
    if args.source in ("done", "both"):
        results["done"] = backfill_from_done(dry_run=args.dry_run)
    if args.source in ("audit", "both"):
        results["audit"] = backfill(days=args.days, dry_run=args.dry_run)
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
