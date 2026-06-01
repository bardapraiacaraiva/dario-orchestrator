---
name: oraculo-peer-review
description: Peer review — heuristics, rebuttals, area chair, OpenReview. Triggers em "peer review", "rebuttal", "OpenReview", "area chair", "AC", "meta-review".
license: MIT
parent_agent: oraculo-director
compliance: [research_integrity, audit_immutable]
---

# ORACULO-PEER-REVIEW

## Review categories (NeurIPS-style)
- **1: Strong reject** — fatally flawed
- **3: Reject** — significant issues
- **5: Borderline reject** — minor issues
- **6: Weak accept** — needs improvement
- **7: Accept** — good paper
- **9: Strong accept** — top 15% paper
- **Confidence 1-5** — reviewer expertise

## Quality criteria
- **Soundness:** methodology correct
- **Novelty:** new contribution
- **Significance:** advances field
- **Clarity:** well-written
- **Reproducibility:** code + data

## Reviewer biases (mitigate)
- **Confirmation bias** — favor familiar approaches
- **Halo effect** — famous authors/affiliations
- **Length bias** — confuse longer with better
- **Math heaviness** — confuse complex with rigorous
- **Sample bias** — only read top of pile
- **Reviewer fatigue** — late reviews suffer

## Rebuttal strategies
- **Address each concern** — point by point
- **Cite paper changes** — "in revision, we added..."
- **Acknowledge limitations** — show humility
- **Provide additional experiments** if possible
- **Don't argue subjectively** — facts > emotion
- **Respect reviewer** even if wrong

## Templates
1. Review template (per criterion)
2. Rebuttal template (point-by-point)
3. AC meta-review structure
4. Code review for ML papers
5. Conflict of interest declaration
6. Reviewer ethics guidelines

## Cross-references
- [[oraculo-paper-writing]] · [[oraculo-replication-studies]] · [[oraculo-conference-tracking]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **oraculo-peer-review** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in oraculo-peer-review:**

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
