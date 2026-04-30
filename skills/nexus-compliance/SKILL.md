---
name: nexus-compliance
description: "IT compliance — SOC2, ISO 27001 technical controls, change management, evidence collection, audit readiness"
version: "1.0"
---

# NEXUS-COMPLIANCE: IT Compliance Skill

## When to Activate

**Trigger words (PT):** compliance ti, soc2, iso 27001 tecnico, gestao de mudancas, evidencias, auditoria ti, controlos tecnicos, change management, segregacao de ambientes
**Trigger words (EN):** it compliance, soc2, iso 27001 technical, change management, evidence collection, it audit, technical controls, change advisory board, cab, segregation of environments, audit trail

## Step-by-Step Workflow

### Phase 1: Compliance Framework Mapping
1. Identify applicable frameworks:
   - **SOC 2**: Trust Service Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy)
   - **ISO 27001**: Annex A technical controls (A.8)
   - **PCI DSS**: if processing payment card data
   - **HIPAA**: if handling health information
   - **NIS2**: if essential/important entity in EU
2. Map framework requirements to technical controls
3. Identify overlapping controls (implement once, evidence for multiple)
4. Gap analysis: current state vs required controls
5. Prioritize: mandatory (regulatory) > contractual > best practice

### Phase 2: Change Management
1. Change classification:
   - **Standard**: pre-approved, low risk (e.g., config update within parameters)
   - **Normal**: requires CAB approval, scheduled implementation
   - **Emergency**: bypass normal process, retroactive approval within 48h
2. Change request template: description, impact, risk, rollback, testing
3. Change Advisory Board (CAB): weekly review of normal changes
4. Change calendar: no changes during freeze periods (month-end, peak)
5. Post-implementation review: verify success, close change ticket
6. Change log: immutable audit trail of all changes

### Phase 3: Access Control Evidence
1. Access provisioning records (who approved, when, what access)
2. Quarterly access reviews with evidence (screenshots, exports)
3. Privileged access logs and session recordings
4. Service account inventory with rotation evidence
5. MFA enrollment evidence (enrollment date, method)
6. Termination process evidence (access revoked within SLA)

### Phase 4: Security Controls Evidence
1. Vulnerability scan reports (scheduled + remediation evidence)
2. Patch management records (what, when, which systems)
3. Encryption configuration evidence (at rest, in transit)
4. Firewall rule reviews (quarterly review documentation)
5. Penetration test reports (annual + remediation plans)
6. Security awareness training records (completion, scores)

### Phase 5: Operational Controls Evidence
1. Backup records: job logs, success/failure, restore test results
2. Monitoring and alerting: alert rules, incident response records
3. Business continuity: BCP document, test records
4. Incident management: ticket logs, response times, resolution
5. Capacity management: utilization reports, scaling events
6. Availability records: uptime reports, SLA compliance

### Phase 6: Audit Preparation
1. Evidence repository: organized by control, time period, framework
2. Continuous compliance monitoring (automated where possible)
3. Internal audit schedule for IT controls
4. Pre-audit readiness assessment (30 days before external audit)
5. Auditor communication: scope clarification, evidence delivery, issue resolution
6. Remediation tracking for audit findings

## Commands Table

| Command | Description |
|---------|-------------|
| `nexus compliance audit` | IT compliance readiness assessment |
| `nexus compliance soc2` | SOC 2 control mapping and evidence checklist |
| `nexus compliance change` | Change management procedure template |
| `nexus compliance evidence` | Evidence collection guide by control |
| `nexus compliance gap` | Gap analysis against framework |
| `nexus compliance matrix` | Control-to-framework mapping matrix |
| `nexus compliance cab` | CAB process and meeting template |
| `nexus compliance report` | Compliance status dashboard |

## Output Template

```markdown
# IT Compliance Assessment — [Organization]
**Date:** YYYY-MM-DD | **Framework(s):** [SOC2/ISO27001/etc.] | **Audit Date:** YYYY-MM-DD

## 1. Control Maturity
| Domain | Controls | Implemented | Evidenced | Gap | Maturity |
|--------|----------|-------------|-----------|-----|----------|
| Access Control | | | | | /5 |
| Change Management | | | | | /5 |
| Security Operations | | | | | /5 |
| Data Protection | | | | | /5 |
| Business Continuity | | | | | /5 |
| Monitoring & Logging | | | | | /5 |
| **Overall** | | | | | **/5** |

## 2. Change Management Summary (Period)
| Type | Count | Approved | Emergency | Failed | Unauthorized |
|------|-------|----------|-----------|--------|-------------|
| Standard | | | | | |
| Normal | | | | | |
| Emergency | | | | | |

## 3. Evidence Status
| Control | Evidence Type | Frequency | Last Collected | Gap |
|---------|-------------|-----------|---------------|-----|

## 4. Open Audit Findings
| Finding | Framework | Severity | Owner | Deadline | Status |
|---------|-----------|----------|-------|----------|--------|

## 5. Upcoming Audit Readiness
| Area | Ready | Evidence Gap | Action Needed |
|------|-------|-------------|--------------|

## 6. Recommendations
| # | Control Gap | Framework | Action | Priority |
|---|-----------|-----------|--------|----------|

## 7. Next Audit: YYYY-MM-DD | Next Review: YYYY-MM-DD
```

## Red Flags

- No change management process (changes applied ad-hoc to production)
- Emergency changes >10% of total changes (process bypass habit)
- No evidence of access reviews (or reviews only on paper)
- Audit findings from prior year not remediated
- No segregation of environments (dev can access production data)
- Deployment to production without testing or approval
- No audit trail for administrative actions
- Evidence collection only at audit time (not continuous)
- SOC 2 Type II period with control gaps (failed audit)
- No CAB or change approval process
- Developer access to production databases and servers
- Compliance framework not mapped to actual technical controls
