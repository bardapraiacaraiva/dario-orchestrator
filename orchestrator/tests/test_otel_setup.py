"""Tests for Onda 1 #4 — otel_setup.py (real OpenTelemetry wiring)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from observability import otel_setup


@pytest.fixture
def in_memory_exporter(monkeypatch):
    """Inspect spans via an in-memory exporter.

    OTel only allows ONE global TracerProvider per process. After the first
    one is installed we cannot replace it cleanly — so we attach an extra
    SpanProcessor with our in-memory exporter to whatever provider is
    currently active. This is the recommended OTel testing pattern.
    """
    # Ensure a provider exists (idempotent — installs on first call)
    otel_setup.setup_tracing()
    provider = trace.get_tracer_provider()

    exporter = InMemorySpanExporter()
    # Hot-add an in-memory processor to the existing provider
    if hasattr(provider, "add_span_processor"):
        processor = SimpleSpanProcessor(exporter)
        provider.add_span_processor(processor)
        try:
            yield exporter
        finally:
            exporter.clear()
            # Best-effort detach — OTel SDK exposes _active_span_processor
            try:
                processor.shutdown()
            except Exception:
                pass
    else:
        pytest.skip("Active TracerProvider does not allow adding processors")


# ─── Setup behaviour ─────────────────────────────────────────────────────────


class TestSetup:
    def test_setup_returns_tracer(self):
        tracer = otel_setup.setup_tracing()
        assert tracer is not None
        # Has the OTel-tracer interface
        assert hasattr(tracer, "start_as_current_span")

    def test_setup_is_idempotent(self):
        t1 = otel_setup.setup_tracing()
        t2 = otel_setup.setup_tracing()
        assert t1 is t2  # same instance — provider only installed once

    def test_exporter_picks_langfuse_when_env_set(self, monkeypatch):
        monkeypatch.setenv("LANGFUSE_HOST", "https://example.com")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        mode, _ = otel_setup._resolve_exporter()
        assert mode == "langfuse"

    def test_exporter_picks_console_in_dev(self, monkeypatch):
        monkeypatch.delenv("LANGFUSE_HOST", raising=False)
        monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
        monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
        monkeypatch.delenv("OTEL_EXPORTER_OTLP_ENDPOINT", raising=False)
        mode, _ = otel_setup._resolve_exporter()
        assert mode == "console"

    def test_exporter_picks_otlp_when_endpoint_set(self, monkeypatch):
        monkeypatch.delenv("LANGFUSE_HOST", raising=False)
        monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")
        mode, _ = otel_setup._resolve_exporter()
        assert mode == "otlp"


# ─── Span emission ───────────────────────────────────────────────────────────


class TestSpanEmission:
    def test_agent_invoke_emits_span(self, in_memory_exporter):
        with otel_setup.trace_agent_invoke(
            task_id="T-001", skill="dario-brand", model="opus", project="acme"
        ):
            pass
        spans = in_memory_exporter.get_finished_spans()
        assert len(spans) == 1
        s = spans[0]
        assert s.name == "agent.invoke:dario-brand"
        assert s.attributes["dario.task_id"] == "T-001"
        assert s.attributes["dario.skill"] == "dario-brand"
        assert s.attributes["gen_ai.system"] == "anthropic"
        assert s.attributes["gen_ai.request.model"] == "opus"
        assert s.attributes["dario.project"] == "acme"

    def test_tool_call_emits_span(self, in_memory_exporter):
        with otel_setup.trace_tool_call("grep", pattern="error", path="/var/log"):
            pass
        spans = in_memory_exporter.get_finished_spans()
        assert len(spans) == 1
        s = spans[0]
        assert s.name == "tool.call:grep"
        assert s.attributes["dario.tool"] == "grep"
        assert s.attributes["dario.tool.arg.pattern"] == "error"

    def test_guard_emits_span_with_attributes(self, in_memory_exporter):
        with otel_setup.trace_guard(
            "ethical_gate", task_id="T-001", verdict="pass", reason="ok"
        ):
            pass
        spans = in_memory_exporter.get_finished_spans()
        assert len(spans) == 1
        s = spans[0]
        assert s.name == "guard:ethical_gate"
        assert s.attributes["dario.guard"] == "ethical_gate"
        assert s.attributes["dario.verdict"] == "pass"

    def test_dispatch_emits_span(self, in_memory_exporter):
        with otel_setup.trace_dispatch(
            task_id="T-001", skill_decided="aegis-breach-simulation", confidence=0.84
        ):
            pass
        spans = in_memory_exporter.get_finished_spans()
        assert len(spans) == 1
        s = spans[0]
        assert s.name == "dispatch"
        assert s.attributes["dario.dispatch.skill"] == "aegis-breach-simulation"
        assert s.attributes["dario.dispatch.confidence"] == 0.84

    def test_nested_spans_have_parent(self, in_memory_exporter):
        with otel_setup.trace_agent_invoke(task_id="T-2", skill="dario-brand"):
            with otel_setup.trace_tool_call("grep", pattern="x"):
                pass
        spans = in_memory_exporter.get_finished_spans()
        # OTel exports children before parents
        child = next(s for s in spans if s.name.startswith("tool.call"))
        parent = next(s for s in spans if s.name.startswith("agent.invoke"))
        assert child.parent is not None
        assert child.parent.span_id == parent.context.span_id

    def test_exception_recorded_on_span(self, in_memory_exporter):
        with pytest.raises(RuntimeError):
            with otel_setup.trace_agent_invoke(task_id="T-3", skill="dario-brand"):
                raise RuntimeError("boom")
        spans = in_memory_exporter.get_finished_spans()
        assert len(spans) == 1
        s = spans[0]
        assert s.status.status_code.name == "ERROR"
        # The exception should be present as a span event
        assert any(
            "exception" in (e.name or "").lower() for e in s.events
        ), f"no exception event: {[e.name for e in s.events]}"
