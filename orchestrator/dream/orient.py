"""Dream Phase 1 — ORIENT.

Load the current state: episodes window, existing memories, retrieval stats.
Produces a snapshot the other phases work against.
"""

from __future__ import annotations

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import time

from memory import episodic, procedural, retrieval, semantic
from memory.schemas import PhaseReport


def orient(window_days: int = 7) -> tuple[PhaseReport, dict]:
    """Load state. Returns (report, state_dict)."""
    t0 = time.monotonic()
    episodes = list(episodic.iter_episodes(window_days))
    semantic_items = semantic.list_semantic()
    workflows = procedural.list_workflows()
    retrieval_freq = retrieval.frequency_by_memory(window_days)
    retrieval_layer = retrieval.frequency_by_layer(window_days)
    user_memory = semantic.parse_user_memory_index()

    state = {
        "episodes": episodes,
        "semantic": semantic_items,
        "procedural": workflows,
        "retrieval_freq": retrieval_freq,
        "retrieval_layer": retrieval_layer,
        "user_memory_entries": user_memory,
    }

    report = PhaseReport(
        name="orient",
        duration_seconds=round(time.monotonic() - t0, 3),
        actions=[
            f"Loaded {len(episodes)} episodes (window={window_days}d)",
            f"Loaded {len(semantic_items)} structured semantic memories",
            f"Loaded {len(workflows)} procedural workflows",
            f"Loaded {len(user_memory)} entries from user MEMORY.md index",
            f"Retrieval log: {sum(retrieval_freq.values())} hits across {len(retrieval_freq)} unique memories",
        ],
        counts={
            "episodes": len(episodes),
            "semantic": len(semantic_items),
            "procedural": len(workflows),
            "user_memory": len(user_memory),
            "retrieval_hits": sum(retrieval_freq.values()),
        },
    )
    return report, state
