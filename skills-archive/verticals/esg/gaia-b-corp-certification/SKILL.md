---
name: gaia-b-corp-certification
description: B-Corp Certification — B Impact Assessment (BIA), 5 impact areas, recertification. Triggers em "B Corp", "B Corporation", "B Impact Assessment", "BIA", "certified B Corp", "B Lab".
license: SEE-LICENSE
parent_agent: gaia-director
compliance: [audit_immutable]
---

# GAIA-B-CORP-CERTIFICATION

## Quando usar
- B-Corp certification first-time
- Recertification (every 3 years)
- B-Corp score improvement
- Legal requirement integration (benefit corporation status)
- Marketing as B-Corp (stakeholder economy positioning)

## Marco
- **B Lab** — non-profit certifying body
- **BIA (B Impact Assessment)** — 200+ questions, 5 impact areas
- **Minimum score:** 80/200 to certify
- **Legal requirement:** stakeholder consideration in articles
- **2024 standards update:** more rigorous

## 5 Impact Areas
1. **Governance** — mission lock, ethics, transparency
2. **Workers** — compensation, benefits, training, ownership
3. **Community** — diversity, civic engagement, supply chain, local economy
4. **Environment** — environmental management, air/climate, water, land/life
5. **Customers** — beneficial products/services, customer welfare

## Workflow
```
1. BIA self-assessment (free, 90-120 min)
2. Improvement plan (typically 6-12 months to reach 80+)
3. Submit assessment to B Lab
4. Verification call (operational review)
5. Documentation review
6. Background check (legal, public records)
7. Legal requirement adoption (articles amendment)
8. Certification (3-year validity)
```

## Templates
1. BIA section-by-section preparation guide
2. Score improvement plan (gap → 80+)
3. Articles amendment template (PT/BR/EU jurisdictions)
4. Documentation evidence checklist
5. B-Corp marketing playbook (post-certification)
6. Recertification roadmap (3-year cycle)

## Cross-references
- [[gaia-social-impact]] · [[gaia-governance-frameworks]] · [[gaia-sustainability-strategy]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **gaia-b-corp-certification** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in gaia-b-corp-certification:**

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
