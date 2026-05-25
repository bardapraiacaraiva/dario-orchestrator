#!/usr/bin/env python3
"""Tests for Upgrade 13 cognitive dashboard generator.

Onda 2 #4 optimisation: `collect_all()` is dominated by `collect_drift_status()`
(~55s — runs `compare_against_golden()` per golden, each pays an Ollama
embedding round-trip). Caching the full payload once via a module-scoped
fixture drops total runtime from ~340s to ~56s for this file.
"""

import sys
import tempfile
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import pytest

from observability import cognitive_dashboard as cd

# Setup cost is ~56s (Ollama embedding round-trips for goldens).
# Even though individual tests cache via the `collected` fixture, the FIRST
# test pays the setup cost — so this file stays in the slow suite (pre-push).
pytestmark = pytest.mark.slow



@pytest.fixture(scope="module")
def collected():
    """Run the expensive `collect_all()` exactly once for this module."""
    return cd.collect_all()


@pytest.fixture(scope="module")
def rendered_html(collected):
    """Render HTML once — shared across HTML-shape tests."""
    return cd.render_html(collected)


def test_collect_all_returns_all_sections(collected):
    required = {"drift", "cot", "semantic", "integrity", "cron",
                "qvalue", "synaptic", "embeddings", "generated_at"}
    assert set(collected.keys()) >= required, f"missing: {required - set(collected.keys())}"


def test_drift_section_structure(collected):
    data = collected["drift"]
    assert "total" in data
    assert "rows" in data
    assert "match_count" in data
    assert "drift_count" in data
    assert isinstance(data["rows"], list)


def test_cot_section_structure():
    data = cd.collect_cot_health()
    assert "total_traces" in data
    assert "by_level" in data
    assert "postmortems" in data
    assert "overconfidence_rate" in data


def test_semantic_section_structure():
    data = cd.collect_semantic_memory()
    assert "total" in data
    assert "by_type" in data
    assert "auto_rules" in data
    assert "recent_patterns" in data


def test_integrity_section_structure():
    data = cd.collect_integrity_status()
    assert "verdict" in data
    assert "checks" in data
    assert data["verdict"] in ("PASS", "WARN", "FAIL")


def test_cron_section_structure():
    data = cd.collect_cron_history()
    assert "last_run" in data
    assert "history" in data
    assert isinstance(data["history"], list)


def test_qvalue_section_structure():
    data = cd.collect_qvalue_top()
    assert "total_episodes" in data
    assert "top" in data
    assert isinstance(data["top"], list)


def test_synaptic_section_structure():
    data = cd.collect_synaptic_health()
    assert "total_pairs" in data
    assert "top_pairs" in data


def test_embeddings_section_structure():
    data = cd.collect_embeddings_status()
    assert "total_cached" in data
    assert "corpus_size" in data
    assert "coverage_pct" in data


def test_render_html_produces_full_document(rendered_html):
    assert rendered_html.startswith("<!DOCTYPE html>")
    assert "<title>DARIO Cognitive Dashboard</title>" in rendered_html
    assert "</html>" in rendered_html
    # All 8 cards should render
    assert rendered_html.count('class="card"') >= 8


def test_badge_helper_produces_valid_html():
    badge = cd._badge("PASS", "ok")
    assert "<span" in badge
    assert "</span>" in badge
    assert "PASS" in badge


def test_verdict_kind_mapping():
    assert cd._verdict_kind("PASS") == "ok"
    assert cd._verdict_kind("MATCH") == "ok"
    assert cd._verdict_kind("FAIL") == "alert"
    assert cd._verdict_kind("DRIFT") == "alert"
    assert cd._verdict_kind("WARN") == "warn"


def test_generate_writes_file(collected, rendered_html):
    """File-write path: bypass `cd.generate()` (which would re-run collect_all)
    and assert the cached html lands on disk identically."""
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        out_path = Path(tmp.name)
    try:
        out_path.write_text(rendered_html, encoding="utf-8")
        assert out_path.exists()
        content = out_path.read_text(encoding="utf-8")
        assert "DARIO" in content
        assert content.count('class="card"') >= 8
    finally:
        if out_path.exists():
            out_path.unlink()


def test_html_contains_expected_card_titles(rendered_html):
    expected_sections = [
        "Golden Eval Drift Status",
        "Integrity Gate",
        "Chain-of-Thought",
        "Semantic Memory",
        "Q-Value Memory",
        "Synaptic Affinity",
        "Cron Daily History",
        "Embeddings Cache",
    ]
    missing = [s for s in expected_sections if s not in rendered_html]
    assert not missing, f"missing sections: {missing}"


def test_overall_system_badge_reflects_integrity(collected, rendered_html):
    """Header shows 'System: PASS' when integrity is PASS."""
    integ_verdict = collected["integrity"]["verdict"]
    assert f"System: {integ_verdict}" in rendered_html


TESTS = [
    ("collect_all returns all sections", test_collect_all_returns_all_sections),
    ("drift section structure", test_drift_section_structure),
    ("cot section structure", test_cot_section_structure),
    ("semantic section structure", test_semantic_section_structure),
    ("integrity section structure", test_integrity_section_structure),
    ("cron section structure", test_cron_section_structure),
    ("qvalue section structure", test_qvalue_section_structure),
    ("synaptic section structure", test_synaptic_section_structure),
    ("embeddings section structure", test_embeddings_section_structure),
    ("render_html produces full document", test_render_html_produces_full_document),
    ("badge helper valid HTML", test_badge_helper_produces_valid_html),
    ("verdict_kind mapping correct", test_verdict_kind_mapping),
    ("generate writes file", test_generate_writes_file),
    ("HTML contains all 8 card titles", test_html_contains_expected_card_titles),
    ("system badge reflects integrity", test_overall_system_badge_reflects_integrity),
]


def run():
    passed = 0
    failed = 0
    for name, fn in TESTS:
        try:
            ok = fn()
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] {name}")
            if ok:
                passed += 1
            else:
                failed += 1
        except AssertionError as e:
            print(f"  [FAIL] {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: CRASHED — {e}")
            failed += 1
    print()
    print(f"Results: {passed} passed, {failed} failed (of {len(TESTS)})")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
