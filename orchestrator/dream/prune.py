"""Dream Phase 2 — PRUNE.

Remove stale, never-retrieved, and noisy memories. Conservative — only prunes
items that meet ALL of: never retrieved AND older than threshold AND not linked
to other memories.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from datetime import UTC, datetime

from memory import semantic
from memory.config import get as _cfg
from memory.decay import effective_confidence
from memory.schemas import PhaseReport
from memory.semantic import SEMANTIC_DIR

STALE_DAYS = 90
NEVER_RETRIEVED_MIN_AGE_DAYS = 14
DECAY_PRUNE_FLOOR = float(_cfg("decay_prune_floor"))


def _age_days(ts: str) -> float:
    try:
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return (datetime.now(UTC) - dt).total_seconds() / 86400.0
    except Exception:
        return 0.0


def prune(state: dict[str, Any], dry_run: bool = False) -> tuple[PhaseReport, dict[str, Any]]:
    t0 = time.monotonic()
    actions: list[str] = []

    stale = semantic.find_stale(days=STALE_DAYS)
    never = semantic.find_never_retrieved(min_age_days=NEVER_RETRIEVED_MIN_AGE_DAYS)
    pruned_ids: set[str] = set()
    archived = 0

    archive_dir = SEMANTIC_DIR / ".archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    for mem in stale:
        if mem.retrieval_count > 0:
            continue
        if mem.links:
            continue
        if not dry_run:
            src = SEMANTIC_DIR / f"{mem.memory_id}.yaml"
            if src.exists():
                src.rename(archive_dir / f"{mem.memory_id}.yaml")
                archived += 1
        pruned_ids.add(mem.memory_id)

    for mem in never:
        if mem.memory_id in pruned_ids:
            continue
        if mem.links:
            continue
        # Decayed confidence, not the static field — an old high-confidence
        # memory that was never used loses its protection over time
        # (DD finding A13, 2026-06-12).
        if effective_confidence(mem) >= 0.85:
            continue
        if not dry_run:
            src = SEMANTIC_DIR / f"{mem.memory_id}.yaml"
            if src.exists():
                src.rename(archive_dir / f"{mem.memory_id}.yaml")
                archived += 1
        pruned_ids.add(mem.memory_id)

    # Decay floor pass — any memory whose effective confidence fell below the
    # floor is archived, regardless of past retrievals (frequent retrieval
    # extends the half-life, so useful memories self-protect).
    decayed_below_floor = 0
    for mem in semantic.list_semantic():
        if mem.memory_id in pruned_ids:
            continue
        if mem.links:
            continue
        if _age_days(mem.created_at) < NEVER_RETRIEVED_MIN_AGE_DAYS:
            continue  # grace period for freshly written low-confidence memories
        if effective_confidence(mem) >= DECAY_PRUNE_FLOOR:
            continue
        decayed_below_floor += 1
        if not dry_run:
            src = SEMANTIC_DIR / f"{mem.memory_id}.yaml"
            if src.exists():
                src.rename(archive_dir / f"{mem.memory_id}.yaml")
                archived += 1
        pruned_ids.add(mem.memory_id)

    actions.append(f"Identified {len(stale)} stale memories (>{STALE_DAYS}d, 0 retrievals)")
    actions.append(f"Identified {len(never)} never-retrieved memories (>{NEVER_RETRIEVED_MIN_AGE_DAYS}d old)")
    actions.append(f"Identified {decayed_below_floor} memories with decayed confidence <{DECAY_PRUNE_FLOOR}")
    actions.append(f"Archived {archived} memories to .archive/ (dry_run={dry_run})")

    state["pruned_ids"] = list(pruned_ids)

    report = PhaseReport(
        name="prune",
        duration_seconds=round(time.monotonic() - t0, 3),
        actions=actions,
        counts={
            "stale_found": len(stale),
            "never_retrieved_found": len(never),
            "decayed_below_floor": decayed_below_floor,
            "archived": archived,
        },
    )
    return report, state
