"""Temporal activities (Onda 5 #5 piloto, Onda 7 #5 LLM wired).

Each activity wraps a single DARIO chain step. Temporal calls the activity,
journals the input + output, and replays from history if the worker crashes
between calls. Side-effects only happen INSIDE activities — never in the
workflow itself (Temporal rule).

Onda 7 #5: `execute_step` now supports two modes:

    1. **Stub mode** (default; used in tests and when no API key present):
       returns a deterministic placeholder. Zero cost, deterministic.

    2. **Live mode** (when `DARIO_TEMPORAL_LIVE=1` env var is set):
       invokes Anthropic via `providers.anthropic` with the skill's
       prompt template. Real LLM call; costs real tokens.

The activity input adds an optional `prompt` field — when present and
live mode is on, that prompt drives the LLM call.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import UTC, datetime

from temporalio import activity


@dataclass
class StepInput:
    """Activity input contract."""

    chain_name: str
    skill: str
    step_index: int
    upstream_artifacts: dict
    # Onda 7 #5: optional prompt + model hints for live mode
    prompt: str | None = None
    model: str = "claude-haiku-4-5"
    max_tokens: int = 800
    extras: dict = field(default_factory=dict)


@dataclass
class StepOutput:
    """Activity output contract."""

    skill: str
    artifact: dict
    score: int
    completed_at: str
    mode: str = "stub"  # "stub" | "live"


def _live_mode_enabled() -> bool:
    """Live mode requires explicit opt-in via env var to avoid surprise spend."""
    return os.getenv("DARIO_TEMPORAL_LIVE", "").lower() in ("1", "true", "yes")


async def _invoke_anthropic(req: StepInput) -> dict:
    """Call Anthropic via the SDK directly (deferred import keeps stub fast)."""
    import anthropic

    client = anthropic.AsyncAnthropic()
    prompt = req.prompt or (
        f"You are executing skill `{req.skill}` as step "
        f"{req.step_index} of chain `{req.chain_name}`. "
        f"Upstream artifacts so far: {list(req.upstream_artifacts.keys())}. "
        "Produce a structured output suitable for downstream steps."
    )
    response = await client.messages.create(
        model=req.model,
        max_tokens=req.max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(
        block.text for block in response.content if block.type == "text"
    )
    return {
        "text": text,
        "tokens_in": response.usage.input_tokens,
        "tokens_out": response.usage.output_tokens,
        "model": req.model,
    }


@activity.defn
async def execute_step(req: StepInput) -> StepOutput:
    """Execute one chain step.

    Stub mode by default. Set DARIO_TEMPORAL_LIVE=1 to invoke Anthropic.
    Whether stub or live, the activity completion is journalled by Temporal
    so a worker crash mid-step replays cleanly from history.
    """
    completed = datetime.now(UTC).isoformat()

    if _live_mode_enabled():
        try:
            llm_result = await _invoke_anthropic(req)
            return StepOutput(
                skill=req.skill,
                artifact={
                    "status": "completed",
                    "step_index": req.step_index,
                    "saw_upstream": list(req.upstream_artifacts.keys()),
                    "output": llm_result["text"],
                    "tokens_in": llm_result["tokens_in"],
                    "tokens_out": llm_result["tokens_out"],
                    "model": llm_result["model"],
                    "completed_at": completed,
                },
                score=80,  # baseline; rubric scoring happens elsewhere
                completed_at=completed,
                mode="live",
            )
        except Exception as e:
            # Fall through to stub with an error annotation — Temporal will
            # still journal the failure and the workflow decides retry policy.
            return StepOutput(
                skill=req.skill,
                artifact={
                    "status": "failed",
                    "step_index": req.step_index,
                    "saw_upstream": list(req.upstream_artifacts.keys()),
                    "error": str(e)[:300],
                    "completed_at": completed,
                },
                score=0,
                completed_at=completed,
                mode="live",
            )

    # Stub mode (default)
    return StepOutput(
        skill=req.skill,
        artifact={
            "status": "queued",
            "step_index": req.step_index,
            "saw_upstream": list(req.upstream_artifacts.keys()),
            "queued_at": completed,
        },
        score=0,
        completed_at=completed,
        mode="stub",
    )


__all__ = ["StepInput", "StepOutput", "execute_step"]
