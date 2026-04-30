---
name: dario-offer
description: Build an irresistible Grand Slam Offer using Hormozi's value equation, 4-part formula, pricing tiers, bonuses, guarantees and urgency. Triggers on "oferta", "grand slam offer", "construir oferta", "pricing", "value equation", "bundle".
license: MIT
---

# DARIO Skill — Grand Slam Offer Builder

Turns a raw product/service into an offer that's hard to say no to, using Alex Hormozi's `$100M Offers` framework. Used before writing sales copy (`dario-sales-letter`) and for pricing/relaunch decisions.

## When to activate

- User asks for help "constructing an offer"
- New service launch
- Pricing discussion
- Conversion is failing but the product is solid → the problem is the offer
- Before Facebook/Google Ads campaign (ads are only as good as the offer)

## Workflow

### 1. Gather inputs
- **Product / service** — what it is
- **Dream outcome** — what the customer wants in their own words
- **Target avatar** — who specifically
- **Current price + packaging** (if exists)
- **Competitor offers** (who else, at what price, with what)
- **Customer objections** (top 5 "but what if..." fears)
- **Proof points** (results, testimonials, case studies)

If any of these are missing, stop and ask.

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "hormozi grand slam offer value equation", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "hormozi pricing tiers value-based", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "hormozi guarantees conditional unconditional", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "hormozi bonus stack naming offer", collection: "dario", limit: 5)
```

### 3. Apply the Value Equation

```
          (Dream Outcome × Perceived Likelihood of Achievement)
Value  =  ────────────────────────────────────────────────────
          (Time Delay × Effort & Sacrifice)
```

Iterate each lever to **maximize value**:
- **Dream outcome:** is it vivid, specific, tangible? ("Lose 20 pounds" > "get healthier")
- **Likelihood of achievement:** add proof, guarantees, frameworks
- **Time delay:** how fast will they see results? Accelerate it.
- **Effort & sacrifice:** how much do they have to do? Reduce it. "Done-for-you" > "Done-with-you" > "DIY".

### 4. Apply the 5-step Grand Slam formula

#### Step 1: Identify the dream outcome (1 sentence)
"<Target>, get <dream outcome> in <timeframe> without <pain>."

#### Step 2: List every problem that stands in the way
Brainstorm 15-20 problems. These become the bonuses that eliminate each.

#### Step 3: Turn problems into solutions
Each problem → a specific deliverable that solves it.

#### Step 4: Stack the value
Create "Bonus stack":
- **Bonus 1:** Solves [problem 1]. Value: $X
- **Bonus 2:** Solves [problem 2]. Value: $Y
- ...
Total perceived value: $ZZZZZ

The offer price should be 10-20% of the perceived stacked value.

#### Step 5: Name it and frame it
- **Magnetic name:** benefit-driven, specific, memorable
  - Bad: "Consulting Package Premium"
  - Good: "The 90-Day Lisbon Listing Dominator"
- **Frame:** context that positions the offer as different/unique

### 5. Design the guarantee
Choose one (or stack multiple):
- **Unconditional** — 100% money back, no questions
- **Conditional** — "if you do X, we guarantee Y"
- **Anti-guarantee** — "we don't refund but we promise X" (works when trust is high)
- **Implied** — case studies + pay-for-results
- **Performance** — "we hit KPI or work free until we do"
- **Service** — "we redo the work"

### 6. Add urgency + scarcity (real, never fake)
- Cohort-based (next cohort starts X)
- Seat-limited (20 clients per quarter)
- Price-escalating (price goes up every N sales)
- Bonus-expiring (bonuses available until X date)

### 7. Stack pricing tiers (optional)
- **Good:** entry (DIY)
- **Better:** managed (done-with-you)
- **Best:** full-service (done-for-you) — highest margin, highest ticket
Price gap between tiers: 2.5-5x (anchor the Best)

## Output template

```markdown
---
project: <client or product>
date: <YYYY-MM-DD>
type: grand-slam-offer
hormozi_framework: yes
---

# Grand Slam Offer — <Offer Name>

## One-liner
> <Target>, <dream outcome> in <timeframe> without <pain>.

## Avatar
- Who: ...
- What they want: ...
- What they fear: ...

## Value Equation Analysis
| Lever | Current | After Offer |
|---|---|---|
| Dream Outcome | ... | ... |
| Likelihood | ... | ... |
| Time Delay | ... | ... |
| Effort | ... | ... |

## Core Offer
<What they get, in plain language>

## Bonus Stack
| # | Bonus | Solves Problem | Value |
|---|---|---|---|
| 1 | ... | ... | $X |
| 2 | ... | ... | $Y |
| N | ... | ... | $Z |
| **Total** | | | **$TTTT** |

## Guarantee
<Specific guarantee language>

## Urgency / Scarcity
<Real, not fake>

## Pricing Tiers
| Tier | Price | Delivery | Who it's for |
|---|---|---|---|
| Good | $X | DIY | ... |
| Better | $XX | DWY | ... |
| Best | $XXX | DFY | ... |

## Objection → Reframe
| Objection | Response |
|---|---|
| "Too expensive" | ... |
| "I don't have time" | ... |
| "Not sure it'll work for me" | ... |

## Next Steps
- [ ] Pair with `dario-sales-letter` for copy
- [ ] Pair with `dario-ads-blueprint` for traffic
- [ ] Test price on 10 calls before public launch
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Grand Slam Offer.md`

## Red flags to avoid
- Fake scarcity ("only 2 left!" when there are 200)
- Vague dream outcome ("better life")
- Bonuses that duplicate the core (not new problems solved)
- No guarantee — implies no confidence
- Price too low (implies low value)
- Too many tiers (>3) — paralysis

## Interactions
- Follow up with `dario-sales-letter` to write the long-form copy
- Follow up with `dario-ads-blueprint` to drive traffic
- Save via `dario-obsidian-save` to vault

## Red Flags
- Never build an offer without brand positioning completed first (`dario-brand`) — an offer disconnected from brand voice and values feels generic and erodes trust
- Never use the value equation with vague or generic terms ("better results", "more success") — each lever must be specific and measurable or the equation produces meaningless output
- Always include a guarantee in the final offer — an offer without risk reversal signals low confidence and leaves the biggest conversion objection unaddressed
- Never create fake scarcity or urgency — fabricated deadlines and phantom limits destroy credibility when discovered, and they always get discovered
- Always validate the offer with 5-10 real conversations before public launch — an untested offer at scale wastes ad budget and poisons the market's first impression
