---
name: risco-bcp
description: "Business continuity — BIA, recovery strategies, crisis management, BCM testing, ISO 22301"
version: "1.0"
---

# RISCO-BCP: Business Continuity Planning Skill

## When to Activate

**Trigger words (PT):** continuidade de negocio, bcp, bia, plano de recuperacao, gestao de crises, desastre, resiliencia, rto, rpo, iso 22301, plano de contingencia, exercicio de continuidade
**Trigger words (EN):** business continuity, bcp, bia, business impact analysis, disaster recovery, crisis management, resilience, rto, rpo, iso 22301, contingency plan, bcm testing, incident command

## Step-by-Step Workflow

### Phase 1: Business Impact Analysis (BIA)
1. Identify all critical business processes and services
2. Determine Maximum Tolerable Period of Disruption (MTPD) per process
3. Define Recovery Time Objective (RTO): time to restore minimum service
4. Define Recovery Point Objective (RPO): maximum acceptable data loss
5. Identify resource dependencies: people, IT, facilities, suppliers, data
6. Quantify financial and non-financial impact over time (1h, 4h, 1d, 3d, 1w, 1m)
7. Rank processes by criticality (Tier 1/2/3)

### Phase 2: Recovery Strategies
1. For each Tier 1 process, define recovery strategy:
   - **People**: cross-training, remote work, temporary staff
   - **Technology**: failover, backup restoration, DR site, cloud
   - **Facilities**: alternative workspace, work-from-home, co-working
   - **Suppliers**: alternative suppliers, stockpiling, dual-sourcing
2. Cost-benefit analysis of strategies vs risk
3. Document Minimum Business Continuity Objective (MBCO) per process
4. Define resource requirements for recovery

### Phase 3: BCP Documentation
1. Business Continuity Plan structure:
   - Plan activation criteria and authority
   - Contact lists (internal + external: suppliers, regulators, media)
   - Recovery procedures per Tier 1/2 process
   - IT Disaster Recovery sub-plan
   - Communication plan (internal + external)
2. Crisis Management Plan:
   - Incident Command Structure (ICS)
   - Escalation matrix
   - Decision-making authority
   - Media/stakeholder communication templates

### Phase 4: Testing & Exercises
1. Tabletop exercise (annual minimum): scenario walkthrough with leadership
2. Functional test: execute specific recovery procedures
3. Full simulation: comprehensive test including IT failover
4. Test types rotation: fire, cyber, pandemic, supplier failure, natural disaster
5. Document lessons learned and update plans
6. Track test results and improvement actions

### Phase 5: Crisis Communication
1. Pre-draft templates: employee, customer, media, regulator
2. Designate spokesperson(s) and approve chain
3. Social media monitoring and response plan
4. Internal communication cascade (who notifies whom)
5. Regulatory notification requirements (sector-specific)

### Phase 6: Maintenance & Improvement
1. Review and update BCP at least annually
2. Update after organizational changes (new systems, restructuring, M&A)
3. Update after incidents or near-misses
4. Track action items from tests and real incidents
5. Management review and Board reporting
6. Align with ISO 22301 for certification (if desired)

## Commands Table

| Command | Description |
|---------|-------------|
| `risco bcp bia` | Business Impact Analysis template |
| `risco bcp plan` | BCP document template |
| `risco bcp crisis` | Crisis Management Plan template |
| `risco bcp dr` | IT Disaster Recovery Plan template |
| `risco bcp test` | Exercise/test scenario generator |
| `risco bcp contacts` | Emergency contact list template |
| `risco bcp comms` | Crisis communication templates |
| `risco bcp review` | BCP maturity assessment |

## Output Template

```markdown
# Business Continuity Assessment — [Organization]
**Date:** YYYY-MM-DD | **BC Manager:** [Name] | **Standard:** ISO 22301

## 1. BIA Summary
| Process | Tier | MTPD | RTO | RPO | Dependencies |
|---------|------|------|-----|-----|-------------|

## 2. Recovery Strategy Status
| Tier 1 Process | Strategy | Implemented | Last Tested | Gap |
|---------------|----------|-------------|-------------|-----|

## 3. BCP Documentation Status
| Document | Version | Last Updated | Owner | Review Due |
|----------|---------|-------------|-------|------------|
| Business Continuity Plan | | | | |
| Crisis Management Plan | | | | |
| IT DR Plan | | | | |
| Communication Plan | | | | |

## 4. Test History
| Date | Type | Scenario | Result | Actions |
|------|------|----------|--------|---------|

## 5. Open Actions
| # | Action | Source | Owner | Deadline | Status |
|---|--------|--------|-------|----------|--------|

## 6. Maturity Score
| Dimension | Score (1-5) |
|-----------|-------------|
| BIA completeness | |
| Recovery strategies | |
| Documentation | |
| Testing | |
| Crisis management | |
| Maintenance | |
| **Overall** | **/5** |

## 7. Next Review: YYYY-MM-DD
```

## Red Flags

- No BIA conducted or BIA older than 2 years
- RTO/RPO not defined for critical processes
- BCP never tested or last test >12 months ago
- No crisis management team or escalation matrix
- Single points of failure in Tier 1 processes
- IT disaster recovery not aligned with business RTO/RPO
- No alternative workplace or remote work capability
- Key supplier with no continuity plan (cascade risk)
- Contact lists outdated
- Crisis communication templates not pre-drafted
- No management review of BCP
- Real incident revealed gaps not addressed in plan
