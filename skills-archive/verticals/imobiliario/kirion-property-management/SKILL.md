---
name: kirion-property-management
description: Property management — leases, maintenance, tenant ops, ALD/AL PT. Triggers em "property management", "gestão imobiliária", "ALD", "AL Portugal", "Alojamento Local", "tenant management", "maintenance".
license: SEE-LICENSE
parent_agent: kirion-director
---

# KIRION-PROPERTY-MANAGEMENT

## Modelos
- **Long-term residential:** lease contracts 1-5 years
- **Short-term (Airbnb-style):** AL Portugal, Airbnb arbitrage
- **Commercial:** retail, office leases
- **Industrial/logistics:** warehouses, distribution
- **Mixed-use:** ground floor retail + residential above

## PT specifics — AL (Alojamento Local)
- **Decreto-Lei 128/2014 + DL 80/2024** Cláusula Travão
- **Registo AL** obrigatório
- **Categorias:** apartamento, moradia, estabelecimento hospedagem
- **Limitações por zona** (Lisboa, Porto centro restritivos)
- **IRS Categoria F** (renda) vs **Categoria B** (atividade comercial)

## Operations key
- **Tenant screening:** credit, references, fitness checks
- **Lease management:** renewal, indexação INE PT, rescisão
- **Maintenance:** preventive + reactive scheduling
- **Vacancy management:** marketing + turnover SLA
- **Rent collection:** automation + delinquency workflow

## Stack
- **Yardi, RealPage, AppFolio:** enterprise líderes
- **MRI Software, Buildium:** mid-market
- **BR-specific:** Superlógica, Group Software
- **PT-specific:** UniRENTAL, AreaCO

## Templates
1. Tenant screening rubric (BR + PT)
2. Lease agreement templates
3. Maintenance schedule (preventive + reactive)
4. Vacancy marketing playbook
5. Rent collection workflow + dunning
6. AL Portugal compliance checklist

## Cross-references
- [[kirion-leasing-strategy]] · [[kirion-hospitality-management]] · [[lex-imobiliario]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **kirion-property-management** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in kirion-property-management:**

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
