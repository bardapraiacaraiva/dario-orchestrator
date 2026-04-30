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
