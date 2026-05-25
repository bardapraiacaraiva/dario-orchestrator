#!/usr/bin/env python3
"""Tests for Upgrade 12 cron daily background job."""

import shutil
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import pytest

import cron_daily

pytestmark = pytest.mark.slow

def _backup_last_run():
    if cron_daily.LAST_RUN_FILE.exists():
        backup = cron_daily.LAST_RUN_FILE.with_suffix(".yaml.test-bak")
        shutil.copy(cron_daily.LAST_RUN_FILE, backup)
        return backup
    return None


def _restore_last_run(backup):
    if backup and backup.exists():
        shutil.copy(backup, cron_daily.LAST_RUN_FILE)
        backup.unlink()


def test_dry_run_returns_skipped_jobs():
    r = cron_daily.run_all(dry_run=True)
    assert r["dry_run"] is True
    assert len(r["jobs"]) == 6  # cognitive + integrity + prompt hints
    for job in r["jobs"]:
        assert "skipped" in job["status"]


def test_run_all_executes_6_jobs():
    backup = _backup_last_run()
    try:
        r = cron_daily.run_all(dry_run=False)
        assert len(r["jobs"]) == 6
        job_names = {j["name"] for j in r["jobs"]}
        expected = {"promote_episodes", "regression_check",
                    "dispatch_cot_stats", "state_snapshot", "integrity_gate",
                    "prompt_hints_promote"}
        assert job_names == expected, f"got {job_names}"
        assert "status" in r
        assert r["status"] in ("ok", "warn", "alert")
        return True
    finally:
        _restore_last_run(backup)


def test_run_persists_report_file():
    backup = _backup_last_run()
    try:
        r = cron_daily.run_all(dry_run=False)
        report_file = Path(r["report_file"])
        assert report_file.exists()
        return True
    finally:
        _restore_last_run(backup)


def test_maybe_run_skips_within_cooldown():
    backup = _backup_last_run()
    try:
        cron_daily.run_all(dry_run=False)
        r = cron_daily.maybe_run(force=False)
        assert r.get("skipped") is True
        assert "cooldown" in r["reason"].lower()
        return True
    finally:
        _restore_last_run(backup)


def test_maybe_run_executes_when_stale():
    """If we manually backdate last_run to >22h ago, maybe_run should execute."""
    backup = _backup_last_run()
    try:
        old = (datetime.now(UTC) - timedelta(hours=30)).isoformat()
        cron_daily._dump_yaml(
            {"ran_at": old, "alerts": 0, "warnings": 0},
            str(cron_daily.LAST_RUN_FILE)
        )
        r = cron_daily.maybe_run(force=False)
        assert not r.get("skipped"), f"should have executed: {r}"
        assert "jobs" in r
        return True
    finally:
        _restore_last_run(backup)


def test_force_overrides_cooldown():
    backup = _backup_last_run()
    try:
        cron_daily.run_all(dry_run=False)
        r = cron_daily.maybe_run(force=True)
        assert not r.get("skipped"), "force=True should always execute"
        return True
    finally:
        _restore_last_run(backup)


def test_status_returns_structure():
    backup = _backup_last_run()
    try:
        cron_daily.run_all(dry_run=False)
        s = cron_daily.status()
        assert "last_run" in s
        assert "hours_since_last_run" in s
        assert "cooldown_hours" in s
        assert "recent_runs" in s
        assert s["hours_since_last_run"] < 1.0  # just ran
        return True
    finally:
        _restore_last_run(backup)


def test_alert_evaluation_detects_drift():
    """Synthetic test — feed a fake report with drift, check alert is raised."""
    fake_report = {
        "jobs": [
            {"name": "regression_check", "status": "ok", "output": {
                "drift_count": 2, "alert_count": 1,
                "alerts": ["eval-brand-01"],
                "drifting": ["eval-brand-01", "eval-seo-01"],
            }},
            {"name": "dispatch_cot_stats", "status": "ok", "output": {
                "overconfidence_rate": 0.05,
            }},
            {"name": "state_snapshot", "status": "ok", "output": {
                "qvalue": {"avg_q_value": 0.9},
            }},
        ],
    }
    alerts, warnings = cron_daily._evaluate_alerts(fake_report)
    assert any(a["source"] == "regression_check" for a in alerts)


