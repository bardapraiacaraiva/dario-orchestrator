---
name: aegis-threat-modeling
description: Threat modeling — STRIDE, PASTA, LINDDUN, attack trees, OWASP Threat Dragon. Triggers em "threat modeling", "STRIDE", "PASTA", "LINDDUN", "attack tree", "modelagem de ameaças".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [audit_immutable]
---

# AEGIS-THREAT-MODELING

## Quando usar
- New system design (greenfield)
- Major architecture change
- Pre-pentest (focar test scope)
- Compliance requirement (ISO 27001 A.14)
- Post-incident retrospective

## Frameworks
- **STRIDE (Microsoft):** Spoofing/Tampering/Repudiation/Info Disclosure/DoS/Elevation
- **PASTA:** 7 stages, risk-centric
- **LINDDUN:** privacy-focused (Linkability/Identifiability/Non-repudiation/Detectability/Unawareness/Non-compliance)
- **Attack trees (Schneier):** hierarchical attacks
- **OCTAVE:** asset-centric
- **VAST:** scalable for agile

## Templates
1. STRIDE analysis per component (data flow diagram + threats)
2. Attack tree template
3. LINDDUN privacy threat model
4. Threat library (kb of common threats)
5. Mitigation tracking (threat → control → status)

## Stack
- **OWASP Threat Dragon** (open-source)
- **Microsoft Threat Modeling Tool**
- **IriusRisk** (enterprise)
- **ThreatModeler**
- **PyTM** (code-as-threat-model)

## Cross-references
- [[aegis-secure-sdlc]] · [[aegis-pentest-methodology]] · [[aegis-soc-operations]]
