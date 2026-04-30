---
name: client-recovery
description: "C.L.I.E.N.T. Churn Recovery — win-back campaigns, exit interviews, save playbooks, re-engagement sequences, and root cause analysis"
version: "1.0"
agent: CLIENT
tags: [churn, recovery, win-back, exit-interview, save-play, re-engagement, root-cause]
---

# CLIENT Churn Recovery Skill

## Triggers

Activate this skill when the user says or implies:
- "churn", "churned customer", "lost customer"
- "win back", "win-back campaign", "re-engage"
- "save play", "save the account", "prevent churn"
- "exit interview", "cancellation reason", "why did they leave"
- "re-engagement", "reactivation", "bring back"
- "root cause analysis", "churn reasons", "why customers leave"

## Workflow

### Step 1 — Save Play (Pre-Churn Intervention)
**Trigger**: Customer signals intent to cancel or health score hits Red

1. **Immediate Response (within 24 hours)**
   - Acknowledge the situation without being defensive
   - Schedule a call with the right person (CSM + manager if needed)
   - Prepare account history: timeline, issues, value delivered, gaps
2. **Discovery Call**
   - Listen first: "Help me understand what's driving this decision"
   - Identify root cause: Product gap? Service failure? Budget? Competition? Strategic shift?
   - Assess if the issue is solvable or terminal
   - Quantify the switching cost (their effort to migrate)
3. **Save Offer Tiers**
   - **Tier 1 — Fix It**: Resolve the specific issue (bug fix, feature priority, training)
   - **Tier 2 — Restructure**: Change plan, reduce scope, adjust pricing, add services
   - **Tier 3 — Executive Escalation**: VP/C-level to C-level conversation, strategic commitment
   - **Tier 4 — Concession**: Temporary discount, free months, extended trial of new features
   - **Tier 5 — Graceful Exit**: If unsaveable, make the exit smooth (protect relationship for future)
4. **30-Day Save Plan**
   - Define specific milestones to address the root cause
   - Weekly check-ins during save period
   - Executive sponsor involvement
   - Clear success criteria: customer confirms intent to stay

### Step 2 — Exit Interview (Post-Churn)
1. **Timing**: Within 2 weeks of cancellation
2. **Format**: 20-minute call (preferred) or structured survey
3. **Questions**
   - What was the primary reason for leaving?
   - When did you first start considering alternatives?
   - Was there a specific event that triggered the decision?
   - What could we have done differently?
   - Would you consider returning in the future? Under what conditions?
   - Where are you moving to? (competitor intelligence)
4. **Documentation**: Structured form with categorized reasons, verbatim quotes, actionable insights

### Step 3 — Root Cause Analysis
1. **Categorize Churn Reasons**
   - Product (missing features, bugs, performance, UX)
   - Service (support quality, responsiveness, CSM relationship)
   - Value (not seeing ROI, not using the product enough)
   - Price (too expensive, budget cuts, competitor pricing)
   - Strategic (M&A, pivot, went in-house, business closure)
   - Competition (switched to competitor, better fit)
2. **Pattern Analysis**
   - Churn by segment, plan, tenure, industry, ARR band
   - Cohort analysis: which signup cohorts churn most?
   - Seasonal patterns in churn timing
   - Correlation with health score trajectory
3. **Systemic Fix Recommendations**
   - For each top churn reason, propose a systemic fix (not just save plays)
   - Assign ownership to product, CS, support, or sales teams
   - Track fix implementation and impact on churn rate

### Step 4 — Win-Back Campaign
**Timing**: 3-6 months after churn (let the dust settle)

1. **Segmentation**: Only target customers who left for solvable reasons
2. **Trigger Events**
   - New feature launches that address their stated reason for leaving
   - Competitor issues (outages, price hikes, acquisitions)
   - Contact changes (new decision-maker who may reconsider)
   - Budget cycle reset (new fiscal year)
3. **Win-Back Sequence**
   - **Email 1 (Month 3)**: "We listened" — share improvements made since they left
   - **Email 2 (Month 4)**: Social proof — case study from similar company
   - **Email 3 (Month 5)**: Specific offer — trial, discount, or pilot of new capability
   - **Email 4 (Month 6)**: Personal outreach from executive or former CSM
