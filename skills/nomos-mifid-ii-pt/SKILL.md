---
name: nomos-mifid-ii-pt
description: MiFID II PT — investment services, advice, suitability, best execution, costs disclosure. Triggers em "MiFID II", "MiFID", "investment advice PT", "suitability", "best execution", "ESMA", "intermediação financeira".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [cmvm_disclosure_gate, audit_immutable]
jurisdiction: Portugal + EU
---

# NOMOS-MIFID-II-PT

## Marco
- **Directive 2014/65/EU (MiFID II)** + **MiFIR Regulation 600/2014**
- **DL 357-A/2007** — transposição PT (intermediação financeira)
- **Lei 35/2018** — MiFID II implementation
- **ESMA guidelines** — multiple
- **MiFID II Review (Directive 2024/790)** — Feb 2024, applicable Mar 2025+
- **Retail Investment Strategy (RIS)** — em discussão 2025+

## Quando usar
- Investment firm authorization
- Investment advice service setup
- Suitability/appropriateness assessments
- Best execution policy
- Product governance (manufacturer/distributor)
- Inducements review
- Costs & charges disclosure
- Investor classification (retail/professional/eligible counterparty)

## MiFID II key obligations
- **Knowledge & competence:** staff certifications (CFA, CMVM exams)
- **Suitability:** capture investment objectives, financial situation, knowledge
- **Best execution:** RTS 27/28 reporting (top venues, execution quality)
- **Inducements:** ban on retrocessions for independent advice
- **Product governance:** target market identification + distribution strategy
- **Recording communications:** phone + electronic (5-7 year retention)

## Templates
1. Investor classification questionnaire
2. Suitability assessment template
3. Best execution policy
4. Product governance manufacturer doc
5. Inducements disclosure
6. Costs ex-ante + ex-post disclosure
7. RTS 28 annual report (top execution venues)

## Cross-references
- [[nomos-cmvm-compliance]] · [[nomos-bdp-banking-pt]] · [[atlas-fin-foreign-exchange]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-mifid-ii-pt** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-mifid-ii-pt:**

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
