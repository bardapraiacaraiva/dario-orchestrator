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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-secrets-management** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-secrets-management:**

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
