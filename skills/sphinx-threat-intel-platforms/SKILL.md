---
name: sphinx-threat-intel-platforms
description: TIP — MISP, ThreatConnect, Anomali, strategic/tactical/operational intel. Triggers em "threat intel platform", "TIP", "MISP", "ThreatConnect", "Anomali", "Recorded Future", "Mandiant Advantage", "STIX TAXII".
license: SEE-LICENSE
parent_agent: sphinx-director
compliance: [audit_immutable, classified_handling]
---

# SPHINX-THREAT-INTEL-PLATFORMS

## Intel levels
- **Strategic:** geopolitical, industry trends (CEO/board audience)
- **Operational:** campaign-level, threat actor groups (security manager)
- **Tactical:** TTPs (techniques, tactics, procedures) (SOC analyst)
- **Technical:** IOCs (hashes, IPs, domains) (automated tools)

## Stack
- **MISP** — open-source standard, IOC sharing
- **ThreatConnect** — commercial líder
- **Anomali ThreatStream** — enterprise
- **Recorded Future** — automated collection
- **Mandiant Advantage** — Google + Mandiant intel
- **CrowdStrike Falcon Intelligence**
- **Tidal Cyber** — community ATT&CK navigator

## Standards
- **STIX 2.1** — Structured Threat Information Expression
- **TAXII 2.1** — Trusted Automated Exchange
- **OpenIOC** — older Mandiant format
- **MITRE ATT&CK Navigator**

## Templates
1. TIP deployment architecture
2. Intel requirements management (PIRs)
3. Producer-consumer model
4. Indicator lifecycle (TTL, scoring)
5. Strategic intel report (quarterly)
6. ISAC participation framework

## Cross-references
- [[sphinx-osint-investigations]] · [[sphinx-advanced-persistent-threat]] · [[aegis-soc-operations]]
