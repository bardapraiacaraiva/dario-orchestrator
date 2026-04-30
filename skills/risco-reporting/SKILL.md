---
name: risco-reporting
description: "Compliance reporting — KRI dashboards, incident log, board reports, regulatory filings, compliance metrics"
version: "1.0"
---

# RISCO-REPORTING: Compliance Reporting & Dashboards Skill

## When to Activate

**Trigger words (PT):** relatorio de compliance, dashboard, kri, indicadores de risco, relatorio ao conselho, metricas, incidente, registo de incidentes, relatorio regulatorio, kpi de compliance
**Trigger words (EN):** compliance report, dashboard, kri, key risk indicators, board report, metrics, incident log, regulatory reporting, compliance kpi, compliance dashboard, management information

## Step-by-Step Workflow

### Phase 1: KRI Framework Design
1. Select KRIs per risk domain:
   - **RGPD**: data breaches, DSR response time, consent rate, DPIAs completed
   - **AML**: STRs filed, CDD completion rate, overdue reviews, alerts cleared
   - **Audit**: open findings, overdue actions, audit plan completion
   - **Contracts**: SLA breaches, overdue renewals, disputes active
   - **BCP**: test frequency, action item closure, plan review currency
   - **Ethics**: training completion, COI declarations, reports received
2. Define thresholds: green/amber/red for each KRI
3. Assign data owners and collection frequency
4. Validate data quality and calculation methodology

### Phase 2: Incident Log
1. Standardize incident categories: data breach, compliance breach, regulatory fine, fraud, operational failure, security incident
2. Capture: date, category, description, impact, root cause, remediation, status
3. Severity classification: Critical / Major / Minor / Near-miss
4. Trend analysis: frequency by category, month-over-month
5. Lessons learned integration
6. Regulatory notification tracking (filed / not required / pending)

### Phase 3: Management Dashboard
1. Design one-page compliance health dashboard
2. Include: overall compliance score, traffic light KRIs, trend arrows
3. Top risks summary with movement since last period
4. Open action items by priority and age
5. Upcoming deadlines (next 30/60/90 days)
6. Refresh frequency: monthly minimum

### Phase 4: Board/Audit Committee Reporting
1. Quarterly compliance report structure:
   - Executive summary (1 page max)
   - Compliance program highlights and lowlights
   - KRI dashboard with commentary
   - Top risks and emerging risks
   - Regulatory change pipeline
   - Incident summary
   - Open audit findings status
   - Compliance budget vs actual
2. Annual compliance report: program effectiveness review
3. Ad-hoc reports for material events

### Phase 5: Regulatory Filings
1. Calendar of all regulatory reporting obligations
2. Template library per filing type
3. Preparation checklist and review/approval workflow
4. Filing confirmation and record keeping
5. Track: due date, submitted date, accepted/rejected, follow-up

### Phase 6: Continuous Improvement
1. Benchmark KRIs against prior periods and industry
2. Identify root causes for deteriorating metrics
3. Feed insights into risk assessment updates
4. Automate data collection where possible
5. Annual review of KRI relevance and thresholds
6. Stakeholder feedback on report usefulness

## Commands Table

| Command | Description |
|---------|-------------|
| `risco report dashboard` | Generate compliance dashboard |
| `risco report kri` | KRI framework and scorecard |
| `risco report incident` | Incident log template |
| `risco report board` | Board/Audit Committee report |
| `risco report regulatory` | Regulatory filing tracker |
| `risco report annual` | Annual compliance program report |
| `risco report metrics` | Compliance metrics calculation guide |
| `risco report trend` | Trend analysis and benchmarking |

## Output Template

```markdown
# Compliance Dashboard — [Organization]
**Period:** YYYY-MM | **Compliance Officer:** [Name]

## 1. Overall Compliance Health: [GREEN/AMBER/RED] — Score: X/100

## 2. KRI Scorecard
| # | KRI | Target | Actual | Status | Trend |
|---|-----|--------|--------|--------|-------|
| 1 | Data breaches (month) | 0 | | | |
| 2 | DSR response within 30d | 100% | | | |
| 3 | CDD completion rate | >95% | | | |
| 4 | Open audit findings (Critical/High) | 0 | | | |
| 5 | Training completion | >90% | | | |
| 6 | SLA compliance | >98% | | | |
| 7 | BCP test current | Yes | | | |
| 8 | Regulatory deadlines met | 100% | | | |

## 3. Incident Summary (Period)
| Category | Count | Severity | Trend | Notified |
|----------|-------|----------|-------|----------|

## 4. Top 5 Risks
| # | Risk | Score | Movement | Owner | Action Status |
|---|------|-------|----------|-------|---------------|

## 5. Open Actions (Overdue/Critical)
| # | Source | Action | Owner | Due | Days Overdue |
|---|--------|--------|-------|-----|-------------|

## 6. Upcoming Deadlines (30d)
| Date | Obligation | Owner | Status |
|------|-----------|-------|--------|

## 7. Compliance Budget
| Category | Budget | Actual | Variance |
|----------|--------|--------|----------|

## 8. Next Board Report: YYYY-MM-DD
```

## Red Flags

- No compliance dashboard or regular reporting to management
- KRIs not defined or thresholds not set
- Incident log not maintained or incidents not categorized
- Board/Audit Committee not receiving compliance reports
- Regulatory filings missed or filed late
- Data quality issues undermining KRI accuracy
- No trend analysis (point-in-time only, no context)
- Compliance metrics always green (possible underreporting)
- No escalation mechanism for KRI threshold breaches
- Reports produced but no action taken on findings
- Compliance program effectiveness never assessed
- Manual data collection creating bottlenecks and errors
