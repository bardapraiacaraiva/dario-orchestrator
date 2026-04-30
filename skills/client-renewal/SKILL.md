---
name: client-renewal
description: "C.L.I.E.N.T. Renewal Management — renewal pipeline, pricing negotiation, contract terms, auto-renewal mechanics, and early warning system"
version: "1.0"
agent: CLIENT
tags: [renewal, retention, contract, pricing, negotiation, churn-prevention]
---

# CLIENT Renewal Management Skill

## Triggers

Activate this skill when the user says or implies:
- "renewal", "contract renewal", "renew the account"
- "retention", "keep the customer", "prevent churn"
- "pricing negotiation", "discount request", "contract terms"
- "auto-renewal", "renewal pipeline", "upcoming renewals"
- "early warning", "renewal risk", "renewal forecast"
- "contract expiration", "renewal playbook"

## Workflow

### Step 1 — Renewal Pipeline Management (T-180 to T-0)
1. **T-180 (6 months out)**: Flag upcoming renewals, assign renewal owner
2. **T-120 (4 months out)**: Health check — pull health score, usage data, open issues
3. **T-90 (3 months out)**: Renewal strategy call — internal alignment on approach
4. **T-60 (2 months out)**: Customer conversation — renewal intent, satisfaction, changes
5. **T-30 (1 month out)**: Proposal delivered, negotiation if needed
6. **T-14 (2 weeks out)**: Final terms agreed, contract sent for signature
7. **T-0 (Renewal date)**: Contract executed or escalation triggered

### Step 2 — Renewal Risk Assessment
- Cross-reference with `client-health` score
- Review support ticket history for unresolved issues
- Check NPS/CSAT trend (improving vs. declining)
- Assess competitive threats (mentions of alternatives)
- Evaluate stakeholder changes since last renewal
- Review product usage vs. contracted value (are they getting ROI?)

### Step 3 — Pricing & Negotiation Framework
1. **Anchor on Value**: Lead with documented outcomes and ROI before discussing price
2. **Standard Renewal**: Same terms, possible annual uplift (CPI or contractual escalator)
3. **Expansion Renewal**: Bundle expansion with renewal for better terms
4. **Discount Governance**: Define discount authority levels (CSM: 0-5%, Manager: 5-15%, VP: 15%+)
5. **Multi-Year Incentive**: Offer discount for 2-3 year commitment
6. **Concession Trading**: If giving discount, get something back (case study, referral, longer term)

### Step 4 — Contract Terms Checklist
- Renewal term length (annual, multi-year, month-to-month)
- Auto-renewal clause with opt-out window (typically 30-60 days)
- Price escalation clause (fixed %, CPI-linked, or none)
- SLA commitments and penalties
- Termination for convenience clause
- Data portability and exit provisions
- Payment terms (net-30, quarterly, annual upfront)

### Step 5 — Auto-Renewal Management
- Track auto-renewal dates and opt-out windows
- Send proactive notification to customer 90 days before auto-renewal
- Internal alert if customer has not acknowledged auto-renewal by T-60
- Ensure billing system aligned with renewal terms
- Document any verbal agreements about future renewals

### Step 6 — Early Warning System
- Automated alerts when: health drops below 50 within renewal window
- Alert when: customer requests data export or API documentation for migration
- Alert when: champion goes silent during renewal period
- Alert when: procurement/legal contact replaces business contact in renewal conversation
- Alert when: customer asks about contract termination clause

## Commands

```
/client-renewal pipeline              — View all upcoming renewals with risk tiers
/client-renewal [company_name]        — Generate renewal strategy for specific account
/client-renewal negotiate [company]   — Pricing negotiation prep with talk tracks
/client-renewal terms [company]       — Contract terms checklist and recommendations
/client-renewal forecast              — Renewal revenue forecast with risk-adjusted view
/client-renewal alerts                — Active early warning signals
```

## Output Template

```markdown
# Renewal Strategy: [Company Name]

## Renewal Overview
- **Current ARR**: $[X]
- **Renewal Date**: [Date]
- **Days to Renewal**: [X]
- **Current Term**: [Annual/Multi-year]
- **Auto-Renewal**: [Yes/No — opt-out by Date]

## Risk Assessment
- Health Score: [XX]/100 — [GREEN/YELLOW/RED]
- NPS: [X] (trend: [up/down/stable])
- Open Support Issues: [X] ([X] critical)
- Competitive Threat: [Low/Medium/High]
- Stakeholder Stability: [Stable/Changed]

## Recommended Strategy
- **Approach**: [Straightforward / Expansion bundle / Save play / Multi-year lock]
- **Target Outcome**: [Flat renewal / Expansion / Downsell to save]
- **Pricing**: [Standard uplift / Custom / Discount with concession]
- **Talk Track**: [Key messages for renewal conversation]

## Timeline
| Date | Action | Owner | Status |
|------|--------|-------|--------|
| [T-90] | Internal strategy alignment | CSM | [ ] |
| [T-60] | Customer renewal conversation | CSM | [ ] |
| [T-30] | Proposal delivered | CSM + Sales | [ ] |
| [T-14] | Contract sent | Legal/Ops | [ ] |
| [T-0] | Renewal executed | CSM | [ ] |

## Contingency Plan
- If customer pushes back: [Action]
- If champion unresponsive: [Action]
- If competitor threat: [Action]
```

## Red Flags

- Renewal less than 90 days away with no strategy defined
- No customer conversation about renewal by T-60
- Customer proactively asks about termination or cancellation clauses
- Health score is Red and no save plan activated
- Champion departed and no new champion identified before renewal
- Customer requests full data export during renewal window
- Procurement/legal takes over conversation from business stakeholder
- Customer benchmarks your pricing against competitors
- Auto-renewal approaching with unresolved billing disputes
- Discount exceeds authority level without proper approval chain
- Renewal proposal sent without value summary / business review

## Integration Points

- Receives from: `client-health` (risk tier), `client-expansion` (expansion bundling), `client-voc` (NPS/CSAT)
- Feeds into: `client-recovery` (if renewal lost), `client-qbr` (renewal prep in QBR)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - CLIENT - Renewal [Company].md`

## Metrics to Track

- **Gross Revenue Retention (GRR)**: Target >90%
- **Renewal Rate**: % of eligible renewals closed (by count and by value)
- **On-Time Renewal Rate**: % of renewals closed by T-0 (not late)
- **Average Renewal Cycle Time**: Days from first conversation to close
- **Discount Rate**: Average discount given on renewals
- **Multi-Year Conversion**: % of renewals converted to multi-year
