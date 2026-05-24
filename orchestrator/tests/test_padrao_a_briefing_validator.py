"""Tests for Padrão A briefing validator (Tier 2 pre-flight check)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from scripts.padrao_a_briefing_validator import (
    InputCheck,
    ValidationResult,
    check_input,
    load_validators_config,
    render_human,
    validate_briefing,
)


# ─────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────

RICH_BRAND_BRIEFING = (
    "Cuidaí brand positioning workshop. Target audience: HNW caregivers BR. "
    "Compete com Famileo (260K families) e CaringBridge. Tom premium e "
    "trustworthy. Differential: BR-native LGPD-saude. Archetype hint: caregiver."
)

RICH_SALES_LETTER_BRIEFING = (
    "Landing hero + body para SAQUEI relatorio. Customers: 8000+ users que "
    "ja compraram. NPS 67. Pricing R$ 29 single report + R$ 19/mes subscription. "
    "Garantia 14 dias money-back. Audience: solution-aware brasileiros 30-55. "
    "Persona: pai de familia procurando dinheiro esquecido no CPF."
)

SPARSE_BRAND_BRIEFING = "Brand positioning para uma startup"
SPARSE_SALES_LETTER_BRIEFING = "Copy para landing page"


# ─────────────────────────────────────────────────────────────────────
# Config loader tests
# ─────────────────────────────────────────────────────────────────────

class TestConfigLoading:

    def test_config_loads(self):
        cfg = load_validators_config()
        assert "validators" in cfg
        assert "tier_1_no_validation_required" in cfg

    def test_both_tier_2_workers_present(self):
        cfg = load_validators_config()
        validators = cfg["validators"]
        assert "worker-brand" in validators
        assert "worker-sales-letter" in validators

    def test_tier_1_workers_listed(self):
        cfg = load_validators_config()
        tier_1 = cfg["tier_1_no_validation_required"]
        for w in ("worker-pitch", "worker-offer", "worker-funnel",
                  "worker-product", "worker-wp-audit", "worker-financial-model"):
            assert w in tier_1, f"{w} missing from tier_1 list"

    def test_brand_has_required_inputs(self):
        cfg = load_validators_config()
        brand = cfg["validators"]["worker-brand"]
        assert "competitive_context" in brand["required_inputs"]
        assert "tone_target" in brand["required_inputs"]

    def test_sales_letter_has_required_inputs(self):
        cfg = load_validators_config()
        sl = cfg["validators"]["worker-sales-letter"]
        for name in ("testimonials_or_proof", "offer_terms", "audience_awareness"):
            assert name in sl["required_inputs"], f"{name} missing"


# ─────────────────────────────────────────────────────────────────────
# Brand validation tests
# ─────────────────────────────────────────────────────────────────────

class TestBrandValidation:

    def test_rich_brand_briefing_passes(self):
        r = validate_briefing("worker-brand", RICH_BRAND_BRIEFING)
        assert r.passed, f"Rich briefing should pass. Missing: {[c.name for c in r.missing_required]}"
        assert r.is_tier_2

    def test_sparse_brand_briefing_fails(self):
        r = validate_briefing("worker-brand", SPARSE_BRAND_BRIEFING)
        assert not r.passed
        assert len(r.missing_required) >= 1

    def test_brand_competitor_keyword_detected(self):
        briefing = "We compete with X and Y in the SMB market"
        r = validate_briefing("worker-brand", briefing)
        comp = next(c for c in r.required_checks if c.name == "competitive_context")
        assert comp.passed
        assert "compete" in comp.matched_keywords or "compete with" in comp.matched_keywords

    def test_brand_tone_keyword_detected(self):
        briefing = "We need to compete vs incumbents. Target persona: C-level executives."
        r = validate_briefing("worker-brand", briefing)
        tone = next(c for c in r.required_checks if c.name == "tone_target")
        assert tone.passed

    def test_brand_optional_archetype_recognized(self):
        briefing = "Compete with X. Target HNW. Archetype: hero with caring undertones."
        r = validate_briefing("worker-brand", briefing)
        arch = next(c for c in r.optional_checks if c.name == "archetype_hint")
        assert arch.passed


# ─────────────────────────────────────────────────────────────────────
# Sales-letter validation tests
# ─────────────────────────────────────────────────────────────────────

class TestSalesLetterValidation:

    def test_rich_sl_briefing_passes(self):
        r = validate_briefing("worker-sales-letter", RICH_SALES_LETTER_BRIEFING)
        assert r.passed, f"Rich briefing should pass. Missing: {[c.name for c in r.missing_required]}"

    def test_sparse_sl_briefing_fails(self):
        r = validate_briefing("worker-sales-letter", SPARSE_SALES_LETTER_BRIEFING)
        assert not r.passed
        # Should be missing all 3 required
        assert len(r.missing_required) == 3

    def test_sl_pricing_pattern_detected(self):
        briefing = "Plano R$ 29/mes com garantia. Target ICP: PMEs."
        r = validate_briefing("worker-sales-letter", briefing)
        offer = next(c for c in r.required_checks if c.name == "offer_terms")
        assert offer.passed
        # Should match either pattern OR keyword
        assert offer.matched_patterns or offer.matched_keywords

    def test_sl_proof_keyword_detected(self):
        briefing = "5 testimonials + R$ 29/mes + persona definida"
        r = validate_briefing("worker-sales-letter", briefing)
        proof = next(c for c in r.required_checks if c.name == "testimonials_or_proof")
        assert proof.passed


# ─────────────────────────────────────────────────────────────────────
# Tier 1 / non-Padrão-A worker tests
# ─────────────────────────────────────────────────────────────────────

class TestTier1WorkersSkipValidation:

    @pytest.mark.parametrize("worker", [
        "worker-pitch", "worker-offer", "worker-funnel",
        "worker-product", "worker-wp-audit", "worker-financial-model",
    ])
    def test_tier_1_skipped(self, worker):
        r = validate_briefing(worker, "any briefing")
        assert not r.is_tier_2
        assert r.passed  # passed=True for skipped workers (no checks failed)
        assert "Tier 1" in (r.rationale or "")

    def test_unknown_worker_skipped_with_message(self):
        r = validate_briefing("worker-nonexistent", "any briefing")
        assert not r.is_tier_2
        assert "not subject" in (r.rationale or "")


# ─────────────────────────────────────────────────────────────────────
# Check helper tests
# ─────────────────────────────────────────────────────────────────────

class TestCheckInputHelper:

    def test_check_passes_with_keyword(self):
        defn = {"keywords": ["foo"], "patterns": [], "description": "test"}
        c = check_input("text with FOO in it", defn, "test_input")
        assert c.passed
        assert "foo" in c.matched_keywords

    def test_check_passes_with_pattern(self):
        defn = {"keywords": [], "patterns": [r"\d+%"], "description": "test"}
        c = check_input("price drops 30% today", defn, "test_input")
        assert c.passed
        assert r"\d+%" in c.matched_patterns

    def test_check_fails_with_no_match(self):
        defn = {"keywords": ["xyz"], "patterns": [r"\d+\$"], "description": "test"}
        c = check_input("plain text without anything relevant", defn, "test_input")
        assert not c.passed

    def test_bad_pattern_does_not_crash(self):
        defn = {"keywords": [], "patterns": ["[unclosed"], "description": "test"}
        c = check_input("any text", defn, "test_input")
        # Should not raise — bad pattern silently skipped
        assert not c.passed


# ─────────────────────────────────────────────────────────────────────
# Rendering tests
# ─────────────────────────────────────────────────────────────────────

class TestHumanRendering:

    def test_render_passing_result(self):
        r = validate_briefing("worker-brand", RICH_BRAND_BRIEFING)
        text = render_human(r)
        assert "PASS" in text
        assert "dispatch may proceed" in text

    def test_render_failing_result(self):
        r = validate_briefing("worker-brand", SPARSE_BRAND_BRIEFING)
        text = render_human(r)
        assert "FAIL" in text
        assert "ask user" in text

    def test_render_tier_1_skip(self):
        r = validate_briefing("worker-pitch", "any")
        text = render_human(r)
        assert "[SKIP]" in text


# ─────────────────────────────────────────────────────────────────────
# Serialization tests
# ─────────────────────────────────────────────────────────────────────

class TestResultSerialization:

    def test_to_dict_has_all_fields(self):
        r = validate_briefing("worker-brand", RICH_BRAND_BRIEFING)
        d = r.to_dict()
        for k in ("worker", "skill_client_facing", "is_tier_2", "passed",
                  "required_inputs", "optional_inputs_present", "missing_required"):
            assert k in d, f"to_dict missing key {k}"

    def test_to_dict_shows_missing_when_failed(self):
        r = validate_briefing("worker-brand", SPARSE_BRAND_BRIEFING)
        d = r.to_dict()
        assert d["passed"] is False
        assert len(d["missing_required"]) >= 1
        for missing in d["missing_required"]:
            assert "name" in missing
            assert "description" in missing
