---
name: kirion-fii-br
description: FIIs BR — types, CVM regulação, liquidez, taxation, screening. Triggers em "FII", "FII BR", "fundo imobiliário", "CVM 175", "dividend tax exempt FII", "FII tijolo papel".
license: SEE-LICENSE
parent_agent: kirion-director
compliance: [cvm_compliance, anbima_alignment]
jurisdiction: Brasil
---

# KIRION-FII-BR

## Marco
- **Lei 8.668/93** — institui FIIs
- **CVM Resolução 175** (2023) — novo marco fundos
- **CVM Instrução 472** (antiga) — supletivamente aplicável
- **Lei 11.033/2004 Art. 3, III:** isenção IR para PF dividendos (50%+ cotistas, >50 cotistas, ≥ 95% pagamento)

## Tipos FII
- **Tijolo (Equity):** direct property (logística, shopping, lajes)
- **Papel (Debt):** CRIs, LCIs (mortgage-backed)
- **FoF (Fund of Funds):** investe em outros FIIs
- **Híbrido:** mix tijolo + papel
- **Desenvolvimento:** greenfield projects

## Segmentos top
- **Logística:** XPLG, HGLG, BTLG (institutional storage)
- **Lajes corporativas:** HGRE, JSRE, PVBI (office)
- **Shoppings:** XPML, HGBS (retail)
- **Residencial:** poucos puros (RBRP, JFLL)
- **Híbridos top:** BTCR, KNRI

## Métricas screening
- **DY (Dividend Yield):** 7-12% típico
- **P/VPA:** Price / Net Asset per share (premium/discount)
- **Vacância física + financeira**
- **WAULT:** Weighted Average Unexpired Lease Term
- **Liquidez diária**

## Templates
1. FII screening dashboard (DY + P/VPA + vacancy)
2. Sector allocation strategy
3. Tax efficiency (PF vs PJ holding)
4. FoF analysis methodology
5. Yield trap detection (ex-dividend cliffs)
6. WAULT analysis lease portfolio

## Cross-references
- [[kirion-reit-analysis]] · [[kirion-dcf-property]] · [[atlas-fin-foreign-exchange]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **kirion-fii-br** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in kirion-fii-br:**

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
