"""Tests for Onda 5 #5 — Temporal durable execution piloto.

Uses Temporal's `WorkflowEnvironment.from_local` to run an embedded
test environment — no Docker, no external server required. The same
workflow definition + activities run unchanged against a production
Temporal cluster when wired.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


pytestmark = pytest.mark.slow  # Temporal test env takes ~5-10s to spin up


@pytest.mark.asyncio
async def test_chain_workflow_runs_three_steps():
    """End-to-end: workflow executes 3 activities, returns artifacts dict."""
    from temporalio.client import Client
    from temporalio.testing import WorkflowEnvironment
    from temporalio.worker import Worker

    from durable.activities import execute_step
    from durable.workflow import ChainWorkflow

    async with await WorkflowEnvironment.start_time_skipping() as env:
        client: Client = env.client
        task_queue = "dario-test-queue"

        async with Worker(
            client,
            task_queue=task_queue,
            workflows=[ChainWorkflow],
            activities=[execute_step],
        ):
            payload = {
                "chain_name": "smoke",
                "context": "test",
                "steps": [
                    {"skill": "step-a"},
                    {"skill": "step-b"},
                    {"skill": "step-c"},
                ],
            }
            result = await client.execute_workflow(
                ChainWorkflow.run,
                payload,
                id="wf-smoke-1",
                task_queue=task_queue,
            )

    assert result["status"] == "completed"
    assert result["completed_steps"] == 3
    assert set(result["artifacts"].keys()) == {"step-a", "step-b", "step-c"}
    # Later step saw earlier artifacts (upstream observation)
    assert "step-a" in result["artifacts"]["step-c"]["saw_upstream"]


@pytest.mark.asyncio
async def test_workflow_empty_chain_yields_zero_steps():
    from temporalio.client import Client
    from temporalio.testing import WorkflowEnvironment
    from temporalio.worker import Worker

    from durable.activities import execute_step
    from durable.workflow import ChainWorkflow

    async with await WorkflowEnvironment.start_time_skipping() as env:
        client: Client = env.client
        task_queue = "dario-test-queue-empty"

        async with Worker(
            client,
            task_queue=task_queue,
            workflows=[ChainWorkflow],
            activities=[execute_step],
        ):
            result = await client.execute_workflow(
                ChainWorkflow.run,
                {"chain_name": "empty", "steps": [], "context": ""},
                id="wf-empty-1",
                task_queue=task_queue,
            )

    assert result["completed_steps"] == 0
    assert result["artifacts"] == {}
