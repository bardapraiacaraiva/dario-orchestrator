---
name: campus-mec-regulation
description: MEC regulation BR — credenciamento, Sinaes, ENADE, recredenciamento. Triggers em "MEC", "credenciamento", "Sinaes", "ENADE", "INEP", "recredenciamento", "autorização curso".
license: SEE-LICENSE
parent_agent: campus-director
compliance: [mec_credenciamento, audit_trail]
jurisdiction: Brasil
---

# CAMPUS-MEC-REGULATION

## Quando usar
- Credenciamento de IES (novo) ou polos EAD
- Recredenciamento (5 anos)
- Autorização de novo curso
- Reconhecimento de curso
- Visita in loco MEC (preparação)
- Resposta a notificação INEP

## Marco
- **Decreto 9.235/2017** — Credenciamento/recredenciamento IES
- **Portaria Normativa MEC 23/2017** — Procedimentos
- **Decreto 9.057/2017** — EAD
- **Lei 10.861/2004 (Sinaes)** — Avaliação
- **Portaria MEC 2.117/2019** — 40% EAD em presencial

## Templates
1. PDI (Plano de Desenvolvimento Institucional) template
2. PPC (Projeto Pedagógico de Curso) template
3. Auto-avaliação CPA (Comissão Própria Avaliação)
4. Preparação visita in loco INEP
5. Recurso administrativo MEC

## Métricas chave
- **CI (Conceito Institucional):** 1-5
- **IGC (Índice Geral de Cursos):** 1-5
- **CC (Conceito Curso):** 1-5
- **CPC (Conceito Preliminar Curso):** computado
- **ENADE:** referência

## Cross-references
- [[campus-ead-regulation]] · [[campus-enem-enade-prep]] · [[lex-administrativo]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **campus-mec-regulation** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in campus-mec-regulation:**

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
