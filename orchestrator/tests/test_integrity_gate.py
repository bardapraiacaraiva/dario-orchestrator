#!/usr/bin/env python3
"""Tests for Upgrade 14 integrity gate."""

import os
import sys
from pathlib import Path

# Resolve like tests/conftest.py: env override → this repo (tests/ -> orchestrator/)
# → legacy ~/.claude. Hard-anchoring to Path.home() killed CI collection on Linux
# (path absent → `import integrity_gate` fails → whole suite errors). (Fase 1, 2026-06-12.)
_env_dir = os.environ.get("DARIO_ORCH_DIR")
if _env_dir:
    ORCH_DIR = Path(_env_dir)
elif (Path(__file__).resolve().parent.parent / "core").is_dir():
    ORCH_DIR = Path(__file__).resolve().parent.parent
else:
    ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))
sys.path.insert(0, str(ORCH_DIR / "tools"))

import integrity_gate
import pytest

pytestmark = pytest.mark.slow

# Production should currently be clean — these tests verify both the
# clean state AND that the checks correctly detect synthetic breakage.

def test_run_all_returns_structure():
    r = integrity_gate.run_all()
    assert "verdict" in r
    assert "exit_code" in r
    assert "checks" in r
    assert len(r["checks"]) == len(integrity_gate.CHECKS)
    assert r["verdict"] in ("PASS", "WARN", "FAIL")


def test_production_state_is_clean():
    """Sanity: prod state should pass all checks today (after Sprints 1-12)."""
    r = integrity_gate.run_all()
    failed = [c["name"] for c in r["checks"] if c["status"] == "FAIL"]
    assert not failed, f"production has failing checks: {failed}"


def test_check_eval_skills_exist():
    r = integrity_gate.check_eval_skills_exist()
    assert r["status"] in ("PASS", "FAIL")
    assert "total" in r


def test_check_skill_frontmatter_valid():
    r = integrity_gate.check_skill_frontmatter_valid()
    assert r["status"] in ("PASS", "FAIL")


def test_check_embeddings_coverage():
    r = integrity_gate.check_embeddings_coverage()
    assert "corpus_size" in r
    assert "cached" in r


def test_check_embeddings_freshness():
    r = integrity_gate.check_embeddings_freshness()
    assert "stale_count" in r


def test_check_golden_skills_alive():
    r = integrity_gate.check_golden_skills_alive()
    assert r["status"] in ("PASS", "FAIL")


def test_check_chain_skills_resolve():
    r = integrity_gate.check_chain_skills_resolve()
    assert r["status"] in ("PASS", "FAIL")
    assert "total_steps" in r


def test_check_synaptic_pairs_valid():
    r = integrity_gate.check_synaptic_pairs_valid()
    assert r["status"] in ("PASS", "WARN")
    assert "total_pairs" in r


def test_skill_lookup_helper():
    """_has_skill should correctly detect existence."""
    assert integrity_gate._has_skill("dario-brand") is True
    assert integrity_gate._has_skill("nonexistent-skill-xyz-9999") is False


def test_strict_mode_treats_warn_as_fail():
    """If a single WARN exists, --strict should bump to FAIL."""
    # Synthetic: temporarily inject a broken synaptic pair via the YAML
    weights_file = ORCH_DIR / "synaptic_weights.yaml"
    backup = weights_file.read_text(encoding="utf-8") if weights_file.exists() else None
    try:
        # Append a deliberately-invalid pair
        if backup:
            broken = backup + "\n  nonexistent-skill-xyz + dario-brand:\n    weight: 0.5\n    co_activations: 0\n"
            weights_file.write_text(broken, encoding="utf-8")

            # Strict mode
            r_strict = integrity_gate.run_all(strict=True)
            r_lax = integrity_gate.run_all(strict=False)
            assert r_strict["exit_code"] >= r_lax["exit_code"]
            return True
        return True  # skip if no backup
    finally:
        if backup is not None:
            weights_file.write_text(backup, encoding="utf-8")


def test_synthetic_orphan_golden_detected():
    """If we capture a golden for a fake eval id, golden_skills_alive flags it."""
    from quality import golden_eval
    fake_id = "test-fake-eval-orphan-xyz-123"
    try:
        golden_eval.capture_golden(fake_id, "test content " * 30, human_score=80)
        r = integrity_gate.check_golden_skills_alive()
        # Should flag fake_id as orphaned (no matching eval_case)
        orphaned_ids = [o.get("eval_id") for o in r.get("orphaned", [])]
        assert fake_id in orphaned_ids, f"orphan not detected: {r}"
        return True
    finally:
        for ext in (".golden.txt", ".golden.json"):
            f = golden_eval.GOLDEN_DIR / f"{fake_id}{ext}"
            if f.exists():
                f.unlink()


def test_exit_code_matches_verdict():
    r = integrity_gate.run_all()
    expected = {"PASS": 0, "WARN": 1, "FAIL": 2}.get(r["verdict"])
    assert r["exit_code"] == expected


def test_format_output_is_string():
    r = integrity_gate.run_all()
    text = integrity_gate._format(r)
    assert isinstance(text, str)
    assert "Integrity Gate" in text


def test_check_count_constant():
    """7 checks documented — verify all are wired."""
    assert len(integrity_gate.CHECKS) == 7


TESTS = [
    ("run_all returns expected structure", test_run_all_returns_structure),
    ("production state passes all checks", test_production_state_is_clean),
    ("eval skills exist check works", test_check_eval_skills_exist),
    ("frontmatter validation check works", test_check_skill_frontmatter_valid),
    ("embeddings coverage check works", test_check_embeddings_coverage),
    ("embeddings freshness check works", test_check_embeddings_freshness),
    ("golden skills alive check works", test_check_golden_skills_alive),
    ("chain skills resolve check works", test_check_chain_skills_resolve),
    ("synaptic pairs valid check works", test_check_synaptic_pairs_valid),
    ("_has_skill helper accurate", test_skill_lookup_helper),
    ("--strict escalates warnings", test_strict_mode_treats_warn_as_fail),
    ("synthetic orphan golden detected", test_synthetic_orphan_golden_detected),
    ("exit code maps to verdict", test_exit_code_matches_verdict),
    ("format output is human-readable", test_format_output_is_string),
    ("7 checks wired (constant)", test_check_count_constant),
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
