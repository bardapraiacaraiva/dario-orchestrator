---
name: "A360 Business Metrics Dashboard"
description: "Comprehensive business metrics tracking — CAC, LTV, MRR, churn, conversion rates, runway, burn rate, break-even timeline, unit economics health check. The financial pulse of the business."
version: "1.0"
agent: "A360 — Accelera 360"
category: "Phase 5 — Scale"
---

# A360 Business Metrics Dashboard

## Triggers

Activate this skill when the user says any of:
- "metrics", "metricas", "KPIs", "dashboard"
- "CAC", "LTV", "MRR", "churn", "burn rate"
- "how is my business doing?", "como esta o negocio?"
- "unit economics", "economia unitaria"
- "runway", "break-even", "ponto de equilibrio"
- "conversion rates", "taxas de conversao"
- "business health check", "saude do negocio"
- Any request to track, analyze, or report on business performance

## Frameworks & References

- **David Skok** (forEntrepreneurs) — SaaS metrics, CAC payback, LTV:CAC, Rule of 40
- **Alex Hormozi** ($100M Offers) — revenue per employee, enterprise value drivers
- **Eric Ries** (Lean Startup) — innovation accounting, actionable vs vanity metrics
- **Sean Ellis** (Hacking Growth) — North Star Metric, AARRR framework
- **Jason Lemkin** (SaaStr) — SaaS benchmarks, T2D3 growth, magic number
- **Tomasz Tunguz** — SaaS benchmarks, cohort analysis, unit economics

## Workflow

### Step 1: Business Type Classification

Metrics vary by model. Identify which applies:

| Model | Primary Metrics | Revenue Pattern |
|-------|----------------|-----------------|
| **SaaS / Subscription** | MRR, ARR, churn, NRR, CAC payback | Recurring |
| **E-commerce** | AOV, purchase frequency, COGS, inventory turns | Transactional |
| **Service / Agency** | Utilization rate, client LTV, project margin | Project-based |
| **Marketplace** | GMV, take rate, liquidity, supply/demand ratio | Commission |
| **Info Products / Courses** | Launch revenue, refund rate, completion rate | Launch/evergreen |
| **Hybrid** | Combine relevant metrics from above | Mixed |

### Step 2: Core Financial Metrics

| Metric | Formula | Your Number | Health |
|--------|---------|-------------|--------|
| **Monthly Revenue** | Total revenue this month | $X | |
| **MRR** (if recurring) | Sum of all monthly subscriptions | $X | |
| **ARR** | MRR x 12 | $X | |
| **Revenue Growth** (MoM) | (This month - Last month) / Last month | X% | >10% MoM early stage |
| **Gross Revenue** | Total before refunds/discounts | $X | |
| **Net Revenue** | After refunds, chargebacks, discounts | $X | |
| **Gross Margin** | (Revenue - COGS) / Revenue | X% | >60% SaaS, >40% services |
| **Net Profit Margin** | Net profit / Revenue | X% | >15% healthy |

### Step 3: Customer Acquisition Metrics

| Metric | Formula | Your Number | Benchmark |
|--------|---------|-------------|-----------|
| **CAC** | Total marketing + sales spend / New customers | $X | <1/3 of LTV |
| **Blended CAC** | All costs / All new customers (paid + organic) | $X | |
| **Paid CAC** | Paid marketing spend / Paid-acquired customers | $X | |
| **Organic CAC** | Organic marketing cost / Organic-acquired customers | $X | |
| **CAC Payback** | CAC / Monthly gross profit per customer | X months | <12 months |
| **Leads Generated** | Total new leads this month | X | |
| **Lead-to-Customer Rate** | New customers / New leads | X% | >2% |
| **Cost Per Lead (CPL)** | Marketing spend / Leads generated | $X | |
| **Traffic Sources** | Channel breakdown | | |

**CAC by Channel:**

