---
name: gaia-esg-due-diligence
description: ESG due diligence — M&A pre-acquisition ESG diligence, integration risk, value creation. Triggers em "ESG due diligence", "M&A ESG", "sustainability due diligence", "ESG integration M&A".
license: SEE-LICENSE
parent_agent: gaia-director
compliance: [audit_immutable, csrd_disclosure_gate]
---

# GAIA-ESG-DUE-DILIGENCE

## Quando usar
- Pre-acquisition ESG diligence
- Sell-side ESG vendor due diligence
- PE portfolio company ESG baselining
- Joint venture ESG alignment
- Strategic partnership evaluation

## ESG DD categorias
- **Environmental:** GHG emissions baseline, regulatory exposure, contaminated sites, water/waste, biodiversity, stranded assets
- **Social:** workforce, modern slavery, community impact, customer welfare
- **Governance:** board diversity, ethics, anti-corruption, whistleblower, related-party
- **Compliance:** regulatory fines history, litigation, sanctions exposure
- **Reputational:** controversies, social media analysis, stakeholder relationships

## Workflow
```
1. Pre-LOI screening (red flags)
2. Confirmatory due diligence (data room access)
3. Site visits (selective, high-risk locations)
4. Interviews (management, employees, suppliers)
5. Third-party verification (background, public records)
6. Findings report + risk-adjusted valuation
7. Integration plan (Day 1 to Day 100)
8. Post-acquisition monitoring
```

## Templates
1. ESG DD request list (200+ items)
2. Red flags checklist (deal-breaker indicators)
3. Climate risk quick assessment
4. Modern slavery screening tool
5. Findings report structure (executive + detail)
6. Risk-adjusted valuation framework
7. Integration playbook (ESG harmonization)

## Risk categorias
- **Deal-breakers:** sanctions, fraud, severe human rights
- **High:** material env liabilities, ongoing investigations, governance failures
- **Medium:** disclosure gaps, target misalignment, supply chain risks
- **Low:** minor compliance gaps, optimization opportunities

## Cross-references
- [[gaia-supply-chain-esg]] · [[zenith-ma-evaluation]] · [[aegis-third-party-risk]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **gaia-esg-due-diligence** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in gaia-esg-due-diligence:**

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
