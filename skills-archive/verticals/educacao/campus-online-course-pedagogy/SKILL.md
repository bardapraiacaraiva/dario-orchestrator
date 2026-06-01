---
name: campus-online-course-pedagogy
description: Pedagogia online — cohort-based, async, hybrid, MOOC, peer learning. Triggers em "cohort-based", "MOOC", "async learning", "hybrid course", "peer learning", "asynchronous".
license: SEE-LICENSE
parent_agent: campus-director
compliance: [bncc_curriculum_alignment]
---

# CAMPUS-ONLINE-COURSE-PEDAGOGY

## Modelos
- **Self-paced (MOOC):** student-controlled timing. Completion <10% típica
- **Cohort-based (CBC):** start/end fixos, peer + accountability. 60-70% completion
- **Hybrid (blended):** presencial + online
- **Flipped classroom:** conteúdo em casa, prática em aula
- **Live online:** Zoom-based synchronous
- **Bootcamp:** intensivo, full-time

## Quando usar cada
- **MOOC:** awareness/leads, low-touch, escala massiva
- **CBC:** high-ticket ($500+), transformation outcome
- **Bootcamp:** career change ($$$$, high commitment)
- **Hybrid:** acadêmico ou enterprise training

## Templates
1. Cohort-based course playbook (Maven/Sora-style)
2. MOOC structure (5 weeks, peer-graded)
3. Live-online session script (90 min, Zoom)
4. Hybrid course design (50% online + 50% presencial)
5. Bootcamp curriculum (12 weeks, full-time)

## Princípios chave
- **Spaced repetition:** content distribuído no tempo
- **Active retrieval:** test > re-read
- **Interleaving:** misturar tópicos > blocked practice
- **Production over consumption:** "do" > "watch"
- **Cohort effects:** peer pressure positiva

## Cross-references
- [[campus-learning-experience]] · [[campus-microlearning]] · [[orion-product-launch]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **campus-online-course-pedagogy** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in campus-online-course-pedagogy:**

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
