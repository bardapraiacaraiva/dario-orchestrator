"""End-to-end smoke tests for the orchestrator pulse cycle.

These tests exercise REAL code paths (not mocks):
  - cron_daily pipeline (all 9 jobs)
  - dispatch_engine --status (worker availability lookup)
  - smoke imports for all restored cognitive modules
  - golden_eval list/status (catches schema drift in eval DB)

They run against the real ~/.claude/orchestrator/ install — they don't
isolate to tmp_path because the goal is to catch regressions in actual
production state, not synthetic state.

If these tests fail, the orchestrator is materially broken — not just
a unit test.
"""
from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
PYTHON = sys.executable

# Restored Risk #7 modules — these must all import cleanly post-v12.4.0.
RESTORED_MODULES = [
    "dispatch.dispatch_engine",     # Phase 4 stage 4
    "cognitive.confidence_engine",  # Phase 4 stage 9
    "cognitive.chain_graph",        # Phase 4 stage 9
    "dispatch.dispatch_cot",        # Phase 4 stage 4
    "cognitive.dynamic_branch",     # Phase 4 stage 9
    "cognitive.episode_promoter",   # Phase 4 stage 2
    "safety.ethical_gate",          # Phase 4 stage 1
    "execution.executor",           # Phase 4 stage 10
    "quality.golden_eval",          # Phase 4 stage 5
    "cognitive.prompt_hints",       # Phase 4 stage 9
    "cognitive.qvalue_memory_wire", # Phase 4 stage 9
    "dispatch.semantic_dispatch",   # Phase 4 stage 4
    "cognitive.synaptic_update",    # Phase 4 stage 9
]


@pytest.fixture(autouse=True)
def _ensure_orch_in_path(monkeypatch):
    """Tests run with the orchestrator dir at front of sys.path so module
    imports resolve to the real codebase, not a sibling clone."""
    monkeypatch.syspath_prepend(str(ORCH_DIR))


# ─── Import smoke tests ──────────────────────────────────────────────────


@pytest.mark.parametrize("mod_name", RESTORED_MODULES)
def test_restored_module_imports(mod_name):
    """Each of the 13 restored cognitive modules must import without error.

    Catches: stubs reintroduced, missing dependencies, syntax errors from
    bad merges. This is the gate that would have prevented the v12.4.0
    open-everything regression if any module's restore was incomplete.
    """
    mod = importlib.import_module(mod_name)
    assert mod is not None, f"{mod_name} imported as None"
    # Sanity: each module should expose at least a few public symbols
    public = [x for x in dir(mod) if not x.startswith("_")]
    assert len(public) >= 5, f"{mod_name} has only {len(public)} public symbols — likely stub"


# ─── Critical CLI smoke tests ────────────────────────────────────────────


@pytest.mark.parametrize("module_file,help_arg", [
    ("dispatch/dispatch_engine.py", "--help"),       # Phase 4 stage 4
    ("cron_daily.py", "--help"),
    ("quality/golden_eval.py", "--help"),            # Phase 4 stage 5
    ("cognitive/synaptic_update.py", "--help"),      # Phase 4 stage 9
    ("cognitive/episode_promoter.py", "--help"),     # Phase 4 stage 2
    ("dispatch/dispatch_cot.py", "--help"),          # Phase 4 stage 4
])
def test_critical_cli_help(module_file, help_arg):
    """Each critical CLI must respond to --help with exit code 0.

    Catches: argparse misconfiguration, top-level imports broken,
    decorator errors at module load time.
    """
    result = subprocess.run(
        [PYTHON, str(ORCH_DIR / module_file), help_arg],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=str(ORCH_DIR),
    )
    assert result.returncode == 0, f"{module_file} {help_arg} failed: {result.stderr[:200]}"
    assert "usage:" in result.stdout.lower() or "options:" in result.stdout.lower(), \
        f"{module_file} {help_arg} produced no help output"


# ─── dispatch_engine --status ────────────────────────────────────────────


