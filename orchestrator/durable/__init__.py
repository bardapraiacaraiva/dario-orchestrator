"""Durable execution piloto (Onda 5 #5).

Wraps a DARIO chain (`brand_to_market`) as a Temporal workflow so that:
    - Each step is journalled before/after execution.
    - A worker crash mid-step replays the workflow from history without
      re-executing the successfully-completed predecessors.
    - Long-running steps survive process restarts (server restart, deploy).

This is a CONTRACT pilot — the workflow shape is wired but not yet pointed
at the orchestrator's real per-step LLM caller. Equivalence to chain_graph
is exercised end-to-end via an in-memory Temporal worker in tests.

To run against real Temporal Server:
    docker run --rm -p 7233:7233 temporalio/auto-setup:latest
    python -m durable.run_brand_workflow

Modules:
    durable.activities   — One activity per chain step.
    durable.workflow     — `ChainWorkflow` orchestrating the activities.
    durable.run_brand_workflow — CLI entry-point.
"""
