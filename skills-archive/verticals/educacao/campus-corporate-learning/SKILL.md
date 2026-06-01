---
name: campus-corporate-learning
description: Corporate L&D — onboarding, upskilling, reskilling, compliance training, leadership development. Triggers em "corporate learning", "L&D", "onboarding employee", "upskilling", "reskilling", "compliance training".
license: SEE-LICENSE
parent_agent: campus-director
compliance: [lgpd_education_marker, audit_trail]
---

# CAMPUS-CORPORATE-LEARNING

## Quando usar
- Onboarding employee program (first 90 days)
- Compliance training (annual, mandatory)
- Upskilling para nova tecnologia
- Reskilling para career transition
- Leadership development program

## Frameworks
- **70-20-10:** 70% on-job + 20% peers + 10% formal
- **Kirkpatrick 4 levels:** reaction → learning → behavior → results
- **Phillips ROI:** Kirkpatrick + level 5 ROI ($)
- **ADDIE for corporate:** instructional design enterprise
- **Agile L&D:** sprints, iterations

## Templates
1. Onboarding 30/60/90 plan
2. Compliance training automation (annual + new hire)
3. Upskilling pathway (skill gap → curriculum)
4. Leadership development program (cohort-based)
5. ROI measurement (Kirkpatrick L4 + L5)

## Stack
- **LMS:** Cornerstone, Workday Learning, Docebo, TalentLMS
- **LXP:** Degreed, EdCast, Cornerstone Insights
- **Content libraries:** LinkedIn Learning, Coursera Business, Udemy Business

## Cross-references
- [[campus-microlearning]] · [[campus-certification]] · [[pessoa-learning]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **campus-corporate-learning** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in campus-corporate-learning:**

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
