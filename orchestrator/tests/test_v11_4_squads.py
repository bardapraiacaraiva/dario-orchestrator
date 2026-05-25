import pytest
#!/usr/bin/env python3
"""Tests for v11.4 squads — ORION, OBSIDIAN-CORP, MEDIK, CAMPUS, AEGIS, ZENITH.

6 squads × 15 skills = 90 new skills. Validates foundation, skills,
license tiers (HMAC), and company.yaml integration.
"""
import sys
from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
SKILLS_DIR = Path.home() / ".claude" / "skills"
sys.path.insert(0, str(ORCH_DIR))


SQUADS = {
    "orion": {
        "subdir": "orion",
        "skills": ["product-strategy", "product-discovery", "prd-writing",
            "user-research", "jobs-to-be-done", "product-analytics",
            "roadmap-planning", "prioritization", "feature-flags", "beta-program",
            "product-launch", "growth-product", "retention-engineering",
            "pricing-strategy", "product-ops"],
        "tier_keys": ["orion_solo", "orion_team", "orion_enterprise"],
        "tier_suffixes": ["ORS", "ORT", "ORE"],
        "agent_section": "agents_product",
        "agent_id": "orion_director",
    },
    "obsidian": {
        "subdir": "obsidian-corp",
        "skills": ["knowledge-graph", "second-brain", "atomic-notes", "moc-design",
            "para-organization", "zettelkasten-method", "rag-corpus-engineering",
            "taxonomy-design", "ontology-modeling", "search-relevance",
            "semantic-search", "embedding-models", "knowledge-base-curation",
            "cross-referencing", "knowledge-compaction"],
        "tier_keys": ["obsidian_solo", "obsidian_team", "obsidian_enterprise"],
        "tier_suffixes": ["OBS", "OBT", "OBE"],
        "agent_section": "agents_knowledge",
        "agent_id": "obsidian_director",
    },
    "medik": {
        "subdir": "medik",
        "skills": ["ans-compliance", "anvisa-regulatory", "cfm-resolutions",
            "lgpd-healthcare", "telemedicine", "clinical-protocols",
            "emr-integration", "medical-billing-tuss", "clinical-decision-support",
            "health-insurance-operations", "hospital-management", "primary-care",
            "mental-health-digital", "rcm-revenue-cycle", "claim-management"],
        "tier_keys": ["medik_solo", "medik_team", "medik_enterprise"],
        "tier_suffixes": ["MDS", "MDT", "MDE"],
        "agent_section": "agents_healthcare",
        "agent_id": "medik_director",
    },
    "campus": {
        "subdir": "campus",
        "skills": ["mec-regulation", "ldb-compliance", "bncc-alignment",
            "enem-enade-prep", "ead-regulation", "instructional-design",
            "learning-experience", "education-analytics", "lms-architecture",
            "online-course-pedagogy", "gamification", "microlearning",
            "assessment-design", "certification", "corporate-learning"],
        "tier_keys": ["campus_solo", "campus_team", "campus_enterprise"],
        "tier_suffixes": ["CPS", "CPT", "CPE"],
        "agent_section": "agents_education",
        "agent_id": "campus_director",
    },
    "aegis": {
        "subdir": "aegis",
        "skills": ["threat-modeling", "pentest-methodology",
            "vulnerability-management", "soc-operations", "siem-integration",
            "edr-management", "zero-trust-architecture", "iam-identity",
            "secrets-management", "incident-response", "digital-forensics",
            "compliance-frameworks", "security-awareness", "secure-sdlc",
            "cloud-security", "third-party-risk", "supply-chain-security",
            "breach-simulation"],
        "tier_keys": ["aegis_solo", "aegis_team", "aegis_enterprise"],
        "tier_suffixes": ["AGS", "AGT", "AGE"],
        "agent_section": "agents_security",
        "agent_id": "aegis_director",
        "expected_skills": 18,
        "expected_workers": 18,
    },
    "zenith": {
        "subdir": "zenith",
        "skills": ["strategic-planning", "okr-design", "board-pack-generation",
            "ma-evaluation", "scenario-planning", "war-gaming",
            "executive-dashboard", "sensitivity-analysis", "monte-carlo",
            "decision-intelligence", "risk-assessment", "strategic-options",
            "competitive-intelligence", "capital-allocation",
            "succession-planning"],
        "tier_keys": ["zenith_solo", "zenith_team", "zenith_enterprise"],
        "tier_suffixes": ["ZNS", "ZNT", "ZNE"],
        "agent_section": "agents_executive",
        "agent_id": "zenith_director",
    },
}


