---
name: helios-mercado-livre-br
description: Mercado Livre Energia BR — migração cativo→livre, viabilidade económica, ACL. Triggers em "Mercado Livre Energia", "ACL", "migração cativo livre", "consumidor livre", "Lei 14.300", "Reforma Tarifária".
license: SEE-LICENSE
parent_agent: helios-director
compliance: [aneel_compliance_gate, audit_immutable]
jurisdiction: Brasil
---

# HELIOS-MERCADO-LIVRE-BR

## Marco
- **Lei 9.074/1995** — instituiu ambiente livre
- **Lei 10.848/2004** — ACL formal
- **Lei 14.300/2022** — microgeração distribuída + abertura mercado
- **Resolução Normativa ANEEL 1000/2021** — REN GD
- **Decreto 11.000/2022** — abertura para consumidores especiais
- **Reforma Tarifária 2026** — em implementação

## Eligibility para ACL (Ambiente Contratação Livre)
- **Antes 2024:** demanda ≥ 1.500 kW
- **2024:** ≥ 500 kW
- **2026:** ≥ 100 kW (consumidor especial)
- **Futuro:** abertura total residencial (data TBD)

## Workflow migração
```
1. Análise viabilidade (savings vs custos)
2. Cadastro ANEEL como consumidor livre
3. Adesão CCEE (Câmara Comercialização Energia Elétrica)
4. Contratação comercializadora
5. Conexão distribuidora (TUSD)
6. Operação + faturamento
```

## ROI típico
- **Economia:** 15-30% conta luz
- **Payback:** 12-24 meses
- **Custo migração:** R$ 5K-30K (one-off + ongoing)

## Templates
1. Análise viabilidade migração (calculator)
2. RFP comercializadoras energia
3. PPA structuring (sleeve vs virtual vs physical)
4. CCEE cadastro workflow
5. Risco de mercado (PLD, sazonalidade)
6. Reforma Tarifária impact assessment

## Cross-references
- [[helios-ppa-power-purchase]] · [[helios-aneel-compliance]] · [[gaia-carbon-accounting]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **helios-mercado-livre-br** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in helios-mercado-livre-br:**

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
