---
name: helios-utility-rate-design
description: Utility rate design — tariff structure, ToU, demand charges, social tariffs, dynamic pricing. Triggers em "utility rate design", "tariff design", "ToU", "demand charge", "social tariff", "dynamic pricing", "Reforma Tarifária".
license: SEE-LICENSE
parent_agent: helios-director
compliance: [aneel_compliance_gate]
---

# HELIOS-UTILITY-RATE-DESIGN

## Componentes tarifários BR
- **TUSD (Tarifa Uso Sistema Distribuição):** fio
- **TE (Tarifa Energia):** energia consumida
- **Bandeira tarifária:** verde/amarela/vermelha 1/vermelha 2
- **Encargos setoriais:** CDE, CCRBT, PROINFA
- **Tributos:** ICMS, PIS/COFINS

## Tipos tarifa
- **Convencional B1/B2/B3:** residencial/rural/commercial pequeno
- **Branca:** ToU residencial (3 períodos)
- **Verde:** opção horária A (industrial)
- **Azul:** demanda + energia (industrial alta)
- **Tarifa social:** baixa renda subsidiada

## Reforma Tarifária 2026
- Em implementação ANEEL
- Subsídios cruzados reduction
- TUSD demand mais alocada para grandes
- Adoption de tarifas dinâmicas (real-time)

## Dynamic pricing models
- **ToU (Time-of-Use):** fixed bands (peak/off-peak)
- **CPP (Critical Peak Pricing):** spike eventos críticos
- **RTP (Real-Time Pricing):** wholesale-linked
- **Tiered:** consumption-based blocks

## Templates
1. Tariff structure analysis (per cliente)
2. Class cross-subsidy quantification
3. ToU design (3-period vs hourly)
4. Reforma Tarifária impact por cliente
5. Social tariff eligibility framework
6. Dynamic pricing rollout plan

## Cross-references
- [[helios-aneel-compliance]] · [[helios-mercado-livre-br]] · [[helios-demand-response]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **helios-utility-rate-design** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in helios-utility-rate-design:**

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
