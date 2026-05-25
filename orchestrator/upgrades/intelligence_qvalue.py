"""Q-Value Memory (extracted from `upgrades/intelligence.py` — Onda 3 #2).

This module holds the `Episode` dataclass and `QValueMemory` class that
together implement MemRL-style episodic memory with Q-value learning.

Why extracted
-------------
`upgrades/intelligence.py` was 1,052 LOC mixing 7 unrelated concerns
(tiered memory, Q-value, knowledge graph, learned router, tool memory,
benchmark evolution, metrics registry). The Q-value subsystem is the most
heavily-imported (`qvalue_memory_wire.py`, tests, dispatch fallback path),
so it is the highest-leverage extraction.

The parent module `upgrades/intelligence.py` re-imports these names so
existing callers (`from upgrades.intelligence import QValueMemory, Episode`)
keep working unchanged.

Future modules to extract (Onda 3 #2 follow-up):
- `intelligence_tiered.py` — TieredMemory + MemoryTier + MemoryEntry
- `intelligence_kg.py` — KnowledgeGraph + GraphEntity + GraphRelation
- `intelligence_router.py` — LearnedRouter + RoutingDecision
- `intelligence_tools.py` — ToolMemory + ToolPattern
- `intelligence_benchmark.py` — BenchmarkEvolution + Mutation
- `intelligence_metrics.py` — MetricsRegistry
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class Episode:
    """A past experience with outcome value."""

    episode_id: str = field(default_factory=lambda: uuid.uuid4().hex[:10])
    context: str = ""          # What was the situation
    strategy: str = ""         # What strategy was used
    skill: str = ""            # Which skill executed
    outcome_score: float = 0   # Quality score (0-100)
    tokens_used: int = 0
    q_value: float = 0.0       # Learned utility value
    visits: int = 1
    created_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )


class QValueMemory:
    """
    Episodic memory with Q-value learning. Inspired by MemRL.
    No fine-tuning — learns which strategies work by reinforcement.

    Two-Phase Retrieval:
    1. Semantic relevance filter (keyword match)
    2. Q-value selection (pick highest utility from relevant episodes)
    """

    def __init__(self, learning_rate: float = 0.1, discount: float = 0.95):
        self.lr = learning_rate
        self.discount = discount
        self._episodes: list[Episode] = []

    def record(
        self,
        context: str,
        strategy: str,
        skill: str,
        outcome_score: float,
        tokens_used: int = 0,
    ) -> Episode:
        """Record a new episode and update Q-values."""
        existing = self._find_similar(context, strategy)
        if existing:
            # Update Q-value with TD-learning
            reward = outcome_score / 100.0  # Normalize to 0-1
            existing.q_value += self.lr * (reward - existing.q_value)
            existing.visits += 1
            existing.outcome_score = (
                existing.outcome_score * (existing.visits - 1) + outcome_score
            ) / existing.visits
            return existing

        ep = Episode(
            context=context,
            strategy=strategy,
            skill=skill,
            outcome_score=outcome_score,
            tokens_used=tokens_used,
            q_value=outcome_score / 100.0,
        )
        self._episodes.append(ep)
        return ep

    def select_strategy(self, context: str, top_k: int = 3) -> list[dict]:
        """Two-phase retrieval:
        1. Find relevant episodes by context similarity
        2. Rank by Q-value (highest utility first)
        """
        context_words = set(context.lower().split())
        relevant = []
        for ep in self._episodes:
            ep_words = set(ep.context.lower().split())
            overlap = len(context_words & ep_words)
            if overlap > 0:
                relevance = overlap / max(len(context_words), 1)
                relevant.append((relevance, ep))

        relevant.sort(key=lambda x: (-x[1].q_value, -x[0]))

        return [
            {
                "strategy": ep.strategy,
                "skill": ep.skill,
                "q_value": round(ep.q_value, 3),
                "avg_score": round(ep.outcome_score, 1),
                "visits": ep.visits,
                "relevance": round(rel, 3),
            }
            for rel, ep in relevant[:top_k]
        ]

    def _find_similar(self, context: str, strategy: str) -> Episode | None:
        """Find an existing episode with similar context and same strategy."""
        ctx_words = set(context.lower().split())
        for ep in self._episodes:
            if ep.strategy == strategy:
                ep_words = set(ep.context.lower().split())
                if len(ctx_words & ep_words) / max(len(ctx_words), 1) > 0.5:
                    return ep
        return None

    def get_top_strategies(self, n: int = 10) -> list[dict]:
        """Get top strategies by Q-value."""
        sorted_eps = sorted(self._episodes, key=lambda e: -e.q_value)
        return [
            {
                "strategy": e.strategy,
                "skill": e.skill,
                "q_value": round(e.q_value, 3),
                "visits": e.visits,
            }
            for e in sorted_eps[:n]
        ]

    def stats(self) -> dict:
        return {
            "total_episodes": len(self._episodes),
            "avg_q_value": round(
                sum(e.q_value for e in self._episodes)
                / max(len(self._episodes), 1),
                3,
            ),
            "top_skill": max(self._episodes, key=lambda e: e.q_value).skill
            if self._episodes
            else None,
        }


__all__ = ["Episode", "QValueMemory"]
