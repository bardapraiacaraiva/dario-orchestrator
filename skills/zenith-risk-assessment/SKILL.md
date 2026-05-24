---
name: zenith-risk-assessment
description: Enterprise risk — COSO ERM, ISO 31000, risk matrix, top risks. Triggers em "enterprise risk", "ERM", "COSO", "ISO 31000", "risk register", "risk matrix", "top risks".
license: SEE-LICENSE
parent_agent: zenith-director
compliance: [audit_immutable]
---

# ZENITH-RISK-ASSESSMENT

## Quando usar
- ERM program greenfield
- Annual risk review
- Top-down risk identification (CEO/board level)
- M&A risk evaluation
- Crisis risk identification

## Frameworks
- **COSO ERM (2017):** Mission/Strategy/Performance integrated
- **ISO 31000:** risk management principles
- **NIST RMF:** infosec-focused
- **Three Lines of Defense:** ops + risk + audit

## Templates
1. Risk register (per category + likelihood + impact)
2. Risk matrix (5×5 heat map)
3. Top-10 risks board report
4. Risk appetite statement
5. Key Risk Indicators (KRIs) dashboard
6. Risk treatment plan (avoid/reduce/transfer/accept)

## Categorias risco
- **Strategic:** market, competitive, technology
- **Operational:** processes, systems, people
- **Financial:** liquidity, FX, credit
- **Compliance/Legal:** regulatory, litigation
- **Reputational:** brand, social, ESG

## Cross-references
- [[zenith-scenario-planning]] · [[risco-matrix]] · [[risco-bcp]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **zenith-risk-assessment** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in zenith-risk-assessment:**

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
