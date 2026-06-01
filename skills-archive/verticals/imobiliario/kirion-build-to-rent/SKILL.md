---
name: kirion-build-to-rent
description: BTR — Build-to-Rent, multifamily institutional, residentials yields. Triggers em "BTR", "Build-to-Rent", "multifamily", "residential institutional", "PRS", "co-living", "single family rental".
license: SEE-LICENSE
parent_agent: kirion-director
---

# KIRION-BUILD-TO-RENT

## Conceito
**BTR = institutional landlord builds purpose-designed residential rental.** Different from condo (for-sale). Long-term hold (15-25 years).

## Sub-categorias
- **Multifamily:** apartment buildings 50+ units
- **Co-living:** shared amenities (Common, Welive, BR: Yuca, Hub)
- **Single Family Rental (SFR):** scattered houses (US líder, Brookfield, Invitation Homes)
- **Build-to-Rent communities:** purpose-built clusters
- **PRS (Private Rented Sector — UK terminology)**

## Investment thesis
- Stable cash flow (residential more recession-resistant)
- Inflation hedge (rents adjust)
- Demographic tailwinds (urbanization, smaller households)
- ESG positive (housing affordability narrative)

## Yields típicos BR/PT/Global
- **BR multifamily São Paulo:** 7-9% gross / 5-7% net
- **PT Lisboa multifamily:** 4-5% gross (low yield premium urban)
- **US multifamily:** 4-6% (institutional Class A)
- **UK PRS:** 4-6%

## Templates
1. BTR feasibility study
2. Underwriting model BTR (10y hold)
3. Operating expense benchmarks
4. Resident profile segmentation
5. Amenity design ROI (gym, coworking, etc.)
6. Property management partner RFP

## Cross-references
- [[kirion-dcf-property]] · [[kirion-property-management]] · [[kirion-fii-br]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **kirion-build-to-rent** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in kirion-build-to-rent:**

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
