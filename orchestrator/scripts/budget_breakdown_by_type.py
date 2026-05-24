#!/usr/bin/env python3
"""Budget breakdown by project type — dev vs client visibility.

Reads:
  - quality budget yaml(s) under budgets/
  - config/project_types.yaml — slug → {dev|client|unknown} mapping

Outputs:
  - Per-month totals: dev tokens, client tokens, unknown tokens
  - Per-project rows sorted by spend
  - Optional --json for dashboard consumption

Usage:
    python -m scripts.budget_breakdown_by_type                  # current month
    python -m scripts.budget_breakdown_by_type --month 2026-04  # specific month
    python -m scripts.budget_breakdown_by_type --all            # all months
    python -m scripts.budget_breakdown_by_type --json           # machine-readable

Exit codes:
    0 — success
    1 — config or budget file missing
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
BUDGETS_DIR = ORCH_DIR / "budgets"
TYPES_FILE = ORCH_DIR / "config" / "project_types.yaml"


def load_types_config() -> dict:
    if not TYPES_FILE.exists():
        return {"clients": {}, "dev": {}, "default_for_unmapped": "unknown"}
    with open(TYPES_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def classify(slug: str, cfg: dict) -> str:
    """Return 'client', 'dev', or 'unknown' for a project slug."""
    if not slug or slug.strip() == "":
        return "unknown"  # blank/missing project — needs attention
    if slug in (cfg.get("clients") or {}):
        return "client"
    if slug in (cfg.get("dev") or {}):
        return "dev"
    return cfg.get("default_for_unmapped", "unknown")


def load_budget_file(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def aggregate_month(month_yaml: dict, cfg: dict) -> dict:
    """Compute totals per type for one month + per-project breakdown."""
    by_project = month_yaml.get("by_project") or {}
    totals = defaultdict(int)
    breakdown = []
    for slug, tokens in by_project.items():
        if not isinstance(tokens, (int, float)):
            continue
        typ = classify(str(slug), cfg)
        totals[typ] += int(tokens)
        breakdown.append({
            "project": slug,
            "type": typ,
            "tokens": int(tokens),
        })
    total_all = sum(totals.values())
    return {
        "month": month_yaml.get("month") or "unknown",
        "total_tokens": total_all,
        "by_type": dict(totals),
        "percentages_by_type": {
            t: (round(v / total_all * 100, 1) if total_all else 0.0)
            for t, v in totals.items()
        },
        "breakdown": sorted(breakdown, key=lambda x: x["tokens"], reverse=True),
    }


def list_budget_months() -> list[Path]:
    if not BUDGETS_DIR.exists():
        return []
    return sorted(BUDGETS_DIR.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9].yaml"))


def render_human(agg: dict) -> str:
    lines = [f"=== Budget — {agg['month']} ==="]
    total = agg["total_tokens"]
    if total == 0:
        lines.append("  (no project spend recorded)")
        return "\n".join(lines)

    lines.append(f"  Total tracked: {total:,} tokens")
    lines.append("")
    lines.append("  By type:")
    for typ in ("client", "dev", "unknown"):
        v = agg["by_type"].get(typ, 0)
        pct = agg["percentages_by_type"].get(typ, 0.0)
        lines.append(f"    {typ:<8} {v:>12,} tokens  ({pct:>5.1f}%)")

    lines.append("")
    lines.append("  Per project (top 10 by spend):")
    lines.append(f"    {'project':<20} {'type':<10} {'tokens':>12}  pct")
    grand_total = total or 1
    for row in agg["breakdown"][:10]:
        slug = row["project"] or "<blank>"
        slug = str(slug)[:18]
        pct = row["tokens"] / grand_total * 100
        lines.append(f"    {slug:<20} {row['type']:<10} {row['tokens']:>12,}  {pct:>4.1f}%")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", help="YYYY-MM (default: current)")
    ap.add_argument("--all", action="store_true", help="Aggregate all months")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    cfg = load_types_config()

    if args.all:
        months = list_budget_months()
        results = []
        for path in months:
            data = load_budget_file(path)
            results.append(aggregate_month(data, cfg))
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for r in results:
                print(render_human(r))
                print()
        return 0

    target_month = args.month or datetime.now(UTC).strftime("%Y-%m")
    path = BUDGETS_DIR / f"{target_month}.yaml"
    if not path.exists():
        print(f"No budget file for {target_month} at {path}", file=sys.stderr)
        return 1

    data = load_budget_file(path)
    agg = aggregate_month(data, cfg)
    if args.json:
        print(json.dumps(agg, indent=2))
    else:
        print(render_human(agg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
