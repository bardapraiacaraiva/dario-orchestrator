"""Message Bus (extracted from `upgrades/core.py` — Onda 6 #2).

AutoGen-inspired in-process pub/sub. `MessageType` enum + `TypedMessage`
dataclass + `MessageBus` with subscribe/publish + history.

Parent `upgrades/core.py` re-imports these for backward-compat.
"""

from __future__ import annotations

import logging
import uuid
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum

log = logging.getLogger("upgrades.core_messagebus")


class MessageType(Enum):
    TASK_CREATED = "task_created"
    TASK_DISPATCHED = "task_dispatched"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    QUALITY_SCORED = "quality_scored"
    BUDGET_WARNING = "budget_warning"
    BUDGET_CRITICAL = "budget_critical"
    TAX_ALERT = "tax_alert"
    HEALTH_CHECK = "health_check"
    HANDOFF_REQUEST = "handoff_request"
    EVOLUTION_CYCLE = "evolution_cycle"
    GUARDRAIL_TRIPWIRE = "guardrail_tripwire"


@dataclass
class TypedMessage:
    """Typed message for the bus."""

    msg_type: MessageType
    source: str
    payload: dict = field(default_factory=dict)
    target: str | None = None  # None = broadcast
    msg_id: str = field(default_factory=lambda: uuid.uuid4().hex[:10])
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    correlation_id: str | None = None  # For request/response pairing


class MessageBus:
    """In-process typed message bus inspired by AutoGen 0.4's actor model.

    Engines subscribe to message types and receive only relevant messages.
    """

    def __init__(self):
        self._subscribers: dict[MessageType, list[Callable]] = {}
        self._history: list[dict] = []
        self._stats: dict[str, int] = {}

    def subscribe(self, msg_type: MessageType, handler: Callable):
        """Subscribe to a message type."""
        if msg_type not in self._subscribers:
            self._subscribers[msg_type] = []
        self._subscribers[msg_type].append(handler)

    def publish(self, message: TypedMessage):
        """Publish a message to all subscribers."""
        self._history.append(asdict(message))
        type_key = message.msg_type.value
        self._stats[type_key] = self._stats.get(type_key, 0) + 1

        handlers = self._subscribers.get(message.msg_type, [])
        for handler in handlers:
            try:
                if message.target and hasattr(handler, "__self__"):
                    engine_name = getattr(handler.__self__, "name", "")
                    if engine_name != message.target:
                        continue
                handler(message)
            except Exception as e:
                log.warning(f"Message handler error for {type_key}: {e}")

    def get_stats(self) -> dict:
        """Get message bus statistics."""
        return {
            "total_messages": sum(self._stats.values()),
            "by_type": dict(self._stats),
            "subscribers": {k.value: len(v) for k, v in self._subscribers.items()},
            "history_size": len(self._history),
        }

    def get_history(
        self, msg_type: MessageType | None = None, limit: int = 50
    ) -> list[dict]:
        """Get message history."""
        history = self._history
        if msg_type:
            history = [m for m in history if m.get("msg_type") == msg_type.value]
        return history[-limit:]


__all__ = ["MessageType", "TypedMessage", "MessageBus"]