| Channel | Spend | Customers | CAC | LTV:CAC |
|---------|-------|-----------|-----|---------|
| Facebook Ads | $X | X | $X | X:1 |
| Google Ads | $X | X | $X | X:1 |
| Organic/SEO | $X | X | $X | X:1 |
| Referral | $X | X | $X | X:1 |
| Email | $X | X | $X | X:1 |
| **Total** | **$X** | **X** | **$X** | **X:1** |

### Step 4: Customer Lifetime Value

| Metric | Formula | Your Number | Benchmark |
|--------|---------|-------------|-----------|
| **LTV (simple)** | ARPU x Avg. customer lifespan (months) | $X | >3x CAC |
| **LTV (with margin)** | ARPU x Gross margin % x Lifespan | $X | |
| **ARPU** | Monthly revenue / Active customers | $X | |
| **Avg. Lifespan** | 1 / Monthly churn rate | X months | |
| **LTV:CAC Ratio** | LTV / CAC | X:1 | >3:1 (ideal 5:1) |
| **Purchase Frequency** | Purchases / Customers (per year) | X | |
| **Avg. Order Value (AOV)** | Revenue / Number of orders | $X | |

**LTV Health Assessment:**
- LTV:CAC > 5:1 = Excellent (consider investing more in growth)
- LTV:CAC 3-5:1 = Healthy
- LTV:CAC 1-3:1 = Warning (optimize retention or reduce CAC)
- LTV:CAC < 1:1 = Critical (losing money on every customer)

### Step 5: Retention & Churn Metrics

| Metric | Formula | Your Number | Benchmark |
|--------|---------|-------------|-----------|
| **Monthly Churn Rate** | Lost customers / Start-of-month customers | X% | <5% |
| **Annual Churn** | 1 - (1 - monthly churn)^12 | X% | <30% |
| **Net Revenue Retention (NRR)** | (Start MRR + expansion - contraction - churn) / Start MRR | X% | >100% |
| **Gross Revenue Retention (GRR)** | (Start MRR - contraction - churn) / Start MRR | X% | >85% |
| **Logo Retention** | 1 - (Lost customers / Start customers) | X% | >90% |
| **Reactivation Rate** | Returned customers / Total churned | X% | |
| **Time to Churn** | Avg. months before customer leaves | X months | |

**Cohort Analysis:**
Track retention by signup month to spot trends.

| Cohort | Month 1 | Month 2 | Month 3 | Month 6 | Month 12 |
|--------|---------|---------|---------|---------|----------|
| Jan | 100% | X% | X% | X% | X% |
| Feb | 100% | X% | X% | X% | |
| Mar | 100% | X% | X% | | |

### Step 6: Funnel Conversion Metrics

| Stage | Visitors/Leads | Converted | Rate | Benchmark |
|-------|---------------|-----------|------|-----------|
| **Website → Lead** | X | X | X% | 2-5% |
| **Lead → MQL** | X | X | X% | 15-30% |
| **MQL → SQL** | X | X | X% | 30-50% |
| **SQL → Customer** | X | X | X% | 20-30% |
| **Customer → Repeat** | X | X | X% | 30%+ |
| **Customer → Referral** | X | X | X% | 15%+ |

### Step 7: Cash & Runway Metrics

| Metric | Formula | Your Number | Health |
|--------|---------|-------------|--------|
| **Cash on Hand** | Bank balance | $X | |
| **Monthly Burn Rate** | Total monthly expenses | $X | |
| **Revenue** | Monthly income | $X | |
| **Net Burn** | Burn rate - Revenue | $X | (negative = profitable) |
| **Runway** | Cash / Net burn | X months | >6 months |
| **Break-even Revenue** | Fixed costs / Gross margin % | $X/mo | |
| **Months to Break-even** | (Break-even - Current revenue) / Monthly growth | X months | |
| **Cash Conversion Score** | Free cash flow / Net income | X% | >80% |

**Runway Traffic Light:**
- GREEN: >12 months runway or profitable
- YELLOW: 6-12 months runway
- ORANGE: 3-6 months runway (start fundraising or cutting)
- RED: <3 months runway (emergency mode)

