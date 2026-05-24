---
name: skill-restaurante-pt
description: "Posicionamento completo para restaurantes em Portugal: marca sensorial, naming gastronómico, oferta experiencial, storytelling e SEO local. COMPOSED SKILL — combina dario-brand, dario-naming, dario-offer, dario-story-circle, seo-local para restaurante em Portugal. Triggers: 'restaurante', 'gastronomia', 'chef', 'menu', 'comida portuguesa'."
license: MIT
---

# Restaurante Portugal Specialist

Skill composto gerado automaticamente pelo DARIO Skill Composer.
Combina o melhor de 5 skills para o nicho **restaurante** em **Portugal**.

## Skills Base

- `dario-brand`
- `dario-naming`
- `dario-offer`
- `dario-story-circle`
- `seo-local`

## Quando activar

- User menciona: 'restaurante', 'gastronomia', 'chef', 'menu', 'comida portuguesa'
- Projecto para restaurante em Portugal
- Qualquer tarefa que combine dario-brand + dario-naming + dario-offer + dario-story-circle + seo-local

## Workflow

Executar os skills base em sequência, adaptando o output de cada um ao nicho restaurante:

1. **dario-brand** — adaptar output para restaurante
2. **dario-naming** — adaptar output para restaurante
3. **dario-offer** — adaptar output para restaurante
4. **dario-story-circle** — adaptar output para restaurante
5. **seo-local** — adaptar output para restaurante

Cada step deve considerar o contexto de restaurante em Portugal e aplicar o conhecimento do nicho abaixo.

## Conhecimento do Nicho (aprendido por IA)

Baseado em 6 execuções anteriores para 'restaurante':

- Para 'restaurante', dario-brand tem score médio de 90% (7% acima da média global). Padrão de sucesso: 'storytelling sensorial'. Baseado em 8 execuções.
- Para 'restaurante', dario-offer tem score médio de 86% (5% acima da média global). Padrão de sucesso: 'experiência > preço'. Baseado em 5 execuções.

### O que funciona neste nicho:
- **archetype Creator** (comprovado 2x)
- **experiência > preço** (comprovado 1x)
- **bonus exclusivo** (comprovado 1x)
- **garantia emocional** (comprovado 1x)
- **storytelling sensorial** (comprovado 1x)

### O que evitar neste nicho:
- ~~demasiado formal~~ (falhou 1x)

## Instruções Específicas

Sempre usar tom quente e sensorial. Referências à gastronomia portuguesa. Archetype Creator é o default para restaurantes.

## Red Flags

- Não usar abordagens genéricas — este skill é ESPECÍFICO para restaurante
- Consultar skill_memory antes de executar (GET /skill-memory/brief/skill-restaurante-pt)
- Se score < 70, consultar learning pool (GET /learning/recommend/skill-restaurante-pt/restaurante)


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **skill-restaurante-pt** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in skill-restaurante-pt:**

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
