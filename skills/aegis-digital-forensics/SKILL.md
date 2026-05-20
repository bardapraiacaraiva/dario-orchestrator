---
name: aegis-digital-forensics
description: Digital forensics — disk imaging, memory analysis, network forensics, mobile forensics. Triggers em "digital forensics", "FTK", "Autopsy", "Volatility", "memory forensics", "Wireshark forensics".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [audit_immutable, chain_of_custody]
---

# AEGIS-DIGITAL-FORENSICS

## Quando usar
- Post-breach investigation
- Insider threat investigation
- Legal hold + e-discovery
- Mobile forensics
- Cloud forensics

## Stack
- **Disk imaging:** FTK Imager, dd, dc3dd
- **Disk analysis:** Autopsy (open-source), FTK, EnCase, X-Ways
- **Memory:** Volatility 3, Rekall, MemProcFS
- **Network:** Wireshark, NetworkMiner, Zeek
- **Mobile:** Cellebrite, Magnet AXIOM
- **Cloud:** AWS GuardDuty + CloudTrail, Magnet AXIOM Cyber

## Princípios
- **Chain of custody mandatory**
- **Write-blockers** ao copiar disk
- **Hash everything** (MD5 + SHA-256 mínimo)
- **Documentation extensive** (cada step)
- **Trained personnel** (court-defensible)

## Templates
1. Chain of custody form
2. Forensic image acquisition SOP
3. Memory analysis playbook (Volatility + common artifacts)
4. Network forensics workflow (Zeek + logs)
5. Final report template (executive + technical + appendix)
6. Cloud forensics (AWS/Azure/GCP)

## Compliance
- ✓ Evidence court-admissible
- ✓ LGPD specific care (PII em evidence)
- ✓ ISO 27037 — Identification, collection, acquisition

## Cross-references
- [[aegis-incident-response]] · [[aegis-soc-operations]] · [[lex-criminal]]
