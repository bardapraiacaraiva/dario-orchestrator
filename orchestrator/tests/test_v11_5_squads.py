import pytest
#!/usr/bin/env python3
"""Tests for v11.5 squads — GAIA + NOMOS.

2 squads × 15 skills = 30 new skills. Validates foundation, skills,
license tiers (HMAC), and company.yaml integration.
"""
import sys
from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
SKILLS_DIR = Path.home() / ".claude" / "skills"
sys.path.insert(0, str(ORCH_DIR))


SQUADS = {
    "gaia": {
        "subdir": "gaia",
        "skills": ["carbon-accounting", "csrd-reporting", "esg-rating",
            "sustainability-strategy", "supply-chain-esg", "social-impact",
            "governance-frameworks", "sbti-targets", "climate-risk-tcfd",
            "ungc-reporting", "sasb-standards", "gri-reporting",
            "b-corp-certification", "esg-due-diligence", "transition-planning"],
        "tier_keys": ["gaia_solo", "gaia_team", "gaia_enterprise"],
        "tier_suffixes": ["GAS", "GAT", "GAE"],
        "tier_prices": [1497, 3997, 12997],
        "agent_section": "agents_sustainability",
        "agent_id": "gaia_director",
    },
    "nomos": {
        "subdir": "nomos",
        "skills": ["cmvm-compliance", "bdp-banking-pt", "asae-food-safety",
            "acss-healthcare-pt", "rgpd-pt-marker", "igac-events-pt",
            "anac-aviation-pt", "concorrencia-pt", "eu-ai-act-pt",
            "dora-resilience", "mifid-ii-pt", "psd2-open-banking-pt",
            "anti-fraude-pt", "kyc-aml-pt", "dl-79-2024-digital"],
        "tier_keys": ["nomos_solo", "nomos_team", "nomos_enterprise"],
        "tier_suffixes": ["NMS", "NMT", "NME"],
        "tier_prices": [997, 2997, 9997],
        "agent_section": "agents_regulatory_pt",
        "agent_id": "nomos_director",
    },
}


def test_all_manifestos_load():
    for name, cfg in SQUADS.items():
        path = ORCH_DIR / cfg["subdir"] / "manifesto.yaml"
        assert path.exists(), f"{name} manifesto missing"
        with open(path, encoding="utf-8") as f:
            m = yaml.safe_load(f)
        assert m["identity"]["name"] == name.upper(), \
            f"{name} identity wrong: {m['identity']['name']}"
        assert m["skills_count"] == 15


def test_all_skills_exist():
    for name, cfg in SQUADS.items():
        prefix = f"{name}-"
        for skill in cfg["skills"]:
            skill_md = SKILLS_DIR / f"{prefix}{skill}" / "SKILL.md"
            assert skill_md.exists(), f"{name}: {prefix}{skill}/SKILL.md missing"


def test_all_skills_have_frontmatter():
    for name, cfg in SQUADS.items():
        prefix = f"{name}-"
        for skill in cfg["skills"]:
            skill_md = SKILLS_DIR / f"{prefix}{skill}" / "SKILL.md"
            content = skill_md.read_text(encoding="utf-8")
            assert content.startswith("---"), f"{prefix}{skill} no frontmatter"
            assert "name:" in content
            assert "description:" in content
            assert "parent_agent:" in content


@pytest.mark.skip(reason="Tier model simplified 2026-05-24 (RFC_STRATEGIC_DECISIONS Risk #4): 59 tiers reduced to 3 (trial/pro/enterprise). Squad foundation still tested.")
def test_license_tiers_present():
    from license_manager import TIER_SUFFIXES, TIERS
    for name, cfg in SQUADS.items():
        for tier_key, suffix in zip(cfg["tier_keys"], cfg["tier_suffixes"]):
            assert tier_key in TIERS, f"tier {tier_key} missing"
            assert TIER_SUFFIXES[tier_key] == suffix, \
                f"{tier_key} suffix mismatch"


@pytest.mark.skip(reason="Tier model simplified 2026-05-24 (RFC_STRATEGIC_DECISIONS Risk #4): 59 tiers reduced to 3 (trial/pro/enterprise). Squad foundation still tested.")
def test_pricing_correct():
    from license_manager import TIERS
    for name, cfg in SQUADS.items():
        for tier_key, expected_price in zip(cfg["tier_keys"], cfg["tier_prices"]):
            tier = TIERS[tier_key]
            actual = tier.get("price_brl_month") or tier.get("price_brl_month_from")
            assert actual == expected_price, \
                f"{tier_key} price {actual} != expected {expected_price}"


@pytest.mark.skip(reason="Tier model simplified 2026-05-24 (RFC_STRATEGIC_DECISIONS Risk #4): 59 tiers reduced to 3 (trial/pro/enterprise). Squad foundation still tested.")
def test_hmac_keys_roundtrip():
    from license_manager import generate_key, validate_key
    for name, cfg in SQUADS.items():
        for tier_key in cfg["tier_keys"]:
            key = generate_key(tier_key, f"test-{name}@example.com")
            r = validate_key(key)
            assert r["valid"] is True, f"{tier_key} key validation failed"
            assert r["tier"] == tier_key


def test_company_yaml_has_squads():
    with open(ORCH_DIR / "company.yaml", encoding="utf-8") as f:
        c = yaml.safe_load(f)
    for name, cfg in SQUADS.items():
        assert cfg["agent_section"] in c, \
            f"{name}: section {cfg['agent_section']} missing"
        assert cfg["agent_id"] in c[cfg["agent_section"]]
        workers_key = f"workers_{name}"
        assert workers_key in c
        assert len(c[workers_key]) == 15, \
            f"{workers_key} has {len(c[workers_key])}, expected 15"


def test_total_30_skills():
    total = 0
    for name in SQUADS:
        prefix = f"{name}-"
        found = sum(1 for d in SKILLS_DIR.iterdir()
                    if d.is_dir() and d.name.startswith(prefix)
                    and (d / "SKILL.md").exists())
        total += found
    assert total == 30, f"expected 30 new skills, got {total}"


def test_jurisdiction_metadata():
    """NOMOS skills must declare PT/EU jurisdiction."""
    for skill in SQUADS["nomos"]["skills"]:
        skill_md = SKILLS_DIR / f"nomos-{skill}" / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert "jurisdiction" in content.lower(), \
            f"nomos-{skill} missing jurisdiction declaration"


def run_all():
    tests = [
        test_all_manifestos_load,
        test_all_skills_exist,
        test_all_skills_have_frontmatter,
        test_license_tiers_present,
        test_pricing_correct,
        test_hmac_keys_roundtrip,
        test_company_yaml_has_squads,
        test_total_30_skills,
        test_jurisdiction_metadata,
    ]
    passed = 0
    failed = []
    for test in tests:
        try:
            test()
            passed += 1
            print(f"  PASS  {test.__name__}")
        except Exception as e:
            failed.append((test.__name__, str(e)))
            print(f"  FAIL  {test.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed")
    return len(failed) == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
