---
name: medik-medical-billing-tuss
description: TUSS billing — Tabela Única de Saúde Suplementar, CBHPM, AMB. Codificação para operadoras. Triggers em "TUSS", "CBHPM", "AMB", "faturamento médico", "código procedimento", "tabela operadora".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [ans_regulatory, audit_trail]
jurisdiction: Brasil
---

# MEDIK-MEDICAL-BILLING-TUSS

## Quando usar
- Setup faturamento ANS-compliant
- Codificação TUSS de procedimentos
- Negociação tabela com operadora
- Glosas e recursos
- Migration AMB → CBHPM → TUSS

## Tabelas
- **TUSS (ANS)** — Tabela Única, padrão obrigatório operadoras
- **CBHPM 2022** — Classificação Brasileira Hierarquizada
- **AMB 92** — legada, ainda referenciada
- **SUS SIGTAP** — público (referência para precificação)

## Templates
1. Mapeamento procedimento → TUSS
2. Tabela negociação operadora (CH + valor) com benchmarks
3. Workflow glosa → recurso administrativo
4. Auditoria de faturamento (% recuperação)
5. Análise sinistralidade

## Compliance
- ✓ ANS RN 305/2012 (TISS — troca info operadora)
- ✓ Padrão TISS comunicação
- ✓ Auditoria CFC

## Cross-references
- [[medik-claim-management]] · [[medik-rcm-revenue-cycle]] · [[medik-ans-compliance]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **medik-medical-billing-tuss** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in medik-medical-billing-tuss:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->
