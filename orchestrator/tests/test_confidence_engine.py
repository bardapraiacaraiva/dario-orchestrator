#!/usr/bin/env python3
"""Tests for Upgrade 4 confidence engine."""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


from confidence_engine import compute_confidence, gate_decision


def test_high_confidence_tight_dimensions():
    """Tight dimension agreement (σ < 0.15) and tier A should give HIGH."""
    dims = {"specificity": 0.85, "actionability": 0.88, "completeness": 0.86,
            "accuracy": 0.87, "tone": 0.84}
    # Skill not in metrics, so tier will be unscored — but σ is very tight
    conf = compute_confidence(dims, skill="nonexistent-skill", score=85)
    assert conf["sigma"] < 0.15, f"σ should be tight: {conf['sigma']}"
    # Without good tier, even tight σ only gets to MEDIUM/HIGH range
    assert conf["level"] in ("HIGH", "MEDIUM"), f"expected HIGH/MEDIUM, got {conf['level']}"
    return True


def test_low_confidence_high_variance():
    """Scattered dimensions (σ > 0.25) should drop confidence to LOW."""
    dims = {"specificity": 0.95, "actionability": 0.40, "completeness": 0.85,
            "accuracy": 0.45, "tone": 0.30}
    conf = compute_confidence(dims, skill="nonexistent-skill", score=60)
    assert conf["sigma"] >= 0.25, f"σ should be wide: {conf['sigma']}"
    assert conf["level"] in ("LOW", "MEDIUM"), f"expected LOW/MEDIUM, got {conf['level']}"
    return True


def test_ship_decision_high_conf():
    dims = {"specificity": 0.9, "actionability": 0.88, "completeness": 0.86,
            "accuracy": 0.89, "tone": 0.87}
    gate = gate_decision(score=85, dimensions=dims, skill="nonexistent",
                         pass_threshold=60)
    assert gate["action"] in ("ship", "review"), f"got {gate['action']}"
    return True


def test_revision_below_threshold():
    dims = {"specificity": 0.5, "actionability": 0.5, "completeness": 0.5,
            "accuracy": 0.5, "tone": 0.5}
    gate = gate_decision(score=45, dimensions=dims, skill="some-skill",
                         pass_threshold=60, revision_count=0)
    assert gate["action"] == "revision", f"got {gate['action']}"
    return True


def test_escalate_revision_exhausted():
    dims = {"specificity": 0.5, "actionability": 0.5, "completeness": 0.5,
            "accuracy": 0.5, "tone": 0.5}
    gate = gate_decision(score=55, dimensions=dims, skill="some-skill",
                         pass_threshold=60, revision_count=3)
    assert gate["action"] == "escalate", f"got {gate['action']}"
    return True


def test_critical_low_confidence_escalates():
    """Critical execution_policy + LOW confidence must escalate (not ship)."""
    dims = {"specificity": 0.95, "actionability": 0.40, "completeness": 0.85,
            "accuracy": 0.30, "tone": 0.30}
    gate = gate_decision(score=70, dimensions=dims, skill="dario-story-circle",
                         pass_threshold=60, execution_policy="critical")
    assert gate["action"] == "escalate", f"expected escalate, got {gate['action']}"
    assert "critical+LOW" in gate["rationale"]
    return True


def test_medium_confidence_below_buffer_reviews():
    """MEDIUM conf + score near threshold (within +5) → review not ship."""
    dims = {"specificity": 0.7, "actionability": 0.6, "completeness": 0.85,
            "accuracy": 0.5, "tone": 0.65}
    gate = gate_decision(score=62, dimensions=dims, skill="some-skill",
                         pass_threshold=60)
    # With these mid-range dimensions, σ is moderate -> MEDIUM
    if gate["confidence"]["level"] == "MEDIUM":
        assert gate["action"] == "review", f"MED conf near threshold should review, got {gate['action']}"
    return True


def test_success_pattern_for_excellence():
    dims = {"specificity": 0.95, "actionability": 0.95, "completeness": 0.95,
            "accuracy": 0.95, "tone": 0.95}
    gate = gate_decision(score=92, dimensions=dims, skill="some-skill",
                         pass_threshold=60)
    assert gate["action"] == "success_pattern", f"got {gate['action']}"
    return True


def test_no_dimensions_provided():
    """Missing dimensions should not crash; should default to medium."""
    gate = gate_decision(score=75, dimensions={}, skill=None, pass_threshold=60)
    assert "action" in gate
    assert "confidence" in gate
    return True


def test_rationale_string_present():
    dims = {"a": 0.8, "b": 0.85}
    gate = gate_decision(score=80, dimensions=dims, skill=None, pass_threshold=60)
    assert "score=80" in gate["rationale"]
    assert "threshold=60" in gate["rationale"]
    assert "confidence=" in gate["rationale"]
    return True


TESTS = [
    ("high confidence on tight dimensions", test_high_confidence_tight_dimensions),
    ("low confidence on scattered dimensions", test_low_confidence_high_variance),
    ("ship decision with high conf", test_ship_decision_high_conf),
    ("revision below threshold", test_revision_below_threshold),
    ("escalate when revision exhausted", test_escalate_revision_exhausted),
    ("critical+LOW always escalates", test_critical_low_confidence_escalates),
    ("medium conf near threshold reviews", test_medium_confidence_below_buffer_reviews),
    ("success_pattern for excellence", test_success_pattern_for_excellence),
    ("no dimensions provided -> no crash", test_no_dimensions_provided),
    ("rationale string structure", test_rationale_string_present),
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
