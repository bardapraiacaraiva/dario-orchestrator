"""Behavior tests for the execution timeline collector (Next-Gen N3, 2026-06-12).

The /timeline page is rendered from get_timeline() — these tests pin the
feed's contract against an isolated DB with N2 journal data: in-flight tasks
always appear, journal steps ride along, the resumable flag mirrors the N2
executed-but-not-finalized condition, and old idle tasks fall outside the
window.
"""

import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import pytest

from core.db import DB
from observability.timeline import TIMELINE_HTML, get_timeline


@pytest.fixture
def db(tmp_path):
    d = DB(db_path=str(tmp_path / "test.db"))
    for tid, status in (("T-RUN", "in_progress"), ("T-DONE", "done"), ("T-OLD", "done")):
        d.create_task({"id": tid, "title": f"probe {tid}", "description": "p",
                       "project": "test", "priority": "medium",
                       "assignee": "worker-x", "skill": "dario-content"})
        if status != "todo":
            d.update_task(tid, {"status": status})
    # T-OLD: activity far outside the 24h window
    old = (datetime.now(UTC) - timedelta(days=9)).isoformat()
    with d._conn() as conn:
        conn.execute("UPDATE tasks SET updated_at = ? WHERE id = 'T-OLD'", (old,))
    # T-RUN: journal shows the API output exists but finalize never ran
    d.journal_step("T-RUN", "checked_out", payload={"source": "api"})
    d.journal_step("T-RUN", "executed", payload={"output": "x" * 600})
    # T-DONE: full cycle closed
    d.journal_step("T-DONE", "checked_out")
    d.journal_step("T-DONE", "executed")
    d.journal_step("T-DONE", "finalized", status="done")
    return d


def test_timeline_shape_and_window(db):
    feed = get_timeline(db, hours=24)
    ids = [t["id"] for t in feed["tasks"]]
    assert "T-RUN" in ids and "T-DONE" in ids
    assert "T-OLD" not in ids  # idle outside the window
    assert feed["counts"]["in_progress"] == 1
    assert feed["window_hours"] == 24


def test_timeline_carries_journal_steps(db):
    feed = get_timeline(db)
    by_id = {t["id"]: t for t in feed["tasks"]}
    run_steps = [s["step"] for s in by_id["T-RUN"]["steps"]]
    assert run_steps == ["checked_out", "executed"]
    done_steps = [s["step"] for s in by_id["T-DONE"]["steps"]]
    assert done_steps == ["checked_out", "executed", "finalized"]


def test_resumable_flag_mirrors_n2_condition(db):
    feed = get_timeline(db)
    by_id = {t["id"]: t for t in feed["tasks"]}
    assert by_id["T-RUN"]["resumable"] is True    # executed, never finalized
    assert by_id["T-DONE"]["resumable"] is False  # cycle closed


def test_timeline_is_read_only(db):
    before = {t["id"]: t["status"] for t in db.get_tasks()}
    get_timeline(db)
    after = {t["id"]: t["status"] for t in db.get_tasks()}
    assert before == after


def test_page_polls_the_feed():
    assert "/api/timeline" in TIMELINE_HTML
    assert "EventSource" in TIMELINE_HTML  # SSE ticker enhancement
