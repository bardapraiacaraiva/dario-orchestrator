---
name: campus-microlearning
description: Microlearning — spaced repetition, just-in-time learning, mobile-first. Triggers em "microlearning", "spaced repetition", "Anki", "Duolingo-style", "just-in-time learning".
license: SEE-LICENSE
parent_agent: campus-director
compliance: [no_dark_patterns]
---

# CAMPUS-MICROLEARNING

## Filosofia
**< 7 minutos por unit. Mobile-first. Spaced.** Não substitui deep learning; complementa.

## Quando usar
- Corporate training (compliance, product updates)
- Language learning
- Onboarding (split em micro-units)
- Knowledge retention (post-course)
- Just-in-time performance support

## Princípios
- **5-7 min max** per unit
- **One concept** per unit
- **Mobile-first** (não desktop-shrunk)
- **Spaced delivery:** Anki/SM-2 algorithm
- **Active retrieval:** quiz > video

## Stack
- **Anki:** spaced repetition líder (open-source)
- **Duolingo:** gamified microlearning (language)
- **Quizlet:** flashcards + games
- **Memrise:** mnemonics + spaced
- **EdApp:** corporate microlearning
- **TalentCards (TalentLMS):** corporate mobile

## Templates
1. Microlearning unit template (hook + 3 key points + quiz)
2. Spaced repetition schedule (Anki SM-2)
3. Mobile-first content adaptation
4. Just-in-time embedded help (in-app)
5. Microlearning curriculum (60-day reinforcement)

## Cross-references
- [[campus-learning-experience]] · [[campus-gamification]] · [[campus-corporate-learning]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **campus-microlearning** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in campus-microlearning:**

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
