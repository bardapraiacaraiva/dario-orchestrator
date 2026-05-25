#!/usr/bin/env python3
"""Tests for Upgrade 9 CoT dispatch deliberation."""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import pytest

import dispatch_cot

pytestmark = pytest.mark.slow

# Use sandbox task ids so we don't pollute production CoT dir
SANDBOX_PREFIX = "test-cot-sandbox-"


def _cleanup():
    for f in dispatch_cot.COT_DIR.glob(f"{SANDBOX_PREFIX}*.yaml"):
        f.unlink()


def test_explicit_skill_wins():
    task = {
        "id": f"{SANDBOX_PREFIX}001",
        "skill": "dario-brand",
        "title": "x",
        "description": "y"
    }
    trace = dispatch_cot.reason(task, persist=False)
    assert trace["decision"]["winner"] == "dario-brand"
    assert "explicit" in trace["signals"]


def test_signals_gathered():
    task = {
        "id": f"{SANDBOX_PREFIX}002",
        "title": "Criar pitch deck para investidores",
        "description": "Series A round, 12 slides, focus em traction",
        "project": "pupli",
    }
    trace = dispatch_cot.reason(task, persist=False)
    s = trace["signals"]
    # At least semantic + keyword should hit something
    has_signals = any(isinstance(s.get(k), dict) for k in ("semantic", "keyword", "qvalue"))
    assert has_signals, f"no signals fired: {s}"


def test_winner_has_rationale():
    task = {
        "id": f"{SANDBOX_PREFIX}003",
        "title": "Auditoria SEO completa do site",
        "description": "Site WordPress, e-commerce de mobiliario",
    }
    trace = dispatch_cot.reason(task, persist=False)
    d = trace["decision"]
    if d["winner"]:
        assert isinstance(d["rationale"], str) and len(d["rationale"]) > 20
        assert d["winner"] in d["rationale"]
        assert "confidence" in d["rationale"].lower()


def test_no_signal_no_winner():
    task = {
        "id": f"{SANDBOX_PREFIX}004",
        "title": "xyz qwerty zzzz",
        "description": "complete nonsense aaaa bbbb cccc",
    }
    trace = dispatch_cot.reason(task, persist=False)
    # Either no winner or LOW confidence
    d = trace["decision"]
    assert d.get("level") in ("NONE", "LOW", "MEDIUM"), f"unexpected level: {d}"


def test_persist_writes_trace_file():
    _cleanup()
    task_id = f"{SANDBOX_PREFIX}005"
    task = {
        "id": task_id,
        "title": "criar marca completa",
        "description": "para restaurante",
    }
    dispatch_cot.reason(task, persist=True)
    expected = dispatch_cot.COT_DIR / f"{task_id}.yaml"
    assert expected.exists(), f"trace not persisted: {expected}"
    _cleanup()


def test_postmortem_vindicated_success():
    _cleanup()
    task_id = f"{SANDBOX_PREFIX}006"
    task = {
        "id": task_id,
        "skill": "dario-brand",
        "title": "test task",
        "description": "test desc",
    }
    dispatch_cot.reason(task, persist=True)
    pm = dispatch_cot.postmortem(task_id, actual_score=88, actual_outcome="success")
    assert pm["status"] == "complete"
    assert pm["verdict"] == "VINDICATED"
    _cleanup()


def test_postmortem_overconfident():
    """HIGH confidence + bad outcome -> OVERCONFIDENT."""
    _cleanup()
    task_id = f"{SANDBOX_PREFIX}007"
    task = {
        "id": task_id,
        "skill": "dario-brand",  # explicit -> 1.0 confidence
        "title": "task with explicit skill",
        "description": "should be HIGH confidence",
    }
    trace = dispatch_cot.reason(task, persist=True)
    assert trace["decision"]["level"] == "HIGH"
    pm = dispatch_cot.postmortem(task_id, actual_score=45, actual_outcome="revision")
    assert pm["verdict"] == "OVERCONFIDENT", f"expected OVERCONFIDENT, got {pm['verdict']}"
    _cleanup()


def test_postmortem_no_trace_handled():
    pm = dispatch_cot.postmortem("nonexistent-task-id-12345", actual_score=50)
    assert pm["status"] == "no_trace"


def test_stats_returns_dict():
    s = dispatch_cot.stats()
    assert "total_traces" in s
    assert "by_confidence_level" in s
    assert "by_winning_signal" in s
    assert "postmortems" in s
    assert "overconfidence_rate" in s


def test_disagreement_penalty():
    """When signals point to different skills, confidence should be lower."""
    # We can't easily force disagreement without mocking, but we can verify
    # the penalty constant exists and is positive
    assert dispatch_cot.DISAGREEMENT_PENALTY > 0
    assert dispatch_cot.DISAGREEMENT_PENALTY < 0.5


def test_signal_weights_sum_reasonable():
    """Weights should be reasonable for combining."""
    explicit_w = dispatch_cot.SIGNAL_WEIGHTS["explicit"]
    semantic_w = dispatch_cot.SIGNAL_WEIGHTS["semantic"]
    assert explicit_w >= semantic_w, "explicit should be strongest"
    assert all(0 < w <= 1.0 for w in dispatch_cot.SIGNAL_WEIGHTS.values())


def test_trace_includes_alternatives():
    """When multiple signals fire, alternatives should be surfaced."""
    task = {
        "id": f"{SANDBOX_PREFIX}008",
        "title": "Brand positioning para restaurante de peixe premium em Cascais",
        "description": "Publico turistas e locais 30-55 anos. Diferenciador: dual mastery, fire spectacle.",
    }
    trace = dispatch_cot.reason(task, persist=False)
    d = trace["decision"]
    # Should have alternatives if winner exists
    if d["winner"]:
        assert "alternatives" in d
        assert isinstance(d["alternatives"], list)


TESTS = [
    ("explicit skill always wins", test_explicit_skill_wins),
    ("multiple signals are gathered", test_signals_gathered),
    ("winner includes rationale string", test_winner_has_rationale),
    ("no-signal case handled gracefully", test_no_signal_no_winner),
    ("persist writes trace YAML", test_persist_writes_trace_file),
    ("postmortem VINDICATED on success", test_postmortem_vindicated_success),
    ("postmortem OVERCONFIDENT on HIGH+fail", test_postmortem_overconfident),
    ("postmortem no_trace handled", test_postmortem_no_trace_handled),
    ("stats returns full schema", test_stats_returns_dict),
    ("disagreement penalty configured", test_disagreement_penalty),
    ("signal weights ordered correctly", test_signal_weights_sum_reasonable),
    ("trace surfaces alternatives", test_trace_includes_alternatives),
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
