---
name: aegis-secure-sdlc
description: Secure SDLC — SAST, DAST, SCA, IAST, threat modeling, secure coding. Triggers em "Secure SDLC", "SAST", "DAST", "SCA", "Snyk", "Checkmarx", "Veracode", "shift left security".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, secure_coding]
---

# AEGIS-SECURE-SDLC

## Filosofia
**Shift left + shield right.** Security em todas fases SDLC, não só pre-prod.

## Frameworks
- **OWASP SAMM:** Software Assurance Maturity Model
- **BSIMM:** Building Security In Maturity Model
- **NIST SSDF (SP 800-218)** — Secure Software Dev Framework
- **Microsoft SDL** — classic reference

## SAST / DAST / SCA / IAST
- **SAST:** Static analysis (Checkmarx, Veracode, Snyk Code, Semgrep)
- **DAST:** Dynamic, runtime (OWASP ZAP, Burp Suite, Acunetix)
- **SCA:** Software Composition (Snyk Open Source, Mend, Dependabot)
- **IAST:** Interactive (Contrast Security, Synopsys Seeker)
- **Container scan:** Trivy, Grype, Snyk Container

## Templates
1. Secure SDLC policy + RACI
2. Threat modeling per major feature (lightweight)
3. CI security gates (lint + SAST + SCA + secret scan + IaC scan)
4. Pre-prod DAST automation
5. Security champions program (1 per team)
6. Vuln remediation SLA matrix

## Pipeline (gates típicos)
```
PR open → secret scan + SAST → tests
Merge → SCA + container scan
Pre-deploy → DAST + IaC scan
Post-deploy → DAST scheduled + runtime
```

## Cross-references
- [[aegis-threat-modeling]] · [[aegis-vulnerability-management]] · [[builder-ci-cd]]