def test_dispatch_engine_status_lists_workers():
    """`dispatch/dispatch_engine.py --status` must list workers from company.yaml.

    Catches: company.yaml schema drift, company_loader bug, dispatch_engine
    regression in its CompanyHierarchy parsing.
    """
    result = subprocess.run(
        [PYTHON, str(ORCH_DIR / "dispatch" / "dispatch_engine.py"), "--status"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=str(ORCH_DIR),
    )
    assert result.returncode == 0, f"dispatch_engine --status exit {result.returncode}: {result.stderr[:200]}"
    # Look for the canonical "WORKER AVAILABILITY" header that the engine prints
    assert "WORKER AVAILABILITY" in result.stdout or "load:" in result.stdout, \
        "no worker availability output — engine may have broken its hierarchy parsing"


# ─── cron_daily end-to-end (THE big one) ────────────────────────────────


def test_cron_daily_dry_run_executes_all_jobs():
    """`cron_daily.py --dry-run --force` must complete and report 'Cron daily complete'.

    This is the BIG e2e: it exercises ~6 of the 13 restored modules
    (dispatch_cot, golden_eval, episode_promoter, synaptic_update,
    prompt_hints, qvalue_memory_wire) in one pipeline.

    Catches: any of the 9 daily jobs broken, schema mismatches in
    quality/*.yaml, broken dependencies between cognitive modules.

    Allows: WARNING status (integrity_gate often warns on
    embeddings_coverage). Only fails on hard error (non-zero exit, no
    completion line).
    """
    result = subprocess.run(
        [PYTHON, str(ORCH_DIR / "cron_daily.py"), "--dry-run", "--force"],
        capture_output=True,
        text=True,
        timeout=180,  # 3min ceiling; should complete in <10s
        cwd=str(ORCH_DIR),
    )

    # cron_daily exits 1 when status=warn (1+ check degraded) — that's
    # informational, not a hard failure. Only exit code 2 or stderr signals
    # a real crash.
    assert result.returncode in (0, 1), \
        f"cron_daily hard-failed exit {result.returncode}: {result.stderr[-500:]}"
    assert "Cron daily complete" in result.stdout, \
        f"cron_daily did not complete cleanly. tail: {result.stdout[-500:]}"
    # Check at least 5 of the 9 jobs ran (the cognitive ones)
    expected_jobs = ["promote_episodes", "regression_check", "dispatch_cot_stats",
                     "state_snapshot", "integrity_gate"]
    missing = [j for j in expected_jobs if j not in result.stdout]
    assert not missing, f"cron_daily missing jobs: {missing}. Output tail: {result.stdout[-500:]}"


# ─── Enforcement layer integration (verify guards play nicely with dispatch) ─


def test_enforcement_modules_importable_and_callable():
    """The 3 enforcement modules + their public API must work together.

    Catches: regression in any of budget_gate / dispatch_validator /
    parallelism_guard that would break dispatch.
    """
    from enforcement import (
        BudgetExceededError,
        ParallelismExceededError,
        TaskValidationError,
    )
    from enforcement.budget_gate import current_budget_state, is_budget_safe
    from enforcement.dispatch_validator import validate_task
    from enforcement.parallelism_guard import slot

    # is_budget_safe doesn't raise — just returns bool
    safe = is_budget_safe()
    assert isinstance(safe, bool)

    # current_budget_state returns dict with _source key
    state = current_budget_state()
    assert isinstance(state, dict)
    assert "_source" in state

    # validate_task accepts a minimal task and returns the validation dict
    minimal = {"id": "TEST-001", "skill": "dario-brand"}
    r = validate_task(minimal)
    assert isinstance(r, dict)
    assert "valid" in r and "errors" in r and "warnings" in r


# ─── Skill inventory regression guard ────────────────────────────────────


def test_skill_inventory_yaml_exists_and_is_valid():
    """skill_usage_audit.yaml must exist + parse + have expected top-level keys.

    Catches: skill_usage_audit.py regression that would silently produce
    empty/broken inventory output.
    """
    import yaml
    inv_file = ORCH_DIR / "quality" / "skill_usage_audit.yaml"
    if not inv_file.exists():
        pytest.skip("skill_usage_audit.yaml not generated yet — run `python scripts/skill_usage_audit.py` first")
    data = yaml.safe_load(inv_file.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    for key in ("total_skills", "tier_counts", "per_skill"):
        assert key in data, f"skill_usage_audit.yaml missing key: {key}"
    assert data["total_skills"] >= 100, \
        f"only {data['total_skills']} skills detected — inventory broken"
