---
name: medik-rcm-revenue-cycle
description: Revenue Cycle Management — autorização → produção → faturamento → recebimento. Triggers em "RCM", "revenue cycle", "ciclo receita hospitalar", "gestão financeira hospital", "DSO healthcare".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [ans_regulatory, audit_trail]
jurisdiction: Brasil
---

# MEDIK-RCM-REVENUE-CYCLE

## Quando usar
- Diagnóstico de ciclo de receita (DSO alto? glosa alta?)
- Setup RCM em greenfield (hospital novo)
- Automação de faturamento (TISS)
- Negociação de tabela com operadora
- Programa de redução de glosas

## Stages
```
1. Pre-service:    autorização + elegibilidade + estimativa
2. Service:        captura clínica + codificação
3. Faturamento:    TUSS/TISS submission
4. Adjudication:   operadora análise + glosa
5. Recurso:        re-submission + auditoria
6. Recebimento:    payment posting + reconciliation
```

## Métricas
- **DSO (Days Sales Outstanding):** dias para receber
- **Glosa rate:** % faturado glosado
- **Net collection rate:** % recebido / faturado líquido
- **Denied claim rate:** % primária negada
- **A/R aging:** distribuição idade contas a receber

## Templates
1. RCM workflow end-to-end (BPMN)
2. Glosa root cause analysis
3. Programa de redução de glosas (causas top-10)
4. DSO improvement playbook
5. KPI dashboard RCM

## Cross-references
- [[medik-medical-billing-tuss]] · [[medik-claim-management]] · [[demeter-bi-dashboard]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **medik-rcm-revenue-cycle** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in medik-rcm-revenue-cycle:**

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
