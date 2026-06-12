#!/usr/bin/env python3
"""
DARIO Executor — Durable Task Execution Engine.
=================================================
The "last mile" that transforms infrastructure into a real execution engine.
Coordinates ALL subsystems for each task: guardrails → context → trace → execute → score → advance.

This is what makes DARIO a "durable execution engine" vs a "todo list with dispatcher":
- State is TRANSACTIONAL (DB-first, single source of truth)
- Routing is CONDITIONAL (guardrails gate execution, replanner handles failure)
- Communication is STRUCTURED (artifacts validated, context assembled, traces logged)
- Execution is DURABLE (checkpoints per step, resume on crash)

Usage:
    # Execute a single task (full lifecycle: guard → context → trace → run → score)
    python executor.py --task MNB-002

    # Execute next wave (all ready tasks in parallel)
    python executor.py --wave

    # Execute a chain step-by-step (durable, checkpointed)
    python executor.py --chain brand_to_market --project mar-brasa --context "..."

    # Dry-run (show what WOULD execute without running)
    python executor.py --wave --dry-run

    # Full pulse (state check → dispatch → wave execute → score → log)
    python executor.py --pulse

    # JSON output
    python executor.py --pulse --json

Architecture:
    executor.py orchestrates:
    ┌─────────────────────────────────────────────────────────────┐
    │  1. guardrails.py  — PRE-EXECUTION: can this run?           │
    │  2. context_injector.py — CONTEXT: what does it need?       │
    │  3. adaptive_rubric.py — RUBRIC: how will we score it?      │
    │  4. tracer.py — TRACE START: record inputs                  │
    │  5. [EXECUTE] — Claude runs the skill (via skill invocation)│
    │  6. quality_scorer.py — SCORE: how good was it?             │
    │  7. tracer.py — TRACE END: record outputs                   │
    │  8. replanner.py — IF FAILED: auto-recover                  │
    │  9. db.py — STATE ADVANCE: update DB atomically             │
    │ 10. audit_logger.py — LOG: append to trail                  │
    └─────────────────────────────────────────────────────────────┘

Exit codes:
    0 = execution successful
    1 = error
    2 = task blocked by guardrails (not executed)
    3 = task failed, replanner activated
"""

import argparse
import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import functools

# ─── OpenTelemetry tracing (P0-4: wire real spans into the execution path) ───
# Guarded + opt-in: observability deps are an optional extra. Tracing only
# activates when an export target is configured (Langfuse / OTLP) or DARIO_OTEL=1,
# so a default install gets a silent no-op (no console span spam) while a
# configured deployment gets real distributed traces. Never affects execution.
import os as _os_otel

from core.db import DB
from execution import lifecycle
from execution.lifecycle import build_execution_prompt, run_engine  # noqa: F401 — re-exported; single source is lifecycle.py

_OTEL_TARGET = (
    _os_otel.environ.get("DARIO_OTEL") == "1"
    or _os_otel.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    or _os_otel.environ.get("LANGFUSE_PUBLIC_KEY")
)
if _OTEL_TARGET:
    try:
        from opentelemetry import trace as _otel_trace

        from observability.otel_setup import setup_tracing, trace_agent_invoke
        setup_tracing("dario-orchestrator")
        _OTEL_OK = True
    except Exception:
        _OTEL_OK = False
else:
    _OTEL_OK = False


def _span_set(**attrs) -> None:
    """Set attributes on the current OTel span, if tracing is active. No-op otherwise."""
    if not _OTEL_OK:
        return
    try:
        span = _otel_trace.get_current_span()
        for key, value in attrs.items():
            if value is not None and value != "":
                span.set_attribute(f"dario.{key}", value)
    except Exception:
        pass


def _traced_task(fn):
    """Wrap a single-task execution in an OTel span (P0-4). Captures timing + exceptions."""
    @functools.wraps(fn)
    def wrapper(task_id, *args, **kwargs):
        if not _OTEL_OK:
            return fn(task_id, *args, **kwargs)
        with trace_agent_invoke(task_id=task_id, skill="(pending)", agent="executor"):
            return fn(task_id, *args, **kwargs)
    return wrapper


PYTHON = sys.executable

# The ONE pipeline + lifecycle (Next-Gen N1, 2026-06-12): this module is now a
# thin adapter over execution/lifecycle.py — the full prepare/finalize cycle
# lives there, shared verbatim with the autonomous API engine.
PIPELINE = lifecycle.PIPELINE
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("executor")


