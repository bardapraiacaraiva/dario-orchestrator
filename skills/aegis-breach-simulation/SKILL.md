---
name: aegis-breach-simulation
description: Breach & Attack Simulation (BAS) — AttackIQ, SafeBreach, Picus, MITRE Caldera, Atomic Red Team. Triggers em "BAS", "breach simulation", "AttackIQ", "SafeBreach", "Picus", "Caldera", "Atomic Red Team", "purple team", "continuous validation".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, audit_immutable, responsible_disclosure]
---

# AEGIS-BREACH-SIMULATION

## Filosofia
**Continuous validation > point-in-time pentest.** BAS runs ATT&CK techniques diariamente, validates detection coverage.

## Quando usar
- Validate detection coverage (qual % ATT&CK detectamos?)
- Purple team continuous engagement
- Post-breach validation (gap closed?)
- Annual control attestation (compliance evidence)
- M&A integration (security maturity)

## BAS vs Pentest vs Red Team
| | BAS | Pentest | Red Team |
|---|---|---|---|
| Frequência | Continuous | Annual | Quarterly |
| Scope | Detection coverage | Vulnerabilities | Objective-based |
| Automation | High | Low | Low-Medium |
| Cost | $$ subscription | $$ engagement | $$$ engagement |

## Stack
- **AttackIQ Platform** — enterprise líder BAS
- **SafeBreach** — enterprise BAS
- **Picus Security** — BAS + Security Validation
- **Mandiant Security Validation** (ex-Verodin)
- **MITRE Caldera** — open-source BAS framework
- **Atomic Red Team (Red Canary)** — open-source ATT&CK tests
- **Cymulate** — BAS platform

## Templates
1. BAS program design (purple team operating model)
2. ATT&CK coverage matrix (technique × detection × response)
3. Atomic Red Team test execution playbook
4. Caldera adversary emulation campaign
5. Quarterly BAS report (coverage trend + gaps + fixes)
6. Purple team tabletop scenarios

## Métricas
- **ATT&CK coverage:** % techniques detected
- **MTTD trend:** Mean Time to Detect (improving?)
- **Defense efficacy:** % simulated attacks detected
- **False positive rate:** detections that fired but shouldn't

## Compliance
- ✓ ISO 27001 A.12.6.1 — Vuln management
- ✓ SOC 2 CC7.1 — System operations monitoring
- ✓ PCI-DSS 11.4 — Network IDS/IPS testing
- ✓ NIST CSF DE.CM — Continuous monitoring

## Cross-references
- [[aegis-pentest-methodology]] · [[aegis-soc-operations]] · [[aegis-threat-modeling]]
