---
name: atlas-fin-kyc-onboarding
description: KYC onboarding — document validation, liveness check, biometrics, PEP screening, BR + EU. Triggers em "KYC onboarding", "liveness check", "biometric KYC", "Jumio", "Onfido", "Sumsub", "Unico", "PEP screening".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [audit_immutable, sanctions_realtime]
---

# ATLAS-FIN-KYC-ONBOARDING

## Workflow KYC
```
1. Customer initiates signup
2. Document capture (CNH/RG/Passport)
3. Document validation (OCR + authenticity)
4. Liveness check (selfie + face match)
5. Biometric vs doc face
6. PEP + sanctions screening
7. Address validation (proof of address)
8. Risk scoring
9. Onboarding decision (auto/review/reject)
```

## Stack
- **Jumio** — global líder
- **Onfido (now Entrust)** — UK líder
- **Sumsub** — emerging markets focus
- **Unico (BR)** — líder BR (PIX endorsed)
- **Veriff** — emerging markets
- **iDenfy** — mid-market
- **Persona** — developer-friendly

## BR document types
- CNH (Carteira Nacional Habilitação)
- RG (Registro Geral) com CPF
- Passaporte
- CRNM (Carteira Registro Nacional Migratório)

## Liveness check types
- **Passive:** selfie analysis (mais UX-friendly)
- **Active:** turn head, smile, blink (mais seguro)
- **3D depth:** TrueDepth iOS, structured light Android

## Templates
1. KYC flow architecture
2. Document validation rules per country
3. Liveness check UX best practices
4. Risk scoring matrix (auto-approve threshold)
5. Manual review queue + SLA
6. KYC refresh policy (annual high-risk)

## Cross-references
- [[atlas-fin-aml-monitoring]] · [[atlas-fin-sanctions-screening]] · [[nomos-kyc-aml-pt]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-fin-kyc-onboarding** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-fin-kyc-onboarding:**

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
