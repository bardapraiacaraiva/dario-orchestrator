---
name: risco-seguros
description: "Insurance management — coverage analysis, renewal calendar, claims management, policy gap identification"
version: "1.0"
---

# RISCO-SEGUROS: Insurance & Coverage Management Skill

## When to Activate

**Trigger words (PT):** seguros, apolice, cobertura, sinistro, renovacao, franquia, premio, responsabilidade civil, seguro profissional, d&o, cyber seguro, mediador, asm
**Trigger words (EN):** insurance, policy, coverage, claim, renewal, deductible, premium, professional indemnity, d&o, cyber insurance, broker, underwriter, risk transfer

## Step-by-Step Workflow

### Phase 1: Insurance Audit
1. Inventory all active policies (type, insurer, broker, policy number)
2. Map coverage to organizational risks (use risk matrix)
3. Review limits and sub-limits adequacy
4. Check deductible/franchise levels vs risk appetite
5. Identify uninsured or underinsured exposures
6. Review policy exclusions and conditions

### Phase 2: Coverage Analysis
1. **Mandatory insurance** (PT): workers comp (AT), auto, professional liability (sector-specific), construction (DL 273/2003)
2. **Recommended**: general liability, D&O, cyber/tech E&O, property, business interruption, key person
3. Gap analysis: risks identified vs coverage held
4. Benchmark premiums against market rates
5. Assess policy wording quality and breadth

### Phase 3: Renewal Management
1. Maintain renewal calendar (12-month rolling view)
2. Start renewal process 90 days before expiry
3. Prepare renewal submission: updated risk profile, claims history, loss runs
4. Obtain competitive quotes (minimum 3 for major lines)
5. Negotiate terms, conditions, and pricing
6. Bind coverage before expiry date (no gaps)

### Phase 4: Claims Management
1. Immediate notification to insurer/broker upon incident (within policy deadline)
2. Document loss: photos, reports, witness statements, cost estimates
3. Maintain claims register with status tracking
4. Cooperate with loss adjuster while protecting interests
5. Track claim progress: submitted, under review, approved, paid, disputed
6. Appeals process for denied or underpaid claims

### Phase 5: Cost Optimization
1. Review deductible levels (higher deductible = lower premium)
2. Bundle policies for multi-line discounts
3. Implement risk improvement measures for premium reduction
4. Consider captive or self-insurance for mature programs
5. Loss prevention ROI analysis
6. Annual premium budget vs actual tracking

## Commands Table

| Command | Description |
|---------|-------------|
| `risco seguros audit` | Full insurance program review |
| `risco seguros calendar` | Renewal calendar generation |
| `risco seguros gap` | Coverage gap analysis |
| `risco seguros claim` | Claims management checklist |
| `risco seguros compare` | Policy comparison template |
| `risco seguros budget` | Insurance cost analysis |
| `risco seguros mandatory` | PT mandatory insurance checklist |
| `risco seguros renewal` | Renewal submission template |

## Output Template

```markdown
# Insurance Program Review — [Organization]
**Date:** YYYY-MM-DD | **Broker:** [Name] | **Total Annual Premium:** EUR X

## 1. Policy Portfolio
| # | Type | Insurer | Policy # | Limit | Deductible | Premium | Expiry |
|---|------|---------|----------|-------|------------|---------|--------|

## 2. Coverage Gap Analysis
| Risk | Current Coverage | Gap Identified | Recommended Action |
|------|-----------------|----------------|-------------------|

## 3. Renewal Calendar
| Policy | Expiry | Renewal Start | Status | Notes |
|--------|--------|---------------|--------|-------|

## 4. Claims Summary (12 months)
| Policy Type | Claims Filed | Settled | Pending | Total Paid | Loss Ratio |
|-------------|-------------|---------|---------|------------|------------|

## 5. Mandatory Insurance Compliance (PT)
| Requirement | Policy Held | Compliant | Notes |
|-------------|------------|-----------|-------|
| Workers Comp (AT) | | [Yes/No] | |
| Auto | | [Yes/No] | |
| Professional Liability | | [Yes/No] | |
| Construction (if applicable) | | [Yes/No] | |

## 6. Recommendations
| # | Recommendation | Impact | Cost | Priority |
|---|---------------|--------|------|----------|

## 7. Next Review: YYYY-MM-DD
```

## Red Flags

- Mandatory insurance missing (workers comp, auto, professional liability)
- Policies expired with no renewal (coverage gap)
- Limits significantly below industry benchmarks or revenue
- No D&O coverage for companies with board members
- No cyber insurance despite digital operations
- Claims not notified within policy-required deadlines
- Single insurer dependency (no market competition at renewal)
- Policy exclusions covering major operational risks
- No claims register maintained
- Renewal process started too late (<30 days before expiry)
- Deductibles misaligned with cash flow capacity
- Business interruption limit insufficient for actual recovery time
