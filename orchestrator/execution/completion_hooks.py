"""Shared post-completion learning write-backs.

Single home for the cognitive feedback that must fire whenever a task finishes,
regardless of which executor ran it. Before this (Fase 2, 2026-06-12) the full
set lived only in execution.executor.record_execution_result, so tasks completed
through the autonomous API path (providers.anthropic) never updated synaptic
weights, Q-values, CoT post-mortems, episodes, etc. — the "system that learns"
did not learn in the mode that generates the most volume (audit finding F-08).

Both executors now call run_learning_writebacks() so the loop closes on every
path. Budget/token accounting is deliberately NOT here: budget is owned solely
by core.db.complete_task, and the per-model spend ledger (token_meter) is
path-specific — folding either in would re-introduce the double-count that
Fase 2 just removed.

Every hook is best-effort and self-isolating: a failure in one never blocks
completion or the others.
"""
from __future__ import annotations

import logging
from typing import Any

log = logging.getLogger("completion_hooks")


def run_learning_writebacks(
    *,
    task: dict[str, Any],
    task_id: str,
    skill: str,
    project: str,
    score: int,
    tokens: int,
    status: str,
    output: str,
    model: str = "opus",
    duration_seconds: float = 0.0,
    retrieved_memories: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Fire all cognitive write-backs for a finished task.

    Returns a small dict describing what ran (for the caller's result/log).
    Mirrors the conditions previously inlined in executor.record_execution_result.
    """
    info: dict[str, Any] = {}
    out = output or ""

    # ── Synaptic weights write-back (co-activation reinforcement) ──────────
    if status == "done" and score > 0 and skill and project:
        try:
            from cognitive.synaptic_update import process_completion as _synaptic_update
            deltas = _synaptic_update(task_id=task_id, skill=skill,
                                      project=project, score=score)
            if deltas:
                info["synaptic_updates"] = len(deltas)
        except Exception:
            log.debug("synaptic write-back skipped", exc_info=True)

    # ── Q-value memory (TD-learning episode for future dispatch) ───────────
    if status == "done" and score > 0 and skill:
        try:
            from cognitive.qvalue_memory_wire import record_outcome as _qvm_record
            ctx = f"{task.get('title', '')} {task.get('description', '')}".strip()
            if ctx:
                _qvm_record(context=ctx[:500], skill=skill, score=score,
                            tokens_used=int(tokens or 0), project=project)
                info["qvalue_recorded"] = True
        except Exception:
            log.debug("qvalue write-back skipped", exc_info=True)

    # ── Dispatch CoT post-mortem (recalibrate overconfident dispatches) ────
    if score > 0:
        try:
            from dispatch.dispatch_cot import postmortem as _cot_postmortem
            _cot_postmortem(task_id, score, "success" if status == "done" else "revision")
            info["cot_postmortem"] = True
        except Exception:
            log.debug("cot post-mortem skipped", exc_info=True)

    # ── Auto-learn + episode→semantic promotion (excellence only) ──────────
    if score >= 90:
        try:
            from cognitive.memory_blocks import auto_learn
            auto_learn(out[:200], scope=project or "global", skill=skill, score=score)
            info["auto_learned"] = True
        except Exception:
            log.debug("auto_learn skipped", exc_info=True)
        try:
            from cognitive.episode_promoter import promote as _promote_episodes
            _promote_episodes(days=7, generate_rules=True, verbose=False)
            info["episodes_promoted"] = True
        except Exception:
            log.debug("episode promotion skipped", exc_info=True)

    # ── Reactive subscriptions (trigger downstream tasks) ──────────────────
    if status == "done":
        try:
            from reliability.reactive_subscriptions import on_task_completed
            created = on_task_completed(task, score=score, tokens=tokens)
            if created:
                info["reactive_tasks_created"] = len(created)
        except Exception:
            log.debug("reactive subscriptions skipped", exc_info=True)

    # ── Lifecycle hooks (emit events to subscribers) ───────────────────────
    try:
        from core.lifecycle_hooks import get_registry
        registry = get_registry()
        registry.emit("task_complete", task=task, output=out[:200], score=score)
        if score >= 90:
            registry.emit("quality_scored", task=task, score=score)
    except Exception:
        log.debug("lifecycle hooks skipped", exc_info=True)

    # ── Episodic memory (Memory & Dreaming subsystem) ──────────────────────
    try:
        from memory import hooks as mem_hooks
        # Consume memories staged at context-injection time so retrieval_count /
        # last_retrieved actually move and the dream prune can tell useful
        # memories from junk (DD finding A13, 2026-06-12).
        rms = retrieved_memories
        if rms is None:
            try:
                from memory import retrieval as mem_retrieval
                rms = mem_retrieval.pop_pending(task_id)
            except Exception:
                rms = []
        mem_hooks.on_task_complete(
            task_id=task_id,
            skill=skill,
            outcome="success" if status == "done" else "revision",
            score=score if score else None,
            project=project,
            duration_seconds=float(duration_seconds or 0.0),
            tokens_used=int(tokens or 0),
            model=model,
            output_summary=out[:500],
            retrieved_memories=rms or None,
        )
        info["episode_recorded"] = True
        if rms:
            info["retrieved_memories_tracked"] = len(rms)
    except Exception:
        log.debug("episodic memory skipped", exc_info=True)

    return info
