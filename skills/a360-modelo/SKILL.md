---
name: "A360 Business Model Design"
description: "Design a complete business model — revenue streams, pricing strategy, unit economics, cost structure, value chain, competitive moat, and scalability assessment. From idea to viable business architecture."
version: "1.0"
agent: "A360 — Accelera 360"
category: "Phase 2 — Validation"
license: SEE-LICENSE
parent_agent: a360-director
compliance: [audit_immutable]
---

# A360 Business Model Design

## Triggers

Activate this skill when the user says any of:
- "business model", "modelo de negocio"
- "revenue model", "modelo de receita"
- "pricing strategy", "estrategia de precos"
- "unit economics", "economia unitaria"
- "how will I make money?", "como vou ganhar dinheiro?"
- "cost structure", "estrutura de custos"
- "scalability", "escalabilidade"
- Any request to design the financial and operational backbone of a business

## Frameworks & References

- **Alex Osterwalder** (Business Model Canvas) — 9 building blocks
- **Alex Hormozi** ($100M Offers) — pricing based on value, not cost
- **Eric Ries** (Lean Startup) — validated learning, pivot points, innovation accounting
- **Peter Thiel** (Zero to One) — monopoly characteristics, 10x value
- **Hamilton Helmer** (7 Powers) — counter-positioning, switching costs, network effects, scale economies, branding, cornered resource, process power
- **Patrick Campbell** (ProfitWell) — pricing methodology, value metrics

## Workflow

### Step 1: Business Model Canvas (Osterwalder)

Fill each of the 9 blocks:

| Block | Description | Your Answer |
|-------|-------------|-------------|
| **Customer Segments** | Who are you serving? | [from a360-avatar] |
| **Value Propositions** | What unique value? | [from a360-oferta or hypothesis] |
| **Channels** | How do you reach them? | [from a360-funil] |
| **Customer Relationships** | How do you retain? | [self-serve/personal/automated] |
| **Revenue Streams** | How do you earn? | [see Step 2] |
| **Key Resources** | What assets needed? | [tech/people/IP/capital] |
| **Key Activities** | What must you do daily? | [development/marketing/delivery] |
| **Key Partnerships** | Who do you need? | [suppliers/affiliates/platforms] |
| **Cost Structure** | What are the costs? | [see Step 4] |

### Step 2: Revenue Model Selection

Choose and design the primary revenue model:

| Model | Description | Best For | Scalability |
|-------|-------------|----------|-------------|
| **One-time sale** | Single purchase | Physical products, courses | Low |
| **Subscription/SaaS** | Recurring payment | Software, content, services | Very High |
| **Freemium** | Free tier + paid upgrade | SaaS, apps, platforms | High |
| **Marketplace/Commission** | % of transactions | Platforms, directories | Very High |
| **Advertising** | Monetize attention | Media, content, apps | High (at scale) |
| **Licensing** | Charge for IP usage | Software, frameworks, content | High |
| **Service retainer** | Monthly recurring service | Agencies, consulting | Medium |
| **Usage-based** | Pay per use | API, cloud, utilities | High |
| **Affiliate** | Commission on referrals | Content creators, influencers | Medium |
| **Hybrid** | Combination of above | Mature businesses | Varies |

**Recommended for 0-to-revenue speed**: Start with service/one-time, transition to recurring.

### Step 3: Pricing Strategy

**Value-Based Pricing (Hormozi method):**
1. What is the dream outcome worth to the customer? = $X
2. Your price should be 10-20% of that value = $Y
3. Test 3 price points: Low ($Y x 0.7), Mid ($Y), High ($Y x 1.5)

**Pricing Tiers:**

| Tier | Name | Price | Includes | Target % |
|------|------|-------|----------|----------|
| **Basic** | [Name] | $X/mo | [Core features] | 60% |
| **Pro** | [Name] | $X/mo | [Core + advanced] | 30% |
| **Premium** | [Name] | $X/mo | [Everything + VIP] | 10% |

**Price Anchoring**: Always show the highest tier first. Use a "decoy" tier to push toward your target tier.

**Pricing Psychology:**
- Charm pricing ($97 vs $100) for consumer
- Round pricing ($500, $1000) for B2B / high-ticket
- Annual discount (2 months free) to reduce churn
- Founding member pricing for launch validation

### Step 4: Cost Structure

| Cost Category | Monthly | Annual | Type |
|---------------|---------|--------|------|
| **Fixed Costs** | | | |
| Hosting / Infrastructure | $X | $X | Fixed |
| Tools / Software | $X | $X | Fixed |
| Team / Freelancers | $X | $X | Fixed |
| Office / Workspace | $X | $X | Fixed |
| **Variable Costs** | | | |
| Customer acquisition (CAC) | $X | $X | Variable |
| Payment processing fees | $X | $X | Variable |
| Delivery / Fulfillment | $X | $X | Variable |
| Support | $X | $X | Semi-variable |
| **Total Monthly Burn** | **$X** | **$X** | |

### Step 5: Unit Economics

Calculate the fundamental health metrics:

