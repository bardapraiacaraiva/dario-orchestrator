---
name: risco-esg
description: "ESG reporting — CSRD compliance, EU Taxonomy, double materiality, carbon footprint, sustainability metrics"
version: "1.0"
---

# RISCO-ESG: ESG & Sustainability Reporting Skill

## When to Activate

**Trigger words (PT):** esg, sustentabilidade, csrd, taxonomia europeia, materialidade, pegada carbonica, relatorio de sustentabilidade, emissoes, ambiente, social, governanca, greenwashing, esrs
**Trigger words (EN):** esg, sustainability, csrd, eu taxonomy, materiality, carbon footprint, sustainability report, emissions, environmental, social, governance, greenwashing, esrs, scope 1 2 3

## Step-by-Step Workflow

### Phase 1: CSRD Applicability & Timeline
1. Determine if subject to CSRD:
   - Large companies (2 of 3: >250 employees, >EUR 50M revenue, >EUR 25M assets) — FY 2024+
   - Listed SMEs — FY 2026+
   - Non-EU companies with EUR 150M+ EU revenue — FY 2028+
2. Identify reporting standards: ESRS (European Sustainability Reporting Standards)
3. Plan assurance: limited assurance required, moving to reasonable
4. Select digital reporting format (XHTML with ESEF taxonomy)

### Phase 2: Double Materiality Assessment
1. **Impact materiality**: how the company affects people and environment
2. **Financial materiality**: how ESG issues affect the company financially
3. Stakeholder engagement: identify and consult key groups
4. Map material topics across ESRS categories:
   - E1: Climate change | E2: Pollution | E3: Water | E4: Biodiversity | E5: Circular economy
   - S1: Own workforce | S2: Value chain workers | S3: Communities | S4: Consumers
   - G1: Business conduct
5. Score and prioritize material topics
6. Document methodology and results

### Phase 3: Environmental (E)
1. **Carbon footprint**: Scope 1 (direct), Scope 2 (energy), Scope 3 (value chain)
2. GHG Protocol methodology for calculations
3. Climate targets: alignment with Paris Agreement / SBTi
4. EU Taxonomy alignment: eligible activities, DNSH criteria, minimum safeguards
5. Energy consumption and renewable energy share
6. Water usage, waste management, circular economy metrics

### Phase 4: Social (S)
1. Workforce metrics: headcount, diversity, gender pay gap, turnover
2. Health & safety: incident rates, lost time, fatalities
3. Training and development: hours per employee, investment
4. Human rights due diligence in supply chain
5. Community engagement and social impact
6. Living wage analysis

### Phase 5: Governance (G)
1. Board composition: independence, diversity, ESG expertise
2. ESG governance structure: committees, responsibilities
3. Executive remuneration linked to ESG targets
4. Anti-corruption and bribery (cross-reference risco-etica)
5. Tax transparency and responsible tax practices
6. Lobbying and political engagement disclosure

### Phase 6: Reporting & Assurance
1. Draft sustainability report per ESRS standards
2. Integrate with annual management report (CSRD requirement)
3. Submit to limited assurance by statutory auditor
4. Publish on company website
5. File with business register (RCBE in PT)
6. Plan for continuous improvement and next cycle

## Commands Table

| Command | Description |
|---------|-------------|
| `risco esg assess` | Full ESG maturity assessment |
| `risco esg materiality` | Double materiality assessment guide |
| `risco esg carbon` | Carbon footprint calculation template |
| `risco esg taxonomy` | EU Taxonomy alignment analysis |
| `risco esg csrd` | CSRD compliance checklist |
| `risco esg metrics` | ESG KPI dashboard template |
| `risco esg report` | Sustainability report structure |
| `risco esg gap` | Gap analysis against ESRS |

## Output Template

```markdown
# ESG Assessment — [Organization]
**Date:** YYYY-MM-DD | **Framework:** CSRD/ESRS | **Period:** FY YYYY

## 1. Materiality Matrix
| Topic | Impact Score | Financial Score | Material? | ESRS Standard |
|-------|------------|----------------|-----------|---------------|

## 2. Environmental Summary
| Metric | Current | Target | YoY Change |
|--------|---------|--------|-----------|
| Scope 1 (tCO2e) | | | |
| Scope 2 (tCO2e) | | | |
| Scope 3 (tCO2e) | | | |
| Energy (MWh) | | | |
| Renewable % | | | |
| Water (m3) | | | |
| Waste diverted % | | | |

## 3. Social Summary
| Metric | Current | Target |
|--------|---------|--------|
| Employees | | |
| Gender diversity % | | |
| Pay gap % | | |
| Training hours/emp | | |
| LTIR | | |

## 4. Governance Summary
| Metric | Status |
|--------|--------|
| Board independence % | |
| ESG Committee | [Yes/No] |
| Exec comp linked to ESG | [Yes/No] |
| Anti-corruption policy | [Yes/No] |

## 5. EU Taxonomy Alignment
| Activity | Eligible | Aligned | % Revenue | % CapEx | % OpEx |
|----------|----------|---------|-----------|---------|--------|

## 6. Gaps & Roadmap
| # | Gap | ESRS Ref | Priority | Action | Deadline |
|---|-----|----------|----------|--------|----------|

## 7. Next Reporting Cycle: FY YYYY
```

## Red Flags

- No double materiality assessment conducted
- Carbon footprint limited to Scope 1+2 only (Scope 3 omitted)
- EU Taxonomy alignment claimed without DNSH assessment
- Greenwashing risk: marketing claims without data backing
- No third-party assurance on sustainability data
- ESG targets not time-bound or not science-based
- Board has no ESG oversight responsibility
- Supply chain human rights not assessed
- CSRD deadline approaching with no preparation
- Gender pay gap not measured or not disclosed
- No stakeholder engagement in materiality process
- Sustainability report disconnected from financial report


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **risco-esg** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in risco-esg:**

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
