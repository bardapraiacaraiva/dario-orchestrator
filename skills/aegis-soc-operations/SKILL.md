---
name: aegis-soc-operations
description: SOC operations — MITRE ATT&CK, detection engineering, alert triage, MTTR optimization. Triggers em "SOC", "Security Operations Center", "MITRE ATT&CK", "detection engineering", "SOAR", "alert triage".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, audit_immutable]
---

# AEGIS-SOC-OPERATIONS

## Quando usar
- SOC greenfield setup
- Detection engineering program
- Alert fatigue mitigation
- MTTR/MTTD improvement
- Tier 1/2/3 SOC structure

## Frameworks
- **MITRE ATT&CK** — adversary tactics + techniques (matrix)
- **MITRE D3FEND** — defensive countermeasures
- **Lockheed Cyber Kill Chain** — 7 stages
- **Pyramid of Pain (Bianco):** hash → IP → domain → tools → TTP
- **Diamond Model:** adversary / capability / infrastructure / victim

## SOC tiers
- **Tier 1:** triagem inicial, escalation (90% volume, 10% complexity)
- **Tier 2:** investigation + containment
- **Tier 3:** advanced threat hunting + IR
- **SOC Manager:** runbook + metrics

## Templates
1. Detection use case library (ATT&CK-mapped)
2. Detection engineering SDLC (idea → develop → test → deploy → tune)
3. Alert triage SOP (SOAR-ready)
4. SOC metrics dashboard (MTTD/MTTR/FP rate)
5. Threat hunting hypotheses + IOAs (Indicators of Attack)

## Métricas
- **MTTD:** Mean Time To Detect
- **MTTR:** Mean Time To Respond
- **False Positive rate:** <5% target
- **Coverage:** % ATT&CK techniques detected
- **Dwell time:** attacker presence before detection

## Cross-references
- [[aegis-siem-integration]] · [[aegis-edr-management]] · [[aegis-incident-response]]
