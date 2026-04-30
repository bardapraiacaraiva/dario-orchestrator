---
name: risco-iso27001
description: "ISO 27001/NIS2 — ISMS implementation, Annex A controls, Statement of Applicability, incident management, certification"
version: "1.0"
---

# RISCO-ISO27001: Information Security Management Skill

## When to Activate

**Trigger words (PT):** iso 27001, sgsi, seguranca da informacao, nis2, declaracao de aplicabilidade, controlos, incidente de seguranca, certificacao, politica de seguranca, gestao de ativos, continuidade
**Trigger words (EN):** iso 27001, isms, information security, nis2, statement of applicability, soa, security controls, security incident, certification, security policy, asset management, annex a

## Step-by-Step Workflow

### Phase 1: ISMS Scope & Context
1. Define ISMS scope (locations, systems, processes, organizational units)
2. Identify interested parties and their requirements
3. Determine internal/external issues affecting ISMS
4. Document scope statement
5. Secure management commitment and resources

### Phase 2: Risk Assessment (ISO 27001 Clause 6.1.2)
1. Define risk assessment methodology
2. Identify information assets within scope
3. Identify threats and vulnerabilities per asset
4. Assess likelihood and impact (use risco-matrix skill)
5. Determine risk levels and risk acceptance criteria
6. Document risk treatment plan (Clause 6.1.3)

### Phase 3: Statement of Applicability (SOA)
1. Review all 93 Annex A controls (ISO 27001:2022)
2. For each control: applicable/not applicable with justification
3. Map controls to identified risks
4. Document implementation status (implemented, partially, planned, not)
5. Cross-reference with NIS2 requirements if applicable

### Phase 4: Control Implementation
1. Organizational controls (A.5): policies, roles, asset management, access
2. People controls (A.6): screening, awareness, training, disciplinary
3. Physical controls (A.7): perimeters, entry, offices, equipment, media
4. Technological controls (A.8): endpoints, access rights, crypto, logging, network, secure dev
5. Document control procedures and evidence

### Phase 5: Incident Management
1. Define incident classification scheme (P1-P4)
2. Establish reporting channels and response team
3. Incident response procedure: detect, contain, eradicate, recover
4. Post-incident review and lessons learned
5. NIS2: report significant incidents to CNCS within 24h (early warning), 72h (full notification)
6. Maintain incident register with root cause analysis

### Phase 6: Monitoring & Certification
1. Conduct internal audits (Clause 9.2) per audit schedule
2. Management review (Clause 9.3) — at least annually
3. Measure ISMS performance (KPIs, metrics)
4. Continuous improvement (Clause 10) — corrective actions
5. Stage 1 audit (documentation review) + Stage 2 audit (implementation)
6. Surveillance audits (annual) + Recertification (3-year cycle)

## Commands Table

| Command | Description |
|---------|-------------|
| `risco iso27001 gap` | Gap analysis against ISO 27001:2022 |
| `risco iso27001 soa` | Generate Statement of Applicability template |
| `risco iso27001 risk` | Information security risk assessment |
| `risco iso27001 policy` | Generate ISMS policy templates |
| `risco iso27001 incident` | Incident management procedure |
| `risco iso27001 nis2` | NIS2 compliance checklist (EU Directive 2022/2555) |
| `risco iso27001 audit` | Internal ISMS audit checklist |
| `risco iso27001 controls` | Annex A control implementation guide |

## Output Template

```markdown
# ISMS Assessment — [Organization]
**Date:** YYYY-MM-DD | **Standard:** ISO 27001:2022 | **Scope:** [Description]

## 1. Maturity Overview
| Domain | Controls | Implemented | Partial | Planned | N/A | Score |
|--------|----------|-------------|---------|---------|-----|-------|
| A.5 Organizational | 37 | | | | | /100 |
| A.6 People | 8 | | | | | /100 |
| A.7 Physical | 14 | | | | | /100 |
| A.8 Technological | 34 | | | | | /100 |
| **Total** | **93** | | | | | **/100** |

## 2. Top Gaps
| # | Control | Gap Description | Risk | Priority |
|---|---------|----------------|------|----------|

## 3. Risk Treatment Plan
| Risk ID | Control(s) | Status | Owner | Deadline |
|---------|-----------|--------|-------|----------|

## 4. NIS2 Alignment (if applicable)
- Entity classification: [Essential / Important / Out of scope]
- Notification obligations: [24h early warning, 72h full report to CNCS]
- Supply chain security: [assessed / not assessed]

## 5. Certification Readiness: [Ready / Not Ready — X gaps to close]

## 6. Next Review: YYYY-MM-DD
```

## Red Flags

- No formal ISMS scope defined
- Risk assessment not conducted or not aligned with ISO 27001 methodology
- SOA missing or not updated after ISO 27001:2022 transition
- No incident response procedure or team
- Annex A controls marked "N/A" without justification
- No internal ISMS audit conducted in last 12 months
- Management review not performed annually
- NIS2 obligations not mapped (if entity is essential/important)
- Security awareness training not conducted for all staff
- No business continuity plan integrated with ISMS
- Vendor/supplier security not assessed
- Encryption policies absent for data at rest and in transit
