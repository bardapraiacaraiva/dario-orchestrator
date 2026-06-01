---
name: gaia-sbti-targets
description: Science-Based Targets initiative (SBTi) — 1.5°C/2°C pathway, near-term + long-term targets, validation. Triggers em "SBTi", "science based targets", "1.5°C pathway", "net zero target", "SBTi validation".
license: SEE-LICENSE
parent_agent: gaia-director
compliance: [ghg_protocol_verification, audit_immutable]
---

# GAIA-SBTI-TARGETS

## Quando usar
- SBTi commitment letter signing
- Near-term target setting (5-10 years)
- Net-zero target setting (by 2050)
- SBTi validation submission
- Annual progress reporting
- Sector-specific pathway (FLAG, financial institutions)

## Marco
- **SBTi Corporate Net-Zero Standard** (Oct 2021, v1.2 2024)
- **SBTi Criteria Version 5** — target validation
- **Sectoral Decarbonization Approach (SDA)** — for sectors
- **Absolute Contraction Approach (ACA)** — universal pathway

## Workflow
```
1. Sign commitment letter (24 months to validate)
2. Inventory base year (GHG Protocol compliant)
3. Choose ambition (1.5°C aligned)
4. Set near-term targets:
   - Scope 1+2: 4.2% annual absolute reduction (1.5°C)
   - Scope 3: 2.5% annual reduction OR engagement targets
5. Set long-term net-zero target (2040-2050)
6. Submit for SBTi validation
7. Communicate publicly
8. Annual progress reporting
9. Recalculate targets every 5 years
```

## Templates
1. SBTi commitment letter
2. Near-term target setting calculator
3. Net-zero target structure
4. Scope 3 engagement target template (67% of suppliers by 2027)
5. SBTi validation submission package
6. Annual progress disclosure
7. Sectoral pathway selection guide

## Compliance built-in
- Pathway alignment verification (1.5°C scientific)
- Recalculation triggers (M&A, divestiture, methodology)
- Buffer for residual emissions (net-zero = 90% reduction + 10% removal)

## Cross-references
- [[gaia-carbon-accounting]] · [[gaia-transition-planning]] · [[gaia-climate-risk-tcfd]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **gaia-sbti-targets** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in gaia-sbti-targets:**

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
