---
name: "PESSOA Workforce Planning"
description: "Workforce planning — headcount forecasting, FTE vs contractor analysis, capacity models, attrition modeling, scenario planning, and strategic workforce design."
version: "1.0"
agent: "P.E.S.S.O.A. — People, Engagement, Skills, Succession, Organization & Alignment"
category: "Planning"
---

# PESSOA Workforce Planning

## Triggers

Activate this skill when the user says any of:
- "workforce planning", "planeamento de pessoal"
- "headcount", "quadro de pessoal", "FTE"
- "capacity planning", "planeamento de capacidade"
- "contractor vs employee", "freelancer vs contrato"
- "attrition", "turnover forecast", "rotatividade"
- "scenario planning", "cenarios de pessoal"
- "how many people do I need?", "quantas pessoas preciso?"
- Any request to plan, forecast, or optimize workforce size and composition

## Frameworks & References

- **Peter Cappelli** (Managing Talent in a New World) — Talent on demand, workforce agility
- **BCG / McKinsey** — Strategic workforce planning methodology
- **SHRM** — Workforce analytics best practices
- **Mercer** — Internal labor market analysis, workforce modeling
- **Codigo do Trabalho (PT)** — Contract types, outsourcing rules, temporary work

## Workflow

### Step 1: Current Workforce Snapshot

| Metric | Value | Benchmark |
|--------|-------|-----------|
| **Total headcount** | X | — |
| **FTEs** | X | — |
| **Contractors / Freelancers** | X | <20% of total |
| **Part-time** | X | — |
| **Revenue per employee** | EUR X | >EUR 80K (services), >EUR 150K (SaaS) |
| **Employee cost ratio** | X% of revenue | 40-60% (services), 25-40% (SaaS) |
| **Average tenure** | X years | >2.5 years |
| **Voluntary turnover** | X% annual | <15% |
| **Involuntary turnover** | X% annual | <5% |
| **Open positions** | X | — |
| **Time to fill (avg)** | X days | <45 days |

**Workforce by Department:**

| Department | FTEs | Contractors | Total | % of Workforce | Revenue/Head |
|-----------|------|------------|-------|---------------|-------------|
| Sales & Marketing | X | X | X | X% | EUR X |
| Product / Engineering | X | X | X | X% | EUR X |
| Operations / Delivery | X | X | X | X% | EUR X |
| Finance / Admin | X | X | X | X% | EUR X |
| HR / People | X | X | X | X% | EUR X |
| **Total** | **X** | **X** | **X** | **100%** | **EUR X** |

### Step 2: Demand Forecasting

**Method 1: Revenue-Based (Top-Down)**

| Quarter | Projected Revenue | Revenue/Employee | Headcount Needed | Current | Gap |
|---------|------------------|-----------------|-----------------|---------|-----|
| Q1 | EUR X | EUR X | X | X | +/-X |
| Q2 | EUR X | EUR X | X | X | +/-X |
| Q3 | EUR X | EUR X | X | X | +/-X |
| Q4 | EUR X | EUR X | X | X | +/-X |

**Method 2: Workload-Based (Bottom-Up)**

| Function | Workload Unit | Volume/Quarter | Hours/Unit | FTE Capacity (h/quarter) | FTEs Needed |
|----------|-------------|---------------|-----------|------------------------|------------|
| [Function 1] | [e.g., clients served] | X | X hours | 480h | X |
| [Function 2] | [e.g., tickets handled] | X | X hours | 480h | X |
| [Function 3] | [e.g., projects delivered] | X | X hours | 480h | X |

**Method 3: Ratio-Based**

| Ratio | Current | Target | Implication |
|-------|---------|--------|-------------|
| Clients per account manager | X:1 | 15:1 | Need X more AMs |
| Developers per PM | X:1 | 6:1 | Need X more devs |
| Revenue per salesperson | EUR X | EUR X | Need X more sales |
| Employees per HR | X:1 | 100:1 | Need X more HR |
| Support tickets per agent | X/day | 30/day | Need X more agents |

### Step 3: FTE vs Contractor Decision Matrix

