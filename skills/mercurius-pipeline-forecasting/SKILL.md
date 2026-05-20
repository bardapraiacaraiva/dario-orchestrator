---
name: mercurius-pipeline-forecasting
description: Pipeline forecasting — deal scoring, pipeline coverage, forecast accuracy, weighted vs committed. Triggers em "pipeline forecasting", "sales forecast", "deal scoring", "pipeline coverage", "weighted pipeline", "commit forecast".
license: MIT
parent_agent: mercurius-director
compliance: [audit_trail]
---

# MERCURIUS-PIPELINE-FORECASTING

## Métodos forecasting

| Método | Acurácia | Esforço |
|---|---|---|
| **Pipeline weighted** | 60-70% | Baixo |
| **Stage-based** | 70-80% | Médio |
| **Rep commit + sandbag** | 75-85% | Médio |
| **AI/ML based (Clari, Gong)** | 85-95% | Alto |
| **Custom multi-touch** | 80-90% | Médio-Alto |

## Pipeline coverage
- 3x pipeline coverage = healthy (need $3 in pipeline per $1 quota)
- 4x = comfortable
- <2x = red flag, prospecting need

## Deal scoring (MEDDIC-based)
- Metrics (quantified value)
- Economic buyer identified
- Decision criteria documented
- Decision process understood
- Identified pain (validated)
- Champion confirmed

Score 0-100 → confidence weighting

## Forecast cadence
- **Weekly:** rep self-commit
- **Bi-weekly:** manager review + adjustment
- **Monthly:** CRO/VP forecast (commit + best case)
- **Quarterly:** board forecast (high confidence only)

## Templates
1. Pipeline review template (weekly)
2. Deal scoring rubric (MEDDIC)
3. Forecast accuracy dashboard
4. Pipeline health metrics (coverage, age, slip)
5. Slippage analysis (why deals push)
6. Commit vs actual variance tracker

## Cross-references
- [[mercurius-sales-ops]] · [[zenith-sensitivity-analysis]] · [[demeter-predictive]]
