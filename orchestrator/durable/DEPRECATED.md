# `durable/` — DEPRECATED (2026-06-01)

**Decision:** Temporal-based durable execution is deprecated. Audit P0-3.

## Why

- The pilot **never left stub mode**: `activities.py` returns `status="queued"`
  unless `DARIO_TEMPORAL_LIVE=1`, and `execution/checkpoint_interrupt.py` was
  never implemented (empty). It was a "stub-as-feature".
- It requires a **Temporal Server** (`localhost:7233`) — heavyweight infra for a
  tool whose real execution model is **single-session and Claude-Code-native**
  (the Python executor prepares + atomically checks out a task; the Claude Agent
  in the autopilot/skill does the actual LLM work).
- Distributed workflow orchestration is **overkill** for that model, and the
  SaaS / multi-tenant direction that would justify it is KILLED.
- Nothing in the production path imports `durable/` (only `tests/test_durable_pilot.py`).

## What provides durability instead (the real, lighter mechanism)

| Concern | Mechanism | Where |
|---|---|---|
| Atomic state writes | SQLite **WAL** journal mode | `core/db.py` |
| No double-execution | Atomic DB checkout (`checkout_task`) | `core/db.py` / `execution/executor.py` |
| Auditability / replay | Append-only audit log | `core/db.py` (`log_event`) |
| Crash mid-pulse | Stale-task recovery (in_progress > SLA → re-queue) | heartbeat / dispatch |
| Task state | Per-task YAML + DB single source of truth | `tasks/` + `core/db.py` |

## Status

- Code **kept, not deleted** — preserved for reference and for a possible future
  multi-machine / long-running autonomous-workflow scenario.
- **Do NOT** wire into production without a deliberate decision to stand up
  Temporal Server and implement real checkpoint/resume.
- `integration_registry.yaml`: `temporal` and `durable-swarm` entries marked
  `deprecated`.
