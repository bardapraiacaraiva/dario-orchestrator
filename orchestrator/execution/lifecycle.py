"""The ONE task lifecycle shared by both execution engines (Next-Gen N1, 2026-06-12).

Before this module, executor.py (session path) and providers/anthropic.py
(autonomous API path) each implemented the full lifecycle — prepare
(guardrails → context → rubric → trace → prompt → gates → checkout) and
finalize (filter-after → tripwire → score → complete → write-backs) — as two
hand-maintained copies. The C1 quality-gate bug existed on only one of them;
the API path silently lacked the approval gate, interrupt check, error
handlers and task_fail hook; the session path lacked pre/post-conditions.
Every lifecycle fix had to be made twice.

Both engines are now thin adapters over prepare() / finalize_success() /
finalize_failure(). Where the two paths deliberately differ, the difference
is an explicit PARAMETER here (greppable), not a divergent copy:

  - quality_score_for_filter: the session path feeds the autopilot's score to
    the after-pipeline (low score → tripwire → replan); the API path feeds
    None (output is unscored at pipeline time — the real gate is final_status,
    see the C1 fix) and scores via Haiku before finalize.
  - claim_slot: the session executor claims a per-task parallelism slot at
    checkout; the autonomous pulse already executes under a pulse-level slot.
  - shield_input: the API path inspects the assembled prompt for injection
    BEFORE checkout (untrusted text reaches the API unsupervised); the
    interactive session is human-supervised.
  - meter_tokens: the session path estimates a 70/30 split into the token
    meter; the API path gets exact per-call metering from TrackedAnthropic.

Budget accounting stays OUT of this module by design: db.complete_task is the
sole budget writer (Fase 2, 2026-06-12); the only exception is the tripwire
quarantine on the API path, where spent tokens would otherwise vanish.
"""

import json
import logging
import subprocess
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from core.db import DB
from execution.pipeline import build_execution_pipeline

log = logging.getLogger("lifecycle")

PYTHON = sys.executable

# Module-level shared pipeline — both adapters use this single instance unless
# they inject their own (tests do).
PIPELINE = build_execution_pipeline()


def run_engine(script: str, args: list, timeout: int = 30) -> dict:
    """Run an orchestrator engine script, return parsed JSON (best-effort)."""
    path = ORCH_DIR / script
    if not path.exists():
        return {"error": f"{script} not found"}
    try:
        r = subprocess.run([PYTHON, str(path)] + args,
                           capture_output=True, text=True, timeout=timeout, cwd=str(ORCH_DIR))
        if r.stdout.strip():
            try:
                return json.loads(r.stdout.strip())
            except json.JSONDecodeError:
                return {"raw": r.stdout.strip()[:300], "exit_code": r.returncode}
        return {"exit_code": r.returncode, "stderr": r.stderr.strip()[:200]}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": str(e)[:200]}


def build_execution_prompt(task: dict, context_block: str, rubric: dict) -> str:
    """Build the structured execution prompt (single source for both engines)."""
    skill = task.get("skill", "")
    title = task.get("title", "")
    description = task.get("description", "")
    project = task.get("project", "")
    policy = task.get("execution_policy", "default")

    rubric_text = ""
    if rubric.get("dimensions"):
        rubric_text = "## Scoring Rubric (how this output will be evaluated):\n"
        for d in rubric.get("dimensions", []):
            rubric_text += f"- **{d.get('name')}** ({d.get('weight', 0):.0%}): {d.get('description', '')}\n"
        rubric_text += f"\nPass threshold: {rubric.get('pass_threshold', 60)}/100\n"

    has_context = bool(context_block and context_block.strip() and "###" in context_block)

    if has_context:
        context_instruction = (
            "You have real project data in the Context section below. "
            "USE IT — reference specific names, numbers, and facts from the context. "
            "Do NOT invent data when real data is provided. "
            "Do NOT add [CONFIRMAR] or placeholder tags for information already in the context."
        )
    else:
        context_instruction = (
            "No project-specific data was provided. To maximize usefulness:\n"
            "- Use REALISTIC invented examples clearly marked as [EXEMPLO]\n"
            "- Base assumptions on the Portuguese market and the business type described\n"
            "- Make the output a READY-TO-EDIT DRAFT, not a template with blanks\n"
            "- Include a short 'Dados a Confirmar' section at the end listing what the client must verify"
        )

    prompt = f"""# Task Execution: {task.get('id', '')}

## Assignment
- **Title:** {title}
- **Skill:** /{skill}
- **Project:** {project}
- **Policy:** {policy}

## Description
{description}

## Instructions
{context_instruction}

{rubric_text}

## Context
{context_block if context_block else '(none provided)'}
"""
    return prompt


