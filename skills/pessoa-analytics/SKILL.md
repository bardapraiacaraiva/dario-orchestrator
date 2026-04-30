---
name: "PESSOA People Analytics"
description: "People analytics — HR dashboards, turnover analysis, time-to-hire, cost-per-hire, employee lifetime value, predictive attrition, and data-driven HR decision making."
version: "1.0"
agent: "P.E.S.S.O.A. — People, Engagement, Skills, Succession, Organization & Alignment"
category: "Analytics"
---

# PESSOA People Analytics

## Triggers

Activate this skill when the user says any of:
- "people analytics", "analitica de pessoas", "HR analytics"
- "HR dashboard", "dashboard de RH"
- "turnover analysis", "analise de rotatividade"
- "time to hire", "cost per hire"
- "employee lifetime value", "valor do colaborador"
- "predictive attrition", "prever saidas"
- "HR data", "dados de RH", "HR metrics"
- Any request to analyze, visualize, or predict workforce data

## Frameworks & References

- **Josh Bersin** — People analytics maturity model (4 levels: reporting, advanced, predictive, prescriptive)
- **David Green** — People analytics operating model, data ethics
- **SHRM** — HR metrics and benchmarks
- **Fink & Sturman** — Human capital analytics, ROI of HR
- **RGPD** — Employee data protection requirements for analytics

## Workflow

### Step 1: Analytics Maturity Assessment

| Level | Description | Capabilities | Your Level? |
|-------|------------|-------------|------------|
| **Level 1: Reporting** | Basic headcount, turnover, demographics | Static reports, manual data | [ ] |
| **Level 2: Advanced** | Trends, correlations, drill-down dashboards | Interactive dashboards, benchmarks | [ ] |
| **Level 3: Predictive** | Forecasting attrition, performance, hiring needs | Statistical models, ML | [ ] |
| **Level 4: Prescriptive** | Recommending actions, automated interventions | AI-powered, real-time decisions | [ ] |

**Current maturity**: _______________
**Target maturity**: _______________

### Step 2: Core HR Metrics Dashboard

**Workforce Overview:**

| Metric | Definition | Formula | Value | Benchmark |
|--------|-----------|---------|-------|-----------|
| **Headcount** | Total active employees | Count of active employees | X | — |
| **FTE** | Full-time equivalent | Sum of (hours worked / standard hours) | X | — |
| **Span of control** | Avg direct reports per manager | Total non-managers / Total managers | X | 5-8 |
| **Management ratio** | % of workforce that are managers | Managers / Total headcount | X% | 10-15% |
| **Employee cost ratio** | People cost as % of revenue | Total people cost / Revenue | X% | 40-60% |

**Recruitment Metrics:**

| Metric | Definition | Formula | Value | Target |
|--------|-----------|---------|-------|--------|
| **Time to fill** | Days from req open to offer accept | Avg(accept date - req open date) | X days | <30 (jr), <45 (sr) |
| **Time to hire** | Days from first contact to accept | Avg(accept date - first contact) | X days | <21 |
| **Cost per hire** | Total recruitment cost per hire | (Internal costs + External costs) / Hires | EUR X | <EUR 3K (jr), <EUR 8K (sr) |
| **Quality of hire** | New hire performance at 12 months | % of hires rated "Meets" or above at 12m | X% | >85% |
| **Offer acceptance rate** | % of offers accepted | Accepted / Offers made | X% | >80% |
| **Source effectiveness** | Hires per channel and quality | Hires by source / Applications by source | X% | Track per channel |
| **First-year turnover** | % of hires who leave within 12 months | 1-year leavers / Total hires in cohort | X% | <15% |

**Retention & Turnover:**

| Metric | Definition | Formula | Value | Target |
|--------|-----------|---------|-------|--------|
| **Voluntary turnover** | Annual voluntary exit rate | Voluntary exits / Avg headcount | X% | <15% |
| **Involuntary turnover** | Annual involuntary exit rate | Involuntary exits / Avg headcount | X% | <5% |
| **Total turnover** | All departures | All exits / Avg headcount | X% | <20% |
| **Regrettable turnover** | High performers who leave voluntarily | High-perf voluntary exits / Total voluntary | X% | <5% |
| **Retention rate** | % of employees retained | (Start HC - Exits) / Start HC | X% | >85% |
| **Average tenure** | Avg years of service | Sum(tenure) / Headcount | X years | >2.5 |

**Compensation & Cost:**

