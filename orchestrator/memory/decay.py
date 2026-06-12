"""Confidence decay for semantic memories (DD finding A13, 2026-06-12).

Memories used to live forever with a static confidence. This module computes
an *effective* (time-decayed) confidence:

    effective = confidence * 0.5 ** (age_days / half_life)

- age counts from the LAST retrieval (falling back to updated_at, then
  created_at) — so using a memory freezes its decay clock;
- half_life grows with retrieval_count — frequently used memories decay
  slower even between retrievals;
- missing/unparseable timestamps return the static confidence unchanged
  (legacy behaviour, backward compatible).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from .config import get as _cfg


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt


def half_life_days(retrieval_count: int) -> float:
    """Half-life in days, extended by usage (capped)."""
    base = float(_cfg("decay_half_life_days"))
    bonus = float(_cfg("decay_retrieval_bonus"))
    cap = int(_cfg("decay_retrieval_bonus_cap"))
    rc = max(0, min(int(retrieval_count or 0), cap))
    return base * (1.0 + bonus * rc)


def effective_confidence(mem: Any, now: datetime | None = None) -> float:
    """Time-decayed confidence for a SemanticMemory (or duck-typed object)."""
    base = float(getattr(mem, "confidence", 0.7) or 0.7)
    ref = (
        _parse_ts(getattr(mem, "last_retrieved", None))
        or _parse_ts(getattr(mem, "updated_at", None))
        or _parse_ts(getattr(mem, "created_at", None))
    )
    if ref is None:
        return base  # legacy memory without timestamps → old static behaviour
    now = now or datetime.now(UTC)
    age_days = max(0.0, (now - ref).total_seconds() / 86400.0)
    if age_days == 0.0:
        return base
    hl = half_life_days(getattr(mem, "retrieval_count", 0))
    return base * 0.5 ** (age_days / hl)
