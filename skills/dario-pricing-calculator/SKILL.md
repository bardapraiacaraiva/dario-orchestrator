---
name: dario-pricing-calculator
description: Service pricing calculator for agencies — calculates real cost/hour, utilization-adjusted rates, project pricing with margins, retainer values. Uses Agency Business Model spec. Triggers on "pricing", "quanto cobrar", "rate hora", "preço do serviço", "margem", "utilization".
license: MIT
---

# DARIO Skill — Pricing Calculator

## Workflow
1. RAG: `search_kb("agency pricing utilization rate margin", collection: "dario")`
2. Gather: monthly costs, target income, hours available, utilization target
3. Calculate: real cost/hour, minimum rate, recommended rate, project pricing
4. Present 3 pricing tiers (Good/Better/Best)
5. Compare: hourly vs project vs retainer vs value-based

## Formulas
- Cost/hour = (Total monthly costs) / (Hours available × Utilization%)
- Min rate = Cost/hour × 1.3 (30% margin)
- Recommended rate = Cost/hour × 1.5-2.0
- Project price = (Estimated hours × Internal rate) × 1.5-2.0 markup

## Input Gathering

Collect the following inputs before running any calculation. Use defaults if the client does not provide a value:

| Input | Description | Default |
|---|---|---|
| **Monthly fixed costs** | Rent, software, subscriptions, insurance, accountant, tools, utilities | 3.000€ |
| **Owner target salary** | What the owner needs/wants to take home monthly (gross, before IRS) | 4.000€ |
| **Employee costs** | Total salaries + SS (23.75%) for all staff, or 0 if solo | 0€ |
| **Hours available/month** | Working hours per month (22 days x 8h = 176h, or adjusted) | 160h |
| **Utilization target** | % of hours that are billable (not admin, sales, learning) | 65% |
| **Profit margin target** | Desired net profit margin after all costs | 30% |
| **Annual one-off costs** | Training, conferences, equipment, divided by 12 | 500€/month |

## Calculation Engine

### Step-by-step with worked example (using defaults)

**Step 1: Total monthly cost**
```
Fixed costs:          3.000€
Owner salary:         4.000€
Employee costs:           0€
Annual one-offs/12:     500€
─────────────────────────────
Total monthly cost:   7.500€
```

**Step 2: Cost per available hour**
```
7.500€ / 160h = 46,88€/hour
```
This is your raw cost — if you charge this, you break even with 100% utilization (impossible).

**Step 3: Cost per billable hour (utilization-adjusted)**
```
160h × 65% utilization = 104 billable hours/month
7.500€ / 104h = 72,12€/hour
```
This is the real cost of each billable hour — the minimum to break even.

**Step 4: Minimum rate (with margin)**
```
72,12€ / (1 - 0.30) = 103,03€/hour
```
At this rate, with 65% utilization, you cover all costs + 30% profit margin.

**Step 5: Recommended rate**
```
Minimum rate × 1.3 = 133,94€ ≈ 135€/hour
```
Adds a buffer for scope creep, slow months, and investment in growth.

**Step 6: Premium rate**
```
Minimum rate × 1.8 = 185,45€ ≈ 185€/hour
```
For specialist work, urgent timelines, or high-value strategic projects.

### Summary table
| Metric | Value |
|---|---|
| Total monthly cost | 7.500€ |
| Billable hours/month | 104h |
| Break-even rate | 72€/h |
| Minimum rate (30% margin) | 103€/h |
| Recommended rate | 135€/h |
| Premium rate | 185€/h |
| Monthly revenue target (recommended) | 14.040€ |
| Annual revenue target | 168.480€ |

## Project Pricing Guide

Use this table to sanity-check project quotes. Ranges assume the recommended rate (~100-135€/h for a mid-level PT agency):

| Deliverable | Hour Range | Price Range (€) | Notes |
|---|---|---|---|
| Logo + brand identity basic | 8–20h | 800–2.500€ | Logo, colour palette, typography, basic guidelines |
| Full branding package | 25–50h | 3.000–7.000€ | Logo + identity manual + stationery + social templates |
| Website 5 pages (WordPress) | 40–80h | 3.000–8.000€ | Home, about, services, contact, blog setup |
| Website 10+ pages (custom) | 80–160h | 8.000–18.000€ | Custom design, CMS, integrations, SEO |
| E-commerce (WooCommerce) | 100–200h | 10.000–25.000€ | Product setup, payments (MB/MBWay), shipping |
| Landing page (single) | 10–25h | 1.000–3.000€ | Design + copy + form + analytics |
| SEO monthly retainer | 15–30h/month | 1.500–4.000€/month | Audit, on-page, content, link building, reporting |
| Content marketing monthly | 20–40h/month | 2.000–5.000€/month | Blog posts, social content, email newsletter |
| Social media management | 15–30h/month | 1.200–3.500€/month | Content creation, scheduling, community, reporting |
| Google Ads management | 10–20h/month | 800–2.500€/month + ad spend | Setup, optimization, reporting, excludes ad budget |

