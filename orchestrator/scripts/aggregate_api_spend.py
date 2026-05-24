#!/usr/bin/env python3
"""Aggregate api_spend_log.yaml into rolling spend metrics.

Reads quality/api_spend_log.yaml and computes:
  - Last 24h spend (USD + tokens)
  - This month spend (USD + tokens)
  - Per-caller breakdown
  - Per-model breakdown

Designed for dashboard widget consumption + CLI inspection.

Usage:
    python -m scripts.aggregate_api_spend            # Print + write metrics yaml
    python -m scripts.aggregate_api_spend --json     # JSON to stdout
    python -m scripts.aggregate_api_spend --print-only
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
SPEND_LOG = ORCH_DIR / "quality" / "api_spend_log.yaml"
SPEND_JSONL = ORCH_DIR / "quality" / "api_spend_log.jsonl"
METRICS_FILE = ORCH_DIR / "quality" / "api_spend_metrics.yaml"


def load_entries() -> list[dict]:
    """Load entries from JSONL (source of truth) with YAML fallback for
    pre-2026-05-24 entries logged before JSONL migration."""
    import json
    entries: list[dict] = []

    # Primary: JSONL (concurrent-safe, source of truth post-2026-05-24)
    if SPEND_JSONL.exists():
        with open(SPEND_JSONL, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue  # skip malformed line, don't crash whole aggregate

    # Secondary: YAML — read but DON'T double-count entries also in JSONL.
    # Heuristic: YAML entries written before JSONL existed are unique;
    # post-migration both files have same entries, so we only take YAML
    # if it has more entries than JSONL (legacy data).
    if SPEND_LOG.exists():
        with open(SPEND_LOG, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        yaml_entries = data.get("entries") or []
        if len(yaml_entries) > len(entries):
            # YAML has historical entries JSONL doesn't — use YAML count
            entries = yaml_entries

    return entries


def _parse_ts(ts: str | None) -> datetime:
    if not ts:
        return datetime.min.replace(tzinfo=UTC)
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return datetime.min.replace(tzinfo=UTC)


def aggregate(entries: list[dict], window_hours: int | None = None,
              month: str | None = None) -> dict:
    """Compute aggregated spend metrics.

    window_hours: filter to last N hours (None = no time filter)
    month: filter to YYYY-MM (None = no month filter)
    """
    filtered = entries
    if window_hours is not None:
        cutoff = datetime.now(UTC) - timedelta(hours=window_hours)
        filtered = [e for e in filtered if _parse_ts(e.get("ts")) >= cutoff]
    if month is not None:
        filtered = [e for e in filtered
                    if (e.get("ts") or "").startswith(month)]

    total_usd = sum(e.get("cost_usd", 0) or 0 for e in filtered)
    total_tokens = sum(e.get("total_tokens", 0) or 0 for e in filtered)

    by_caller: dict[str, dict] = defaultdict(lambda: {"cost_usd": 0.0, "tokens": 0, "calls": 0})
    by_model: dict[str, dict] = defaultdict(lambda: {"cost_usd": 0.0, "tokens": 0, "calls": 0})

    for e in filtered:
        caller = e.get("caller") or "unknown"
        model = e.get("model") or "unknown"
        cost = e.get("cost_usd", 0) or 0
        tokens = e.get("total_tokens", 0) or 0
        by_caller[caller]["cost_usd"] += cost
        by_caller[caller]["tokens"] += tokens
        by_caller[caller]["calls"] += 1
        by_model[model]["cost_usd"] += cost
        by_model[model]["tokens"] += tokens
        by_model[model]["calls"] += 1

    # Round costs to cents for readability
    for d in (by_caller, by_model):
        for v in d.values():
            v["cost_usd"] = round(v["cost_usd"], 4)

    return {
        "n_calls": len(filtered),
        "total_usd": round(total_usd, 4),
        "total_tokens": total_tokens,
        "by_caller": dict(by_caller),
        "by_model": dict(by_model),
    }


def render_table(label: str, agg: dict) -> str:
    lines = [f"=== {label} ==="]
    lines.append(f"  Total: ${agg['total_usd']:.4f} · {agg['total_tokens']:,} tokens · {agg['n_calls']} calls")
    if not agg["by_caller"]:
        return "\n".join(lines)
    lines.append("")
    lines.append(f"  {'caller':<35} {'calls':>5} {'tokens':>10} {'cost USD':>10}")
    for caller, m in sorted(agg["by_caller"].items(), key=lambda kv: kv[1]["cost_usd"], reverse=True):
        lines.append(f"  {caller:<35} {m['calls']:>5} {m['tokens']:>10,} ${m['cost_usd']:>9.4f}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--print-only", action="store_true")
    args = ap.parse_args()

    entries = load_entries()
    if not entries:
        print("[aggregate_api_spend] No entries found at", SPEND_LOG, file=sys.stderr)
        # Still write empty metrics file so dashboard knows nothing's there
        if not args.print_only:
            METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(METRICS_FILE, "w", encoding="utf-8") as f:
                yaml.safe_dump({
                    "computed_at": datetime.now(UTC).isoformat(timespec="seconds"),
                    "last_24h": {"n_calls": 0, "total_usd": 0.0, "total_tokens": 0,
                                 "by_caller": {}, "by_model": {}},
                    "this_month": {"n_calls": 0, "total_usd": 0.0, "total_tokens": 0,
                                   "by_caller": {}, "by_model": {}},
                    "all_time":   {"n_calls": 0, "total_usd": 0.0, "total_tokens": 0,
                                   "by_caller": {}, "by_model": {}},
                }, f, sort_keys=False)
        return 0

    month = datetime.now(UTC).strftime("%Y-%m")
    agg_24h = aggregate(entries, window_hours=24)
    agg_month = aggregate(entries, month=month)
    agg_all = aggregate(entries)

    out = {
        "computed_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "last_24h": agg_24h,
        "this_month": agg_month,
        "all_time": agg_all,
    }

    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(render_table("Last 24 hours", agg_24h))
        print()
        print(render_table(f"This month ({month})", agg_month))
        print()
        print(render_table("All time", agg_all))

    if not args.print_only:
        METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(METRICS_FILE, "w", encoding="utf-8") as f:
            yaml.safe_dump(out, f, sort_keys=False, allow_unicode=True)
        print(f"\n[aggregate_api_spend] Wrote {METRICS_FILE}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
