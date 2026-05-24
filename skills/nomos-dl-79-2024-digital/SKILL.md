---
name: nomos-dl-79-2024-digital
description: DL 79/2024 + digital transition PT — e-fatura, SAF-T, Portal Único Empresa, IES, declaração inventário. Triggers em "DL 79/2024", "e-fatura", "SAF-T PT", "Portal Único", "IES", "ATCUD", "Modelo 22 PT", "factura electrónica".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [audit_immutable]
jurisdiction: Portugal
---

# NOMOS-DL-79-2024-DIGITAL

## Marco
- **DL 79/2024** — transição digital empresarial PT (Set 2024)
- **DL 28/2019** — facturação electrónica mandatory pública
- **Portaria 195/2020** — comunicação facturas AT
- **Portaria 363/2010** — SAF-T (Standard Audit File-Tax)
- **DL 198/2012** — comunicação cliente final
- **Despacho 12541/2024** — ATCUD novos formatos
- **Lei 7/2009 CIRE** — Código Insolvência (e-publicação)

## Quando usar
- Implementação e-fatura B2G (governo) — obrigatório 2024+
- B2B / B2C invoice software certification AT
- SAF-T mensal upload AT
- ATCUD em todas faturas
- IES (Informação Empresarial Simplificada) anual
- Modelo 22 IRC submission
- Portal Único Empresa (one-stop shop empresarial)

## E-fatura B2G timeline
- 2021: grandes empresas → AP central
- 2023: PMEs → AP central
- 2024+: full mandatory todos
- B2B: voluntary (becoming standard 2025+)

## Templates
1. Software facturação AT certification process
2. SAF-T monthly upload checklist
3. ATCUD format validation
4. E-fatura B2G integration AP
5. IES annual submission template
6. Modelo 22 IRC pre-fill
7. Portal Único integration (one-time setup empresa)
8. Digital records retention (10 anos AT)

## Coimas (RGIT)
- Não emissão factura: €375-3.750
- SAF-T atraso: €450-4.500
- IES atraso: €375-22.500

## Cross-references
- [[conta-facturacao]] · [[conta-iva]] · [[conta-irc]] · [[lex-tributario]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-dl-79-2024-digital** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-dl-79-2024-digital:**

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
