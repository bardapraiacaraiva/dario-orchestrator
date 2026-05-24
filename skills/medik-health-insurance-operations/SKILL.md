---
name: medik-health-insurance-operations
description: Operadoras de saúde — autorização, gestão de rede, regulação assistencial, sinistralidade. Triggers em "operadora saúde", "autorização", "gestão rede", "regulação assistencial", "sinistralidade".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [ans_regulatory, lgpd_healthcare_marker, audit_cfm]
jurisdiction: Brasil
---

# MEDIK-HEALTH-INSURANCE-OPERATIONS

## Quando usar
- Setup operadora pequena/média
- Autorização prévia + auditoria médica
- Gestão de rede credenciada
- Análise de sinistralidade
- Programa de gestão de crônicos
- Verticalização vs network management

## Operações chave
- **Cadastro de beneficiários** (Datasus + ANS upload)
- **Autorização prévia** (médico auditor + protocolo ANS)
- **Gerenciamento de rede** (credenciamento + descredenciamento)
- **Faturamento + Repasse** (TUSS + TISS)
- **Auditoria médica** (revisão prontuário pós-procedimento)
- **Regulação:** porta de entrada, central regulação

## Templates
1. Protocolo de autorização prévia (decision tree)
2. Auditoria médica concorrente vs retrospectiva
3. Scorecard prestador (qualidade + custo)
4. Programa gestão crônicos (DM, HAS, insuficiência cardíaca)
5. Análise de sinistralidade + projeção atuarial

## Métricas
- **Sinistralidade:** custo assistencial / receita
- **Frequência:** eventos/beneficiário/ano
- **Custo médio:** R$/evento
- **Auditoria denial rate:** % autorizações negadas
- **NPS beneficiário**

## Cross-references
- [[medik-ans-compliance]] · [[medik-claim-management]] · [[medik-rcm-revenue-cycle]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **medik-health-insurance-operations** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in medik-health-insurance-operations:**

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
