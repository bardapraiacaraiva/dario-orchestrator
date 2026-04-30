---
name: "PESSOA Talent Acquisition"
description: "Full-cycle talent acquisition — job descriptions, sourcing strategy, ATS workflow, structured interviews, scorecards, offer letters, and onboarding handoff."
version: "1.0"
agent: "P.E.S.S.O.A. — People, Engagement, Skills, Succession, Organization & Alignment"
category: "Recruit"
---

# PESSOA Talent Acquisition

## Triggers

Activate this skill when the user says any of:
- "recruit", "recrutar", "recrutamento", "hiring"
- "job description", "descricao de funcao", "anuncio de emprego"
- "interview", "entrevista", "structured interview"
- "sourcing", "candidate pipeline"
- "scorecard", "offer letter", "carta de oferta"
- "ATS", "applicant tracking"
- "I need to hire", "preciso de contratar"
- Any request to find, evaluate, or hire talent

## Frameworks & References

- **Geoff Smart & Randy Street** (Who) — A Method for Hiring, scorecard, topgrading interview
- **Laszlo Bock** (Work Rules!) — Google's structured interview methodology, qDroid
- **Lou Adler** (Hire With Your Head) — performance-based job descriptions, quality of hire
- **SHRM** — Competency-based hiring standards, legal compliance
- **Codigo do Trabalho (PT)** — Portuguese labor law on recruitment, non-discrimination, trial periods

## Workflow

### Step 1: Hiring Request & Role Definition

| Field | Detail |
|-------|--------|
| **Role title** | [Title] |
| **Department** | [Department] |
| **Reports to** | [Manager name/title] |
| **Location** | [Office / Remote / Hybrid] |
| **Contract type** | [Termo certo / Sem termo / Freelancer / Estagio] |
| **Start date** | [Target] |
| **Budget (salary range)** | EUR X - Y gross/month |
| **Urgency** | [Critical / High / Normal] |
| **Headcount approval** | [Approved by whom, date] |

### Step 2: Job Description (Performance-Based, Adler)

**Template:**

```markdown
## [ROLE TITLE]
### About [COMPANY]
[2-3 sentences about company, mission, culture]

### The Role
[2-3 sentences about impact this role will have]

### Key Outcomes (First 12 Months)
1. [Outcome 1 — specific, measurable result expected]
2. [Outcome 2]
3. [Outcome 3]
4. [Outcome 4]
5. [Outcome 5]

### Requirements
**Must-Have:**
- [Requirement 1 — skill or experience]
- [Requirement 2]
- [Requirement 3]

**Nice-to-Have:**
- [Bonus skill 1]
- [Bonus skill 2]

### What We Offer
- [Compensation range]
- [Benefits]
- [Growth opportunity]
- [Culture/perks]

### How to Apply
[Instructions, link, deadline]
```

**Rules:**
- Focus on outcomes, not tasks (what they ACHIEVE, not what they DO)
- Max 5 must-have requirements (more = fewer applicants)
- Include salary range (transparency increases quality applicants by 30%)
- Gender-neutral language throughout

### Step 3: Sourcing Strategy

| Channel | Type | Cost | Best For | Expected Volume |
|---------|------|------|----------|----------------|
| **LinkedIn** | Active sourcing | EUR 0-300/mo | Mid-senior, B2B | Medium |
| **Net Empregos / Sapo Emprego** | Job board | EUR 50-200 | Junior-mid PT market | High |
| **Indeed** | Job board | Free-paid | All levels | High |
| **Employee referrals** | Internal | EUR 0-500 bonus | All levels (best quality) | Low-Med |
| **University partnerships** | Campus | Free | Interns, juniors | Low |
| **Recruitment agency** | External | 15-25% salary | Senior, specialized | Low |
| **Social media (organic)** | Content | Free | Culture-fit candidates | Variable |
| **IEFP** | Government | Free/subsidized | Supported hiring programs | Variable |

**Sourcing Funnel Math:**

| Stage | Volume | Conversion |
|-------|--------|-----------|
| Applications received | X | 100% |
| CV screen pass | X | 30-40% |
| Phone screen pass | X | 50-60% |
| Interview 1 pass | X | 40-50% |
| Interview 2 / Task pass | X | 50-60% |
| Offer made | X | 80-90% |
| Offer accepted | 1 | 70-80% |

### Step 4: ATS Workflow & Pipeline

**Stages:**
1. **Applied** — CV received, awaiting review
2. **Screening** — CV review against scorecard criteria
3. **Phone Screen** — 15-20 min call (culture, motivation, expectations)
4. **Interview 1** — Structured behavioral interview (60 min)
5. **Task/Assessment** — Technical test or case study (take-home or live)
6. **Interview 2** — Final interview with hiring manager + team (45 min)
7. **Reference Check** — 2-3 professional references
8. **Offer** — Verbal then written offer
9. **Hired** — Contract signed, onboarding scheduled

**SLA Targets:**

| Metric | Target | Measure |
|--------|--------|---------|
| Time to fill | <30 days (junior), <45 days (senior) | Application to acceptance |
| Time to first response | <48 hours | Application to first contact |
| Interview-to-offer | <7 days | Last interview to offer |
| Candidate NPS | >7/10 | Post-process survey |

