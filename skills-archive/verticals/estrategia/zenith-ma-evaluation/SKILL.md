---
name: zenith-ma-evaluation
description: M&A evaluation — diligence, valuation (DCF/Comps/LBO), integration, deal structuring. Triggers em "M&A", "due diligence", "valuation", "DCF", "Comparable Companies", "LBO", "acquisition", "merger".
license: SEE-LICENSE
parent_agent: zenith-director
compliance: [privilege_executive, insider_trading_safeguard, board_confidentiality]
---

# ZENITH-MA-EVALUATION

## Quando usar
- Acquisition target evaluation
- Sell-side prep (banker pitch)
- Strategic alternatives review
- Integration planning (post-merger)
- Joint venture decision

## Diligence categorias
- **Commercial:** market, customers, competition
- **Financial:** quality of earnings, cash flow, working capital
- **Operational:** systems, processes, scalability
- **HR:** talent, culture, retention risks
- **Legal:** contracts, IP, litigation, regulatory
- **Tech:** stack, architecture, security
- **Tax:** structure optimization
- **ESG:** governance, environment, social

## Valuation
- **DCF:** Discounted Cash Flow (intrinsic)
- **Comparable Companies (CCA):** multiples (EV/Revenue, EV/EBITDA)
- **Precedent Transactions:** M&A multiples
- **LBO (PE):** IRR back-into deal
- **Sum of Parts:** divisões separadas

## Templates
1. Diligence checklist (300+ items)
2. DCF model template (5y projection + terminal value)
3. CCA comparable set + multiples
4. Quality of Earnings adjustment
5. Integration 100-day plan
6. Synergy capture tracker
7. Deal memo (1-pager for board)

## Cross-references
- [[zenith-capital-allocation]] · [[zenith-strategic-planning]] · [[zenith-risk-assessment]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **zenith-ma-evaluation** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in zenith-ma-evaluation:**

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