| Metric | Formula | Your Number | Healthy Range |
|--------|---------|-------------|---------------|
| **CAC** (Customer Acquisition Cost) | Total marketing / new customers | $X | Varies |
| **LTV** (Lifetime Value) | ARPU x avg. lifespan (months) | $X | >3x CAC |
| **LTV:CAC Ratio** | LTV / CAC | X:1 | >3:1 |
| **Gross Margin** | (Revenue - COGS) / Revenue | X% | >60% (SaaS), >40% (services) |
| **Payback Period** | CAC / monthly ARPU | X months | <12 months |
| **Break-even** | Fixed costs / (price - variable cost per unit) | X units | |
| **Monthly Burn Rate** | Total monthly expenses | $X | |
| **Runway** | Cash / burn rate | X months | >6 months |

**Unit Economics Health Check:**
- LTV:CAC > 3:1 = Healthy
- LTV:CAC 1-3:1 = Survivable but tight
- LTV:CAC < 1:1 = Unsustainable (losing money per customer)

### Step 6: Value Chain Analysis

Map where you create and capture value:

```
[Input] → [Activity 1] → [Activity 2] → [Activity 3] → [Output/Customer]
  $cost      $cost           $cost          $cost          $revenue
```

For each activity:
- Build vs Buy vs Partner decision
- Core competency? (keep in-house)
- Commodity? (outsource/automate)
- Differentiator? (invest heavily)

### Step 7: Competitive Moat Assessment (Hamilton Helmer's 7 Powers)

| Power | Applicability | Score (1-5) | Strategy to Build |
|-------|--------------|-------------|-------------------|
| **Scale Economies** | Cost advantages from size | /5 | [action] |
| **Network Effects** | Product improves with more users | /5 | [action] |
| **Counter-Positioning** | Incumbents can't copy without hurting themselves | /5 | [action] |
| **Switching Costs** | Painful for customers to leave | /5 | [action] |
| **Branding** | Willingness to pay premium | /5 | [action] |
| **Cornered Resource** | Exclusive access to asset | /5 | [action] |
| **Process Power** | Superior operational ability | /5 | [action] |

**Moat Score: X/35**
- 25-35: Strong defensibility
- 15-24: Moderate, needs strengthening
- 0-14: Weak, vulnerable to competition

### Step 8: Scalability Assessment

| Dimension | Current | At 10x Scale | Bottleneck? |
|-----------|---------|--------------|-------------|
| **Revenue** | $X/mo | $X/mo | |
| **Team size** | X | X | Y/N |
| **Tech infrastructure** | [description] | [needed] | Y/N |
| **Delivery capacity** | X units/mo | X units/mo | Y/N |
| **Customer support** | [method] | [needed] | Y/N |
| **Cash requirements** | $X | $X | Y/N |

**Scalability Score:**
- Product scales with zero marginal cost (SaaS, digital) = 10/10
- Product scales with low marginal cost (templates, courses) = 7/10
- Product scales linearly with headcount (services) = 4/10
- Product doesn't scale (1-on-1 custom work) = 2/10

### Step 9: Revenue Projections (3 Scenarios)

| Month | Conservative | Base Case | Optimistic |
|-------|-------------|-----------|------------|
| 1 | $X | $X | $X |
| 3 | $X | $X | $X |
| 6 | $X | $X | $X |
| 12 | $X | $X | $X |
| 18 | $X | $X | $X |
| 24 | $X | $X | $X |

Assumptions for each scenario documented clearly.

## Output Template

```markdown
# A360 Business Model Design
## Business: [NAME]
## Date: YYYY-MM-DD

### Business Model Canvas
[9-block summary]

### Revenue Model: [TYPE]
[Description of how money is earned]

### Pricing
| Tier | Price | Includes |
|------|-------|----------|
| Basic | $X | [features] |
| Pro | $X | [features] |
| Premium | $X | [features] |

### Unit Economics
| Metric | Value | Health |
|--------|-------|--------|
| CAC | $X | [status] |
| LTV | $X | [status] |
| LTV:CAC | X:1 | [status] |
| Gross Margin | X% | [status] |
| Break-even | X units/mo | [status] |

### Competitive Moat: X/35
[Top 3 powers to develop]

### Scalability: X/10
[Key bottlenecks and solutions]

### 12-Month Revenue Projection
[Base case with key assumptions]

### Critical Risks
1. [Risk 1] — Mitigation: [action]
2. [Risk 2] — Mitigation: [action]
3. [Risk 3] — Mitigation: [action]
```

## Red Flags

Stop and warn the user if:
- LTV:CAC ratio is below 1:1 (business loses money on every customer)
- Break-even requires more than 18 months at current burn rate
- Gross margins below 30% with no path to improvement
- No identifiable moat and operating in a crowded market
- Revenue model depends entirely on advertising (high risk at small scale)
- Pricing is based on cost-plus instead of value (leaving money on the table)
- User is planning to be the cheapest option (race to the bottom)
- No clear path from current model to scalable model
- Cash requirements exceed available capital with no funding plan

## Handoff

After business model design:
- Route to `a360-oferta` to construct the irresistible offer
- Route to `a360-metricas` to set up the metrics dashboard
- Route to `a360-pitch` if seeking investment/partners
- Save output to Obsidian: `05 - Claude - IA/Outputs/YYYY-MM-DD - A360 - Business Model - [BusinessName].md`
