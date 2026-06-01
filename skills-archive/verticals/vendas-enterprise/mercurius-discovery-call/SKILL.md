---
name: mercurius-discovery-call
description: Discovery call structure — agenda, question library, pain identification, next-step commitment. Triggers em "discovery call", "discovery questions", "qualification call", "first call", "intro call".
license: MIT
parent_agent: mercurius-director
compliance: [audit_trail]
---

# MERCURIUS-DISCOVERY-CALL

## Estrutura ideal (30-45 min)
```
0-3min:  Rapport + agenda setting
3-10min: Current state diagnostic (SPIN Situation+Problem)
10-25min: Pain quantification (SPIN Implication)
25-35min: Future state vision (SPIN Need-Payoff)
35-40min: Process + decision criteria
40-45min: Next steps + mutual close plan
```

## Question library categorias
- **Current state:** "Hoje, como vocês fazem X?"
- **Quantified pain:** "Quantas horas/mês isto consome?"
- **Decision process:** "Quem mais precisa estar envolvido?"
- **Budget signals:** "Existe budget alocado para isto?"
- **Timeline:** "Quando precisariam ter isto a funcionar?"
- **Competition:** "Estão a avaliar outras opções?"

## Anti-patterns
- ❌ Demo no discovery (premature solution)
- ❌ Talking > listening (target 80% listen)
- ❌ Yes/no questions only
- ❌ Skipping pain quantification
- ❌ Not getting next-step commitment

## Templates
1. Discovery script (3 personas × 3 verticals)
2. Question library (200+ questions categorized)
3. Discovery scorecard (MEDDIC fields capture)
4. Mutual close plan template
5. Recording + transcript analysis framework
6. Discovery call coaching rubric (10 criteria)

## Cross-references
- [[mercurius-sales-methodology]] · [[mercurius-objection-handling]] · [[mercurius-demo-script]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-discovery-call** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-discovery-call:**

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
