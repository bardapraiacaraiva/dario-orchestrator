#!/usr/bin/env python3
"""Tests for LEX-BR agent — 15 skills + compliance + MCP servers."""

import sys
from pathlib import Path

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
LEX_DIR = ORCH_DIR / "lex-br"
SKILLS_DIR = Path.home() / ".claude" / "skills"

sys.path.insert(0, str(ORCH_DIR))
sys.path.insert(0, str(LEX_DIR / "compliance"))


# ─── Foundation tests ───────────────────────────────────────

def test_lex_br_directory_exists():
    assert LEX_DIR.exists()
    assert (LEX_DIR / "manifesto.yaml").exists()
    assert (LEX_DIR / "compliance").is_dir()
    assert (LEX_DIR / "memory").is_dir()
    assert (LEX_DIR / "mcp_servers").is_dir()
    return True


def test_manifesto_loads():
    import yaml
    with open(LEX_DIR / "manifesto.yaml", encoding="utf-8") as f:
        m = yaml.safe_load(f)
    assert m["identity"]["name"] == "LEX-BR"
    assert m["identity"]["jurisdiction"] == "Brasil"
    assert len(m["coverage"]) == 15
    return True


def test_all_15_skills_exist():
    expected = {
        "lex-civil", "lex-commercial", "lex-corporate", "lex-trabalhista",
        "lex-tributario", "lex-lgpd", "lex-regulatorio", "lex-ai-governance",
        "lex-ip", "lex-litigation", "lex-consumidor", "lex-administrativo",
        "lex-imobiliario", "lex-familia", "lex-criminal",
    }
    found = set()
    for d in SKILLS_DIR.iterdir():
        if d.is_dir() and d.name.startswith("lex-"):
            if (d / "SKILL.md").exists():
                found.add(d.name)
    missing = expected - found
    assert not missing, f"missing skills: {missing}"
    return True


def test_skills_have_compliance_in_frontmatter():
    for skill_name in ["lex-civil", "lex-trabalhista", "lex-lgpd", "lex-criminal"]:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert "compliance:" in content, f"{skill_name} missing compliance field"
        assert "oab_205" in content, f"{skill_name} missing oab_205"
    return True


# ─── Compliance modules ────────────────────────────────────

def test_oab_205_gate_blocks_external_without_review():
    from oab_205_gate import check
    task = {"skill": "lex-trabalhista", "output_type": "tribunal",
            "revisao_humana_confirmada": False}
    r = check(task)
    assert r["passed"] is False
    assert r["verdict"] == "REQUIRES_HUMAN_REVIEW"
    assert r["blocking"] is True
    return True


def test_oab_205_gate_allows_external_with_review():
    from oab_205_gate import check
    task = {"skill": "lex-civil", "output_type": "tribunal",
            "revisao_humana_confirmada": True,
            "advogado_oab_numero": "OAB/SP 123456"}
    r = check(task)
    assert r["passed"] is True
    assert r["verdict"] == "PASS"
    return True


def test_oab_205_gate_skips_non_lex_skills():
    from oab_205_gate import check
    task = {"skill": "dario-brand", "output_type": "tribunal"}
    r = check(task)
    assert r["verdict"] == "NOT_APPLICABLE"
    return True


def test_oab_205_internal_outputs_pass():
    from oab_205_gate import check
    task = {"skill": "lex-trabalhista", "output_type": "draft_interno"}
    r = check(task)
    assert r["passed"] is True
    return True


def test_lgpd_marker_adds_rodape():
    from lgpd_marker import add_marker
    text = "Parecer extensivo sobre cláusula contratual " * 30
    out = add_marker(text, escritorio="Test Adv", dpo_contact="dpo@test.com")
    assert "DARIO/LEX-BR" in out
    assert "Controlador: Test Adv" in out
    assert "ZDR" in out
    return True


