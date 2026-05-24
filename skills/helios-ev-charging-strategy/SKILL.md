---
name: helios-ev-charging-strategy
description: EV charging — infrastructure, fast charging, V2G, fleet electrification, charge points. Triggers em "EV charging", "estações carregamento", "fast charging", "V2G", "vehicle to grid", "fleet electrification", "ChargePoint", "EVgo".
license: SEE-LICENSE
parent_agent: helios-director
---

# HELIOS-EV-CHARGING-STRATEGY

## Charging levels
- **Level 1 (slow):** AC 1.4-1.9 kW, 8-20h full charge
- **Level 2 (medium):** AC 3.3-19.2 kW, 4-8h full
- **DC Fast (Level 3):** 25-150 kW, 30-60min 80%
- **Ultra-Fast (XFC):** 150-350 kW, 15-30min 80%
- **Tesla Supercharger V4:** up to 350 kW

## Connector standards
- **Type 2 (Mennekes):** EU AC standard
- **CCS Combo 2:** EU DC fast
- **CHAdeMO:** Japan DC fast (declining)
- **GB/T:** China standard
- **NACS (Tesla, now SAE J3400):** becoming US standard

## Business models
- **CPO (Charge Point Operator):** own + operate stations
- **eMSP (e-Mobility Service Provider):** customer-facing app/billing
- **Roaming:** cross-network access
- **Workplace:** employer-provided
- **Fleet:** depot charging private
- **Public:** highway + urban DC fast

## V2G (Vehicle-to-Grid)
- EV battery sells back to grid
- Pilots Nissan, Ford, Hyundai
- Regulatory + warranty challenges
- DERMS integration required

## Templates
1. Charging infrastructure site selection
2. CPO business model
3. Fleet electrification roadmap
4. V2G pilot framework
5. Charging tariff design
6. Roaming agreement template

## Cross-references
- [[helios-grid-integration]] · [[helios-demand-response]] · [[helios-microgrid-design]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **helios-ev-charging-strategy** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in helios-ev-charging-strategy:**

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