4. **Win-Back Offer**
   - Free trial period (30-60 days) to re-evaluate
   - Migration assistance (help them come back)
   - Locked-in pricing for returning customers
   - Dedicated onboarding to ensure better second experience

### Step 5 — Re-Engagement Sequences (Dormant Accounts)
For customers still under contract but disengaged:
1. **Week 1**: "We noticed you haven't logged in" — helpful tips email
2. **Week 2**: CSM personal reach-out — "How can I help?"
3. **Week 3**: Share relevant use case or success story
4. **Week 4**: Offer 1:1 training session or product walkthrough
5. **Week 6**: Executive outreach if still disengaged
6. **Week 8**: Formal at-risk intervention (save play activation)

## Commands

```
/client-recovery save [company]        — Generate save play for at-risk account
/client-recovery exit-interview         — Exit interview template and guide
/client-recovery root-cause [period]   — Root cause analysis of churn for a period
/client-recovery winback [company]     — Win-back campaign for churned customer
/client-recovery re-engage [company]   — Re-engagement sequence for dormant account
/client-recovery dashboard             — Churn recovery metrics dashboard
```

## Output Template

```markdown
# Churn Recovery: [Company Name]

## Situation Assessment
- **Status**: [At-Risk / Churned / Dormant / Win-Back Target]
- **ARR at Risk/Lost**: $[X]
- **Churn Date / Risk Date**: [Date]
- **Root Cause**: [Category — specific reason]
- **Solvability**: [Solvable / Partially Solvable / Terminal]

## Save Play (if at-risk)
- **Tier**: [1-5]
- **Proposed Action**: [Specific intervention]
- **Owner**: [CSM / Manager / Executive]
- **Timeline**: [30-day plan with milestones]

## Exit Interview Summary (if churned)
- **Primary Reason**: [Reason]
- **Trigger Event**: [What finally caused the decision]
- **Competitor**: [Where they went, if known]
- **Win-Back Potential**: [High / Medium / Low]
- **Conditions for Return**: [What they said]

## Root Cause Classification
| Reason | Count | % of Total | Trend | Systemic Fix |
|--------|-------|------------|-------|-------------|
| [Reason] | [X] | [X]% | [up/down] | [Fix] |

## Win-Back Plan (if applicable)
| Step | Timing | Action | Channel | Owner |
|------|--------|--------|---------|-------|
| 1 | Month 3 | [Action] | [Email/Call] | [Name] |
```

## Red Flags

- Save play attempted without understanding root cause (throwing discounts at the problem)
- No exit interview conducted for churned accounts with ARR >$5K
- Churn reasons not categorized or tracked systematically
- Same churn reasons repeat quarter after quarter with no systemic fixes
- Win-back attempted for customers who left due to terminal reasons (business closure, M&A)
- Win-back campaign sent too soon (<3 months) — feels desperate
- Save play relies solely on discounts without addressing the underlying issue
- No executive involvement in save plays for strategic accounts
- Dormant account re-engagement starts with a sales pitch instead of value
- Churn data not shared with product team for roadmap input
- Customer leaves and no one notices for weeks (no monitoring)
- Save play success not tracked or celebrated (team learns nothing)

## Integration Points

- Receives from: `client-health` (Red alerts trigger save plays), `client-renewal` (failed renewals), `client-voc` (detractor alerts)
- Feeds into: `client-onboard` (improved onboarding from churn lessons), `client-health` (churn signals refine model), `client-journey` (journey pain points from exit data)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - CLIENT - Recovery [Company].md`

## Metrics to Track

- **Save Rate**: % of at-risk accounts saved (stayed >6 months after save play)
- **Win-Back Rate**: % of churned accounts that returned within 12 months
- **Exit Interview Completion Rate**: % of churned accounts with completed exit interview
- **Time to Intervene**: Average days from churn signal to first save action
- **Churn Root Cause Distribution**: Top reasons by category, trend over time
- **Revenue Saved**: ARR preserved through successful save plays
