"""Versioned CheckpointStore (extracted from `upgrades/core.py` — Onda 7 #1).

LangGraph-inspired checkpoint store backed by SQLite. Two tables:
    - `checkpoints` (thread_id, checkpoint_id, version, state_blob, ...)
    - `checkpoint_writes` (per-channel write log)

Note: production chain checkpointing in v12.1 uses `chain_graph.SqliteSaver`
(LangGraph's official checkpointer). This CheckpointStore remains the
substrate for legacy engines that still call `save/load/list_versions`
directly.
"""

from __future__ import annotations

import json
import os
import sqlite3
import uuid
from datetime import UTC, datetime
from pathlib import Path

ORCH_DIR = Path(os.path.expanduser("~/.claude/orchestrator"))
DB_PATH = ORCH_DIR / "orchestrator.db"


class CheckpointStore:
    """Versioned checkpoint store inspired by LangGraph's checkpointer.

    Uses SQLite with blobs + writes tables for proper versioning. Each
    checkpoint is immutable — new versions are appended.
    """

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or str(DB_PATH)
        self._ensure_tables()

    def _ensure_tables(self):
        """Create checkpoint tables if not exist."""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS checkpoints (
                thread_id TEXT NOT NULL,
                checkpoint_id TEXT NOT NULL,
                parent_id TEXT,
                version INTEGER NOT NULL DEFAULT 1,
                state_blob TEXT NOT NULL,
                metadata TEXT DEFAULT '{}',
                created_at TEXT NOT NULL,
                PRIMARY KEY (thread_id, checkpoint_id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS checkpoint_writes (
                thread_id TEXT NOT NULL,
                checkpoint_id TEXT NOT NULL,
                channel TEXT NOT NULL,
                value TEXT NOT NULL,
                task_id TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_cp_thread ON checkpoints(thread_id, version DESC)"
        )
        conn.commit()
        conn.close()

    def save(
        self,
        thread_id: str,
        state: dict,
        metadata: dict | None = None,
        parent_id: str | None = None,
        task_id: str | None = None,
    ) -> str:
        """Save a checkpoint. Returns checkpoint_id."""
        checkpoint_id = f"cp_{uuid.uuid4().hex[:10]}"
        now = datetime.now(UTC).isoformat()
        conn = sqlite3.connect(self.db_path)

        row = conn.execute(
            "SELECT MAX(version) FROM checkpoints WHERE thread_id = ?",
            (thread_id,),
        ).fetchone()
        version = (row[0] or 0) + 1

        conn.execute(
            "INSERT INTO checkpoints (thread_id, checkpoint_id, parent_id, version, state_blob, metadata, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                thread_id,
                checkpoint_id,
                parent_id,
                version,
                json.dumps(state, default=str),
                json.dumps(metadata or {}),
                now,
            ),
        )

        for channel, value in state.items():
            conn.execute(
                "INSERT INTO checkpoint_writes (thread_id, checkpoint_id, channel, value, task_id, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    thread_id,
                    checkpoint_id,
                    channel,
                    json.dumps(value, default=str),
                    task_id,
                    now,
                ),
            )

        conn.commit()
        conn.close()
        return checkpoint_id

    def load(
        self,
        thread_id: str,
        checkpoint_id: str | None = None,
    ) -> dict | None:
        """Load a checkpoint. If no checkpoint_id, loads latest."""
        conn = sqlite3.connect(self.db_path)
        if checkpoint_id:
            row = conn.execute(
                "SELECT state_blob, metadata, version, created_at FROM checkpoints WHERE thread_id = ? AND checkpoint_id = ?",
                (thread_id, checkpoint_id),
            ).fetchone()
        else:
            row = conn.execute(
                "SELECT state_blob, metadata, version, created_at FROM checkpoints WHERE thread_id = ? ORDER BY version DESC LIMIT 1",
                (thread_id,),
            ).fetchone()
        conn.close()
        if not row:
            return None
        return {
            "state": json.loads(row[0]),
            "metadata": json.loads(row[1]),
            "version": row[2],
            "created_at": row[3],
        }

    def list_versions(self, thread_id: str) -> list[dict]:
        """List all checkpoint versions for a thread."""
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT checkpoint_id, version, parent_id, created_at FROM checkpoints WHERE thread_id = ? ORDER BY version DESC",
            (thread_id,),
        ).fetchall()
        conn.close()
        return [
            {
                "checkpoint_id": r[0],
                "version": r[1],
                "parent_id": r[2],
                "created_at": r[3],
            }
            for r in rows
        ]

    def get_writes(self, thread_id: str, checkpoint_id: str) -> dict:
        """Get all channel writes for a specific checkpoint."""
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT channel, value FROM checkpoint_writes WHERE thread_id = ? AND checkpoint_id = ?",
            (thread_id, checkpoint_id),
        ).fetchall()
        conn.close()
        return {r[0]: json.loads(r[1]) for r in rows}


__all__ = ["CheckpointStore"]
