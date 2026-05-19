#!/usr/bin/env python3
"""Tests for Upgrade 6 chain validation gates."""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from chain_validator import (
    validate_step_output, validate_full_chain, list_chains, _load_chains
)


def test_chains_loaded():
    chains = _load_chains()
    assert len(chains) > 0, "no chains loaded"
    assert "brand_to_market" in chains, "expected brand_to_market chain"
    return True


def test_step_with_all_fields_passes():
    artifact = {
        "posicionamento": "Premium boutique brand",
        "archetype": "Magician",
        "tom_de_voz": "Sophisticated yet warm",
        "diferenciadores": ["craftsmanship", "exclusivity", "story"],
    }
    r = validate_step_output("brand_to_market", 0, artifact)
    assert r["valid"] is True, f"expected valid, got {r}"
    assert r["verdict"] == "PASS"
    assert r["missing"] == []
    return True


def test_step_with_missing_fields():
    artifact = {
        "posicionamento": "X",
        # archetype, tom_de_voz, diferenciadores missing
    }
    r = validate_step_output("brand_to_market", 0, artifact)
    assert r["valid"] is False
    assert "archetype" in r["missing"]
    assert r["verdict"] in ("INCOMPLETE", "EMPTY")
    assert r["escalation"] is not None
    return True


def test_step_with_empty_artifact():
    r = validate_step_output("brand_to_market", 0, {})
    assert r["verdict"] == "EMPTY"
    assert r["valid"] is False
    return True


def test_terminal_step_has_no_pass_to_next():
    """Last step of brand_to_market has pass_to_next: null."""
    # brand_to_market step 4 = dario-email-seq, pass_to_next=null
    r = validate_step_output("brand_to_market", 4, {"some": "output"})
    assert r["verdict"] == "TERMINAL"
    assert r["valid"] is True
    return True


def test_unknown_chain():
    r = validate_step_output("nonexistent_chain", 0, {"x": 1})
    assert r["verdict"] == "UNKNOWN_CHAIN"
    assert r["valid"] is False
    return True


def test_step_out_of_range():
    r = validate_step_output("brand_to_market", 99, {"x": 1})
    assert r["verdict"] == "STEP_OUT_OF_RANGE"
    assert r["valid"] is False
    return True


def test_string_artifact_substring_match():
    """If artifact is raw text, fields are checked as substrings."""
    artifact = "We propose the posicionamento as: Premium. The archetype is Magician. tom_de_voz: sophisticated. diferenciadores: craft, story."
    r = validate_step_output("brand_to_market", 0, artifact)
    # All four fields appear in the text
    assert r["valid"] is True, f"text substring matching failed: {r}"
    return True


def test_partial_string_artifact():
    artifact = "We propose the posicionamento: Premium. Nothing else."
    r = validate_step_output("brand_to_market", 0, artifact)
    assert r["verdict"] == "INCOMPLETE"
    assert "archetype" in r["missing"]
    return True


def test_none_values_treated_as_missing():
    artifact = {
        "posicionamento": None,
        "archetype": "",
        "tom_de_voz": [],
        "diferenciadores": "x",
    }
    r = validate_step_output("brand_to_market", 0, artifact)
    assert "posicionamento" in r["missing"]
    assert "archetype" in r["missing"]
    assert "tom_de_voz" in r["missing"]
    assert "diferenciadores" in r["present"]
    return True


def test_full_chain_validation_aggregate():
    """Walk through every step of a chain with mixed artifacts."""
    artifacts = [
        {"posicionamento": "X", "archetype": "Y", "tom_de_voz": "Z", "diferenciadores": ["d"]},
        {"nome_escolhido": "BrandName", "dominio": "brand.com"},
        {"oferta_completa": "...", "pricing": "...", "bonuses": "...", "garantia": "..."},
        {"headline": "h", "lead": "l", "body": "b", "cta": "c"},
        {"final": "emails"},  # terminal — no fields required
    ]
    r = validate_full_chain("brand_to_market", artifacts)
    assert r["valid"] is True, f"full chain should validate: {r}"
    assert r["total_steps"] == 5
    return True


def test_list_chains_returns_structure():
    s = list_chains()
    assert isinstance(s, dict)
    assert "brand_to_market" in s
    assert "steps" in s["brand_to_market"]
    return True


TESTS = [
    ("chains loaded from yaml", test_chains_loaded),
    ("step with all fields passes", test_step_with_all_fields_passes),
    ("step with missing fields incomplete", test_step_with_missing_fields),
    ("empty artifact = EMPTY verdict", test_step_with_empty_artifact),
    ("terminal step skips validation", test_terminal_step_has_no_pass_to_next),
    ("unknown chain handled", test_unknown_chain),
    ("step out of range handled", test_step_out_of_range),
    ("string artifact substring match", test_string_artifact_substring_match),
    ("partial string artifact", test_partial_string_artifact),
    ("None/empty values treated missing", test_none_values_treated_as_missing),
    ("full chain validation aggregate", test_full_chain_validation_aggregate),
    ("list_chains structure", test_list_chains_returns_structure),
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
