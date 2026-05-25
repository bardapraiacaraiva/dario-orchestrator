"""Seed 3 brand goldens for the DSPy pilot (Onda 5 #3).

Captures 3 hand-written brand positioning outputs for distinct verticals.
Each is a realistic-but-synthetic example calibrated to the BrandPositioning
signature shape so the DSPy optimiser has labelled examples to bootstrap from.

Usage:
    python -m optimization.seed_brand_goldens
"""

from __future__ import annotations

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from quality.golden_eval import capture_golden

GOLDENS = [
    {
        "eval_id": "brand-fintech-pt-01",
        "briefing": (
            "SaaS de gestão financeira para PMEs portuguesas. "
            "Concorre com Moloni/SAGE. Target: 50-250 colaboradores, "
            "CFO ou contabilista. Diferencial: integração nativa com "
            "Banco de Portugal e SAFT automatizado."
        ),
        "output": """# Brand Positioning

## Posicionamento
O parceiro financeiro digital das PMEs portuguesas que tratam contabilidade como vantagem competitiva, não como burocracia obrigatória.

archetype: Sage

## Tom de voz
Confiante, técnico, sem jargão. Como um CFO sénior a explicar a um colega.

## Diferenciadores
- Conformidade SAFT-PT validada em tempo real, não no fecho do mês
- Integração nativa com Banco de Portugal (SIBS/IBAN)
- Dashboards focados em decisão de tesouraria, não em compliance
""",
        "score": 87,
        "notes": (
            "SaaS de gestão financeira para PMEs portuguesas. "
            "Concorre com Moloni/SAGE. Target: 50-250 colaboradores, "
            "CFO ou contabilista. Diferencial: integração nativa com "
            "Banco de Portugal e SAFT automatizado."
        ),
    },
    {
        "eval_id": "brand-boutique-hotel-01",
        "briefing": (
            "Hotel boutique 14 quartos em Lisboa, Príncipe Real. "
            "Edifício Pombalino restaurado. Hóspede-tipo: viajante de "
            "negócios premium 40-60 que troca cadeias por experiência. "
            "Preço €280-450/noite."
        ),
        "output": """# Brand Positioning

## Posicionamento
A casa lisboeta onde o viajante exigente troca anonimato hoteleiro por uma noite que pertence só àquele edifício de 1758.

archetype: Lover

## Tom de voz
Calmo, cúmplice, próximo. Português europeu sem floreados.

## Diferenciadores
- 14 quartos significam que o concierge sabe o seu nome no primeiro check-in
- Pequeno-almoço servido à mesa, com produtores nomeados em cada prato
- Edifício classificado como referência arquitetónica pelo CML
""",
        "score": 91,
        "notes": (
            "Hotel boutique 14 quartos em Lisboa, Príncipe Real. "
            "Edifício Pombalino restaurado. Hóspede-tipo: viajante de "
            "negócios premium 40-60 que troca cadeias por experiência. "
            "Preço €280-450/noite."
        ),
    },
    {
        "eval_id": "brand-ai-devtools-01",
        "briefing": (
            "Startup SaaS B2B: ferramenta de observability para agentes "
            "de IA em produção. Target: VP Engineering em scale-ups com "
            "100+ engenheiros que correm LangChain/LangGraph. "
            "Concorrem com LangSmith e Helicone."
        ),
        "output": """# Brand Positioning

## Posicionamento
A plataforma que dá aos engineering leaders a mesma confiança que têm na sua infra de microservices, agora estendida aos agentes de IA que correm em produção.

archetype: Sage

## Tom de voz
Direto, técnico, com humor seco. Engenheiro para engenheiro.

## Diferenciadores
- OpenTelemetry-native — sem vendor lock-in no plano de tracing
- Drill-down do span ao prompt ao tool-call ao output em três cliques
- SLA-aware: alerta antes de o utilizador final reportar regressão de qualidade
""",
        "score": 89,
        "notes": (
            "Startup SaaS B2B: ferramenta de observability para agentes "
            "de IA em produção. Target: VP Engineering em scale-ups com "
            "100+ engenheiros que correm LangChain/LangGraph. "
            "Concorrem com LangSmith e Helicone."
        ),
    },
]


def seed() -> dict:
    results = []
    for g in GOLDENS:
        r = capture_golden(
            eval_id=g["eval_id"],
            output_text=g["output"],
            human_score=g["score"],
            notes=g["notes"],
            force=True,
        )
        results.append({"eval_id": g["eval_id"], "status": r.get("status")})
    return {"captured": len(results), "results": results}


def main():
    report = seed()
    import json as _json
    print(_json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
