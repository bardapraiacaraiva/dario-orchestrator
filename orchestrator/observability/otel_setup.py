"""DARIO Orchestrator — real OpenTelemetry wiring (Onda 1 #4).

Replaces the in-memory `OTelInstrumentationRegistry` (observability_upgrades.py)
with a real OTel SDK that exports OTLP spans to Langfuse (or any OTLP-compatible
collector: Jaeger, Datadog, Honeycomb, Tempo).

Activation
----------
Zero config by default — calling `setup_tracing()` is a no-op unless one of
the following env vars is set:

    LANGFUSE_HOST=https://cloud.langfuse.com  (or your self-hosted URL)
    LANGFUSE_PUBLIC_KEY=pk-lf-...
    LANGFUSE_SECRET_KEY=sk-lf-...

Or — for vendor-agnostic export — set:

    OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
    OTEL_EXPORTER_OTLP_HEADERS=authorization=Bearer ...

If none are set, `setup_tracing()` installs an in-process console exporter
(useful for development) and emits a single info log so it's obvious tracing
is "on" but not shipping anywhere.

What we instrument
------------------
- **FastAPI** — auto-instrumentation of every HTTP route (request/response,
  status codes, latency, exceptions).
- **Agent invocations** — manual spans via `trace_agent_invoke()` context manager.
- **Tool calls** — manual spans via `trace_tool_call()` context manager.
- **Guard decisions** — manual spans via `trace_guard()` context manager.
- **Dispatch decisions** — manual spans via `trace_dispatch()` context manager.

Span attributes follow OpenInference semantic conventions where possible:
    - `dario.task_id`, `dario.skill`, `dario.agent`
    - `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, ...
"""

from __future__ import annotations

import base64
import logging
import os
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
    SpanExporter,
    SpanExportResult,
)

log = logging.getLogger("dario.otel")

_ORCH_DIR = Path.home() / ".claude" / "orchestrator"
_TRACES_DIR = _ORCH_DIR / "traces"

_PROVIDER_INSTALLED = False
_TRACER: trace.Tracer | None = None


class FileSpanExporter(SpanExporter):
    """Append finished spans as JSONL to traces/otel-YYYY-MM-DD.jsonl.

    The default exporter when no OTLP/Langfuse endpoint is configured (Fase 4,
    2026-06-12). It replaces ConsoleSpanExporter, whose output evaporated to
    stdout — every span (agent/tool/guard/dispatch) is now captured to an
    inspectable local file, turning the existing instrumentation into a real
    zero-infrastructure trace store. Point OTEL_EXPORTER_OTLP_ENDPOINT at a
    collector to ship to Grafana/Jaeger/Tempo instead, or set DARIO_OTEL_CONSOLE
    to fall back to stdout.
    """

    def __init__(self, directory: Path | None = None) -> None:
        self._dir = directory or _TRACES_DIR
        try:
            self._dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    def _path(self) -> Path:
        return self._dir / f"otel-{datetime.now(UTC).strftime('%Y-%m-%d')}.jsonl"

    def export(self, spans) -> SpanExportResult:
        try:
            with self._path().open("a", encoding="utf-8") as fh:
                for span in spans:
                    fh.write(span.to_json(indent=None) + "\n")
            return SpanExportResult.SUCCESS
        except Exception:
            return SpanExportResult.FAILURE

    def shutdown(self) -> None:
        return None

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


# ─── Setup ───────────────────────────────────────────────────────────────────


def _resolve_exporter() -> tuple[str, Any]:
    """Pick an exporter based on env vars. Returns (mode, exporter)."""
    # 1) Langfuse — preferred, ergonomics for our stack
    lf_host = os.getenv("LANGFUSE_HOST")
    lf_pk = os.getenv("LANGFUSE_PUBLIC_KEY")
    lf_sk = os.getenv("LANGFUSE_SECRET_KEY")
    if lf_host and lf_pk and lf_sk:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )

        token = base64.b64encode(f"{lf_pk}:{lf_sk}".encode()).decode()
        endpoint = f"{lf_host.rstrip('/')}/api/public/otel/v1/traces"
        return "langfuse", OTLPSpanExporter(
            endpoint=endpoint,
            headers={"Authorization": f"Basic {token}"},
        )

    # 2) Generic OTLP (Jaeger, Tempo, etc.)
    if os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"):
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )

        # OTel SDK reads OTEL_* env vars natively
        return "otlp", OTLPSpanExporter()

    # 3) Console (only if explicitly requested)
    if os.getenv("DARIO_OTEL_CONSOLE"):
        return "console", ConsoleSpanExporter()

    # 4) File-based local trace store (default — replaces evaporating console)
    return "file", FileSpanExporter()


