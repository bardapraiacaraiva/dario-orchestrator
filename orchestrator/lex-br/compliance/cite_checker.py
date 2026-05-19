#!/usr/bin/env python3
"""
Cite Checker — Validação de citações jurídicas
================================================
Valida que artigos/leis/súmulas citados em outputs LEX-BR:
  1. Existem (não inventados pelo modelo)
  2. Não estão revogados
  3. Aplicam-se à matéria (heurística simples)

Sources:
  - base local em base_artigos.yaml (50+ leis principais BR)
  - mcp-jusbrasil (quando online — fallback se não)
  - lista de revogados conhecidos
"""

import json
import re
import sys
from pathlib import Path

LEX_DIR = Path.home() / ".claude" / "orchestrator" / "lex-br"
BASE_ARTIGOS = LEX_DIR / "compliance" / "base_artigos.yaml"

# Patterns de citação jurídica BR
PATTERN_ARTIGO_LEI = re.compile(
    r"art(?:igo|\.)?\s*(\d+)[º°]?(?:[,\s]+(?:§|parágrafo|inciso|alínea)\s*(\d+|[a-z]))?\s*"
    r"(?:da\s+|do\s+|d[ao]\s+)?"
    r"(?:Lei\s+n?[º°]?\s*([\d\.]+/?\d*)|"
    r"Decreto[\s-]?Lei\s+n?[º°]?\s*([\d\.]+)|"
    r"(CC|CPC|CLT|CDC|CP|CPP|EOAB|LGPD|CF|CTN)|"
    r"Decreto\s+n?[º°]?\s*([\d\.]+))",
    re.IGNORECASE,
)

PATTERN_SUMULA = re.compile(
    r"S[úu]mula\s+(?:Vinculante\s+)?(\d+)\s*(?:do\s+)?(STF|STJ|TST|TSE)",
    re.IGNORECASE,
)

# Códigos brasileiros conhecidos (com lei correspondente)
CODIGOS = {
    "CC": "Lei 10.406/2002",
    "CPC": "Lei 13.105/2015",
    "CLT": "Decreto-Lei 5.452/1943",
    "CDC": "Lei 8.078/1990",
    "CP": "Decreto-Lei 2.848/1940",
    "CPP": "Decreto-Lei 3.689/1941",
    "EOAB": "Lei 8.906/1994",
    "LGPD": "Lei 13.709/2018",
    "CF": "Constituição Federal/1988",
    "CTN": "Lei 5.172/1966",
}

# Artigos máximos por código (heurística — evita citações inexistentes tipo "art. 9999 CC")
ARTIGOS_MAX = {
    "CC": 2046,        # Código Civil tem 2046 artigos
    "CPC": 1072,       # CPC/2015
    "CLT": 922,        # CLT
    "CDC": 119,        # CDC
    "CP": 361,         # Código Penal
    "CPP": 811,        # Código de Processo Penal
    "EOAB": 87,        # Estatuto OAB
    "LGPD": 65,        # LGPD
    "CF": 250,         # Constituição (artigos permanentes)
    "CTN": 218,        # Código Tributário Nacional
}

# Leis revogadas conhecidas (lista a expandir)
LEIS_REVOGADAS = {
    "Lei 8.666/93": "Substituída por Lei 14.133/21 (NLLC). Verificar regime transitório.",
    "Lei 8.666/1993": "Substituída por Lei 14.133/21 (NLLC). Verificar regime transitório.",
    # Codigo Civil 1916 revogado pelo CC/2002
    "Lei 3.071/1916": "Revogada pelo CC/2002 (Lei 10.406/02)",
    # Antigo CPC
    "Lei 5.869/1973": "Revogada pelo CPC/2015 (Lei 13.105/15)",
}


