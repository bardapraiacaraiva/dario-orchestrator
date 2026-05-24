---
name: atlas-fin-open-banking-br
description: Open Finance BR — Bacen APIs, consent management, data sharing, fases. Triggers em "Open Banking BR", "Open Finance", "Bacen API", "consent management", "compartilhamento dados", "BCB 1300".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [bcb_compliance_gate, audit_immutable]
jurisdiction: Brasil
---

# ATLAS-FIN-OPEN-BANKING-BR

## Marco
- **Resolução BCB 32/2020** + **Resolução Conjunta BCB/CMN 1/2020**
- **Lei 14.063/2020** — assinaturas eletrônicas
- **LGPD Art. 7-11** — base legal
- **API specs Bacen** — versão atual

## Fases Open Finance BR
- **Fase 1:** dados produtos institucionais (concluído 2021)
- **Fase 2:** dados pessoais (consentido) — concluído 2021
- **Fase 3:** iniciação pagamentos + investimentos — concluído 2022
- **Fase 4:** mais dados (seguros, câmbio, previdência) — em curso 2025+

## Quando usar
- Fintech autorização Bacen (S1-S5 segmentação)
- API integration consent + data sharing
- ITP (Iniciador Transação Pagamento) implementation
- AISP (Account Information Service Provider) equivalente BR

## Templates
1. Open Finance maturity assessment
2. API integration architecture
3. Consent management workflow
4. ITP authorization request Bacen
5. Customer journey consent UX
6. Data lifecycle + retention policy

## Cross-references
- [[atlas-fin-pix-rules-bcb]] · [[nomos-psd2-open-banking-pt]] · [[atlas-fin-regulatory-reporting-bcb]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-fin-open-banking-br** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-fin-open-banking-br:**

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
