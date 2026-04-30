---
name: client-health
description: "C.L.I.E.N.T. Health Scoring — engagement metrics, usage patterns, support tickets, NPS, churn prediction model, and risk tiers (green/yellow/red)"
version: "1.0"
agent: CLIENT
tags: [health-score, churn-prediction, engagement, NPS, risk-tiers, customer-success]
---

# CLIENT Health Scoring Skill

## Triggers

Activate this skill when the user says or implies:
- "customer health", "health score", "client health"
- "churn prediction", "churn risk", "at-risk accounts"
- "engagement metrics", "usage patterns", "adoption metrics"
- "risk tier", "green/yellow/red", "account risk"
- "support ticket trends", "NPS score", "customer sentiment"
- "early warning", "proactive alerts"

## Workflow

### Step 1 — Define Health Dimensions (5 Pillars)
1. **Product Engagement** (weight: 30%)
   - DAU/WAU/MAU ratios, feature adoption breadth, session depth
   - Login frequency trend (increasing / stable / declining)
   - Key feature usage vs. contracted use case
   - Power user ratio (users exceeding baseline engagement)
2. **Support Health** (weight: 20%)
   - Ticket volume trend (normalized per user)
   - Average resolution time, first-response time
   - Escalation rate, severity distribution
   - Sentiment analysis on support interactions
3. **Relationship Quality** (weight: 20%)
   - NPS / CSAT / CES scores (latest + trend)
   - Executive sponsor engagement level
   - Meeting attendance and responsiveness
   - Champion strength (single vs. multi-threaded)
4. **Financial Health** (weight: 15%)
   - Payment timeliness, outstanding invoices
   - Contract value trend (growing / flat / shrinking)
   - Expansion signals vs. contraction signals
   - Budget cycle alignment
5. **Strategic Fit** (weight: 15%)
   - Product roadmap alignment with customer needs
   - Competitive threat level
   - Industry / market headwinds affecting customer
   - Organizational changes (M&A, leadership turnover)

### Step 2 — Scoring Model
- Each dimension: 0–100 score
- Weighted composite: sum of (dimension_score x weight)
- **Green**: 70–100 (healthy, growth potential)
- **Yellow**: 40–69 (at risk, needs intervention)
- **Red**: 0–39 (critical, immediate action required)

### Step 3 — Churn Prediction Signals
- Declining login frequency over 3+ consecutive weeks
- NPS detractor score (0–6) with no follow-up resolution
- Champion departure without new champion identified
- Support escalation rate >15% of total tickets
- Contract renewal <90 days away + no renewal conversation started
- Feature requests repeatedly deprioritized
- Competitor mentioned in support tickets or meetings

### Step 4 — Intervention Playbooks by Tier
- **Green**: Quarterly QBR, expansion conversations, advocacy asks
- **Yellow**: Bi-weekly check-ins, success plan review, executive outreach, training refresh
- **Red**: War room activation, executive escalation, save plan with 30-day milestones, daily monitoring

### Step 5 — Dashboard & Reporting
- Portfolio health distribution (% green/yellow/red)
- Trending accounts (improving vs. declining)
- Cohort analysis (by segment, plan, tenure)
- Leading indicators dashboard for early warning

## Commands

```
/client-health [company_name]         — Calculate health score with breakdown
/client-health portfolio              — Portfolio-wide health distribution
/client-health trending               — Accounts with biggest score changes (30d)
/client-health alerts                 — Active red/yellow alerts requiring action
/client-health model [segment]        — Configure scoring weights for a segment
```

## Output Template

```markdown
# Customer Health Report: [Company Name]

## Overall Score: [XX]/100 — [GREEN/YELLOW/RED]

### Dimension Breakdown
| Dimension | Score | Weight | Weighted | Trend |
|-----------|-------|--------|----------|-------|
| Product Engagement | [XX] | 30% | [XX] | [arrow] |
| Support Health | [XX] | 20% | [XX] | [arrow] |
| Relationship Quality | [XX] | 20% | [XX] | [arrow] |
| Financial Health | [XX] | 15% | [XX] | [arrow] |
| Strategic Fit | [XX] | 15% | [XX] | [arrow] |

## Churn Risk Signals
- [ ] [Signal 1 — severity, evidence]
- [ ] [Signal 2 — severity, evidence]

## Recommended Actions
1. [Action] — Owner: [Name] — Deadline: [Date]
2. [Action] — Owner: [Name] — Deadline: [Date]

## 30-Day Forecast
- Predicted tier at +30d: [GREEN/YELLOW/RED]
- Key driver: [factor most likely to change score]
```

## Red Flags

- Health score drops >15 points in a single month without documented cause
- Account stays Yellow for >60 days without an active intervention plan
- Red account with no executive escalation within 48 hours
- NPS detractor with no closed-loop follow-up within 5 business days
- Champion departure detected with no succession plan
- Zero product usage for >14 consecutive days
- Support tickets increasing month-over-month for 3+ months
- Financial health flagged (late payments) combined with engagement decline
- Health score calculated without fresh data (>30 days stale)
- Portfolio has >25% accounts in Yellow/Red without a capacity plan for CSM team

## Integration Points

- Receives from: `client-onboard` (initial baseline), `client-voc` (NPS/CSAT), `client-qbr` (relationship data)
- Feeds into: `client-renewal` (risk-aware renewal), `client-recovery` (churn save triggers), `client-expansion` (green accounts)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - CLIENT - Health [Company].md`

## Metrics to Track

- **Portfolio Health Distribution**: % of accounts in each tier over time
- **Prediction Accuracy**: % of churned accounts that were flagged Red/Yellow >60d prior
- **Intervention Effectiveness**: % of Yellow accounts returned to Green within 90d
- **False Positive Rate**: % of Red alerts that resolved without intervention
- **Time to Intervene**: Average days from score drop to first action taken
