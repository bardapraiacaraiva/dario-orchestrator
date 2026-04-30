---
name: risco-audit
description: "Internal audit — planning, fieldwork, findings documentation, management response, follow-up tracking"
version: "1.0"
---

# RISCO-AUDIT: Internal Audit Skill

## When to Activate

**Trigger words (PT):** auditoria interna, plano de auditoria, achados, recomendacoes, fieldwork, amostragem, controlo interno, resposta da gestao, follow-up, universo de auditoria, risco de auditoria
**Trigger words (EN):** internal audit, audit plan, audit findings, audit recommendations, fieldwork, sampling, internal control, management response, follow-up, audit universe, audit risk, audit committee

## Step-by-Step Workflow

### Phase 1: Annual Audit Planning
1. Define audit universe (all auditable entities/processes/systems)
2. Conduct risk-based prioritization using risk matrix scores
3. Allocate resources (hours, team, budget) per engagement
4. Draft Annual Audit Plan with timeline
5. Present to Audit Committee/Board for approval
6. Reserve capacity for ad-hoc/special investigations (15-20%)

### Phase 2: Engagement Planning
1. Issue engagement letter with scope, objectives, timeline
2. Review prior audit reports and open findings
3. Understand process through walkthroughs and documentation review
4. Identify key risks and controls to test
5. Develop audit program (test procedures, sample sizes, criteria)
6. Schedule interviews and data requests

### Phase 3: Fieldwork
1. Execute test procedures per audit program
2. Collect and analyze evidence (documents, screenshots, data extracts)
3. Conduct interviews with process owners
4. Perform substantive testing and compliance testing
5. Document working papers with cross-references
6. Identify exceptions and potential findings

### Phase 4: Findings & Reporting
1. Draft findings using structured format (condition, criteria, cause, effect)
2. Rate findings by severity (Critical / High / Medium / Low / Advisory)
3. Discuss findings with auditee (exit meeting)
4. Obtain management response and action plan with deadlines
5. Issue draft report for review
6. Issue final audit report

### Phase 5: Follow-Up
1. Track open findings in follow-up register
2. Verify implementation of corrective actions (evidence-based)
3. Re-test controls after remediation
4. Escalate overdue items to Audit Committee
5. Close findings only when fully remediated and verified

## Commands Table

| Command | Description |
|---------|-------------|
| `risco audit plan` | Generate annual audit plan template |
| `risco audit engage` | Create engagement planning document |
| `risco audit program` | Build audit program with test procedures |
| `risco audit finding` | Document finding (4Cs format) |
| `risco audit report` | Generate audit report template |
| `risco audit followup` | Follow-up tracker for open findings |
| `risco audit universe` | Define/update audit universe |
| `risco audit sample` | Calculate sample size for testing |

## Output Template

```markdown
# Internal Audit Report — [Engagement Title]
**Report #:** IA-YYYY-NNN | **Date:** YYYY-MM-DD
**Auditor(s):** [Names] | **Period Under Review:** [Dates]

## 1. Executive Summary
- **Overall Rating:** [Satisfactory / Needs Improvement / Unsatisfactory]
- **Scope:** [Description]
- **Objectives:** [List]
- Findings: X Critical, X High, X Medium, X Low

## 2. Findings

### Finding #1: [Title]
- **Rating:** [Critical/High/Medium/Low]
- **Condition:** What was found (the fact)
- **Criteria:** What should be (policy, regulation, best practice)
- **Cause:** Why it happened (root cause)
- **Effect:** Business impact / risk exposure
- **Recommendation:** Suggested corrective action
- **Management Response:** [Agree/Partially Agree/Disagree]
- **Action Owner:** [Name] | **Deadline:** YYYY-MM-DD

## 3. Positive Observations
- [List of well-functioning controls or good practices]

## 4. Scope Limitations
- [Any access issues, data gaps, or constraints]

## 5. Follow-Up on Prior Findings
| Finding # | Original Date | Status | Evidence Verified |
|-----------|--------------|--------|-------------------|
```

## Red Flags

- No annual audit plan or plan not risk-based
- Audit findings with no management response or vague action plans
- Overdue findings (>6 months past deadline) with no escalation
- Audit reports not distributed to Audit Committee
- No follow-up process for open findings
- Auditor independence compromised (auditing own prior work area)
- Sampling methodology not documented or not statistically valid
- Working papers incomplete or missing evidence
- No audit universe defined
- Repeat findings year after year with no root cause analysis
- Management response: "risk accepted" for critical findings without Board approval
- Audit function understaffed relative to risk profile
