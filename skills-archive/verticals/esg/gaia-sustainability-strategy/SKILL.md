---
name: gaia-sustainability-strategy
description: Sustainability strategy — double materiality assessment, strategy roadmap, ESG governance integration. Triggers em "sustainability strategy", "ESG strategy", "double materiality", "sustainability roadmap".
license: SEE-LICENSE
parent_agent: gaia-director
compliance: [audit_immutable]
---

# GAIA-SUSTAINABILITY-STRATEGY

## Quando usar
- Greenfield sustainability strategy
- Post-IPO sustainability commitment (signal to market)
- Industry transition (oil&gas → renewables, automotive → EV)
- B-Corp certification preparation
- M&A sustainability integration

## Frameworks
- **Double materiality (CSRD):** impact materiality × financial materiality
- **SASB materiality map:** industry-specific
- **GRI material topics:** stakeholder-driven
- **AA1000:** stakeholder engagement standard
- **Theory of Change:** social impact framework
- **Future-Fit Business Benchmark:** science-based targets

## Workflow
```
1. Stakeholder mapping + engagement
2. Material topics longlist (50-100 topics)
3. Impact assessment (positive/negative, severity, probability)
4. Financial materiality assessment
5. Materiality matrix (2x2)
6. Strategy pillars (3-5 themes)
7. Targets + KPIs per pillar
8. Governance structure
9. Resource allocation
10. Communication plan
```

## Templates
1. Stakeholder map + engagement plan
2. Double materiality assessment template (CSRD compliant)
3. Sustainability strategy 1-pager (executive)
4. Strategy on a Page deck (board)
5. ESG KPI dashboard structure
6. Sustainability governance RACI

## Cross-references
- [[gaia-csrd-reporting]] · [[gaia-governance-frameworks]] · [[gaia-sbti-targets]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **gaia-sustainability-strategy** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in gaia-sustainability-strategy:**

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
