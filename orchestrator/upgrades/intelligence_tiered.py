"""Tiered Memory subsystem (extracted from `upgrades/intelligence.py` — Onda 4 #3).

`MemoryTier` enum + `MemoryEntry` dataclass + `TieredMemory` class. Stores
mem0-style multi-level memory (user/project/agent/session) backed by SQLite.
Recall scores combine keyword match + importance + recency + access frequency.

Parent `upgrades/intelligence.py` re-imports these names so existing callers
keep working.
"""

from __future__ import annotations

import json
import math
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
DB_PATH = ORCH_DIR / "orchestrator.db"


class MemoryTier(Enum):
    USER = "user"           # Persists across all projects
    PROJECT = "project"     # Persists within a project
    AGENT = "agent"         # Persists for a specific agent/skill
    SESSION = "session"     # Ephemeral, current session only


@dataclass
class MemoryEntry:
    """A single memory entry with metadata."""

    entry_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    tier: MemoryTier = MemoryTier.SESSION
    content: str = ""
    tags: list[str] = field(default_factory=list)
    scope: str = ""  # project_id, agent_id, or session_id
    importance: float = 0.5  # 0-1
    access_count: int = 0
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    last_accessed: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    expires_at: str | None = None


class TieredMemory:
    """Multi-level memory system inspired by mem0.

    Memories are stored by tier, scored by composite relevance:
    +26% accuracy over full-context, 90% fewer tokens.
    """

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or str(DB_PATH)
        self._ensure_table()

    def _ensure_table(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tiered_memory (
                entry_id TEXT PRIMARY KEY,
                tier TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT DEFAULT '[]',
                scope TEXT DEFAULT '',
                importance REAL DEFAULT 0.5,
                access_count INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                last_accessed TEXT NOT NULL,
                expires_at TEXT
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_mem_tier ON tiered_memory(tier)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_mem_scope ON tiered_memory(scope)"
        )
        conn.commit()
        conn.close()

    def store(
        self,
        content: str,
        tier: MemoryTier,
        scope: str = "",
        tags: list[str] | None = None,
        importance: float = 0.5,
    ) -> str:
        """Store a memory entry. Returns entry_id."""
        entry = MemoryEntry(
            tier=tier,
            content=content,
            scope=scope,
            tags=tags or [],
            importance=importance,
        )
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT OR REPLACE INTO tiered_memory VALUES (?,?,?,?,?,?,?,?,?,?)",
            (
                entry.entry_id,
                entry.tier.value,
                entry.content,
                json.dumps(entry.tags),
                entry.scope,
                entry.importance,
                entry.access_count,
                entry.created_at,
                entry.last_accessed,
                entry.expires_at,
            ),
        )
        conn.commit()
        conn.close()
        return entry.entry_id

    def recall(
        self,
        query: str,
        tier: MemoryTier | None = None,
        scope: str | None = None,
        limit: int = 10,
    ) -> list[dict]:
        """Recall memories matching query.

        Scored by:
            keyword_match * 0.4 + importance * 0.3 + recency * 0.2 + access_freq * 0.1
        """
        conn = sqlite3.connect(self.db_path)
        sql = "SELECT * FROM tiered_memory WHERE 1=1"
        params: list[str] = []
        if tier:
            sql += " AND tier = ?"
            params.append(tier.value)
        if scope:
            sql += " AND scope = ?"
            params.append(scope)

        rows = conn.execute(sql, params).fetchall()
        conn.close()

        query_words = set(query.lower().split())
        now = datetime.now(UTC)
        scored = []

        for row in rows:
            (
                entry_id,
                tier_v,
                content,
                tags_j,
                scope_v,
                importance,
                access_count,
                _created,
                accessed,
                expires,
            ) = row

            if expires and datetime.fromisoformat(expires) < now:
                continue

            content_words = set(content.lower().split())
            tags_set = set(json.loads(tags_j))
            all_words = content_words | tags_set
            keyword_score = len(query_words & all_words) / max(len(query_words), 1)

            try:
                age_days = (now - datetime.fromisoformat(accessed)).total_seconds() / 86400
            except Exception:
                age_days = 30
            recency_score = math.exp(-age_days / 30)

            freq_score = min(math.log(access_count + 1) / 5, 1.0)

            total = (
                keyword_score * 0.4
                + importance * 0.3
                + recency_score * 0.2
                + freq_score * 0.1
            )

            if total > 0.05:
                scored.append(
                    {
                        "entry_id": entry_id,
                        "tier": tier_v,
                        "content": content,
                        "tags": json.loads(tags_j),
                        "scope": scope_v,
                        "score": round(total, 3),
                        "importance": importance,
                    }
                )

        scored.sort(key=lambda x: -x["score"])

        if scored:
            conn = sqlite3.connect(self.db_path)
            now_str = now.isoformat()
            for s in scored[:limit]:
                conn.execute(
                    "UPDATE tiered_memory SET access_count = access_count + 1, last_accessed = ? WHERE entry_id = ?",
                    (now_str, s["entry_id"]),
                )
            conn.commit()
            conn.close()

        return scored[:limit]

    def stats(self) -> dict:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT tier, COUNT(*) FROM tiered_memory GROUP BY tier"
        ).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM tiered_memory").fetchone()[0]
        conn.close()
        return {"total": total, "by_tier": {r[0]: r[1] for r in rows}}


__all__ = ["MemoryTier", "MemoryEntry", "TieredMemory"]
