---
name: nomos-kyc-aml-pt
description: KYC/AML PT — UIF Portugal, Lei 83/2017, beneficial ownership, SARs, sanctions screening. Triggers em "KYC", "AML PT", "UIF", "Lei 83/2017", "beneficiário efectivo", "RCBE", "branqueamento capitais", "AMLD6".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [audit_immutable]
jurisdiction: Portugal + EU
---

# NOMOS-KYC-AML-PT

## Marco
- **Lei 83/2017** — Prevenção BC/FT (transposição AMLD4/5)
- **DL 27/2024** — actualização AMLD5
- **Lei 89/2017** — RCBE (Registo Central Beneficiário Efectivo)
- **AMLD6 (Directive (EU) 2024/1640)** — applicable July 2027
- **AML Package (Regulation 2024/1624)** — directly applicable
- **EU AML Authority (AMLA)** — operational 2025+, based in Frankfurt

## Entidades obrigadas (Art. 3 Lei 83/2017)
- Instituições financeiras (bancos, seguradoras, fundos)
- Sociedades fiduciárias e gestoras de fundos
- Notários, advogados, contabilistas (atividades específicas)
- Empresas leilões, antiguidades, alta gama
- Casinos + apostas online
- VASPs (Virtual Asset Service Providers — crypto)
- Imobiliárias (transações > €10K cash)

## Workflow KYC
```
1. Customer identification (ID, address, beneficial owners)
2. Risk classification (low/medium/high)
3. Customer Due Diligence (CDD) ou Enhanced (EDD)
4. Sanctions screening (UN, EU, OFAC, BdP lists)
5. PEP screening
6. Ongoing monitoring + transaction monitoring
7. SAR (Suspicious Activity Report) → UIF if needed
8. Recordkeeping (7 years)
```

## RCBE obrigatório
- Pessoas colectivas portuguesas
- Inscrição RCBE até 30 dias após constituição
- Atualização sempre que muda beneficiário efectivo
- Sanção falta inscrição: até €50.000

## Templates
1. KYC/CDD onboarding form (PF + PJ)
2. EDD high-risk + PEP procedures
3. Sanctions screening workflow (OFAC + EU + UN)
4. Transaction monitoring scenarios (typical 30-50 rules)
5. SAR template UIF
6. RCBE submission template
7. AML training curriculum (annual)
8. AML risk assessment institutional

## Cross-references
- [[nomos-anti-fraude-pt]] · [[nomos-bdp-banking-pt]] · [[atlas-fin-kyc-onboarding]] · [[atlas-fin-aml-monitoring]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-kyc-aml-pt** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-kyc-aml-pt:**

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
