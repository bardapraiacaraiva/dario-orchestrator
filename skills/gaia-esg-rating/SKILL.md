---
name: gaia-esg-rating
description: ESG rating optimization — MSCI ESG Ratings, Sustainalytics, S&P Global, CDP. Gap analysis + improvement plan. Triggers em "ESG rating", "MSCI ESG", "Sustainalytics", "S&P Global ESG", "CDP", "ISS ESG".
license: SEE-LICENSE
parent_agent: gaia-director
compliance: [audit_immutable]
---

# GAIA-ESG-RATING

## Quando usar
- Pre-IPO ESG rating preparation
- Annual rating cycle (improve from BBB → A → AA)
- Investor inquiry (sustainability fund requirements)
- M&A ESG due diligence
- Bond issuance (sustainability-linked, green bonds)

## Rating agencies
- **MSCI ESG Ratings:** AAA-CCC scale, industry-relative
- **Sustainalytics:** Risk Rating (0-100, lower=better)
- **S&P Global ESG (DJSI):** 0-100 score, industry leaders
- **CDP:** A-F climate, water, forests
- **ISS ESG:** Prime status (top quartile)
- **Refinitiv ESG Scores**

## Improvement strategies
- **Quick wins (3-6 months):** disclosures completeness, policy gaps
- **Medium (6-12 months):** targets setting, board diversity, controversies management
- **Long-term (12-24 months):** structural change (board composition, supply chain audits)

## Templates
1. Rating agency response templates (CDP, MSCI questionnaire)
2. ESG controversy management playbook
3. Industry peer benchmarking
4. Investor sustainability briefing
5. ESG materiality matrix
6. Improvement roadmap with quarterly milestones

## Cross-references
- [[gaia-csrd-reporting]] · [[gaia-sasb-standards]] · [[gaia-transition-planning]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **gaia-esg-rating** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in gaia-esg-rating:**

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
