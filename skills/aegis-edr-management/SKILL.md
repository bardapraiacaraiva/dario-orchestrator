---
name: aegis-edr-management
description: EDR/XDR — CrowdStrike Falcon, SentinelOne, Microsoft Defender, Cortex XDR. Triggers em "EDR", "XDR", "CrowdStrike", "SentinelOne", "Defender for Endpoint", "Cortex XDR", "endpoint detection".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit]
---

# AEGIS-EDR-MANAGEMENT

## Quando usar
- EDR selection (greenfield)
- Migration legacy AV → modern EDR
- Detection tuning (false positives)
- Threat hunting via EDR data
- Containment workflows

## Stack
- **CrowdStrike Falcon** — líder Gartner
- **SentinelOne Singularity** — autonomous AI
- **Microsoft Defender for Endpoint** — bundled Microsoft
- **Palo Alto Cortex XDR** — XDR completo
- **SophosLabs Intercept X**
- **Trend Micro Vision One**
- **Bitdefender GravityZone**
- **Open-source:** Wazuh, Velociraptor

## Templates
1. EDR selection scorecard (detection + cost + management + integration)
2. Onboarding playbook (deploy + tune + train)
3. Detection tuning workflow (FP analysis + suppression)
4. EDR-based threat hunting queries
5. Containment playbook (isolate, kill process, evict)

## Princípios
- **Don't block silently:** alert humano antes de block
- **Allowlist obrigatória:** dev tools, scripts internos
- **Tune progressively:** 30/60/90d ramp-up
- **Network containment:** EDR pode isolar host
- **Integrar com SIEM:** raw events para correlação

## Cross-references
- [[aegis-soc-operations]] · [[aegis-incident-response]] · [[aegis-cloud-security]]
