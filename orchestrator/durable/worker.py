"""Temporal production worker daemon (Onda 6 #4).

Connects to a Temporal Server (default: localhost:7233) and registers the
DARIO `ChainWorkflow` + activities so chains can be executed durably across
worker crashes and process restarts.

Setup
-----
1. Start Temporal Server locally:

    docker run --rm -p 7233:7233 -p 8233:8233 temporalio/auto-setup:latest

   Or via docker compose (see `scripts/temporal-self-host.yml`).

2. Start the worker:

    python -m durable.worker

3. Trigger a workflow from anywhere (REPL, script, runtime.py):

    from temporalio.client import Client
    client = await Client.connect("localhost:7233")
    handle = await client.start_workflow(
        ChainWorkflow.run,
        {"chain_name": "brand_to_market", "context": "...", "steps": [...]},
        id="run-1",
        task_queue="dario-chains",
    )

The worker journals each step before/after the activity runs, so a crash
mid-step replays from history without re-executing successful predecessors.

Honest scope
------------
This is the daemon scaffolding. The activity body itself (`execute_step`)
still returns a placeholder — wiring the real per-step LLM caller is the
final mile and belongs in the autopilot path. The journal + replay
guarantees are real today; the LLM execution is deferred.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys

from temporalio.client import Client
from temporalio.worker import Worker

from durable.activities import execute_step
from durable.workflow import ChainWorkflow

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("durable.worker")


DEFAULT_TARGET = os.getenv("TEMPORAL_TARGET", "localhost:7233")
DEFAULT_NAMESPACE = os.getenv("TEMPORAL_NAMESPACE", "default")
DEFAULT_TASK_QUEUE = os.getenv("TEMPORAL_TASK_QUEUE", "dario-chains")


async def run_worker(
    target: str = DEFAULT_TARGET,
    namespace: str = DEFAULT_NAMESPACE,
    task_queue: str = DEFAULT_TASK_QUEUE,
) -> None:
    """Connect to Temporal Server and run the worker until interrupted."""
    log.info(
        f"Connecting to Temporal at {target} (namespace={namespace}, "
        f"task_queue={task_queue})..."
    )

    client = await Client.connect(target, namespace=namespace)

    worker = Worker(
        client,
        task_queue=task_queue,
        workflows=[ChainWorkflow],
        activities=[execute_step],
    )

    log.info(f"[OK] Worker started — listening on '{task_queue}'")
    log.info("Press Ctrl+C to stop.")

    await worker.run()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="DARIO durable execution worker (Temporal)"
    )
    parser.add_argument(
        "--target",
        default=DEFAULT_TARGET,
        help=f"Temporal server address (default: {DEFAULT_TARGET})",
    )
    parser.add_argument(
        "--namespace",
        default=DEFAULT_NAMESPACE,
        help=f"Temporal namespace (default: {DEFAULT_NAMESPACE})",
    )
    parser.add_argument(
        "--task-queue",
        default=DEFAULT_TASK_QUEUE,
        help=f"Task queue name (default: {DEFAULT_TASK_QUEUE})",
    )
    args = parser.parse_args()

    try:
        asyncio.run(
            run_worker(
                target=args.target,
                namespace=args.namespace,
                task_queue=args.task_queue,
            )
        )
        return 0
    except KeyboardInterrupt:
        log.info("Worker stopped by user.")
        return 0
    except RuntimeError as e:
        log.error(f"Worker failed to start: {e}")
        log.error(
            "Hint: is Temporal Server running? Try:\n"
            "  docker run --rm -p 7233:7233 -p 8233:8233 "
            "temporalio/auto-setup:latest"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
