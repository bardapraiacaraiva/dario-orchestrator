---
name: mercurius-demo-script
description: Demo script design — pain-driven demo, ROI calculator, custom storyline per persona. Triggers em "demo script", "product demo", "demo storytelling", "demo customization", "ROI calculator demo".
license: MIT
parent_agent: mercurius-director
---

# MERCURIUS-DEMO-SCRIPT

## Princípio
**Demo é storytelling, não feature tour.** Show outcome → solution → pain solved.

## Estrutura demo (45-60 min)
```
0-5min:  Recap discovery (mostrar entendi a pain)
5-10min: Hero outcome (start with end state)
10-30min: Custom storyline (3-5 use cases relevantes)
30-40min: ROI quantification (their numbers)
40-50min: Handle questions
50-60min: Next steps mutual
```

## Tipos de demo
- **Discovery demo** (10 min, validate fit)
- **Standard demo** (30-45 min, persona-customized)
- **Deep dive** (60-90 min, technical/security review)
- **Pilot demo** (proof of concept, 1-2 weeks)

## Templates
1. Demo storyline matrix (3 personas × 5 use cases = 15 scripts)
2. ROI calculator (industry-specific inputs)
3. Demo environment setup checklist
4. Objection-in-demo handling (top 10)
5. Demo recording + analysis framework
6. POC (Proof of Concept) success criteria

## Demo tools
- **Storylane / Navattic** — interactive product tours
- **Reprise / Walnut** — custom demo environments
- **Demodesk** — meeting platform sales-focused

## Cross-references
- [[mercurius-discovery-call]] · [[mercurius-objection-handling]] · [[mercurius-closing]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-demo-script** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-demo-script:**

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
