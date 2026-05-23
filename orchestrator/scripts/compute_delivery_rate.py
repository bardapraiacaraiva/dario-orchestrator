#!/usr/bin/env python3
"""
DARIO compute_delivery_rate — Recompute delivery_ready_rate from current metrics.
=================================================================================

Standalone scanner that re-aggregates the production_scores_delivery_ready
and deliverable_*_count fields from quality/skill-metrics.yaml into the
top-level `delivery_ready_rate_pct` metric.

Run it any time to refresh the global metric after manual edits, or
schedule it daily via cron.

Usage:
    python scripts/compute_delivery_rate.py            # Print + update
    python scripts/compute_delivery_rate.py --check    # Print only, no writes
    python scripts/compute_delivery_rate.py --json     # JSON output

Exit codes:
    0 = computed
    1 = error
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ORCH = Path.home() / ".claude" / "orchestrator"
METRICS_PATH = ORCH / "quality" / "skill-metrics.yaml"

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


def compute() -> dict:
    metrics = load_y(METRICS_PATH)
    skills = metrics.get("skills") or {}

    delivery_yes = 0
    delivery_needs_review = 0
    delivery_no = 0
    delivery_total = 0
    by_skill = []
    production_validated = 0

    for name, m in skills.items():
        if not isinstance(m, dict):
            continue
        n = int(m.get("production_n_real_outputs") or 0)
        if n == 0:
            continue
        production_validated += 1
        yes = int(m.get("deliverable_yes_count") or 0)
        no = int(m.get("deliverable_no_count") or 0)
        review = int(m.get("deliverable_needs_review_count") or 0)
        # Backfill review count if missing (n - yes - no)
        if review == 0 and (n - yes - no) > 0:
            review = n - yes - no
        delivery_yes += yes
        delivery_no += no
        delivery_needs_review += review
        delivery_total += n
        by_skill.append({
            "skill": name,
            "n": n,
            "yes": yes,
            "needs_review": review,
            "no": no,
            "delivery_rate": round(100.0 * yes / n, 1) if n else 0.0,
            "production_avg": m.get("production_avg_delivery_ready"),
        })

    delivery_rate = (100.0 * delivery_yes / delivery_total) if delivery_total else 0.0

    return {
        "delivery_ready_rate_pct": round(delivery_rate, 1),
        "delivery_ready_yes_count": delivery_yes,
        "delivery_ready_needs_review_count": delivery_needs_review,
        "delivery_ready_no_count": delivery_no,
        "delivery_ready_total": delivery_total,
        "production_validated_skills": production_validated,
        "by_skill": sorted(by_skill, key=lambda x: -x["delivery_rate"]),
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Recompute delivery_ready_rate from metrics.")
    p.add_argument("--check", action="store_true", help="Print without writing.")
    p.add_argument("--json", action="store_true", help="JSON output.")
    args = p.parse_args()

    if not METRICS_PATH.exists():
        print(f"error: {METRICS_PATH} not found", file=sys.stderr)
        return 1

    result = compute()

    if not args.check:
        # Write top-level metrics
        metrics = load_y(METRICS_PATH)
        metrics["delivery_ready_rate_pct"] = result["delivery_ready_rate_pct"]
        metrics["delivery_ready_yes_count"] = result["delivery_ready_yes_count"]
        metrics["delivery_ready_needs_review_count"] = result["delivery_ready_needs_review_count"]
        metrics["delivery_ready_no_count"] = result["delivery_ready_no_count"]
        metrics["delivery_ready_total"] = result["delivery_ready_total"]
        metrics["production_validated_skills"] = result["production_validated_skills"]
        metrics["last_updated"] = datetime.now(UTC).isoformat()
        dump_y(metrics, METRICS_PATH)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
        return 0

    print(f"=== Delivery-ready rate ===")
    print(f"  Rate:                  {result['delivery_ready_rate_pct']:.1f}%")
    print(f"  Yes (ready as-is):     {result['delivery_ready_yes_count']}")
    print(f"  Needs review:          {result['delivery_ready_needs_review_count']}")
    print(f"  Rework / not usable:   {result['delivery_ready_no_count']}")
    print(f"  Total real outputs:    {result['delivery_ready_total']}")
    print(f"  Skills with prod data: {result['production_validated_skills']}")

    if result["by_skill"]:
        print(f"\n=== Per skill (top {min(len(result['by_skill']), 15)}) ===")
        for s in result["by_skill"][:15]:
            ratio = f"{s['yes']}/{s['n']}"
            pavg = s.get("production_avg")
            avg_s = f"avg {pavg}" if pavg is not None else "avg ?"
            print(f"  {s['delivery_rate']:>5.1f}%  {ratio:>7}  {avg_s:>9}   {s['skill']}")

    if not args.check:
        print(f"\nUpdated {METRICS_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
