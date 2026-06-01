---
name: campus-ead-regulation
description: EAD regulação — Decreto 9.057/2017, Portaria MEC 2.117/2019, polos EAD. Triggers em "EAD", "ensino a distância", "Decreto 9057", "polos EAD", "credenciamento EAD".
license: SEE-LICENSE
parent_agent: campus-director
compliance: [mec_credenciamento, audit_trail]
jurisdiction: Brasil
---

# CAMPUS-EAD-REGULATION

## Marco
- **Decreto 9.057/2017** — Marco EAD
- **Portaria Normativa MEC 2.117/2019** — 40% EAD em presencial
- **Portaria MEC 11/2017** — Sistema CapacEAD
- **Resolução CNE/CES 1/2016** — Pós-graduação a distância

## Modalidades
- **100% EAD:** graduação totalmente a distância (carga horária presencial somente para avaliações)
- **Híbrido:** até 40% EAD em curso presencial (sem credenciamento adicional)
- **Semi-presencial:** modalidade pós-graduação

## Quando usar
- Credenciamento institucional EAD
- Solicitar autorização polo EAD
- Adequação curricular hybrid (40%)
- AVA selection (Moodle, Canvas, Brightspace)
- Compliance auditoria MEC EAD

## Templates
1. Solicitação credenciamento institucional EAD
2. Polo EAD setup (infraestrutura + tutoria)
3. PPC EAD template
4. Adequação 40% híbrido (curso presencial)
5. AVA selection scorecard

## Cross-references
- [[campus-mec-regulation]] · [[campus-lms-architecture]] · [[campus-online-course-pedagogy]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **campus-ead-regulation** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in campus-ead-regulation:**

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
