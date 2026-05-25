#!/usr/bin/env python3
"""Tests for Upgrade 10 dynamic chain branching."""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


from cognitive import dynamic_branch as db


def test_excellence_foundational_continues_serial():
    """dario-brand is foundational; even with excellence, stay serial."""
    r = db.decide_next_action("brand_to_market", 0, score=92)
    assert r["action"] == db.CONTINUE_SERIAL
    assert r["next_steps"] == [1]
    assert r["metadata"].get("foundational") is True


def test_below_gate_triggers_revision():
    r = db.decide_next_action("brand_to_market", 0, score=55, revision_count=0)
    assert r["action"] == db.REVISION_LOOP
    assert r["next_steps"] == [0]
    assert r["metadata"]["revision_count"] == 1


def test_revision_exhausted_escalates():
    r = db.decide_next_action("brand_to_market", 0, score=55, revision_count=1)
    assert r["action"] == db.ESCALATE


def test_catastrophic_first_attempt_escalates():
    r = db.decide_next_action("brand_to_market", 1, score=25)
    assert r["action"] == db.ESCALATE


def test_catastrophic_after_revision_stops():
    r = db.decide_next_action("brand_to_market", 1, score=25, revision_count=1)
    assert r["action"] == db.EARLY_STOP


def test_low_confidence_escalates_even_with_good_score():
    r = db.decide_next_action("brand_to_market", 1, score=80,
                               confidence_level="LOW", dimension_variance=0.35)
    assert r["action"] == db.ESCALATE
    assert "LOW" in r["rationale"]


def test_excellence_non_foundational_parallelizes():
    """At step 2 (dario-offer), score 90 + steps 3+4 likely independent -> parallel."""
    r = db.decide_next_action("brand_to_market", 2, score=90)
    # dario-offer is NOT in FOUNDATIONAL_SKILLS, so excellence may parallelize
    # if steps 3 and 4 are independent (sales-letter and email-seq)
    assert r["action"] in (db.PARALLELIZE_NEXT, db.CONTINUE_SERIAL)


def test_last_step_terminal():
    """The 5th step (index 4) of brand_to_market is the last."""
    r = db.decide_next_action("brand_to_market", 4, score=85)
    assert r["action"] == db.CONTINUE_SERIAL
    assert r["metadata"]["terminal"] is True


def test_unknown_chain_escalates():
    r = db.decide_next_action("nonexistent_chain", 0, score=90)
    assert r["action"] == db.ESCALATE
    assert "not found" in r["rationale"]


def test_step_out_of_range():
    r = db.decide_next_action("brand_to_market", 99, score=85)
    assert r["action"] == db.EARLY_STOP


def test_decision_is_pure_function():
    """Same inputs must produce same output (no hidden state)."""
    r1 = db.decide_next_action("brand_to_market", 0, score=85)
    r2 = db.decide_next_action("brand_to_market", 0, score=85)
    assert r1["action"] == r2["action"]
    assert r1["next_steps"] == r2["next_steps"]


def test_rationale_includes_score_and_decision():
    r = db.decide_next_action("brand_to_market", 1, score=82)
    assert "82" in r["rationale"]
    assert isinstance(r["rationale"], str)


def test_steps_independent_helper():
    """Manual check of independence detection."""
    step_a = {"pass_to_next": ["headline", "lead", "body", "cta"]}
    step_b = {"receives": "oferta + sales letter + tom de voz"}
    # step_b mentions "letter" but not headline/lead/body/cta directly
    # The function checks if ANY of a's fields appear in b's receives string
    # "headline" not in receives, "lead" not in receives... none match
    assert db._steps_independent(step_a, step_b) is True

    step_b2 = {"receives": "headline plus lead from previous step"}
    assert db._steps_independent(step_a, step_b2) is False


def test_revision_metadata_increments():
    r = db.decide_next_action("brand_to_market", 0, score=60, revision_count=0)
    assert r["action"] == db.REVISION_LOOP
    assert r["metadata"]["revision_count"] == 1


TESTS = [
    ("excellence on foundational skill = continue serial", test_excellence_foundational_continues_serial),
    ("below gate triggers revision loop", test_below_gate_triggers_revision),
    ("revision exhausted = escalate", test_revision_exhausted_escalates),
    ("catastrophic first attempt = escalate", test_catastrophic_first_attempt_escalates),
    ("catastrophic after revision = early stop", test_catastrophic_after_revision_stops),
    ("LOW confidence + good score = escalate", test_low_confidence_escalates_even_with_good_score),
    ("excellence + non-foundational allows parallelize", test_excellence_non_foundational_parallelizes),
    ("last step is terminal", test_last_step_terminal),
    ("unknown chain escalates", test_unknown_chain_escalates),
    ("step out of range early-stops", test_step_out_of_range),
    ("decision is pure (deterministic)", test_decision_is_pure_function),
    ("rationale includes score", test_rationale_includes_score_and_decision),
    ("steps independence helper correct", test_steps_independent_helper),
    ("revision metadata increments", test_revision_metadata_increments),
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
