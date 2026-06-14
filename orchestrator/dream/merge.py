"""Dream Phase 3 — MERGE.

Cluster duplicate / near-duplicate semantic memories and merge them.
Cluster correction events from episodes by skill + error pattern.
"""

from __future__ import annotations

import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from memory import semantic
from memory.schemas import PhaseReport, SemanticMemory


def _normalize(text: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9]{4,}", text.lower())
    stop = {"para", "como", "este", "esta", "uma", "the", "and", "from", "with", "memory"}
    return {t for t in tokens if t not in stop}


def _similarity(a: str, b: str) -> float:
    ta, tb = _normalize(a), _normalize(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def merge(state: dict[str, Any], dry_run: bool = False, threshold: float = 0.55) -> tuple[PhaseReport, dict[str, Any]]:
    t0 = time.monotonic()
    actions: list[str] = []

    pruned = set(state.get("pruned_ids", []))
    items: list[SemanticMemory] = [m for m in state.get("semantic", []) if m.memory_id not in pruned]

    duplicates: list[tuple[str, str, float]] = []
    merged_count = 0
    used = set()

    for i, a in enumerate(items):
        if a.memory_id in used:
            continue
        for b in items[i + 1:]:
            if b.memory_id in used:
                continue
            if a.type != b.type:
                continue
            sim = _similarity(a.name + " " + a.description + " " + a.content[:300],
                              b.name + " " + b.description + " " + b.content[:300])
            if sim >= threshold:
                duplicates.append((a.memory_id, b.memory_id, round(sim, 2)))
                if not dry_run:
                    merged_content = a.content + "\n\n---\n[merged from " + b.memory_id + "]\n" + b.content
                    a.content = merged_content[:4096]
                    a.retrieval_count = max(a.retrieval_count, b.retrieval_count) + b.retrieval_count
                    a.links = list(set(a.links + b.links))
                    a.promoted_from_episodes = list(set(a.promoted_from_episodes + b.promoted_from_episodes))
                    semantic.write_semantic(a)
                    archive_dir = semantic.SEMANTIC_DIR / ".archive"
                    archive_dir.mkdir(parents=True, exist_ok=True)
                    src = semantic.SEMANTIC_DIR / f"{b.memory_id}.yaml"
                    if src.exists():
                        dest = archive_dir / f"{b.memory_id}.yaml"
                        if dest.exists():
                            dest.unlink()
                        src.rename(dest)
                    merged_count += 1
                used.add(b.memory_id)

    correction_clusters: dict[str, list[str]] = defaultdict(list)
    for ep in state.get("episodes", []):
        for corr in ep.corrections:
            key = f"{ep.skill}::{corr.severity}"
            correction_clusters[key].append(ep.episode_id)
    significant_clusters = {k: v for k, v in correction_clusters.items() if len(v) >= 2}

    actions.append(f"Compared {len(items)} semantic memories pairwise (threshold={threshold})")
    actions.append(f"Found {len(duplicates)} duplicate pairs, merged {merged_count}")
    actions.append(f"Detected {len(significant_clusters)} correction clusters (>=2 occurrences)")

    state["correction_clusters"] = significant_clusters
    state["merged_pairs"] = duplicates

    report = PhaseReport(
        name="merge",
        duration_seconds=round(time.monotonic() - t0, 3),
        actions=actions,
        counts={
            "duplicate_pairs": len(duplicates),
            "merged": merged_count,
            "correction_clusters": len(significant_clusters),
        },
    )
    return report, state
