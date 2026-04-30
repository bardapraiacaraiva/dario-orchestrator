---
name: nexus-iam
description: "IAM — RBAC, SSO/SAML, MFA enforcement, access reviews, least privilege, identity governance"
version: "1.0"
---

# NEXUS-IAM: Identity & Access Management Skill

## When to Activate

**Trigger words (PT):** iam, controlo de acesso, rbac, sso, mfa, autenticacao, autorizacao, privilegios, revisao de acessos, identidade, principio do menor privilegio, active directory
**Trigger words (EN):** iam, access control, rbac, sso, saml, mfa, authentication, authorization, privileges, access review, identity, least privilege, active directory, oauth, oidc, zero trust

## Step-by-Step Workflow

### Phase 1: Identity Inventory
1. Inventory all identity providers: Active Directory, Entra ID, Okta, Auth0, Google Workspace
2. Catalog all systems and applications requiring access control
3. Map user types: employees, contractors, service accounts, API keys, third-party
4. Document current authentication methods per system
5. Identify orphaned accounts (no owner, inactive >90 days)
6. Count privileged accounts (admin, root, service accounts with elevated access)

### Phase 2: RBAC Design
1. Define role hierarchy aligned with organizational structure
2. Standard roles: viewer, editor, admin, super-admin (avoid per-user permissions)
3. Map roles to permissions per application/system
4. Implement role assignment workflow: request -> approve -> provision -> review
5. Separation of duties: conflicting roles cannot be held simultaneously
6. Service account roles: minimal, documented, rotated credentials

### Phase 3: SSO/SAML Implementation
1. Select IdP: Entra ID, Okta, Google Workspace, Keycloak
2. Integrate all applications via SAML 2.0 or OIDC
3. Centralized authentication eliminates password sprawl
4. Just-in-time (JIT) provisioning for SAML-connected apps
5. Session management: timeout, re-authentication for sensitive operations
6. SSO coverage target: >95% of all applications

### Phase 4: MFA Enforcement
1. MFA mandatory for all users (no exceptions for convenience)
2. Preferred methods (in order): hardware key (FIDO2) > authenticator app (TOTP) > push notification > SMS (last resort)
3. MFA for all admin/privileged access (mandatory, hardware key preferred)
4. Conditional access policies: MFA required for external access, new devices, sensitive operations
5. Recovery procedure: backup codes, admin reset with identity verification
6. Phishing-resistant MFA: FIDO2/WebAuthn for high-value targets

### Phase 5: Access Reviews
1. Quarterly access reviews for privileged accounts
2. Semi-annual access reviews for standard accounts
3. Review process: manager certifies access, remove if not justified
4. Automated detection: accounts inactive >90 days flagged for deactivation
5. Joiner-Mover-Leaver (JML) process:
   - **Joiner**: provision access based on role, day-1 ready
   - **Mover**: adjust access when changing role/department
   - **Leaver**: revoke all access within 24h of departure
6. Track review completion rates and remediation actions

### Phase 6: Governance & Monitoring
1. Privileged Access Management (PAM): just-in-time elevation, session recording
2. API key management: rotation schedule, scope limitation, usage monitoring
3. Authentication logs: centralized, monitored for anomalies
4. Impossible travel detection, brute force alerts, credential stuffing detection
5. Compliance reporting: access matrix, privileged account report, MFA adoption
6. Annual IAM program review and maturity assessment

## Commands Table

| Command | Description |
|---------|-------------|
| `nexus iam audit` | Full IAM posture assessment |
| `nexus iam rbac` | RBAC design template |
| `nexus iam sso` | SSO integration checklist |
| `nexus iam mfa` | MFA enforcement policy and rollout plan |
| `nexus iam review` | Access review procedure and template |
| `nexus iam jml` | Joiner-Mover-Leaver process design |
| `nexus iam pam` | Privileged access management setup |
| `nexus iam report` | IAM metrics dashboard |

## Output Template

```markdown
# IAM Assessment — [Organization]
**Date:** YYYY-MM-DD | **IdP:** [Entra ID/Okta/etc.] | **Total Users:** X

## 1. Identity Overview
| Category | Count | MFA Enabled | SSO Integrated | Last Review |
|----------|-------|-------------|----------------|-------------|
| Employees | | | | |
| Contractors | | | | |
| Service accounts | | N/A | | |
| API keys | | N/A | | |

## 2. MFA Coverage
| Method | Users | % |
|--------|-------|---|
| FIDO2/Hardware | | |
| Authenticator app | | |
| Push notification | | |
| SMS | | |
| None | | |
| **Total MFA adoption** | | **%** |

## 3. SSO Coverage
| Application | SSO | Protocol | Notes |
|------------|-----|----------|-------|

## 4. Privileged Accounts
| Account | System | Type | Last Review | MFA | Risk |
|---------|--------|------|-------------|-----|------|

## 5. Access Review Status
| Scope | Due Date | Completed | Revocations | % Complete |
|-------|----------|-----------|-------------|-----------|

## 6. Recommendations
| # | Finding | Risk | Action | Priority |
|---|---------|------|--------|----------|

## 7. Next Review: YYYY-MM-DD
```

## Red Flags

- No MFA enforced (especially for admin accounts)
- Shared admin credentials between team members
- No access reviews conducted in >12 months
- Orphaned accounts (ex-employees with active access)
- Service accounts with admin privileges and no rotation
- Applications not integrated with SSO (standalone passwords)
- No JML process (access not revoked on departure)
- API keys without expiration or rotation
- No PAM solution for privileged access
- Root/admin accounts used for daily operations
- SMS as primary MFA method (SIM swap vulnerable)
- No logging or monitoring of authentication events
