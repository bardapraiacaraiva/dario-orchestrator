---
name: gaia-climate-risk-tcfd
description: TCFD climate risk — physical risk (acute, chronic), transition risk (policy, technology, market, reputation), scenario analysis, financial impact. Triggers em "TCFD", "climate risk", "physical risk", "transition risk", "scenario analysis", "climate financial".
license: SEE-LICENSE
parent_agent: gaia-director
compliance: [audit_immutable, csrd_disclosure_gate]
---

# GAIA-CLIMATE-RISK-TCFD

## Marco
- **TCFD (Task Force on Climate-related Financial Disclosures)** — 4 pilares
- **ISSB IFRS S2** — Climate-related disclosures (TCFD-aligned, supersedes TCFD 2024)
- **CSRD ESRS E1** — Climate change (TCFD-aligned)
- **NGFS scenarios** — Network for Greening the Financial System
- **IEA Net Zero scenarios** — World Energy Outlook

## 4 TCFD pillars
1. **Governance:** board + management oversight
2. **Strategy:** physical + transition risks, scenarios
3. **Risk Management:** identification, assessment, integration
4. **Metrics & Targets:** Scope 1+2+3, climate-aligned

## Risk types
- **Physical (acute):** floods, wildfires, hurricanes
- **Physical (chronic):** sea level rise, temperature rise, water stress
- **Transition (policy):** carbon pricing, regulations
- **Transition (technology):** stranded assets, R&D obsolescence
- **Transition (market):** consumer preference shifts, supply chain
- **Transition (reputation):** stakeholder pressure, litigation

## Scenarios típicos
- **1.5°C:** IEA NZE 2050, IPCC SR1.5
- **2°C:** IEA APS, IPCC SSP1-2.6
- **3°C+ (hothouse):** SSP3-7.0, SSP5-8.5

## Templates
1. TCFD disclosure structure
2. Physical risk assessment by location (GIS-based)
3. Transition risk identification matrix
4. Scenario analysis quantitative model
5. Financial impact assessment (NPV at risk)
6. Climate risk register
7. Stress testing framework (banks/insurance)

## Cross-references
- [[gaia-csrd-reporting]] · [[gaia-transition-planning]] · [[zenith-risk-assessment]] · [[zenith-scenario-planning]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **gaia-climate-risk-tcfd** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in gaia-climate-risk-tcfd:**

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
