---
name: mercurius-sales-methodology
description: Sales methodologies — BANT, MEDDIC/MEDDPICC, Challenger Sale, SPIN, Sandler, Solution Selling. Qual usar quando. Triggers em "sales methodology", "MEDDIC", "BANT", "Challenger", "SPIN", "Sandler", "Solution Selling".
license: MIT
parent_agent: mercurius-director
compliance: [no_dark_patterns]
---

# MERCURIUS-SALES-METHODOLOGY

## Quando usar
- Setup sales playbook (greenfield)
- Methodology decision: qual fit org?
- Sales rep onboarding training
- Pipeline review re-qualification
- Win/loss analysis

## Frameworks chave
- **BANT** (IBM) — Budget/Authority/Need/Timeline. Simples, transactional sales.
- **MEDDIC / MEDDPICC** (PTC) — Metrics/Economic buyer/Decision criteria/Decision process/Identify pain/Champion (+Competition+Paper process). Complex enterprise.
- **Challenger Sale** (Dixon/Adamson) — Teach/Tailor/Take control. High-info buyers.
- **SPIN Selling** (Rackham) — Situation/Problem/Implication/Need-payoff. Diagnostic.
- **Sandler** — Pain funnel, reverse psychology. Pull > push.
- **Solution Selling** — Pain → vision → proof → buy.
- **Value Selling** — quantified business outcomes.
- **GAP Selling** — current state → future state gap quantified.

## Decision tree (qual methodology)
- Transactional <$10K: BANT
- Mid-market $10-100K: SPIN + Solution
- Enterprise $100K+: MEDDIC + Challenger
- Long sales cycle 9+ months: MEDDPICC mandatory
- Educated buyer: Challenger
- Diagnostic phase needed: SPIN

## Templates
1. Methodology selection workshop
2. MEDDIC scorecard template (per opportunity)
3. Challenger commercial teaching pitch
4. SPIN question library by industry
5. Pain funnel script (Sandler)
6. Value Selling business case template

## Cross-references
- [[mercurius-discovery-call]] · [[mercurius-objection-handling]] · [[mercurius-closing]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-sales-methodology** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-sales-methodology:**

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