| Metric | Definition | Formula | Value | Target |
|--------|-----------|---------|-------|--------|
| **Average salary** | Mean gross monthly salary | Sum(salaries) / Headcount | EUR X | Market median |
| **Compa-ratio** | Position vs midpoint | Avg(salary / band midpoint) | X% | 95-105% |
| **Gender pay gap** | Adjusted gap | (Avg M - Avg F) / Avg M (same grade) | X% | <3% |
| **Revenue per employee** | Productivity measure | Total revenue / FTEs | EUR X | >EUR 80K |
| **Profit per employee** | Profitability measure | Net profit / FTEs | EUR X | Positive |
| **Training spend per head** | L&D investment | Total L&D budget / Headcount | EUR X | EUR 500-2000 |

**Engagement & Wellbeing:**

| Metric | Definition | Formula | Value | Target |
|--------|-----------|---------|-------|--------|
| **eNPS** | Employee Net Promoter Score | % Promoters - % Detractors | X | >30 |
| **Engagement score** | Pulse survey average | Avg of all engagement questions | X/5 | >4.0 |
| **Absenteeism rate** | Unplanned absence rate | Absent days / Available days | X% | <3% |
| **Avg weekly hours** | Workload indicator | Avg reported hours/week | X h | <42 |
| **Vacation utilization** | % of vacation days used | Days used / Days available | X% | >90% |

### Step 3: Turnover Analysis Deep Dive

**Turnover by Dimension:**

| Dimension | Category | Turnover Rate | vs Average | Insight |
|-----------|----------|--------------|-----------|---------|
| **Department** | Sales | X% | +/-X pp | |
| | Engineering | X% | +/-X pp | |
| | Operations | X% | +/-X pp | |
| **Tenure band** | 0-1 year | X% | | Onboarding issue? |
| | 1-3 years | X% | | Growth gap? |
| | 3-5 years | X% | | Career plateau? |
| | 5+ years | X% | | Burnout/stagnation? |
| **Performance** | Top performers | X% | | Retention crisis? |
| | Average performers | X% | | |
| | Low performers | X% | | Managed exits? |
| **Age group** | <30 | X% | | Expectations gap? |
| | 30-45 | X% | | |
| | 45+ | X% | | Retirement planning? |
| **Gender** | Female | X% | | Equity issue? |
| | Male | X% | | |
| **Manager** | Manager A | X% | | Manager problem? |
| | Manager B | X% | | |

**Exit Interview Themes:**

| Reason | % of Exits Citing | Trend | Actionable? |
|--------|------------------|-------|------------|
| Better compensation elsewhere | X% | [trend] | Compensation review |
| Lack of growth/promotion | X% | [trend] | Career paths, L&D |
| Manager relationship | X% | [trend] | Manager training |
| Work-life balance | X% | [trend] | Flexibility policy |
| Company culture/values | X% | [trend] | Culture assessment |
| Role mismatch | X% | [trend] | Better hiring, JD clarity |
| Relocation | X% | [trend] | Remote options |

### Step 4: Predictive Attrition Model

**Flight Risk Scoring:**

| Factor | Data Point | Weight | Score (1-5) |
|--------|-----------|--------|-------------|
| **Tenure** | Years in current role | 15% | |
| **Compensation** | Compa-ratio vs market | 20% | |
| **Performance trajectory** | Rating trend (improving/declining) | 15% | |
| **Manager engagement** | Manager eNPS score | 15% | |
| **Promotion velocity** | Time since last promotion | 10% | |
| **Engagement trend** | Survey score trend (3 months) | 10% | |
| **Life events** | Major changes (commute, family, etc.) | 5% | |
| **Market demand** | Scarcity of their skill set | 10% | |

**Risk Score Interpretation:**

| Score | Risk Level | Action |
|-------|-----------|--------|
| 4.0-5.0 | Critical | Immediate stay interview, retention package |
| 3.0-3.9 | High | Proactive manager conversation, development plan |
| 2.0-2.9 | Medium | Monitor, quarterly check-in |
| 1.0-1.9 | Low | Standard management |

### Step 5: Employee Lifetime Value (ELTV)

**ELTV Calculation:**

```
ELTV = (Annual Revenue per Employee x Avg Tenure) - (Recruitment Cost + Onboarding Cost + Training Cost)
```

| Component | Value | Notes |
|-----------|-------|-------|
| Annual revenue per employee | EUR X | Total revenue / FTEs |
| Average tenure | X years | From HR data |
| Recruitment cost | EUR X | Cost per hire |
| Onboarding cost | EUR X | Time to productivity x salary |
| Annual training cost | EUR X | L&D spend per head |
| Time to full productivity | X months | When new hire reaches 100% output |
| **ELTV** | **EUR X** | |

**ELTV Optimization Levers:**
1. Increase tenure (reduce turnover) = highest impact
2. Decrease time to productivity (better onboarding)
3. Decrease recruitment cost (better sourcing, employer brand)
4. Increase revenue per employee (training, tools, automation)

### Step 6: HR Analytics Data Model

**Key Data Sources:**

