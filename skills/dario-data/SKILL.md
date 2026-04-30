---
name: dario-data
description: Data squad — analytics, customer science, and growth hacking. Avinash Kaushik (See-Think-Do-Care, 10/90 rule), Peter Fader (CLV, Pareto/NBD), Sean Ellis (PMF, North Star Metric, AARRR, ICE). Triggers on "data", "analytics", "metrics", "CLV", "LTV", "churn", "cohort", "PMF", "north star metric", "AARRR", "pirate metrics", "growth", "activation", "retention", "ICE score", "dashboard".
version: 1.0.0
license: MIT
---

# DARIO Skill — Data Squad

Three minds, one mission: turn data into decisions. Combines Avinash Kaushik's digital analytics philosophy, Peter Fader's customer-centric CLV science, and Sean Ellis's growth hacking methodology into a single skill that answers "what should we measure, what does it mean, and what do we do about it?"

## Squad Agents

| Agent | Mindset | Core Philosophy | Superpower |
|-------|---------|----------------|------------|
| **Chief Data (Kaushik)** | "Fail faster, succeed sooner" | 10/90 rule: spend 10% on tools, 90% on people who analyze. See-Think-Do-Care framework for audience intent. | Cutting through vanity metrics to find actionable insights |
| **Customer Data Scientist (Fader)** | "Not all customers are created equal" | CLV models, customer-centricity, probability models (Pareto/NBD, BG/NBD). Future value > past revenue. | Predicting which customers matter most and why |
| **Growth Hacker (Ellis)** | "If you're not growing, you're dying" | Product-market fit test, North Star Metric, AARRR pirate metrics, ICE scoring for experiment prioritization. | Systematic experimentation for compounding growth |
| **Analytics Engineer** | "Garbage in, garbage out" | Data pipeline quality, warehouse design, metric definitions, dashboard architecture. The infrastructure that makes insights possible. | Building the measurement foundation everyone else depends on |

## When to activate

- "What should we be measuring?" — metric framework design
- "We have data but don't know what it means" — analysis and interpretation
- "How do we know if we have product-market fit?" — PMF assessment
- "Which customers should we focus on?" — CLV segmentation
- "Our growth is flat/declining" — growth audit and experiment design
- "We need a dashboard" — dashboard specification with the right metrics
- New product/feature launch — measurement plan before launch
- Fundraising preparation — metrics narrative for investors
- SaaS metrics deep-dive (MRR, churn, NRR, CAC payback)
- Cohort analysis request — retention curves, revenue cohorts
- Before any paid campaign — baseline metrics + attribution model
- User mentions LUSOconta, Atelier AI, or any SaaS project — data-driven product decisions

## Workflow

### 1. Gather context

