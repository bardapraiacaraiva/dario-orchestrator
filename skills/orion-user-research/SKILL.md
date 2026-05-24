---
name: orion-user-research
description: User research mixed-methods — interviews, surveys, usability testing, diary studies, ethnographic research. Triggers em "user research", "entrevistas", "usability testing", "survey design", "diary study".
license: MIT
parent_agent: orion-director
compliance: [user_consent_explicit, lgpd_by_design, irb_ethics]
---

# ORION-USER-RESEARCH

## Quando usar
- Programa de research from scratch
- Recruitment strategy + screener design
- Survey design (NPS, CSAT, custom)
- Usability test (moderated/unmoderated)
- Synthesis de findings (affinity mapping)

## Métodos
- **Qualitative:** entrevistas (1:1), focus groups, diary studies, ethnography
- **Quantitative:** surveys, analytics analysis, A/B test results
- **Behavioral:** usability tests, eye tracking, session replays
- **Mixed:** triangulação cross-method

## Stack
- **User interview platforms:** Dovetail, Notably, Condens
- **Recruitment:** UserInterviews, Respondent, Prolific
- **Usability testing:** Maze, UserTesting, Lookback
- **Survey:** Typeform, SurveyMonkey, Google Forms
- **Session replay:** Hotjar, FullStory, LogRocket

## Templates
1. Screener questionnaire
2. Interview discussion guide (~30 min)
3. Survey design checklist (avoid leading Qs)
4. Usability test protocol
5. Synthesis report (insights + quotes + recommendations)

## Compliance
- ✓ Informed consent obrigatório
- ✓ LGPD/GDPR data handling
- ✓ Anonymization de quotes em reports
- ✓ Direito ao esquecimento

## Cross-references
- [[orion-product-discovery]] · [[orion-jobs-to-be-done]] · [[demeter-ab-testing]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **orion-user-research** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in orion-user-research:**

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
