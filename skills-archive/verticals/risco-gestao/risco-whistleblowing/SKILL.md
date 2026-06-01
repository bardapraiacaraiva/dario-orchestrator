---
name: risco-whistleblowing
description: "Whistleblowing — DL 93/2021 compliance, internal reporting channel, investigation procedure, retaliation protection"
version: "1.0"
---

# RISCO-WHISTLEBLOWING: Whistleblowing Channel Skill

## When to Activate

**Trigger words (PT):** denuncias, canal de denuncias, whistleblowing, dl 93/2021, protecao do denunciante, canal interno, retaliacao, investigacao interna, anonimato, lei dos denunciantes
**Trigger words (EN):** whistleblowing, reporting channel, whistleblower protection, internal channel, retaliation, anonymous reporting, investigation, eu whistleblower directive, reporting mechanism

## Step-by-Step Workflow

### Phase 1: Legal Requirements (DL 93/2021)
1. Determine if mandatory: entities with 50+ workers, public sector, financial sector, aviation, maritime, certain regulated sectors
2. Deadline compliance: 250+ workers since June 2022; 50-249 since Dec 2023
3. Designate responsible person/department (independent, no COI)
4. Ensure channel handles reports on: corruption, fraud, public procurement irregularities, consumer protection, data protection, financial services, environmental, public health, nuclear safety, food safety, product safety, transport

### Phase 2: Channel Design
1. Select channel type: digital platform, email, phone, in-person, postal
2. Ensure accessibility: available 24/7, in Portuguese, user-friendly
3. Enable anonymous reporting (not mandatory but recommended)
4. Secure data protection (encrypted, restricted access)
5. Publish channel information on website, intranet, contracts
6. Allow reports from: employees, ex-employees, contractors, suppliers, shareholders, trainees, volunteers

### Phase 3: Report Handling
1. Acknowledge receipt within 7 days
2. Assess admissibility (within scope, good faith, sufficient detail)
3. Assign investigator (independent, qualified, no COI)
4. Preliminary assessment within 15 days
5. Provide feedback to reporter within 3 months maximum
6. If external reporting needed: direct to MENAC or sector authority

### Phase 4: Investigation
1. Plan investigation scope and methodology
2. Collect evidence (documents, interviews, system logs)
3. Interview witnesses with confidentiality safeguards
4. Maintain chain of custody for evidence
5. Draft investigation report (facts, findings, recommendations)
6. Present to decision-maker for remedial action

### Phase 5: Retaliation Protection
1. Prohibit all forms of retaliation (Art. 21 DL 93/2021): dismissal, demotion, harassment, discrimination, blacklisting
2. Shift burden of proof to employer if adverse action follows report
3. Monitor reporter's situation after filing
4. Interim protection measures if needed
5. Penalties for retaliation: administrative fines + compensation

### Phase 6: Record Keeping & Reporting
1. Maintain report register (encrypted, access-controlled)
2. Retain records for 5 years after case closure
3. Annual statistics: reports received, investigated, substantiated, time to resolution
4. Report to Board/Audit Committee on channel effectiveness
5. Destroy personal data when no longer needed (RGPD alignment)

## Commands Table

| Command | Description |
|---------|-------------|
| `risco whistle setup` | Channel implementation checklist |
| `risco whistle policy` | Whistleblowing policy template |
| `risco whistle report` | Report intake form template |
| `risco whistle investigate` | Investigation procedure and template |
| `risco whistle protect` | Retaliation protection measures guide |
| `risco whistle stats` | Annual channel statistics template |
| `risco whistle assess` | Channel effectiveness assessment |
| `risco whistle training` | Training materials for staff |

## Output Template

```markdown
# Whistleblowing Channel Report — [Organization]
**Date:** YYYY-MM-DD | **Channel Manager:** [Name] | **Period:** [Start-End]

## 1. Channel Status
- Type: [platform/email/phone/mixed]
- Live since: YYYY-MM-DD
- DL 93/2021 compliant: [Yes/No — gaps listed below]
- Anonymous reporting: [Enabled/Disabled]

## 2. Report Statistics (Period)
| Metric | Count |
|--------|-------|
| Reports received | X |
| Admissible | X |
| Under investigation | X |
| Substantiated | X |
| Unsubstantiated | X |
| Avg. time to feedback | X days |
| Avg. investigation time | X days |

## 3. Report Categories
| Category | Count | % |
|----------|-------|---|

## 4. Remedial Actions Taken
| Case # | Action | Status |
|--------|--------|--------|

## 5. Retaliation Monitoring
- Retaliation claims: X | Confirmed: X
- Protective measures active: X

## 6. Compliance Gaps
| # | Gap | Risk | Action | Deadline |
|---|-----|------|--------|----------|

## 7. Next Review: YYYY-MM-DD
```

## Red Flags

- No internal channel established despite legal obligation (50+ workers)
- Channel not accessible to external stakeholders (contractors, suppliers)
- Acknowledgment of receipt exceeds 7-day deadline
- Feedback to reporter exceeds 3-month deadline
- Reporter identity disclosed without consent
- No retaliation protection measures documented
- Investigation conducted by person with conflict of interest
- Records not encrypted or access not restricted
- No annual statistics or Board reporting on channel
- Channel existence not communicated to all eligible reporters
- Reports dismissed without proper admissibility assessment
- No designated independent person responsible for channel
- Anonymous reports automatically rejected
- Retention of personal data beyond necessary period


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **risco-whistleblowing** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in risco-whistleblowing:**

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
