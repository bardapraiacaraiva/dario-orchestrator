"""Behavior tests for the unified execution lifecycle (Next-Gen N1, 2026-06-12).

Both engines (session executor + autonomous API) must be thin adapters over
execution/lifecycle.py. These tests pin the contract:
  - both engines route through lifecycle.prepare (no private copies),
  - prepare short-circuits on guardrails FAIL before any checkout,
  - the API path now hits the approval gate (it silently lacked it pre-N1),
  - finalize_failure computes the failure type instead of hardcoding it,
  - both pipelines are the same INSTANCE (composition cannot drift).
"""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import pytest

from core.db import DB
from execution import lifecycle

TASK_ID = "LIFE-001"


@pytest.fixture
def db(tmp_path):
    test_db = DB(db_path=str(tmp_path / "test.db"))
    test_db.create_task({
        "id": TASK_ID, "title": "lifecycle unification probe",
        "description": "probe task for the shared lifecycle",
        "project": "test", "priority": "medium",
        "assignee": "worker-x", "skill": "dario-brand",
    })
    return test_db


@pytest.fixture
def quiet_engines(monkeypatch):
    """Stub the subprocess engines (task_spec/context/rubric/tracer/replanner)
    so prepare/finalize run in-process and fast."""
    calls = []

    def fake_run_engine(script, args, timeout=30):
        calls.append((script, list(args)))
        return {"pass": True, "context_block": "", "dimensions_count": 5,
                "action": "retry_same"}

    monkeypatch.setattr(lifecycle, "run_engine", fake_run_engine)
    return calls


# ─── both engines share lifecycle.prepare ─────────────────────────────────


def test_both_engines_call_shared_prepare(monkeypatch):
    seen = []

    def fake_prepare(task_id, **kwargs):
        seen.append((task_id, kwargs.get("source")))
        return {"task_id": task_id, "ok": False, "status": "blocked",
                "error": "stub", "steps": []}

    monkeypatch.setattr(lifecycle, "prepare", fake_prepare)

    from execution import executor
    from providers import anthropic as api_engine

    executor.execute_task("X-1")
    api_engine.execute_task("X-2")

    sources = dict(seen)
    assert sources.get("X-1") == "session"
    assert sources.get("X-2") == "api"


def test_pipelines_are_the_same_instance():
    from execution.executor import PIPELINE
    from providers.anthropic import API_PIPELINE
    assert PIPELINE is API_PIPELINE is lifecycle.PIPELINE


# ─── prepare short-circuits ────────────────────────────────────────────────


def test_prepare_blocks_on_guardrails_fail(db, quiet_engines, monkeypatch):
    import safety.guardrails as guardrails
    monkeypatch.setattr(guardrails, "validate_task",
                        lambda task_id: {"verdict": "FAIL", "errors": ["nope"]})

    prep = lifecycle.prepare(TASK_ID, db=db, source="api")
    assert prep["ok"] is False
    assert prep["status"] == "blocked"
    assert "Guardrails" in prep["error"]
    # never checked out
    assert db.get_task(TASK_ID)["status"] != "in_progress"


def test_prepare_api_path_hits_approval_gate(db, quiet_engines, monkeypatch):
    """Pre-N1 the autonomous path executed approval-requiring skills
    unattended. The shared lifecycle must stop BOTH paths."""
    import safety.guardrails as guardrails
    monkeypatch.setattr(guardrails, "validate_task",
                        lambda task_id: {"verdict": "PASS", "checks": {}})
    import safety.approval_gates as gates
    monkeypatch.setattr(gates, "get_approval_level",
                        lambda task: {"needs_approval": True, "level": "ceo"})
    approved = []
    monkeypatch.setattr(gates, "request_approval",
                        lambda task_id, reason="": approved.append(task_id))

    prep = lifecycle.prepare(TASK_ID, db=db, source="api", shield_input=True)
    assert prep["status"] == "pending_approval"
    assert prep["approval_level"] == "ceo"
    assert approved == [TASK_ID]
    assert db.get_task(TASK_ID)["status"] != "in_progress"


def test_prepare_ready_checks_out_atomically(db, quiet_engines, monkeypatch):
    import safety.guardrails as guardrails
    monkeypatch.setattr(guardrails, "validate_task",
                        lambda task_id: {"verdict": "PASS", "checks": {}})
    import safety.approval_gates as gates
    monkeypatch.setattr(gates, "get_approval_level",
                        lambda task: {"needs_approval": False})

    prep = lifecycle.prepare(TASK_ID, db=db, source="api")
    assert prep["ok"] is True and prep["status"] == "ready"
    assert prep["prompt"] and TASK_ID in prep["prompt"]
    assert db.get_task(TASK_ID)["status"] == "in_progress"

    # second prepare must lose the atomic checkout
    second = lifecycle.prepare(TASK_ID, db=db, source="api")
    assert second["status"] == "already_running"


# ─── finalize semantics ────────────────────────────────────────────────────


def test_finalize_failure_computes_failure_type(db, quiet_engines):
    """The pre-N1 API copy hardcoded agent_timeout for every failure."""
    task = db.get_task(TASK_ID)

    lifecycle.finalize_failure(TASK_ID, task, "request timeout after 30s", db=db, source="api")
    lifecycle.finalize_failure(TASK_ID, task, "model refused", score=42, db=db, source="api")

    replans = [args for script, args in quiet_engines if "replanner" in script]
    assert len(replans) == 2
    assert replans[0][replans[0].index("--failure") + 1] == "agent_timeout"
    assert replans[1][replans[1].index("--failure") + 1] == "quality_below_50"


def test_finalize_success_completes_with_adapter_status_rule(db, quiet_engines, monkeypatch):
    # dario-content has no artifact schema — the real dario-brand schema would
    # (correctly) tripwire this probe output for missing required sections.
    db.update_task(TASK_ID, {"skill": "dario-content", "status": "in_progress"})
    task = db.get_task(TASK_ID)

    output = ("## Deliverable\n" + "Substantive client-ready content line.\n" * 20
              + "## Summary\nProbe deliverable for the unified lifecycle test.")
    res = lifecycle.finalize_success(
        TASK_ID, task, output, tokens=1000, score=72,
        db=db, source="api", model="sonnet",
        final_status="done", quality_score_for_filter=None,
        count_budget_on_tripwire=True, meter_tokens=False)

    assert res["status"] == "done"
    assert db.get_task(TASK_ID)["status"] == "done"
