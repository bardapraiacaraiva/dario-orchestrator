"""One-shot backfill — walk all historical transcripts and capture tokens.

Reuses enforcement.token_capture.capture() so behavior is identical to the
live SubagentStop hook. State file dedup guarantees idempotency: re-running
this script after a partial run will only process new content.

Usage:
    python scripts/backfill_token_capture.py [--dry-run] [--limit N]

Output: summary table of (session, messages, tokens, cost, task_id).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from enforcement.token_capture import capture  # noqa: E402

PROJECTS_DIR = Path.home() / ".claude" / "projects" / "C--Users-barda"


def find_sessions_with_subagents() -> list[tuple[str, Path]]:
    """Return list of (session_uuid, transcript_path) for sessions with sidechain activity."""
    sessions = []
    for subdir in PROJECTS_DIR.glob("*/subagents"):
        session_uuid = subdir.parent.name
        transcript = PROJECTS_DIR / f"{session_uuid}.jsonl"
        if transcript.exists():
            sessions.append((session_uuid, transcript))
    sessions.sort(key=lambda x: x[1].stat().st_mtime)
    return sessions


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Skip state mutation, report only")
    ap.add_argument("--limit", type=int, default=None, help="Process only first N sessions")
    args = ap.parse_args()

    sessions = find_sessions_with_subagents()
    if args.limit:
        sessions = sessions[: args.limit]

    print(f"Found {len(sessions)} sessions with subagent activity")
    print(f"{'='*100}")
    print(f"{'Session':<10} {'Msgs':>6} {'Total tokens':>15} {'Cost USD':>10} {'Task ID':<12} {'Status':<10}")
    print(f"{'='*100}")

    grand_total = {"messages": 0, "tokens": 0, "cost_usd": 0.0, "captured": 0, "skipped": 0}

    for sess_uuid, transcript in sessions:
        payload = {
            "hook_event_name": "SubagentStop",
            "session_id": sess_uuid,
            "transcript_path": str(transcript).replace("\\", "/"),
        }
        if args.dry_run:
            # Just parse, don't write state
            from enforcement.token_capture import (
                aggregate_usage,
                find_task_id,
                parse_transcript_sidechains,
            )
            msgs = parse_transcript_sidechains(transcript, None, set())
            if not msgs:
                continue
            totals = aggregate_usage(msgs)
            tid = find_task_id(msgs)
            print(f"{sess_uuid[:8]:<10} {len(msgs):>6} {totals['total_tokens']:>15,} "
                  f"${totals['cost_usd']:>9.4f} {tid or '-':<12} {'DRY-RUN':<10}")
            grand_total["messages"] += len(msgs)
            grand_total["tokens"] += totals["total_tokens"]
            grand_total["cost_usd"] += totals["cost_usd"]
            grand_total["captured"] += 1
        else:
            result = capture(payload)
            status = result.get("status", "?")
            if status == "captured":
                print(f"{sess_uuid[:8]:<10} {result['messages_captured']:>6} "
                      f"{result['total_tokens']:>15,} ${result.get('cost_usd', 0):>9.4f} "
                      f"{result.get('task_id') or '-':<12} {status:<10}")
                grand_total["messages"] += result["messages_captured"]
                grand_total["tokens"] += result["total_tokens"]
                grand_total["cost_usd"] += result.get("cost_usd", 0)
                grand_total["captured"] += 1
            else:
                grand_total["skipped"] += 1

    print(f"{'='*100}")
    print(f"GRAND TOTAL: {grand_total['captured']} sessions captured, "
          f"{grand_total['skipped']} skipped")
    print(f"  Messages: {grand_total['messages']:,}")
    print(f"  Tokens:   {grand_total['tokens']:,}")
    print(f"  Cost USD: ${grand_total['cost_usd']:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
