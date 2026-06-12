"""SLA rules — single source of truth (audit 2026-06-12 Onda 4).

Before this module, SLA enforcement was markdown in lucas-heartbeat/SKILL.md
plus a fixed 60-minute zombie reaper in the runtime that ignored execution
policy entirely (a `default` task has 8h of SLA but was being blocked at 1h).

Protocol (mirrors the heartbeat doctrine):
  age <  SLA        → ok
  age >= SLA        → breach: critical/financial policies BLOCK; others warn
  age >= 2x SLA     → critical_breach: BLOCK regardless of policy
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

SLA_HOURS = {"critical": 1, "financial": 2, "client_facing": 4, "default": 8}

# Policies whose first breach already blocks (the rest only warn until 2x)
BLOCK_ON_FIRST_BREACH = {"critical", "financial"}


def sla_hours(policy: str | None) -> int:
    return SLA_HOURS.get(policy or "default", SLA_HOURS["default"])


def deadline_from(start_iso: str, policy: str | None) -> str | None:
    """Deadline ISO string from an assignment/checkout timestamp."""
    try:
        start = datetime.fromisoformat(str(start_iso).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None
    return (start + timedelta(hours=sla_hours(policy))).isoformat()


def evaluate(task: dict, now: datetime | None = None) -> dict:
    """Classify an in_progress task against its SLA.

    Returns {"status": "ok"|"breach"|"critical_breach"|"no_clock",
             "age_hours": float|None, "sla_hours": int, "should_block": bool}
    Tasks without checked_out_at/assigned_at have no running clock (e.g. founder
    external actions) — never blocked by SLA.
    """
    policy = task.get("execution_policy")
    hours = sla_hours(policy)
    start = task.get("checked_out_at") or task.get("assigned_at")
    if not start:
        return {"status": "no_clock", "age_hours": None, "sla_hours": hours, "should_block": False}
    try:
        start_dt = datetime.fromisoformat(str(start).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return {"status": "no_clock", "age_hours": None, "sla_hours": hours, "should_block": False}

    now = now or datetime.now(UTC)
    age = (now - start_dt).total_seconds() / 3600
    if age >= 2 * hours:
        return {"status": "critical_breach", "age_hours": round(age, 1), "sla_hours": hours, "should_block": True}
    if age >= hours:
        block = (policy or "default") in BLOCK_ON_FIRST_BREACH
        return {"status": "breach", "age_hours": round(age, 1), "sla_hours": hours, "should_block": block}
    return {"status": "ok", "age_hours": round(age, 1), "sla_hours": hours, "should_block": False}
