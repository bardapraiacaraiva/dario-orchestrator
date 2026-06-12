"""Acceptance tests for per-step durability (Next-Gen N2, 2026-06-12).

The N2 contract: a crash mid-wave must not lose paid-for work. Scenario
under test — a 3-task wave dies mid-flight:

  task 1: completed before the crash            -> untouched
  task 2: API call done, finalize never ran     -> finalize REPLAYED from the
                                                   journal, API NOT re-called
  task 3: never started                          -> untouched (still todo)

Plus: the SLA reaper must NOT reset a resumable task (resetting would make
the next wave re-pay the API call), and journal writes must be append-only
records of the lifecycle.
"""

import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import pytest

from core.db import DB
from execution import lifecycle

LONG_OUTPUT = ("## Deliverable\n" + "Substantive client-ready content line.\n" * 20
               + "## Summary\nProbe deliverable for the durability test.")


def _mk(db, tid, status, skill="dario-content"):
    db.create_task({"id": tid, "title": f"wave probe {tid}", "description": "p",
                    "project": "test", "priority": "medium",
                    "assignee": "worker-x", "skill": skill})
    if status != "todo":
        db.update_task(tid, {"status": status})


@pytest.fixture
def crashed_wave(tmp_path):
    """A 3-task wave interrupted mid-flight (simulated crash state)."""
    db = DB(db_path=str(tmp_path / "test.db"))
    _mk(db, "W-1", "done")
    _mk(db, "W-2", "in_progress")
    _mk(db, "W-3", "todo")
    # W-2: the API call completed and was journaled; finalize never ran.
    db.journal_step("W-2", "checked_out", payload={"source": "api", "model": "sonnet"})
    db.journal_step("W-2", "executed", payload={
        "output": LONG_OUTPUT, "input_tokens": 800, "output_tokens": 400,
        "total_tokens": 1200, "cost": 0.012, "model": "sonnet", "rubric": {}})
    return db


@pytest.fixture
def quiet_engines(monkeypatch):
    monkeypatch.setattr(lifecycle, "run_engine",
                        lambda script, args, timeout=30: {"pass": True, "action": "retry_same"})


def test_resume_replays_only_the_interrupted_task(crashed_wave, quiet_engines, monkeypatch):
    db = crashed_wave
    from providers import anthropic as api

    api_calls = []
    monkeypatch.setattr(api, "call_claude_api",
                        lambda *a, **k: api_calls.append(a) or {"success": False})
    monkeypatch.setattr(api, "auto_score_output", lambda out, rub, task: {"score": 75})

    res = api.resume_interrupted(db=db)

    # W-2 finalized from the journal — done, with the journaled tokens
    assert [r["task_id"] for r in res["resumed"]] == ["W-2"]
    w2 = db.get_task("W-2")
    assert w2["status"] == "done"
    assert w2["actual_tokens"] == 1200
    # the API was NEVER re-called (the whole point of the journal)
    assert api_calls == []
    # the rest of the wave is untouched
    assert db.get_task("W-1")["status"] == "done"
    assert db.get_task("W-3")["status"] == "todo"
    # journal now closes the loop
    fin = db.last_journal_step("W-2", "finalized")
    assert fin and fin["status"] == "done"


def test_resume_is_idempotent(crashed_wave, quiet_engines, monkeypatch):
    db = crashed_wave
    from providers import anthropic as api
    monkeypatch.setattr(api, "auto_score_output", lambda out, rub, task: {"score": 75})

    first = api.resume_interrupted(db=db)
    second = api.resume_interrupted(db=db)
    assert len(first["resumed"]) == 1
    assert second["resumed"] == []  # nothing left to replay


def test_sla_reaper_skips_resumable_tasks(crashed_wave):
    """Resetting a resumable task would re-pay the API call — the reaper
    must leave it for resume_interrupted and reset only journal-less orphans."""
    db = crashed_wave
    past = (datetime.now(UTC) - timedelta(hours=30)).isoformat()
    _mk(db, "W-4", "in_progress")  # orphan WITHOUT journal
    for tid in ("W-2", "W-4"):
        # the SLA clock runs from checked_out_at (default policy: 8h → 30h = critical breach)
        with db._conn() as conn:
            conn.execute("UPDATE tasks SET checked_out_at = ? WHERE id = ?", (past, tid))

    from core.sla import recover_orphaned
    rec = recover_orphaned(db=db)

    assert [t["id"] for t in rec["resumable"]] == ["W-2"]
    assert [t["id"] for t in rec["tasks"]] == ["W-4"]
    assert db.get_task("W-2")["status"] == "in_progress"  # preserved for replay
    assert db.get_task("W-4")["status"] == "todo"          # classic reset


def test_lifecycle_writes_checkout_and_finalize_journal(tmp_path, quiet_engines, monkeypatch):
    db = DB(db_path=str(tmp_path / "test.db"))
    _mk(db, "J-1", "todo")
    import safety.guardrails as guardrails
    monkeypatch.setattr(guardrails, "validate_task",
                        lambda task_id: {"verdict": "PASS", "checks": {}})
    import safety.approval_gates as gates
    monkeypatch.setattr(gates, "get_approval_level", lambda task: {"needs_approval": False})

    prep = lifecycle.prepare("J-1", db=db, source="api")
    assert prep["ok"]
    assert db.last_journal_step("J-1", "checked_out") is not None

    task = db.get_task("J-1")
    lifecycle.finalize_success("J-1", task, LONG_OUTPUT, tokens=500, score=80,
                               db=db, source="api", model="sonnet",
                               final_status="done", quality_score_for_filter=None,
                               count_budget_on_tripwire=True, meter_tokens=False)
    fin = db.last_journal_step("J-1", "finalized")
    assert fin and fin["status"] == "done" and fin["payload"]["score"] == 80
