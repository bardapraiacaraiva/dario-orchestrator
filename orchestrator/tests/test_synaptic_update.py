#!/usr/bin/env python3
"""Tests for Upgrade 3 synaptic weights write-back."""

import shutil
import sys
import tempfile
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import synaptic_update


def with_isolated_weights(test_fn):
    """Run test against a copy of synaptic_weights.yaml (no production impact)."""
    original = ORCH_DIR / "synaptic_weights.yaml"
    backup = ORCH_DIR / "synaptic_weights.yaml.test-backup"
    shutil.copy(original, backup)
    try:
        return test_fn()
    finally:
        shutil.copy(backup, original)
        backup.unlink()


def test_simulate_new_pair():
    delta = synaptic_update.update_pair("dario-pitch", "dario-naming", 88, 92, simulate=True)
    assert delta["pair"] == "dario-naming + dario-pitch", f"canonical key wrong: {delta['pair']}"
    assert delta["combined_avg"] == 90.0, f"combined avg wrong: {delta['combined_avg']}"
    assert delta["rule_applied"] == "success_increment", f"rule wrong: {delta['rule_applied']}"
    assert delta["new_weight"] > delta["old_weight"], "weight should increase"
    return True


def test_simulate_existing_pair_success():
    # dario-brand + dario-content exists with weight 0.55
    delta = synaptic_update.update_pair("dario-brand", "dario-content", 90, 90, simulate=True)
    assert delta["old_weight"] == 0.55
    assert delta["new_weight"] == 0.60
    assert delta["rule_applied"] == "success_increment"
    return True


def test_simulate_existing_pair_failure():
    delta = synaptic_update.update_pair("dario-brand", "dario-content", 40, 45, simulate=True)
    assert delta["rule_applied"] == "failure_decrement"
    assert delta["new_weight"] < delta["old_weight"]
    return True


def test_simulate_no_change_midrange():
    delta = synaptic_update.update_pair("dario-brand", "dario-content", 70, 75, simulate=True)
    assert delta["rule_applied"] == "no_change"
    assert delta["new_weight"] == delta["old_weight"]
    return True


def test_canonical_key_symmetry():
    a = synaptic_update.update_pair("seo-audit", "seo-plan", 85, 85, simulate=True)
    b = synaptic_update.update_pair("seo-plan", "seo-audit", 85, 85, simulate=True)
    assert a["pair"] == b["pair"], "pair key not canonical (alphabetical)"
    return True


def test_write_persists():
    """Run with isolated weights file — verify write actually persists."""
    def inner():
        before = synaptic_update._load_weights()
        before_weight = before["affinity_graph"].get("dario-brand + dario-content", {}).get("weight", 0.5)
        synaptic_update.update_pair("dario-brand", "dario-content", 92, 92, simulate=False)
        after = synaptic_update._load_weights()
        after_weight = after["affinity_graph"]["dario-brand + dario-content"]["weight"]
        assert after_weight > before_weight, f"write did not persist: {before_weight} -> {after_weight}"
        assert after["affinity_graph"]["dario-brand + dario-content"]["co_activations"] == \
               before["affinity_graph"]["dario-brand + dario-content"]["co_activations"] + 1
        return True
    return with_isolated_weights(inner)


def test_self_pair_ignored():
    delta = synaptic_update.update_pair("dario-brand", "dario-brand", 90, 90, simulate=True)
    assert delta["rule_applied"] == "self_pair_ignored"
    assert delta["pair"] is None
    return True


def test_weight_capped():
    """Weight should not exceed max_weight."""
    def inner():
        # diva-moodboard + diva-materials starts at 1.0 (already at cap)
        delta = synaptic_update.update_pair("diva-moodboard", "diva-materials", 95, 95, simulate=False)
        assert delta["new_weight"] <= 1.0, f"weight exceeded cap: {delta['new_weight']}"
        return True
    return with_isolated_weights(inner)


def test_stats_returns_metrics():
    s = synaptic_update.stats()
    assert "total_pairs" in s
    assert "active_pairs" in s
    assert "avg_weight" in s
    assert s["total_pairs"] > 0
    return True


TESTS = [
    ("simulate new pair", test_simulate_new_pair),
    ("simulate existing pair (success)", test_simulate_existing_pair_success),
    ("simulate existing pair (failure)", test_simulate_existing_pair_failure),
    ("simulate no-change midrange", test_simulate_no_change_midrange),
    ("canonical key symmetry", test_canonical_key_symmetry),
    ("write persists (isolated)", test_write_persists),
    ("self-pair ignored", test_self_pair_ignored),
    ("weight capped at max", test_weight_capped),
    ("stats returns metrics", test_stats_returns_metrics),
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
