---
name: helios-hydrogen-strategy
description: Hydrogen strategy — H2 verde, blue, gray. Produção, transporte, certificação. Triggers em "hydrogen", "H2 verde", "green hydrogen", "blue hydrogen", "electrolyser", "Marco Legal H2".
license: SEE-LICENSE
parent_agent: helios-director
---

# HELIOS-HYDROGEN-STRATEGY

## Marco BR
- **Lei 14.948/2024** — Marco Legal Hidrogênio Baixo Carbono
- **Política Nacional Hidrogênio (PNH2)** — Decreto 11.255/2022
- **PROBIO H2** — incentivos
- **Programa Combustível Verde** — H2 + biofuels

## Tipos H2 por cor
- **Cinza:** steam methane reforming (SMR), fóssil
- **Azul:** SMR + CCUS (carbon capture)
- **Verde:** electrolysis com renewable energy
- **Rosa:** electrolysis com nuclear
- **Turquesa:** methane pyrolysis (emerging)

## Custos comparados 2026
- **Gray:** ~US$ 1.50-2.50/kg
- **Blue:** ~US$ 2.50-4.00/kg
- **Green:** ~US$ 3.50-6.00/kg (BR cheaper due to cheap renewables)

## Aplicações
- Industrial: refino, amônia, aço (DRI-EAF)
- Mobilidade pesada: caminhões, navios, aviação
- Energy storage long-duration (seasonal)
- Power-to-X (e-methanol, e-SAF)

## Templates
1. H2 viability assessment (vertical-specific)
2. Electrolyser selection (PEM/Alkaline/SOEC)
3. PPA + electrolyser combined modeling
4. H2 hub feasibility (Pecém, Suape, Açu)
5. CertifHy + H2-BR certification
6. EU CBAM hydrogen impact

## Cross-references
- [[helios-renewable-financing]] · [[helios-carbon-credits-energy]] · [[gaia-transition-planning]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **helios-hydrogen-strategy** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in helios-hydrogen-strategy:**

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
