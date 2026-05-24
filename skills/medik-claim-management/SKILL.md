---
name: medik-claim-management
description: Claim management — glosas, recursos, denials management, root cause analysis. Triggers em "glosa", "recurso glosa", "denial management", "auditoria operadora", "claim management".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [ans_regulatory, audit_trail]
jurisdiction: Brasil
---

# MEDIK-CLAIM-MANAGEMENT

## Quando usar
- Glosa rate alto (>10%)
- Recursos administrativos sistemáticos
- Auditoria de operadora pós-faturamento
- Disputa judicial procedimento negado
- Programa de redução de denials

## Tipos de glosa
- **Glosa técnica:** procedimento sem código TUSS válido
- **Glosa administrativa:** sem autorização, fora prazo
- **Glosa clínica:** auditor médico questiona indicação
- **Glosa contratual:** valor diferente do contratado

## Workflow recurso
```
1. Glosa recebida (operadora)
2. Análise root cause
3. Recurso documentado (laudo médico, prontuário, protocolo)
4. Re-submission via TISS
5. Decisão operadora
6. Se mantida: NIP ANS ou jurídico
```

## Templates
1. Recurso administrativo template (por tipo de glosa)
2. Root cause analysis 5-why
3. Programa preventivo de glosas (top-10 causas)
4. NIP ANS template
5. Petição inicial vs operadora (com lex-civil + lex-consumidor cross)

## Métricas
- **Glosa primária:** %
- **Recuperação após recurso:** %
- **Time to recovery:** dias
- **Net denial rate:** glosa - recovery

## Cross-references
- [[medik-rcm-revenue-cycle]] · [[medik-medical-billing-tuss]] · [[lex-consumidor]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **medik-claim-management** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in medik-claim-management:**

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
