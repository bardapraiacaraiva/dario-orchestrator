---
name: helios-carbon-credits-energy
description: Carbon credits energia — REC, I-REC, MDL legacy, mercados voluntário e regulado. Triggers em "carbon credits", "REC", "I-REC", "RenovaBio", "MDL", "Verra", "Gold Standard", "EU ETS".
license: SEE-LICENSE
parent_agent: helios-director
---

# HELIOS-CARBON-CREDITS-ENERGY

## Tipos certificados
- **I-REC (International REC):** energy attribute certificate global
- **REC (US):** Renewable Energy Certificate
- **GO (EU):** Guarantee of Origin
- **CBIO (RenovaBio BR):** biocombustíveis
- **VCS / Verra:** voluntary carbon (florestal, energia)
- **Gold Standard:** premium voluntary
- **EU ETS:** EUA (allowances) regulated market

## Mercados BR
- **RenovaBio (Lei 13.576/2017):** CBIOs biocombustíveis
- **SBCE (Sistema Brasileiro Comércio Emissões):** Lei 15.042/2024 — regulated market BR a partir 2026
- **Voluntary BR:** projetos REDD+, ARR Amazônia

## Pricing 2026
- **I-REC BR:** US$ 0.50-2.00/MWh
- **CBIO:** R$ 60-150 (volatile com Inmetro auction)
- **EU ETS EUA:** €60-100/tCO₂
- **VCS Verra:** US$ 3-15/tCO₂ (varies)
- **Gold Standard premium:** US$ 8-30/tCO₂

## Templates
1. Carbon credit strategy (vendor vs buyer)
2. I-REC issuance workflow
3. CBIO compliance (distribuidoras)
4. SBCE BR readiness assessment
5. Voluntary project methodology selection
6. EU ETS allowance management

## Cross-references
- [[helios-ppa-power-purchase]] · [[gaia-carbon-accounting]] · [[gaia-sbti-targets]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **helios-carbon-credits-energy** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in helios-carbon-credits-energy:**

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
