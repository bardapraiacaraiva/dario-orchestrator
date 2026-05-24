---
name: atlas-fin-psd2-eu
description: PSD2 EU implementation — SCA, XS2A, TPP, EBA RTS. Triggers em "PSD2", "PSD2 EU", "SCA EU", "XS2A", "Berlin Group", "STET", "Open Banking UK".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [ecb_compliance_gate, audit_immutable]
jurisdiction: EU
---

# ATLAS-FIN-PSD2-EU

(See also [[nomos-psd2-open-banking-pt]] for PT-specific transposição)

## Marco
- **Directive (EU) 2015/2366 (PSD2)**
- **RTS on SCA & CSC (EU 2018/389)**
- **Open Banking UK** (CMA standard, post-Brexit)
- **PSD3 + PSR proposals (2023)** — em discussão
- **eIDAS 2 + EU Digital Identity Wallet**

## TPP types
- **AISP** — read-only account info
- **PISP** — payment initiation
- **CBPII** — card-based payment instrument issuer
- **ASPSP** — Account Servicing Payment Service Provider (banks)

## XS2A interface options
- **Berlin Group NextGen PSD2** — most adopted EU
- **STET (France)** — alternative
- **Open Banking UK Standard** — UK-focused

## SCA exemptions
- Low-value < €30
- Recurring transactions
- Trusted beneficiaries (whitelist)
- Corporate payments via secure protocols
- TRA (Transaction Risk Analysis) ≤ €500

## Templates
1. TPP authorization application (national regulator)
2. XS2A API spec (Berlin Group)
3. SCA exemption decision tree
4. Consent management framework
5. Fallback mechanism (when bank API down)
6. PSD3 readiness assessment

## Cross-references
- [[nomos-psd2-open-banking-pt]] · [[atlas-fin-open-banking-br]] · [[aegis-iam-identity]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-fin-psd2-eu** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-fin-psd2-eu:**

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
