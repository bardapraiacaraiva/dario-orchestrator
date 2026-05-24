---
name: client-qbr
description: "C.L.I.E.N.T. Account Management — QBR templates, success plans, executive business reviews, stakeholder mapping, and relationship scoring"
version: "1.0"
agent: CLIENT
tags: [QBR, account-management, success-plan, EBR, stakeholder-mapping, relationship]
---

# CLIENT Account Management & QBR Skill

## Triggers

Activate this skill when the user says or implies:
- "QBR", "quarterly business review", "business review"
- "success plan", "account plan", "strategic account plan"
- "executive business review", "EBR"
- "stakeholder mapping", "stakeholder map", "org chart"
- "relationship scoring", "account strategy"
- "account management", "key account", "strategic account"

## Workflow

### Step 1 — Stakeholder Mapping
1. **Identify Key Stakeholders**
   - Economic Buyer: Controls budget, signs contracts
   - Champion: Internal advocate, daily user, drives adoption
   - Technical Lead: Evaluates technical fit, manages integration
   - End Users: Day-to-day users of the product
   - Executive Sponsor: Senior leader who cares about outcomes
   - Detractor/Blocker: Anyone opposing or resistant
2. **Map Relationships**
   - Influence level (high/medium/low)
   - Engagement level (active/passive/disengaged)
   - Sentiment (positive/neutral/negative)
   - Reporting lines and decision-making dynamics
3. **Multi-Threading Score**
   - Single-threaded (1 contact): HIGH RISK
   - Dual-threaded (2-3 contacts): MODERATE RISK
   - Multi-threaded (4+ contacts across levels): LOW RISK

### Step 2 — Success Plan Creation
1. **Business Objectives**: Customer's top 3 goals for the next 12 months
2. **Success Metrics**: Measurable KPIs tied to each objective
3. **Current Baseline**: Where they are today on each metric
4. **Target State**: Where they want to be
5. **Action Plan**: Steps to get from baseline to target, with owners and dates
6. **Risk Register**: Obstacles that could prevent success
7. **Review Cadence**: When and how we check progress

### Step 3 — QBR Preparation (2 weeks before)
1. **Data Gathering**
   - Usage analytics (adoption, engagement, feature usage)
   - Support history (tickets, CSAT, resolution times)
   - Health score and trend
   - ROI/value metrics achieved
   - Product roadmap items relevant to this customer
2. **Narrative Construction**
   - Story arc: Where we started → What we achieved → Where we're going
   - Wins to celebrate (with data)
   - Challenges addressed or in progress
   - Strategic recommendations for next quarter
3. **Agenda Alignment**
   - Send draft agenda to champion for input 1 week before
   - Confirm attendees (aim for executive sponsor presence)
   - Prepare customer-specific slides (no generic decks)

### Step 4 — QBR Meeting Structure (60 minutes)
1. **(5 min) Opening**: Relationship check, agenda overview
2. **(10 min) Business Update**: Customer shares their priorities and changes
3. **(15 min) Value Delivered**: Usage data, outcomes achieved, ROI summary
4. **(10 min) Roadmap Preview**: Upcoming features relevant to their goals
5. **(10 min) Success Plan Review**: Progress on goals, adjust targets
6. **(5 min) Strategic Recommendations**: 1-2 suggestions for next quarter
7. **(5 min) Next Steps & Close**: Action items with owners and deadlines

### Step 5 — Post-QBR Actions
1. Send QBR summary within 24 hours (action items, decisions, next steps)
2. Update success plan with any new objectives or changes
3. Log action items in tracking system with owners and deadlines
4. Share internally: key insights, risks, expansion signals
5. Schedule next QBR date before leaving the meeting

### Step 6 — Executive Business Review (EBR)
- For strategic accounts, annual or bi-annual
- C-level to C-level meeting format
- Focus on strategic partnership, not operational metrics
- Include: industry trends, mutual growth opportunities, innovation roadmap
- Outcome: Joint strategic vision for the next 12-24 months

## Commands

```
/client-qbr [company_name]            — Generate full QBR deck outline and prep
/client-qbr agenda [company]          — Generate QBR agenda with talking points
/client-qbr success-plan [company]    — Create or update success plan
/client-qbr stakeholders [company]    — Generate stakeholder map
/client-qbr ebr [company]             — Executive business review prep
/client-qbr summary [company]         — Post-QBR summary template
```

## Output Template

```markdown
# Quarterly Business Review: [Company Name] — [Quarter/Year]

## Stakeholder Map
| Name | Role | Influence | Engagement | Sentiment |
|------|------|-----------|------------|-----------|
| [Name] | Economic Buyer | High | Active | Positive |
| [Name] | Champion | High | Active | Positive |
| [Name] | Technical Lead | Medium | Passive | Neutral |

**Multi-Threading Score**: [X contacts] — [LOW/MODERATE/HIGH] RISK

## Value Delivered This Quarter
| Metric | Baseline | Target | Actual | Status |
|--------|----------|--------|--------|--------|
| [KPI 1] | [X] | [Y] | [Z] | [On/Off track] |

## Success Plan Progress
| Objective | Progress | Next Milestone | Risk |
|-----------|----------|----------------|------|
| [Obj 1] | [X]% | [Milestone] | [L/M/H] |

## Strategic Recommendations
1. [Recommendation with rationale]
2. [Recommendation with rationale]

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| [Action] | [Name] | [Date] | [ ] |

## Next QBR: [Date]
```

## Red Flags

- QBR scheduled without executive sponsor invited or present
- Using a generic slide deck not customized to the customer
- QBR focused only on product features, not business outcomes
- No usage data or value metrics prepared before the meeting
- Success plan not updated for >2 quarters
- Single-threaded relationship with no plan to multi-thread
- Customer cancels or reschedules QBR repeatedly
- No action items documented after QBR
- QBR summary not sent within 48 hours
- Account plan exists on paper but CSM cannot articulate the strategy
- EBR held without C-level attendance from either side
- Stakeholder map has not been updated after org changes

## Integration Points

- Receives from: `client-health` (health score for QBR), `client-voc` (NPS/CSAT data), `client-expansion` (growth opportunities to discuss)
- Feeds into: `client-renewal` (renewal prep from QBR), `client-expansion` (expansion signals from QBR), `client-journey` (touchpoint quality)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - CLIENT - QBR [Company].md`

## Metrics to Track

- **QBR Completion Rate**: % of eligible accounts that had QBR this quarter
- **Executive Attendance**: % of QBRs with executive sponsor present
- **Action Item Completion**: % of QBR action items completed by next QBR
- **Success Plan Currency**: % of success plans updated within last 90 days
- **Multi-Threading Score**: Average contacts per account, trend over time
- **Post-QBR CSAT**: Customer rating of QBR value (1-5)


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **client-qbr** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in client-qbr:**

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
