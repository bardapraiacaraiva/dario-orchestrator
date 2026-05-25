import pytest
#!/usr/bin/env python3
"""Tests for DEMETER squad — 15 skills + pricing tiers + license integration.

Verifies foundation, skills, taxonomy, cross-references, and licensing.
"""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
DEMETER_DIR = ORCH_DIR / "demeter"
SKILLS_DIR = Path.home() / ".claude" / "skills"

sys.path.insert(0, str(ORCH_DIR))


EXPECTED_SKILLS = {
    "demeter-etl", "demeter-warehouse", "demeter-bi-dashboard",
    "demeter-data-quality", "demeter-ml-pipelines", "demeter-ab-testing",
    "demeter-cohort-analysis", "demeter-predictive", "demeter-realtime-streaming",
    "demeter-data-catalog", "demeter-dataops", "demeter-dbt-workflows",
    "demeter-metrics-layer", "demeter-event-tracking", "demeter-data-storytelling",
}


# ─── Foundation tests ───────────────────────────────────────

def test_demeter_directory_exists():
    assert DEMETER_DIR.exists(), "demeter dir missing"
    assert (DEMETER_DIR / "manifesto.yaml").exists(), "manifesto missing"


def test_manifesto_loads_and_has_15_areas():
    import yaml
    with open(DEMETER_DIR / "manifesto.yaml", encoding="utf-8") as f:
        m = yaml.safe_load(f)
    assert m["identity"]["name"] == "DEMETER"
    assert len(m["coverage"]) == 15, f"expected 15 areas, got {len(m['coverage'])}"


def test_manifesto_has_pricing_tiers():
    import yaml
    with open(DEMETER_DIR / "manifesto.yaml", encoding="utf-8") as f:
        m = yaml.safe_load(f)
    tiers = m.get("pricing_tiers", {})
    assert "solo" in tiers
    assert "team" in tiers
    assert "enterprise" in tiers


# ─── Skills tests ───────────────────────────────────────────

def test_all_15_skills_exist():
    found = set()
    for d in SKILLS_DIR.iterdir():
        if d.is_dir() and d.name.startswith("demeter-"):
            if (d / "SKILL.md").exists():
                found.add(d.name)
    missing = EXPECTED_SKILLS - found
    assert not missing, f"missing skills: {missing}"
    extra = found - EXPECTED_SKILLS
    assert not extra, f"unexpected skills: {extra}"


def test_skills_have_valid_frontmatter():
    for skill_name in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert content.startswith("---"), f"{skill_name} missing frontmatter start"
        assert "name:" in content, f"{skill_name} missing name field"
        assert "description:" in content, f"{skill_name} missing description"
        assert "parent_agent: demeter-director" in content, \
            f"{skill_name} missing parent_agent"


def test_skills_have_triggers_in_description():
    for skill_name in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert "Triggers" in content or "triggers" in content, \
            f"{skill_name} missing triggers"


def test_skills_have_cross_references():
    skills_with_xref = 0
    for skill_name in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        if "Cross-references" in content or "[[demeter-" in content:
            skills_with_xref += 1
    assert skills_with_xref >= 12, \
        f"only {skills_with_xref}/15 skills have cross-references"


# ─── Compliance/governance ──────────────────────────────────

def test_skills_have_compliance_field():
    skills_with_compliance = 0
    for skill_name in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        if "compliance:" in content:
            skills_with_compliance += 1
    assert skills_with_compliance == 15, \
        f"only {skills_with_compliance}/15 skills have compliance field"


def test_lgpd_mentioned_in_data_skills():
    """ETL, warehouse, event-tracking deal with PII — must mention LGPD."""
    pii_skills = ["demeter-etl", "demeter-warehouse", "demeter-event-tracking",
                  "demeter-data-catalog"]
    for skill_name in pii_skills:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert "lgpd" in content.lower() or "LGPD" in content, \
            f"{skill_name} doesn't mention LGPD despite handling PII"


# ─── License integration ────────────────────────────────────

@pytest.mark.skip(reason="Tier model simplified 2026-05-24 (RFC_STRATEGIC_DECISIONS Risk #4): 59 tiers reduced to 3 (trial/pro/enterprise). Squad foundation still tested.")
def test_license_tiers_include_demeter():
    from license_manager import TIERS
    assert "demeter_solo" in TIERS
    assert "demeter_team" in TIERS
    assert "demeter_enterprise" in TIERS


@pytest.mark.skip(reason="Tier model simplified 2026-05-24 (RFC_STRATEGIC_DECISIONS Risk #4): 59 tiers reduced to 3 (trial/pro/enterprise). Squad foundation still tested.")
def test_demeter_solo_pricing():
    from license_manager import TIERS
    solo = TIERS["demeter_solo"]
    assert solo["price_brl_month"] == 297
    assert solo["max_parallel"] == 1
    assert solo["demeter_skills_count"] == 8
    assert solo["demeter_dashboards_month"] == 5


