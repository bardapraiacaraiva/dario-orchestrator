---
name: kirion-smart-building
description: Smart buildings — IoT, BMS/BAS, energy mgmt, occupancy analytics, digital twins. Triggers em "smart building", "BMS", "BAS", "IoT building", "digital twin", "Niagara", "Honeywell", "Siemens Building".
license: SEE-LICENSE
parent_agent: kirion-director
---

# KIRION-SMART-BUILDING

## Layers
- **Sensors/IoT:** occupancy, environmental, energy
- **Connectivity:** BACnet, Modbus, LoRaWAN, 5G
- **BAS/BMS (Building Automation):** HVAC, lighting, access control
- **Analytics platform:** energy mgmt, fault detection, predictive maintenance
- **Digital twin:** virtual model (BIM-derived)

## Stack
- **Niagara (Honeywell):** open framework
- **Siemens Building X**
- **Schneider EcoStruxure Building**
- **Johnson Controls OpenBlue**
- **Switch Automation (now Honeywell):** platform
- **BR:** Inova, Buildsim

## Use cases ROI
- **Energy savings 15-30%:** HVAC optimization, lighting scheduling
- **Predictive maintenance:** avoid equipment failures (-30% downtime)
- **Occupancy optimization:** right-size space (post-pandemic hybrid)
- **Tenant experience:** apps, mobile access control
- **ESG reporting:** automated CSRD data
- **Cybersec:** OT security (Stuxnet-style threats)

## Templates
1. Smart building strategy roadmap
2. IoT sensor deployment plan
3. BMS upgrade RFP
4. Digital twin scope definition
5. Energy savings business case
6. OT cybersec assessment

## Cross-references
- [[helios-smart-meter-data]] · [[kirion-esg-real-estate]] · [[aegis-iam-identity]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **kirion-smart-building** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in kirion-smart-building:**

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