def test_all_manifestos_load():
    for name, cfg in SQUADS.items():
        path = ORCH_DIR / cfg["subdir"] / "manifesto.yaml"
        assert path.exists(), f"{name} manifesto missing"
        with open(path, encoding="utf-8") as f:
            m = yaml.safe_load(f)
        assert m["identity"]["name"].lower().startswith(name[:3].lower()) or \
            name.upper() in m["identity"]["name"], f"{name} identity wrong"
        expected = cfg.get("expected_skills", 15)
        assert m["skills_count"] == expected, \
            f"{name} skills_count={m['skills_count']} != expected {expected}"


def test_all_skills_exist():
    for name, cfg in SQUADS.items():
        prefix = "obsidian-" if name == "obsidian" else f"{name}-"
        for skill in cfg["skills"]:
            skill_md = SKILLS_DIR / f"{prefix}{skill}" / "SKILL.md"
            assert skill_md.exists(), f"{name}: {prefix}{skill}/SKILL.md missing"


def test_all_skills_have_valid_frontmatter():
    for name, cfg in SQUADS.items():
        prefix = "obsidian-" if name == "obsidian" else f"{name}-"
        for skill in cfg["skills"]:
            skill_md = SKILLS_DIR / f"{prefix}{skill}" / "SKILL.md"
            content = skill_md.read_text(encoding="utf-8")
            assert content.startswith("---"), f"{prefix}{skill} no frontmatter"
            assert "name:" in content
            assert "description:" in content
            assert "parent_agent:" in content


@pytest.mark.skip(reason="Tier model simplified 2026-05-24 (RFC_STRATEGIC_DECISIONS Risk #4): 59 tiers reduced to 3 (trial/pro/enterprise). Squad foundation still tested.")
def test_license_tiers_all_present():
    from licensing.license_manager import TIER_SUFFIXES, TIERS
    for name, cfg in SQUADS.items():
        for tier_key in cfg["tier_keys"]:
            assert tier_key in TIERS, f"tier {tier_key} missing in TIERS"
        for tier_key, suffix in zip(cfg["tier_keys"], cfg["tier_suffixes"]):
            assert TIER_SUFFIXES[tier_key] == suffix, \
                f"{tier_key} suffix mismatch: {TIER_SUFFIXES[tier_key]} != {suffix}"


@pytest.mark.skip(reason="Tier model simplified 2026-05-24 (RFC_STRATEGIC_DECISIONS Risk #4): 59 tiers reduced to 3 (trial/pro/enterprise). Squad foundation still tested.")
def test_hmac_keys_roundtrip_all_squads():
    from licensing.license_manager import generate_key, validate_key
    for name, cfg in SQUADS.items():
        for tier_key in cfg["tier_keys"]:
            key = generate_key(tier_key, f"test-{name}@example.com")
            r = validate_key(key)
            assert r["valid"] is True, f"{tier_key} key validation failed"
            assert r["tier"] == tier_key


def test_company_yaml_has_all_squads():
    with open(ORCH_DIR / "company.yaml", encoding="utf-8") as f:
        c = yaml.safe_load(f)
    for name, cfg in SQUADS.items():
        assert cfg["agent_section"] in c, \
            f"{name}: {cfg['agent_section']} missing from company.yaml"
        assert cfg["agent_id"] in c[cfg["agent_section"]], \
            f"{name}: {cfg['agent_id']} missing"
        workers_key = f"workers_{name}"
        assert workers_key in c, f"{workers_key} missing"
        expected_workers = cfg.get("expected_workers", 15)
        assert len(c[workers_key]) == expected_workers, \
            f"{workers_key} has {len(c[workers_key])} workers, expected {expected_workers}"


def test_compliance_fields_in_critical_skills():
    """Skills with sensitive data must have compliance field."""
    critical = [
        ("medik-", "lgpd_healthcare_marker"),
        ("lex-", "oab_205"),
        ("aegis-", "audit"),
    ]
    for prefix, marker in critical:
        for skill_dir in SKILLS_DIR.iterdir():
            if skill_dir.is_dir() and skill_dir.name.startswith(prefix):
                content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
                # At least mentions compliance frontmatter
                assert "compliance:" in content, \
                    f"{skill_dir.name} missing compliance"


def test_total_new_skills_is_93():
    """5 squads × 15 + AEGIS 18 = 93 new skills total."""
    total = 0
    for name, cfg in SQUADS.items():
        prefix = "obsidian-" if name == "obsidian" else f"{name}-"
        found = sum(1 for d in SKILLS_DIR.iterdir()
                    if d.is_dir() and d.name.startswith(prefix)
                    and (d / "SKILL.md").exists())
        total += found
    assert total == 93, f"expected 93 new skills, got {total}"


def run_all():
    tests = [
        test_all_manifestos_load,
        test_all_skills_exist,
        test_all_skills_have_valid_frontmatter,
        test_license_tiers_all_present,
        test_hmac_keys_roundtrip_all_squads,
        test_company_yaml_has_all_squads,
        test_compliance_fields_in_critical_skills,
        test_total_new_skills_is_93,
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
