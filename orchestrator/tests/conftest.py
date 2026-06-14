"""Shared fixtures for DARIO orchestrator tests.

Onda 3 #1 — Mock Ollama embeddings by default.

Why
----
`semantic_dispatch._embed()` does a 4-5s HTTP round-trip to a local Ollama
server (`nomic-embed-text` model). Several test files call this indirectly
via `golden_eval.compare_against_golden()`. The result was a test suite
dominated by network latency rather than by what we're actually testing.

Default behaviour
-----------------
Every test gets a fast deterministic mock automatically — `_embed(text)`
returns a hash-derived 768-dim vector. Same text → same vector. Different
text → different vector.

Opt-out
-------
A test that NEEDS the real Ollama (smoke tests, integration with the live
model) declares it:

    @pytest.mark.real_embedding
    def test_real_ollama_connection():
        ...

Side benefit: the mock also unblocks CI environments that don't have
Ollama running. Today the suite implicitly required an Ollama daemon.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

# Add orchestrator to path.
# Resolve in priority order so the suite runs both locally AND in CI
# (where the checkout lives in /home/runner/work/..., not ~/.claude):
#   1. DARIO_ORCH_DIR env var (explicit override)
#   2. the repo this conftest lives in (tests/ -> orchestrator/)
#   3. ~/.claude/orchestrator (legacy local-install default)
# (Fase 1 fix, 2026-06-12 — was hard-anchored to Path.home(), red CI.)
_env_dir = os.environ.get("DARIO_ORCH_DIR")
if _env_dir:
    ORCH_DIR = Path(_env_dir)
elif (Path(__file__).resolve().parent.parent / "core").is_dir():
    ORCH_DIR = Path(__file__).resolve().parent.parent
else:
    ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


EMBED_DIM = 768  # nomic-embed-text dimension


def _deterministic_embed(text: str, timeout: int = 30) -> list[float]:
    """Hash-derived pseudo-embedding. Same text → same vector, no I/O."""
    if not text:
        return [0.0] * EMBED_DIM
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    needed = (EMBED_DIM + 31) // 32
    expanded = digest * needed
    return [(b / 127.5) - 1.0 for b in expanded[:EMBED_DIM]]


def pytest_configure(config):
    """Register the real_embedding marker so pytest.ini doesn't reject it."""
    config.addinivalue_line(
        "markers",
        "real_embedding: bypass the Ollama mock and call the real _embed() "
        "(requires Ollama running on localhost:11434).",
    )


# Tests that depend on a populated ~/.claude (runtime tasks/, seeded goldens,
# promoted episodes, the orch CLI driving a real state DB). They pass locally
# (pre-push) where that environment exists, but a clean CI checkout has none of
# it. Marked requires_live_env here and excluded in CI; see pytest.ini.
# TODO(2026-06-14): make these hermetic (tmp_path fixtures + seeded fixtures)
# and drop them from this list so CI regains the coverage.
_LIVE_ENV_TESTS = (
    "test_engines.py::TestDispatchEngine::test_status_runs",
    "test_engines.py::TestDispatchEngine::test_dry_run",
    "test_engines.py::TestDispatchEngine::test_json_output",
    "test_engines.py::TestStateMachine::test_show_state",
    "test_engines.py::TestStateMachine::test_evaluate",
    "test_engines.py::TestQualityScorer::test_dashboard",
    "test_goldens_seeded.py::test_all_eval_cases_have_golden",
    "test_goldens_seeded.py::test_calibration_log_has_entries",
    "test_goldens_seeded.py::test_drift_simulation_triggers_alert",
    "test_episode_promoter.py::test_stats_returns_counts",
    "test_episode_promoter.py::test_existing_semantic_names_includes_promoted",
    "test_db_yaml_divergence.py::test_detects_yaml_only_task",
    "test_lex_br.py::test_semantic_dispatch_routes_to_lex_trabalhista",
    "test_pulse_e2e.py::test_cron_daily_dry_run_executes_all_jobs",
)


def pytest_collection_modifyitems(config, items):
    """Auto-tag the known live-env-dependent tests so CI can exclude them."""
    for item in items:
        if any(key in item.nodeid for key in _LIVE_ENV_TESTS):
            item.add_marker(pytest.mark.requires_live_env)


@pytest.fixture(autouse=True)
def mock_ollama_embed(request, monkeypatch):
    """Replace `semantic_dispatch._embed` with a deterministic mock by default.

    If `semantic_dispatch` is unavailable (e.g. trial repo where it's a VIP
    stub that raises ImportError), this becomes a no-op — the test simply
    doesn't get embedding mocking. Tests that don't use embeddings work fine;
    tests that do will hit a different error closer to their actual usage.
    """
    if request.node.get_closest_marker("real_embedding"):
        # Test opted out — let it use the real Ollama HTTP client.
        yield
        return

    try:
        from dispatch import semantic_dispatch
    except ImportError:
        # Module not available in this install — fixture becomes no-op
        yield
        return

    monkeypatch.setattr(semantic_dispatch, "_embed", _deterministic_embed)

    # Modules that did `from semantic_dispatch import _embed` at import time
    # need their local binding patched too.
    for mod_name in ("golden_eval",):
        mod = sys.modules.get(mod_name)
        if mod is not None and hasattr(mod, "_embed"):
            monkeypatch.setattr(mod, "_embed", _deterministic_embed)

    yield


# ─── Pre-existing fixtures ───────────────────────────────────────────────────


@pytest.fixture
def test_db(tmp_path):
    """Fresh SQLite DB for each test."""
    from core.db import DB
    db_path = str(tmp_path / "test.db")
    db = DB(db_path=db_path)
    return db


@pytest.fixture
def populated_db(test_db):
    """DB with sample tasks."""
    test_db.create_task({"id": "T-001", "title": "Brand positioning", "project": "test", "skill": "dario-brand", "priority": "critical"})
    test_db.create_task({"id": "T-002", "title": "Naming check", "project": "test", "skill": "dario-naming", "priority": "medium", "depends_on": json.dumps(["T-001"])})
    test_db.create_task({"id": "T-003", "title": "SEO audit", "project": "test", "skill": "seo-audit", "priority": "high"})
    return test_db
