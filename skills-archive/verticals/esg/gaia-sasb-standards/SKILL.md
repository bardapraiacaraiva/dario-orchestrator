---
name: gaia-sasb-standards
description: SASB Standards — industry-specific sustainability disclosure for 77 SICS sectors. Now under ISSB. Triggers em "SASB", "Sustainability Accounting Standards Board", "ISSB", "industry-specific ESG", "SICS".
license: SEE-LICENSE
parent_agent: gaia-director
compliance: [audit_immutable, csrd_disclosure_gate]
---

# GAIA-SASB-STANDARDS

## Marco
- **SASB Standards** (now under ISSB — IFRS Foundation)
- **77 SICS sectors** (Sustainable Industry Classification System)
- **5 dimensions:** Environment, Social Capital, Human Capital, Business Model & Innovation, Leadership & Governance
- **Financial materiality** focus (different from GRI stakeholder materiality)
- **IFRS S1 + IFRS S2** — ISSB sustainability standards (TCFD-aligned)

## Quando usar
- US/global listed companies SEC disclosures
- Investor relations (SASB is investor-grade)
- Industry benchmarking
- ISSB IFRS S1/S2 adoption
- M&A sustainability due diligence

## SICS sectors examples
- **11 Consumer Goods:** Apparel/Footwear, Food/Beverage, Household & Personal
- **22 Extractives & Minerals Processing:** Coal Ops, Oil & Gas, Mining
- **31 Financials:** Asset Management, Banks, Insurance
- **51 Health Care:** Drug Retailers, Health Care Delivery
- **62 Infrastructure:** Electric Utilities, Real Estate, Waste Mgmt
- **71 Renewable Resources:** Forestry, Pulp & Paper

## Templates
1. SICS sector identification (auto)
2. Industry-specific metric list (typical 6-8 metrics per industry)
3. Materiality map by sector
4. Quantitative metrics calculation guide
5. SEC 10-K integration template
6. ISSB IFRS S1 transition checklist

## Cross-references
- [[gaia-csrd-reporting]] · [[gaia-gri-reporting]] · [[gaia-climate-risk-tcfd]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **gaia-sasb-standards** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in gaia-sasb-standards:**

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