# =============================================================================
# CORE: Execute a single task through the full lifecycle
# =============================================================================

@_traced_task
def execute_task(task_id: str, dry_run: bool = False) -> dict:
    """
    Full lifecycle execution of a single task (session path).

    Thin adapter over execution/lifecycle.prepare (Next-Gen N1) — the shared
    cycle is pre-conditions -> filter -> guardrails -> context -> rubric ->
    trace -> prompt -> approval gate -> slot -> atomic checkout. This adapter
    only maps the result to the legacy shape the autopilot/CLI consume.
    """
    db = DB()
    prep = lifecycle.prepare(
        task_id, db=db, source="session", dry_run=dry_run,
        claim_slot=not dry_run,           # per-task slot; released by record_execution_result
        shield_input=False,               # interactive path is human-supervised
    )

    result = {
        "task_id": task_id,
        "status": prep["status"],
        "steps": prep.get("steps", []),
    }
    for key in ("recommended_model", "model_id", "prompt_tokens_est",
                "approval_level", "error"):
        if key in prep:
            result[key] = prep[key]

    task = prep.get("task") or {}
    if task:
        _span_set(skill=task.get("skill", ""), project=task.get("project", ""),
                  worker=task.get("assignee", ""),
                  model=prep.get("model_id", ""),
                  recommended_model=prep.get("recommended_model", ""))

    if prep["status"] == "dry_run":
        result["prompt_preview"] = prep.get("prompt_preview", "")
        return result

    if not prep.get("ok"):
        # blocked / pending_approval / already_running / error — shape as-is.
        if prep["status"] == "pending":
            result["status"] = "error"
        return result

    # Ready: the actual execution happens via the Claude Agent tool in the
    # autopilot (or the API engine in autonomous mode). This path PREPARES
    # everything and RECORDS the result later via record_execution_result.
    result["status"] = "ready_for_execution"
    result["execution_prompt"] = prep["prompt"]
    result["skill"] = task.get("skill", "")
    result["worker"] = task.get("assignee", "")
    result["rubric"] = prep.get("rubric", {})
    return result


def record_execution_result(task_id: str, success: bool, output: str = "",
                            tokens: int = 0, score: int = 0, error: str = "") -> dict:
    """
    Record the result of an execution (called AFTER Claude finishes).

    Thin adapter over lifecycle.finalize_success/finalize_failure (Next-Gen
    N1). Session-path semantics, expressed as explicit parameters:
      - the autopilot's score feeds the after-pipeline (low score -> tripwire
        -> replan), unlike the API path which scores after the pipeline;
      - unscored (score == 0) completes as done (the session reviewer already
        saw the output);
      - tokens are ESTIMATED into the meter (70/30) — exact metering only
        exists on the API path.
    """
    db = DB()
    slot_caller = f"executor:{task_id}"

    task = db.get_task(task_id)
    if not task:
        try:
            from enforcement.parallelism_guard import release_by_caller
            release_by_caller(slot_caller)
        except Exception:
            pass
        return {"error": "Task not found"}

    if success:
        final_status = "done" if score >= 60 or score == 0 else "in_review"
        return lifecycle.finalize_success(
            task_id, task, output, tokens, score,
            db=db, source="session", model="opus", final_status=final_status,
            quality_score_for_filter=score,
            count_budget_on_tripwire=False,   # session tokens are captured by the transcript hook
            release_slot_caller=slot_caller,
            meter_tokens=True,
        )
    return lifecycle.finalize_failure(
        task_id, task, error, score,
        db=db, source="session", release_slot_caller=slot_caller,
    )



# =============================================================================
# WAVE EXECUTION — Multiple tasks in parallel
# =============================================================================

def execute_wave(dry_run: bool = False) -> dict:
    """Execute all ready tasks as a wave."""
    db = DB()
    ready = [t for t in db.get_tasks(status="todo") if t.get("assignee")]

    if not ready:
        return {"wave_size": 0, "status": "idle", "message": "No tasks ready for execution"}

    # Limit to max 3 parallel
    state = run_engine("core/state_machine.py", ["--json"])
    max_parallel = state.get("max_parallel", 3)
    wave = ready[:max_parallel]

    results = []
    for task in wave:
        r = execute_task(task["id"], dry_run=dry_run)
        results.append(r)

    return {
        "wave_size": len(wave),
        "max_parallel": max_parallel,
        "dry_run": dry_run,
        "tasks": results,
    }


