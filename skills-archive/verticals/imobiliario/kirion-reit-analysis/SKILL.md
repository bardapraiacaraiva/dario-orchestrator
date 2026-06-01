---
name: kirion-reit-analysis
description: REIT/FII analysis — NAV, dividend yield, leverage, FFO/AFFO, premium/discount. Triggers em "REIT", "FII", "NAV", "dividend yield", "FFO", "AFFO", "FII BR", "REIT US".
license: SEE-LICENSE
parent_agent: kirion-director
compliance: [cvm_compliance, anbima_alignment]
---

# KIRION-REIT-ANALYSIS

## Métricas chave
- **NAV (Net Asset Value):** Assets - Liabilities (per share)
- **Premium/Discount to NAV:** Stock price vs NAV ratio
- **FFO (Funds From Operations):** Net Income + Depreciation - Gains
- **AFFO (Adjusted FFO):** FFO - Capex maintenance
- **Dividend yield:** Annual dividend / Stock price
- **Payout ratio:** Dividend / FFO (target 70-90%)
- **Leverage:** Debt / Total Assets (target 30-50%)
- **WACC:** debt + equity cost weighted

## Tipos REITs/FIIs
- **Equity REITs:** direct ownership (residential, office, retail)
- **Mortgage REITs:** lender (interest rate sensitive)
- **Hybrid:** mix
- **FII tijolo (BR):** own property
- **FII papel (BR):** debt securities (CRIs, LCIs)
- **FII fundo de fundos (BR):** invest in other FIIs

## Marcos
- **BR FII:** Lei 8.668/93 + CVM Resolução 175
- **US REIT:** IRS Code Sec. 856 (90% distribution requirement)
- **PT SIIC equivalent:** SICAFI (Lei 26/2018)

## Templates
1. REIT/FII screening model
2. NAV calculation methodology
3. FFO/AFFO bridge
4. Peer comparison matrix
5. Distribution sustainability analysis
6. Premium/discount historical chart

## Cross-references
- [[kirion-dcf-property]] · [[kirion-build-to-rent]] · [[zenith-ma-evaluation]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **kirion-reit-analysis** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in kirion-reit-analysis:**

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
