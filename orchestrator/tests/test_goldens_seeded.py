#!/usr/bin/env python3
"""Tests for U11 seeded goldens — verifies the 12 eval cases have captured
references, all goldens roundtrip cleanly, and the canonical seed list matches
eval_suite.EVAL_CASES.
"""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import golden_eval
from tools import seed_goldens


def test_all_eval_cases_have_golden():
    """Every EVAL_CASES entry in eval_suite must have a seeded golden."""
    from eval_suite import EVAL_CASES
    eval_ids = {c["id"] for c in EVAL_CASES}
    captured = {g["eval_id"] for g in golden_eval.list_goldens()}
    missing = eval_ids - captured
    assert not missing, f"missing goldens: {missing}"
    return True


def test_seed_list_matches_eval_suite():
    """The seed_goldens GOLDENS list should cover every EVAL_CASES entry."""
    from eval_suite import EVAL_CASES
    eval_ids = {c["id"] for c in EVAL_CASES}
    seed_ids = {eid for eid, _, _, _ in seed_goldens.GOLDENS}
    not_seeded = eval_ids - seed_ids
    assert not not_seeded, f"eval cases without seed entry: {not_seeded}"
    extra = seed_ids - eval_ids
    assert not extra, f"seed entries with no matching eval: {extra}"
    return True


def test_human_scores_in_reasonable_range():
    """Every seeded golden should have human_score in [70, 95]."""
    for eval_id, score, text, notes in seed_goldens.GOLDENS:
        assert 70 <= score <= 95, f"{eval_id} human_score={score} outside [70,95]"
    return True


def test_seeded_goldens_meet_minimum_length():
    """Each golden should match or exceed the min_length declared in its eval case."""
    from eval_suite import EVAL_CASES
    case_lookup = {c["id"]: c for c in EVAL_CASES}
    for eval_id, score, text, notes in seed_goldens.GOLDENS:
        case = case_lookup.get(eval_id)
        if not case:
            continue
        min_len = case.get("min_length", 0)
        assert len(text) >= min_len, (
            f"{eval_id} golden length {len(text)} < min_length {min_len}"
        )
    return True


def test_seeded_goldens_contain_expected_keywords():
    """Each golden should contain at least 50% of its eval's expected_keywords."""
    from eval_suite import EVAL_CASES
    case_lookup = {c["id"]: c for c in EVAL_CASES}
    for eval_id, score, text, notes in seed_goldens.GOLDENS:
        case = case_lookup.get(eval_id)
        if not case:
            continue
        kws = case.get("expected_keywords", [])
        if not kws:
            continue
        text_lower = text.lower()
        found = sum(1 for k in kws if k.lower() in text_lower)
        ratio = found / len(kws)
        assert ratio >= 0.50, (
            f"{eval_id} only {found}/{len(kws)} expected keywords present ({ratio:.0%})"
        )
    return True


def test_self_comparison_yields_match():
    """Each golden compared against itself MUST be a perfect MATCH."""
    for g in golden_eval.list_goldens():
        text_file = golden_eval.GOLDEN_DIR / f"{g['eval_id']}.golden.txt"
        if not text_file.exists():
            continue
        text = text_file.read_text(encoding="utf-8")
        r = golden_eval.compare_against_golden(
            g["eval_id"], text, candidate_score=g["human_score"]
        )
        assert r["verdict"] == "MATCH", (
            f"{g['eval_id']} self-comparison verdict={r['verdict']}"
        )
        assert r["lexical_jaccard"] == 1.0
        assert r["score_delta"] == 0
    return True


def test_calibration_log_has_entries():
    """Calibration log should have entries from the seed run."""
    status = golden_eval.calibration_status()
    assert status["total_entries"] >= 12, (
        f"only {status['total_entries']} calibration entries"
    )
    return True


def test_drift_simulation_triggers_alert():
    """If a candidate has a 15pt score drop, regression detection should alert."""
    sample = golden_eval.list_goldens()[0]
    text_file = golden_eval.GOLDEN_DIR / f"{sample['eval_id']}.golden.txt"
    text = text_file.read_text(encoding="utf-8")
    r = golden_eval.compare_against_golden(
        sample["eval_id"], text, candidate_score=sample["human_score"] - 15
    )
    assert r["drift_severity"] == "alert"
    assert r["verdict"] in ("DRIFT", "DEGRADED")
    return True


TESTS = [
    ("all eval cases have golden seeded", test_all_eval_cases_have_golden),
    ("seed list matches eval_suite", test_seed_list_matches_eval_suite),
    ("human scores in [70,95]", test_human_scores_in_reasonable_range),
    ("seeded goldens meet min_length", test_seeded_goldens_meet_minimum_length),
    ("seeded goldens cover keywords", test_seeded_goldens_contain_expected_keywords),
    ("self-comparison yields MATCH", test_self_comparison_yields_match),
    ("calibration log has entries", test_calibration_log_has_entries),
    ("15pt drift triggers alert", test_drift_simulation_triggers_alert),
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
