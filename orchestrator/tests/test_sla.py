"""Behavior tests for SLA enforcement (Onda 4, 2026-06-12).

core/sla.py replaced the fixed 60-minute zombie reaper (which ignored
execution policy) and the markdown-only SLA tables in lucas-heartbeat.
"""

import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from core.sla import BLOCK_ON_FIRST_BREACH, SLA_HOURS, deadline_from, evaluate, sla_hours

NOW = datetime(2026, 6, 12, 12, 0, 0, tzinfo=UTC)


def _task(policy, hours_ago):
    return {
        "id": "SLA-TEST",
        "execution_policy": policy,
        "checked_out_at": (NOW - timedelta(hours=hours_ago)).isoformat(),
    }


def test_doctrine_table_matches_heartbeat_skill():
    assert SLA_HOURS == {"critical": 1, "financial": 2, "client_facing": 4, "default": 8}
    assert BLOCK_ON_FIRST_BREACH == {"critical", "financial"}
    assert sla_hours(None) == 8
    assert sla_hours("unknown-policy") == 8


def test_within_sla_is_ok():
    v = evaluate(_task("default", hours_ago=7), now=NOW)
    assert v["status"] == "ok" and not v["should_block"]


def test_default_breach_warns_but_does_not_block():
    v = evaluate(_task("default", hours_ago=9), now=NOW)
    assert v["status"] == "breach" and v["should_block"] is False


def test_critical_breach_blocks_on_first_breach():
    v = evaluate(_task("critical", hours_ago=1.5), now=NOW)
    assert v["status"] == "breach" and v["should_block"] is True


def test_financial_breach_blocks_on_first_breach():
    v = evaluate(_task("financial", hours_ago=2.5), now=NOW)
    assert v["status"] == "breach" and v["should_block"] is True


def test_double_sla_blocks_any_policy():
    v = evaluate(_task("default", hours_ago=17), now=NOW)
    assert v["status"] == "critical_breach" and v["should_block"] is True


def test_no_clock_never_blocks():
    """Founder external actions sit in_progress for days with no checkout —
    they must never be SLA-blocked (RADAR-009 case)."""
    v = evaluate({"id": "X", "execution_policy": "critical"}, now=NOW)
    assert v["status"] == "no_clock" and v["should_block"] is False


def test_deadline_from_policy():
    d = deadline_from(NOW.isoformat(), "client_facing")
    assert d == (NOW + timedelta(hours=4)).isoformat()
    assert deadline_from("garbage", "default") is None


def test_db_assign_stamps_sla_deadline(tmp_path):
    from core.db import DB
    db = DB(db_path=str(tmp_path / "test.db"))
    db.create_task({"id": "SLA-DB-1", "title": "t", "execution_policy": "financial"})
    assert db.assign_task("SLA-DB-1", "worker-x", "test")
    t = db.get_task("SLA-DB-1")
    assert t["sla_deadline"], "assign must stamp sla_deadline"
    assigned = datetime.fromisoformat(t["assigned_at"])
    deadline = datetime.fromisoformat(t["sla_deadline"])
    assert abs((deadline - assigned) - timedelta(hours=2)) < timedelta(seconds=1)
