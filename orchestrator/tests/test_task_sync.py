"""core/task_sync.py — per-file YAML->DB upsert (dual-write path for skills).

Guards the interactive-path gap: session skills write task YAML directly;
sync_file must make the DB row match without re-running create_task (which
would force status='todo' and lose real state).
"""

import yaml

from core.task_sync import sync_file


def _write_task(tmp_path, **overrides):
    task = {
        "id": "TST-SYNC-901",
        "title": "task sync unit",
        "description": "unit",
        "project": "test-sync",
        "status": "in_review",  # non-default on purpose: insert must preserve it
        "priority": "low",
        "skill": "dario-content",
        "execution_policy": "default",
        "estimated_tokens": 100,
        "depends_on": ["TST-SYNC-900"],
        "created_at": "2026-06-12T20:00:00+00:00",
        "updated_at": "2026-06-12T20:00:00+00:00",
    }
    task.update(overrides)
    p = tmp_path / f"{task['id']}.yaml"
    p.write_text(yaml.dump(task, allow_unicode=True), encoding="utf-8")
    return p, task


def _cleanup(task_id):
    from core.db import DB
    with DB()._conn() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))


def test_insert_preserves_status_then_idempotent_then_update(tmp_path):
    path, task = _write_task(tmp_path)
    try:
        outcome, detail = sync_file(path)
        assert outcome == "inserted", detail

        from core.db import DB
        row = DB().get_task(task["id"])
        assert row is not None
        assert row["status"] == "in_review"  # not forced back to 'todo'

        # second run: no-op
        outcome, _ = sync_file(path)
        assert outcome == "unchanged"

        # edit YAML -> targeted update, created_at untouched
        task["priority"] = "critical"
        task["created_at"] = "1999-01-01T00:00:00+00:00"  # must be ignored
        path.write_text(yaml.dump(task, allow_unicode=True), encoding="utf-8")
        outcome, detail = sync_file(path)
        assert outcome == "updated"
        assert "priority" in detail and "created_at" not in detail

        row = DB().get_task(task["id"])
        assert row["priority"] == "critical"
        assert row["created_at"] == "2026-06-12T20:00:00+00:00"
    finally:
        _cleanup(task["id"])


def test_skips_non_task_yaml(tmp_path):
    p = tmp_path / "not-a-task.yaml"
    p.write_text("just: a string map\n", encoding="utf-8")
    outcome, _ = sync_file(p)
    assert outcome == "skipped"

    p2 = tmp_path / "broken.yaml"
    p2.write_text("{::not yaml::", encoding="utf-8")
    outcome, _ = sync_file(p2)
    assert outcome == "skipped"
