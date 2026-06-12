"""Retrieval tracking — which memories were read by which task.

Used by Dream to identify never-retrieved memories (candidates for pruning)
and high-value memories (candidates for promotion).
"""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path

from .schemas import MemoryLayer, RetrievalLogEntry

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
RETRIEVAL_DIR = ORCH_DIR / "memory" / "retrieval"
RETRIEVAL_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = RETRIEVAL_DIR / "retrieval_log.jsonl"
# Per-task staging of memories injected at context time, consumed at completion
# (DD finding A13, 2026-06-12 — retrieval_count was always 0 because nothing
# carried retrieved memory ids from context injection to the completion hooks).
PENDING_DIR = RETRIEVAL_DIR / "pending"


def log_retrieval(episode_id: str, memory_id: str, layer: str = "semantic", relevance: str = "medium") -> None:
    entry = RetrievalLogEntry(
        episode_id=episode_id,
        memory_id=memory_id,
        layer=MemoryLayer(layer),
        relevance=relevance,
    )
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry.model_dump(mode="json")) + "\n")


def _pending_path(task_id: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", task_id)[:80]
    return PENDING_DIR / f"{safe}.json"


def record_pending(task_id: str, memories: list[dict]) -> None:
    """Stage memories retrieved for a task; merged by memory_id (idempotent)."""
    if not task_id or not memories:
        return
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    path = _pending_path(task_id)
    existing: list[dict] = []
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                existing = []
        except Exception:
            existing = []
    seen = {m.get("memory_id") for m in existing if isinstance(m, dict)}
    for m in memories:
        mid = m.get("memory_id") if isinstance(m, dict) else None
        if not mid or mid in seen:
            continue
        existing.append({
            "memory_id": mid,
            "layer": m.get("layer", "semantic"),
            "relevance": m.get("relevance", "medium"),
        })
        seen.add(mid)
    path.write_text(json.dumps(existing, ensure_ascii=False), encoding="utf-8")


def pop_pending(task_id: str) -> list[dict]:
    """Consume (read + delete) staged retrievals for a task. Returns []."""
    if not task_id:
        return []
    path = _pending_path(task_id)
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        data = []
    try:
        path.unlink()
    except OSError:
        pass
    return data if isinstance(data, list) else []


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
