---
name: gaia-carbon-accounting
description: Carbon accounting GHG Protocol — Scope 1+2+3 calculation, emissions factor library, audit trail. Triggers em "carbon accounting", "GHG Protocol", "Scope 1 2 3", "emissions inventory", "carbon footprint".
license: SEE-LICENSE
parent_agent: gaia-director
compliance: [ghg_protocol_verification, audit_immutable]
---

# GAIA-CARBON-ACCOUNTING

## Quando usar
- GHG inventory greenfield (empresa primeira vez)
- Scope 3 deep dive (supplier emissions, upstream)
- CDP submission preparation
- M&A acquisition emissions integration
- Annual recalculation + base year update

## Marco normativo
- **GHG Protocol Corporate Standard** — Scope 1+2 (mandatory)
- **GHG Protocol Scope 3 Standard** — 15 categorias
- **ISO 14064-1** — quantification + reporting GHG
- **PAS 2060** — carbon neutrality demonstration
- **SBTi Corporate Net-Zero Standard** — alignment

## Workflow
```
1. Organizational boundary (operational/financial/equity control)
2. Operational boundary (Scope 1 direct, Scope 2 energy, Scope 3 value chain)
3. Base year selection + recalculation policy
4. Data collection (fuel, electricity, travel, suppliers)
5. Emissions factors (DEFRA, EPA, IEA, ecoinvent)
6. Calculation + uncertainty analysis
7. Verification (limited/reasonable assurance)
8. Reporting (CDP, CSRD, B3)
```

## Templates
1. Organizational boundary decision matrix
2. Emissions factor library (DEFRA + Brasil/PT specific)
3. Scope 3 screening (15 categorias relevance)
4. Supplier emissions data collection form
5. Annual GHG inventory report
6. Verification scope document (ISO 14064-3)

## Cross-references
- [[gaia-csrd-reporting]] · [[gaia-sbti-targets]] · [[gaia-supply-chain-esg]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **gaia-carbon-accounting** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in gaia-carbon-accounting:**

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
