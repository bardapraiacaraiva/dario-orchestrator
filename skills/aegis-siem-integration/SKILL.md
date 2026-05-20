---
name: aegis-siem-integration
description: SIEM — Splunk, ELK, Sentinel, QRadar, Wazuh. Log aggregation, correlation, detection rules. Triggers em "SIEM", "Splunk", "ELK", "Microsoft Sentinel", "QRadar", "Wazuh", "log aggregation", "correlation rules".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, audit_immutable]
---

# AEGIS-SIEM-INTEGRATION

## Quando usar
- SIEM selection (greenfield ou migration)
- Log source onboarding
- Detection rule writing (Sigma)
- SIEM cost optimization (ingestion)
- Migration: legacy → cloud-native

## Stack
- **Splunk Enterprise / Cloud** — líder histórico
- **Microsoft Sentinel** — cloud-native, líder Azure
- **Elastic SIEM (ELK)** — open-source enterprise
- **IBM QRadar** — enterprise legado
- **Wazuh** — open-source SIEM + XDR
- **Datadog Cloud SIEM** — observability + security
- **Devo / Exabeam / Securonix** — alternatives

## Log sources prioritárias
- **Identity:** AD/Entra ID, Okta auth logs
- **Endpoint:** EDR, Sysmon, audit logs
- **Network:** Firewall, proxy, DNS, NetFlow
- **Cloud:** AWS CloudTrail, GCP Audit Logs, Azure Activity
- **Apps:** Web server, app logs, database audit

## Templates
1. SIEM architecture (collectors → ingestion → storage → analytics)
2. Sigma detection rule library
3. Log source onboarding checklist
4. Cost optimization playbook (filter at source, retention tiering)
5. Detection rule lifecycle (idea → tune → production → retire)

## Detection rules (Sigma)
- Vendor-agnostic format
- Translates to Splunk SPL, KQL (Sentinel), ES Query DSL
- Public rule library: SigmaHQ/sigma

## Cross-references
- [[aegis-soc-operations]] · [[aegis-edr-management]] · [[aegis-cloud-security]]