def test_lgpd_marker_idempotent():
    from lgpd_marker import add_marker
    text = "Parecer " * 100
    once = add_marker(text, escritorio="X", dpo_contact="y")
    twice = add_marker(once, escritorio="X", dpo_contact="y")
    # Should not duplicate
    assert twice.count("DARIO/LEX-BR") == 1
    return True


def test_zdr_detects_cpf():
    from zdr_check import detect_sensitive_data
    text = "Cliente João Silva, CPF 123.456.789-00"
    findings = detect_sensitive_data(text)
    assert "CPF" in findings
    return True


def test_zdr_detects_processo_cnj():
    from zdr_check import detect_sensitive_data
    text = "Processo 1234567-89.2026.5.02.0001 contra empresa"
    findings = detect_sensitive_data(text)
    assert "NUMERO_PROCESSO" in findings
    return True


def test_zdr_clean_text_passes():
    from zdr_check import enforce
    r = enforce("Mero texto sem dados sensíveis aqui.")
    assert r["passed"] is True
    assert r["verdict"] == "CLEAN"
    return True


def test_cite_checker_validates_codigos():
    from cite_checker import validate
    r = validate("Fundamento: art. 186 do CC e art. 927 CC.")
    assert r["total_citations"] >= 1
    return True


def test_cite_checker_flags_artigo_inexistente():
    from cite_checker import validate
    r = validate("Aplicando art. 9999 do CC")
    invalid_or_flagged = any(
        not d["valid"] or d["flags"] for d in r["details"]
    )
    assert invalid_or_flagged, f"Should flag art. 9999 CC: {r}"
    return True


def test_privilege_marker_adds_banner():
    from privilege_marker import mark
    text = "Estratégia processual sigilosa"
    out = mark(text, output_type="estrategia_processual")
    assert "SIGILOSO" in out
    assert "PRIVILÉGIO" in out
    return True


def test_privilege_marker_skips_non_privileged_type():
    from privilege_marker import mark
    text = "Conteúdo público"
    out = mark(text, output_type="publicacao")
    assert "SIGILOSO" not in out
    return True


def test_audit_oab_logs_event():
    from audit_oab import count_today, log
    before = count_today()
    log(
        skill="lex-test", task_id="TEST-001",
        output="test", client_id="test-client",
        output_type="draft_interno",
        flags={"test": True},
    )
    after = count_today()
    assert after == before + 1
    return True


# ─── MCP Servers ────────────────────────────────────────────

def test_mcp_jusbrasil_search_returns_structure():
    sys.path.insert(0, str(LEX_DIR / "mcp_servers" / "jusbrasil"))
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "jb_server", LEX_DIR / "mcp_servers" / "jusbrasil" / "server.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.search_jurisprudence("rescisão indireta")
    assert "mode" in r
    assert "results" in r
    return True


def test_mcp_jusbrasil_sumula_lookup():
    sys.path.insert(0, str(LEX_DIR / "mcp_servers" / "jusbrasil"))
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "jb_server", LEX_DIR / "mcp_servers" / "jusbrasil" / "server.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.get_sumula("STJ", "145")
    assert r.get("numero") == "145" or "error" in r
    return True


def test_mcp_stf_sumula_vinculante():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "stf_server", LEX_DIR / "mcp_servers" / "stf" / "server.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.get_sumula_vinculante("14")
    assert r.get("numero") == "14"
    return True


def test_mcp_stf_repercussao_geral():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "stf_server", LEX_DIR / "mcp_servers" / "stf" / "server.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.get_repercussao_geral_temas()
    assert r["total"] > 0
    assert "temas" in r
    return True


def test_mcp_cnj_datajud_module_loads():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "cnj_server", LEX_DIR / "mcp_servers" / "cnj_datajud" / "server.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.TRIBUNAIS_VALIDOS
    assert "tjsp" in mod.TRIBUNAIS_VALIDOS
    assert "trt2" in mod.TRIBUNAIS_VALIDOS
    return True