def test_alert_evaluation_detects_overconfidence():
    fake_report = {
        "jobs": [
            {"name": "regression_check", "status": "ok",
             "output": {"drift_count": 0, "alert_count": 0,
                        "alerts": [], "drifting": []}},
            {"name": "dispatch_cot_stats", "status": "ok",
             "output": {"overconfidence_rate": 0.35}},
            {"name": "state_snapshot", "status": "ok", "output": {}},
        ],
    }
    alerts, warnings = cron_daily._evaluate_alerts(fake_report)
    assert any(a["source"] == "dispatch_cot" for a in alerts)


def test_alert_evaluation_detects_qvalue_drop():
    fake_report = {
        "jobs": [
            {"name": "regression_check", "status": "ok",
             "output": {"drift_count": 0, "alert_count": 0,
                        "alerts": [], "drifting": []}},
            {"name": "dispatch_cot_stats", "status": "ok",
             "output": {"overconfidence_rate": 0.05}},
            {"name": "state_snapshot", "status": "ok",
             "output": {"qvalue": {"avg_q_value": 0.3}}},
        ],
    }
    alerts, warnings = cron_daily._evaluate_alerts(fake_report)
    assert any(w["source"] == "qvalue_memory" for w in warnings)


def test_job_error_becomes_alert():
    fake_report = {
        "jobs": [
            {"name": "promote_episodes", "status": "error", "error": "DB locked"},
            {"name": "regression_check", "status": "ok",
             "output": {"drift_count": 0, "alert_count": 0,
                        "alerts": [], "drifting": []}},
            {"name": "dispatch_cot_stats", "status": "ok",
             "output": {"overconfidence_rate": 0.05}},
            {"name": "state_snapshot", "status": "ok", "output": {}},
        ],
    }
    alerts, _ = cron_daily._evaluate_alerts(fake_report)
    assert any(a["source"] == "promote_episodes" for a in alerts)
    assert any("job failed" in a["message"] for a in alerts)


def test_hours_since_last_run_calculation():
    backup = _backup_last_run()
    try:
        old = (datetime.now(UTC) - timedelta(hours=5)).isoformat()
        cron_daily._dump_yaml(
            {"ran_at": old, "alerts": 0, "warnings": 0},
            str(cron_daily.LAST_RUN_FILE)
        )
        h = cron_daily._hours_since_last_run()
        assert 4.5 < h < 5.5, f"expected ~5h, got {h}"
        return True
    finally:
        _restore_last_run(backup)


def test_never_run_returns_infinity():
    backup = _backup_last_run()
    try:
        if cron_daily.LAST_RUN_FILE.exists():
            cron_daily.LAST_RUN_FILE.unlink()
        h = cron_daily._hours_since_last_run()
        assert h == float("inf")
        return True
    finally:
        _restore_last_run(backup)


TESTS = [
    ("dry-run returns skipped jobs", test_dry_run_returns_skipped_jobs),
    ("run_all executes 6 jobs (incl. prompt hints)", test_run_all_executes_6_jobs),
    ("run persists report file", test_run_persists_report_file),
    ("maybe_run skips within cooldown", test_maybe_run_skips_within_cooldown),
    ("maybe_run executes when stale", test_maybe_run_executes_when_stale),
    ("--force overrides cooldown", test_force_overrides_cooldown),
    ("status returns expected structure", test_status_returns_structure),
    ("alert evaluation detects drift", test_alert_evaluation_detects_drift),
    ("alert evaluation detects overconfidence", test_alert_evaluation_detects_overconfidence),
    ("warning when Q-value drops", test_alert_evaluation_detects_qvalue_drop),
    ("job error becomes alert", test_job_error_becomes_alert),
    ("hours_since_last_run accurate", test_hours_since_last_run_calculation),
    ("never run returns infinity", test_never_run_returns_infinity),
]


def run():
    passed = 0
    failed = 0
    for name, fn in TESTS:
        try:
            ok = fn()
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] {name}")
            if ok:
                passed += 1
            else:
                failed += 1
        except AssertionError as e:
            print(f"  [FAIL] {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: CRASHED — {e}")
            failed += 1
    print()
    print(f"Results: {passed} passed, {failed} failed (of {len(TESTS)})")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
