---
name: helios-ppa-power-purchase
description: PPA structuring — sleeve, virtual, physical, corporate PPA. Triggers em "PPA", "Power Purchase Agreement", "sleeve PPA", "virtual PPA", "physical PPA", "corporate PPA", "RE100".
license: SEE-LICENSE
parent_agent: helios-director
---

# HELIOS-PPA-POWER-PURCHASE

## Tipos PPA
- **Physical PPA:** delivery física de energia (mesma rede)
- **Sleeve PPA:** comercializadora intermedia (BR comum)
- **Virtual PPA (VPPA):** financeiro, sem entrega física (cross-region)
- **Onsite PPA:** generation in customer premises (rooftop solar)
- **Offsite PPA:** generation remote (utility-scale solar/wind)

## Termos típicos PPA
- **Duração:** 10-25 anos (utility-scale) / 5-15 anos (corporate)
- **Pricing:** fixed, indexed (CPI), tiered, hybrid
- **Volume:** fixed MWh, % of output, pay-as-produced
- **Risk allocation:** weather, curtailment, transmission

## Corporate PPA grandes
- Google, Amazon, Microsoft (RE100 commitments)
- BR: Vale (eólica), Suzano (solar), Klabin (biomassa)
- Pricing typical 2026: R$ 180-220/MWh solar, R$ 200-280/MWh eólica

## Templates
1. PPA term sheet template
2. RE100 commitment alignment
3. PPA pricing comparison (fixed vs indexed)
4. Curtailment risk allocation
5. Credit support (LC, parent guarantee)
6. PPA modeling (financial impact 10y)

## Cross-references
- [[helios-renewable-financing]] · [[helios-carbon-credits-energy]] · [[gaia-transition-planning]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **helios-ppa-power-purchase** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in helios-ppa-power-purchase:**

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
