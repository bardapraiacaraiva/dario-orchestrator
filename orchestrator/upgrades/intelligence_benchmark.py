"""Benchmark Evolution subsystem (extracted from `upgrades/intelligence.py` — Onda 6 #1).

`Mutation` dataclass + `BenchmarkEvolution` class. EvoAgentX-inspired
benchmark-driven workflow mutation: propose → evaluate → accept/reject.

Parent `upgrades/intelligence.py` re-imports these for backward-compat.
"""

from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class Mutation:
    """A proposed workflow mutation."""

    mutation_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    mutation_type: str = ""  # add_step, remove_step, reorder, swap_skill, adjust_param
    target: str = ""
    before: Any = None
    after: Any = None
    benchmark_score_before: float = 0.0
    benchmark_score_after: float = 0.0
    accepted: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class BenchmarkEvolution:
    """Benchmark-driven evolution. Inspired by EvoAgentX.

    1. Propose mutation (e.g., swap skill, reorder steps)
    2. Run against benchmark (eval_suite golden tests)
    3. Accept if score improves, reject otherwise
    """

    def __init__(self, improvement_threshold: float = 2.0):
        self.threshold = improvement_threshold
        self._mutations: list[Mutation] = []
        self._generation: int = 0

    def propose_mutation(
        self,
        mutation_type: str,
        target: str,
        before: Any,
        after: Any,
    ) -> Mutation:
        """Propose a mutation for testing."""
        return Mutation(
            mutation_type=mutation_type,
            target=target,
            before=before,
            after=after,
        )

    def evaluate(
        self,
        mutation: Mutation,
        score_before: float,
        score_after: float,
    ) -> bool:
        """Evaluate if mutation should be accepted."""
        mutation.benchmark_score_before = score_before
        mutation.benchmark_score_after = score_after
        improvement = score_after - score_before

        if improvement >= self.threshold:
            mutation.accepted = True
            self._generation += 1
        else:
            mutation.accepted = False

        self._mutations.append(mutation)
        return mutation.accepted

    def get_history(self, accepted_only: bool = False) -> list[dict]:
        """Get mutation history."""
        mutations = self._mutations
        if accepted_only:
            mutations = [m for m in mutations if m.accepted]
        return [asdict(m) for m in mutations]

    def stats(self) -> dict:
        accepted = sum(1 for m in self._mutations if m.accepted)
        return {
            "generation": self._generation,
            "total_mutations": len(self._mutations),
            "accepted": accepted,
            "rejected": len(self._mutations) - accepted,
            "acceptance_rate": round(accepted / max(len(self._mutations), 1) * 100, 1),
        }


__all__ = ["Mutation", "BenchmarkEvolution"]
