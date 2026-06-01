"""Invariant: SQLite (TaskStore) is the single source of truth for tasks.

CONVENTIONS.md declares the DB authoritative. The 2026-06-01 audit found the
dashboard and budget_tracker still globbed tasks/*.yaml as their PRIMARY source
(YAML empty post-migration) while the engine/runtime acted on the DB — they
showed 0 tasks / 0 tokens while the DB held 115 tasks. This test is the tripwire
that stops that divergence class from coming back:

  Any production file that reads tasks from the YAML task dirs MUST also have a
  DB path (reference TaskStore / task_store / DB.get_tasks). A YAML glob is only
  acceptable as a documented DB-first *fallback*. A new pure-YAML task reader
  fails this test, forcing it to go DB-first before it can merge.

This is a static guard (cheap, deterministic, no live DB needed). It does not
prove ordering is DB-first — that is covered by the per-reader behavior tests
(test_budget_tracker_monthly, etc.) — but it guarantees no reader is YAML-only.
"""
from __future__ import annotations

import re
from pathlib import Path

ORCH = Path.home() / ".claude" / "orchestrator"

# Signals that a file reads tasks from the YAML task directories.
TASK_YAML_READER = re.compile(
    r"""TASKS_DIR\.glob"""          # the common pattern
    r"""|TASKS_ACTIVE"""            # active task dir constant
    r"""|TASKS_DONE"""              # done task dir constant
    r"""|["']tasks["']\s*/""",      # Path(...) / "tasks" / subdir   (dashboard)
    re.VERBOSE,
)
GLOBS_YAML = re.compile(r"""\.glob\(\s*['"]\*\.yaml['"]""")

# Markers proving the file has a DB path (so the YAML glob is a fallback, not
# the primary source). Includes the ORM-ish helpers AND raw sqlite access, since
# some readers (e.g. synaptic_update) hit orchestrator.db directly.
DB_MARKER = re.compile(
    r"""TaskStore|task_store|get_tasks|core\.db|\bDB\(\)"""
    r"""|sqlite3|conn\.execute|orchestrator\.db|DB_PATH"""
)


def _production_py_files():
    for py in ORCH.rglob("*.py"):
        parts = py.parts
        if ".venv" in parts or "__pycache__" in parts:
            continue
        if "tests" in parts:
            continue
        yield py


def test_no_yaml_only_task_reader():
    offenders = []
    for py in _production_py_files():
        try:
            text = py.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        reads_task_yaml = bool(TASK_YAML_READER.search(text)) and bool(GLOBS_YAML.search(text))
        if reads_task_yaml and not DB_MARKER.search(text):
            offenders.append(str(py.relative_to(ORCH)))
    assert not offenders, (
        "These files read tasks from YAML without a DB-first path (SQLite is the "
        "source of truth — see CONVENTIONS.md). Route them through TaskStore:\n  - "
        + "\n  - ".join(sorted(offenders))
    )


def test_canonical_loader_is_db_first():
    """The canonical TaskStore.get_all must try the DB before the YAML fallback."""
    text = (ORCH / "core" / "task_store.py").read_text(encoding="utf-8")
    assert "_yaml_fallback" in text, "TaskStore lost its YAML fallback"
    # DB attempt must appear before the YAML fallback in get_all.
    db_idx = text.find("self._db.get_tasks")
    fallback_idx = text.find("_yaml_fallback")
    assert db_idx != -1 and fallback_idx != -1
    assert db_idx < fallback_idx, "TaskStore.get_all must try the DB before YAML"
