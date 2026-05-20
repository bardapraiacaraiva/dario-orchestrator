---
name: aegis-third-party-risk
description: Third-Party Risk Management (TPRM) — vendor security assessment, SIG/SIG Lite, SOC 2 review, continuous monitoring. Triggers em "third party risk", "TPRM", "vendor risk", "SIG questionnaire", "SOC 2 review", "vendor assessment", "supply chain risk".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, soc2_type2, audit_immutable]
---

# AEGIS-THIRD-PARTY-RISK

## Quando usar
- TPRM program greenfield (vendors >50)
- Vendor onboarding security review
- Critical vendor annual reassessment
- M&A vendor inventory + risk
- Incident em vendor (response coordination)

## Frameworks
- **SIG / SIG Lite (Shared Assessments):** standard questionnaire
- **CAIQ (CSA):** Consensus Assessments Initiative
- **HECVAT** (higher ed-focused)
- **NIST SP 800-161:** Supply Chain Risk Management
- **ISO 27036:** supplier relationships

## Tipos de vendor
- **Critical:** access to crown jewels (production data, PII massa)
- **High:** material business dependency (SaaS líder)
- **Medium:** moderate access ou criticality
- **Low:** no sensitive data, easily replaceable

## Stack
- **Drata Trust** — automated TPRM
- **OneTrust Vendorpedia / Whistic**
- **ProcessUnity / Prevalent**
- **BitSight / SecurityScorecard** — continuous monitoring (external posture)
- **UpGuard** — combined questionnaire + continuous

## Templates
1. Vendor risk classification rubric (Critical/High/Medium/Low)
2. SIG Lite questionnaire (45 questions baseline)
3. Critical vendor deep dive (SOC 2 + pentest report + SBOM review)
4. Continuous monitoring setup (BitSight/SecurityScorecard)
5. Vendor incident playbook (their breach → our exposure)
6. Vendor offboarding checklist (data destruction certification)

## Compliance
- ✓ ISO 27001 A.15 — Supplier relationships
- ✓ SOC 2 CC9 — Risk Mitigation
- ✓ LGPD Art. 39 — Operator obligations
- ✓ NIS2 (EU) supply chain requirements

## Cross-references
- [[aegis-compliance-frameworks]] · [[aegis-supply-chain-security]] · [[risco-terceiros]]