| Factor | Favor FTE | Favor Contractor | Your Situation |
|--------|----------|-----------------|----------------|
| **Duration** | Ongoing, permanent need | Project-based, temporary | |
| **Core/non-core** | Core competency | Non-core, specialized | |
| **Skill availability** | Available in market | Scarce, niche expertise | |
| **Cost** | Lower long-term (with benefits) | Lower short-term (no benefits) | |
| **Control** | Need close management | Independent output OK | |
| **IP/confidentiality** | High sensitivity | Low sensitivity | |
| **Scalability** | Steady demand | Variable, seasonal | |
| **Legal risk** | Proper employment contract | Risk of misclassification | |

**PT Legal Note on Contractor Misclassification:**
- If contractor works exclusively for you, at your premises, with your tools, on your schedule = employment relationship (Art. 12 CT)
- ACT can reclassify as employee retroactively
- Employer owes back SS contributions, vacation, subsidies
- Fine: EUR 2,040-61,200

**Cost Comparison:**

| Element | FTE (Annual) | Contractor (Annual) |
|---------|-------------|-------------------|
| Base compensation | EUR X x 14 months | EUR X x 12 months |
| SS employer (23.75%) | EUR X | EUR 0 |
| Meal allowance | EUR X | EUR 0 |
| Insurance | EUR X | EUR 0 |
| Benefits | EUR X | EUR 0 |
| Equipment | EUR X | EUR 0 (usually) |
| Recruitment cost | EUR X (one-time) | EUR 0 |
| **Total annual cost** | **EUR X** | **EUR X** |
| **Effective hourly rate** | **EUR X** | **EUR X** |

### Step 4: Attrition Modeling

**Historical Attrition Analysis:**

| Period | Start HC | Voluntary Exits | Involuntary Exits | Total Attrition | Rate |
|--------|---------|----------------|-------------------|----------------|------|
| Q1 | X | X | X | X | X% |
| Q2 | X | X | X | X | X% |
| Q3 | X | X | X | X | X% |
| Q4 | X | X | X | X | X% |
| **Annual** | **X** | **X** | **X** | **X** | **X%** |

**Attrition Prediction Model:**

| Risk Factor | Weight | High Risk Indicators |
|-------------|--------|---------------------|
| **Tenure** | 25% | <1 year or >5 years (U-curve) |
| **Performance** | 20% | Top performers (poached) or low performers (managed out) |
| **Compensation** | 20% | Below P50 for role/market |
| **Manager quality** | 15% | Low manager eNPS score |
| **Growth opportunity** | 10% | No promotion in 3+ years |
| **Engagement** | 10% | eNPS detractor, declining survey scores |

**Replacement Planning:**

| Attrition Rate | Expected Exits/Year | Recruitment Needed | Budget Impact |
|---------------|--------------------|--------------------|--------------|
| 10% (optimistic) | X | X hires | EUR X recruitment cost |
| 15% (expected) | X | X hires | EUR X recruitment cost |
| 20% (pessimistic) | X | X hires | EUR X recruitment cost |

### Step 5: Scenario Planning

**Scenario A: Growth (Revenue +30%)**

| Element | Impact | Action |
|---------|--------|--------|
| Headcount | +X FTEs needed | Hire X in [departments] |
| Timeline | X months to full capacity | Start hiring in [month] |
| Budget | +EUR X annual payroll | Finance approval needed |
| Risk | Hiring speed, culture dilution | Phased hiring, strong onboarding |

**Scenario B: Steady State (Revenue +5-10%)**

| Element | Impact | Action |
|---------|--------|--------|
| Headcount | Maintain + replace attrition | X replacement hires |
| Focus | Efficiency, upskilling | Invest in L&D, automation |
| Budget | Flat payroll + inflation adjustment | 3-5% salary review |
| Risk | Stagnation, top talent leaves | Career development, retention focus |

**Scenario C: Contraction (Revenue -15%)**

