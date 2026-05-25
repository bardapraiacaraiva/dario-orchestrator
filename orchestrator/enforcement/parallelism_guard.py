"""Parallelism guard (Risk #1 thin layer module 3/3).

Before this module, "max 3 parallel workers" was Claude's job to honor
from SKILL.md. Two Claude sessions running concurrent dispatches could
both believe they were under the limit, with no enforcement.

This module uses portalocker (cross-platform file locking) to maintain
a shared counter of active dispatches in
`~/.claude/orchestrator/runtime/active_dispatches.json`. claim_slot()
acquires lock, reads counter, raises if >= max, increments. release_slot()
re-acquires lock and decrements. Context manager handles both.

Design notes:
  - File lock not in-memory: must survive Python process boundaries.
  - Counter file is a single number, not a list of slot ids. Simpler
    semantics — we only care "how many active right now".
  - Stale-slot recovery: counter file has timestamps; slots older than
    DARIO_SLOT_TIMEOUT_S (default 3600 = 1h) are reaped on next claim.
    This handles crashes that didn't call release_slot().
  - Max parallel comes from license_manager.get_max_parallel() (tier-aware)
    or DARIO_MAX_PARALLEL env override.

Usage:
    from enforcement.parallelism_guard import slot

    with slot(caller="dario-pitch-polished"):
        dispatch_to_worker(task)
    # slot auto-released on exit (including exceptions)

    # OR manual:
    slot_id = claim_slot("my-script")
    try:
        do_work()
    finally:
        release_slot(slot_id)
"""

from __future__ import annotations

import contextlib
import json
import logging
import os
import time
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path

import portalocker

from enforcement import ParallelismExceededError

log = logging.getLogger("enforcement.parallelism_guard")

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
RUNTIME_DIR = ORCH_DIR / "runtime"
SLOTS_FILE = RUNTIME_DIR / "active_dispatches.json"
LOCK_FILE = RUNTIME_DIR / "active_dispatches.lock"

DEFAULT_MAX_PARALLEL = int(os.getenv("DARIO_MAX_PARALLEL", "3"))
SLOT_TIMEOUT_SECONDS = int(os.getenv("DARIO_SLOT_TIMEOUT_S", "3600"))


def _get_max_parallel() -> int:
    """Resolve max parallel from env > license tier > default."""
    env = os.getenv("DARIO_MAX_PARALLEL")
    if env:
        try:
            return int(env)
        except ValueError:
            pass
    try:
        import sys
        sys.path.insert(0, str(ORCH_DIR))
        from licensing.license_manager import get_max_parallel
        return int(get_max_parallel())
    except Exception:
        return DEFAULT_MAX_PARALLEL


def _ensure_files() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    if not SLOTS_FILE.exists():
        SLOTS_FILE.write_text("[]", encoding="utf-8")
    if not LOCK_FILE.exists():
        LOCK_FILE.touch()


def _load_slots(now: datetime) -> list[dict]:
    """Read current slots, reaping any that exceeded SLOT_TIMEOUT_SECONDS."""
    try:
        data = json.loads(SLOTS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        data = []
    if not isinstance(data, list):
        data = []
    cutoff = now - timedelta(seconds=SLOT_TIMEOUT_SECONDS)
    alive: list[dict] = []
    for s in data:
        try:
            ts = datetime.fromisoformat(s.get("claimed_at", ""))
            if ts > cutoff:
                alive.append(s)
            else:
                log.warning(
                    f"Reaping stale slot {s.get('id')!r} (caller {s.get('caller', '?')}, "
                    f"claimed at {s.get('claimed_at')})"
                )
        except (ValueError, TypeError):
            continue
    return alive


def _save_slots(slots: list[dict]) -> None:
    SLOTS_FILE.write_text(json.dumps(slots, indent=2), encoding="utf-8")


def claim_slot(caller: str = "anonymous", max_parallel: int | None = None) -> str:
    """Acquire a slot. Raises ParallelismExceededError if no slot available.

    Returns: opaque slot_id (pass to release_slot to free).
    """
    if not caller:
        raise ValueError("caller required (used for audit/debugging)")

    _ensure_files()
    max_p = max_parallel if max_parallel is not None else _get_max_parallel()
    slot_id = str(uuid.uuid4())
    now = datetime.now(UTC)

    with portalocker.Lock(str(LOCK_FILE), timeout=10) as _:
        slots = _load_slots(now)
        if len(slots) >= max_p:
            active_callers = [s.get("caller", "?") for s in slots]
            raise ParallelismExceededError(
                f"Max parallel dispatches reached ({len(slots)}/{max_p}). "
                f"Active callers: {active_callers}. "
                f"Wait or raise DARIO_MAX_PARALLEL / upgrade tier."
            )
        slots.append({
            "id": slot_id,
            "caller": caller,
            "claimed_at": now.isoformat(timespec="seconds"),
            "pid": os.getpid(),
        })
        _save_slots(slots)
    log.debug(f"Slot claimed: id={slot_id} caller={caller} active={len(slots)}/{max_p}")
    return slot_id


def release_slot(slot_id: str) -> bool:
    """Release a previously claimed slot. Returns True if slot existed, False if not."""
    _ensure_files()
    with portalocker.Lock(str(LOCK_FILE), timeout=10) as _:
        slots = _load_slots(datetime.now(UTC))
        before = len(slots)
        slots = [s for s in slots if s.get("id") != slot_id]
        released = len(slots) < before
        if released:
            _save_slots(slots)
        return released


def active_slots() -> list[dict]:
    """Read-only inspection — used by dashboard widget + tests."""
    _ensure_files()
    with portalocker.Lock(str(LOCK_FILE), timeout=10) as _:
        return _load_slots(datetime.now(UTC))


def active_count() -> int:
    return len(active_slots())


@contextlib.contextmanager
def slot(caller: str = "anonymous", max_parallel: int | None = None):
    """Context manager — auto-claim and auto-release a slot.

    Raises ParallelismExceededError if no slot available.

        with slot(caller="dario-pitch-polished"):
            dispatch_to_worker(task)
    """
    slot_id = claim_slot(caller=caller, max_parallel=max_parallel)
    try:
        yield slot_id
    finally:
        release_slot(slot_id)


def reset_for_test() -> None:
    """Hard reset for test isolation. NEVER call in production."""
    if SLOTS_FILE.exists():
        SLOTS_FILE.unlink()
    if LOCK_FILE.exists():
        try:
            LOCK_FILE.unlink()
        except (OSError, PermissionError):
            pass
