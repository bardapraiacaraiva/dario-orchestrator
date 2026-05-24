---
name: helios-energy-efficiency-iso50001
description: ISO 50001 EnMS, M&V Protocol, ESCO contracts, energy efficiency audits. Triggers em "ISO 50001", "EnMS", "energy management", "energy efficiency", "ESCO", "M&V", "IPMVP", "energy audit".
license: SEE-LICENSE
parent_agent: helios-director
compliance: [iso50001_certification_ready, audit_immutable]
---

# HELIOS-ENERGY-EFFICIENCY-ISO50001

## Marco
- **ISO 50001:2018** — Energy Management Systems (EnMS)
- **ISO 50004:** EnMS implementation guidance
- **ISO 50006:** Energy baselines + EnPI (Energy Performance Indicators)
- **IPMVP:** International Performance M&V Protocol
- **EVO (Efficiency Valuation Organization)**

## EnMS components (PDCA)
- **Plan:** energy review, baseline, EnPIs, objectives, plans
- **Do:** implement plans, operational controls
- **Check:** monitoring, measurement, audits
- **Act:** management review, continual improvement

## IPMVP M&V Options
- **A:** retrofit isolation, key parameter measurement
- **B:** retrofit isolation, all parameter measurement
- **C:** whole facility (utility bills)
- **D:** calibrated simulation (energy models)

## ESCO contracts
- **Shared savings:** ESCO finances, shares savings
- **Guaranteed savings:** customer finances, ESCO guarantees
- **Chauffage:** ESCO owns + operates + bills customer
- **EPC (Energy Performance Contract):** standardized

## Templates
1. ISO 50001 implementation roadmap
2. Energy review + baseline
3. EnPI selection (kWh/unit, kWh/m²)
4. ESCO contract template (5 modalities)
5. M&V plan per IPMVP option
6. Annual EnMS management review

## Cross-references
- [[helios-smart-meter-data]] · [[gaia-csrd-reporting]] · [[gaia-sbti-targets]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **helios-energy-efficiency-iso50001** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in helios-energy-efficiency-iso50001:**

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
