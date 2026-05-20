---
name: aegis-cloud-security
description: Cloud security — CSPM, CWPP, CIEM, CNAPP. Wiz, Lacework, Prisma Cloud, Orca. Triggers em "cloud security", "CSPM", "CWPP", "CIEM", "CNAPP", "Wiz", "Lacework", "Prisma Cloud", "Orca Security".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, soc2_type2]
---

# AEGIS-CLOUD-SECURITY

## Quando usar
- Multi-cloud security posture (AWS+Azure+GCP)
- Cloud-native app security (containers, serverless)
- Compliance em cloud (PCI, HIPAA on AWS)
- IAM cloud (over-permissioned roles)
- Cloud incident response

## Categorias tools
- **CSPM (Cloud Security Posture Management):** misconfigurations
- **CWPP (Cloud Workload Protection):** runtime workloads
- **CIEM (Cloud Infrastructure Entitlement Mgmt):** identity + privileges
- **CNAPP (Cloud-Native App Protection):** CSPM + CWPP + CIEM unified
- **SaaS Security:** SSPM (SaaS Security Posture Mgmt)

## Stack
- **Wiz** — líder CNAPP, agentless
- **Palo Alto Prisma Cloud** — enterprise líder
- **Lacework** — strong analytics
- **Orca Security** — agentless deep scan
- **Cloud-native:** AWS Security Hub, Azure Defender, GCP SCC
- **CIEM:** Sonrai, Ermetic (now Tenable Cloud)

## Templates
1. Cloud security baseline (per provider — CIS Benchmark-aligned)
2. IAM least-privilege audit (over-permissioned roles)
3. Container security pipeline (Trivy + admission controller)
4. Serverless security (functions over-permissioned?)
5. K8s security (Pod Security Standards + NetworkPolicy)
6. Cloud incident response runbook (AWS account compromise)

## Cross-references
- [[aegis-vulnerability-management]] · [[aegis-zero-trust-architecture]] · [[nexus-cloud]]
