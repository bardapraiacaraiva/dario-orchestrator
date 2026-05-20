---
name: aegis-secrets-management
description: Secrets management — HashiCorp Vault, AWS Secrets Manager, age, sops, secret rotation. Triggers em "secrets management", "HashiCorp Vault", "AWS Secrets Manager", "age", "sops", "secret rotation".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, audit_immutable]
---

# AEGIS-SECRETS-MANAGEMENT

## Quando usar
- Secret sprawl (passwords em config, .env não-encrypted)
- Rotation automatizada
- GitHub secret leaks remediation
- Multi-cloud secret federation
- Service-to-service auth (mTLS, dynamic)

## Stack
- **HashiCorp Vault** — gold standard
- **AWS Secrets Manager + Parameter Store**
- **GCP Secret Manager**
- **Azure Key Vault**
- **Doppler / Infisical** (developer-friendly)
- **age + sops** (file-encryption for GitOps)
- **1Password Connect** (team-friendly)

## Princípios
- **Never in code:** secret detection CI gate (gitleaks, trufflehog)
- **Rotate frequently:** API keys 90d, certs 1y, root credentials immediate-on-personnel-change
- **Audit access:** quem leu que secret quando
- **Dynamic secrets:** generated on-demand, short TTL
- **Encryption in transit + at rest**

## Templates
1. Secret management policy
2. Vault deployment (HA + auto-unseal)
3. Rotation automation playbook
4. Secret scanning CI integration (gitleaks pre-commit + CI)
5. Migration plan: .env → Vault
6. Service-to-service mTLS via Vault PKI

## Compliance
- ✓ PCI-DSS 8.3 — separate password store
- ✓ ISO 27001 A.9.4.5 — strong authentication
- ✓ SOC 2 CC6.1 — logical access controls

## Cross-references
- [[aegis-iam-identity]] · [[aegis-secure-sdlc]] · [[aegis-cloud-security]]
