---
name: nomos-psd2-open-banking-pt
description: PSD2 + Open Banking PT — Strong Customer Authentication (SCA), TPP authorization, account info services, payment initiation. Triggers em "PSD2", "Open Banking PT", "SCA", "Strong Customer Authentication", "TPP", "AIS", "PIS", "PSD3".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [bdp_regulatory_reporting_gate, audit_immutable]
jurisdiction: Portugal + EU
---

# NOMOS-PSD2-OPEN-BANKING-PT

## Marco
- **Directive (EU) 2015/2366 (PSD2)** — Payment Services Directive 2
- **DL 91/2018** — transposição PT
- **RTS on SCA & CSC** (Regulation 2018/389)
- **PSD3 + PSR proposals (2023)** — under discussion, applicable 2026-2027
- **eIDAS 2** + **Digital Identity Wallet** — convergence
- **PT Open Banking** — implementação BdP

## TPP types (Third-Party Providers)
- **AISP (Account Info Service Provider):** read access, no payments
- **PISP (Payment Initiation Service Provider):** initiate payments from user account
- **CBPII (Card-Based Payment Instrument Issuer):** confirm funds availability

## SCA (Strong Customer Authentication)
- **Two factors required:** knowledge + possession + inherence
- **Exemptions:** low-value (<€30), recurring, MOTO, trusted beneficiaries, TRA (Transaction Risk Analysis)

## Quando usar
- TPP authorization BdP (AISP/PISP/CBPII)
- Bank API setup (PSD2 compliant XS2A interface)
- SCA implementation + UX optimization
- Open Banking commercial APIs (Premium APIs beyond PSD2)
- PSD3 readiness assessment

## Templates
1. TPP authorization application BdP
2. XS2A API specification (Berlin Group / STET / Open Banking UK)
3. SCA exemption decision tree
4. Consent management framework
5. Fallback mechanism for API outages
6. Premium API pricing model (beyond regulated)
7. PSD3 gap analysis (vs current PSD2)

## Cross-references
- [[nomos-bdp-banking-pt]] · [[atlas-fin-open-banking-br]] · [[atlas-fin-psd2-eu]] · [[aegis-iam-identity]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-psd2-open-banking-pt** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-psd2-open-banking-pt:**

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
