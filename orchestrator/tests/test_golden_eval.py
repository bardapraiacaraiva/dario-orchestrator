#!/usr/bin/env python3
"""Tests for Upgrade 7 golden eval / regression detection."""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from quality import golden_eval

# Use a sandbox eval id so we don't pollute real goldens
TEST_EVAL_ID = "test-eval-golden-xyz-123"


def _cleanup():
    for ext in (".golden.txt", ".golden.json"):
        f = golden_eval.GOLDEN_DIR / f"{TEST_EVAL_ID}{ext}"
        if f.exists():
            f.unlink()


def test_capture_creates_files():
    _cleanup()
    sample = "This is a golden output. It mentions posicionamento, archetype, and tom de voz. " * 5
    r = golden_eval.capture_golden(TEST_EVAL_ID, sample, human_score=88,
                                    notes="unit-test")
    assert r["status"] == "captured", f"got {r}"
    assert (golden_eval.GOLDEN_DIR / f"{TEST_EVAL_ID}.golden.txt").exists()
    assert (golden_eval.GOLDEN_DIR / f"{TEST_EVAL_ID}.golden.json").exists()
    _cleanup()


def test_capture_idempotent_unchanged():
    _cleanup()
    sample = "Same content twice"
    r1 = golden_eval.capture_golden(TEST_EVAL_ID, sample, human_score=80)
    r2 = golden_eval.capture_golden(TEST_EVAL_ID, sample, human_score=80)
    assert r1["status"] == "captured"
    assert r2["status"] == "unchanged", f"second capture should be unchanged: {r2}"
    _cleanup()


def test_capture_force_re_captures():
    _cleanup()
    sample = "Same content"
    golden_eval.capture_golden(TEST_EVAL_ID, sample, human_score=80)
    r = golden_eval.capture_golden(TEST_EVAL_ID, sample, human_score=80, force=True)
    assert r["status"] == "captured"
    assert r["version"] == 2, f"version should bump on force: {r['version']}"
    _cleanup()


def test_compare_no_golden_returns_status():
    _cleanup()
    r = golden_eval.compare_against_golden(TEST_EVAL_ID, "any candidate")
    assert r["status"] == "no_golden"


def test_compare_match_when_identical():
    _cleanup()
    sample = ("posicionamento marca premium boutique restaurant cascais "
              "archetype magician tom de voz sofisticado warm differentiation "
              "craftsmanship exclusivity story " * 5)
    golden_eval.capture_golden(TEST_EVAL_ID, sample, human_score=90)
    r = golden_eval.compare_against_golden(TEST_EVAL_ID, sample, candidate_score=90)
    # With identical content, lex jaccard = 1.0, length ratio = 1.0
    assert r["lexical_jaccard"] == 1.0
    assert r["length_ratio"] == 1.0
    assert r["score_delta"] == 0
    assert r["verdict"] in ("MATCH", "DEGRADED"), f"identical should match: {r}"
    _cleanup()


def test_compare_drift_score_delta():
    _cleanup()
    sample = ("posicionamento marca premium boutique restaurant cascais "
              "archetype magician tom de voz " * 5)
    golden_eval.capture_golden(TEST_EVAL_ID, sample, human_score=90)
    # Candidate scored 25 points lower
    r = golden_eval.compare_against_golden(TEST_EVAL_ID, sample, candidate_score=65)
    assert r["score_delta"] == -25
    assert r["drift_severity"] == "alert"
    assert any("score_drift" in f for f in r["flags"])
    _cleanup()


def test_compare_low_lexical_overlap():
    _cleanup()
    golden = "posicionamento marca premium archetype magician differentiation craftsmanship story"
    golden_eval.capture_golden(TEST_EVAL_ID, golden, human_score=90)
    # Totally different content
    candidate = "completely unrelated text about gardening planting flowers and watering"
    r = golden_eval.compare_against_golden(TEST_EVAL_ID, candidate, candidate_score=70)
    assert r["lexical_jaccard"] < golden_eval.LEXICAL_MIN
    assert r["verdict"] == "DRIFT"
    assert any("low_lexical_overlap" in f for f in r["flags"])
    _cleanup()


def test_compare_length_too_short():
    _cleanup()
    golden = "long detailed answer " * 50
    golden_eval.capture_golden(TEST_EVAL_ID, golden, human_score=85)
    candidate = "short"
    r = golden_eval.compare_against_golden(TEST_EVAL_ID, candidate, candidate_score=85)
    assert r["length_ratio"] < golden_eval.LENGTH_RATIO_MIN
    assert any("output_too_short" in f for f in r["flags"])
    _cleanup()


def test_compare_length_too_long():
    _cleanup()
    golden = "short answer"
    golden_eval.capture_golden(TEST_EVAL_ID, golden, human_score=85)
    candidate = "very long padded answer " * 200
    r = golden_eval.compare_against_golden(TEST_EVAL_ID, candidate, candidate_score=85)
    assert r["length_ratio"] > golden_eval.LENGTH_RATIO_MAX
    assert any("output_too_long" in f for f in r["flags"])
    _cleanup()


def test_calibration_log_appends():
    _cleanup()
    # Capture twice with different content, count log entries
    pre = golden_eval.calibration_status()
    pre_count = pre.get("total_entries", 0)
    golden_eval.capture_golden(TEST_EVAL_ID, "content one", human_score=80)
    golden_eval.capture_golden(TEST_EVAL_ID, "content two", human_score=82, force=False)
    # content two is different hash -> capture, not unchanged
    post = golden_eval.calibration_status()
    assert post["total_entries"] >= pre_count + 2, f"log not appending: {pre_count} -> {post['total_entries']}"
    _cleanup()


def test_list_goldens_returns_list():
    out = golden_eval.list_goldens()
    assert isinstance(out, list)


def test_token_filter_strips_stop_words():
    """Internal tokeniser used for jaccard — should ignore stop words."""
    tokens = golden_eval._tokens("the brand of the restaurant is premium")
    assert "the" not in tokens
    assert "of" not in tokens
    assert "brand" in tokens
    assert "restaurant" in tokens


TESTS = [
    ("capture creates files", test_capture_creates_files),
    ("capture idempotent on unchanged content", test_capture_idempotent_unchanged),
    ("capture --force bumps version", test_capture_force_re_captures),
    ("compare without golden returns no_golden", test_compare_no_golden_returns_status),
    ("identical content -> MATCH", test_compare_match_when_identical),
    ("score delta triggers drift alert", test_compare_drift_score_delta),
    ("low lexical overlap -> DRIFT", test_compare_low_lexical_overlap),
    ("length too short flagged", test_compare_length_too_short),
    ("length too long flagged", test_compare_length_too_long),
    ("calibration log appends", test_calibration_log_appends),
    ("list_goldens returns list", test_list_goldens_returns_list),
    ("token filter strips stop words", test_token_filter_strips_stop_words),
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
