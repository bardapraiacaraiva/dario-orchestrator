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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **risco-seguros** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in risco-seguros:**

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
