---
name: demeter-data-storytelling
description: Data storytelling — executive narratives, slide decks data-driven, Tableau Story Points. Comunicar insights para não-técnicos. Triggers em "data storytelling", "executive presentation", "data slides", "narrative", "story points", "data visualization narrative".
license: MIT
parent_agent: demeter-director
compliance: [data_integrity, no_misleading_charts]
---

# DEMETER-DATA-STORYTELLING — Insights → Acção

## Filosofia
**Análise técnica sem narrativa = report ignorado.** Storytelling traduz p-values em decisões.

## Quando usar
- Apresentação executiva pós-A/B test
- QBR (Quarterly Business Review)
- Board pack / investor update
- Pitch deck com dados
- Post-mortem de experiment
- Annual report

## Frameworks
- **Pyramid Principle (McKinsey):** conclusão first, depois suporte
- **SCQA:** Situation → Complication → Question → Answer
- **STAR:** Situation → Task → Action → Result
- **Hero's Journey:** desafio → insight → resolução
- **Cole Nussbaumer Knaflic:** "Storytelling with Data" framework

## Templates
1. Executive 1-slide summary (recomendação + 3 razões)
2. A/B test result slides (10 slides: hipótese → setup → resultados → recomendação)
3. QBR deck (15 slides: highlights + lowlights + ações)
4. Board pack (5 metrics + commentary + outlook)
5. Pitch deck data section (TAM/SAM/SOM + traction)

## Princípios de visual design
- **Highlight é mais importante que beleza:** uma cor para focal point, resto grayscale
- **Title como takeaway:** "Revenue cresceu 30%" não "Revenue Q4 2025"
- **Annotate context:** anotação na curva explicando spike
- **Remove chart junk:** Tufte data-ink ratio
- **Order matters:** ordenar bars por value, não alphabetical

## Anti-patterns (chart crimes)
- ❌ Pie chart com 8 fatias
- ❌ Y-axis truncado para inflar visual
- ❌ 3D anything
- ❌ Dual-axis sem cor consistente
- ❌ Legenda fora do contexto (use direct labels)

## Cross-references
- [[demeter-bi-dashboard]] — visualizações
- [[demeter-ab-testing]] — reportar resultados
- [[dario-pitch]] — pitch frameworks
- [[a360-pitch]] — investor decks


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **demeter-data-storytelling** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in demeter-data-storytelling:**

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
