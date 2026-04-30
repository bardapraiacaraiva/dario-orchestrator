---
name: dario-ads-blueprint
description: Paid traffic campaign blueprint for Facebook / Google / YouTube ads. Covers audiences, creative framework, funnel structure, tracking, budget allocation, and KPIs. Based on Pittman / Burns / Kasim / Breeze / Sobral frameworks. Triggers on "ads", "tráfego pago", "facebook ads", "google ads", "youtube ads", "campanha", "media buying".
license: MIT
---

# DARIO Skill — Paid Ads Blueprint

Designs a ready-to-execute paid traffic campaign. Does not write creative copy itself (pairs with `dario-sales-letter` + creatives brief) — it builds the **structure, targeting, and flow**.

## When to activate

- Client wants to start paid traffic (first campaign)
- Existing campaigns underperforming (audit + rebuild)
- Launch campaign for a new offer (pair with `dario-offer`)
- Planning quarterly ads budget

## Workflow

### 1. Gather inputs
- **Offer** — what's being sold, price, margin
- **Target avatar** — demographics, psychographics, interests
- **Dream outcome** — what the customer wants
- **Current baseline** (if any): CAC, ROAS, conversion rate
- **Budget** — monthly or per campaign
- **Platforms** — where the avatar lives (FB/IG, Google, YouTube, TikTok, LinkedIn)
- **Conversion event** — what's the north star metric
- **Tracking stack** — sGTM? Meta CAPI? Enhanced Conversions? GA4?

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "molly pittman facebook ads campaign structure", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "ralph burns facebook ads scale", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "kasim aslam google ads performance max", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "tom breeze youtube ads creative", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "pedro sobral BPM method facebook ads", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "consent mode v2 meta capi tracking", collection: "dario", limit: 5)
```

### 3. Platform selection matrix

| Goal | Best Platform | Why |
|---|---|---|
| Low-intent discovery | Meta (FB/IG) | interest + LAL audiences |
| High-intent capture | Google Search | keyword intent |
| Brand + education | YouTube | long-form trust |
| B2B SaaS | LinkedIn + Google | buyer intent |
| Visual product | TikTok + IG Reels | short video |
| Local service | Google LSA + Maps | geo intent |

**Rule:** start with ONE platform. Master it before expanding. Avoid multi-platform dilettantism.

### 4. Campaign structure

#### Meta (Facebook / Instagram)
```
Account
├── Campaign: COLD — Prospecting (CBO ou ABO?)
│   ├── AdSet: Broad targeting (Advantage+)
│   │   └── 3-5 Ad creatives (different angles)
│   ├── AdSet: Interest stack (1-3 stacks)
│   │   └── 3-5 Ad creatives
│   └── AdSet: LAL 1% from purchasers
│       └── 3-5 Ad creatives
├── Campaign: WARM — Engaged (retargeting)
│   └── AdSet: 7d engagers + website visitors
│       └── 2-3 Ad creatives
└── Campaign: HOT — Cart abandoners / Non-converters
    └── AdSet: 14d website add-to-cart, no purchase
        └── 2-3 Ad creatives + urgency
