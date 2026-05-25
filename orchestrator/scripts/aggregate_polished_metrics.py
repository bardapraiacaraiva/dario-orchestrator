#!/usr/bin/env python3
"""Padrão A — Aggregate polished_production_runs.yaml into rolling metrics.

Reads quality/polished_production_runs.yaml and computes:
  - Last 30 days: per-skill mean lift, gate-pass rate, n_runs
  - All-time:     per-skill mean lift, gate-pass rate, n_runs
  - Overall:      cross-skill mean lift on passed runs

Writes summary to quality/polished_production_metrics.yaml.
Also prints a compact table to stdout.

Usage:
    python -m scripts.aggregate_polished_metrics            # print + write
    python -m scripts.aggregate_polished_metrics --print-only
"""

from __future__ import annotations

import argparse
import statistics
import sys
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
RUNS_FILE = ORCH_DIR / "quality" / "polished_production_runs.yaml"
METRICS_FILE = ORCH_DIR / "quality" / "polished_production_metrics.yaml"


def load_runs() -> list[dict]:
    """Load runs — SQLite primary (v3 schema), YAML fallback for legacy entries.

    Source of truth precedence:
      1. SQLite polished_runs table
      2. YAML file (legacy / fallback)

    Returns whichever source has more entries (handles migration period
    where SQLite may still be backfilling from YAML).
    """
    sources: list[list[dict]] = []

    # Source 1: SQLite (preferred)
    try:
        import sys as _sys
        _sys.path.insert(0, str(Path.home() / ".claude" / "orchestrator"))
        from core.db import DB
        db_rows = DB().get_polished_runs()
        if db_rows:
            sources.append(db_rows)
    except Exception:
        pass

    # Source 2: YAML legacy
    if RUNS_FILE.exists():
        with open(RUNS_FILE, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        yaml_entries = data.get("runs") or []
        if yaml_entries:
            sources.append(yaml_entries)

    if not sources:
        return []
    sources.sort(key=len, reverse=True)
    return sources[0]


def _legacy_load_runs() -> list[dict]:
    """Legacy YAML-only loader, kept for tests / fallback compatibility."""
    if not RUNS_FILE.exists():
        return []
    with open(RUNS_FILE, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("runs") or []


def aggregate(runs: list[dict], window_days: int | None = None) -> dict:
    """Compute per-skill + overall metrics. window_days=None means all-time."""
    if window_days is not None:
        cutoff = datetime.now(UTC) - timedelta(days=window_days)
        runs = [r for r in runs if _parse_ts(r.get("ts")) >= cutoff]

    per_skill: dict[str, list[dict]] = defaultdict(list)
    for r in runs:
        per_skill[r["skill"]].append(r)

    skill_metrics = {}
    for skill, skill_runs in per_skill.items():
        total = len(skill_runs)
        passed = [r for r in skill_runs if r["gate_decision"] != "aborted"]
        aborted = total - len(passed)

        if passed:
            lifts = [r["lift_pts"] for r in passed]
            mean_lift = round(statistics.mean(lifts), 2)
            stdev_lift = round(statistics.stdev(lifts), 2) if len(lifts) > 1 else 0.0
        else:
            mean_lift = None
            stdev_lift = None

        skill_metrics[skill] = {
            "n_runs": total,
            "n_passed": len(passed),
            "n_aborted": aborted,
            "gate_pass_rate": round(len(passed) / total, 3) if total else 0.0,
            "mean_lift_pts": mean_lift,
            "stdev_lift_pts": stdev_lift,
        }

    # Overall (cross-skill on passed runs only)
    all_passed = [r for r in runs if r["gate_decision"] != "aborted"]
    if all_passed:
        all_lifts = [r["lift_pts"] for r in all_passed]
        overall = {
            "n_runs": len(runs),
            "n_passed": len(all_passed),
            "n_aborted": len(runs) - len(all_passed),
            "gate_pass_rate": round(len(all_passed) / len(runs), 3) if runs else 0.0,
            "mean_lift_pts": round(statistics.mean(all_lifts), 2),
            "stdev_lift_pts": round(statistics.stdev(all_lifts), 2) if len(all_lifts) > 1 else 0.0,
        }
    else:
        overall = {
            "n_runs": len(runs), "n_passed": 0, "n_aborted": len(runs),
            "gate_pass_rate": 0.0, "mean_lift_pts": None, "stdev_lift_pts": None,
        }

    return {"per_skill": skill_metrics, "overall": overall}


def _parse_ts(ts: str | None) -> datetime:
    if not ts:
        return datetime.min.replace(tzinfo=UTC)
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return datetime.min.replace(tzinfo=UTC)


def render_table(label: str, agg: dict) -> str:
    overall = agg["overall"]
    lines = [
        f"=== {label} (n={overall['n_runs']}) ===",
        f"  Gate pass rate: {overall['gate_pass_rate']*100:.1f}% ({overall['n_passed']}/{overall['n_runs']})",
    ]
    if overall["mean_lift_pts"] is not None:
        lines.append(f"  Mean lift on passed: +{overall['mean_lift_pts']}pts (std {overall['stdev_lift_pts']})")
    else:
        lines.append("  Mean lift: n/a (no passed runs)")
    lines.append("")
    lines.append(f"  {'skill':<35} {'runs':>5} {'pass%':>6} {'lift':>7}")
    for skill in sorted(agg["per_skill"]):
        m = agg["per_skill"][skill]
        lift = f"+{m['mean_lift_pts']}" if m['mean_lift_pts'] is not None else "n/a"
        lines.append(
            f"  {skill:<35} {m['n_runs']:>5} {m['gate_pass_rate']*100:>5.1f}% {lift:>7}"
        )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--print-only", action="store_true",
                    help="Print to stdout but don't write metrics yaml")
    args = ap.parse_args()

    runs = load_runs()
    if not runs:
        print("[aggregate] No runs found at", RUNS_FILE, file=sys.stderr)
        return 0

    agg_30 = aggregate(runs, window_days=30)
    agg_all = aggregate(runs, window_days=None)

    print(render_table("Last 30 days", agg_30))
    print()
    print(render_table("All time", agg_all))

    if args.print_only:
        return 0

    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    out = {
        "computed_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "last_30_days": agg_30,
        "all_time": agg_all,
    }
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        yaml.safe_dump(out, f, sort_keys=False, allow_unicode=True)

    print(f"\n[aggregate] Wrote {METRICS_FILE}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
