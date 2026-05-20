---
name: aegis-zero-trust-architecture
description: Zero Trust — NIST SP 800-207, BeyondCorp, ZTNA, segmentation, conditional access. Triggers em "zero trust", "ZTNA", "BeyondCorp", "NIST 800-207", "microsegmentation", "conditional access".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit]
---

# AEGIS-ZERO-TRUST-ARCHITECTURE

## Filosofia
**Never trust, always verify.** Identity + device + context + continuous validation.

## Marco
- **NIST SP 800-207** — Zero Trust Architecture
- **NIST SP 1800-35** — implementação
- **DoD ZT Reference Architecture**
- **BeyondCorp (Google)** — early reference

## 7 tenets NIST
1. Todos data sources + services são resources
2. Comunicação secured regardless of network
3. Acesso per-session
4. Acesso determined by dynamic policy
5. Monitor integrity + security posture
6. Authn/authz dynamic + strictly enforced
7. Coleta data sobre asset/network/comms

## Quando usar
- Migration: VPN → ZTNA
- Hybrid work secure access
- Microsegmentation (data center)
- Conditional access (Entra ID, Okta)
- M&A integration sem network full mesh

## Stack
- **ZTNA:** Cloudflare Access, Zscaler ZPA, Netskope, Twingate
- **Microsegmentation:** Illumio, Akamai Guardicore
- **Identity:** Okta, Entra ID, Auth0, JumpCloud
- **SASE:** Zscaler, Netskope, Palo Alto Prisma, Cisco Umbrella

## Templates
1. ZT maturity assessment (CISA ZTMM)
2. Identity-first access policy
3. Microsegmentation strategy (east-west)
4. Conditional access playbook (device + location + risk)
5. Migration plan VPN → ZTNA

## Cross-references
- [[aegis-iam-identity]] · [[aegis-cloud-security]] · [[nexus-network]]
