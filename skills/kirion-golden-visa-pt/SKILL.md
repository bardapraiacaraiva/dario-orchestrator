---
name: kirion-golden-visa-pt
description: Golden Visa PT — ARI investment routes, due diligence, residence by investment. Triggers em "Golden Visa", "ARI", "Autorização Residência Investimento", "investment visa PT", "EU residency by investment".
license: SEE-LICENSE
parent_agent: kirion-director
compliance: [audit_immutable]
jurisdiction: Portugal
---

# KIRION-GOLDEN-VISA-PT

## Marco
- **Lei 23/2007 + alterações** — Lei Estrangeiros PT
- **Portaria 1334-D/2010** + atualizações
- **Lei 18/2022 — Mais Habitação:** removeu investimento imobiliário urbano (Out 2023+)
- **DL 9/2023:** reformulou Golden Visa

## Rotas investimento (pós-2023)
- **Investment funds (PT/UE):** ≥ €500K + 5y hold + non-RE
- **Capital transfer (PT):** ≥ €1.5M
- **Research + heritage:** ≥ €250-500K
- **Job creation:** ≥ 10 jobs (no minimum capital)
- **Company creation:** PT commercial company + 5 jobs

## NÃO elegíveis (pós-Out 2023)
- ❌ Compra imóvel residencial urbano (era rota popular antes)
- ❌ Lisboa, Porto, costa (high-density restricted antes 2023 já)

## Workflow ARI
```
1. Investimento + comprovativo origem fundos
2. KYC AML PT (UIF compliance)
3. Comprovação NIF + conta bancária PT
4. Submissão pedido SEF/AIMA
5. Análise (6-18 meses típico)
6. Aprovação + ARI 2 anos initial
7. Renovação 3 anos
8. Permanente após 5 anos (Lei Nacionalidade)
```

## Templates
1. Eligibility assessment (route selection)
2. KYC documentation pack
3. Investment fund due diligence
4. Tax planning (NHR ou RNH new regime)
5. Family reunification petition
6. Citizenship application after 5y

## Cross-references
- [[kirion-portuguese-renda-vitalicia]] · [[lex-administrativo]] · [[nomos-kyc-aml-pt]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **kirion-golden-visa-pt** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in kirion-golden-visa-pt:**

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
