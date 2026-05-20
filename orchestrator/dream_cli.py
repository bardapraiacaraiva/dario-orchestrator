"""Top-level CLI for /dream command.

Wraps dream.engine and adds quick health reports.

Usage:
    python dream_cli.py                  # full cycle
    python dream_cli.py --window 14
    python dream_cli.py --dry-run
    python dream_cli.py health           # show memory health only
    python dream_cli.py episodes         # list recent episodes
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from dream.engine import run_dream
from memory import hooks, episodic, procedural


def cmd_dream(args) -> int:
    report = run_dream(window_days=args.window, dry_run=args.dry_run)
    if args.json:
        print(json.dumps(report.model_dump(mode="json", exclude_none=True), indent=2))
    else:
        print(f"[DREAM] {report.dream_id}  episodes={report.episodes_processed}  "
              f"mem {report.memories_before}->{report.memories_after}  "
              f"patterns={len(report.patterns_detected)}  workflows={len(report.convergent_workflows)}")
    return 0


def cmd_health(args) -> int:
    h = hooks.health()
    if args.json:
        print(json.dumps(h, indent=2, default=str))
        return 0
    print("\n[MEMORY HEALTH]")
    print(f"  Episodic (7d):  {h['episodic']['total']} episodes  avg_score={h['episodic'].get('avg_score')}")
    print(f"  Semantic:       {h['semantic']['structured_count']} structured + {h['semantic']['user_memory_entries']} user-memory")
    print(f"                  retrievals={h['semantic']['total_retrievals']}")
    print(f"  Procedural:     {h['procedural']['total']} workflows  ({h['procedural']['discovered_from_convergence']} convergent)")
    print(f"  Cache:          {h['cache']['entries']} entries  hits={h['cache']['total_hits']}  tokens_saved~={h['cache']['tokens_saved_estimate']}")
    print(f"  Retrieval log:  {h['retrieval']['total_retrievals']} hits in {h['retrieval']['window_days']}d")
    return 0


def cmd_episodes(args) -> int:
    for ep in episodic.iter_episodes(args.window):
        print(f"  {ep.episode_id}  {ep.timestamp[:19]}  {ep.skill:30s}  {ep.outcome.value:8s}  score={ep.score}")
    return 0


def cmd_workflows(args) -> int:
    for wf in procedural.list_workflows():
        print(f"  {wf.workflow_id}  ({wf.discovered_from})  sessions={wf.sessions_observed}  "
              f"avg_score={wf.avg_score}  use_count={wf.use_count}")
        print(f"    -> {' → '.join(wf.skills_sequence)}")
    return 0


def main():
    parser = argparse.ArgumentParser(prog="dream", description="DARIO Dream Engine CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_run = sub.add_parser("run", help="Run a full dream cycle (default)")
    p_run.add_argument("--window", type=int, default=7)
    p_run.add_argument("--dry-run", action="store_true")
    p_run.add_argument("--json", action="store_true")
    p_run.set_defaults(func=cmd_dream)

    p_h = sub.add_parser("health", help="Show memory health snapshot")
    p_h.add_argument("--json", action="store_true")
    p_h.set_defaults(func=cmd_health)

    p_e = sub.add_parser("episodes", help="List recent episodes")
    p_e.add_argument("--window", type=int, default=7)
    p_e.set_defaults(func=cmd_episodes)

    p_w = sub.add_parser("workflows", help="List procedural workflows")
    p_w.set_defaults(func=cmd_workflows)

    args, _ = parser.parse_known_args()
    if not args.cmd:
        args = parser.parse_args(["run"] + sys.argv[1:])
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
