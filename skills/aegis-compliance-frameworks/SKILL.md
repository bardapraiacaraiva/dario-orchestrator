---
name: aegis-compliance-frameworks
description: Compliance — ISO 27001/2, SOC 2, PCI-DSS, HIPAA, NIST CSF. Audit prep, gap analysis. Triggers em "ISO 27001", "SOC 2", "PCI DSS", "HIPAA", "NIST CSF", "compliance audit", "auditoria segurança".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, soc2_type2, audit_immutable]
---

# AEGIS-COMPLIANCE-FRAMEWORKS

## Quando usar
- Certification first-time (ISO 27001, SOC 2)
- Annual recertification
- Customer/vendor requirement (enterprise customers asking for SOC 2)
- Gap analysis pré-audit
- Multi-framework alignment (single program, multiple certs)

## Frameworks
- **ISO 27001/27002:** ISMS, controls (Annex A 2022)
- **SOC 2 Type II:** Trust Service Criteria (5 TSCs)
- **PCI-DSS 4.0:** payment card data
- **HIPAA:** US healthcare
- **NIST CSF 2.0:** Identify/Protect/Detect/Respond/Recover/Govern
- **CIS Controls v8:** 18 controls + IGs
- **CSA STAR:** cloud security
- **LGPD/GDPR:** privacy

## Templates
1. ISO 27001 Statement of Applicability (SoA)
2. Risk register (ISO 27005)
3. Annex A control implementation tracker
4. SOC 2 evidence collection schedule
5. PCI-DSS scoping (CDE + connected systems)
6. Multi-framework crosswalk matrix

## Stack
- **GRC tools:** Drata, Vanta, Secureframe, Tugboat
- **Risk:** ServiceNow GRC, RSA Archer, OneTrust
- **Audit:** AuditBoard, Workiva

## Cross-references
- [[risco-iso27001]] · [[aegis-secure-sdlc]] · [[lex-lgpd]]
