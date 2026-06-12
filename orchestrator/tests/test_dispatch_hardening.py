"""Hardening session behavior tests (DD findings A7/A9/A12, 2026-06-12).

Covers the three dispatch/execution-path fixes:
  - A12: ethical gate string-bypass killed — "approved" in free text no
    longer counts as confirmation for destructive tasks.
  - A9: release_by_caller frees slots across process boundaries (executor
    claims at checkout, record_execution_result releases by caller string).
  - A7: build_execution_pipeline is the single pipeline source for BOTH
    engines — composition asserted here so drift fails loudly.
"""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import pytest


# ─── A12: ethical gate — no free-text confirmation bypass ─────────────────


def _destructive_task(**extra):
    task = {
        "id": "HARD-001",
        "title": "delete all old client data",
        "description": "Remove every record older than 2 years from the database",
        "project": "atrium",
        "skill": "dario-legal",
    }
    task.update(extra)
    return task


def test_freedom_blocks_destructive_without_structured_confirmation():
    from safety.ethical_gate import evaluate_freedom
    passed, _, reasons = evaluate_freedom(_destructive_task())
    assert not passed
    assert any("without confirmation" in r for r in reasons)


def test_freedom_string_approved_does_not_bypass():
    """The word "approved" in the description must NOT count as confirmation."""
    from safety.ethical_gate import evaluate_freedom
    task = _destructive_task(
        description="Remove every record older than 2 years. Client said approved and confirmed.",
    )
    passed, _, reasons = evaluate_freedom(task)
    assert not passed, "free-text 'approved' bypassed the destructive-action check"
    assert any("without confirmation" in r for r in reasons)


@pytest.mark.parametrize("field", ["confirmation_received", "user_approved"])
def test_freedom_structured_confirmation_passes(field):
    from safety.ethical_gate import evaluate_freedom
    passed, _, _ = evaluate_freedom(_destructive_task(**{field: True}))
    assert passed


# ─── A9: parallelism guard — release_by_caller ─────────────────────────────


@pytest.fixture
def isolated_slots(tmp_path, monkeypatch):
    import enforcement.parallelism_guard as pg
    fake_runtime = tmp_path / "runtime"
    fake_runtime.mkdir()
    monkeypatch.setattr(pg, "RUNTIME_DIR", fake_runtime)
    monkeypatch.setattr(pg, "SLOTS_FILE", fake_runtime / "active_dispatches.json")
    monkeypatch.setattr(pg, "LOCK_FILE", fake_runtime / "active_dispatches.lock")
    monkeypatch.setenv("DARIO_MAX_PARALLEL", "3")
    return pg


def test_release_by_caller_frees_only_matching_slots(isolated_slots):
    pg = isolated_slots
    pg.claim_slot(caller="executor:TASK-A")
    pg.claim_slot(caller="executor:TASK-B")
    assert pg.active_count() == 2

    released = pg.release_by_caller("executor:TASK-A")
    assert released == 1
    assert pg.active_count() == 1
    assert pg.active_slots()[0]["caller"] == "executor:TASK-B"


def test_release_by_caller_unknown_or_empty_is_noop(isolated_slots):
    pg = isolated_slots
    pg.claim_slot(caller="executor:TASK-A")
    assert pg.release_by_caller("executor:GHOST") == 0
    assert pg.release_by_caller("") == 0
    assert pg.active_count() == 1


def test_claim_then_release_by_caller_frees_capacity(isolated_slots):
    """The executor pattern: claim at checkout, release by caller at record."""
    pg = isolated_slots
    for tid in ("T1", "T2", "T3"):
        pg.claim_slot(caller=f"executor:{tid}")
    with pytest.raises(pg.ParallelismExceededError):
        pg.claim_slot(caller="executor:T4")
    pg.release_by_caller("executor:T2")
    pg.claim_slot(caller="executor:T4")  # must not raise now
    assert pg.active_count() == 3


# ─── A7: single pipeline factory for both engines ─────────────────────────


EXPECTED_FILTERS = [
    "LoggingFilter",
    "ModelRouterFilter",
    "BudgetFilter",
    "SchemaValidationFilter",
    "OutputGuardrailFilter",
    "QualityGateFilter",
    "TokenBudgetFilter",
]


def test_build_execution_pipeline_composition():
    from execution.pipeline import build_execution_pipeline
    pipe = build_execution_pipeline()
    names = [type(f).__name__ for f in pipe.filters]
    assert names == EXPECTED_FILTERS


def test_both_engines_share_the_factory():
    """executor.PIPELINE and anthropic.API_PIPELINE must have identical
    composition AND identical filter parameters — they drift apart otherwise
    (the C1 quality-gate bug only existed on one engine)."""
    from execution.executor import PIPELINE
    from providers.anthropic import API_PIPELINE

    exec_names = [type(f).__name__ for f in PIPELINE.filters]
    api_names = [type(f).__name__ for f in API_PIPELINE.filters]
    assert exec_names == api_names == EXPECTED_FILTERS

    for ef, af in zip(PIPELINE.filters, API_PIPELINE.filters):
        for attr in ("warn_pct", "block_pct", "min_score"):
            assert getattr(ef, attr, None) == getattr(af, attr, None), (
                f"{type(ef).__name__}.{attr} differs between engines"
            )
