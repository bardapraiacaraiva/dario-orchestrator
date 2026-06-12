"""Behavior tests for the replanner dual-write persistence (DD finding A8, 2026-06-12).

The replanner was the last YAML-only task writer in a DB-first system: every
run reopened the DB<->YAML divergence the 2026-06-01/Onda 2 fixes closed.
Convention under test: SQLite is the authority, tasks/active/*.yaml is a
mirror — every mutation must hit BOTH in the same operation.

Isolated via tmp_path: a throwaway DB is injected into the module-level cache
and TASKS_DIR is repointed, so no production state is touched.
"""

import sys
from pathlib import Path

import pytest
import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import execution.replanner as replanner  # noqa: E402
from core.db import DB  # noqa: E402

TASK_ID = "RPL-001"


def _make_task(task_id=TASK_ID, status="in_progress"):
    return {
        "id": task_id,
        "title": "replanner dual-write probe",
        "description": "probe",
        "project": "test",
        "status": status,
        "priority": "medium",
        "assignee": "worker-x",
        "skill": "dario-brand",
        "revision_count": 0,
        "notes": [],
        "watchers": [],
    }


@pytest.fixture
def env(tmp_path, monkeypatch):
    """Throwaway DB + tasks dir wired into the replanner module."""
    tasks_dir = tmp_path / "tasks" / "active"
    tasks_dir.mkdir(parents=True)
    db = DB(db_path=str(tmp_path / "test.db"))
    monkeypatch.setattr(replanner, "TASKS_DIR", tasks_dir)
    monkeypatch.setattr(replanner, "_DB", db)
    return {"db": db, "tasks_dir": tasks_dir}


def _seed(env, status="in_progress"):
    """Seed the same task in DB and YAML mirror (the reconciled state)."""
    task = _make_task()
    env["db"].create_task(task)  # create_task forces status='todo'
    env["db"].update_task(TASK_ID, {"status": status})
    yaml_file = env["tasks_dir"] / f"{TASK_ID}.yaml"
    yaml_file.write_text(
        yaml.dump({**task, "status": status}, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return yaml_file


# ─── Dual-write: mutation must land in DB AND YAML ───────────────────────


def test_retry_mutation_hits_db_and_yaml(env):
    yaml_file = _seed(env, status="in_progress")

    result = replanner.replan(TASK_ID, "agent_timeout")

    assert result["action"] == "retry_same"
    assert result["applied"] is True

    db_task = env["db"].get_task(TASK_ID)
    assert db_task["status"] == "todo", "DB (authority) missed the mutation"

    mirrored = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
    assert mirrored["status"] == "todo", "YAML mirror missed the mutation"
    assert mirrored["revision_count"] == 1
    assert any("REPLAN" in str(n) for n in mirrored["notes"])


def test_escalate_mutation_hits_db_and_yaml(env):
    yaml_file = _seed(env, status="in_progress")

    # budget_exceeded goes straight to escalate (no company.yaml lookup)
    result = replanner.replan(TASK_ID, "budget_exceeded")

    assert result["action"] == "escalate"
    db_task = env["db"].get_task(TASK_ID)
    assert db_task["status"] == "blocked"
    assert "Auto-recovery exhausted" in (db_task["blocked_reason"] or "")

    mirrored = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
    assert mirrored["status"] == "blocked"
    assert "dario-ceo" in mirrored["watchers"]


# ─── Divergence healing ──────────────────────────────────────────────────


def test_yaml_only_task_is_healed_into_db(env):
    """Legacy YAML-only task: a replan write must create the DB row, keeping
    the db_yaml_divergence tripwire green instead of perpetuating drift."""
    task = _make_task()
    yaml_file = env["tasks_dir"] / f"{TASK_ID}.yaml"
    yaml_file.write_text(yaml.dump(task, allow_unicode=True, sort_keys=False), encoding="utf-8")
    assert env["db"].get_task(TASK_ID) is None  # precondition: YAML-only

    result = replanner.replan(TASK_ID, "budget_exceeded")

    assert result["applied"] is True
    db_task = env["db"].get_task(TASK_ID)
    assert db_task is not None, "YAML-only task was not backfilled into the DB"
    assert db_task["status"] == "blocked"


def test_db_only_task_gets_yaml_mirror(env):
    """DB-only task (no YAML file): replan must still work and write the mirror."""
    env["db"].create_task(_make_task())
    env["db"].update_task(TASK_ID, {"status": "in_progress"})
    yaml_file = env["tasks_dir"] / f"{TASK_ID}.yaml"
    assert not yaml_file.exists()

    result = replanner.replan(TASK_ID, "agent_timeout")

    assert result["action"] == "retry_same"
    assert env["db"].get_task(TASK_ID)["status"] == "todo"
    assert yaml_file.exists(), "YAML mirror was not written"
    assert yaml.safe_load(yaml_file.read_text(encoding="utf-8"))["status"] == "todo"


# ─── Safety rails ────────────────────────────────────────────────────────


def test_missing_task_does_not_explode(env):
    result = replanner.replan("NOPE-404", "unknown")

    assert result["action"] == "escalate"
    assert result["applied"] is False
    assert result["details"] == "Task not found"
    assert not (env["tasks_dir"] / "NOPE-404.yaml").exists()
    assert env["db"].get_task("NOPE-404") is None


def test_dry_run_writes_nothing(env):
    yaml_file = _seed(env, status="in_progress")
    before = yaml_file.read_text(encoding="utf-8")

    result = replanner.replan(TASK_ID, "agent_timeout", dry_run=True)

    assert result["action"] == "retry_same"  # plan is still computed
    assert result["applied"] is False
    assert result["dry_run"] is True
    assert env["db"].get_task(TASK_ID)["status"] == "in_progress", "dry-run wrote to DB"
    assert yaml_file.read_text(encoding="utf-8") == before, "dry-run wrote to YAML"