@pytest.mark.skip(reason="Tier model simplified 2026-05-24 (RFC_STRATEGIC_DECISIONS Risk #4): 59 tiers reduced to 3 (trial/pro/enterprise). Squad foundation still tested.")
def test_demeter_team_pricing():
    from license_manager import TIERS
    team = TIERS["demeter_team"]
    assert team["price_brl_month"] == 997
    assert team["max_parallel"] == 3
    assert team["demeter_skills_count"] == 15
    assert team["features"]["ml_pipelines"] is True
    assert team["features"]["realtime_streaming"] is True


@pytest.mark.skip(reason="Tier model simplified 2026-05-24 (RFC_STRATEGIC_DECISIONS Risk #4): 59 tiers reduced to 3 (trial/pro/enterprise). Squad foundation still tested.")
def test_demeter_enterprise_pricing():
    from license_manager import TIERS
    ent = TIERS["demeter_enterprise"]
    assert ent["price_brl_month_from"] == 4000
    assert ent["max_parallel"] == 5
    assert ent["features"]["sla_4h_support"] is True
    assert ent["features"]["data_lineage"] is True


@pytest.mark.skip(reason="Tier model simplified 2026-05-24 (RFC_STRATEGIC_DECISIONS Risk #4): 59 tiers reduced to 3 (trial/pro/enterprise). Squad foundation still tested.")
def test_demeter_tier_suffixes_registered():
    from license_manager import TIER_MAP, TIER_SUFFIXES
    assert TIER_SUFFIXES["demeter_solo"] == "DMS"
    assert TIER_SUFFIXES["demeter_team"] == "DMT"
    assert TIER_SUFFIXES["demeter_enterprise"] == "DME"
    # Reverse map should also be populated
    assert TIER_MAP["DMS"] == "demeter_solo"


@pytest.mark.skip(reason="Tier model simplified 2026-05-24 (RFC_STRATEGIC_DECISIONS Risk #4): 59 tiers reduced to 3 (trial/pro/enterprise). Squad foundation still tested.")
def test_demeter_key_generation_and_validation():
    """End-to-end HMAC key roundtrip for demeter_team."""
    from license_manager import generate_key, validate_key
    key = generate_key("demeter_team", "test@flipperboys.com")
    assert key.startswith("DARIO-")
    assert key.endswith("-DMT")
    r = validate_key(key)
    assert r["valid"] is True, f"key validation failed: {r}"
    assert r["tier"] == "demeter_team"


@pytest.mark.skip(reason="Tier model simplified 2026-05-24 (RFC_STRATEGIC_DECISIONS Risk #4): 59 tiers reduced to 3 (trial/pro/enterprise). Squad foundation still tested.")
def test_demeter_key_tamper_rejected():
    """Tampering with a key must invalidate the HMAC."""
    from license_manager import generate_key, validate_key
    key = generate_key("demeter_solo", "test@example.com")
    # Flip a character in the middle (not the prefix/suffix)
    parts = key.split("-")
    parts[2] = "FFFF" if parts[2] != "FFFF" else "AAAA"
    tampered = "-".join(parts)
    r = validate_key(tampered)
    assert r["valid"] is False, "tampered key should be rejected"


# ─── Company.yaml integration ───────────────────────────────

def test_company_yaml_has_demeter_section():
    import yaml
    company_path = ORCH_DIR / "company.yaml"
    with open(company_path, encoding="utf-8") as f:
        c = yaml.safe_load(f)
    # Must have agents_data with demeter_director
    assert "agents_data" in c, "company.yaml missing agents_data section"
    assert "demeter_director" in c["agents_data"], \
        "demeter_director missing from agents_data"
    # Must have workers_demeter with 15 workers
    assert "workers_demeter" in c, "company.yaml missing workers_demeter"
    assert len(c["workers_demeter"]) == 15, \
        f"expected 15 workers, got {len(c['workers_demeter'])}"
    # Must have squads
    assert "squads_demeter" in c, "company.yaml missing squads_demeter"


# ─── Test runner ─────────────────────────────────────────────

def run_all():
    tests = [
        # Foundation
        test_demeter_directory_exists,
        test_manifesto_loads_and_has_15_areas,
        test_manifesto_has_pricing_tiers,
        # Skills
        test_all_15_skills_exist,
        test_skills_have_valid_frontmatter,
        test_skills_have_triggers_in_description,
        test_skills_have_cross_references,
        # Compliance
        test_skills_have_compliance_field,
        test_lgpd_mentioned_in_data_skills,
        # License
        test_license_tiers_include_demeter,
        test_demeter_solo_pricing,
        test_demeter_team_pricing,
        test_demeter_enterprise_pricing,
        test_demeter_tier_suffixes_registered,
        test_demeter_key_generation_and_validation,
        test_demeter_key_tamper_rejected,
        # Integration
        test_company_yaml_has_demeter_section,
    ]
    passed = 0
    failed = []
    for test in tests:
        try:
            test()
            passed += 1
            print(f"  PASS  {test.__name__}")
        except AssertionError as e:
            failed.append((test.__name__, str(e)))
            print(f"  FAIL  {test.__name__}: {e}")
        except Exception as e:
            failed.append((test.__name__, f"{type(e).__name__}: {e}"))
            print(f"  ERR   {test.__name__}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed")
    if failed:
        print(f"FAILURES ({len(failed)}):")
        for name, reason in failed:
            print(f"  - {name}: {reason}")
    return len(failed) == 0


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