# =============================================================================
# PREPARE — everything before the actual execution
# =============================================================================

def prepare(task_id: str, *, db: DB | None = None, pipeline=None,
            source: str = "session", model_override: str | None = None,
            dry_run: bool = False, claim_slot: bool = False,
            shield_input: bool = False) -> dict:
    """Shared pre-execution lifecycle. Returns a dict with ok/status/steps.

    On ok=True the caller receives task, prompt, model recommendation,
    filter_ctx, context_block and rubric, with the task already CHECKED OUT
    (unless dry_run). On ok=False, status explains the short-circuit
    (blocked / pending_approval / already_running / dry_run / error).
    """
    db = db or DB()
    pipeline = pipeline or PIPELINE
    actor = "api-executor" if source == "api" else "executor"
    result = {"task_id": task_id, "ok": False, "status": "pending", "steps": []}

    task = db.get_task(task_id)
    if not task:
        result.update(status="error", error="Task not found in DB")
        return result

    # Pre-conditions (task-format-spec v1) — was API-only, now both paths.
    spec_pre = run_engine("core/task_spec.py", ["--check-pre", task_id, "--json"])
    if not spec_pre.get("pass", True) and spec_pre.get("blockers"):
        result.update(status="blocked", error=f"Pre-conditions: {spec_pre['blockers']}")
        return result
    result["steps"].append({"step": "pre_conditions", "pass": spec_pre.get("pass", True)})

    # Reload after enrichment (check-pre may have added fields).
    task = db.get_task(task_id) or task
    skill = task.get("skill", "")
    project = task.get("project", "")
    worker = task.get("assignee", "")

    # Filter pipeline — BEFORE (logging, model routing, budget).
    filter_ctx = pipeline.before(task)
    result["steps"].append({
        "step": "filter_pipeline_before",
        "blocked": filter_ctx.get("blocked", False),
        "model": filter_ctx.get("recommended_model", "sonnet"),
    })
    if filter_ctx.get("blocked"):
        result.update(status="blocked",
                      error=f"Filter pipeline blocked: {filter_ctx.get('block_reason', '?')}")
        db.log_event(actor, "task_blocked", task_id=task_id,
                     details=f"Pipeline: {filter_ctx.get('block_reason', '?')}")
        return result

    result["recommended_model"] = model_override or filter_ctx.get("recommended_model", "sonnet")
    result["model_id"] = filter_ctx.get("model_id", "claude-sonnet-4-6")
    result["filter_ctx"] = filter_ctx

    # Lifecycle hook — task_start (was session-only).
    try:
        from core.lifecycle_hooks import get_registry
        get_registry().emit("task_start", task=task)
    except Exception:
        pass

    # Guardrails — direct import on both paths (the API path used a
    # subprocess; one in-process call is faster and cannot drift).
    from safety.guardrails import validate_task
    guard = validate_task(task_id)
    verdict = guard.get("verdict", "FAIL")
    result["steps"].append({"step": "guardrails", "result": verdict,
                            "checks": guard.get("checks", {})})
    if verdict == "FAIL":
        result.update(status="blocked", error=f"Guardrails FAIL: {guard.get('errors', [])}")
        db.log_event(actor, "task_blocked", task_id=task_id,
                     details=f"Guardrails: {guard.get('errors', [])}")
        return result

    # Context injection + adaptive rubric + trace start.
    context = run_engine("cognitive/context_injector.py", ["--task", task_id, "--json"])
    context_block = context.get("context_block", "")
    result["steps"].append({"step": "context", "sources": context.get("sources_used", 0)})

    rubric = run_engine("quality/adaptive_rubric.py", ["--task", task_id, "--json"])
    result["steps"].append({"step": "rubric", "dimensions": rubric.get("dimensions_count", 5)})

    run_engine("observability/tracer.py", ["--start", "--task", task_id, "--skill", skill,
                                           "--worker", worker, "--project", project,
                                           "--context", context_block[:200]])

    prompt = build_execution_prompt(task, context_block, rubric)
    result.update(task=task, prompt=prompt, context_block=context_block, rubric=rubric)
    result["prompt_tokens_est"] = len(prompt) // 4

    if dry_run:
        result.update(ok=True, status="dry_run", prompt_preview=prompt[:500])
        return result

    # Approval gate — was session-only; the autonomous path executed
    # approval-requiring skills unattended. Now both paths stop here.
    try:
        from safety.approval_gates import get_approval_level, request_approval
        approval = get_approval_level(task)
        if approval.get("needs_approval"):
            request_approval(task_id, reason=f"Skill '{skill}' requires {approval['level']} approval")
            result.update(status="pending_approval", approval_level=approval["level"])
            result["steps"].append({"step": "approval_gate", "level": approval["level"]})
            return result
    except Exception:
        pass  # approval-gate failure must not block execution

    # Prompt shield — input (API path: untrusted text reaches the API
    # unsupervised; block BEFORE checkout so a poisoned task costs zero).
    if shield_input:
        from safety.prompt_shield import inspect_input
        shield_verdict = inspect_input(prompt)
        result["steps"].append({"step": "prompt_shield",
                                "block": shield_verdict.get("block", False)})
        if shield_verdict.get("block"):
            reason = shield_verdict.get("reason", "prompt injection pattern")
            log.warning(f"[SHIELD] {task_id}: {reason}")
            db.block_task(task_id, f"prompt_shield: {reason[:200]}")
            db.log_event(actor, "task_blocked", task_id=task_id,
                         details=f"prompt_shield: {reason[:200]}")
            result.update(status="blocked", error=f"Prompt shield: {reason}")
            return result

    # Parallelism slot (session path; the pulse holds its own slot).
    if claim_slot:
        from enforcement.parallelism_guard import ParallelismExceededError, claim_slot as _claim
        try:
            _claim(caller=f"executor:{task_id}")
        except ParallelismExceededError as e:
            result.update(status="blocked", error=f"Parallelism guard: {e}")
            db.log_event(actor, "task_blocked", task_id=task_id,
                         details=f"parallelism_guard: {e}")
            return result

    # Atomic checkout.
    if not db.checkout_task(task_id):
        if claim_slot:
            from enforcement.parallelism_guard import release_by_caller
            release_by_caller(f"executor:{task_id}")
        result.update(status="already_running",
                      error="Task could not be checked out (already in_progress or not todo)")
        return result

    result["steps"].append({"step": "checked_out"})
    try:
        # Execution journal (N2): marks the start of the at-risk window.
        db.journal_step(task_id, "checked_out",
                        payload={"source": source,
                                 "model": result.get("recommended_model", "")})
    except Exception:
        pass
    db.log_event(actor, "task_executing", task_id=task_id,
                 details=f"skill={skill} worker={worker} prompt_tokens={result['prompt_tokens_est']}")
    result.update(ok=True, status="ready")
    return result


