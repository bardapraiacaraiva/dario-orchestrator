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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-iam-identity** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-iam-identity:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->
