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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-zero-trust-architecture** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-zero-trust-architecture:**

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
