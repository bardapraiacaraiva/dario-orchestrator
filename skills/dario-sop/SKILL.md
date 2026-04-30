---
name: dario-sop
description: SOP (Standard Operating Procedure) generator — creates step-by-step documented procedures for any repeatable process. Uses Operations Squad (Carpenter, Gawande, Gerber). Triggers on "sop", "procedimento", "documentar processo", "checklist operacional", "standard operating procedure", "como fazer".
license: MIT
---

# DARIO Skill — SOP Generator

## Workflow
1. RAG: `search_kb("sop standard operating procedure checklist process", collection: "dario")`
2. Identify the process to document
3. Interview/observe: what steps, what order, what tools, what decisions
4. Write SOP with: objective, scope, steps, decision points, exceptions, QA check
5. Add Gawande checklist (5-9 items) for quality gate
6. Save to Obsidian + optionally ingest in RAG

## SOP template
```
## SOP: [Process Name]
**Version:** 1.0 | **Owner:** [Name] | **Last updated:** [Date]

### Objective
[What this process achieves]

### Trigger
[When to start this process]

### Steps
1. [Action] → [Expected result]
2. [Action] → [Expected result]
...

### Decision points
- If [condition]: do [A]
- If [condition]: do [B]

### Quality checklist
- [ ] [Check 1]
- [ ] [Check 2]
...

### Exceptions
- [Edge case] → [How to handle]

### Tools needed
- [Tool 1]
- [Tool 2]
```

## Common Agency SOPs (ready to generate)

| SOP | Trigger | Typical Steps |
|-----|---------|--------------|
| New client onboarding | Contract signed | Kickoff call → brief → access gathering → baseline audit → timeline → Slack channel |
| Website launch | Site approved | Pre-launch checklist → DNS → SSL → redirects → analytics → indexing → announce |
| Content publication | Article approved | SEO check → images → schema → preview → publish → social → email → GSC |
| Monthly SEO report | 1st of month | GSC data → analytics → rankings → actions → client email |
| Invoice + follow-up | Work delivered | Generate invoice → send → 7-day follow-up → 14-day reminder → escalate |
| Client offboarding | Contract ends | Final delivery → access handover → archive project → feedback request |
| Bug/issue response | Client reports bug | Triage (P1-P3) → acknowledge (<2h) → investigate → fix → verify → close |
| Backup & recovery | Weekly / incident | Verify backups → test restore → document → alert if failed |

## Gawande Checklist Rules (from The Checklist Manifesto)

1. **5-9 items max** — more than 9, people skip them
2. **DO-CONFIRM format** — do the work from memory, THEN run checklist to verify
3. **READ-DO format** — read each item, do it, check it off (for unfamiliar tasks)
4. **Single-page** — if it doesn't fit on one page, it's too long
5. **Test in real conditions** — pilot with the team before finalizing
6. **Version + owner** — every checklist has a responsible person and a date

## Example: Client Onboarding SOP (expanded)

```markdown
## SOP: New Client Onboarding
**Version:** 2.0 | **Owner:** Account Manager | **Last updated:** 2026-04-27

### Objective
Ensure every new client is properly set up within 48h of contract signing with zero missed steps.

### Trigger
Contract signed + payment received (or first invoice sent)

### Steps
1. Create client folder in Obsidian → `01 - Projetos/<Client Name>/`
2. Run `/dario-client-onboard` → auto-creates memory, RAG context, audit baseline
3. Schedule kickoff call (within 3 business days)
4. Send pre-kickoff brief questionnaire (use dario-briefing template)
5. Gather access: hosting, CMS, analytics, GSC, GBP, social accounts
6. Run baseline diagnostic → `/dario-diagnose`
7. If WordPress: run `/dario-wp-audit` + `/dario-woo-audit` (if ecommerce)
8. Create project in orchestrator taskboard → define first sprint tasks
9. Setup communication channel (Slack channel or WhatsApp group)
10. Send welcome email with: timeline, team contacts, how to request support

### Decision points
- If client has WordPress → add wp-audit + woo-audit to sprint 1
- If client is new brand → add dario-brand before any marketing work
- If client has existing SEO → run seo-audit before seo-plan
- If budget < 2000€/month → limit to 1 parallel track; if > 5000€ → 3 parallel

### Quality checklist (DO-CONFIRM)
- [ ] Client folder created in Obsidian
- [ ] Agent memory project file exists
- [ ] All access credentials received and stored securely
- [ ] Baseline diagnostic completed and saved
- [ ] Kickoff call scheduled within 3 business days
- [ ] First sprint tasks created in taskboard
- [ ] Welcome email sent with timeline

### Exceptions
- Client unresponsive after contract → 3-day follow-up → 7-day escalate to owner
- Missing access credentials → document what's missing, proceed with available, flag blocked tasks
- Contract scope unclear → pause onboarding, schedule scope clarification call

### Tools needed
- Claude Code (orchestrator, skills)
- Obsidian vault (D.A.R.I.O)
- Client communication channel
- Access management (1Password or similar)
```

## SOP Complexity Guide

| Complexity | Steps | Format | Review Cycle |
|------------|-------|--------|-------------|
| Simple | 3-5 | Single checklist | 6 months |
| Standard | 6-10 | Template above | 90 days |
| Complex | 11-15 | Split into 2-3 sub-SOPs | 60 days |
| Critical | Any | Add approval gate + training | 30 days |

## Integration

- Pairs with `dario-hr` for team onboarding SOPs
- Pairs with `dario-support` for client-facing SOPs
- Pairs with `dario-client-onboard` — the onboarding SOP is the human wrapper around the automated skill
- Generated SOPs can be ingested into RAG for future reference
- Save complex SOPs as Obsidian notes for team access

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Process> - SOP.md`

## Red Flags

- Never create SOPs for processes that change weekly — those need guidelines, not procedures
- Never exceed 15 steps without splitting into sub-SOPs
- Never skip the "Exceptions" section — edge cases cause the most errors
- Always include "who does what" — a checklist without ownership is decoration
- Review and update SOPs every 90 days or after any incident
