"""SQLite storage for the DARIO license server (Onda 8)."""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path

DEFAULT_DB_PATH = (
    Path(os.getenv("LICENSE_SERVER_DB", str(Path.home() / ".dario-license-server.db")))
)


SCHEMA = """
CREATE TABLE IF NOT EXISTS trials (
    machine_id      TEXT PRIMARY KEY,
    first_init_at   TEXT NOT NULL,    -- ISO-8601 UTC, immutable
    expires_at      TEXT NOT NULL,    -- ISO-8601 UTC, immutable
    last_seen_at    TEXT NOT NULL,    -- updated on every /validate
    token           TEXT NOT NULL,    -- HMAC-signed opaque blob
    tier            TEXT NOT NULL DEFAULT 'trial',  -- trial | pro | enterprise
    status          TEXT NOT NULL DEFAULT 'active', -- active | expired | revoked
    heartbeat_count INTEGER NOT NULL DEFAULT 1,
    vip_key         TEXT,             -- set after /vip/activate
    notes           TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS audit_log (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id    TEXT NOT NULL,
    event         TEXT NOT NULL,      -- activate | validate | tampered | rollback | upgrade
    payload       TEXT DEFAULT '{}',  -- JSON
    server_ts     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_machine ON audit_log(machine_id, server_ts DESC);
"""


@contextmanager
def db_connect(db_path: Path = DEFAULT_DB_PATH):
    """Context manager that yields a connected sqlite3.Connection.

    Ensures schema exists; commits on clean exit, rolls back on exception,
    always closes the connection.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), isolation_level=None)
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(SCHEMA)
        yield conn
    except Exception:
        try:
            conn.rollback()
        except Exception:
            pass
        raise
    finally:
        conn.close()


def now_utc() -> str:
    return datetime.now(UTC).isoformat()


def get_trial(conn: sqlite3.Connection, machine_id: str) -> dict | None:
    row = conn.execute(
        "SELECT * FROM trials WHERE machine_id = ?", (machine_id,)
    ).fetchone()
    return dict(row) if row else None


def insert_trial(
    conn: sqlite3.Connection,
    machine_id: str,
    first_init_at: str,
    expires_at: str,
    token: str,
) -> dict:
    last_seen = first_init_at
    conn.execute(
        """INSERT INTO trials
            (machine_id, first_init_at, expires_at, last_seen_at, token,
             tier, status, heartbeat_count)
           VALUES (?, ?, ?, ?, ?, 'trial', 'active', 1)""",
        (machine_id, first_init_at, expires_at, last_seen, token),
    )
    return dict(
        machine_id=machine_id,
        first_init_at=first_init_at,
        expires_at=expires_at,
        last_seen_at=last_seen,
        token=token,
        tier="trial",
        status="active",
        heartbeat_count=1,
    )


def update_heartbeat(conn: sqlite3.Connection, machine_id: str) -> None:
    conn.execute(
        "UPDATE trials SET last_seen_at = ?, heartbeat_count = heartbeat_count + 1 "
        "WHERE machine_id = ?",
        (now_utc(), machine_id),
    )


def mark_status(conn: sqlite3.Connection, machine_id: str, status: str) -> None:
    conn.execute(
        "UPDATE trials SET status = ? WHERE machine_id = ?",
        (status, machine_id),
    )


def upgrade_to_vip(
    conn: sqlite3.Connection, machine_id: str, tier: str, vip_key: str
) -> None:
    conn.execute(
        "UPDATE trials SET tier = ?, status = 'active', vip_key = ?, "
        "expires_at = '' WHERE machine_id = ?",
        (tier, vip_key, machine_id),
    )


def log_event(
    conn: sqlite3.Connection,
    machine_id: str,
    event: str,
    payload: str = "{}",
) -> None:
    conn.execute(
        "INSERT INTO audit_log (machine_id, event, payload, server_ts) "
        "VALUES (?, ?, ?, ?)",
        (machine_id, event, payload, now_utc()),
    )


__all__ = [
    "DEFAULT_DB_PATH",
    "db_connect",
    "get_trial",
    "insert_trial",
    "update_heartbeat",
    "mark_status",
    "upgrade_to_vip",
    "log_event",
    "now_utc",
]
