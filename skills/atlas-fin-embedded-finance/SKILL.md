---
name: atlas-fin-embedded-finance
description: Embedded finance — payments in non-financial apps, embedded lending, embedded insurance. Triggers em "embedded finance", "embedded payments", "embedded lending", "embedded insurance", "Klarna", "Affirm", "BNPL".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [audit_immutable]
---

# ATLAS-FIN-EMBEDDED-FINANCE

## Definição
**Embedded finance = financial products native dentro de non-financial app.** Uber não é banco mas paga drivers; Shopify não é credit mas oferece empréstimos.

## Tipos
- **Embedded payments:** checkout in-app (Stripe, Adyen)
- **Embedded lending:** BNPL (Klarna, Affirm), instant credit
- **Embedded insurance:** product-specific (Cover Genius)
- **Embedded investing:** brokerage-in-app (Apex Clearing)
- **Embedded banking:** accounts + cards (Unit, Treasury Prime)

## Quando faz sense
- Customer já tem alta frequência uso
- Friction de saída pagar = revenue loss
- Data network effects (mais dados = better credit decisions)
- Vertical-specific knowledge advantage (Ramp = corporate cards SaaS-aware)

## BNPL specifically
- Klarna (US$ 15B valuation 2024)
- Afterpay (acquired Square US$ 29B)
- Affirm (NASDAQ: AFRM)
- BR: Mercado Pago, RecargaPay, Iupp
- Risks: underwriting young consumers, regulatory pushback

## Templates
1. Embedded finance opportunity assessment
2. Build vs partner vs buy decision
3. BNPL underwriting model
4. Embedded insurance partnership framework
5. Compliance responsibility matrix
6. Take-rate economics model

## Cross-references
- [[atlas-fin-banking-as-a-service]] · [[orion-pricing-strategy]] · [[atlas-fin-fraud-prevention]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-fin-embedded-finance** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-fin-embedded-finance:**

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
