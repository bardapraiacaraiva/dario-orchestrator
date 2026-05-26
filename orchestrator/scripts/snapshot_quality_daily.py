#!/usr/bin/env python3
"""Append a daily quality snapshot to quality/quality_daily.yaml.

Designed to be called by the daily cron (same one that runs dream consolidation).
Each entry records the current global avg + delivery_ready rate so we can build
a sparkline over time. Append-only — never modifies existing entries.

Idempotent for the same day: if today's snapshot already exists, it overwrites
(captures latest state of the day rather than first state).
"""
from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

ORCH = Path.home() / ".claude" / "orchestrator"
METRICS_FILE = ORCH / "quality" / "skill-metrics.yaml"
SNAPSHOT_FILE = ORCH / "quality" / "quality_daily.yaml"


def load_metrics() -> dict:
    if not METRICS_FILE.exists():
        return {}
    with open(METRICS_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def compute_snapshot(metrics: dict) -> dict:
    """Extract the headline numbers we want to track over time."""
    skills = metrics.get("skills", {})
    scored_avgs = [
        s.get("avg_quality_score") for s in skills.values()
        if isinstance(s, dict) and isinstance(s.get("avg_quality_score"), (int, float))
    ]
    if scored_avgs:
        global_avg = sum(scored_avgs) / len(scored_avgs)
    else:
        global_avg = metrics.get("global_avg_quality", 0)

    delivery_rate = metrics.get("bundle_delivery_rate_pct")
    if delivery_rate is None:
        # Derive from delivery_ready counts if present
        yes = metrics.get("bundles_yes", 0)
        total = metrics.get("bundles_total", 0)
        delivery_rate = (yes / total * 100) if total else 0

    return {
        "date": datetime.now(UTC).date().isoformat(),
        "ts": datetime.now(UTC).isoformat(timespec="seconds"),
        "global_avg": round(float(global_avg), 1),
        "delivery_rate_pct": round(float(delivery_rate), 1),
        "n_skills_scored": len(scored_avgs),
    }


def append_snapshot(snapshot: dict) -> dict:
    """Write snapshot to YAML. Overwrites same-day entry if exists."""
    if SNAPSHOT_FILE.exists():
        with open(SNAPSHOT_FILE, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}
    data.setdefault("description", "Daily quality snapshot — driven by cron. Append-only-by-day.")
    data.setdefault("entries", [])

    # Overwrite same-day entry if exists; else append
    today = snapshot["date"]
    data["entries"] = [e for e in data["entries"] if e.get("date") != today]
    data["entries"].append(snapshot)
    data["entries"].sort(key=lambda e: e.get("date", ""))

    SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
    return snapshot


def main() -> int:
    metrics = load_metrics()
    snap = compute_snapshot(metrics)
    append_snapshot(snap)
    print(f"[snapshot_quality_daily] {snap['date']} · "
          f"avg={snap['global_avg']} · delivery={snap['delivery_rate_pct']}% · "
          f"n_skills={snap['n_skills_scored']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
