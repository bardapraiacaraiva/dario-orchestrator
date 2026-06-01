---
name: helios-energy-storage
description: BESS — Battery Energy Storage Systems, arbitrage, ancillary services, behind-the-meter. Triggers em "BESS", "energy storage", "battery storage", "arbitrage energy", "ancillary services", "Tesla Megapack", "behind the meter".
license: SEE-LICENSE
parent_agent: helios-director
---

# HELIOS-ENERGY-STORAGE

## Use cases BESS
- **Arbitrage:** charge low price, discharge high (PLD volatility BR)
- **Ancillary services:** frequency regulation, voltage support
- **Demand charge mgmt:** peak shaving for industrial
- **Backup power:** UPS-style, resilience
- **Renewables firming:** smooth solar/wind variability
- **Black start:** restart grid after blackout

## Stack
- **Tesla Megapack** — utility-scale
- **Fluence** — Siemens/AES JV
- **Wartsila** — large hybrid
- **CATL, BYD** — Chinese suppliers
- **Sungrow, Sineng** — inverters + integrated
- **BR:** WEG, partnerships growing

## Economics 2026
- BESS cost: ~US$ 250-350/kWh installed (down from US$ 600 in 2020)
- Lifetime: 10-15 years, 4-6K cycles
- Round-trip efficiency: 85-92%
- IRR projects: 12-20% typical

## Templates
1. BESS sizing calculator (use case-driven)
2. Revenue stack modeling (arbitrage + ancillary)
3. Demand charge mgmt ROI
4. Lifecycle TCO analysis
5. RFP utility-scale BESS
6. Behind-the-meter compliance ANEEL

## Cross-references
- [[helios-grid-integration]] · [[helios-microgrid-design]] · [[helios-demand-response]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **helios-energy-storage** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in helios-energy-storage:**

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