- **Business model:** SaaS, e-commerce, marketplace, agency, services?
- **Stage:** pre-PMF, post-PMF, growth, scale?
- **Current data:** what's tracked, what tools exist (GA4, Mixpanel, Amplitude, Stripe, custom)?
- **Team:** who looks at data? How often? What decisions do they make with it?
- **Burning question:** what do they actually want to know?
- **Historical data:** how much history is available? (Months? Years?)

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "avinash kaushik see think do care framework analytics", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "peter fader CLV customer lifetime value pareto NBD", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "sean ellis product market fit north star metric AARRR", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "growth hacking ICE scoring experiment prioritization", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "cohort analysis retention churn SaaS metrics", collection: "dario", limit: 5)
```

### 3. Apply frameworks

#### Kaushik: See-Think-Do-Care

Map every metric and content piece to an audience intent stage:

| Stage | Audience | Intent | Key Metrics | Content Type |
|-------|----------|--------|-------------|-------------|
| **See** | Largest addressable qualified audience | Awareness, no intent to buy | Impressions, reach, brand search volume, new visitors | Blog, video, social, PR |
| **Think** | Audience with some commercial intent | Considering, researching | Engagement rate, time on site, pages/session, email signups | Comparison guides, webinars, case studies |
| **Do** | Audience with clear intent to buy | Ready to transact | Conversion rate, add-to-cart, sign-ups, trials, revenue | Product pages, pricing, demos, offers |
| **Care** | Existing customers (2+ purchases) | Loyalty, expansion | NPS, repeat purchase rate, CLV, upsell rate, referral rate | Onboarding, support, community, loyalty programs |

**Kaushik's 10/90 rule:** If the analytics budget is $100, spend $10 on tools and $90 on analysts who can extract insights. Tools without human interpretation produce dashboards no one reads.

#### Fader: Customer Lifetime Value (CLV)

**CLV = Average Revenue per Period x Customer Lifetime (periods) x Gross Margin**

For more sophisticated modeling:
- **Pareto/NBD model:** Predicts future purchasing behavior based on recency and frequency
- **BG/NBD model:** Simplified version, better for contractual settings (SaaS)
- **Gamma-Gamma model:** Predicts monetary value conditional on purchase frequency

**Key CLV insights:**
- Top 20% of customers typically generate 60-80% of revenue (Pareto principle)
- Acquiring a new customer costs 5-25x more than retaining an existing one
- A 5% increase in retention can increase profits by 25-95%
- CLV should guide: marketing spend allocation, feature prioritization, support investment

**CLV segmentation matrix:**

| Segment | CLV | Recency | Strategy |
|---------|-----|---------|----------|
| **Champions** | High | Recent | Reward, upsell, ask for referrals |
| **Loyal** | High | Moderate | Engage, prevent churn, deepen relationship |
| **At Risk** | High | Lapsed | Win-back campaign, personal outreach, understand why |
| **New High-Potential** | Low (so far) | Very recent | Activate quickly, onboard well, nurture toward champion |
| **Low Value** | Low | Any | Automate, self-serve, don't over-invest |

#### Ellis: Product-Market Fit & Growth

**PMF Test (Sean Ellis Test):**
Ask existing users: "How would you feel if you could no longer use [product]?"
- **Very disappointed** → PMF signal
- **Somewhat disappointed** → Weak signal
- **Not disappointed** → No PMF

**Threshold:** If 40%+ say "very disappointed," you have PMF. Below 40%, iterate on the product before scaling.

**North Star Metric (NSM):**
The single metric that best captures the core value your product delivers to customers.

| Business Type | NSM Example |
|---------------|-------------|
| SaaS | Weekly active users, or features used per session |
| E-commerce | Purchase frequency per customer |
| Marketplace | Transactions completed per week |
| Content/Media | Time spent reading/watching per session |
| Agency | Recurring retainer revenue |

**Rules for a good NSM:**
- Reflects customer value received (not just company revenue)
- Leading indicator of revenue (not lagging)
- Measurable weekly
- Actionable by the team
- One metric, not a composite

#### AARRR Pirate Metrics

| Stage | Metric | Benchmark (SaaS) | Diagnostic Question |
|-------|--------|-------------------|-------------------|
| **Acquisition** | Visitors, signups by channel | CAC varies by channel | "Where do our best customers come from?" |
| **Activation** | % completing key action within X days | 20-40% typical | "Do new users experience the aha moment?" |
| **Retention** | Day 1, Day 7, Day 30 retention | D1: 40%, D7: 20%, D30: 10% | "Do users come back after first use?" |
| **Revenue** | Conversion to paid, ARPU, MRR | Trial→paid: 2-5% (freemium), 15-25% (free trial) | "Do retained users pay?" |
| **Referral** | Viral coefficient, NPS, referral rate | K-factor > 0.5 is strong | "Do users tell others?" |

**Diagnosis priority:** Fix from the bottom up. Referral without retention is a leaky bucket. Revenue without activation means you're charging before delivering value. Always fix retention first.

#### ICE Scoring for Experiment Prioritization

For every growth experiment, score 1-10 on three dimensions:

| Dimension | Question | 1 (Low) | 10 (High) |
|-----------|----------|---------|-----------|
| **Impact** | If this works, how big is the effect? | Marginal improvement | 2x or more on target metric |
| **Confidence** | How sure are we this will work? | Pure guess | Strong data/precedent |
| **Ease** | How easy is this to implement? | Months of engineering | Ship in a day |

**ICE Score = (Impact + Confidence + Ease) / 3**

Run experiments in ICE score order. Review scores weekly. Kill experiments that don't move the metric within the test period.

### 4. Core metrics reference

#### SaaS Metrics (for LUSOconta, Atelier AI, and future SaaS)

| Metric | Formula | Healthy Range | Red Flag |
|--------|---------|---------------|----------|
| **MRR** | Sum of all monthly recurring revenue | Growing month-over-month | Flat or declining for 2+ months |
| **ARR** | MRR x 12 | Aligns with growth targets | Diverges from fundraise projections |
| **Net Revenue Retention (NRR)** | (Starting MRR + expansion - contraction - churn) / Starting MRR | > 100% (ideally > 110%) | < 90% means shrinking without new customers |
| **Gross Churn** | Lost MRR / Starting MRR | < 3% monthly (< 5% for SMB) | > 5% monthly — product or market problem |
| **CAC** | Total sales+marketing spend / New customers | Varies by ACV | CAC > 12 months of revenue |
| **LTV** | ARPU x (1 / Monthly Churn Rate) x Gross Margin | LTV:CAC > 3:1 | LTV:CAC < 1:1 — losing money on every customer |
| **CAC Payback** | CAC / Monthly Gross Margin per Customer | < 12 months | > 18 months — cash flow risk |
| **Activation Rate** | % of signups completing key action | > 25% | < 10% — onboarding is broken |
| **Trial-to-Paid** | % of trial users converting to paid | 15-25% (free trial), 2-5% (freemium) | < 1% — value proposition unclear |

#### E-commerce / Agency Metrics

| Metric | Formula | Notes |
|--------|---------|-------|
| **CAC** | Marketing spend / New customers | Track by channel |
| **AOV** | Revenue / Orders | Increase with bundles, upsells |
| **Purchase Frequency** | Orders / Unique customers | Per year |
| **Customer Retention Rate** | Customers at end / Customers at start | Excludes new acquisitions |
| **NPS** | % Promoters - % Detractors | > 50 is excellent |
| **Revenue per Employee** | Total revenue / FTE count | Agency benchmark: 100-200K EUR/year |

### 5. Dashboard specification

Every dashboard must answer: "What happened, why, and what should we do about it?"

**Structure:**
1. **Header:** NSM trend (current vs previous period vs target)
2. **AARRR funnel:** Each stage with trend arrows
3. **Cohort retention grid:** Monthly cohorts, retention by week/month
4. **Revenue breakdown:** By plan, by channel, by segment
5. **Experiment tracker:** Active experiments, results, next actions
6. **Alerts:** Metrics outside normal range

## Commands

| Command | Description |
|---------|-------------|
| `/pmf-test` | Design and analyze a Sean Ellis PMF survey — question design, distribution, scoring, interpretation |
| `/nsm-define` | Define the North Star Metric for a product — candidates, evaluation criteria, selection, input metrics |
| `/aarrr-audit` | Full AARRR pirate metrics audit — measure each stage, identify the weakest link, prioritize fixes |
| `/ice-backlog` | Create ICE-scored experiment backlog — brainstorm experiments, score each, rank by ICE, plan sprints |
| `/activation-optimize` | Activation rate deep-dive — map the activation funnel, find drop-off points, design experiments |
| `/clv-model` | Build CLV model — RFM segmentation, CLV calculation, segment strategies, marketing budget allocation |
| `/cohort-analysis` | Cohort retention analysis — build retention curves, identify healthy vs leaky cohorts, find patterns |
| `/dashboard-spec` | Design executive dashboard — metric selection, layout, data sources, update cadence, alert thresholds |
| `/metric-define` | Define a specific metric precisely — formula, data source, filters, frequency, owner, target |
| `/growth-audit` | Full growth audit — current state, bottlenecks, experiment history, recommended growth model |
| `/data-quality` | Data quality assessment — coverage, accuracy, freshness, consistency, gaps, remediation plan |
| `/attribution` | Marketing attribution model — channel performance, attribution methodology, budget reallocation |

## Output template

```markdown
---
project: <client or product>
date: <YYYY-MM-DD>
type: data-analysis
framework: <kaushik|fader|ellis|combined>
---

