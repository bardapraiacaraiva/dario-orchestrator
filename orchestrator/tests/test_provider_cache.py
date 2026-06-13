"""Cache wiring on the autonomous API path (Fix A, 2026-06-13).

The cache module + hooks existed but nothing called them, so memory/cache stayed
empty (0 entries, 0 tokens saved). These tests pin the wiring now added to
providers.anthropic.execute_task:

  - a byte-identical prompt on a cacheable skill is served from cache, the
    Claude API is NOT re-called, and the run reports 0 tokens;
  - a non-cacheable skill (no cache_key) never touches the cache.
"""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import pytest

FIXED_PROMPT = "DETERMINISTIC-PROMPT-FOR-CACHE-TEST"
GENERATED = "## Deliverable\nGenerated client-ready content.\n"


def _wire(monkeypatch, tmp_path, *, cache_key):
    """Stub execute_task's heavy collaborators; return the API-call recorder."""
    from providers import anthropic as api
    import memory.cache as cache

    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    monkeypatch.setattr(cache, "CACHE_DIR", cache_dir)

    class _DB:
        def journal_step(self, *a, **k):
            pass

    monkeypatch.setattr(api, "DB", lambda *a, **k: _DB())
    monkeypatch.setattr(api, "run_engine", lambda *a, **k: {})

    task = {"id": "T-1", "skill": "dario-offer", "project": "p"}
    if cache_key:
        task["cache_key"] = cache_key
    prep = {"ok": True, "status": "ready", "steps": [], "task": task,
            "prompt": FIXED_PROMPT, "rubric": {}, "recommended_model": "sonnet"}
    monkeypatch.setattr(api.lifecycle, "prepare", lambda *a, **k: prep)

    calls = []

    def fake_api(prompt, skill, model, retries=2):
        calls.append(prompt)
        return {"success": True, "output": GENERATED,
                "input_tokens": 500, "output_tokens": 300, "cost": 0.02}

    monkeypatch.setattr(api, "call_claude_api", fake_api)
    monkeypatch.setattr(api, "auto_score_output", lambda out, rub, task: {"score": 80})
    monkeypatch.setattr(api.lifecycle, "finalize_success",
                        lambda *a, **k: {"status": "done", "steps": []})
    return api, calls


def test_cache_hit_skips_api(tmp_path, monkeypatch):
    import memory.cache as cache
    api, calls = _wire(monkeypatch, tmp_path, cache_key="dario-offer_p_T-1")

    # 1st run — miss: API called, cache populated on the clean done.
    r1 = api.execute_task("T-1")
    assert len(calls) == 1
    assert r1["tokens"]["total"] == 800
    assert cache.stats()["entries"] == 1

    # 2nd run — byte-identical prompt: hit, API not re-called, 0 tokens.
    r2 = api.execute_task("T-1")
    assert len(calls) == 1, "API must not be called again on a cache hit"
    assert any(s.get("step") == "cache_hit" for s in r2["steps"])
    assert r2["tokens"]["total"] == 0


def test_non_cacheable_skill_ignores_cache(tmp_path, monkeypatch):
    import memory.cache as cache
    api, calls = _wire(monkeypatch, tmp_path, cache_key=None)

    api.execute_task("T-1")
    api.execute_task("T-1")
    # No cache_key => never consulted nor populated; API hit both times.
    assert len(calls) == 2
    assert cache.stats()["entries"] == 0
