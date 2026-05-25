"""Dream Phase 4 — REORGANIZE.

- Promote high-frequency successful episodes into semantic memories
- Promote convergent skill sequences into procedural workflows
- Detect statistical patterns and write them as observations
- Reorder user MEMORY.md index by retrieval frequency (non-destructive)
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from datetime import UTC

from dream.convergence import promote_convergent
from dream.pattern_detector import detect_convergence, detect_patterns
from memory import semantic
from memory.schemas import PhaseReport


def reorganize(state: dict, dry_run: bool = False) -> tuple[PhaseReport, dict]:
    t0 = time.monotonic()
    actions: list[str] = []
    episodes = state.get("episodes", [])

    patterns = detect_patterns(episodes)
    actions.append(f"Detected {len(patterns)} statistical patterns")
    state["patterns_detected"] = patterns

    convergent = detect_convergence(episodes)
    actions.append(f"Detected {len(convergent)} convergent skill sequences (>=3 sessions)")
    promoted_workflows = promote_convergent(episodes, convergent, dry_run=dry_run)
    actions.append(f"Promoted {len(promoted_workflows)} workflows to procedural memory")
    state["promoted_workflows"] = promoted_workflows

    promoted_semantic = 0
    if patterns and not dry_run:
        from datetime import datetime
        today = datetime.now(UTC).strftime("%Y-%m-%d")
        obs_content = "Observations from dream cycle " + today + ":\n\n" + "\n".join(f"- {p}" for p in patterns)
        mem = semantic.promote_from_episode(
            name=f"Dream observations {today}",
            content=obs_content,
            source_episode_ids=[ep.episode_id for ep in episodes[:20]],
            type_="observation",
            confidence=0.6,
        )
        promoted_semantic = 1
        actions.append(f"Wrote observation memory {mem.memory_id}")

    state["promoted_semantic_count"] = promoted_semantic

    report = PhaseReport(
        name="reorganize",
        duration_seconds=round(time.monotonic() - t0, 3),
        actions=actions,
        counts={
            "patterns_detected": len(patterns),
            "convergent_sequences": len(convergent),
            "promoted_workflows": len(promoted_workflows),
            "promoted_semantic": promoted_semantic,
        },
    )
    return report, state
