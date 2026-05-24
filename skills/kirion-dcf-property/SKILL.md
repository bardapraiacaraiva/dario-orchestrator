---
name: kirion-dcf-property
description: DCF property — NPV, IRR, cap rate, exit yield, leveraged returns. Triggers em "DCF property", "NPV imóvel", "IRR real estate", "cap rate", "exit yield", "leveraged IRR", "underwriting".
license: SEE-LICENSE
parent_agent: kirion-director
---

# KIRION-DCF-PROPERTY

## DCF components RE
```
NOI = Gross Rent - Vacancy - Operating Expenses
DCF Year N:
  CF = NOI_N + Capex_N
  Terminal Value = NOI_(N+1) / Exit Cap Rate
  PV = Σ CF / (1+r)^t + TV / (1+r)^N
```

## Métricas chave
- **Going-in cap rate:** NOI Year 1 / Price
- **Exit cap rate:** assumption tipicamente 25-50 bps above going-in
- **Stabilized cap rate:** post-leasing/renovation
- **Cash-on-Cash:** Cash flow / Equity invested (leveraged metric)
- **Unleveraged IRR:** all-cash deal
- **Leveraged IRR:** with debt financing
- **Equity multiple:** total cash returned / cash invested

## Discount rates típicas
- **Office stabilized:** WACC 6-8%
- **Retail prime:** 7-9%
- **Industrial:** 6.5-8.5%
- **Development:** 12-18% (risk premium)
- **Hotel:** 10-14%

## Templates
1. 10-year DCF model template (5 sheets)
2. Sensitivity table (cap rate × growth rate)
3. Leveraged vs unleveraged comparison
4. Capex schedule (capital improvements)
5. Hold period analysis (3y, 5y, 7y, 10y)
6. Waterfall structure (LP/GP)

## Cross-references
- [[kirion-real-estate-valuation]] · [[kirion-reit-analysis]] · [[zenith-ma-evaluation]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **kirion-dcf-property** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in kirion-dcf-property:**

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