### Step 5: Structured Interview Design (Bock/Smart)

**Scorecard Dimensions (Smart "Who" Method):**

| Dimension | Questions | Rating (1-5) |
|-----------|-----------|-------------|
| **Mission fit** | "Tell me about a time you [mission-aligned behavior]" | /5 |
| **Outcome 1 competency** | "Describe how you achieved [relevant outcome] in a past role" | /5 |
| **Outcome 2 competency** | "Walk me through your approach to [relevant challenge]" | /5 |
| **Culture add** | "What work environment brings out your best work?" | /5 |
| **Growth potential** | "What skill are you actively developing right now?" | /5 |

**Behavioral Interview Formula (STAR):**
- **S**ituation — "Tell me about a time when..."
- **T**ask — "What was your role/responsibility?"
- **A**ction — "What specifically did YOU do?"
- **R**esult — "What was the outcome? What did you learn?"

**Interview Anti-Patterns (avoid):**
- Unstructured "tell me about yourself" conversations
- Brain teasers or trick questions
- Questions about age, marital status, religion, politics (illegal in PT)
- Same interviewer evaluating alone (minimum 2 interviewers)
- Gut feeling without scorecard documentation

### Step 6: Candidate Scorecard

| Candidate | Mission (1-5) | Comp 1 (1-5) | Comp 2 (1-5) | Culture (1-5) | Growth (1-5) | Total (/25) | Recommendation |
|-----------|--------------|--------------|--------------|---------------|-------------|-------------|----------------|
| [Name 1] | X | X | X | X | X | /25 | Hire / No Hire |
| [Name 2] | X | X | X | X | X | /25 | Hire / No Hire |
| [Name 3] | X | X | X | X | X | /25 | Hire / No Hire |

**Decision Rules:**
- Score 20-25: Strong Hire
- Score 15-19: Hire with reservations (document concerns)
- Score 10-14: No Hire
- Any dimension below 2: Automatic No Hire (non-negotiable weakness)

### Step 7: Offer Letter Template (PT)

**Key Elements:**

| Element | Detail |
|---------|--------|
| **Role title** | [Title] |
| **Gross monthly salary** | EUR X |
| **Subsidio de alimentacao** | EUR X/day (meal allowance) |
| **Contract type** | Sem termo / Termo certo (X months) |
| **Trial period** | 90 days (standard) / 180 days (management) |
| **Working hours** | 40h/week, [schedule] |
| **Start date** | [Date] |
| **Benefits** | [Health insurance, remote policy, etc.] |
| **Notice period** | Per Codigo do Trabalho |

**PT Legal Requirements:**
- Written contract within 60 days of start (Codigo do Trabalho Art. 110)
- Comunicacao de admissao to Seguranca Social before start date
- Seguro de acidentes de trabalho active before start date
- Copy of contract to employee on day 1

### Step 8: Onboarding Handoff

| Item | Responsible | Deadline | Done? |
|------|------------|----------|-------|
| Contract signed | HR/Legal | Before start | [ ] |
| SS registration | HR | Before start | [ ] |
| Insurance active | HR | Before start | [ ] |
| Equipment ordered | IT/Admin | Before start | [ ] |
| Accounts created | IT | Day 1 | [ ] |
| Welcome email sent | Manager | Day -1 | [ ] |
| Day 1 schedule prepared | Manager | Day -1 | [ ] |
| Buddy assigned | HR | Day 1 | [ ] |
| 30-60-90 day plan | Manager | Day 1 | [ ] |

## Output Template

```markdown
# PESSOA Recruitment Plan
## Role: [TITLE]
## Department: [DEPT]
## Date: YYYY-MM-DD

### Job Description
[Full JD following template]

### Sourcing Plan
| Channel | Budget | Target Applications |
|---------|--------|-------------------|
| [Channel] | EUR X | X |

### Interview Process
[Stage-by-stage with timeline]

### Scorecard
[Dimensions and rating criteria]

### Offer Parameters
- Salary range: EUR X-Y
- Contract: [type]
- Start: [date]

### Timeline
- JD published: [date]
- Applications close: [date]
- Interviews: [date range]
- Offer: [date]
- Start: [date]

### Recruitment Health Score: X/10
```

## Red Flags

Stop and warn the user if:
- Job description lists 15+ requirements (will attract zero candidates)
- No salary range disclosed (reduces quality applicants significantly)
- Unstructured interviews with no scorecard (bias-prone, legally risky)
- Hiring based on "gut feeling" without documented evaluation
- No trial period defined in contract (missed legal opportunity)
- Questions about protected characteristics (age, family, religion, health)
- Skipping reference checks for senior roles
- Offering below market rate without compensating benefits
- No onboarding plan prepared before start date
- Single interviewer making the decision alone
- Hiring urgency overriding quality standards

## Handoff

After recruitment:
- Route to `pessoa-compensacao` for salary benchmarking and offer design
- Route to `pessoa-performance` to set OKRs for the new hire
- Route to `pessoa-learning` for training plan design
- Route to `adriana-onboarding` for administrative onboarding checklist
- Route to `pessoa-labor-pt` for contract compliance verification
- Save output to Obsidian: `05 - Claude - IA/Outputs/YYYY-MM-DD - PESSOA - Recruitment - [RoleTitle].md`
