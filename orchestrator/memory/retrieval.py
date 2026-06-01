"""Retrieval tracking — which memories were read by which task.

Used by Dream to identify never-retrieved memories (candidates for pruning)
and high-value memories (candidates for promotion).
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path

from .schemas import MemoryLayer, RetrievalLogEntry

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
RETRIEVAL_DIR = ORCH_DIR / "memory" / "retrieval"
RETRIEVAL_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = RETRIEVAL_DIR / "retrieval_log.jsonl"


def log_retrieval(episode_id: str, memory_id: str, layer: str = "semantic", relevance: str = "medium") -> None:
    entry = RetrievalLogEntry(
        episode_id=episode_id,
        memory_id=memory_id,
        layer=MemoryLayer(layer),
        relevance=relevance,
    )
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry.model_dump(mode="json")) + "\n")


def iter_log(window_days: int = 30):
    if not LOG_FILE.exists():
        return
    cutoff = (datetime.now(UTC) - timedelta(days=window_days)).isoformat()
    with open(LOG_FILE, encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("timestamp", "") >= cutoff:
                    yield entry
            except json.JSONDecodeError:
                continue


def frequency_by_memory(window_days: int = 30) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for entry in iter_log(window_days):
        counter[entry["memory_id"]] += 1
    return dict(counter)


def frequency_by_layer(window_days: int = 30) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for entry in iter_log(window_days):
        counter[entry.get("layer", "unknown")] += 1
    return dict(counter)


def episodes_using(memory_id: str, window_days: int = 30) -> list[str]:
    eps = []
    for entry in iter_log(window_days):
        if entry["memory_id"] == memory_id:
            eps.append(entry["episode_id"])
    return eps


def top_memories(window_days: int = 30, n: int = 10) -> list[tuple[str, int]]:
    counter = Counter(frequency_by_memory(window_days))
    return counter.most_common(n)


def never_retrieved(memory_ids: list[str], window_days: int = 30) -> list[str]:
    retrieved = set(frequency_by_memory(window_days).keys())
    return [m for m in memory_ids if m not in retrieved]


def stats(window_days: int = 30) -> dict:
    by_mem = frequency_by_memory(window_days)
    by_layer = frequency_by_layer(window_days)
    total = sum(by_mem.values())
    return {
        "window_days": window_days,
        "total_retrievals": total,
        "unique_memories_retrieved": len(by_mem),
        "by_layer": by_layer,
        "top_5": Counter(by_mem).most_common(5),
    }


def compact_log(keep_days: int = 90) -> int:
    """Compact the log file by removing entries older than keep_days."""
    if not LOG_FILE.exists():
        return 0
    cutoff = (datetime.now(UTC) - timedelta(days=keep_days)).isoformat()
    kept = []
    dropped = 0
    with open(LOG_FILE, encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("timestamp", "") >= cutoff:
                    kept.append(line)
                else:
                    dropped += 1
            except json.JSONDecodeError:
                dropped += 1
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.writelines(kept)
    return dropped


if __name__ == "__main__":
    print(json.dumps(stats(), indent=2, default=str))