> **Rule of thumb:** If a project quote feels too low, it probably is. Always calculate hours honestly, then apply markup. Never price from the client's budget downward.

## Pricing Model Comparison

| Model | How it works | Pros | Cons | When to use |
|---|---|---|---|---|
| **Hourly** | Bill per hour worked, tracked and reported | Transparent, fair for undefined scope, easy to start | Penalises efficiency, client anxiety about hours, income ceiling | Discovery phases, consulting, maintenance, undefined scope |
| **Project-based** | Fixed price for defined deliverables | Predictable for client, rewards efficiency, cleaner scope | Risk if scope grows, requires accurate estimation | Websites, branding, campaigns with clear deliverables |
| **Retainer** | Fixed monthly fee for allocated hours/services | Recurring revenue, deeper client relationship, predictable cash flow | Scope creep risk, client may under-use, harder to raise price | Ongoing SEO, social media, content, support |
| **Value-based** | Price based on business outcome, not hours | Highest margins, aligns with client goals, no hour-tracking | Requires deep understanding of client's business, harder to justify without track record | Strategic projects, revenue-generating assets, clients with clear ROI metrics |

### Hybrid approach (recommended for PT agencies)
- **New clients:** Start project-based to build trust and deliver a clear win
- **Ongoing work:** Move to retainer after the first project succeeds
- **Strategic clients:** Layer value-based pricing for high-impact projects (e.g., e-commerce redesign that will increase conversion by 2x)

## PT Market Context

Typical agency rates in Portugal (2024-2026 reference):

| Level | Hourly Rate | Monthly Retainer (typical) | Profile |
|---|---|---|---|
| **Junior** | 25–40€/h | 800–1.500€/month | 0-2 years experience, execution-focused, needs supervision |
| **Mid-level** | 40–70€/h | 1.500–3.500€/month | 2-5 years, autonomous, manages small projects |
| **Senior** | 70–120€/h | 3.500–7.000€/month | 5-10 years, strategic input, client-facing, leads teams |
| **Specialist** | 100–200€/h | 5.000–12.000€/month | Deep expertise (SEO, performance, security, UX), consulting |
| **Agency blended rate** | 60–100€/h | — | Average across team for project quoting |

### Key PT market notes
- **Lisbon/Porto premium:** Rates 15-25% higher than rest of country
- **International clients:** Can charge 1.5-2x PT rates when working with EU/US clients remotely
- **IVA:** Always quote without IVA (23%) for B2B, with IVA for B2C. Clarify in every proposal.
- **Freelancer vs agency:** Solo freelancers typically charge 60-70% of agency rates but cannot scale
- **Race to the bottom risk:** Many PT agencies undercharge at 30-50€/h blended — this is unsustainable. The calculator above proves why.
- **SS contributions:** Freelancers pay 21.4% SS on 70% of income; factor this into solo pricing. Empresarios em nome individual pay differently from Unipessoal Lda.

## Save Location

Save generated pricing calculations to Obsidian:
- **Path:** `05 - Claude - IA/Outputs/YYYY-MM-DD - Pricing - [ClientOrContext] - Calculator.md`
- Include frontmatter: `type: pricing`, `client:`, `rate_recommended:`, `monthly_target:`, `status: draft`

## Red Flags

Stop and flag to the user if any of these are detected:
- Calculated minimum rate is below 50€/h (agency is structurally unprofitable)
- Utilization target set above 80% (unrealistic — leaves no time for sales, admin, learning)
- Profit margin target below 15% (no buffer for slow months or unexpected costs)
- Client expects project pricing but cannot define scope (use hourly or discovery phase first)
- Quoted price is more than 30% below the Project Pricing Guide range (undercharging risk)
- Owner salary set to 0€ (unsustainable — the business must pay the owner)
- No budget for annual training/tools (agency skills will decay, losing competitiveness)
