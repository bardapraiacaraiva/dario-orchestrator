"""Handoff protocol (extracted from `upgrades/core.py` — Onda 6 #2).

Typed handoff contracts between engines. `HandoffContext` carries the goal +
input artifacts; `HandoffResult` carries the outcome + token usage. The
`HandoffProtocol` registry validates which source→target routes are allowed.

Parent `upgrades/core.py` re-imports these for backward-compat.
"""

from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class HandoffStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class HandoffContext:
    """Typed context passed at each engine handoff."""

    task_id: str
    source_engine: str
    target_engine: str
    goal: str
    constraints: list[str] = field(default_factory=list)
    input_artifacts: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    parent_handoff_id: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    handoff_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])


@dataclass
class HandoffResult:
    """Typed result returned after engine completes."""

    handoff_id: str
    status: HandoffStatus
    output_artifacts: dict[str, Any] = field(default_factory=dict)
    token_usage: dict[str, int] = field(default_factory=dict)
    quality_score: float | None = None
    error: str | None = None
    duration_ms: int = 0
    completed_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class HandoffProtocol:
    """Registry and validator for engine handoffs."""

    def __init__(self):
        self._history: list[dict] = []
        self._allowed_routes: dict[str, list[str]] = {}

    def register_route(self, source: str, targets: list[str]):
        """Register allowed handoff routes between engines."""
        self._allowed_routes[source] = targets

    def create_handoff(
        self,
        task_id: str,
        source: str,
        target: str,
        goal: str,
        **kwargs: Any,
    ) -> HandoffContext:
        """Create a validated handoff context."""
        allowed = self._allowed_routes.get(source, [])
        if allowed and target not in allowed:
            raise ValueError(
                f"Handoff from '{source}' to '{target}' not allowed. "
                f"Allowed targets: {allowed}"
            )
        ctx = HandoffContext(
            task_id=task_id,
            source_engine=source,
            target_engine=target,
            goal=goal,
            **kwargs,
        )
        self._history.append(asdict(ctx))
        return ctx

    def complete_handoff(
        self,
        handoff_id: str,
        status: HandoffStatus,
        **kwargs: Any,
    ) -> HandoffResult:
        """Record handoff completion."""
        result = HandoffResult(handoff_id=handoff_id, status=status, **kwargs)
        self._history.append({"result": asdict(result)})
        return result

    def get_history(self, task_id: str | None = None) -> list[dict]:
        """Get handoff history, optionally filtered by task."""
        if task_id:
            return [h for h in self._history if h.get("task_id") == task_id]
        return self._history


__all__ = [
    "HandoffStatus",
    "HandoffContext",
    "HandoffResult",
    "HandoffProtocol",
]
