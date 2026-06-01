---
name: campus-gamification
description: Gamification educacional — Octalysis, badges, progressão, leaderboards. Triggers em "gamification", "Octalysis", "badges", "leaderboard", "progressão", "Yu-kai Chou", "game design education".
license: SEE-LICENSE
parent_agent: campus-director
compliance: [no_dark_patterns]
---

# CAMPUS-GAMIFICATION

## Framework chave
**Octalysis (Yu-kai Chou)** — 8 core drives:
1. Epic meaning & calling
2. Development & accomplishment
3. Empowerment of creativity
4. Ownership & possession
5. Social influence & relatedness
6. Scarcity & impatience
7. Unpredictability & curiosity
8. Loss & avoidance

## Quando usar
- Curso com low engagement
- Onboarding employee training
- Children/teen education
- Behavior change (e.g., learning new language)
- Sales training competitive

## Stack
- **IMS Open Badges:** standard for digital credentials
- **Mozilla Backpack** (legacy)
- **Credly / Accredible:** badge platforms
- **Custom platforms:** XP/levels/leaderboards built-in

## Templates
1. Octalysis analysis canvas
2. Badge design + criteria (IMS Open Badges)
3. Leaderboard mechanics (avoid demotivation)
4. Progression system (levels + unlocks)
5. Streak + spaced repetition (Duolingo-style)

## Anti-patterns
- ❌ Reward em vez de motivação intrínseca (overjustification)
- ❌ Leaderboards que desmotivam bottom 50%
- ❌ Badges sem significado real
- ❌ Punishment-based (penalize miss day)

## Cross-references
- [[campus-learning-experience]] · [[campus-microlearning]] · [[campus-certification]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **campus-gamification** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in campus-gamification:**

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