# =============================================================================
# FINALIZE — everything after the actual execution
# =============================================================================

def finalize_success(task_id: str, task: dict, output: str, tokens: int, score: int, *,
                     db: DB | None = None, pipeline=None, source: str = "session",
                     model: str = "opus", final_status: str | None = None,
                     quality_score_for_filter: int | None = None,
                     count_budget_on_tripwire: bool = False,
                     release_slot_caller: str | None = None,
                     meter_tokens: bool = False,
                     duration_seconds: float = 0.0) -> dict:
    """Shared post-execution lifecycle for a successful run."""
    db = db or DB()
    pipeline = pipeline or PIPELINE
    actor = "api-executor" if source == "api" else "executor"
    skill = task.get("skill", "")
    project = task.get("project", "")
    result = {"task_id": task_id, "steps": []}

    if release_slot_caller:
        try:
            from enforcement.parallelism_guard import release_by_caller
            release_by_caller(release_slot_caller)
        except Exception:
            pass  # stale-slot reaping (1h) is the backstop

    # Prompt shield — output (masks leaked secrets; SSH key blocks entirely).
    try:
        from safety.prompt_shield import inspect_output
        out_verdict = inspect_output(output)
        if out_verdict.get("block"):
            reason = out_verdict.get("reason", "critical secret in output")
            log.warning(f"[SHIELD] {task_id}: {reason}")
            db.block_task(task_id, f"prompt_shield: {reason[:200]}")
            if count_budget_on_tripwire and tokens > 0:
                db.update_budget(tokens)
            try:
                db.journal_step(task_id, "finalized", status="tripwire",
                                payload={"reason": f"prompt_shield: {reason[:200]}"})
            except Exception:
                pass
            db.log_event(actor, "task_tripwire", task_id=task_id,
                         details=f"prompt_shield: {reason[:200]}")
            result.update(status="tripwire", tripwire_reason=reason)
            return result
        if out_verdict.get("sanitized") and out_verdict["sanitized"] != output:
            kinds = sorted({m.get("kind", m.get("type", "?"))
                            for m in out_verdict.get("matches", [])})
            log.warning(f"[SHIELD] {task_id}: output sanitized ({', '.join(kinds)})")
            output = out_verdict["sanitized"]
            result["steps"].append({"step": "output_sanitized", "masked": kinds})
    except Exception:
        pass  # shield failure must not lose a paid-for output

    # Filter pipeline — AFTER (schema, output guardrails, quality gate, spend log).
    filter_ctx = {"actual_tokens": tokens, "quality_score": quality_score_for_filter}
    after_result = pipeline.after(task, output, filter_ctx)
    result["steps"].append({
        "step": "filter_pipeline_after",
        "tripwire": after_result.get("tripwire", False),
        "tripwire_reason": after_result.get("tripwire_reason", ""),
        "schema_valid": after_result.get("schema_valid", True),
    })

    if after_result.get("tripwire"):
        reason = after_result.get("tripwire_reason", "?")
        log.warning(f"[TRIPWIRE] {task_id}: {reason}")
        run_engine("observability/tracer.py", ["--end", "--task", task_id,
                                               "--status", "tripwire", "--error", reason[:300]])
        if count_budget_on_tripwire and tokens > 0:
            # API tokens were spent even though the output is quarantined —
            # the blocked task never reaches complete_task (sole budget writer).
            db.block_task(task_id, f"Tripwire: {reason[:200]}")
            db.update_budget(tokens)
        else:
            replan = run_engine("execution/replanner.py", [
                "--task", task_id, "--failure", "output_guardrail_tripwire",
                "--score", str(score), "--error", reason[:200], "--json"])
            result["steps"].append({"step": "replanned_tripwire",
                                    "action": replan.get("action", "?")})
        try:
            db.journal_step(task_id, "finalized", status="tripwire",
                            payload={"reason": reason[:200]})
        except Exception:
            pass
        db.log_event(actor, "task_tripwire", task_id=task_id, details=f"Tripwire: {reason[:100]}")
        result.update(status="tripwire", tripwire_reason=reason)
        return result

    run_engine("observability/tracer.py", ["--end", "--task", task_id, "--status", "success",
                                           "--tokens", str(tokens), "--score", str(score),
                                           "--output", output[:300]])
    result["steps"].append({"step": "trace_end", "status": "success"})

    if score > 0:
        run_engine("quality/quality_scorer.py", [
            "--task", task_id, "--score", str(score),
            "--skill", skill, "--project", project, "--json"])
        result["steps"].append({"step": "scored", "score": score})

    # Human-in-the-loop interrupt — was session-only; the autonomous path
    # completed interrupt-worthy outputs unattended. Now both paths stop here.
    try:
        from execution.checkpoint_interrupt import interrupt_task, should_interrupt
        interrupt_check = should_interrupt(task, output=output, score=score)
        if interrupt_check.get("interrupt"):
            interrupt_task(task_id, reason=interrupt_check["reason"],
                           checkpoint_data={"score": score, "tokens": tokens,
                                            "partial_output": output[:500]})
            result.update(status="awaiting_human",
                          interrupt_reason=interrupt_check["reason"])
            result["steps"].append({"step": "interrupted",
                                    "reason": interrupt_check["reason"]})
            db.log_event(actor, "task_interrupted", task_id=task_id,
                         details=interrupt_check["reason"][:200])
            try:
                from memory import hooks as mem_hooks
                mem_hooks.on_task_complete(
                    task_id=task_id, skill=skill, outcome="revision",
                    score=score if score else None, project=project,
                    duration_seconds=duration_seconds, tokens_used=int(tokens or 0),
                    model=model, output_summary=(output or "")[:500] + " [AWAITING HUMAN]")
            except Exception:
                pass
            return result
    except Exception:
        pass  # interrupt failure must not block completion

    # Complete in DB (the adapter decides the status rule for its path).
    status = final_status or ("done" if score >= 60 else "in_review")
    db.complete_task(task_id, score=score, tokens=tokens, output=output[:2000], status=status)
    result["steps"].append({"step": "completed", "final_status": status})
    result["status"] = status

    # Learning write-backs (synaptic, Q-value, CoT post-mortem, episodes…).
    try:
        from execution.completion_hooks import run_learning_writebacks
        _wb = run_learning_writebacks(
            task=task if isinstance(task, dict) else {}, task_id=task_id,
            skill=skill, project=project, score=score, tokens=int(tokens or 0),
            status=status, output=output, model=model,
            duration_seconds=duration_seconds)
        if _wb:
            result.update({k: v for k, v in _wb.items()
                           if k in ("synaptic_updates", "reactive_tasks_created")})
    except Exception:
        pass

    # Token meter — session path only (the API path gets exact metering
    # from TrackedAnthropic; a second write would double the ledger).
    if meter_tokens and tokens > 0:
        try:
            run_engine("observability/token_meter.py", [
                "--input", str(int(tokens * 0.7)), "--output", str(int(tokens * 0.3)),
                "--model", model, "--skill", skill, "--project", project or "unknown"])
        except Exception:
            pass

    # Post-conditions (task-format-spec v1) — was API-only, now both paths.
    spec_post = run_engine("core/task_spec.py", ["--check-post", task_id, "--json"])
    result["steps"].append({"step": "post_conditions", "pass": spec_post.get("pass", True),
                            "issues": spec_post.get("issues", [])})

    try:
        db.journal_step(task_id, "finalized", status=status,
                        payload={"score": score, "tokens": tokens})
    except Exception:
        pass
    db.log_event(actor, "task_completed", task_id=task_id,
                 details=f"score={score} tokens={tokens} status={status}")
    result["sanitized_output"] = output
    return result


