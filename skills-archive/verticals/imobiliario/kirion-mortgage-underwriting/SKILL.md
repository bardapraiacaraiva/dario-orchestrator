---
name: kirion-mortgage-underwriting
description: Mortgage underwriting BR/PT — DTI, LTV, qualifying ratios, credit risk. Triggers em "mortgage underwriting", "DTI", "LTV", "qualifying ratios", "credit risk mortgage", "Crédito Habitação PT", "Crédito Imobiliário BR".
license: SEE-LICENSE
parent_agent: kirion-director
compliance: [audit_immutable]
---

# KIRION-MORTGAGE-UNDERWRITING

## Métricas chave
- **LTV (Loan-to-Value):** Loan / Property value
- **DTI (Debt-to-Income):** Monthly debt / Monthly income
- **Front-end ratio (PT):** Mortgage / Income (≤ 30% target)
- **Back-end ratio:** Total debt / Income (≤ 36-43% target)
- **DSCR (commercial):** NOI / Debt service (≥ 1.25x)
- **PITI:** Principal + Interest + Taxes + Insurance

## BR specifics
- **SBPE:** Sistema Brasileiro Poupança Empréstimo (savings-backed)
- **FGTS:** programa Casa Verde Amarela (replacement Minha Casa Minha Vida)
- **Pró-Cotista FGTS:** subsidized rates
- **Carteira hipotecária:** Bacen reporting required

## PT specifics
- **DSTI cap:** 50% Banco de Portugal Macroprudential
- **LTV cap:** 90% for primary residence (Banco de Portugal)
- **Maturity cap:** 40 years (35 for second home)
- **Spread + Euribor 6M/12M** standard pricing
- **Crédito habitação custos:** notarial + IMT + IS

## Templates
1. Pre-approval calculator (BR + PT)
2. Underwriting checklist
3. Income verification protocols
4. Credit score interpretation (Banco Portugal score)
5. Documento documentos requeridos
6. Risk-based pricing matrix

## Cross-references
- [[kirion-real-estate-valuation]] · [[atlas-fin-kyc-onboarding]] · [[nomos-bdp-banking-pt]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **kirion-mortgage-underwriting** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in kirion-mortgage-underwriting:**

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
