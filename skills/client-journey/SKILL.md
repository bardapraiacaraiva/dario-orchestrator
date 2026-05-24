---
name: client-journey
description: "C.L.I.E.N.T. Customer Journey Mapping — touchpoints, moments of truth, pain points, delight moments, and journey visualization"
version: "1.0"
agent: CLIENT
tags: [journey-map, touchpoints, moments-of-truth, pain-points, customer-experience, CX]
---

# CLIENT Customer Journey Mapping Skill

## Triggers

Activate this skill when the user says or implies:
- "customer journey", "journey map", "journey mapping"
- "touchpoints", "moments of truth"
- "pain points", "friction points", "delight moments"
- "customer experience", "CX map", "experience design"
- "service blueprint", "customer lifecycle stages"
- "map the customer journey", "visualize the experience"

## Workflow

### Step 1 — Define Journey Scope
1. **Persona Selection**: Which customer segment or persona are we mapping?
2. **Journey Scope**: End-to-end lifecycle or specific phase (e.g., onboarding, support)?
3. **Current vs. Future**: Mapping as-is experience or designing to-be?
4. **Data Sources**: Analytics, surveys, interviews, support tickets, session recordings

### Step 2 — Identify Lifecycle Stages
Standard B2B/SaaS journey stages:
1. **Awareness**: Customer first learns about you (content, ads, referral, event)
2. **Consideration**: Evaluates solution (demo, trial, comparison, references)
3. **Purchase**: Buys (proposal, negotiation, contract, payment)
4. **Onboarding**: Gets started (kickoff, setup, training, first use)
5. **Adoption**: Regular usage (feature discovery, habit formation, integration)
6. **Value Realization**: Achieves outcomes (ROI, efficiency gains, goals met)
7. **Expansion**: Grows usage (upsell, cross-sell, new teams, new use cases)
8. **Advocacy**: Champions you (referrals, reviews, case studies, speaking)
9. **Renewal**: Continues relationship (renewal, renegotiation, recommitment)

### Step 3 — Map Touchpoints per Stage
For each stage, document:
- **Actions**: What the customer does at this stage
- **Touchpoints**: Where they interact (website, app, email, call, meeting, support)
- **Emotions**: How they feel (excited, confused, frustrated, delighted, anxious)
- **Expectations**: What they expect to happen
- **Pain Points**: Where friction or frustration occurs
- **Delight Moments**: Where experience exceeds expectations
- **Channels**: Which channels are used (digital, human, self-service, hybrid)
- **Internal Owners**: Which team owns this touchpoint

### Step 4 — Identify Moments of Truth
Critical moments that disproportionately affect the relationship:
- **First impression**: Initial website visit or first human interaction
- **Aha moment**: When customer first realizes the product's value
- **Support crisis**: First time something goes wrong and they need help
- **Renewal decision**: The moment they decide to stay or leave
- **Expansion trigger**: When they realize they need more
- **Advocacy spark**: Experience so good they want to tell others

### Step 5 — Gap Analysis & Prioritization
1. Map emotional curve across the journey (high points and low points)
2. Identify biggest gaps between expectation and reality
3. Score each gap by (customer impact x frequency x effort to fix)
4. Prioritize: Quick wins (high impact, low effort) first
5. Design interventions for each priority gap

### Step 6 — Journey Visualization
- Horizontal swim lanes: Stages across the top
- Vertical layers: Actions, touchpoints, emotions, pain/delight, owners
- Emotional curve: Visual line showing sentiment highs and lows
- Heat map overlay: Color-code by satisfaction or friction intensity

## Commands

```
/client-journey [persona]              — Full journey map for a persona
/client-journey stage [stage_name]     — Deep dive on a specific stage
/client-journey pain-points            — Consolidated pain point inventory
/client-journey moments-of-truth       — Critical moments analysis
/client-journey gap-analysis           — Expectation vs. reality gaps prioritized
/client-journey blueprint              — Service blueprint with backstage processes
```

## Output Template

```markdown
# Customer Journey Map: [Persona Name]

## Journey Overview
- **Persona**: [Name, Role, Segment]
- **Scope**: [End-to-end / Specific phase]
- **Data Sources**: [List]

## Journey Stages

### [Stage 1: Awareness]
- **Actions**: [What customer does]
- **Touchpoints**: [Where interaction happens]
- **Emotions**: [How they feel] — Intensity: [1-5]
- **Expectations**: [What they expect]
- **Pain Points**: [Friction identified]
- **Delight Opportunities**: [Where to exceed expectations]
- **Owner**: [Internal team]

[Repeat for each stage]

## Emotional Curve
```
Delight  |          *              *
         |        /   \          /   \     *
Neutral  |--*---/-------\------/-----\---/---
         |   \ /         \   /        \ /
Frustrate|    *            *            *
         |________________________________
          Aware  Consider  Buy  Onboard  Adopt  Value  Expand  Renew
```

## Moments of Truth
| Moment | Stage | Current Score | Target | Gap |
|--------|-------|---------------|--------|-----|
| [Moment] | [Stage] | [X/10] | [X/10] | [X] |

## Priority Interventions
| Gap | Impact | Effort | Priority | Proposed Fix |
|-----|--------|--------|----------|-------------|
| [Gap] | [H/M/L] | [H/M/L] | [1-N] | [Fix] |
```

## Red Flags

- Journey mapped without actual customer data (pure assumption)
- Missing stages in the map (e.g., no post-purchase stages mapped)
- No emotional dimension — only listing touchpoints without sentiment
- Pain points identified but no owner assigned for resolution
- Journey map created once and never updated (should refresh annually minimum)
- Only mapping the "happy path" without failure scenarios
- No backstage processes mapped (only customer-facing view)
- Moments of truth not identified or not prioritized
- Journey map not shared with product, marketing, and support teams
- Gap analysis done but no action plan or timeline for fixes
- Customer interviews not included as a data source

## Integration Points

- Receives from: `client-onboard` (onboarding touchpoints), `client-voc` (satisfaction data), `client-health` (engagement patterns)
- Feeds into: `client-education` (training at right moments), `client-community` (community touchpoints), `client-expansion` (expansion triggers in journey)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - CLIENT - Journey Map [Persona].md`

## Metrics to Track

- **Touchpoint Satisfaction**: CSAT per touchpoint, trend over time
- **Stage Conversion**: % of customers progressing from one stage to the next
- **Time in Stage**: Average duration per stage (identify bottlenecks)
- **Drop-off Points**: Stages with highest customer loss
- **Effort Score (CES)**: Per stage or per critical touchpoint
- **Intervention Impact**: Before/after scores for implemented fixes


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **client-journey** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in client-journey:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->
