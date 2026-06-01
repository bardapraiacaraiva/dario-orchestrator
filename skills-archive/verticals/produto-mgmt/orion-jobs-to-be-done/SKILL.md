---
name: orion-jobs-to-be-done
description: JTBD framework — outcome-driven innovation, switch interviews, jobs canvas. Triggers em "JTBD", "jobs to be done", "outcome-driven", "switch interview", "Christensen".
license: MIT
parent_agent: orion-director
compliance: [data_privacy_by_design]
---

# ORION-JOBS-TO-BE-DONE

## Filosofia
**"People don't buy products, they hire them to do a job."** — Clayton Christensen.
Substitui demographic/persona thinking por outcome thinking.

## Quando usar
- Redefinir target market (não por demographics)
- Pricing alignment com value
- Competitive analysis (quem são os "hires" alternativos?)
- New product opportunity identification
- Positioning re-think

## Frameworks
- **JTBD switch interview (Klement):** push/pull/anxiety/habit forces
- **Outcome-Driven Innovation (Ulwick):** 100+ desired outcomes per job
- **Jobs Canvas (Strategyn):** jobs + outcomes + constraints
- **JTBD 5 (Christensen):** functional / emotional / social jobs

## Templates
1. Switch interview script (Bob Moesta style)
2. Job statement formula: "When [situation], I want to [motivation], so I can [outcome]"
3. Outcome statement formula: "Minimize the time/effort it takes to [outcome]"
4. Forces of progress diagram
5. Job mapping (8 stages)

## Cross-references
- [[orion-product-discovery]] · [[orion-product-strategy]] · [[a360-nicho]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **orion-jobs-to-be-done** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in orion-jobs-to-be-done:**

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