```

Budget split: 70% cold, 20% warm, 10% hot (starting). Adjust per Pittman BPM method.

#### Google Ads
```
Account
├── Campaign: Branded Search (must exist, low budget, high ROAS)
├── Campaign: High-intent Search (commercial keywords)
│   ├── AdGroup: service-A keywords
│   ├── AdGroup: service-B keywords
│   └── AdGroup: competitor branded (careful)
├── Campaign: Performance Max (aggregate)
└── Campaign: YouTube Ads (for awareness/retargeting)
```

### 5. Creative framework (Pittman / Depesh 3-2-1)

For each offer, produce:
- **3 creative angles** (emotional × problem × mechanism)
- **2 creative formats** per angle (static, video, carousel, UGC)
- **1 offer** consistent across all

Creative patterns that work:
- **Problem-Solution** (30s video or static)
- **Testimonial-driven** (UGC-style)
- **Before/After** (visual result)
- **"Watch this first"** pattern (stop-scroll)
- **Founder-to-camera** (authenticity)
- **Proof stacking** (numbers, logos, results)

### 6. Funnel structure
```
Ad → Landing Page → Lead Magnet / Booking / Purchase → Email nurture → Retarget
```

Every step needs conversion tracking:
- Ad click → pageview
- Scroll depth (90%)
- Form start → form submit
- Purchase / lead event
- Post-conversion upsell / cross-sell

### 7. Tracking stack (must be compliant)
- **sGTM** ou client-side GTM
- **Consent Mode v2** — mandatório EU
- **Meta CAPI** (Conversions API) — bypass browser blockers
- **Google Enhanced Conversions**
- **GA4** como source of truth
- **Event deduplication** client/server

### 8. Budget allocation rule

Starting budget per campaign:
- **Cold / prospecting:** 5x to 10x the target CPA (to exit learning phase in 7 days)
- **Warm / retargeting:** 10-20% of cold
- **Hot:** 5-10% of cold

**Don't split budget across 15 adsets day 1** — Meta learning phase needs ~50 conversions/week/adset.

### 9. KPI targets

| KPI | Meta | Google Search | YouTube |
|---|---|---|---|
| CTR | 1-2% | 5-8% | 0.5-1.5% (view rate 20%+) |
| CPC | €0.30-€1.50 | €0.80-€3 (sector-dep) | €0.05-€0.20 per view |
| CVR (LP) | 2-5% | 3-6% | 1-3% |
| ROAS | 2-4x cold / 5-10x warm | 3-8x | 1.5-3x (brand+direct) |
| CPA | ≤40% margin | ≤30% margin | — |

Customize for sector. HNW B2B tolerates higher CPA; e-commerce under 30%.

### 10. Testing & iteration
- **Creative refresh:** every 7-14 days
- **Winning creative:** scale +20-50% per day max
- **Losing creative:** kill after 100-200 clicks no conv
- **Copy test:** headline, hook, CTA
- **Audience test:** cold, LAL, interest, broad
- **Placement test:** Reels only, feed only, all placements

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: ads-blueprint
platforms: [meta, google, youtube]
budget_monthly: €X
---

# Paid Ads Blueprint — <Client>

## Strategic Context
- Offer: ...
- Avatar: ...
- Dream outcome: ...
- Baseline CAC / ROAS: ...
- Budget: €X / mês
- North star event: ...

## Platform Choice + Rationale
Primary: <...>
Secondary: <...>
Why: ...

## Campaign Architecture
<diagram or tree>

## Creative Framework (3-2-1)
| Angle | Format | Lead copy | Visual |
|---|---|---|---|

## Landing Page Requirements
- ...

## Tracking Stack
- GTM / sGTM: ...
- Consent Mode v2: ...
- Meta CAPI: ...
- Enhanced Conversions: ...
- Events: ...

## Budget Allocation
| Campaign | Daily | Monthly | % |
|---|---|---|---|

## KPI Targets (30/60/90d)
| Metric | D30 | D60 | D90 |
|---|---|---|---|
| CPA | | | |
| ROAS | | | |
| CTR | | | |
| CVR | | | |

## Weekly Optimization Checklist
- [ ] Creative refresh cadence
- [ ] Audience review
- [ ] Killbox (lost creatives)
- [ ] Scale winners

## Risks & Mitigations
- ...

## Roadmap 90d
- Semana 1-2: ...
- Semana 3-4: ...
- Mês 2-3: ...
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Ads Blueprint.md`

## Red flags / anti-patterns
- No conversion tracking in place (fix this FIRST)
- Running ads to homepage instead of dedicated LP (Oli Gardner violation)
- 15 adsets on day 1 (budget fragmentation)
- No creative refresh cadence (fatigue)
- Scaling winners too aggressively (>50%/day)
- Using Meta without CAPI in 2026 EU traffic (loses 40% of events)
- Zero brand search campaign (competitors steal clicks)
- Performance Max without exclusion lists (cannibalizes brand search)
- Tracking conversions without consent (illegal PT)

## Interactions
- Depends on `dario-offer` (offer clarity)
- Pair with `dario-sales-letter` for LP copy
- Check `spec/server-side-analytics-consent-mode-v2` before launching
- Check `spec/pt-legal-compliance` for banner setup

## Red Flags
- Never launch ads before the landing page is live, tested, and tracking-verified — sending paid traffic to a broken or untracked page burns budget with zero data
- Never skip installing tracking pixels (Meta CAPI, GA4 events, Enhanced Conversions) before the first ad goes live — without conversion data the algorithm cannot optimize and you fly blind
- Always test new creative with a small budget (5-10% of total) for 48-72h before scaling — untested creative at full budget risks blowing the entire monthly spend on a losing angle
- Never ignore negative keywords on Google Search campaigns — broad match without negatives attracts irrelevant clicks that inflate CPC and destroy ROAS
- Always confirm Consent Mode v2 is active before launching any EU campaign — non-compliant tracking is illegal under GDPR and can result in fines plus ad account suspension
- Never scale a winning ad by more than 50% daily — aggressive scaling resets the learning phase and destabilizes CPAs
