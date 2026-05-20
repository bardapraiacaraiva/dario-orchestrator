---
name: aegis-incident-response
description: Incident Response — NIST SP 800-61, playbooks, tabletop exercises, communication. Triggers em "incident response", "IR", "NIST 800-61", "playbook", "tabletop", "breach response", "ransomware response".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, audit_immutable, lgpd_security_marker]
---

# AEGIS-INCIDENT-RESPONSE

## Marco
- **NIST SP 800-61 Rev 2** — Computer Security IR Handbook
- **ISO 27035** — IR management
- **SANS PICERL** — Prep/Identify/Contain/Eradicate/Recover/Lessons
- **MITRE Threat-Informed Defense**

## Quando usar
- IR plan from scratch
- Active incident in progress
- Tabletop exercises
- Post-incident review
- Ransomware response
- Data breach (LGPD/GDPR communication ≤72h)

## NIST IR lifecycle
1. **Preparation:** team + tools + comms + retainer
2. **Detection & Analysis:** triagem + scope
3. **Containment & Eradication:** stop bleeding
4. **Recovery:** restore + verify clean
5. **Post-Incident:** lessons learned + improve

## Templates
1. IR plan + playbooks (ransomware, BEC, data breach, account compromise)
2. Tabletop exercise scenarios
3. Breach communication template (LGPD ANPD 72h)
4. Chain of custody form
5. Post-mortem template
6. IR retainer SOW (external firm)

## Comms
- **Internal:** IR team Slack channel + war room
- **Executive:** updates 2-4h cadence durante incident
- **Legal:** counsel envolvido cedo
- **Regulators:** ANPD (LGPD), SEC (US), DPA (GDPR)
- **Customers:** factual + timeline + mitigation

## Cross-references
- [[aegis-digital-forensics]] · [[aegis-soc-operations]] · [[risco-bcp]]
