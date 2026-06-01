"""Cache memory — computational state reuse with TTL.

Stores deterministic skill outputs keyed by input hash. Lets the executor
skip re-computation when the same input arrives within TTL.
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml

from .schemas import CacheEntry

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
CACHE_DIR = ORCH_DIR / "memory" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_TTL_HOURS = 168  # 7 days


def _hash(skill: str, input_text: str) -> str:
    h = hashlib.sha256()
    h.update(skill.encode("utf-8"))
    h.update(b"::")
    h.update(input_text.encode("utf-8"))
    return h.hexdigest()[:16]


def put(skill: str, input_text: str, output: str, tokens_saved: int = 0, ttl_hours: int = DEFAULT_TTL_HOURS) -> CacheEntry:
    key_hash = _hash(skill, input_text)
    expires = (datetime.now(UTC) + timedelta(hours=ttl_hours)).isoformat()
    entry = CacheEntry(
        cache_id=f"CACHE-{key_hash}",
        key_hash=key_hash,
        skill=skill,
        input_summary=input_text[:200],
        output=output,
        expires_at=expires,
        tokens_saved=tokens_saved,
    )
    path = CACHE_DIR / f"{entry.cache_id}.yaml"
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(entry.model_dump(mode="json"), f, sort_keys=False, allow_unicode=True)
    return entry


def get(skill: str, input_text: str) -> CacheEntry | None:
    key_hash = _hash(skill, input_text)
    path = CACHE_DIR / f"CACHE-{key_hash}.yaml"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        entry: CacheEntry = CacheEntry.model_validate(yaml.safe_load(f))
    if entry.expires_at:
        try:
            if datetime.fromisoformat(entry.expires_at) < datetime.now(UTC):
                path.unlink(missing_ok=True)
                return None
        except Exception:
            pass
    entry.hit_count += 1
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(entry.model_dump(mode="json"), f, sort_keys=False, allow_unicode=True)
    return entry


def evict_expired() -> int:
    now = datetime.now(UTC)
    removed = 0
    for path in CACHE_DIR.glob("CACHE-*.yaml"):
        try:
            with open(path, encoding="utf-8") as f:
                entry = CacheEntry.model_validate(yaml.safe_load(f))
            if entry.expires_at and datetime.fromisoformat(entry.expires_at) < now:
                path.unlink(missing_ok=True)
                removed += 1
        except Exception:
            continue
    return removed


def stats() -> dict:
    items = list(CACHE_DIR.glob("CACHE-*.yaml"))
    total_hits = 0
    total_tokens_saved = 0
    for path in items:
        try:
            with open(path, encoding="utf-8") as f:
                entry = CacheEntry.model_validate(yaml.safe_load(f))
            total_hits += entry.hit_count
            total_tokens_saved += entry.tokens_saved * entry.hit_count
        except Exception:
            continue
    return {
        "entries": len(items),
        "total_hits": total_hits,
        "tokens_saved_estimate": total_tokens_saved,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(stats(), indent=2))
