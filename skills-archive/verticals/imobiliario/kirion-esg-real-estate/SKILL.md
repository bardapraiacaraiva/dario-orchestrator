---
name: kirion-esg-real-estate
description: ESG real estate — LEED, BREEAM, WELL, GRESB, green building, embodied carbon. Triggers em "ESG real estate", "LEED", "BREEAM", "WELL", "GRESB", "green building", "embodied carbon", "net zero building".
license: SEE-LICENSE
parent_agent: kirion-director
---

# KIRION-ESG-REAL-ESTATE

## Certifications
- **LEED (US):** Leadership Energy Environmental Design (Platinum/Gold/Silver/Certified)
- **BREEAM (UK):** Building Research Establishment Environmental Assessment Method
- **WELL Building Standard:** focus health + wellbeing
- **GRESB:** ESG benchmark for real estate funds
- **EDGE (IFC):** emerging markets (BR included)
- **AQUA-HQE (BR):** Alta Qualidade Ambiental

## ESG REIT scoring (GRESB)
- **Management score:** 30%
- **Performance score:** 70% (energy, water, GHG, waste)
- **Anos consecutivos GRESB:** signaling effect
- **5-Star, 4-Star, 3-Star, etc.:** ranking

## Embodied vs operational carbon
- **Operational:** energy use post-occupancy (~70% total over 60y typical)
- **Embodied:** construction materials (~30%)
- **Net zero:** address ambos

## Materials baixo carbono
- **CLT (Cross-Laminated Timber):** wooden structures
- **Low-carbon concrete:** GGBS, fly ash replacement
- **Recycled steel:** lower embodied
- **Biobased insulation:** cork, sheep wool

## Templates
1. LEED/BREEAM certification roadmap
2. GRESB submission framework
3. Building energy modeling (EnergyPlus, IES)
4. Embodied carbon LCA
5. Green building business case
6. Tenant ESG engagement

## Cross-references
- [[gaia-csrd-reporting]] · [[helios-energy-efficiency-iso50001]] · [[kirion-smart-building]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **kirion-esg-real-estate** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in kirion-esg-real-estate:**

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
