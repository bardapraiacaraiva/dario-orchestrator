#!/usr/bin/env python3
"""Model drift detector — compares declared-vs-actual model per polished wrapper.

Closes audit Risk #10 (stamp + warn). Each polished wrapper declares
`tested_with_model: claude-opus-4-7` in its SKILL.md frontmatter. When
record_polished_run is called, it captures `model_used`. This script:

  1. Reads `tested_with_model` from each polished wrapper SKILL.md
  2. Reads recent polished_runs from SQLite
  3. For each run where model_used != tested_with_model: log drift event
  4. Idempotent: skips drift events already logged

Run modes:
  --scan             # default: scan since last_drift_check, log new events
  --since YYYY-MM-DD # explicit since date
  --since-hours N    # last N hours
  --all              # all-time (slow; useful first run)
  --report           # text report of drift events (no scan)
  --json             # JSON output

Exit codes:
  0 — no drift detected (or report mode)
  2 — drift detected (CI-friendly: non-zero alerts)
  3 — error
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"
ORCH_DIR = Path.home() / ".claude" / "orchestrator"

# Polished wrappers (Padrão A) — the ones tracked by drift detector
POLISHED_WRAPPERS = [
    "dario-pitch-polished",
    "dario-brand-polished",
    "dario-offer-polished",
    "dario-funnel-polished",
    "dario-sales-letter-polished",
    "dario-financial-model-polished",
    "dario-product-polished",
    "dario-wp-audit-polished",
]


def read_tested_with_model(skill_name: str) -> str | None:
    """Extract `tested_with_model:` field from skill's SKILL.md frontmatter.

    Returns None if not declared (drift detector skips that skill).
    """
    skill_md = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_md.is_file():
        return None
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError:
        return None

    in_fm = False
    for line in text.splitlines():
        if line.strip() == "---":
            if in_fm:
                break
            in_fm = True
            continue
        if in_fm and line.startswith("tested_with_model:"):
            value = line.split(":", 1)[1].strip().strip('"').strip("'")
            return value or None
    return None


def get_last_drift_check_iso(db) -> str | None:
    """Get the ts of the most recent drift event scan (used as 'since')."""
    events = db.get_drift_events()
    if not events:
        return None
    # events ordered DESC by ts in get_drift_events
    return events[0]["ts"]


def scan(db, since_iso: str | None, dry_run: bool) -> dict:
    """Scan polished_runs for drift since `since_iso`. Returns stats dict."""
    declarations: dict[str, str] = {}
    for w in POLISHED_WRAPPERS:
        declared = read_tested_with_model(w)
        if declared:
            declarations[w] = declared

    if not declarations:
        return {
            "wrappers_with_declaration": 0,
            "runs_scanned": 0,
            "skipped_no_model_used": 0,
            "drift_detected": 0,
            "logged": 0,
            "since": since_iso or "all-time",
            "note": "No wrappers declare tested_with_model — nothing to check",
        }

    # Fetch runs for those skills
    drift_found = 0
    logged = 0
    skipped_no_model = 0
    runs_scanned = 0

    for skill, declared in declarations.items():
        runs = db.get_polished_runs(skill=skill, since_iso=since_iso)
        runs_scanned += len(runs)
        for r in runs:
            actual = (r.get("model_used") or "").strip()
            if not actual:
                skipped_no_model += 1
                continue
            if actual == declared:
                continue
            # Drift!
            drift_found += 1
            if not dry_run:
                db.record_model_drift(
                    skill=skill,
                    declared_model=declared,
                    actual_model=actual,
                    severity="warning",
                    note=f"run {r['id']} at {r['ts']} (client={r.get('client', '?')})",
                    ts=r["ts"],  # use the run's ts for chronology
                )
                logged += 1

    return {
        "wrappers_with_declaration": len(declarations),
        "runs_scanned": runs_scanned,
        "skipped_no_model_used": skipped_no_model,
        "drift_detected": drift_found,
        "logged": logged,
        "since": since_iso or "all-time",
    }


def report(db, since_iso: str | None) -> dict:
    """Build a report of drift events (no DB writes)."""
    events = db.get_drift_events(since_iso=since_iso)
    by_skill: dict[str, list[dict]] = {}
    for e in events:
        by_skill.setdefault(e["skill"], []).append(e)
    return {
        "total_drift_events": len(events),
        "by_skill": {s: len(evts) for s, evts in by_skill.items()},
        "most_recent": events[:10] if events else [],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", action="store_true", help="Default: scan + log new drift")
    ap.add_argument("--since", help="ISO date for scan window")
    ap.add_argument("--since-hours", type=int, help="Scan last N hours")
    ap.add_argument("--all", action="store_true", help="Scan all-time (first run)")
    ap.add_argument("--report", action="store_true", help="Report mode (no scan)")
    ap.add_argument("--dry-run", action="store_true", help="Detect but don't log")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    sys.path.insert(0, str(ORCH_DIR))
    try:
        from core.db import DB
    except ImportError as e:
        print(f"DB module not available: {e}", file=sys.stderr)
        return 3
    db = DB()

    # Determine since_iso
    if args.all:
        since_iso = None
    elif args.since:
        since_iso = args.since
    elif args.since_hours:
        since_iso = (datetime.now(UTC) - timedelta(hours=args.since_hours)).isoformat(timespec="seconds")
    else:
        # Default: from last drift check, OR last 7 days if no prior checks
        last = get_last_drift_check_iso(db)
        if last:
            since_iso = last
        else:
            since_iso = (datetime.now(UTC) - timedelta(days=7)).isoformat(timespec="seconds")

    if args.report:
        result = report(db, since_iso=since_iso)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"=== Model Drift Report (since {since_iso or 'all-time'}) ===")
            print(f"  Total events: {result['total_drift_events']}")
            for skill, count in result["by_skill"].items():
                print(f"    {skill}: {count} drift events")
            if result["most_recent"]:
                print("\n  Most recent:")
                for e in result["most_recent"]:
                    print(f"    {e['ts']} {e['skill']}: {e['declared_model']} → {e['actual_model']}")
                    if e.get("note"):
                        print(f"      {e['note']}")
        return 0

    # Default: scan
    result = scan(db, since_iso=since_iso, dry_run=args.dry_run)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=== Model Drift Scan ===")
        print(f"  Window: {result.get('since')}")
        print(f"  Wrappers with declaration: {result['wrappers_with_declaration']}")
        print(f"  Runs scanned: {result['runs_scanned']}")
        print(f"  Skipped (no model_used): {result['skipped_no_model_used']}")
        print(f"  Drift detected: {result['drift_detected']}")
        print(f"  Drift events logged: {result['logged']}")
        if result.get("note"):
            print(f"  Note: {result['note']}")

    return 2 if result.get("drift_detected", 0) > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
