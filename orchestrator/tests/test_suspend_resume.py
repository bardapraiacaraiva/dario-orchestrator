"""Behavior proof for execution/suspend_resume.py (DD finding C2, 2026-06-12).

The runtime invoked this module at a root path that did not exist since the
2026-05-25 refactor — suspend/resume was a silent no-op for 18 days and the
module itself had ZERO tests. This is the missing proof: the full
checkpoint → suspend → resume cycle against an isolated DB.
"""

import json
import sys
from pathlib import Path

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import execution.suspend_resume as sr  # noqa: E402
from core.db import DB  # noqa: E402

TASK_ID = "SUSP-001"


@pytest.fixture
def db(tmp_path, monkeypatch):
    """Throwaway DB injected into every DB() call inside the module."""
    test_db = DB(db_path=str(tmp_path / "test.db"))
    monkeypatch.setattr(sr, "DB", lambda: test_db)
    test_db.create_task({
        "id": TASK_ID,
        "title": "suspend/resume probe",
        "description": "probe",
        "project": "test",
        "priority": "medium",
        "assignee": "worker-x",
        "skill": "dario-brand",
    })
    test_db.update_task(TASK_ID, {"status": "in_progress"})
    return test_db


def test_full_checkpoint_suspend_resume_cycle(db):
    # checkpoint while running
    cp = sr.save_checkpoint(TASK_ID, {"step_index": 3, "partial_output": "half-done", "tokens": 1200})
    assert cp["success"]

    # suspend: in_progress -> suspended, checkpoint preserved
    s = sr.suspend_task(TASK_ID)
    assert s["success"] and s["status"] == "suspended"
    task = db.get_task(TASK_ID)
    assert task["status"] == "suspended"
    stored = json.loads(task["blocked_reason"])
    assert stored["step_index"] == 3
    assert stored["previous_status"] == "in_progress"

    # resume: suspended -> todo (re-dispatch), resume point exposed
    r = sr.resume_task(TASK_ID)
    assert r["success"] and r["status"] == "todo"
    assert r["resume_from_step"] == 3
    assert db.get_task(TASK_ID)["status"] == "todo"


def test_suspend_rejects_non_running_and_resume_rejects_non_suspended(db):
    db.update_task(TASK_ID, {"status": "todo"})
    assert "error" in sr.suspend_task(TASK_ID)
    assert "error" in sr.resume_task(TASK_ID)
    assert "error" in sr.suspend_task("GHOST-999")


def test_suspend_all_only_touches_in_progress(db):
    db.create_task({
        "id": "SUSP-002", "title": "idle probe", "description": "p",
        "project": "test", "priority": "low", "assignee": "worker-x",
        "skill": "dario-brand",
    })  # stays todo
    out = sr.suspend_all()
    assert out["task_ids"] == [TASK_ID] and out["suspended"] == 1
    assert db.get_task("SUSP-002")["status"] == "todo"

    back = sr.restart_all()
    assert back["task_ids"] == [TASK_ID] and back["resumed"] == 1
    assert db.get_task(TASK_ID)["status"] == "todo"
