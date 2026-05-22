#!/usr/bin/env python3
"""Tests for v12.0 squads — 7 squads × 15 skills = 105 new skills."""
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
SKILLS_DIR = Path.home() / ".claude" / "skills"
sys.path.insert(0, str(ORCH_DIR))

SQUADS = {
    "mercurius": {"subdir": "mercurius", "agent_section": "agents_sales", "agent_id": "mercurius_director"},
    "atlas-fin": {"subdir": "atlas-fin", "agent_section": "agents_fintech", "agent_id": "atlas_fin_director", "prefix": "atlas-fin-"},
    "helios": {"subdir": "helios", "agent_section": "agents_energy", "agent_id": "helios_director"},
    "kirion": {"subdir": "kirion", "agent_section": "agents_realestate", "agent_id": "kirion_director"},
    "sphinx": {"subdir": "sphinx", "agent_section": "agents_cyber_advanced", "agent_id": "sphinx_director"},
    "euterpe": {"subdir": "euterpe", "agent_section": "agents_marketing_advanced", "agent_id": "euterpe_director"},
    "oraculo": {"subdir": "oraculo", "agent_section": "agents_ai_research", "agent_id": "oraculo_director"},
}

NEW_TIERS = ["mercurius_solo", "mercurius_team", "mercurius_enterprise",
             "atlas_fin_solo", "atlas_fin_team", "atlas_fin_enterprise",
             "helios_solo", "helios_team", "helios_enterprise",
             "kirion_solo", "kirion_team", "kirion_enterprise",
             "sphinx_solo", "sphinx_team", "sphinx_enterprise",
             "euterpe_solo", "euterpe_team", "euterpe_enterprise",
             "oraculo_solo", "oraculo_team", "oraculo_enterprise"]


def test_all_manifestos_exist():
    import yaml
    for name, cfg in SQUADS.items():
        path = ORCH_DIR / cfg["subdir"] / "manifesto.yaml"
        assert path.exists(), f"{name} manifesto missing"
        with open(path, encoding="utf-8") as f:
            m = yaml.safe_load(f)
        assert m["skills_count"] == 15, f"{name}: skills_count={m['skills_count']}"
    return True


def test_all_skills_exist_105():
    total = 0
    for name, cfg in SQUADS.items():
        prefix = cfg.get("prefix", f"{name}-")
        count = sum(1 for d in SKILLS_DIR.iterdir()
                    if d.is_dir() and d.name.startswith(prefix)
                    and (d / "SKILL.md").exists())
        assert count == 15, f"{name}: {count}/15 skills"
        total += count
    assert total == 105, f"expected 105 total, got {total}"
    return True


def test_license_tiers_21_new():
    from license_manager import TIER_SUFFIXES, TIERS
    for tier in NEW_TIERS:
        assert tier in TIERS, f"{tier} missing in TIERS"
        assert tier in TIER_SUFFIXES, f"{tier} missing in TIER_SUFFIXES"
    return True


def test_hmac_roundtrip_all_21():
    from license_manager import generate_key, validate_key
    for tier in NEW_TIERS:
        key = generate_key(tier, "test@example.com")
        r = validate_key(key)
        assert r["valid"], f"{tier} HMAC failed"
        assert r["tier"] == tier
    return True


def test_company_yaml_has_7_sections():
    import yaml
    with open(ORCH_DIR / "company.yaml", encoding="utf-8") as f:
        c = yaml.safe_load(f)
    for name, cfg in SQUADS.items():
        assert cfg["agent_section"] in c, f"{cfg['agent_section']} missing"
        assert cfg["agent_id"] in c[cfg["agent_section"]]
        workers_key = f"workers_{name.replace('-', '_')}"
        assert workers_key in c, f"{workers_key} missing"
        assert len(c[workers_key]) == 15, f"{workers_key}: {len(c[workers_key])}/15 workers"
    return True


def test_total_tiers_59():
    # 54 single tiers + 5 Enterprise bundles (Onda 12)
    from license_manager import TIERS
    assert len(TIERS) == 59, f"expected 59 tiers (54 + 5 bundles), got {len(TIERS)}"
    bundles = [k for k, v in TIERS.items() if "bundle_components" in v]
    assert len(bundles) == 5, f"expected 5 bundles, got {len(bundles)}"
    return True


def run_all():
    tests = [test_all_manifestos_exist, test_all_skills_exist_105,
             test_license_tiers_21_new, test_hmac_roundtrip_all_21,
             test_company_yaml_has_7_sections, test_total_tiers_59]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed")
    return passed == len(tests)


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
