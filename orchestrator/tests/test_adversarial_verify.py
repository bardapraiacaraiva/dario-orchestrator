"""Acceptance A/B for adversarial verification (Next-Gen N4, 2026-06-12).

Baseline (pre-N4): every scored-above-60 client_facing deliverable completed
as "done" — seeded defects reached the human as finished work. With the
verifier: critical defects downgrade done -> in_review with issues attached.

The A/B below runs 5 golden-like client_facing deliverables, each seeding a
real defect class observed in production reviews, plus 1 clean control for
the false-positive rate. Acceptance: >= 4/5 seeded defects caught, control
NOT downgraded.
"""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import pytest

import quality.adversarial_verify as av
from core.db import DB
from execution import lifecycle
from quality.adversarial_verify import (
    check_contradictions,
    check_placeholders,
    check_table_totals,
    parse_confidence_block,
    verify_output,
)


@pytest.fixture(autouse=True)
def no_real_api(monkeypatch):
    """O juiz LLM faz chamadas REAIS quando a key existe (keyring) — provado
    em 2026-06-12, quando flaggou corretamente o fixture sintético como texto
    sem substância. Testes ficam determinísticos; produção mantém o juiz."""
    monkeypatch.setattr(av, "llm_judge", lambda task, output: [])

CONF_BLOCK = """
```json
{"confidence": {"mode": "HIGH_CONFIDENCE", "score": 84,
  "verified_facts": ["preço base confirmado no briefing"],
  "assumed_facts": ["prazo de obra de 6 semanas"],
  "needs_client_confirmation": ["data de início"]}}
```
"""

BODY = ("## Proposta\n" + "Conteúdo substantivo e específico para o cliente.\n" * 18)

# ─── 5 goldens client_facing com defeito semeado + 1 controlo limpo ────────

GOLDENS = {
    "G1-confirmar-leak": BODY + "\nPreço final: [CONFIRMAR com a Karen]\n" + CONF_BLOCK,
    "G2-broken-total": BODY + """
| Fase | Valor |
|---|---|
| Branding | € 2.000,00 |
| Arquitetura | € 5.500,00 |
| Obra | € 14.000,00 |
| **Total** | € 19.000,00 |
""" + CONF_BLOCK,  # real: 21.500
    "G3-angle-placeholder": BODY + "\nEntrega prevista: <date> em <client>.\n" + CONF_BLOCK,
    "G4-todo-no-confidence": BODY + "\nTODO: rever margens antes de enviar.\n",
    "G5-contradiction": BODY
        + "\nTotal do investimento: € 30.000\n...\nResumindo, o total do investimento: € 27.500\n"
        + CONF_BLOCK,
    "CONTROL-clean": BODY + """
| Fase | Valor |
|---|---|
| Branding | € 2.000,00 |
| Obra | € 14.000,00 |
| **Total** | € 16.000,00 |
""" + CONF_BLOCK,
}


def _task(tid="N4-1", policy="client_facing"):
    return {"id": tid, "title": "Proposta turnkey loja", "skill": "diva-budget",
            "project": "its-bananas", "execution_policy": policy}


# ─── unit: cada detetor apanha a sua classe ────────────────────────────────


def test_placeholder_detection():
    issues = check_placeholders(GOLDENS["G1-confirmar-leak"])
    assert any(i["severity"] == "critical" and "CONFIRMAR" in i["quote"] for i in issues)
    assert check_placeholders(GOLDENS["CONTROL-clean"]) == []


def test_table_total_mismatch():
    issues = check_table_totals(GOLDENS["G2-broken-total"])
    assert len(issues) == 1 and issues[0]["severity"] == "critical"
    assert "21,500.00" in issues[0]["reason"]
    assert check_table_totals(GOLDENS["CONTROL-clean"]) == []


def test_contradiction_detection():
    issues = check_contradictions(GOLDENS["G5-contradiction"])
    assert len(issues) == 1 and issues[0]["severity"] == "critical"


def test_confidence_block_parses():
    conf = parse_confidence_block(GOLDENS["CONTROL-clean"])
    assert conf["mode"] == "HIGH_CONFIDENCE" and conf["score"] == 84
    assert parse_confidence_block(GOLDENS["G4-todo-no-confidence"]) is None


# ─── ACEITAÇÃO N4: A/B nos 5 goldens ───────────────────────────────────────