| Element | Impact | Action |
|---------|--------|--------|
| Headcount | -X FTEs required | Hiring freeze, natural attrition first |
| Timeline | Reduce over X months | Freeze → Contractor cuts → Restructuring |
| Budget | -EUR X annual savings needed | Reduce contractor spend first |
| Risk | Morale, legal compliance, key talent loss | Transparent communication, retention of key talent |
| PT Legal | Collective dismissal rules if 2+ in 3 months (for companies <50) or 5+ (for 50-300) | DGERT notification, consultation period |

### Step 6: Workforce Mix Optimization

| Category | Current % | Optimal % | Action |
|----------|----------|----------|--------|
| **Permanent FTE** | X% | 70-80% | [increase/decrease] |
| **Fixed-term contract** | X% | 5-15% | [increase/decrease] |
| **Freelancer/Contractor** | X% | 10-15% | [increase/decrease] |
| **Intern/Trainee** | X% | 0-5% | [increase/decrease] |
| **Agency/Temporary** | X% | 0-5% | [increase/decrease] |

### Step 7: Capacity Model

**Available Capacity Calculation:**

| Factor | Value | Notes |
|--------|-------|-------|
| Working days per year | 252 | PT: 365 - 104 weekends - 9 holidays |
| Less: vacation | -22 days | Minimum legal |
| Less: average sick days | -5 days | PT average |
| Less: training | -5 days | 40h = ~5 days |
| Less: admin/overhead | -10 days | Meetings, email, non-productive |
| **Net productive days** | **210 days** | Per FTE |
| **Net productive hours** | **1,680 hours** | At 8h/day |
| **Utilization target** | **75-85%** | Billable/productive ratio |
| **Effective capacity** | **1,260-1,428 hours** | Per FTE per year |

### Step 8: 12-Month Workforce Plan

| Month | Start HC | Planned Hires | Expected Attrition | End HC | Budget |
|-------|---------|---------------|-------------------|--------|--------|
| M1 | X | X | X | X | EUR X |
| M2 | X | X | X | X | EUR X |
| M3 | X | X | X | X | EUR X |
| ... | ... | ... | ... | ... | ... |
| M12 | X | X | X | X | EUR X |

## Output Template

```markdown
# PESSOA Workforce Plan
## Organization: [NAME]
## Period: [YEAR]
## Date: YYYY-MM-DD

### Current State
- Total headcount: X (FTE: X, Contractors: X)
- Revenue/employee: EUR X
- Turnover: X% annual

### Demand Forecast
| Quarter | Revenue | HC Needed | Current | Gap |
|---------|---------|----------|---------|-----|
| Q1 | EUR X | X | X | +/-X |

### Hiring Plan
| Role | Department | Type | Start | Budget |
|------|-----------|------|-------|--------|
| [Role] | [Dept] | FTE/Contract | [Month] | EUR X |

### Scenario Summary
| Scenario | HC Change | Budget Impact | Key Risk |
|----------|----------|--------------|----------|
| Growth | +X | +EUR X | [risk] |
| Steady | +/-0 | +EUR X | [risk] |
| Contraction | -X | -EUR X | [risk] |

### Workforce Health Score: X/10
```

## Red Flags

Stop and warn the user if:
- Revenue per employee below EUR 50K (unsustainable for most businesses)
- Employee cost exceeds 70% of revenue (margin squeeze)
- Contractor percentage above 30% (misclassification risk, culture risk)
- No attrition forecast (will be surprised by departures)
- Hiring plan disconnected from revenue forecast
- No scenario planning for downside (only planning for growth)
- Key roles dependent on single contractor (continuity risk)
- Time to fill exceeding 60 days consistently (pipeline problem)
- Turnover above 25% without root cause analysis
- Capacity model assumes 100% utilization (unrealistic)
- No workforce budget approved before hiring begins

## Handoff

After workforce planning:
- Route to `pessoa-recrutamento` for hiring execution
- Route to `pessoa-compensacao` for budget alignment
- Route to `pessoa-orgdesign` for structure decisions
- Route to `pessoa-sucessao` for critical role coverage
- Route to `dario-financial-model` for financial projections integration
- Save output to Obsidian: `05 - Claude - IA/Outputs/YYYY-MM-DD - PESSOA - Workforce Plan - [Organization].md`