# Data Analysis — <Topic>

## Context
- Business: ...
- Model: SaaS / E-commerce / Agency / ...
- Stage: Pre-PMF / Post-PMF / Growth / Scale
- Data available: ...
- Burning question: ...

## Current State
### Key Metrics Snapshot
| Metric | Current | Previous Period | Trend | Target | Status |
|--------|---------|----------------|-------|--------|--------|
| ... | ... | ... | ... | ... | OK / Warning / Critical |

### See-Think-Do-Care Mapping
| Stage | Current Activity | Metrics | Gap |
|-------|-----------------|---------|-----|
| See | ... | ... | ... |
| Think | ... | ... | ... |
| Do | ... | ... | ... |
| Care | ... | ... | ... |

## Analysis

### PMF Assessment (if applicable)
- Ellis Test result: ...% "very disappointed"
- PMF status: Achieved / Approaching / Not yet
- Key signal: ...

### CLV Segmentation
| Segment | % of Customers | % of Revenue | Strategy |
|---------|---------------|-------------|----------|
| Champions | ... | ... | ... |
| Loyal | ... | ... | ... |
| At Risk | ... | ... | ... |
| Low Value | ... | ... | ... |

### AARRR Funnel
| Stage | Volume | Rate | Benchmark | Verdict |
|-------|--------|------|-----------|---------|
| Acquisition | ... | ... | ... | ... |
| Activation | ... | ... | ... | ... |
| Retention | ... | ... | ... | ... |
| Revenue | ... | ... | ... | ... |
| Referral | ... | ... | ... | ... |

