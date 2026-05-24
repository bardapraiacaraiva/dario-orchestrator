---
name: gaia-supply-chain-esg
description: Supply chain ESG — supplier screening, Scope 3 upstream, modern slavery, conflict minerals, CBAM. Triggers em "supply chain ESG", "supplier ESG", "modern slavery", "Scope 3", "CBAM", "conflict minerals".
license: SEE-LICENSE
parent_agent: gaia-director
compliance: [audit_immutable, csrd_disclosure_gate]
---

# GAIA-SUPPLY-CHAIN-ESG

## Quando usar
- Supplier ESG due diligence program
- Modern Slavery Act statement preparation (UK, AUS)
- CBAM (EU Carbon Border Adjustment) compliance
- Conflict minerals (3TG) reporting (US, EU)
- Supply chain transparency (CSRD ESRS S2)
- German Supply Chain Due Diligence Act (LkSG)

## Marcos regulatórios
- **CSRD ESRS S2** — Workers in value chain
- **CSDDD (EU)** — Corporate Sustainability Due Diligence Directive
- **LkSG (Germany)** — Supply Chain Due Diligence
- **UK Modern Slavery Act** — Section 54
- **AUS Modern Slavery Act**
- **CBAM (EU)** — Carbon border tax 2026
- **Dodd-Frank Section 1502** — Conflict minerals
- **EU Conflict Minerals Regulation**

## Workflow
```
1. Supplier tier mapping (Tier 1, 2, 3+)
2. Risk-based prioritization (country × industry × spend)
3. Self-Assessment Questionnaires (SAQ)
4. Third-party audits (high-risk)
5. Remediation plans
6. Continuous monitoring
7. Disclosure (ESRS S2, modern slavery, conflict minerals)
```

## Templates
1. Supplier ESG SAQ (50 questions, scored)
2. Tier mapping methodology
3. CBAM reporting structure
4. Modern slavery statement template
5. Conflict minerals reasonable inquiry
6. Supplier audit checklist
7. Remediation action plan

## Compliance built-in
- Country-of-origin risk scoring (ITUC, Walk Free, Maplecroft)
- Industry-of-origin risk (textiles, mining, agriculture)
- Sanctions screening integration
- Audit log per supplier interaction

## Cross-references
- [[gaia-carbon-accounting]] · [[gaia-csrd-reporting]] · [[aegis-third-party-risk]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **gaia-supply-chain-esg** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in gaia-supply-chain-esg:**

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