| Source | Data | Frequency | Quality |
|--------|------|-----------|---------|
| HRIS / Payroll | Demographics, salary, contract, attendance | Real-time | High |
| ATS | Applications, pipeline, time-to-hire, source | Per hire | Medium-High |
| Performance system | Ratings, OKRs, feedback | Quarterly | Medium |
| Survey platform | eNPS, engagement, pulse | Per survey | Medium |
| L&D platform | Training completion, certifications | Ongoing | Medium |
| Exit interviews | Reasons for leaving, feedback | Per exit | Variable |
| Financial system | Revenue, costs, budget | Monthly | High |

**RGPD Compliance for People Analytics:**
- Purpose limitation: only collect data needed for specific, documented purpose
- Data minimization: anonymize/aggregate where possible
- Consent: inform employees about data collection and analytics
- Access rights: employees can request their data
- Retention: delete data when no longer needed
- DPIA: required for profiling or automated decision-making
- No automated decisions with legal effects without human review

### Step 7: Dashboard Design

**Executive Dashboard (C-Suite, monthly):**
- Headcount and FTE trend (12 months)
- Revenue per employee trend
- Total turnover rate (rolling 12 months)
- eNPS trend
- Employee cost as % of revenue
- Top 3 flight risks (critical roles only)

**HR Operations Dashboard (HR team, weekly):**
- Open requisitions and pipeline status
- Time-to-fill by role and department
- Onboarding progress (new hires in first 90 days)
- Sick days and absenteeism trend
- Training compliance (40h/year PT requirement)
- Survey response rate and scores

**Manager Dashboard (each manager, bi-weekly):**
- Team composition and changes
- Team eNPS and engagement scores
- Individual performance status (OKR progress)
- Vacation usage per team member
- Overtime and workload indicators
- Flight risk alerts for direct reports

### Step 8: Analytics-Driven Interventions

| Insight | Data Signal | Intervention | Expected Impact |
|---------|-----------|-------------|----------------|
| High early turnover | First-year turnover >20% | Improve onboarding, hiring quality | -5pp first-year turnover |
| Manager-driven exits | Turnover correlated with specific managers | Manager coaching, 360 feedback | -10pp in affected teams |
| Compensation gap | Exit interviews cite pay 40%+ | Market adjustment for critical roles | -3pp overall turnover |
| Burnout signal | Avg hours >48, vacation <50% | Workload audit, mandatory time off | -2pp sick days |
| Diversity pipeline gap | Diverse candidates drop at interview stage | Bias training, structured interviews | +10pp diverse hires |

## Output Template

```markdown
# PESSOA People Analytics Report
## Organization: [NAME]
## Period: [QUARTER/YEAR]
## Date: YYYY-MM-DD

### Key Metrics Summary
| Metric | Value | vs Prior | Target | Status |
|--------|-------|---------|--------|--------|
| Headcount | X | +/-X | X | [status] |
| Turnover | X% | +/-X pp | <15% | [status] |
| Time to fill | X days | +/-X | <45 | [status] |
| eNPS | X | +/-X | >30 | [status] |
| Revenue/employee | EUR X | +/-X% | EUR X | [status] |

### Turnover Analysis
[Dimension breakdown with insights]

### Flight Risks
| Employee | Role | Risk Score | Action |
|----------|------|-----------|--------|
| [Name] | [Role] | X/5 | [Action] |

### Top 3 Data-Driven Actions
1. [Action — data signal — expected impact]
2. [Action — data signal — expected impact]
3. [Action — data signal — expected impact]

### ELTV: EUR X (trend: [up/down])

### Analytics Health Score: X/10
```

## Red Flags

Stop and warn the user if:
- No HR data tracked beyond headcount (flying blind)
- Analytics used for surveillance instead of support (trust destruction)
- Predictive models used for automated decisions without human review (RGPD violation)
- Employee data shared without proper anonymization/aggregation
- Turnover analysis never leads to action (data without decisions)
- Cost-per-hire unknown (cannot optimize recruitment spend)
- No exit interview data collected or analyzed
- Dashboard exists but nobody looks at it (vanity dashboard)
- Data quality poor (garbage in, garbage out)
- Flight risk scores shared with managers without context (creates bias)
- Analytics team reports to IT instead of HR (disconnected from people strategy)
- No RGPD/DPIA assessment for people analytics program

## Handoff

After people analytics:
- Route to `pessoa-engagement` for engagement-driven interventions
- Route to `pessoa-compensacao` for pay equity analytics
- Route to `pessoa-workforce` for workforce planning data
- Route to `pessoa-succession` for flight risk integration
- Route to `pessoa-dei` for diversity analytics
- Route to `risco-rgpd` for data protection compliance
- Save output to Obsidian: `05 - Claude - IA/Outputs/YYYY-MM-DD - PESSOA - Analytics Report - [Organization].md`
