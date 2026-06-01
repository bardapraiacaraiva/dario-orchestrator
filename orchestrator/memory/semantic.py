"""Semantic memory — consolidated facts and patterns.

Wraps the existing MEMORY.md system (~/.claude/projects/.../memory/) AND adds
a structured layer at orchestrator/memory/semantic/ for dream-curated entries
that can be promoted to MEMORY.md after validation.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

import yaml

from .schemas import SemanticMemory, utcnow

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
SEMANTIC_DIR = ORCH_DIR / "memory" / "semantic"
SEMANTIC_DIR.mkdir(parents=True, exist_ok=True)

USER_MEMORY_DIR = Path.home() / ".claude" / "projects" / "C--Users-barda" / "memory"
USER_MEMORY_INDEX = USER_MEMORY_DIR / "MEMORY.md"


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return s[:60] or "memory"


def write_semantic(mem: SemanticMemory) -> Path:
    if not mem.memory_id:
        mem.memory_id = f"SEM-{_slug(mem.name)}"
    mem.updated_at = utcnow()
    path = SEMANTIC_DIR / f"{mem.memory_id}.yaml"
    data = mem.model_dump(mode="json", exclude_none=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
    return path


def read_semantic(memory_id: str) -> SemanticMemory | None:
    path = SEMANTIC_DIR / f"{memory_id}.yaml"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        loaded: SemanticMemory = SemanticMemory.model_validate(yaml.safe_load(f))
        return loaded


def list_semantic() -> list[SemanticMemory]:
    out = []
    for path in sorted(SEMANTIC_DIR.glob("SEM-*.yaml")):
        try:
            with open(path, encoding="utf-8") as f:
                out.append(SemanticMemory.model_validate(yaml.safe_load(f)))
        except Exception:
            continue
    return out


def increment_retrieval(memory_id: str) -> None:
    mem = read_semantic(memory_id)
    if not mem:
        return
    mem.retrieval_count += 1
    mem.last_retrieved = utcnow()
    write_semantic(mem)


def find_stale(days: int = 90) -> list[SemanticMemory]:
    cutoff = datetime.now(UTC).timestamp() - (days * 86400)
    stale = []
    for mem in list_semantic():
        try:
            ts = datetime.fromisoformat(mem.updated_at).timestamp()
        except Exception:
            continue
        if ts < cutoff and mem.retrieval_count == 0:
            stale.append(mem)
    return stale


def find_never_retrieved(min_age_days: int = 14) -> list[SemanticMemory]:
    cutoff = datetime.now(UTC).timestamp() - (min_age_days * 86400)
    out = []
    for mem in list_semantic():
        if mem.retrieval_count > 0:
            continue
        try:
            ts = datetime.fromisoformat(mem.created_at).timestamp()
        except Exception:
            continue
        if ts < cutoff:
            out.append(mem)
    return out


def promote_from_episode(
    name: str,
    content: str,
    source_episode_ids: list[str],
    type_: str = "pattern",
    confidence: float = 0.7,
) -> SemanticMemory:
    mem = SemanticMemory(
        memory_id="",
        name=name,
        description=f"Promoted from {len(source_episode_ids)} episode(s)",
        type=type_,
        content=content,
        promoted_from_episodes=source_episode_ids,
        confidence=confidence,
    )
    write_semantic(mem)
    return mem


def parse_user_memory_index() -> list[dict]:
    if not USER_MEMORY_INDEX.exists():
        return []
    entries = []
    text = USER_MEMORY_INDEX.read_text(encoding="utf-8")
    for line in text.splitlines():
        m = re.match(r"-\s*\[([^\]]+)\]\(([^\)]+)\)\s*(?:[—-]\s*(.*))?", line)
        if m:
            entries.append({
                "title": m.group(1),
                "file": m.group(2),
                "hook": (m.group(3) or "").strip(),
            })
    return entries


def stats() -> dict:
    items = list_semantic()
    by_type: dict[str, int] = {}
    total_retrievals = 0
    for m in items:
        by_type[m.type] = by_type.get(m.type, 0) + 1
        total_retrievals += m.retrieval_count
    user_idx = parse_user_memory_index()
    return {
        "structured_count": len(items),
        "by_type": by_type,
        "total_retrievals": total_retrievals,
        "user_memory_entries": len(user_idx),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(stats(), indent=2))
