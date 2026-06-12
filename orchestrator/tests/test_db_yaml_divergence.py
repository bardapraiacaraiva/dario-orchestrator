"""Behavior tests for the db_yaml_divergence autodiag check (Onda 2, 2026-06-12).

The 2026-06-01 divergence fix covered readers; a YAML-only writer reopened it
(61 June tasks invisible to DB-first dispatch/budget/dashboard). This check is
the tripwire for WRITERS: any YAML task absent from the DB must be flagged.

Uses the real tasks/active dir with a unique probe id + finally-cleanup
(the check reads Path.home() directly), mirroring the existing engine tests.
"""

import os
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

PROBE_ID = f"ZZPROBE-{os.getpid()}"
PROBE_FILE = ORCH_DIR / "tasks" / "active" / f"{PROBE_ID}.yaml"


def test_detects_yaml_only_task():
    from runners.autodiag import check_db_yaml_divergence

    PROBE_FILE.write_text(f"id: {PROBE_ID}\ntitle: divergence probe\nstatus: backlog\n", encoding="utf-8")
    try:
        result = check_db_yaml_divergence(fix=False)
        assert result["passed"] is False
        assert result["issues"], "yaml-only task must produce an issue"
        issue = result["issues"][0]
        assert issue["yaml_only_count"] >= 1
        assert PROBE_ID in issue["sample"] or issue["yaml_only_count"] > 10
    finally:
        PROBE_FILE.unlink(missing_ok=True)


def test_passes_when_reconciled():
    from runners.autodiag import check_db_yaml_divergence

    result = check_db_yaml_divergence(fix=False)
    # Post-backfill the live system must be clean; if this fails, a writer is
    # bypassing the DB again — run scripts/backfill_yaml_tasks_to_db.py and
    # find the writer.
    assert result["passed"] is True, f"writers bypassing DB: {result['issues']}"


def test_registered_in_check_names():
    from runners.autodiag import CHECK_NAMES

    assert "db_yaml_divergence" in CHECK_NAMES
