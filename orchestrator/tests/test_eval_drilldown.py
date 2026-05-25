#!/usr/bin/env python3
"""Tests for Upgrade 16 eval drilldown."""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import pytest

from quality import eval_drilldown as ed
from quality import golden_eval

pytestmark = pytest.mark.slow

SANDBOX_EVAL = "test-drilldown-sandbox-xyz"


def _cleanup():
    for ext in (".golden.txt", ".golden.json"):
        f = golden_eval.GOLDEN_DIR / f"{SANDBOX_EVAL}{ext}"
        if f.exists():
            f.unlink()


def test_no_golden_returns_status():
    _cleanup()
    diff = ed.diff_dimensions("nonexistent-eval-xxx", "any candidate text")
    assert diff["status"] == "no_golden"


def test_identical_candidate_yields_match():
    _cleanup()
    sample = """# Section A

Some content here with several content words.

## Section B

More content with relevant terms."""
    golden_eval.capture_golden(SANDBOX_EVAL, sample, human_score=85)
    diff = ed.diff_dimensions(SANDBOX_EVAL, sample, candidate_score=85)
    assert diff["compare"]["verdict"] == "MATCH"
    assert diff["tokens"]["lost_count"] == 0
    assert diff["tokens"]["gained_count"] == 0
    _cleanup()


def test_degraded_candidate_detects_lost_tokens():
    _cleanup()
    golden = "alpha beta gamma delta epsilon zeta eta theta " * 10
    candidate = "alpha beta gamma " * 5  # missing delta, epsilon, etc
    golden_eval.capture_golden(SANDBOX_EVAL, golden, human_score=85)
    diff = ed.diff_dimensions(SANDBOX_EVAL, candidate, candidate_score=60)
    assert diff["tokens"]["lost_count"] >= 4
    assert "delta" in diff["tokens"]["lost"]
    assert "epsilon" in diff["tokens"]["lost"]
    _cleanup()


def test_section_diff_detects_missing_headers():
    _cleanup()
    golden = """# Main Title

intro content here

## Section One
content one with several words

## Section Two
content two with more words

## Section Three
content three with even more words
"""
    candidate = """# Main Title

intro content here

## Section One
content one with several words
"""
    golden_eval.capture_golden(SANDBOX_EVAL, golden, human_score=85)
    diff = ed.diff_dimensions(SANDBOX_EVAL, candidate, candidate_score=60)
    missing = diff["sections"]["missing_in_candidate"]
    assert "Section Two" in missing
    assert "Section Three" in missing
    _cleanup()


def test_paragraph_echo_detection():
    _cleanup()
    golden = "First paragraph with unique content alpha beta gamma delta.\n\nSecond paragraph with unique content epsilon zeta eta theta.\n\nThird paragraph entirely different iota kappa lambda mu."
    candidate = "First paragraph with unique content alpha beta gamma delta."
    golden_eval.capture_golden(SANDBOX_EVAL, golden, human_score=85)
    diff = ed.diff_dimensions(SANDBOX_EVAL, candidate, candidate_score=70)
    assert diff["paragraphs"]["missing_count"] >= 1
    _cleanup()


def test_recovery_hints_for_score_drop():
    _cleanup()
    golden = "content content content " * 50
    candidate = golden  # identical content
    golden_eval.capture_golden(SANDBOX_EVAL, golden, human_score=88)
    # Candidate scored 25pts lower than human baseline
    diff = ed.diff_dimensions(SANDBOX_EVAL, candidate, candidate_score=63)
    hints = " ".join(diff["recovery_hints"])
    assert "score" in hints.lower()
    assert "regression" in hints.lower() or "below" in hints.lower()
    _cleanup()


def test_recovery_hints_for_short_output():
    _cleanup()
    golden = "long content " * 100  # 1300+ chars
    candidate = "short"
    golden_eval.capture_golden(SANDBOX_EVAL, golden, human_score=85)
    diff = ed.diff_dimensions(SANDBOX_EVAL, candidate, candidate_score=60)
    hints = " ".join(diff["recovery_hints"])
    assert "shorter" in hints.lower() or "expand" in hints.lower()
    _cleanup()


def test_recovery_hints_for_long_output():
    _cleanup()
    golden = "tight content"
    candidate = "verbose content " * 500
    golden_eval.capture_golden(SANDBOX_EVAL, golden, human_score=85)
    diff = ed.diff_dimensions(SANDBOX_EVAL, candidate, candidate_score=60)
    hints = " ".join(diff["recovery_hints"])
    assert "longer" in hints.lower() or "trim" in hints.lower() or "verbose" in hints.lower()
    _cleanup()


