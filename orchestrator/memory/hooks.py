"""Integration hooks — thin facade for executor.py and other callers.

Existing modules (executor, context_injector, session_boot) should call these
functions instead of importing each memory submodule directly.
"""

from __future__ import annotations

from . import cache, episodic, procedural, retrieval, semantic


def on_task_complete(
    task_id: str,
    skill: str,
    outcome: str,
    score: int | None = None,
    project: str = "",
    duration_seconds: float = 0.0,
    tokens_used: int = 0,
    model: str = "",
    output_summary: str = "",
    retrieved_memories: list[dict] | None = None,
) -> str:
    """Called by executor.py after each task. Returns episode_id."""
    ep = episodic.quick_record(
        task_id=task_id,
        skill=skill,
        outcome=outcome,
        score=score,
        project=project,
        duration_seconds=duration_seconds,
        tokens_used=tokens_used,
        model=model,
        output_summary=output_summary,
    )
    for rm in (retrieved_memories or []):
        retrieval.log_retrieval(
            episode_id=ep.episode_id,
            memory_id=rm["memory_id"],
            layer=rm.get("layer", "semantic"),
            relevance=rm.get("relevance", "medium"),
        )
        if rm.get("layer", "semantic") == "semantic":
            semantic.increment_retrieval(rm["memory_id"])

    # Detect workflow completion — count usage when trailing skills match a known sequence
    if outcome == "success" and project:
        try:
            recent = episodic.recent_for_project(project, n=12, window_days=14)
            trailing_skills = [e.skill for e in recent if e.skill]
            completed = procedural.detect_completed(trailing_skills, project=project)
            for wf in completed:
                window_eps = recent[-len(wf.skills_sequence):]
                window_scores = [e.score for e in window_eps if e.score is not None]
                avg = int(sum(window_scores) / len(window_scores)) if window_scores else None
                procedural.record_usage(wf.workflow_id, success=True, score=avg)
        except Exception:
            pass

    return ep.episode_id


def assemble_context_pack(project: str = "", initial_skills: list[str] | None = None) -> dict:
    """Called by context_injector.py at task start. Returns memory pack for prompt."""
    workflows = procedural.find_applicable(project=project, skill_context=initial_skills or [])
    return {
        "procedural_hints": [
            {
                "name": wf.name,
                "skills_sequence": wf.skills_sequence,
                "avg_score": wf.avg_score,
                "use_count": wf.use_count,
            }
            for wf in workflows[:3]
        ],
        "semantic_stats": semantic.stats(),
    }


def try_cache(skill: str, input_text: str) -> str | None:
    """Check cache before invoking a skill. Returns cached output or None."""
    entry = cache.get(skill, input_text)
    return entry.output if entry else None


def save_cache(skill: str, input_text: str, output: str, tokens_saved: int = 0) -> None:
    cache.put(skill, input_text, output, tokens_saved=tokens_saved)


def health() -> dict:
    return {
        "episodic": episodic.stats(7),
        "semantic": semantic.stats(),
        "procedural": procedural.stats(),
        "cache": cache.stats(),
        "retrieval": retrieval.stats(30),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(health(), indent=2, default=str))
