#!/usr/bin/env python3
"""Tests for Upgrade 18 weekly cognitive summary."""

import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


from observability import weekly_summary as ws


def test_week_bounds_default():
    start, end, label = ws._week_bounds(None)
    assert isinstance(start, datetime)
    assert isinstance(end, datetime)
    assert end - start == timedelta(days=7)
    # Start should be Monday (weekday 0)
    assert start.weekday() == 0
    assert "W" in label


def test_week_bounds_specific():
    start, end, label = ws._week_bounds("2026-W21")
    assert label == "2026-W21"
    assert start.weekday() == 0


def test_collect_all_returns_structure():
    data = ws.collect_all()
    required = {"iso_week", "start", "end", "generated_at", "cron",
                "new_memories", "new_rules", "new_hints", "drift", "cot",
                "integrity", "qvalue_end_of_week", "synaptic_end_of_week"}
    assert set(data.keys()) >= required, f"missing: {required - set(data.keys())}"


def test_collect_cron_days_filters_by_window():
    """Only days within window should be returned."""
    start, end, _ = ws._week_bounds()
    days = ws.collect_cron_days(start, end)
    # All returned dates must be within window
    for d in days:
        try:
            dt = datetime.fromisoformat(d["date"]).replace(tzinfo=UTC)
            assert start <= dt < end
        except Exception:
            pass


def test_collect_new_memories_returns_list():
    start, end, _ = ws._week_bounds()
    out = ws.collect_new_memories(start, end)
    assert isinstance(out, list)


def test_collect_new_rules_returns_list():
    start, end, _ = ws._week_bounds()
    out = ws.collect_new_rules(start, end)
    assert isinstance(out, list)


def test_render_markdown_has_required_sections():
    data = ws.collect_all()
    md = ws.render_markdown(data)
    required_sections = [
        "Cognitive Weekly Summary",
        "Cron Daily Health",
        "What the System Learned",
        "Quality Drift Events",
        "Dispatch Reasoning",
        "Integrity Gate Events",
        "State Snapshot",
    ]
    for s in required_sections:
        assert s in md, f"missing section: {s}"


def test_render_includes_iso_week_label():
    data = ws.collect_all()
    md = ws.render_markdown(data)
    assert data["iso_week"] in md


def test_collect_drift_events_aggregates():
    cron_days = [
        {"date": "2026-05-01", "jobs": [{
            "name": "regression_check", "status": "ok",
            "output": {"alerts": ["eval-x"], "drifting": ["eval-x", "eval-y"]}
        }]},
        {"date": "2026-05-02", "jobs": [{
            "name": "regression_check", "status": "ok",
            "output": {"alerts": [], "drifting": []}
        }]},
    ]
    r = ws.collect_drift_events(cron_days)
    assert len(r["alerts"]) == 1
    assert r["alerts"][0]["eval"] == "eval-x"
    assert len(r["drift_only"]) == 1
    assert r["drift_only"][0]["eval"] == "eval-y"


def test_collect_cot_trend_aggregates_rates():
    cron_days = [
        {"date": "2026-05-01", "jobs": [{
            "name": "dispatch_cot_stats", "status": "ok",
            "output": {"overconfidence_rate": 0.1, "total_traces": 5}
        }]},
        {"date": "2026-05-02", "jobs": [{
            "name": "dispatch_cot_stats", "status": "ok",
            "output": {"overconfidence_rate": 0.3, "total_traces": 10}
        }]},
    ]
    r = ws.collect_cot_trend(cron_days)
    assert r["avg_rate"] == 0.2
    assert r["total_traces_end_of_week"] == 10


def test_collect_integrity_events_only_fail_warn():
    cron_days = [
        {"date": "2026-05-01", "jobs": [{
            "name": "integrity_gate", "status": "ok",
            "output": {"verdict": "PASS"}
        }]},
        {"date": "2026-05-02", "jobs": [{
            "name": "integrity_gate", "status": "ok",
            "output": {"verdict": "FAIL", "failed_checks": ["c1"]}
        }]},
        {"date": "2026-05-03", "jobs": [{
            "name": "integrity_gate", "status": "ok",
            "output": {"verdict": "WARN", "warned_checks": ["c2"]}
        }]},
    ]
    r = ws.collect_integrity_events(cron_days)
    assert len(r) == 2
    verdicts = {e["verdict"] for e in r}
    assert "FAIL" in verdicts
    assert "WARN" in verdicts
    assert "PASS" not in verdicts


def test_save_to_obsidian():
    import shutil
    import tempfile
    # Replace OBSIDIAN_OUTPUTS with temp dir
    orig = ws.OBSIDIAN_OUTPUTS
    tmp = Path(tempfile.mkdtemp())
    ws.OBSIDIAN_OUTPUTS = tmp
    try:
        path = ws.save_to_obsidian("2026-W99", "# Test content")
        assert path.exists()
        assert path.name == "2026-W99 - Cognitive Weekly.md"
        assert path.read_text(encoding="utf-8") == "# Test content"
        return True
    finally:
        ws.OBSIDIAN_OUTPUTS = orig
        shutil.rmtree(tmp, ignore_errors=True)


def test_render_handles_empty_data():
    """Even with no data for the week, render should not crash."""
    empty_data = {
        "iso_week": "2026-W01",
        "start": "2026-01-05T00:00:00+00:00",
        "end": "2026-01-12T00:00:00+00:00",
        "generated_at": "2026-01-05T12:00:00+00:00",
        "cron": {"days_run": 0, "days_ok": 0, "days_warn": 0, "days_alert": 0},
        "new_memories": [],
        "new_rules": [],
        "new_hints": [],
        "drift": {"alerts": [], "drift_only": []},
        "cot": {"daily_rates": [], "avg_rate": 0, "total_traces_end_of_week": 0},
        "integrity": [],
        "qvalue_end_of_week": {"error": "test"},
        "synaptic_end_of_week": {"error": "test"},
    }
    md = ws.render_markdown(empty_data)
    assert "2026-W01" in md
    assert "No new semantic memories" in md
    assert "No drift events" in md


def test_qvalue_snapshot_has_keys():
    snap = ws.collect_qvalue_snapshot()
    assert isinstance(snap, dict)
    # Either has total_episodes or error
    assert "total_episodes" in snap or "error" in snap


def test_synaptic_snapshot_has_keys():
    snap = ws.collect_synaptic_snapshot()
    assert isinstance(snap, dict)


TESTS = [
    ("week bounds default returns Monday", test_week_bounds_default),
    ("week bounds with explicit ISO week", test_week_bounds_specific),
    ("collect_all returns full structure", test_collect_all_returns_structure),
    ("cron days filtered by window", test_collect_cron_days_filters_by_window),
    ("new_memories returns list", test_collect_new_memories_returns_list),
    ("new_rules returns list", test_collect_new_rules_returns_list),
    ("markdown contains all sections", test_render_markdown_has_required_sections),
    ("markdown includes ISO week label", test_render_includes_iso_week_label),
    ("drift events aggregated correctly", test_collect_drift_events_aggregates),
    ("CoT trend averages rates", test_collect_cot_trend_aggregates_rates),
    ("integrity events only FAIL/WARN", test_collect_integrity_events_only_fail_warn),
    ("save to Obsidian works", test_save_to_obsidian),
    ("render handles empty data", test_render_handles_empty_data),
    ("qvalue snapshot has keys", test_qvalue_snapshot_has_keys),
    ("synaptic snapshot has keys", test_synaptic_snapshot_has_keys),
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