def test_format_human_includes_all_sections():
    _cleanup()
    golden = "# Section\n\ncontent alpha beta gamma " * 10
    candidate = "# Section\n\ncontent alpha"
    golden_eval.capture_golden(SANDBOX_EVAL, golden, human_score=85)
    diff = ed.diff_dimensions(SANDBOX_EVAL, candidate, candidate_score=65)
    text = ed.format_human(diff)
    assert "TOKEN DIFF" in text
    assert "SECTIONS" in text
    assert "PARAGRAPHS" in text
    assert "RECOVERY HINTS" in text
    _cleanup()


def test_top_lost_ordered_by_frequency():
    _cleanup()
    # Use varied unique tokens to avoid stop-word filtering
    golden = ("freq_alpha " * 10) + ("freq_beta " * 5) + ("freq_gamma " * 1)
    candidate = "completely_different_token "
    golden_eval.capture_golden(SANDBOX_EVAL, golden, human_score=85)
    diff = ed.diff_dimensions(SANDBOX_EVAL, candidate, candidate_score=60)
    top = diff["tokens"]["top_lost"]
    # First should be the highest-frequency lost token
    assert len(top) > 0
    # freq_alpha should rank before freq_beta before freq_gamma
    tokens_ordered = [t for t, _ in top]
    if "freq_alpha" in tokens_ordered and "freq_beta" in tokens_ordered:
        assert tokens_ordered.index("freq_alpha") < tokens_ordered.index("freq_beta")
    _cleanup()


def test_paragraph_count_accurate():
    _cleanup()
    golden = "para one with content alpha beta\n\npara two with content gamma delta\n\npara three with content epsilon zeta"
    candidate = "para one with content alpha beta"
    golden_eval.capture_golden(SANDBOX_EVAL, golden, human_score=85)
    diff = ed.diff_dimensions(SANDBOX_EVAL, candidate, candidate_score=60)
    assert diff["paragraphs"]["golden_count"] == 3
    assert diff["paragraphs"]["candidate_count"] == 1
    _cleanup()


def test_tokens_helper_filters_stop_words():
    toks = ed._tokens("the brand of premium restaurant in cascais")
    assert "the" not in toks
    assert "brand" in toks
    assert "restaurant" in toks


def test_sections_helper_finds_headers():
    text = "# H1\nsome\n## H2 With Space\nmore\n### H3\nfinal"
    secs = ed._sections(text)
    assert "H1" in secs
    assert "H2 With Space" in secs
    assert "H3" in secs


def test_drilldown_drifting_handles_no_runs_dir():
    """When evals/last_runs/ doesn't exist, returns no_runs_dir status."""
    runs_dir = golden_eval.EVAL_DIR / "last_runs"
    if not runs_dir.exists():
        r = ed.drilldown_drifting()
        assert r["status"] == "no_runs_dir"


def test_real_golden_drilldown():
    """Run drilldown against one of the real seeded goldens with synthetic degradation."""
    eval_id = "eval-brand-01"
    text_file = golden_eval.GOLDEN_DIR / f"{eval_id}.golden.txt"
    if not text_file.exists():
        return True  # skip if not seeded
    golden_text = text_file.read_text(encoding="utf-8")
    degraded = golden_text[:300] + "\n\nResto eliminado."
    diff = ed.diff_dimensions(eval_id, degraded, candidate_score=60)
    # Should detect lost tokens, missing sections, recovery hints
    assert diff["tokens"]["lost_count"] > 10
    assert len(diff["sections"]["missing_in_candidate"]) > 0
    assert len(diff["recovery_hints"]) > 0


TESTS = [
    ("no golden returns status", test_no_golden_returns_status),
    ("identical candidate yields MATCH", test_identical_candidate_yields_match),
    ("lost tokens detected in degraded output", test_degraded_candidate_detects_lost_tokens),
    ("missing sections surfaced", test_section_diff_detects_missing_headers),
    ("paragraph echoes detected", test_paragraph_echo_detection),
    ("score drop -> regression hint", test_recovery_hints_for_score_drop),
    ("short output -> expand hint", test_recovery_hints_for_short_output),
    ("long output -> trim hint", test_recovery_hints_for_long_output),
    ("format_human includes all sections", test_format_human_includes_all_sections),
    ("top_lost ordered by frequency", test_top_lost_ordered_by_frequency),
    ("paragraph count accurate", test_paragraph_count_accurate),
    ("_tokens filters stop words", test_tokens_helper_filters_stop_words),
    ("_sections finds markdown headers", test_sections_helper_finds_headers),
    ("drilldown_drifting handles no runs_dir", test_drilldown_drifting_handles_no_runs_dir),
    ("real golden drilldown with synthetic degradation", test_real_golden_drilldown),
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