### Step 8: Growth Health Indicators

| Indicator | Formula | Your Number | Benchmark |
|-----------|---------|-------------|-----------|
| **Rule of 40** (SaaS) | Revenue growth % + Profit margin % | X | >40 = excellent |
| **Magic Number** (SaaS) | Net new ARR / Prior quarter S&M spend | X | >0.75 = efficient |
| **Quick Ratio** (SaaS) | (New MRR + Expansion) / (Contraction + Churn) | X | >4 = healthy |
| **Burn Multiple** | Net burn / Net new ARR | X | <2 = efficient |
| **Revenue per Employee** | Annual revenue / Full-time headcount | $X | >$100K |
| **Payback Period** | CAC / Monthly gross profit per customer | X months | <12 |

### Step 9: Unit Economics Summary Card

```
┌─────────────────────────────────────────────┐
│            UNIT ECONOMICS CARD              │
├─────────────────────────────────────────────┤
│  CAC:  $____    LTV:  $____    Ratio: __:1 │
│  ARPU: $____    Churn: ____%   NRR:  ____% │
│  Margin: ____%  Payback: ___ months         │
│  Burn:  $____   Runway: ___ months          │
│  Break-even: $____/mo   ETA: ___ months     │
├─────────────────────────────────────────────┤
│  Overall Health: [HEALTHY / WARNING / CRITICAL] │
└─────────────────────────────────────────────┘
```

### Step 10: Monthly Review Cadence

**Weekly check (5 min):**
- Revenue this week vs target
- New leads and customers
- Any churn events

**Monthly deep dive (1 hour):**
- Full dashboard update (all metrics)
- Cohort analysis update
- Funnel conversion review
- CAC by channel comparison
- Cash position and runway
- Growth experiment results

**Quarterly strategic review:**
- LTV:CAC trend
- Revenue growth trajectory
- Unit economics vs plan
- Competitive positioning
- Adjust targets for next quarter

## Output Template

```markdown
# A360 Metrics Dashboard
## Business: [NAME]
## Period: [MONTH YYYY]

### Revenue Summary
| Metric | This Month | Last Month | Change |
|--------|-----------|------------|--------|
| Revenue | $X | $X | +X% |
| Customers | X | X | +X |
| ARPU | $X | $X | +X% |

### Unit Economics
| Metric | Value | Status |
|--------|-------|--------|
| CAC | $X | [status] |
| LTV | $X | [status] |
| LTV:CAC | X:1 | [status] |
| Churn | X% | [status] |
| Gross Margin | X% | [status] |

### Cash Position
- Cash: $X | Burn: $X/mo | Runway: X months
- Break-even: $X/mo | ETA: X months

### Funnel Performance
[Stage-by-stage conversion rates]

### Health Score: [HEALTHY/WARNING/CRITICAL]

### Top 3 Actions This Month
1. [Action 1 — addresses biggest metric gap]
2. [Action 2]
3. [Action 3]
```

## Red Flags

Stop and warn the user if:
- LTV:CAC below 1:1 (losing money on every customer acquired)
- Monthly churn above 10% (business is a leaky bucket)
- Runway below 3 months with no funding plan
- CAC increasing month-over-month with no strategy change
- Revenue growth negative for 3+ consecutive months
- Gross margin below 30% (structural problem)
- Net Revenue Retention below 80% (not enough value delivered)
- Zero tracking in place (flying blind)
- Focusing on vanity metrics (followers, page views) instead of revenue metrics

## Handoff

After metrics review:
- Route to `a360-growth` if acquisition metrics need improvement
- Route to `a360-modelo` if unit economics need restructuring
- Route to `a360-scale` when metrics show readiness for next milestone
- Route to `a360-pitch` with metrics for investor conversations
- Feed to `dario-saas-metrics` for SaaS-specific deep dive
- Save output to Obsidian: `05 - Claude - IA/Outputs/YYYY-MM-DD - A360 - Metrics - [BusinessName].md`
