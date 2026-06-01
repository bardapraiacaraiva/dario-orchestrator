---
name: kirion-hospitality-management
description: Hospitality — hotels, hostels, short-term rentals, AL Portugal, golden visa stays. Triggers em "hospitality", "hotel management", "hostel", "Airbnb arbitrage", "Alojamento Local PT", "RevPAR", "ADR", "occupancy".
license: SEE-LICENSE
parent_agent: kirion-director
---

# KIRION-HOSPITALITY-MANAGEMENT

## Métricas chave
- **Occupancy:** Rooms sold / Rooms available
- **ADR (Average Daily Rate):** Room revenue / Rooms sold
- **RevPAR (Revenue Per Available Room):** ADR × Occupancy = Room revenue / Rooms available
- **TRevPAR:** Total revenue per available room (inc F&B, spa)
- **GOP (Gross Operating Profit):** before management fees + insurance
- **GOPPAR:** GOP / Rooms available
- **NOI hotel:** GOP - Management fees - FF&E reserve - Insurance - Taxes

## Operating models
- **Owned + operated:** full integration
- **Managed:** owner + brand operator (Marriott, Hilton)
- **Franchised:** owner uses brand + flag fee
- **Leased:** owner rents to operator (fixed + variable)

## Channels distribution
- **Direct (brand.com):** highest margin
- **OTAs (Booking.com, Expedia, Airbnb):** 15-25% commission
- **GDS (corporate):** Sabre, Amadeus
- **TMCs (Travel Mgmt Companies):** corporate negotiated
- **Wholesalers:** tour operators

## Templates
1. Hotel financial model (P&L 10y)
2. Comp set RevPAR analysis (STR-style)
3. Channel mix optimization
4. Branded vs independent decision
5. Capex reserve schedule
6. F&B segmentation (banquets, restaurant, room service)

## Cross-references
- [[kirion-property-management]] · [[kirion-golden-visa-pt]] · [[atlas-tech]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **kirion-hospitality-management** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in kirion-hospitality-management:**

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
