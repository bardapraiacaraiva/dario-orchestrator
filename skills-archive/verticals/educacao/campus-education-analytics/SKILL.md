---
name: campus-education-analytics
description: Learning analytics — engagement, completion, mastery, dropout prediction. xAPI, Caliper. Triggers em "learning analytics", "xAPI", "Caliper", "education analytics", "dropout prediction", "completion rate".
license: SEE-LICENSE
parent_agent: campus-director
compliance: [lgpd_education_marker, model_explainability]
---

# CAMPUS-EDUCATION-ANALYTICS

## Quando usar
- LMS sem dashboard analytics
- High dropout — identificar at-risk students cedo
- Personalização baseada em performance
- Reporting institucional (CPA, conselhos)
- A/B test de conteúdo educacional

## Stack
- **xAPI (Tin Can):** standard de tracking learning experiences
- **Caliper Analytics:** standard IMS Global
- **SCORM:** legacy, ainda em uso
- **Custom event tracking** (Mixpanel/Amplitude/PostHog)

## Métricas
- **Engagement:** time spent, logins/week, content interactions
- **Completion:** % módulos finalizados
- **Mastery:** assessment scores trend
- **Persistence:** retention week-over-week
- **Dropout risk:** ML-predicted

## Templates
1. xAPI/Caliper event taxonomy
2. Dropout prediction model (XGBoost + features behaviorais)
3. Personalization rules (struggling → easier; advancing → harder)
4. Executive dashboard (institutional level)
5. Student-facing dashboard (self-reflection)

## Compliance
- ✓ LGPD especial menores (consentimento responsável)
- ✓ Anonimização para benchmarks
- ✓ Direito à revisão decisão automatizada

## Cross-references
- [[campus-lms-architecture]] · [[demeter-predictive]] · [[demeter-cohort-analysis]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **campus-education-analytics** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in campus-education-analytics:**

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
