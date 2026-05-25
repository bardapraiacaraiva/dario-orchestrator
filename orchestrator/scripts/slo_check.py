#!/usr/bin/env python3
"""DARIO SLO Check — measures 3 SLOs defined in SLOs.md.

Outputs:
  - quality/slo_status.yaml   current per-SLO state
  - quality/slo_violations.jsonl  append-only history of breaches

Usage:
  python scripts/slo_check.py             pretty print + write files
  python scripts/slo_check.py --json      stdout JSON for dashboards
  python scripts/slo_check.py --quiet     write files only, no stdout
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ORCH = Path.home() / ".claude" / "orchestrator"
QUALITY = ORCH / "quality"

NOW = datetime.now(UTC)


# ─── SLO 1: dispatch latency ────────────────────────────────────────────


def slo_dispatch_latency() -> dict:
    """Run dispatch_engine --status with a 30s timeout; record duration."""
    start = time.perf_counter()
    try:
        result = subprocess.run(
            [sys.executable, str(ORCH / "dispatch_engine.py"), "--status"],
            capture_output=True, text=True, timeout=30, cwd=str(ORCH),
        )
        duration_s = time.perf_counter() - start
        ok = result.returncode == 0
    except subprocess.TimeoutExpired:
        duration_s = 30.0
        ok = False

    target_s = 5.0
    return {
        "slo": "dispatch_latency",
        "target_s": target_s,
        "actual_s": round(duration_s, 3),
        "exit_ok": ok,
        "status": "ok" if (ok and duration_s <= target_s) else "violation",
        "details": f"dispatch --status took {duration_s:.2f}s (target ≤{target_s}s)",
    }


# ─── SLO 2: budget freshness ────────────────────────────────────────────


def slo_budget_freshness() -> dict:
    """Check current month's budget file has `last_updated` within 6h."""
    target_age_h = 6.0
    month_yaml = ORCH / "budgets" / f"{NOW.strftime('%Y-%m')}.yaml"
    if not month_yaml.exists():
        return {
            "slo": "budget_freshness",
            "target_age_h": target_age_h,
            "actual_age_h": None,
            "status": "no_data",
            "details": f"no budget file for {NOW.strftime('%Y-%m')} (orchestrator may not have run this month)",
        }
    try:
        data = yaml.safe_load(month_yaml.read_text(encoding="utf-8")) or {}
    except Exception as e:
        return {
            "slo": "budget_freshness",
            "target_age_h": target_age_h,
            "actual_age_h": None,
            "status": "error",
            "details": f"failed to parse: {e}",
        }
    last_updated = data.get("last_updated")
    if not last_updated:
        return {
            "slo": "budget_freshness",
            "target_age_h": target_age_h,
            "actual_age_h": None,
            "status": "no_data",
            "details": "budget file present but no last_updated key",
        }
    try:
        ts = datetime.fromisoformat(str(last_updated).replace("Z", "+00:00"))
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=UTC)
        age_h = (NOW - ts).total_seconds() / 3600
    except Exception as e:
        return {
            "slo": "budget_freshness",
            "target_age_h": target_age_h,
            "actual_age_h": None,
            "status": "error",
            "details": f"bad last_updated timestamp: {e}",
        }
    return {
        "slo": "budget_freshness",
        "target_age_h": target_age_h,
        "actual_age_h": round(age_h, 1),
        "status": "ok" if age_h <= target_age_h else "violation",
        "details": f"budget file {age_h:.1f}h stale (target ≤{target_age_h}h)",
    }


# ─── SLO 3: pulse cadence ───────────────────────────────────────────────


def slo_pulse_cadence() -> dict:
    """Check cron_daily ran within last 26h."""
    target_h = 26.0
    # cron_daily writes to cron/last_run.yaml with key `ran_at`
    last_run = ORCH / "cron" / "last_run.yaml"
    if not last_run.exists():
        return {
            "slo": "pulse_cadence",
            "target_h": target_h,
            "actual_h": None,
            "status": "no_data",
            "details": f"no {last_run.relative_to(ORCH)} — cron_daily may have never run",
        }
    try:
        data = yaml.safe_load(last_run.read_text(encoding="utf-8")) or {}
    except Exception as e:
        return {
            "slo": "pulse_cadence",
            "target_h": target_h,
            "actual_h": None,
            "status": "error",
            "details": f"failed to parse cron/last_run.yaml: {e}",
        }
    last_completed = data.get("ran_at") or data.get("last_completed_at") or data.get("completed_at") or data.get("timestamp")
    if not last_completed:
        return {
            "slo": "pulse_cadence",
            "target_h": target_h,
            "actual_h": None,
            "status": "no_data",
            "details": "last_run.yaml present but no completed_at key",
        }
    try:
        ts = datetime.fromisoformat(str(last_completed).replace("Z", "+00:00"))
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=UTC)
        age_h = (NOW - ts).total_seconds() / 3600
    except Exception as e:
        return {
            "slo": "pulse_cadence",
            "target_h": target_h,
            "actual_h": None,
            "status": "error",
            "details": f"bad last_completed timestamp: {e}",
        }
    return {
        "slo": "pulse_cadence",
        "target_h": target_h,
        "actual_h": round(age_h, 1),
        "status": "ok" if age_h <= target_h else "violation",
        "details": f"cron_daily last ran {age_h:.1f}h ago (target ≤{target_h}h)",
    }


# ─── Driver ─────────────────────────────────────────────────────────────


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true", help="JSON output to stdout")
    p.add_argument("--quiet", action="store_true", help="silent except errors")
    args = p.parse_args()

    checks = [slo_dispatch_latency(), slo_budget_freshness(), slo_pulse_cadence()]
    summary = {
        "timestamp": NOW.isoformat(),
        "total_slos": len(checks),
        "ok": sum(1 for c in checks if c["status"] == "ok"),
        "violations": sum(1 for c in checks if c["status"] == "violation"),
        "no_data": sum(1 for c in checks if c["status"] == "no_data"),
        "errors": sum(1 for c in checks if c["status"] == "error"),
        "checks": checks,
    }

    # Persist
    QUALITY.mkdir(parents=True, exist_ok=True)
    (QUALITY / "slo_status.yaml").write_text(
        yaml.safe_dump(summary, sort_keys=False), encoding="utf-8"
    )
    # Append violations to history
    violations = [c for c in checks if c["status"] == "violation"]
    if violations:
        log = QUALITY / "slo_violations.jsonl"
        with log.open("a", encoding="utf-8") as f:
            for v in violations:
                f.write(json.dumps({"timestamp": NOW.isoformat(), **v}) + "\n")

    if args.json:
        print(json.dumps(summary, indent=2))
        return

    if args.quiet:
        return 1 if summary["violations"] else 0

    # Pretty
    print(f"\n═══ DARIO SLO Check — {NOW.strftime('%Y-%m-%d %H:%M:%S UTC')} ═══")
    for c in checks:
        emoji = {"ok": "✅", "violation": "🔴", "no_data": "⚪", "error": "💥"}[c["status"]]
        print(f"  {emoji} {c['slo']:<20} {c['status']:<10} {c['details']}")
    print(f"\n  Summary: {summary['ok']}/{summary['total_slos']} ok · "
          f"{summary['violations']} violations · {summary['no_data']} no-data · "
          f"{summary['errors']} errors")
    print(f"  Written: quality/slo_status.yaml")
    if violations:
        print(f"  Logged:  quality/slo_violations.jsonl (+{len(violations)} entries)")
    return 1 if summary["violations"] else 0


if __name__ == "__main__":
    sys.exit(main())
