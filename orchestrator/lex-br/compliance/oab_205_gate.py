#!/usr/bin/env python3
"""
OAB Provimento 205/2021 — Enforcement Gate
============================================
Provimento OAB 205/2021 estabelece que o advogado é responsável pelo
conteúdo final produzido com IA. Este gate força que outputs destinados a
tribunal, cliente externo ou contraparte tenham flag de revisão humana
confirmada antes de release.

Integra com DARIO ethical_gate como Check 0.5 (após o gate genérico).

Outputs internos (memos de equipa, drafts iniciais) não são bloqueados —
apenas outputs que saem do escritório.

CLI:
    python oab_205_gate.py --task TASK-001          # Avaliar task
    python oab_205_gate.py --json                   # JSON output
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LEX_DIR = Path.home() / ".claude" / "orchestrator" / "lex-br"
ORCH_DIR = Path.home() / ".claude" / "orchestrator"

# Output types que requerem revisão humana
EXTERNAL_OUTPUT_TYPES = {
    "tribunal",        # Petições para juiz
    "cliente_externo",  # Comunicações ao cliente
    "contraparte",      # Comunicações à contraparte
    "publicacao",       # Posts, artigos, conteúdo público
    "imprensa",         # Material para imprensa
    "regulador",        # Comunicações a reguladores (ANPD, BACEN, etc)
}

# Output types internos (não bloqueados)
INTERNAL_OUTPUT_TYPES = {
    "draft_interno",
    "memo_equipa",
    "pesquisa_juridica",
    "consulta_interna",
    "estudo_caso",
    "treinamento",
}


def check(task: dict) -> dict:
    """Verifica se task respeita OAB Provimento 205/2021.

    Returns:
        {
          "passed": bool,
          "verdict": "PASS" | "REQUIRES_HUMAN_REVIEW" | "NOT_APPLICABLE",
          "rationale": str,
          "blocking": bool,    # True se output não pode ser libertado
        }
    """
    skill = task.get("skill", "")

    # Só aplica a skills LEX-BR
    if not skill.startswith("lex-"):
        return {
            "passed": True,
            "verdict": "NOT_APPLICABLE",
            "rationale": "Skill não-jurídica — OAB 205 não aplica",
            "blocking": False,
        }

    output_type = task.get("output_type", "draft_interno")

    # Outputs internos passam
    if output_type in INTERNAL_OUTPUT_TYPES:
        return {
            "passed": True,
            "verdict": "PASS",
            "rationale": f"Output interno ({output_type}) — uso assistido sob responsabilidade do advogado",
            "blocking": False,
        }

    # Outputs externos requerem flag de revisão humana
    if output_type in EXTERNAL_OUTPUT_TYPES:
        revisao_confirmada = task.get("revisao_humana_confirmada", False)
        advogado_oab = task.get("advogado_oab_numero")

        if not revisao_confirmada:
            return {
                "passed": False,
                "verdict": "REQUIRES_HUMAN_REVIEW",
                "rationale": (
                    f"Provimento OAB 205/2021 art. 6º: output tipo '{output_type}' "
                    f"requer revisão humana confirmada. Defina "
                    f"`revisao_humana_confirmada: true` no task após revisão pelo "
                    f"advogado responsável (OAB nº)."
                ),
                "blocking": True,
            }

        if not advogado_oab:
            return {
                "passed": False,
                "verdict": "REQUIRES_HUMAN_REVIEW",
                "rationale": (
                    "Revisão confirmada mas advogado_oab_numero ausente. "
                    "Identifique o advogado responsável (formato: 'OAB/SP nº 123456')."
                ),
                "blocking": True,
            }

        return {
            "passed": True,
            "verdict": "PASS",
            "rationale": (
                f"Output revisto por {advogado_oab} — release autorizado sob "
                f"responsabilidade profissional (Provimento 205/2021)."
            ),
            "blocking": False,
            "reviewer_oab": advogado_oab,
        }

    # Output type não reconhecido — fail-safe (requer revisão por default)
    return {
        "passed": False,
        "verdict": "REQUIRES_HUMAN_REVIEW",
        "rationale": (
            f"Output type '{output_type}' não classificado. Especifique como "
            f"'draft_interno' ou um dos tipos externos: {sorted(EXTERNAL_OUTPUT_TYPES)}"
        ),
        "blocking": True,
    }


def render_human(result: dict) -> str:
    verdict = result["verdict"]
    symbol = {"PASS": "+", "REQUIRES_HUMAN_REVIEW": "!",
              "NOT_APPLICABLE": "~"}.get(verdict, "?")
    out = [f"[{symbol}] OAB Provimento 205/2021: {verdict}"]
    out.append(f"  Rationale: {result['rationale']}")
    if result.get("reviewer_oab"):
        out.append(f"  Reviewer: {result['reviewer_oab']}")
    if result.get("blocking"):
        out.append("  → OUTPUT BLOQUEADO até confirmação de revisão.")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="OAB Provimento 205/2021 Gate")
    p.add_argument("--task-file", help="YAML task file to evaluate")
    p.add_argument("--task-json", help="Inline JSON task")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    if args.task_file:
        try:
            import yaml
            with open(args.task_file, "r", encoding="utf-8") as f:
                task = yaml.safe_load(f)
        except Exception as e:
            print(f"Erro lendo task: {e}", file=sys.stderr)
            return 1
    elif args.task_json:
        task = json.loads(args.task_json)
    else:
        p.print_help()
        return 1

    result = check(task)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_human(result))
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    sys.exit(main())
