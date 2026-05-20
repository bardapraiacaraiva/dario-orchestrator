---
name: aegis-iam-identity
description: IAM — Okta, Entra ID, Auth0, Keycloak, RBAC/ABAC, PAM, MFA. Triggers em "IAM", "Okta", "Entra ID", "Auth0", "Keycloak", "RBAC", "ABAC", "MFA", "SSO", "PAM".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, lgpd_security_marker]
---

# AEGIS-IAM-IDENTITY

## Quando usar
- IAM greenfield (workforce + customer)
- Migration AD on-prem → Entra ID hybrid
- B2B identity federation
- CIAM (Customer IAM) setup
- PAM (Privileged Access) program

## Stack workforce
- **Microsoft Entra ID** (ex-Azure AD)
- **Okta Workforce Identity**
- **JumpCloud** (SMB-friendly)
- **Google Workspace + Cloud Identity**
- **Ping Identity**

## Stack CIAM (customers)
- **Auth0 (Okta)**
- **Amazon Cognito**
- **Microsoft Entra External ID**
- **Frontegg**
- **Stytch**
- **Keycloak** (open-source self-host)

## Frameworks
- **RBAC:** Role-Based Access Control (escalável)
- **ABAC:** Attribute-Based (mais granular, complexo)
- **PBAC:** Policy-Based (XACML, OPA)
- **ReBAC:** Relationship-Based (Zanzibar)
- **JIT (Just-In-Time):** privilege only when needed

## Templates
1. IAM architecture (identities + sources of truth + AuthN/Z)
2. RBAC role design (least privilege)
3. MFA rollout playbook (TOTP → FIDO2 → passkeys)
4. PAM workflow (privileged session recording + approval)
5. SCIM provisioning automation
6. SSO via SAML2 / OIDC integration patterns

## Princípios
- **Least privilege** padrão
- **MFA mandatory** para admins
- **Passkeys > TOTP > SMS**
- **Joiner/Mover/Leaver** automation
- **Quarterly access reviews**

## Cross-references
- [[aegis-zero-trust-architecture]] · [[aegis-secrets-management]] · [[nexus-iam]]
