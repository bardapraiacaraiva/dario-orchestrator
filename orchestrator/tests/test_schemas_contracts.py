"""Tests for Onda 1 #2 — central Pydantic contracts in schemas/contracts.py."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from schemas import (
    AgentInput,
    AgentOutput,
    AssignResponse,
    BudgetResponse,
    CheckoutResponse,
    CompleteResponse,
    ExecutionPolicy,
    ExecutorType,
    HealthResponse,
    Priority,
    PulseResponse,
    TaskComplete,
    TaskCreate,
    TaskListResponse,
    TaskSpec,
    TaskStatus,
    ToolCall,
    ToolResult,
    ValidationReport,
)

# ─── TaskCreate ──────────────────────────────────────────────────────────────


class TestTaskCreate:
    def test_minimal_valid(self):
        t = TaskCreate(id="ATR-001", title="Brand audit")
        assert t.id == "ATR-001"
        assert t.priority == Priority.MEDIUM
        assert t.execution_policy == ExecutionPolicy.DEFAULT

    def test_rejects_empty_id(self):
        with pytest.raises(ValidationError):
            TaskCreate(id="", title="x")

    def test_rejects_lowercase_prefix(self):
        with pytest.raises(ValidationError):
            TaskCreate(id="atr-001", title="x")

    def test_rejects_id_without_dash(self):
        with pytest.raises(ValidationError):
            TaskCreate(id="ATR001", title="x")

    def test_rejects_extra_field(self):
        with pytest.raises(ValidationError):
            TaskCreate(id="ATR-001", title="x", unknown_field=42)

    def test_priority_enum_coercion(self):
        t = TaskCreate(id="ATR-001", title="x", priority="high")
        assert t.priority == Priority.HIGH

    def test_estimated_tokens_non_negative(self):
        with pytest.raises(ValidationError):
            TaskCreate(id="ATR-001", title="x", estimated_tokens=-1)


# ─── TaskComplete ────────────────────────────────────────────────────────────


class TestTaskComplete:
    def test_minimal_valid(self):
        c = TaskComplete()
        assert c.score == 0
        assert c.status == TaskStatus.DONE

    def test_score_bounded(self):
        with pytest.raises(ValidationError):
            TaskComplete(score=101)
        with pytest.raises(ValidationError):
            TaskComplete(score=-1)

    def test_status_enum(self):
        c = TaskComplete(status="blocked")
        assert c.status == TaskStatus.BLOCKED


# ─── TaskSpec ────────────────────────────────────────────────────────────────


class TestTaskSpec:
    def test_minimal_valid(self):
        s = TaskSpec(id="ATR-001", title="Audit", skill="dario-brand")
        assert s.executor_type == ExecutorType.AGENT
        assert s.status == TaskStatus.TODO

    def test_allows_domain_extra_fields(self):
        """TaskSpec deliberately allows extra fields (inputs, methodology, ...)."""
        s = TaskSpec(
            id="ATR-001",
            title="x",
            skill="dario-brand",
            inputs=[{"campo": "url"}],
            methodology="Kapferer",
        )
        assert s.id == "ATR-001"

    def test_rejects_missing_skill(self):
        with pytest.raises(ValidationError):
            TaskSpec(id="ATR-001", title="x")


# ─── AgentInput / AgentOutput ────────────────────────────────────────────────


class TestAgentContracts:
    def test_agent_input_round_trip(self):
        a = AgentInput(task_id="ATR-001", skill="dario-brand", prompt="Hello")
        assert a.dry_run is False
        d = a.model_dump()
        a2 = AgentInput.model_validate(d)
        assert a2 == a

    def test_temperature_bounds(self):
        with pytest.raises(ValidationError):
            AgentInput(task_id="x", skill="y", prompt="p", temperature=3.0)
        with pytest.raises(ValidationError):
            AgentInput(task_id="x", skill="y", prompt="p", temperature=-0.1)

    def test_agent_output_round_trip(self):
        o = AgentOutput(
            task_id="ATR-001",
            skill="dario-brand",
            success=True,
            tokens_used=500,
            duration_seconds=2.4,
        )
        j = o.model_dump_json()
        o2 = AgentOutput.model_validate_json(j)
        assert o2 == o


# ─── ToolCall / ToolResult ───────────────────────────────────────────────────


class TestToolContracts:
    def test_tool_call_minimal(self):
        tc = ToolCall(tool_name="grep", arguments={"pattern": "foo"})
        assert tc.tool_name == "grep"
        assert tc.invoked_at  # default factory

    def test_tool_call_rejects_empty_name(self):
        with pytest.raises(ValidationError):
            ToolCall(tool_name="", arguments={})

    def test_tool_result_round_trip(self):
        r = ToolResult(
            tool_name="grep",
            success=True,
            output=["line1", "line2"],
            duration_ms=42,
        )
        assert r.success
        assert r.duration_ms == 42


# ─── ValidationReport ────────────────────────────────────────────────────────


class TestValidationReport:
    def test_minimal(self):
        r = ValidationReport(valid=True)
        assert r.errors == []
        assert r.spec_version == "TASK-FORMAT-SPEC-V1"


# ─── Response envelopes (Onda 3 #4) ──────────────────────────────────────────


class TestResponseEnvelopes:
    def test_health_response_minimal(self):
        h = HealthResponse(status="ok", timestamp="2026-05-22T15:00:00Z")
        assert h.state == "?"   # default
        assert h.health == 0

    def test_health_response_extra_allowed(self):
        """HealthResponse uses extra='allow' for runtime-added fields."""
        h = HealthResponse(
            status="ok",
            timestamp="2026-05-22T15:00:00Z",
            scheduler={"running": True, "pulses": 12},
            db={"task_count": 100},
        )
        # extras survive
        assert h.model_dump()["scheduler"] == {"running": True, "pulses": 12}

    def test_task_list_response(self):
        r = TaskListResponse(count=3, tasks=[{"id": "T-1"}])
        assert r.count == 3
        assert len(r.tasks) == 1

    def test_task_list_response_rejects_negative_count(self):
        with pytest.raises(ValidationError):
            TaskListResponse(count=-1, tasks=[])

    def test_assign_response_round_trip(self):
        r = AssignResponse(assigned=True, task_id="ATR-001", worker="worker-brand")
        d = r.model_dump()
        r2 = AssignResponse.model_validate(d)
        assert r2 == r

    def test_checkout_response(self):
        r = CheckoutResponse(checked_out=True, task_id="ATR-001")
        assert r.checked_out

    def test_complete_response_score_bounded(self):
        with pytest.raises(ValidationError):
            CompleteResponse(completed=True, task_id="T-1", score=101)
        with pytest.raises(ValidationError):
            CompleteResponse(completed=True, task_id="T-1", score=-1)

    def test_budget_response_extra_allowed(self):
        b = BudgetResponse(
            total_tokens_used=1000,
            limit=50000,
            percentage=2.0,
            by_project={"acme": 1000},
        )
        # extras survive
        assert b.model_dump()["by_project"] == {"acme": 1000}

    def test_pulse_response(self):
        p = PulseResponse(pulse=42, status="executed")
        assert p.pulse == 42

    def test_pulse_response_rejects_negative(self):
        with pytest.raises(ValidationError):
            PulseResponse(pulse=-1, status="executed")


# ─── task_spec.validate_task integration ─────────────────────────────────────


class TestTaskSpecIntegration:
    """validate_task() must keep its legacy dict-in / dict-out shape."""

    def test_valid_task_passes(self):
        from core.task_spec import validate_task

        result = validate_task({
            "id": "ATR-001",
            "title": "x",
            "skill": "dario-brand",
        })
        assert result["valid"] is True
        assert result["spec_version"] == "TASK-FORMAT-SPEC-V1"

    def test_missing_fields_reported(self):
        from core.task_spec import validate_task

        result = validate_task({"id": "ATR-001"})
        assert result["valid"] is False
        assert any("title" in e for e in result["errors"])

    def test_invalid_executor_type_reported(self):
        from core.task_spec import validate_task

        result = validate_task({
            "id": "ATR-001",
            "title": "x",
            "skill": "dario-brand",
            "executor_type": "nonsense",
        })
        assert result["valid"] is False
        assert any("executor_type" in e for e in result["errors"])