# =============================================================================
# FULL PULSE — Complete heartbeat cycle via executor
# =============================================================================

def execute_pulse(dry_run: bool = False) -> dict:
    """
    Full heartbeat pulse through the executor.
    This is the DURABLE equivalent of /lucas-heartbeat.
    """
    db = DB()
    pulse = {
        "timestamp": datetime.now(UTC).isoformat(),
        "steps": {},
        "status": "ok",
    }

    # 0. State check
    state = run_engine("core/state_machine.py", ["--evaluate", "--json"])
    pulse["steps"]["state"] = state
    if state.get("state") == "GUARDIAN":
        pulse["status"] = "guardian_stop"
        return pulse

    # 1. Dispatch
    dispatch = run_engine("dispatch/dispatch_engine.py", ["--json"])
    pulse["steps"]["dispatch"] = dispatch

    # 2. AutoDiag
    diag = run_engine("core/autodiag_runner.py", ["--fix", "--json"])
    pulse["steps"]["autodiag"] = {"passed": diag.get("passed", 0), "total": diag.get("total", 0)}

    # 3. Execute wave
    wave = execute_wave(dry_run=dry_run)
    pulse["steps"]["wave"] = wave

    # 4. Budget
    budget = db.get_budget()
    pulse["steps"]["budget"] = budget

    # 5. Task counts
    pulse["steps"]["tasks"] = db.get_task_counts()

    # 6. Log
    db.log_event("executor", "pulse_executed", details=json.dumps({
        "dispatched": dispatch.get("dispatched", 0),
        "wave_size": wave.get("wave_size", 0),
        "state": state.get("state", "?"),
    }, default=str))

    return pulse


# =============================================================================
# MAIN
# =============================================================================

def main():
    # license_guard wired (v11.1+ hardening)
    try:
        from licensing.license_guard import enforce_or_exit
        enforce_or_exit("executor")
    except SystemExit:
        raise
    except Exception:
        pass  # license_guard unavailable — fail-open during dev/testing

    parser = argparse.ArgumentParser(
        description="DARIO Executor — Durable task execution engine",
    )
    parser.add_argument("--task", "-t", help="Execute single task")
    parser.add_argument("--wave", action="store_true", help="Execute next wave")
    parser.add_argument("--pulse", action="store_true", help="Full pulse cycle")
    parser.add_argument("--record", help="Record result for task (requires --success/--failed)")
    parser.add_argument("--success", action="store_true", help="Mark execution as success")
    parser.add_argument("--failed", action="store_true", help="Mark execution as failed")
    parser.add_argument("--output", default="", help="Execution output")
    parser.add_argument("--tokens", type=int, default=0, help="Tokens used")
    parser.add_argument("--score", type=int, default=0, help="Quality score")
    parser.add_argument("--error", default="", help="Error message")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Show without executing")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.json:
        logging.getLogger().setLevel(logging.ERROR)

    if args.record:
        result = record_execution_result(
            args.record, args.success, args.output, args.tokens, args.score, args.error
        )
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print(f"[{'+'if result.get('status')=='done' else '!'}] {args.record}: {result.get('status','?')}")
            for s in result.get("steps", []):
                print(f"  {s.get('step')}: {s}")
        return 0

    elif args.task:
        result = execute_task(args.task, dry_run=args.dry_run)
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print(f"=== EXECUTE: {args.task} → {result['status']} ===\n")
            for s in result.get("steps", []):
                print(f"  [{s.get('step')}] {s}")
            if result.get("prompt_preview"):
                print(f"\n  PROMPT PREVIEW:\n  {result['prompt_preview'][:300]}...")
        return 0 if result["status"] in ("ready_for_execution", "dry_run") else 2

    elif args.wave:
        result = execute_wave(dry_run=args.dry_run)
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print(f"=== WAVE: {result['wave_size']} tasks (max {result.get('max_parallel',3)}) ===\n")
            for t in result.get("tasks", []):
                print(f"  [{t.get('status')}] {t.get('task_id')}: {len(t.get('steps',[]))} steps")
        return 0

    elif args.pulse:
        result = execute_pulse(dry_run=args.dry_run)
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print(f"=== PULSE ({result['status']}) ===\n")
            for name, data in result.get("steps", {}).items():
                print(f"  {name}: {json.dumps(data, default=str)[:100]}")
        return 0

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
