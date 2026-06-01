"""Behavior tests for budget_tracker monthly attribution fix (Faixa 3 #1b).

The bug: scan_tasks_for_tokens() summed actual_tokens across ALL tasks
regardless of when they completed, then took max(budget, scan_total).
After Faixa 3 #1 backfill that inflated May 2026 to 369.7%.

The fix: filter by task.completed_at month, no more max() collusion.
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest
import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


@pytest.fixture
def isolated_tasks(tmp_path, monkeypatch):
    """Redirect task dirs to tmp_path so we don't pollute live state."""
    fake_active = tmp_path / "tasks" / "active"
    fake_done = tmp_path / "tasks" / "done"
    fake_active.mkdir(parents=True)
    fake_done.mkdir(parents=True)
    import finance.budget_tracker as bt
    monkeypatch.setattr(bt, "TASKS_ACTIVE", fake_active)
    monkeypatch.setattr(bt, "TASKS_DONE", fake_done)
    # budget_tracker is DB-first in production (2026-06-01 divergence fix). These
    # tests control input via YAML fixtures, so force the YAML loader here.
    monkeypatch.setattr(bt, "_load_budget_tasks", bt._load_tasks_from_yaml)
    return tmp_path


def _write_task(dir_path: Path, task_id: str, body: dict):
    with open(dir_path / f"{task_id}.yaml", "w", encoding="utf-8") as f:
        yaml.dump(body, f, allow_unicode=True)


class TestTaskMonth:

    def test_uses_completed_at_first(self):
        from finance.budget_tracker import _task_month
        assert _task_month({
            "completed_at": "2026-05-15T10:00:00Z",
            "checked_out_at": "2026-04-01T10:00:00Z",
        }) == "2026-05"

    def test_falls_back_to_checked_out_at_before_token_capture(self):
        """checked_out_at MUST win over last_token_capture_at — backfill bug fix."""
        from finance.budget_tracker import _task_month
        assert _task_month({
            "last_token_capture_at": "2026-05-26T10:00:00Z",  # backfill timestamp
            "checked_out_at": "2026-04-01T10:00:00Z",         # real work month
        }) == "2026-04"

    def test_token_capture_is_last_resort_only(self):
        """last_token_capture_at only counts when no other timestamp exists."""
        from finance.budget_tracker import _task_month
        assert _task_month({
            "last_token_capture_at": "2026-05-26T10:00:00Z",
        }) == "2026-05"

    def test_falls_back_to_checked_out_at(self):
        from finance.budget_tracker import _task_month
        assert _task_month({"checked_out_at": "2026-02-01T10:00:00Z"}) == "2026-02"

    def test_no_timestamps_returns_none(self):
        from finance.budget_tracker import _task_month
        assert _task_month({}) is None
        assert _task_month({"completed_at": ""}) is None
        assert _task_month({"completed_at": "garbage"}) is None


class TestScanMonthlyFilter:

    def test_unfiltered_sums_everything(self, isolated_tasks):
        from finance.budget_tracker import scan_tasks_for_tokens
        active = isolated_tasks / "tasks" / "active"
        done = isolated_tasks / "tasks" / "done"
        _write_task(done, "OLD-001", {
            "id": "OLD-001", "completed_at": "2026-03-15T10:00:00Z",
            "actual_tokens": 1_000_000, "project": "old", "skill": "x",
        })
        _write_task(done, "NEW-001", {
            "id": "NEW-001", "completed_at": "2026-05-20T10:00:00Z",
            "actual_tokens": 500_000, "project": "new", "skill": "y",
        })
        totals = scan_tasks_for_tokens()  # No month filter
        assert totals["total"] == 1_500_000
        assert totals["tasks_counted"] == 2
        assert totals["tasks_skipped_month"] == 0

    def test_filtered_by_month_excludes_others(self, isolated_tasks):
        from finance.budget_tracker import scan_tasks_for_tokens
        active = isolated_tasks / "tasks" / "active"
        done = isolated_tasks / "tasks" / "done"
        _write_task(done, "OLD-001", {
            "id": "OLD-001", "completed_at": "2026-03-15T10:00:00Z",
            "actual_tokens": 1_000_000, "project": "old", "skill": "x",
        })
        _write_task(done, "NEW-001", {
            "id": "NEW-001", "completed_at": "2026-05-20T10:00:00Z",
            "actual_tokens": 500_000, "project": "new", "skill": "y",
        })
        totals = scan_tasks_for_tokens(month="2026-05")
        assert totals["total"] == 500_000
        assert totals["tasks_counted"] == 1
        assert totals["tasks_skipped_month"] == 1
        assert "old" not in totals["by_project"]
        assert totals["by_project"]["new"] == 500_000

    def test_filter_uses_completed_at_priority(self, isolated_tasks):
        """Task with completed_at in May and checked_out_at in April → counts for May."""
        from finance.budget_tracker import scan_tasks_for_tokens
        done = isolated_tasks / "tasks" / "done"
        _write_task(done, "SPAN-001", {
            "id": "SPAN-001",
            "checked_out_at": "2026-04-30T22:00:00Z",
            "completed_at": "2026-05-01T02:00:00Z",
            "actual_tokens": 100_000, "project": "x", "skill": "y",
        })
        totals_may = scan_tasks_for_tokens(month="2026-05")
        assert totals_may["total"] == 100_000
        totals_apr = scan_tasks_for_tokens(month="2026-04")
        assert totals_apr["total"] == 0

    def test_zero_tokens_filtered_out(self, isolated_tasks):
        from finance.budget_tracker import scan_tasks_for_tokens
        done = isolated_tasks / "tasks" / "done"
        _write_task(done, "EMPTY-001", {
            "id": "EMPTY-001", "completed_at": "2026-05-20T10:00:00Z",
            "actual_tokens": 0, "project": "x", "skill": "y",
        })
        _write_task(done, "REAL-001", {
            "id": "REAL-001", "completed_at": "2026-05-20T10:00:00Z",
            "actual_tokens": 5000, "project": "x", "skill": "y",
        })
        totals = scan_tasks_for_tokens(month="2026-05")
        assert totals["total"] == 5000
        assert totals["tasks_counted"] == 1

    def test_missing_completed_at_uses_fallback(self, isolated_tasks):
        from finance.budget_tracker import scan_tasks_for_tokens
        done = isolated_tasks / "tasks" / "done"
        _write_task(done, "FALL-001", {
            "id": "FALL-001",
            "last_token_capture_at": "2026-05-10T10:00:00Z",
            "actual_tokens": 7000, "project": "x", "skill": "y",
        })
        totals = scan_tasks_for_tokens(month="2026-05")
        assert totals["total"] == 7000

    def test_no_timestamps_excluded_from_filter(self, isolated_tasks):
        """Tasks without any month-bearing field are excluded from filtered scans."""
        from finance.budget_tracker import scan_tasks_for_tokens
        done = isolated_tasks / "tasks" / "done"
        _write_task(done, "NOTS-001", {
            "id": "NOTS-001", "actual_tokens": 3000, "project": "x", "skill": "y",
        })
        totals_filtered = scan_tasks_for_tokens(month="2026-05")
        assert totals_filtered["total"] == 0
        assert totals_filtered["tasks_skipped_month"] == 1
        totals_unfiltered = scan_tasks_for_tokens()
        assert totals_unfiltered["total"] == 3000
