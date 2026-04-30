---
name: client-onboard
description: "C.L.I.E.N.T. Customer Onboarding — first 90 days playbook, time-to-value acceleration, kickoff meetings, success milestones, and sales-to-CS handoff"
version: "1.0"
agent: CLIENT
tags: [onboarding, time-to-value, kickoff, milestones, handoff, customer-success]
---

# CLIENT Onboarding Skill

## Triggers

Activate this skill when the user says or implies:
- "onboard a new customer", "client onboarding", "onboarding playbook"
- "first 90 days", "time to value", "TTV"
- "kickoff meeting", "welcome sequence", "new client setup"
- "sales handoff", "handoff to CS", "transition from sales"
- "success milestones", "onboarding checklist"
- "implementation plan", "go-live plan"

## Workflow

### Phase 1 — Pre-Onboarding (Day -7 to Day 0)
1. **Sales-to-CS Handoff**
   - Collect handoff brief: deal context, buyer persona, pain points, success criteria, contract terms
   - Review CRM notes, proposal, signed contract, stakeholder map
   - Identify champion, economic buyer, technical lead, end users
   - Flag any promises made during sales that need validation
2. **Internal Preparation**
   - Assign CSM, onboarding specialist, and technical resources
   - Prepare welcome kit: credentials, documentation links, support channels
   - Configure environment/workspace/tenant for the customer
   - Schedule kickoff meeting within 48h of contract signature

### Phase 2 — Kickoff & Activation (Day 1–14)
3. **Kickoff Meeting Agenda**
   - Introductions and role mapping (who does what)
   - Restate goals and success criteria (align expectations)
   - Walk through onboarding timeline and milestones
   - Define communication cadence (weekly check-ins, Slack/Teams channel)
   - Assign mutual action items with owners and deadlines
4. **Technical Setup & Configuration**
   - Environment provisioning and access grants
   - Data migration or integration setup
   - Initial configuration aligned to customer use case
   - Smoke test / sanity check with customer present

### Phase 3 — Adoption & Habit Formation (Day 15–60)
5. **Guided Adoption**
   - Deliver training sessions (live or async) per user role
   - Share quick-start guides and video walkthroughs
   - Set usage targets: daily active users, key features adopted
   - Monitor adoption metrics weekly; intervene on low engagement
6. **First Value Milestone**
   - Define the "aha moment" specific to this customer's use case
   - Track progress toward first measurable outcome
   - Celebrate and document first win (internal + customer facing)

### Phase 4 — Maturity & Handoff to BAU (Day 61–90)
7. **Success Plan Finalization**
   - Review all milestones achieved vs. planned
   - Document remaining gaps and remediation plan
   - Establish ongoing cadence (monthly check-in, QBR schedule)
   - Transition from onboarding specialist to long-term CSM
8. **Graduation Criteria**
   - Core features actively used by target user group
   - At least one measurable business outcome achieved
   - Customer confirms satisfaction (CSAT >= 4/5)
   - Support ticket volume stabilized

## Commands

```
/client-onboard [company_name]        — Generate full 90-day onboarding plan
/client-onboard kickoff [company]     — Generate kickoff meeting agenda + deck outline
/client-onboard handoff [company]     — Generate sales-to-CS handoff template
/client-onboard checklist [company]   — Generate milestone checklist with dates
/client-onboard status [company]      — Review onboarding progress and flag risks
```

## Output Template

```markdown
# Onboarding Plan: [Company Name]

## Handoff Summary
- **Deal Size**: [ARR/MRR]
- **Champion**: [Name, Role]
- **Success Criteria**: [Primary metric]
- **Contract Start**: [Date]

## Milestone Timeline
| Milestone | Target Date | Owner | Status |
|-----------|-------------|-------|--------|
| Kickoff meeting | Day 1 | CSM | [ ] |
| Technical setup complete | Day 7 | Tech Lead | [ ] |
| Training delivered | Day 14 | CS Specialist | [ ] |
| First value milestone | Day 30 | CSM + Champion | [ ] |
| Adoption target hit | Day 60 | CSM | [ ] |
| Graduation review | Day 90 | CSM | [ ] |

## Risk Register
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [H/M/L] | [Action] |

## Communication Plan
- **Weekly**: 30min check-in with champion
- **Bi-weekly**: Stakeholder update email
- **Monthly**: Executive summary to sponsor
- **Day 90**: Formal onboarding review meeting
```

## Red Flags

- No kickoff meeting scheduled within 5 business days of contract start
- Champion goes silent or unresponsive for >7 days during onboarding
- Technical setup delayed beyond Day 14 without escalation
- Zero logins from end users by Day 21
- Sales made promises not captured in the handoff brief
- Customer pushes back on training sessions or engagement
- No measurable outcome achieved by Day 60
- Stakeholder changes (champion leaves, sponsor changes) without re-alignment
- Customer asks for features not in scope during onboarding (scope creep signal)
- Support ticket volume spikes instead of stabilizing in Phase 4

## Integration Points

- Feeds into: `client-health` (initial health baseline), `client-journey` (touchpoint mapping)
- Receives from: Sales pipeline / CRM, `client-education` (training materials)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - CLIENT - Onboarding [Company].md`

## Metrics to Track

- **Time to First Value (TTFV)**: Days from contract to first measurable outcome
- **Onboarding Completion Rate**: % of milestones completed on time
- **Adoption Rate at Day 30/60/90**: % of target users actively engaged
- **CSAT at Graduation**: Customer satisfaction score at Day 90
- **Handoff Quality Score**: CSM rating of handoff completeness (1-5)
