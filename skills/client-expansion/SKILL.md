---
name: client-expansion
description: "C.L.I.E.N.T. Expansion & Upsell — cross-sell triggers, account growth plans, expansion revenue playbook, and land-and-expand strategy"
version: "1.0"
agent: CLIENT
tags: [upsell, cross-sell, expansion, NRR, land-and-expand, account-growth]
---

# CLIENT Expansion Skill

## Triggers

Activate this skill when the user says or implies:
- "upsell", "cross-sell", "expansion revenue"
- "account growth", "land and expand", "grow account"
- "NRR", "net revenue retention", "expansion MRR"
- "upgrade plan", "add seats", "add modules"
- "whitespace analysis", "wallet share"
- "account growth plan", "expansion playbook"

## Workflow

### Step 1 — Expansion Readiness Assessment
1. **Health Gate**: Only pursue expansion for Green-tier accounts (score >= 70)
2. **Value Realization Check**: Customer has achieved at least one documented success outcome
3. **Relationship Strength**: Multi-threaded (3+ stakeholders engaged), champion active
4. **Usage Signals**: High adoption, power users present, feature ceiling approaching
5. **Timing**: Not within 60 days of a support escalation or unresolved complaint

### Step 2 — Whitespace Analysis
1. **Current Footprint**: Map what the customer uses today (plan, seats, modules, integrations)
2. **Total Addressable Wallet**: All products/services they could buy from you
3. **Gap Matrix**: Overlay current vs. potential — identify whitespace
4. **Priority Ranking**: Score each gap by (revenue potential x likelihood of adoption x strategic value)
5. **Competitive Overlap**: Where competitors fill gaps you could own

### Step 3 — Expansion Triggers (Signal Detection)
- **Usage ceiling**: User/seat count approaching plan limit
- **Feature requests**: Asking for capabilities in higher tiers
- **New use case**: Different department or team expresses interest
- **Business event**: Funding round, acquisition, expansion to new market
- **Champion promotion**: Champion moves to larger scope / budget authority
- **Success milestone**: Major outcome achieved, customer is in "delight" zone
- **Contract anniversary**: Natural moment for plan review
- **Competitor displacement**: Opportunity to replace a competitor tool

### Step 4 — Land-and-Expand Playbook
1. **Phase 1 — Land**: Win initial deal with focused use case and limited scope
2. **Phase 2 — Prove**: Deliver undeniable value in the initial use case
3. **Phase 3 — Expand Horizontally**: Spread to adjacent teams/departments
4. **Phase 4 — Expand Vertically**: Upgrade to higher tier / premium features
5. **Phase 5 — Entrench**: Become mission-critical, integrate deeply, executive sponsorship

### Step 5 — Expansion Conversation Framework
1. **Discover**: "I noticed your team has been [signal]. How is that going?"
2. **Quantify**: "Based on your current usage, [projected value of expansion]"
3. **Propose**: "Here's how [product/feature] could help with [their goal]"
4. **Prove**: Pilot, POC, or trial of expanded scope
5. **Close**: Commercial proposal with clear ROI case

## Commands

```
/client-expansion [company_name]       — Generate expansion opportunity analysis
/client-expansion whitespace [company] — Whitespace analysis with gap matrix
/client-expansion triggers             — Active expansion signals across portfolio
/client-expansion playbook [company]   — Land-and-expand plan for specific account
/client-expansion forecast             — Expansion revenue pipeline forecast
```

## Output Template

```markdown
# Expansion Opportunity: [Company Name]

## Readiness Assessment
- Health Score: [XX] — [GREEN] — PASS/FAIL
- Value Realized: [Yes/No — describe outcome]
- Relationship Depth: [X stakeholders, champion: Name]
- Usage Trend: [Growing/Stable/Declining]

## Whitespace Analysis
| Product/Feature | Current | Available | Revenue Gap | Priority |
|-----------------|---------|-----------|-------------|----------|
| [Module A] | In use | - | - | - |
| [Module B] | Not used | Available | $[X]/yr | HIGH |
| [Seats] | [X]/[limit] | Unlimited | $[X]/yr | MEDIUM |

## Active Expansion Triggers
1. [Trigger] — Confidence: [H/M/L] — Timing: [Now/Q+1/Q+2]
2. [Trigger] — Confidence: [H/M/L] — Timing: [Now/Q+1/Q+2]

## Recommended Play
- **Type**: [Upsell / Cross-sell / Seat expansion / New department]
- **Approach**: [Description]
- **Estimated ARR impact**: $[X]
- **Next Step**: [Action] by [Date]

## Land-and-Expand Status
- Current Phase: [1-5]
- Next Phase Gate: [What needs to happen]
```

## Red Flags

- Pursuing expansion on a Yellow or Red health account
- Expansion conversation without documented value realization
- Single-threaded relationship (only one contact) when proposing expansion
- Expansion proposed within 60 days of a major support escalation
- Pricing discussion before value discussion
- Customer explicitly stated budget freeze and team still pushes
- Expansion revenue forecasted without pipeline stage validation
- No executive sponsor aware of expansion conversation
- Cross-sell to a department that has no current engagement or awareness
- Expansion closes but no onboarding plan for the new scope

## Integration Points

- Receives from: `client-health` (green accounts), `client-qbr` (growth goals from QBRs), `client-voc` (positive sentiment)
- Feeds into: `client-renewal` (expansion before renewal), `client-onboard` (new scope onboarding)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - CLIENT - Expansion [Company].md`

## Metrics to Track

- **Net Revenue Retention (NRR)**: Target >110%
- **Expansion Revenue as % of Total New Revenue**: Target >30%
- **Average Expansion Deal Size**: Trend over time
- **Time from Signal to Close**: Average days from trigger detection to expansion close
- **Expansion Win Rate**: % of qualified expansion opportunities closed
- **Land-to-Expand Conversion Rate**: % of new logos that expand within 12 months


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **client-expansion** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in client-expansion:**

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