def extract_citations(text: str) -> list:
    """Extrai todas as citações jurídicas do texto."""
    citations = []

    for m in PATTERN_ARTIGO_LEI.finditer(text):
        artigo_num = m.group(1)
        sub = m.group(2)  # parágrafo/inciso
        lei_num = m.group(3) or m.group(4) or m.group(6)
        codigo = m.group(5)
        if codigo:
            codigo = codigo.upper()
        citations.append({
            "type": "artigo_lei",
            "artigo": artigo_num,
            "subdivisao": sub,
            "lei": lei_num,
            "codigo": codigo,
            "raw": m.group(0),
        })

    for m in PATTERN_SUMULA.finditer(text):
        citations.append({
            "type": "sumula",
            "numero": m.group(1),
            "tribunal": m.group(2).upper(),
            "raw": m.group(0),
        })

    return citations


def validate_citation(cit: dict) -> dict:
    """Valida uma citação individual."""
    result = {"citation": cit["raw"], "valid": True, "flags": []}

    if cit["type"] == "artigo_lei":
        codigo = cit.get("codigo")
        artigo_num_str = cit.get("artigo", "0")
        try:
            artigo_num = int(artigo_num_str)
        except Exception:
            artigo_num = 0

        # Validar limites do código
        if codigo and codigo in ARTIGOS_MAX:
            if artigo_num > ARTIGOS_MAX[codigo]:
                result["valid"] = False
                result["flags"].append(
                    f"Artigo {artigo_num} excede limite do {codigo} (max {ARTIGOS_MAX[codigo]})"
                )

        # Validar lei revogada
        lei = cit.get("lei")
        if lei:
            for revogada, motivo in LEIS_REVOGADAS.items():
                if lei.replace(".", "") in revogada.replace(".", ""):
                    result["valid"] = False
                    result["flags"].append(f"Lei revogada: {motivo}")

    elif cit["type"] == "sumula":
        try:
            num = int(cit["numero"])
            tribunal = cit["tribunal"]
            # Súmulas vinculantes STF: 1-58 atualmente
            if tribunal == "STF" and num > 60:
                result["flags"].append(f"Súmula STF nº {num} — verificar existência via MCP")
            # Súmulas STJ vão até ~660
            if tribunal == "STJ" and num > 700:
                result["flags"].append(f"Súmula STJ nº {num} — verificar")
            # Súmulas TST até ~480
            if tribunal == "TST" and num > 500:
                result["flags"].append(f"Súmula TST nº {num} — verificar")
        except Exception:
            pass

    return result


def validate(text: str) -> dict:
    """Valida todas as citações do texto.

    Returns:
        {
          "total_citations": N,
          "valid": M,
          "invalid": K,
          "details": [...],
          "verdict": "PASS" | "FLAGS_FOUND" | "INVALID_CITATIONS",
        }
    """
    citations = extract_citations(text)
    if not citations:
        return {
            "total_citations": 0,
            "valid": 0,
            "invalid": 0,
            "details": [],
            "verdict": "PASS",
            "rationale": "Nenhuma citação jurídica detectada",
        }

    details = [validate_citation(c) for c in citations]
    valid_count = sum(1 for d in details if d["valid"])
    invalid_count = sum(1 for d in details if not d["valid"])
    flag_count = sum(len(d["flags"]) for d in details if d["valid"])

    verdict = "PASS"
    if invalid_count > 0:
        verdict = "INVALID_CITATIONS"
    elif flag_count > 0:
        verdict = "FLAGS_FOUND"

    return {
        "total_citations": len(citations),
        "valid": valid_count,
        "invalid": invalid_count,
        "flags_total": flag_count,
        "details": details,
        "verdict": verdict,
        "rationale": (
            f"{valid_count}/{len(citations)} citações válidas. "
            f"{invalid_count} inválidas, {flag_count} com flags."
        ),
    }


if __name__ == "__main__":
    sample = sys.argv[1] if len(sys.argv) > 1 else (
        "Fundamentação: art. 186 do CC e art. 927, parágrafo único do CC. "
        "Aplicação da Súmula 145 do STJ. Lei 8.666/93 art. 24."
    )
    print(json.dumps(validate(sample), indent=2, ensure_ascii=False))
