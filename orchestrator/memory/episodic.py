"""Episodic memory — one record per task execution.

Each episode captures *what happened* during a task: outcome, corrections,
retrieved memories, failed tool calls. Episodes are append-only and feed
the Dream consolidation pipeline.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml

from .schemas import Episode, Outcome, utcnow

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
EPISODES_DIR = ORCH_DIR / "memory" / "episodes"
EPISODES_DIR.mkdir(parents=True, exist_ok=True)

EP_COUNTER_FILE = EPISODES_DIR / ".counter"


def _next_episode_id() -> str:
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    n = 0
    if EP_COUNTER_FILE.exists():
        try:
            saved_date, saved_n = EP_COUNTER_FILE.read_text().strip().split(":")
            if saved_date == today:
                n = int(saved_n)
        except Exception:
            n = 0
    n += 1
    EP_COUNTER_FILE.write_text(f"{today}:{n}")
    return f"EP-{today}-{n:03d}"


def episode_exists_for_task(task_id: str) -> bool:
    """Check if any episode already records this task_id (idempotency guard)."""
    if not task_id:
        return False
    for day_dir in EPISODES_DIR.iterdir():
        if not day_dir.is_dir() or day_dir.name.startswith("."):
            continue
        for path in day_dir.glob("EP-*.yaml"):
            try:
                with open(path, encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                if data.get("task_id") == task_id:
                    return True
            except Exception:
                continue
    return False


def write_episode(ep: Episode) -> Path:
    if not ep.episode_id:
        ep.episode_id = _next_episode_id()
    if not ep.timestamp:
        ep.timestamp = utcnow()
    day = ep.timestamp[:10]
    day_dir = EPISODES_DIR / day
    day_dir.mkdir(parents=True, exist_ok=True)
    path = day_dir / f"{ep.episode_id}.yaml"
    data = ep.model_dump(mode="json", exclude_none=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
    return path


def read_episode(episode_id: str) -> Episode | None:
    for day_dir in EPISODES_DIR.iterdir():
        if not day_dir.is_dir():
            continue
        path = day_dir / f"{episode_id}.yaml"
        if path.exists():
            with open(path, encoding="utf-8") as f:
                loaded: Episode = Episode.model_validate(yaml.safe_load(f))
                return loaded
    return None


def iter_episodes(window_days: int = 30, project: str | None = None) -> Iterable[Episode]:
    cutoff = datetime.now(UTC) - timedelta(days=window_days)
    cutoff_day = cutoff.strftime("%Y-%m-%d")
    for day_dir in sorted(EPISODES_DIR.iterdir()):
        if not day_dir.is_dir() or day_dir.name.startswith("."):
            continue
        if day_dir.name < cutoff_day:
            continue
        for path in sorted(day_dir.glob("EP-*.yaml")):
            try:
                with open(path, encoding="utf-8") as f:
                    ep = Episode.model_validate(yaml.safe_load(f))
                if project and ep.project != project:
                    continue
                yield ep
            except Exception:
                continue


def count_episodes(window_days: int = 30) -> int:
    return sum(1 for _ in iter_episodes(window_days))


def recent_for_project(project: str, n: int = 12, window_days: int = 14) -> list[Episode]:
    """Return last N episodes for a project (chronological order, newest last)."""
    if not project:
        return []
    eps = list(iter_episodes(window_days=window_days, project=project))
    eps.sort(key=lambda e: e.timestamp)
    return eps[-n:]


def quick_record(
    task_id: str,
    skill: str,
    outcome: str,
    score: int | None = None,
    project: str = "",
    duration_seconds: float = 0.0,
    tokens_used: int = 0,
    model: str = "",
    output_summary: str = "",
) -> Episode:
    """One-line helper for executor.py / hooks.py integration."""
    ep = Episode(
        episode_id="",
        task_id=task_id,
        skill=skill,
        outcome=Outcome(outcome),
        score=score,
        project=project,
        duration_seconds=duration_seconds,
        tokens_used=tokens_used,
        model=model,
        output_summary=output_summary[:500],
    )
    write_episode(ep)
    return ep


def stats(window_days: int = 7) -> dict:
    by_outcome: dict[str, int] = {}
    by_skill: dict[str, int] = {}
    total = 0
    score_sum = 0
    score_n = 0
    for ep in iter_episodes(window_days):
        total += 1
        by_outcome[ep.outcome.value] = by_outcome.get(ep.outcome.value, 0) + 1
        by_skill[ep.skill] = by_skill.get(ep.skill, 0) + 1
        if ep.score is not None:
            score_sum += ep.score
            score_n += 1
    return {
        "total": total,
        "window_days": window_days,
        "by_outcome": by_outcome,
        "by_skill": dict(sorted(by_skill.items(), key=lambda x: -x[1])[:10]),
        "avg_score": round(score_sum / score_n, 1) if score_n else None,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "stats":
        print(json.dumps(stats(int(sys.argv[2]) if len(sys.argv) > 2 else 7), indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "list":
        for ep in iter_episodes(7):
            print(f"  {ep.episode_id}  {ep.skill:30s}  {ep.outcome.value:8s}  score={ep.score}")
    else:
        print(json.dumps(stats(), indent=2))
