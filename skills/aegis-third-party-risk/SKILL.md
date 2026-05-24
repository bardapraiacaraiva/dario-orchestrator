---
name: aegis-third-party-risk
description: Third-Party Risk Management (TPRM) — vendor security assessment, SIG/SIG Lite, SOC 2 review, continuous monitoring. Triggers em "third party risk", "TPRM", "vendor risk", "SIG questionnaire", "SOC 2 review", "vendor assessment", "supply chain risk".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, soc2_type2, audit_immutable]
---

# AEGIS-THIRD-PARTY-RISK

## Quando usar
- TPRM program greenfield (vendors >50)
- Vendor onboarding security review
- Critical vendor annual reassessment
- M&A vendor inventory + risk
- Incident em vendor (response coordination)

## Frameworks
- **SIG / SIG Lite (Shared Assessments):** standard questionnaire
- **CAIQ (CSA):** Consensus Assessments Initiative
- **HECVAT** (higher ed-focused)
- **NIST SP 800-161:** Supply Chain Risk Management
- **ISO 27036:** supplier relationships

## Tipos de vendor
- **Critical:** access to crown jewels (production data, PII massa)
- **High:** material business dependency (SaaS líder)
- **Medium:** moderate access ou criticality
- **Low:** no sensitive data, easily replaceable

## Stack
- **Drata Trust** — automated TPRM
- **OneTrust Vendorpedia / Whistic**
- **ProcessUnity / Prevalent**
- **BitSight / SecurityScorecard** — continuous monitoring (external posture)
- **UpGuard** — combined questionnaire + continuous

## Templates
1. Vendor risk classification rubric (Critical/High/Medium/Low)
2. SIG Lite questionnaire (45 questions baseline)
3. Critical vendor deep dive (SOC 2 + pentest report + SBOM review)
4. Continuous monitoring setup (BitSight/SecurityScorecard)
5. Vendor incident playbook (their breach → our exposure)
6. Vendor offboarding checklist (data destruction certification)

## Compliance
- ✓ ISO 27001 A.15 — Supplier relationships
- ✓ SOC 2 CC9 — Risk Mitigation
- ✓ LGPD Art. 39 — Operator obligations
- ✓ NIS2 (EU) supply chain requirements

## Cross-references
- [[aegis-compliance-frameworks]] · [[aegis-supply-chain-security]] · [[risco-terceiros]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-third-party-risk** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-third-party-risk:**

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
