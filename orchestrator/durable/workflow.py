"""Temporal workflow (Onda 5 #5 piloto).

Wraps a DARIO chain as a Temporal workflow. The workflow definition uses
ONLY deterministic operations (no I/O, no datetime.now()), with side-effects
delegated to activities. Crashes mid-step replay from history without
re-running completed predecessors — this is the durable-execution guarantee
LangGraph's SqliteSaver approximates locally but Temporal provides natively
across worker fleets.
"""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from durable.activities import StepInput, StepOutput, execute_step


@workflow.defn
class ChainWorkflow:
    """Run a DARIO chain durably.

    Input:  {"chain_name": str, "steps": [{"skill": str, ...}, ...], "context": str}
    Output: {"artifacts": dict, "scores": list, "completed_steps": int}

    The chain definition is passed in to keep the workflow signature
    deterministic — the workflow itself does not read disk.
    """

    @workflow.run
    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        chain_name = payload["chain_name"]
        steps = payload.get("steps", [])
        context = payload.get("context", "")

        artifacts: dict[str, dict[str, Any]] = {}
        scores: list[dict[str, Any]] = []

        for idx, step_def in enumerate(steps):
            skill = step_def.get("skill", f"step_{idx}")
            result: StepOutput = await workflow.execute_activity(
                execute_step,
                StepInput(
                    chain_name=chain_name,
                    skill=skill,
                    step_index=idx,
                    upstream_artifacts=dict(artifacts),
                ),
                start_to_close_timeout=timedelta(minutes=5),
            )
            artifacts[skill] = result.artifact
            scores.append({"skill": skill, "score": result.score})

        return {
            "chain_name": chain_name,
            "context": context,
            "artifacts": artifacts,
            "scores": scores,
            "completed_steps": len(scores),
            "status": "completed",
        }


__all__ = ["ChainWorkflow"]
