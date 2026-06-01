"""Durable execution piloto (Onda 5 #5).

⚠️ DEPRECATED 2026-06-01 (audit P0-3 decision).
    This Temporal-based pilot is NOT used in the live execution path and never
    left stub mode (activities return status="queued" unless DARIO_TEMPORAL_LIVE=1,
    and checkpoint_interrupt.py was never implemented). DARIO's real execution
    model is single-session and Claude-Code-native (the Python executor prepares +
    checks out; the Claude Agent does the LLM work), for which a distributed
    workflow engine like Temporal is overkill.

    Real durability is provided by the lighter, fit-for-purpose mechanism:
    SQLite WAL (core/db.py) + atomic DB checkout + append-only audit log +
    stale-task recovery on heartbeat. See durable/DEPRECATED.md.

    Kept (not deleted) for reference / possible future multi-machine workflows.
    Do NOT wire into production without a deliberate decision to run Temporal Server.

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
