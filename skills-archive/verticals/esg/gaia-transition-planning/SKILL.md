---
name: gaia-transition-planning
description: Net-zero transition planning — decarbonization roadmap, CapEx prioritization, just transition. Triggers em "transition plan", "net zero plan", "decarbonization roadmap", "climate transition", "just transition".
license: SEE-LICENSE
parent_agent: gaia-director
compliance: [audit_immutable, csrd_disclosure_gate, ghg_protocol_verification]
---

# GAIA-TRANSITION-PLANNING

## Quando usar
- Net-zero commitment operationalization
- CSRD ESRS E1 transition plan disclosure (mandatory)
- CapEx alignment with climate goals
- Sector transition (oil & gas → renewables)
- Investor transition plan inquiries (CA100+, TPI)

## Marcos
- **CSRD ESRS E1-1** — transition plan mandatory
- **GFANZ** — Glasgow Financial Alliance Net Zero, transition plan guidance
- **TPT** — UK Transition Plan Taskforce
- **CDP** — climate transition plan reporting
- **CA100+** — Climate Action 100+ benchmark
- **Just Transition Centre** — equitable transition principles

## Transition plan components
1. **Ambition:** science-based target (SBTi validated)
2. **Action:** decarbonization levers (efficiency, renewables, electrification, CCUS)
3. **Accountability:** governance, KPIs, executive comp linkage
4. **Engagement:** value chain (suppliers, customers), policy
5. **Just Transition:** workforce, communities affected
6. **Disclosure:** annual progress, climate financial implications

## MACC (Marginal Abatement Cost Curve)
- Cost per tCO₂e avoided per intervention
- Prioritize negative-cost (savings) → low-cost → high-cost
- Sequence interventions for CapEx planning

## Templates
1. Transition plan structure (TPT-aligned, 5 chapters)
2. Decarbonization levers list per industry
3. MACC analysis template
4. CapEx roadmap (5-10y)
5. Just Transition workforce assessment
6. Annual progress disclosure
7. Internal carbon price model

## Cross-references
- [[gaia-sbti-targets]] · [[gaia-climate-risk-tcfd]] · [[gaia-csrd-reporting]] · [[zenith-capital-allocation]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **gaia-transition-planning** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in gaia-transition-planning:**

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
