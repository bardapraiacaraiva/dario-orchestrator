---
name: campus-bncc-alignment
description: BNCC alignment — competências, habilidades, objetos de conhecimento. Educação básica. Triggers em "BNCC", "Base Nacional", "competências", "habilidades", "EI EF EM", "currículo escolar".
license: SEE-LICENSE
parent_agent: campus-director
compliance: [bncc_curriculum_alignment]
jurisdiction: Brasil
---

# CAMPUS-BNCC-ALIGNMENT

## Marco
- **BNCC (2017/2018)** — Base Nacional Comum Curricular
- **Resolução CNE/CP 2/2017** — Educação Básica
- **Lei 13.415/2017** — Novo Ensino Médio (40% itinerários formativos)

## Estrutura
- **Competências gerais:** 10 transversais (CG1-CG10)
- **Áreas:** Linguagens, Matemática, Ciências da Natureza, Ciências Humanas, Ensino Religioso
- **Habilidades:** códigos `(EFXXLPYY)` para EF, `(EMXXLPYY)` para EM
- **Objetos de conhecimento:** conteúdos por unidade temática

## Quando usar
- Curriculum mapping (currículo escolar → BNCC)
- Material didático alignment
- Plano de aula BNCC-compliant
- Avaliação por competências/habilidades
- Itinerários formativos EM design

## Templates
1. Curriculum mapping matrix (séries × habilidades BNCC)
2. Plano de aula BNCC (objetivos + habilidades + avaliação)
3. Avaliação por competências (rubrica)
4. Itinerário formativo EM (4 áreas + formação técnica)
5. Material didático BNCC-checklist

## Cross-references
- [[campus-ldb-compliance]] · [[campus-instructional-design]] · [[campus-assessment-design]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **campus-bncc-alignment** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in campus-bncc-alignment:**

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
