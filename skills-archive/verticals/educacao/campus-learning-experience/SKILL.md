---
name: campus-learning-experience
description: Learning Experience Design (LXD) — engagement, flow, motivation, social learning. Triggers em "LXD", "learning experience", "engagement educacional", "flow state", "social learning".
license: SEE-LICENSE
parent_agent: campus-director
compliance: [lgpd_education_marker]
---

# CAMPUS-LEARNING-EXPERIENCE

## Filosofia
**LXD = ID + UX + behavioral psychology.** Cursos não morrem por mau conteúdo; morrem por má experiência.

## Quando usar
- Curso com low completion rate (<30%)
- UX redesign de LMS interno
- Cohort-based course launch
- Corporate L&D platform
- Mobile-first learning

## Frameworks
- **Csikszentmihalyi Flow:** desafio = habilidade
- **Self-Determination Theory (Deci/Ryan):** autonomy + competence + relatedness
- **Cognitive Load Theory:** intrinsic + extraneous + germane
- **Dual Coding:** verbal + visual
- **Generation Effect:** explicar > absorver

## Templates
1. Course experience canvas (touchpoints + emotions)
2. Onboarding sequence design (first 7 days)
3. Notifications/nudges plan (without dark patterns)
4. Social learning features (cohorts, peer review)
5. Mobile-first content adaptation

## Anti-patterns
- ❌ 1h videos sem chunking
- ❌ Quiz no fim com 50 perguntas
- ❌ Forum sem participação obrigada/incentivada
- ❌ Conteúdo idêntico desktop/mobile

## Cross-references
- [[campus-instructional-design]] · [[campus-microlearning]] · [[campus-gamification]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **campus-learning-experience** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in campus-learning-experience:**

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