# ─── Integration tests ────────────────────────────────────

def test_lex_skills_in_semantic_corpus():
    from semantic_dispatch import extract_skill_corpus
    corpus = extract_skill_corpus()
    lex_skills_in_corpus = [s for s in corpus if s.startswith("lex-")]
    assert len(lex_skills_in_corpus) >= 15, \
        f"Expected 15+ lex skills, got {len(lex_skills_in_corpus)}: {lex_skills_in_corpus}"
    return True


@pytest.mark.real_embedding
def test_semantic_dispatch_routes_to_lex_trabalhista():
    """End-to-end semantic routing — requires real Ollama. The mock returns
    hash-derived vectors that defeat ranking by meaning."""
    from semantic_dispatch import semantic_match
    matches = semantic_match("reclamação trabalhista verbas rescisórias", top_k=5)
    top_skills = [m[0] for m in matches]
    assert "lex-trabalhista" in top_skills, \
        f"lex-trabalhista should be in top 5: {top_skills}"
    return True


def test_company_yaml_includes_lex_br():
    import yaml
    with open(ORCH_DIR / "company.yaml", encoding="utf-8") as f:
        company = yaml.safe_load(f)
    # New sections appended
    assert "agents_legal" in company
    assert "workers_lex" in company
    assert "lex_br_director" in company["agents_legal"]
    # 15 workers
    workers = company.get("workers_lex", {})
    lex_workers = [k for k in workers if k.startswith("worker-lex-")]
    assert len(lex_workers) == 15
    return True


TESTS = [
    ("LEX-BR directory exists", test_lex_br_directory_exists),
    ("Manifesto YAML loads", test_manifesto_loads),
    ("All 15 LEX skills have SKILL.md", test_all_15_skills_exist),
    ("Skills have compliance frontmatter", test_skills_have_compliance_in_frontmatter),
    # Compliance
    ("OAB 205 blocks external without review", test_oab_205_gate_blocks_external_without_review),
    ("OAB 205 allows external with review", test_oab_205_gate_allows_external_with_review),
    ("OAB 205 skips non-lex skills", test_oab_205_gate_skips_non_lex_skills),
    ("OAB 205 internal outputs pass", test_oab_205_internal_outputs_pass),
    ("LGPD marker adds rodape", test_lgpd_marker_adds_rodape),
    ("LGPD marker idempotent (no dup)", test_lgpd_marker_idempotent),
    ("ZDR detects CPF", test_zdr_detects_cpf),
    ("ZDR detects processo CNJ", test_zdr_detects_processo_cnj),
    ("ZDR clean text passes", test_zdr_clean_text_passes),
    ("Cite checker validates códigos", test_cite_checker_validates_codigos),
    ("Cite checker flags artigo inexistente", test_cite_checker_flags_artigo_inexistente),
    ("Privilege marker adds banner", test_privilege_marker_adds_banner),
    ("Privilege marker skips public types", test_privilege_marker_skips_non_privileged_type),
    ("Audit OAB logs event", test_audit_oab_logs_event),
    # MCP
    ("mcp-jusbrasil search returns structure", test_mcp_jusbrasil_search_returns_structure),
    ("mcp-jusbrasil sumula lookup", test_mcp_jusbrasil_sumula_lookup),
    ("mcp-stf SV lookup", test_mcp_stf_sumula_vinculante),
    ("mcp-stf RG temas", test_mcp_stf_repercussao_geral),
    ("mcp-cnj-datajud module loads", test_mcp_cnj_datajud_module_loads),
    # Integration
    ("LEX skills in semantic corpus", test_lex_skills_in_semantic_corpus),
    ("Semantic routes to lex-trabalhista", test_semantic_dispatch_routes_to_lex_trabalhista),
    ("company.yaml includes LEX-BR", test_company_yaml_includes_lex_br),
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
