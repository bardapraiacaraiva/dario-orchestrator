---
name: gaia-csrd-reporting
description: CSRD/ESRS reporting — Directive 2022/2464, ESRS E1-E5, S1-S4, G1 disclosure standards. Triggers em "CSRD", "ESRS", "Directive 2022 2464", "sustainability statement", "EU sustainability".
license: SEE-LICENSE
parent_agent: gaia-director
compliance: [csrd_disclosure_gate, audit_immutable]
jurisdiction: EU
---

# GAIA-CSRD-REPORTING

## Marco
- **Directive (EU) 2022/2464 (CSRD)** — Corporate Sustainability Reporting Directive
- **Delegated Act 2023/2772** — ESRS standards
- **Wave 1 (FY 2024):** large public-interest entities (>500 employees)
- **Wave 2 (FY 2025):** large companies (>250 employees, >€50M revenue)
- **Wave 3 (FY 2026):** listed SMEs
- **Wave 4 (FY 2028):** non-EU companies with EU revenue >€150M

## ESRS structure
- **ESRS 1:** General requirements
- **ESRS 2:** General disclosures (always applicable)
- **ESRS E1-E5:** Environment (climate, pollution, water, biodiversity, circular)
- **ESRS S1-S4:** Social (workforce, value chain, communities, consumers)
- **ESRS G1:** Governance (business conduct)

## Quando usar
- CSRD first-time preparation (Wave 1-4)
- Double materiality assessment (impact + financial)
- ESRS gap analysis vs current reporting
- Sustainability statement drafting
- External assurance preparation (Big4)

## Templates
1. Double materiality assessment workshop
2. ESRS data points checklist (1.144 disclosures total)
3. Sustainability statement structure
4. ESRS digital tagging (XBRL) prep
5. Limited → reasonable assurance roadmap
6. Stakeholder engagement plan

## Compliance gates
- CSRD wave applicability check (auto)
- ESRS mandatory vs voluntary disclosures
- Double materiality methodology validation
- XBRL machine-readable verification

## Cross-references
- [[gaia-carbon-accounting]] · [[gaia-sasb-standards]] · [[gaia-gri-reporting]] · [[lex-ai-governance]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **gaia-csrd-reporting** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in gaia-csrd-reporting:**

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
