---
name: risco-terceiros
description: "Third-party risk — vendor due diligence, supply chain risk, onboarding, ongoing monitoring, exit management"
version: "1.0"
---

# RISCO-TERCEIROS: Third-Party Risk Management Skill

## When to Activate

**Trigger words (PT):** terceiros, fornecedores, due diligence, cadeia de abastecimento, risco de fornecedores, onboarding fornecedor, subcontratacao, outsourcing, avaliacao de terceiros, risco de contraparte
**Trigger words (EN):** third-party risk, vendor risk, supplier due diligence, supply chain risk, vendor onboarding, outsourcing, subcontractor, counterparty risk, vendor management, tprm

## Step-by-Step Workflow

### Phase 1: Third-Party Inventory
1. Catalog all third parties: vendors, suppliers, subcontractors, partners, agents
2. Classify by criticality: critical (business dependency), important, standard
3. Classify by risk: data access, financial exposure, regulatory impact, reputational
4. Assign owner per third-party relationship
5. Map dependencies and single points of failure
6. Prioritize for due diligence based on risk tier

### Phase 2: Due Diligence (Onboarding)
1. **Tier 1 (Critical)**: full due diligence
   - Financial health: financial statements, credit reports, debt ratios
   - Legal: litigation history, sanctions screening, beneficial ownership
   - Compliance: certifications (ISO 27001, SOC2), RGPD compliance, AML
   - Operational: BCP, insurance coverage, service capacity
   - Reputational: adverse media screening, ESG practices
2. **Tier 2 (Important)**: standard due diligence
   - Financial: credit check, insurance verification
   - Legal: sanctions screening, contract review
   - Compliance: key certifications, RGPD DPA
3. **Tier 3 (Standard)**: simplified due diligence
   - Basic company verification, sanctions screening
4. Document findings and risk rating in vendor file

### Phase 3: Contractual Safeguards
1. Include: SLAs, KPIs, audit rights, termination clauses
2. RGPD: Data Processing Agreement (DPA) for all data processors
3. Confidentiality/NDA clauses
4. Sub-contractor approval and flow-down requirements
5. Insurance requirements (minimum coverage levels)
6. Right to audit and information access
7. Exit/transition assistance clause

### Phase 4: Ongoing Monitoring
1. Periodic review cycle: Tier 1 annual, Tier 2 biennial, Tier 3 triennial
2. Continuous monitoring: financial alerts, sanctions updates, adverse media
3. Performance tracking against SLAs/KPIs
4. Incident tracking and root cause analysis
5. Annual certification/compliance updates
6. Re-assess risk rating upon trigger events

### Phase 5: Concentration & Resilience
1. Map concentration risk by category, geography, revenue dependency
2. Identify single points of failure in supply chain
3. Develop alternative supplier shortlist for critical services
4. Test supplier BCP (request evidence, conduct joint exercises)
5. N-tier risk: assess critical sub-suppliers of Tier 1 vendors
6. Geopolitical and climate risk overlay on supply chain map

### Phase 6: Exit Management
1. Trigger exit for: persistent underperformance, compliance failure, insolvency, strategic change
2. Execute transition plan: data return/destruction, knowledge transfer, service continuity
3. Confirm RGPD obligations on data deletion/return
4. Update third-party register and notify stakeholders
5. Post-exit review and lessons learned

## Commands Table

| Command | Description |
|---------|-------------|
| `risco terceiros inventory` | Third-party register template |
| `risco terceiros dd` | Due diligence questionnaire by tier |
| `risco terceiros onboard` | Vendor onboarding checklist |
| `risco terceiros monitor` | Ongoing monitoring dashboard |
| `risco terceiros risk` | Third-party risk assessment |
| `risco terceiros concentration` | Concentration risk analysis |
| `risco terceiros exit` | Exit management procedure |
| `risco terceiros report` | TPRM program report |

## Output Template

```markdown
# Third-Party Risk Report — [Organization]
**Date:** YYYY-MM-DD | **Period:** [Q/Year] | **TPRM Manager:** [Name]

## 1. Portfolio Overview
| Tier | Count | DD Complete | DD Due | Overdue |
|------|-------|------------|--------|---------|
| Critical | | | | |
| Important | | | | |
| Standard | | | | |

## 2. Risk Heatmap
| Third Party | Financial | Compliance | Operational | Reputational | Overall |
|-------------|-----------|------------|-------------|-------------|---------|

## 3. Due Diligence Status (Tier 1)
| Vendor | Service | DD Date | Risk Rating | Issues | Next Review |
|--------|---------|---------|-------------|--------|-------------|

## 4. Performance (SLA Compliance)
| Vendor | SLA Target | Actual | Trend | Action |
|--------|-----------|--------|-------|--------|

## 5. Concentration Risk
| Category | Top Vendor | % Dependency | Alternative | Contingency |
|----------|-----------|-------------|-------------|-------------|

## 6. Incidents & Issues
| Vendor | Issue | Date | Severity | Resolution | Status |
|--------|-------|------|----------|-----------|--------|

## 7. Recommendations
| # | Recommendation | Risk | Priority | Deadline |
|---|---------------|------|----------|----------|

## 8. Next Review: YYYY-MM-DD
```

## Red Flags

- No third-party inventory or classification
- Critical vendors without due diligence conducted
- No RGPD DPA with data-processing vendors
- Single-source dependency for critical services
- Vendor insolvency risk unmonitored
- Sub-contractors not identified or assessed
- No contractual audit rights
- Vendor performance not tracked against SLAs
- No exit strategy for critical vendors
- Due diligence reviews overdue by >6 months
- Sanctions screening not conducted or not refreshed
- N-tier supply chain risks unknown