def finalize_failure(task_id: str, task: dict, error: str, score: int = 0, *,
                     db: DB | None = None, source: str = "session",
                     release_slot_caller: str | None = None) -> dict:
    """Shared post-execution lifecycle for a failed run."""
    db = db or DB()
    actor = "api-executor" if source == "api" else "executor"
    skill = task.get("skill", "")
    result = {"task_id": task_id, "steps": []}

    if release_slot_caller:
        try:
            from enforcement.parallelism_guard import release_by_caller
            release_by_caller(release_slot_caller)
        except Exception:
            pass

    run_engine("observability/tracer.py", ["--end", "--task", task_id,
                                           "--status", "failed", "--error", error[:300]])
    result["steps"].append({"step": "trace_end", "status": "failed"})

    # Per-skill error handlers — was session-only, now both paths.
    try:
        from reliability.error_handlers import get_error_registry
        handler = get_error_registry().get(skill)
        recovery = handler.handle(Exception(error), task, {"_retry_count": 0})
        result["steps"].append({"step": "error_handler", "action": recovery.action,
                                "recovered": recovery.recovered})
        if recovery.recovered and recovery.action == "skip":
            result["status"] = "skipped"
            db.log_event(actor, "task_skipped", task_id=task_id, details=recovery.reason[:200])
            return result
    except Exception:
        pass

    # Replan with a COMPUTED failure type (the API path hardcoded
    # agent_timeout for every failure, which skewed strategy selection).
    failure_type = ("agent_timeout" if "timeout" in error.lower()
                    else "quality_below_50" if 0 < score < 50
                    else "unknown")
    replan = run_engine("execution/replanner.py", [
        "--task", task_id, "--failure", failure_type,
        "--score", str(score), "--error", error[:200], "--json"])
    result["steps"].append({"step": "replanned", "action": replan.get("action", "?")})
    result.update(status="replanned", replan_action=replan.get("action"), error=error)

    # Lifecycle hook — task_fail (was session-only).
    try:
        from core.lifecycle_hooks import get_registry
        get_registry().emit("task_fail", task=task, error=error[:200])
    except Exception:
        pass

    try:
        db.journal_step(task_id, "finalized", status="failed",
                        payload={"error": error[:200],
                                 "replan": replan.get("action", "?")})
    except Exception:
        pass
    db.log_event(actor, "task_failed", task_id=task_id,
                 details=f"error={error[:100]} replan={replan.get('action', '?')}")
    return result