def setup_tracing(service_name: str = "dario-orchestrator") -> trace.Tracer:
    """Install the OTel tracer provider. Idempotent — safe to call multiple times."""
    global _PROVIDER_INSTALLED, _TRACER

    if _PROVIDER_INSTALLED and _TRACER is not None:
        return _TRACER

    resource = Resource.create(
        {
            "service.name": service_name,
            "service.version": "12.1.0",
            "deployment.environment": os.getenv("DARIO_ENV", "production"),
        }
    )
    provider = TracerProvider(resource=resource)

    mode, exporter = _resolve_exporter()
    processor: BatchSpanProcessor | SimpleSpanProcessor
    if mode in ("console", "file"):
        processor = SimpleSpanProcessor(exporter)  # immediate flush for local stores
    else:
        processor = BatchSpanProcessor(exporter, max_export_batch_size=64)
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)
    _PROVIDER_INSTALLED = True
    _TRACER = trace.get_tracer("dario.orchestrator", "12.1.0")

    log.info(f"[OTel] tracing active — exporter={mode}")
    return _TRACER


def instrument_fastapi(app) -> None:
    """Attach FastAPI auto-instrumentation. Call AFTER setup_tracing()."""
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        FastAPIInstrumentor.instrument_app(app)
        log.info("[OTel] FastAPI instrumented")
    except Exception as e:
        log.warning(f"[OTel] FastAPI instrumentation failed: {e}")


def get_tracer() -> trace.Tracer:
    """Get a tracer from the current global provider.

    We deliberately do NOT cache — fetching from the global provider on every
    call keeps test fixtures honest (they can swap the provider and the next
    span lands in the new exporter without restarting the process).
    """
    if not _PROVIDER_INSTALLED:
        setup_tracing()
    return trace.get_tracer("dario.orchestrator", "12.1.0")


# ─── Manual span helpers ─────────────────────────────────────────────────────


@contextmanager
def trace_agent_invoke(
    task_id: str,
    skill: str,
    agent: str = "dario-ceo",
    model: str | None = None,
    **extra: Any,
) -> Iterator[trace.Span]:
    """Span around a single agent invocation.

    Usage:
        with trace_agent_invoke(task_id="ATR-001", skill="dario-brand", model="opus") as span:
            output = run_skill(...)
            span.set_attribute("gen_ai.usage.output_tokens", output.tokens)
    """
    tracer = get_tracer()
    with tracer.start_as_current_span(f"agent.invoke:{skill}") as span:
        span.set_attribute("dario.task_id", task_id)
        span.set_attribute("dario.skill", skill)
        span.set_attribute("dario.agent", agent)
        if model:
            span.set_attribute("gen_ai.system", "anthropic")
            span.set_attribute("gen_ai.request.model", model)
        for k, v in extra.items():
            span.set_attribute(f"dario.{k}", v)
        try:
            yield span
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            raise


@contextmanager
def trace_tool_call(
    tool_name: str,
    call_id: str | None = None,
    **arguments: Any,
) -> Iterator[trace.Span]:
    """Span around a tool invocation by an agent."""
    tracer = get_tracer()
    with tracer.start_as_current_span(f"tool.call:{tool_name}") as span:
        span.set_attribute("dario.tool", tool_name)
        if call_id:
            span.set_attribute("dario.tool_call_id", call_id)
        for k, v in arguments.items():
            # Coerce to string to avoid OTel attribute-type errors
            span.set_attribute(f"dario.tool.arg.{k}", str(v)[:1000])
        try:
            yield span
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            raise


@contextmanager
def trace_guard(
    guard_name: str,
    task_id: str | None = None,
    **extra: Any,
) -> Iterator[trace.Span]:
    """Span around a guardrail / policy check."""
    tracer = get_tracer()
    with tracer.start_as_current_span(f"guard:{guard_name}") as span:
        span.set_attribute("dario.guard", guard_name)
        if task_id:
            span.set_attribute("dario.task_id", task_id)
        for k, v in extra.items():
            span.set_attribute(f"dario.{k}", str(v)[:500])
        try:
            yield span
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            raise


@contextmanager
def trace_dispatch(
    task_id: str,
    skill_decided: str | None = None,
    confidence: float | None = None,
) -> Iterator[trace.Span]:
    """Span around a dispatch decision (semantic_dispatch route to skill)."""
    tracer = get_tracer()
    with tracer.start_as_current_span("dispatch") as span:
        span.set_attribute("dario.task_id", task_id)
        if skill_decided:
            span.set_attribute("dario.dispatch.skill", skill_decided)
        if confidence is not None:
            span.set_attribute("dario.dispatch.confidence", confidence)
        try:
            yield span
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            raise


__all__ = [
    "setup_tracing",
    "instrument_fastapi",
    "get_tracer",
    "trace_agent_invoke",
    "trace_tool_call",
    "trace_guard",
    "trace_dispatch",
]
