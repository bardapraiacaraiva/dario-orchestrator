#!/usr/bin/env python3
"""
DARIO Human Review Queue — Bridge from autonomous output to 90+ delivery.
==========================================================================

The structural finding from the 2026-05-23 quality sprint: LLM-judge
ceiling for AI-generated single-skill outputs is ~88. Bundle ceiling
~74. The only proven path to sustained 90+ delivery_ready_rate is
HUMAN REVIEW in the pipeline.

This module wires the human-in-the-loop primitive.

Workflow:
    1. AI generates output (score_real_output.py with --json)
    2. If score < 90, output lands in `human_review_queue/`
    3. Operator opens, reviews, applies edits (typically 15-30 min)
    4. Operator marks resolved with `--resolved <id>` after edits
    5. Re-judge automatically post-resolution
    6. Recorded with `human_polished: True` flag in metrics

Targets:
    - Lift delivery_ready_rate from autonomous baseline 17.5% to 70%+
      with human review applied to needs-review outputs
    - Track time-to-resolution per skill (identify slow skills)
    - Surface review backlog on dashboard

Storage:
    ~/.claude/orchestrator/human_review_queue/
        <skill>__<timestamp>__<id>.md       Original output
        <skill>__<timestamp>__<id>.meta.yaml Score + reasoning + state
        <skill>__<timestamp>__<id>.polished.md  Post-human edits (after resolution)

CLI:
    # Add an output to the queue (auto-called when score < 90)
    python human_review_queue.py --add --skill X --output file.md --context "..."

    # List pending reviews
    python human_review_queue.py --list

    # Mark resolved (after operator edits)
    python human_review_queue.py --resolved <id> --polished-file polished.md

    # Show stats
    python human_review_queue.py --stats

Exit codes:
    0 = success
    1 = error
    2 = queue empty (for --list)
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

ORCH = Path.home() / ".claude" / "orchestrator"
QUEUE_DIR = ORCH / "human_review_queue"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

try:
    from ruamel.yaml import YAML
    _y = YAML()
    _y.preserve_quotes = True
    _y.width = 200

    def load_y(p):
        with open(p, encoding="utf-8") as f:
            return _y.load(f)

    def dump_y(d, p):
        with open(p, "w", encoding="utf-8") as f:
            _y.dump(d, f)
except ImportError:
    import yaml

    def load_y(p):
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f)

    def dump_y(d, p):
        with open(p, "w", encoding="utf-8") as f:
            yaml.safe_dump(d, f, sort_keys=False)


def _short_id() -> str:
    return uuid.uuid4().hex[:8]


def cmd_add(args) -> int:
    """Add an AI-generated output to the review queue."""
    if not Path(args.output).exists():
        print(f"error: {args.output} not found", file=sys.stderr)
        return 1

    item_id = _short_id()
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    base = f"{args.skill}__{timestamp}__{item_id}"

    # Copy output
    output_path = QUEUE_DIR / f"{base}.md"
    output_path.write_text(Path(args.output).read_text(encoding="utf-8"), encoding="utf-8")

    # Meta
    meta = {
        "id": item_id,
        "skill": args.skill,
        "context": args.context,
        "ai_score": args.ai_score,
        "ai_verdict": args.ai_verdict or "needs-review",
        "ai_reasoning": args.ai_reasoning or "",
        "added_at": datetime.now(UTC).isoformat(),
        "state": "pending",
        "polished_at": None,
        "polished_score": None,
        "time_to_resolution_minutes": None,
    }
    dump_y(meta, QUEUE_DIR / f"{base}.meta.yaml")

    print(f"[OK] Added to review queue:")
    print(f"     id={item_id}")
    print(f"     skill={args.skill}")
    print(f"     ai_score={args.ai_score} [{meta['ai_verdict']}]")
    print(f"     file: {output_path}")
    print(f"     edit this file, then: python human_review_queue.py --resolved {item_id}")
    return 0


def _find_item(item_id: str) -> tuple[Path, dict] | None:
    for meta_file in QUEUE_DIR.glob(f"*__{item_id}.meta.yaml"):
        return meta_file, load_y(meta_file)
    return None


def cmd_resolved(args) -> int:
    """Mark an item resolved after human edits."""
    found = _find_item(args.resolved)
    if not found:
        print(f"error: id {args.resolved} not found in queue", file=sys.stderr)
        return 1
    meta_file, meta = found
    base = meta_file.stem.replace(".meta", "")

    # If polished-file provided, save it; else assume operator edited the original
    polished_path = QUEUE_DIR / f"{base}.polished.md"
    if args.polished_file:
        polished_path.write_text(Path(args.polished_file).read_text(encoding="utf-8"), encoding="utf-8")
    else:
        # Use the original file (assume in-place edit)
        original = QUEUE_DIR / f"{base}.md"
        polished_path.write_text(original.read_text(encoding="utf-8"), encoding="utf-8")

    # Mark resolved
    added = datetime.fromisoformat(meta["added_at"].replace("Z", "+00:00"))
    now = datetime.now(UTC)
    ttr_min = round((now - added).total_seconds() / 60, 1)

    meta["state"] = "resolved"
    meta["polished_at"] = now.isoformat()
    meta["time_to_resolution_minutes"] = ttr_min
    meta["polished_score"] = args.polished_score  # if human re-scored, otherwise None
    dump_y(meta, meta_file)

    print(f"[OK] Resolved {args.resolved} in {ttr_min} min")
    print(f"     polished file: {polished_path}")
    if args.polished_score:
        # Re-record in skill-metrics as human-polished
        try:
            sys.path.insert(0, str(ORCH))
            from quality.score_real_output import record_score
            result = record_score(
                meta["skill"], int(args.polished_score), "yes",
                {}, meta.get("context", ""), polished_path.read_text(encoding="utf-8")[:200],
            )
            print(f"     recorded as production with score {args.polished_score}")
            print(f"     skill avg now: {result.get('combined_avg', '?')}")
        except Exception as e:
            print(f"     warn: could not record automatically: {e}")
    return 0


def cmd_list(args) -> int:
    """List pending review items."""
    items = []
    for meta_file in QUEUE_DIR.glob("*.meta.yaml"):
        m = load_y(meta_file)
        if m.get("state") == "pending":
            items.append(m)

    if not items:
        print("Queue empty — no pending reviews")
        return 2

    items.sort(key=lambda x: x["added_at"])
    print(f"=== Pending Reviews ({len(items)}) ===\n")
    for m in items:
        added = datetime.fromisoformat(m["added_at"].replace("Z", "+00:00"))
        age = (datetime.now(UTC) - added).total_seconds() / 3600
        print(f"  [{m['id']}]  {m['skill']:25s}  score={m.get('ai_score', '?'):>3}  age={age:.1f}h")
        if m.get("ai_reasoning"):
            print(f"             {m['ai_reasoning'][:80]}...")
    print()
    print("Edit any file in human_review_queue/, then:")
    print("  python human_review_queue.py --resolved <id> --polished-score 92")
    return 0


def cmd_stats(args) -> int:
    """Print queue + impact stats."""
    items = []
    for meta_file in QUEUE_DIR.glob("*.meta.yaml"):
        items.append(load_y(meta_file))

    pending = [m for m in items if m.get("state") == "pending"]
    resolved = [m for m in items if m.get("state") == "resolved"]

    print(f"=== Human Review Queue Stats ===")
    print(f"  Pending:           {len(pending)}")
    print(f"  Resolved:          {len(resolved)}")
    print(f"  Total processed:   {len(items)}")

    if resolved:
        avg_ttr = sum(m.get("time_to_resolution_minutes", 0) for m in resolved) / len(resolved)
        scored = [m for m in resolved if m.get("polished_score")]
        if scored:
            avg_lift = sum(int(m["polished_score"]) - int(m.get("ai_score", 0)) for m in scored) / len(scored)
            avg_polished = sum(int(m["polished_score"]) for m in scored) / len(scored)
            print(f"\n  Avg time-to-resolution: {avg_ttr:.1f} min")
            print(f"  Avg score lift:         +{avg_lift:.1f} pts (post-human)")
            print(f"  Avg polished score:     {avg_polished:.1f}/100")

        # Per-skill breakdown
        print(f"\n  Per-skill (resolved):")
        from collections import defaultdict
        by_skill = defaultdict(list)
        for m in resolved:
            by_skill[m["skill"]].append(m)
        for skill, ms in sorted(by_skill.items(), key=lambda x: -len(x[1])):
            ttr = sum(m.get("time_to_resolution_minutes", 0) for m in ms) / len(ms)
            print(f"    {skill:25s}  n={len(ms)}  avg_ttr={ttr:.1f}min")

    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="DARIO Human Review Queue")
    p.add_argument("--add", action="store_true")
    p.add_argument("--resolved", type=str, help="Mark item ID resolved")
    p.add_argument("--list", action="store_true")
    p.add_argument("--stats", action="store_true")

    # Add args
    p.add_argument("--skill")
    p.add_argument("--output")
    p.add_argument("--context", default="")
    p.add_argument("--ai-score", type=int)
    p.add_argument("--ai-verdict")
    p.add_argument("--ai-reasoning", default="")

    # Resolved args
    p.add_argument("--polished-file")
    p.add_argument("--polished-score", type=int)

    args = p.parse_args()

    if args.add:
        if not (args.skill and args.output and args.ai_score is not None):
            print("error: --add requires --skill --output --ai-score", file=sys.stderr)
            return 1
        return cmd_add(args)
    if args.resolved:
        return cmd_resolved(args)
    if args.list:
        return cmd_list(args)
    if args.stats:
        return cmd_stats(args)

    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
