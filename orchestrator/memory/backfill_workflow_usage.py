"""Retroactive backfill of procedural.record_usage from historical episodes.

Replays every successful episode per project, checks at each point if the
trailing skill sequence closes a known workflow, and increments use_count /
avg_score / success_rate accordingly.

Idempotent when --reset is used (default). Without --reset, counters accumulate.

Usage:
    python -m memory.backfill_workflow_usage              # reset + full replay
    python -m memory.backfill_workflow_usage --no-reset
    python -m memory.backfill_workflow_usage --dry-run
    python -m memory.backfill_workflow_usage --project cuidai
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from memory import episodic, procedural
from memory.schemas import Outcome


def reset_workflow_counters(dry_run: bool = False) -> int:
    wfs = procedural.list_workflows()
    if dry_run:
        return len(wfs)
    for wf in wfs:
        wf.use_count = 0
        wf.avg_score = 0.0
        wf.success_rate = 0.0
        wf.last_used = None
        procedural.write_workflow(wf)
    return len(wfs)


def backfill(project_filter: str = "", reset: bool = True, dry_run: bool = False, window_days: int = 365) -> dict:
    if reset:
        n_reset = reset_workflow_counters(dry_run=dry_run)
    else:
        n_reset = 0

    by_project: dict[str, list] = defaultdict(list)
    for ep in episodic.iter_episodes(window_days=window_days):
        proj = ep.project or "global"
        if project_filter and proj != project_filter:
            continue
        by_project[proj].append(ep)

    total_episodes = sum(len(eps) for eps in by_project.values())
    completions: list[dict] = []
    per_workflow: dict[str, int] = defaultdict(int)

    for proj, eps in by_project.items():
        eps.sort(key=lambda e: e.timestamp)
        trailing: list[str] = []
        trailing_scores: list = []
        for ep in eps:
            trailing.append(ep.skill)
            trailing_scores.append(ep.score if ep.score is not None else None)
            if ep.outcome != Outcome.SUCCESS:
                continue
            matches = procedural.detect_completed(trailing, project=proj)
            for wf in matches:
                seq_len = len(wf.skills_sequence)
                window_scores = [s for s in trailing_scores[-seq_len:] if s is not None]
                avg = int(sum(window_scores) / len(window_scores)) if window_scores else None
                if not dry_run:
                    procedural.record_usage(wf.workflow_id, success=True, score=avg)
                per_workflow[wf.workflow_id] += 1
                completions.append({
                    "project": proj,
                    "workflow": wf.workflow_id,
                    "closed_by_task": ep.task_id,
                    "closed_at": ep.timestamp,
                    "avg_score": avg,
                    "sequence": wf.skills_sequence,
                })

    return {
        "reset_workflows": n_reset,
        "projects_scanned": len(by_project),
        "episodes_scanned": total_episodes,
        "completions_detected": len(completions),
        "per_workflow": dict(per_workflow),
        "dry_run": dry_run,
        "examples": completions[:5],
    }


def main():
    parser = argparse.ArgumentParser(description="Retroactive workflow usage backfill")
    parser.add_argument("--project", default="", help="Limit to one project")
    parser.add_argument("--no-reset", action="store_true", help="Don't reset counters before replay")
    parser.add_argument("--dry-run", action="store_true", help="Don't write, just count")
    parser.add_argument("--window-days", type=int, default=365)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = backfill(
        project_filter=args.project,
        reset=not args.no_reset,
        dry_run=args.dry_run,
        window_days=args.window_days,
    )

    if args.json:
        print(json.dumps(result, indent=2, default=str))
        return 0

    print("\n[BACKFILL workflow usage]")
    print(f"  Reset:      {result['reset_workflows']} workflows")
    print(f"  Projects:   {result['projects_scanned']}")
    print(f"  Episodes:   {result['episodes_scanned']}")
    print(f"  Completions detected: {result['completions_detected']}")
    if result['per_workflow']:
        print("\n  Per workflow:")
        for wf_id, n in sorted(result['per_workflow'].items(), key=lambda x: -x[1]):
            print(f"    {wf_id:50s}  +{n}")
    if result['examples']:
        print("\n  Examples (first 5):")
        for ex in result['examples']:
            print(f"    [{ex['project']:12s}] {ex['workflow']:50s}  task={ex['closed_by_task']}  avg={ex['avg_score']}")
    if result['dry_run']:
        print("\n  (DRY RUN — no changes written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
