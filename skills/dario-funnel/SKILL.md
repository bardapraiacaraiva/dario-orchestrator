---
name: dario-funnel
description: Sales funnel builder using Russell Brunson's Value Ladder, DotCom Secrets funnels, and Epiphany Bridge storytelling. Designs the full funnel structure (lead magnet → tripwire → core → profit maximizer). Triggers on "funnel", "funil", "value ladder", "tripwire", "lead magnet", "upsell sequence".
license: MIT
---

# DARIO Skill — Funnel Builder

Designs a complete multi-step sales funnel from lead magnet to profit maximizer. Based on Brunson's DotCom Secrets + Expert Secrets + Traffic Secrets trilogy.

## When to activate
- Client wants "a funnel" (often vague — this skill structures it)
- After `dario-offer` (offer exists, now needs a delivery mechanism)
- E-commerce upsell/cross-sell flow design
- Webinar/challenge funnel planning
- SaaS trial-to-paid conversion flow

## Workflow

### 1. RAG consult
```
mcp__dario-rag__search_kb(query: "brunson value ladder funnel epiphany bridge", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "funnel lead magnet tripwire profit maximizer", collection: "dario", limit: 5)
```

### 2. Identify funnel type
| Funnel | Use when |
|---|---|
| **Lead Magnet → Tripwire → Core** | First-time customer acquisition |
| **Webinar** | High-ticket ($1K+), education-based |
| **Challenge** (5/7 day) | Community, transformation-based |
| **Product Launch (PLF)** | Seasonal launch, waitlist |
| **Ascension** | Existing customers → higher tier |
| **SaaS Trial** | Free trial → paid conversion |

### 3. Design Value Ladder
```
[Lead Magnet — FREE]     → builds trust, captures email
     ↓
[Tripwire — $7-$47]     → converts to buyer, lowers acquisition cost
     ↓
[Core Offer — $97-$997] → main revenue, solves main problem
     ↓
[Profit Maximizer — $997+] → high-ticket, done-for-you, continuity
     ↓
[Return Path]            → email nurture, retargeting, community
```

### 4. Map pages + copy needs
For each step:
- **Landing page** (pairs with `dario-sales-letter`)
- **Thank you / confirmation page** (next step CTA)
- **Email sequence** (pairs with `dario-email-seq`)
- **Upsell page** (one-click, time-limited)
- **Downsell page** (if upsell refused, offer lighter version)

### 5. Tracking + metrics per step
| Step | KPI | Target |
|---|---|---|
| Lead Magnet LP | Opt-in rate | 25-45% |
| Tripwire page | Purchase rate | 5-10% of leads |
| Core offer | CVR from nurture | 2-5% |
| Upsell | Take rate | 15-30% |
| Downsell | Take rate | 10-20% |

## Output template
```markdown
# Funnel Blueprint — <Client / Offer>

## Value Ladder
<visual ladder>

## Step-by-step flow
### Step 1: Lead Magnet
- Page: ...
- Offer: ...
- Email: welcome sequence (5 emails)

### Step 2: Tripwire
...

## Pages needed (with copy briefs)
## Email sequences needed
## Tracking events
## Tech stack (ClickFunnels / WordPress / custom)
## Budget estimate + expected metrics
```

## Epiphany Bridge (Brunson's Storytelling Framework)

Every funnel step needs a story to bridge the gap between "I don't need this" and "I must have this":

1. **Backstory** — Where were you before the transformation?
2. **Wall** — What obstacle did you hit?
3. **Epiphany** — What did you realize / discover?
4. **Plan** — What did you do about it?
5. **Result** — What happened? (specific, measurable)
6. **Transformation** — Who are you now?

Apply this in: lead magnet LP copy, webinar intro, email sequences, sales page.

## Integration

- Runs AFTER `dario-offer` (need a defined offer to build a funnel around)
- Landing page copy pairs with `dario-sales-letter`
- Email sequences pair with `dario-email-seq`
- Traffic plan pairs with `dario-ads-blueprint`
- Tracking/metrics feed into `lucas-analytics`

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Funnel Blueprint.md`

## Red Flags

- Never build a funnel without a validated offer first (use `dario-offer`)
- Never skip the downsell — it recovers 10-20% of lost upsell revenue
- Never launch a funnel without email sequences in place (lead magnet without nurture = wasted leads)
- Always include exit-intent or abandoned cart recovery for paid steps
- Always test the full path (mobile + desktop) before going live
- Value Ladder must have at least 3 levels — a single-product funnel isn't a funnel
