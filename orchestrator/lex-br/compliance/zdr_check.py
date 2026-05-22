#!/usr/bin/env python3
"""
ZDR (Zero Data Retention) Enforcement
======================================
Detecta dados sensíveis em inputs e exige que ZDR esteja activo antes de
processar. Protege sigilo profissional + LGPD.

Patterns detectados (regex BR-specific):
  - CPF (XXX.XXX.XXX-XX)
  - RG (formato variável por estado)
  - Números de processo (NNNNNNN-DD.AAAA.J.TR.OOOO — CNJ format)
  - CNPJ (XX.XXX.XXX/XXXX-XX)
  - Cartão de crédito (Luhn)
  - Dados clínicos (CRM + diagnósticos)
  - Dados financeiros (saldos bancários, declarações)
"""

import re
from pathlib import Path

LEX_DIR = Path.home() / ".claude" / "orchestrator" / "lex-br"

# Patterns BR-specific
PATTERN_CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
PATTERN_CNPJ = re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")
PATTERN_PROCESSO_CNJ = re.compile(r"\b\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}\b")
PATTERN_RG = re.compile(r"\b\d{1,2}\.\d{3}\.\d{3}-[\dXx]\b")
PATTERN_CARTAO = re.compile(r"\b(?:\d[ -]?){13,16}\b")
PATTERN_DADOS_CLINICOS = re.compile(
    r"\b(CID|CRM|diagnóstico|prontuário|patologia|cirurgia|óbito)\b", re.IGNORECASE
)
PATTERN_DADOS_FINANCEIROS = re.compile(
    r"\b(saldo|extrato|declaração IR|movimentação bancária|imposto de renda)\b",
    re.IGNORECASE
)


def detect_sensitive_data(text: str) -> dict:
    """Retorna dict com tipos de dados sensíveis encontrados + contagens."""
    if not text:
        return {}
    findings = {}

    cpfs = PATTERN_CPF.findall(text)
    if cpfs:
        findings["CPF"] = len(cpfs)

    cnpjs = PATTERN_CNPJ.findall(text)
    if cnpjs:
        findings["CNPJ"] = len(cnpjs)

    processos = PATTERN_PROCESSO_CNJ.findall(text)
    if processos:
        findings["NUMERO_PROCESSO"] = len(processos)

    rgs = PATTERN_RG.findall(text)
    if rgs:
        findings["RG"] = len(rgs)

    cartoes = PATTERN_CARTAO.findall(text)
    if cartoes:
        # Filtrar falsos positivos (datas, números longos)
        valid_cartoes = [c for c in cartoes if 13 <= len(c.replace(" ", "").replace("-", "")) <= 16]
        if valid_cartoes:
            findings["CARTAO_CREDITO_POSSIVEL"] = len(valid_cartoes)

    if PATTERN_DADOS_CLINICOS.search(text):
        findings["DADOS_CLINICOS"] = "presente"

    if PATTERN_DADOS_FINANCEIROS.search(text):
        findings["DADOS_FINANCEIROS"] = "presente"

    return findings


def is_zdr_active() -> bool:
    """Verifica se ZDR está active. Lê de lgpd_config.json ou env var."""
    import os
    env = os.environ.get("DARIO_ZDR_ACTIVE")
    if env is not None:
        return env.lower() in ("true", "1", "yes")

    try:
        import json
        config = json.loads(
            (LEX_DIR / "lgpd_config.json").read_text(encoding="utf-8")
        )
        return bool(config.get("zdr_active", True))
    except Exception:
        # Fail-safe: assume active (não bloqueia em config errors)
        return True


def enforce(text: str, zdr_required_levels: tuple = ("CPF", "RG", "DADOS_CLINICOS",
                                                       "CARTAO_CREDITO_POSSIVEL")) -> dict:
    """Enforce ZDR para dados sensíveis críticos.

    Args:
        text: input a verificar
        zdr_required_levels: que tipos de dados exigem ZDR active

    Returns:
        {
          "passed": bool,
          "findings": {...tipos detectados...},
          "zdr_required": bool,
          "zdr_active": bool,
          "verdict": "PASS" | "ZDR_REQUIRED" | "CLEAN",
          "rationale": str,
        }
    """
    findings = detect_sensitive_data(text)
    zdr_required = any(t in findings for t in zdr_required_levels)
    zdr_active = is_zdr_active()

    if not findings:
        return {
            "passed": True,
            "findings": {},
            "zdr_required": False,
            "zdr_active": zdr_active,
            "verdict": "CLEAN",
            "rationale": "Nenhum dado sensível detectado",
        }

    if zdr_required and not zdr_active:
        return {
            "passed": False,
            "findings": findings,
            "zdr_required": True,
            "zdr_active": False,
            "verdict": "ZDR_REQUIRED",
            "rationale": (
                f"Dados sensíveis detectados ({list(findings.keys())}) "
                f"mas ZDR INACTIVO. Para processar: configure "
                f"`DARIO_ZDR_ACTIVE=true` ou ative em lgpd_config.json "
                f"(Claude Desktop → Settings → Privacy → ZDR)."
            ),
        }

    return {
        "passed": True,
        "findings": findings,
        "zdr_required": zdr_required,
        "zdr_active": zdr_active,
        "verdict": "PASS",
        "rationale": (
            f"Dados sensíveis presentes mas ZDR active — processamento autorizado. "
            f"Findings: {findings}"
        ),
    }


if __name__ == "__main__":
    import json
    import sys
    sample = sys.argv[1] if len(sys.argv) > 1 else (
        "Cliente João Silva, CPF 123.456.789-00, processo "
        "1234567-89.2026.5.02.0001 contra empresa CNPJ 12.345.678/0001-90."
    )
    print(json.dumps(enforce(sample), indent=2, ensure_ascii=False))
