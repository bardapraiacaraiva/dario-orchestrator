"""Statistical pattern detection across episodes.

Surfaces:
  - Skills with declining quality scores
  - Repeated failed tool calls
  - Frequent correction clusters
  - Skills that consistently retrieve the same memory
"""

from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean
from typing import Any

# Thresholds live in config/memory_dream.yaml — single source instead of
# magic numbers (DD finding A13, 2026-06-12).
try:
    from memory.config import get as _cfg
    TREND_MIN_RUNS = int(_cfg("pattern_trend_min_runs"))
    FAILURE_MIN = int(_cfg("pattern_failure_min"))
    CONVERGENCE_MIN_SESSIONS = int(_cfg("convergence_min_sessions"))
except Exception:  # pragma: no cover - memory package always present in installs
    TREND_MIN_RUNS, FAILURE_MIN, CONVERGENCE_MIN_SESSIONS = 3, 2, 2


def detect_patterns(episodes: list[Any]) -> list[str]:
    """Return list of human-readable pattern descriptions."""
    patterns: list[str] = []
    by_skill_scores: dict[str, list[int]] = defaultdict(list)
    by_skill_failures: dict[str, int] = defaultdict(int)
    tool_failures: Counter[str] = Counter()
    correction_skills: Counter[str] = Counter()

    for ep in episodes:
        if ep.score is not None:
            by_skill_scores[ep.skill].append(ep.score)
        if ep.outcome.value in ("failure", "blocked"):
            by_skill_failures[ep.skill] += 1
        for f in ep.failed_tool_calls:
            tool_failures[f.tool] += 1
        for _ in ep.corrections:
            correction_skills[ep.skill] += 1

    for skill, scores in by_skill_scores.items():
        if len(scores) >= TREND_MIN_RUNS:
            first_half = mean(scores[: len(scores) // 2])
            second_half = mean(scores[len(scores) // 2 :])
            if first_half - second_half >= 10:
                patterns.append(
                    f"Quality regression in `{skill}`: avg dropped from {first_half:.0f} → {second_half:.0f} "
                    f"across {len(scores)} runs"
                )
            elif second_half - first_half >= 10:
                patterns.append(
                    f"Quality improvement in `{skill}`: avg rose from {first_half:.0f} → {second_half:.0f}"
                )

    for skill, n in by_skill_failures.items():
        if n >= FAILURE_MIN:
            patterns.append(f"`{skill}` failed {n} times in this window — investigate root cause")

    for tool, n in tool_failures.most_common(5):
        if n >= FAILURE_MIN:
            patterns.append(f"Tool `{tool}` failed {n} times — possibly unstable or misused")

    for skill, n in correction_skills.most_common(5):
        if n >= 2:
            patterns.append(f"`{skill}` received {n} user corrections — review prompt or rubric")

    return patterns


def detect_convergence(episodes: list[Any], min_sessions: int | None = None, min_len: int = 2) -> list[dict[str, Any]]:
    """Detect skill sequences that recur across multiple sessions.

    Groups episodes by project + day, extracts skill sequence, then finds
    n-grams that appear in >= min_sessions distinct days.
    """
    if min_sessions is None:
        min_sessions = CONVERGENCE_MIN_SESSIONS
    by_session: dict[str, list[str]] = defaultdict(list)
    for ep in sorted(episodes, key=lambda e: e.timestamp):
        day = ep.timestamp[:10]
        session_key = f"{ep.project or 'global'}::{day}"
        by_session[session_key].append(ep.skill)

    ngram_sessions: dict[tuple[Any, ...], set[str]] = defaultdict(set)
    for session_key, skills in by_session.items():
        for size in range(min_len, min(6, len(skills) + 1)):
            for i in range(len(skills) - size + 1):
                gram = tuple(skills[i : i + size])
                if len(set(gram)) < size:
                    continue
                ngram_sessions[gram].add(session_key)

    convergent = []
    for gram, sessions in ngram_sessions.items():
        if len(sessions) >= min_sessions:
            convergent.append({
                "sequence": list(gram),
                "session_count": len(sessions),
                "projects": sorted({s.split("::")[0] for s in sessions}),
            })
    convergent.sort(key=lambda x: (-int(x["session_count"]), -len(x["sequence"])))  # type: ignore[arg-type,call-overload]
    return convergent[:10]
