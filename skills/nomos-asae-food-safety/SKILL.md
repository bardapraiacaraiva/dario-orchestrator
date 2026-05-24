---
name: nomos-asae-food-safety
description: ASAE compliance — Autoridade Segurança Alimentar e Económica PT, HACCP, food labelling, alvarás. Triggers em "ASAE", "segurança alimentar PT", "HACCP", "rotulagem alimentar", "alvará restaurante", "inspeção ASAE".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [audit_immutable]
jurisdiction: Portugal
---

# NOMOS-ASAE-FOOD-SAFETY

## Marco
- **DL 113/2006** — segurança alimentar
- **Regulamento (CE) 852/2004** — higiene alimentos
- **Regulamento (CE) 853/2004** — higiene origem animal
- **Regulamento (UE) 1169/2011** — informação alimentar consumidor
- **DL 26/2016** — venda directa
- **Lei 25/2019** — fast food restrições
- **DL 10/2015** — turismo + restauração (RJACSR)

## Quando usar
- Abertura restaurante/café/cantina (alvará)
- HACCP implementation (mandatory)
- Inspeção ASAE preparação ou resposta
- Recall de produto alimentar
- Rotulagem novos produtos
- Cantinas escolares/hospitalares compliance

## Templates
1. HACCP plan (7 princípios)
2. Plano higiene (limpeza + desinfecção)
3. Plano controlo de pragas
4. Rastreabilidade (forward + backward)
5. Rotulagem checklist (alergénios, valor nutricional)
6. Inspeção ASAE preparation checklist
7. Recall protocol + comunicação

## Coimas típicas ASAE
- Falta de licenciamento: €500-44.000
- Higiene grave: €2.500-22.000
- Rotulagem incorrecta: €750-3.700
- HACCP ausente: €1.500-44.000

## Cross-references
- [[nomos-acss-healthcare-pt]] · [[lex-administrativo]] · [[medik-anvisa-regulatory]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-asae-food-safety** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-asae-food-safety:**

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
