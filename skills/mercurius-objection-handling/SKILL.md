---
name: mercurius-objection-handling
description: Objection handling — LAER framework, top 50 objections + responses, reframing techniques. Triggers em "objection handling", "objections", "price objection", "competitor objection", "LAER", "feel felt found".
license: MIT
parent_agent: mercurius-director
---

# MERCURIUS-OBJECTION-HANDLING

## Framework LAER
1. **Listen** — full sentence, no interrupt
2. **Acknowledge** — "I hear that..."
3. **Explore** — "Can you tell me more about that?"
4. **Respond** — only after fully understanding

## Top 10 objections + responses

| Objection | Reframe |
|---|---|
| "Too expensive" | "Vs what? Compared to cost of inaction = X" |
| "We're happy with current" | "What would have to change for that to not be true?" |
| "No budget" | "Budget é a conclusion, not the start. If we proved ROI, would budget emerge?" |
| "Send me info" | "Happy to. To send what's relevant, can I understand 2 things first?" |
| "Not the right time" | "What would make it the right time?" |
| "We tried similar before" | "Curious — what specifically didn't work?" |
| "Need to think about it" | "What specifically needs more thought?" |
| "Competitor X is cheaper" | "Yes, lower price. Different value proposition — let me explain..." |
| "Procurement will block" | "Mind if I bring them in early to understand their criteria?" |
| "Champion left" | "Sorry to hear. Let me re-establish with new owner..." |

## Templates
1. Objection library (50+ industry-specific)
2. Reframe scripts (3 variations each)
3. Feel/Felt/Found framework templates
4. "Just to play devil's advocate" reverse psychology
5. Objection scorecard (track frequency + win rate by objection)

## Cross-references
- [[mercurius-discovery-call]] · [[mercurius-negotiation-prep]] · [[mercurius-closing]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-objection-handling** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-objection-handling:**

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