def test_ab_verifier_catches_seeded_defects():
    """Baseline: 5/5 defeitos chegavam ao humano como 'done'. Com o
    verificador: >= 4/5 apanhados (critical) e o controlo limpo passa."""
    caught = 0
    for name, output in GOLDENS.items():
        verdict = verify_output(_task(), output, use_llm_judge=False)
        if name.startswith("CONTROL"):
            assert not verdict["critical"], f"falso positivo no controlo: {verdict['issues']}"
        elif verdict["critical"]:
            caught += 1
    assert caught >= 4, f"verificador apanhou só {caught}/5 defeitos semeados"


def test_lifecycle_downgrades_done_to_in_review(tmp_path, monkeypatch):
    """Fio completo: finalize de uma task client_facing com defeito crítico
    fica in_review (não done), com o verdict no journal e na review queue."""
    db = DB(db_path=str(tmp_path / "test.db"))
    db.create_task({"id": "N4-1", "title": "Proposta turnkey", "description": "p",
                    "project": "its-bananas", "priority": "high",
                    "assignee": "worker-diva-budget", "skill": "dario-content"})
    db.update_task("N4-1", {"status": "in_progress",
                            "execution_policy": "client_facing"})
    monkeypatch.setattr(lifecycle, "run_engine",
                        lambda script, args, timeout=30: {"pass": True})
    import quality.adversarial_verify as av
    monkeypatch.setattr(av, "QUEUE_DIR", tmp_path / "queue")

    task = db.get_task("N4-1")
    res = lifecycle.finalize_success(
        "N4-1", task, GOLDENS["G1-confirmar-leak"], tokens=900, score=78,
        db=db, source="api", model="sonnet", final_status="done",
        quality_score_for_filter=None, count_budget_on_tripwire=True,
        meter_tokens=False)

    assert res["status"] == "in_review"          # downgraded, não done
    assert db.get_task("N4-1")["status"] == "in_review"
    ver = db.last_journal_step("N4-1", "verified")
    assert ver and ver["status"] == "flag" and ver["payload"]["critical"]
    assert res.get("confidence", {}).get("score") == 84   # G5 block extraído
    queued = list((tmp_path / "queue").glob("*.meta.yaml"))
    assert len(queued) == 1                       # chegou à human review queue


def test_lifecycle_clean_output_still_completes_done(tmp_path, monkeypatch):
    db = DB(db_path=str(tmp_path / "test.db"))
    db.create_task({"id": "N4-2", "title": "Proposta limpa", "description": "p",
                    "project": "test", "priority": "high",
                    "assignee": "worker-x", "skill": "dario-content"})
    db.update_task("N4-2", {"status": "in_progress",
                            "execution_policy": "client_facing"})
    monkeypatch.setattr(lifecycle, "run_engine",
                        lambda script, args, timeout=30: {"pass": True})

    task = db.get_task("N4-2")
    res = lifecycle.finalize_success(
        "N4-2", task, GOLDENS["CONTROL-clean"], tokens=900, score=78,
        db=db, source="api", model="sonnet", final_status="done",
        quality_score_for_filter=None, count_budget_on_tripwire=True,
        meter_tokens=False)

    assert res["status"] == "done"
    ver = db.last_journal_step("N4-2", "verified")
    assert ver is not None  # verificado e registado, sem downgrade


def test_default_policy_skips_verification(tmp_path, monkeypatch):
    db = DB(db_path=str(tmp_path / "test.db"))
    db.create_task({"id": "N4-3", "title": "Task interna", "description": "p",
                    "project": "test", "priority": "low",
                    "assignee": "worker-x", "skill": "dario-content"})
    db.update_task("N4-3", {"status": "in_progress"})
    monkeypatch.setattr(lifecycle, "run_engine",
                        lambda script, args, timeout=30: {"pass": True})

    task = db.get_task("N4-3")
    lifecycle.finalize_success(
        "N4-3", task, GOLDENS["G1-confirmar-leak"], tokens=100, score=70,
        db=db, source="session", model="opus", final_status="done",
        quality_score_for_filter=None, meter_tokens=False)
    assert db.last_journal_step("N4-3", "verified") is None
    assert db.get_task("N4-3")["status"] == "done"


def test_prompt_builder_requests_confidence_block():
    p_cf = lifecycle.build_execution_prompt(_task(policy="client_facing"), "", {})
    p_def = lifecycle.build_execution_prompt(_task(policy="default"), "", {})
    assert '"confidence"' in p_cf and "Confidence Block" in p_cf
    assert "Confidence Block" not in p_def
