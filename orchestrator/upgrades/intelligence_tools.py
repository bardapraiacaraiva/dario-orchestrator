"""Tool Memory subsystem (extracted from `upgrades/intelligence.py` — Onda 6 #1).

`ToolPattern` dataclass + `ToolMemory` class. MemOS-inspired persistence
of successful tool-use sequences so agents can re-use proven plans.

Parent `upgrades/intelligence.py` re-imports these for backward-compat.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class ToolPattern:
    """A learned tool-use pattern."""

    pattern_id: str = field(default_factory=lambda: uuid.uuid4().hex[:10])
    skill: str = ""
    tool_sequence: list[str] = field(default_factory=list)
    success_rate: float = 0.0
    avg_tokens: int = 0
    usage_count: int = 0
    last_used: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class ToolMemory:
    """Persist successful tool-use sequences for reuse.

    Inspired by MemOS's tool memory for agent planning.
    """

    def __init__(self):
        self._patterns: dict[str, ToolPattern] = {}

    def record_sequence(
        self,
        skill: str,
        tools: list[str],
        success: bool,
        tokens: int = 0,
    ):
        """Record a tool-use sequence and its outcome."""
        key = f"{skill}:{'→'.join(tools)}"

        if key in self._patterns:
            p = self._patterns[key]
            p.usage_count += 1
            p.success_rate = (
                (p.success_rate * (p.usage_count - 1)) + (1.0 if success else 0.0)
            ) / p.usage_count
            p.avg_tokens = int(
                (p.avg_tokens * (p.usage_count - 1) + tokens) / p.usage_count
            )
            p.last_used = datetime.now(UTC).isoformat()
        else:
            self._patterns[key] = ToolPattern(
                skill=skill,
                tool_sequence=tools,
                success_rate=1.0 if success else 0.0,
                avg_tokens=tokens,
                usage_count=1,
            )

    def recommend(self, skill: str, top_k: int = 3) -> list[dict]:
        """Recommend best tool sequences for a skill."""
        relevant = [p for p in self._patterns.values() if p.skill == skill]
        relevant.sort(key=lambda p: (-p.success_rate, -p.usage_count))
        return [
            {
                "tools": p.tool_sequence,
                "success_rate": round(p.success_rate, 2),
                "usage_count": p.usage_count,
                "avg_tokens": int(p.avg_tokens),
            }
            for p in relevant[:top_k]
        ]

    def stats(self) -> dict:
        return {
            "total_patterns": len(self._patterns),
            "skills_covered": len({p.skill for p in self._patterns.values()}),
            "avg_success_rate": round(
                sum(p.success_rate for p in self._patterns.values())
                / max(len(self._patterns), 1),
                2,
            ),
        }


__all__ = ["ToolPattern", "ToolMemory"]