**Weakest stage:** ...
**Recommended focus:** ...

### Cohort Retention
| Cohort | M0 | M1 | M2 | M3 | M6 | M12 |
|--------|----|----|----|----|----|----|
| ... | ... | ... | ... | ... | ... | ... |

## Recommendations

### North Star Metric
**Proposed NSM:** ...
**Rationale:** ...
**Input metrics:** ...

### Experiment Backlog (ICE-ranked)
| # | Experiment | Impact | Confidence | Ease | ICE | Status |
|---|-----------|--------|-----------|------|-----|--------|
| 1 | ... | ... | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... | ... | ... |

### Quick Wins (this week)
1. ...
2. ...
3. ...

### Strategic Moves (this quarter)
1. ...
2. ...

## Dashboard Specification
### Metrics to track
- ...
### Update cadence
- ...
### Alert thresholds
- ...

## Next Steps
- [ ] ...
```

## Save location

- Analytics reports → `05 - Claude - IA/Outputs/YYYY-MM-DD - Data - <Topic>.md`
- CLV models → `05 - Claude - IA/Outputs/YYYY-MM-DD - CLV Model - <Client>.md`
- Dashboard specs → `05 - Claude - IA/Outputs/YYYY-MM-DD - Dashboard Spec - <Client>.md`
- Growth audits → `05 - Claude - IA/Outputs/YYYY-MM-DD - Growth Audit - <Client>.md`

## Integration points

| Skill | Relationship |
|-------|-------------|
| `dario-c-level` | Data squad feeds metrics to CEO/CMO/COO for strategic decisions |
| `dario-saas-metrics` | Overlapping domain — use `dario-saas-metrics` for SaaS-specific deep dives, this skill for broader analytics |
| `dario-financial-model` | CLV and revenue metrics feed financial projections |
| `dario-pipeline` | Pipeline math uses data squad's conversion rate analysis |
| `dario-ads-blueprint` | Attribution and ROAS analysis for paid campaigns |
| `dario-product` | Product metrics (activation, retention) inform feature prioritization |
| `dario-product-mgmt` | NSM, AARRR, and ICE scoring shared with product management workflow |
| `dario-ai-engineering` | Data quality and pipeline design for AI systems |
| `dario-funnel` | Funnel conversion metrics and optimization |
| `dario-diagnose` | Diagnostic uses data squad for quantitative assessment |
| `dario-wp-audit` | Analytics audit as part of WordPress evaluation |
| `dario-obsidian-save` | All outputs saved to vault |

## Red flags / anti-patterns

- **Vanity metrics worship** — page views, total signups, social followers without context are vanity metrics. They go up and to the right but don't correlate with business outcomes. Always tie metrics to revenue or retention.
- **Dashboard without decisions** — a dashboard that no one looks at or that doesn't change behavior is wasted effort. Every metric on a dashboard must have an owner, a target, and a documented "if X happens, we do Y" response.
- **Premature optimization** — optimizing conversion rate when you have 50 visitors/month is statistical noise. You need volume before optimization makes sense. Focus on acquisition first, then optimize.
- **Measuring everything, analyzing nothing** — Kaushik's 10/90 rule. A team with 15 analytics tools and no analyst is worse off than a team with a spreadsheet and someone who thinks. Invest in people, not tools.
- **CLV without action** — calculating CLV and then treating all customers the same defeats the purpose. CLV must drive differentiated strategies: more investment in high-CLV segments, automated/self-serve for low-CLV.
- **Ignoring retention to chase acquisition** — a product with 5% monthly churn loses half its customers in a year. No amount of acquisition can outrun bad retention. Fix retention before scaling acquisition.
- **ICE scores without data** — assigning ICE scores based on gut feeling, then treating them as objective rankings. The scores are heuristics to structure debate, not truth. Update them as you learn.
- **Cohort analysis without segmentation** — aggregate retention curves hide segment-level insights. A flat retention curve might be the average of one segment with 80% retention and another with 10%. Always segment.
- **North Star Metric that the team can't influence** — an NSM that depends on external factors (market growth, competitor actions) rather than product/team actions is useless for decision-making. The team must be able to move the NSM through their work.
- **Attribution certainty** — no attribution model is perfect. Last-click, first-click, linear, and data-driven all have biases. Acknowledge the limitations, use directional guidance, and never make absolute claims about channel ROI.
