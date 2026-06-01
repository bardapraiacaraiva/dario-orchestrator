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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-cloud-security** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-cloud-security:**

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
