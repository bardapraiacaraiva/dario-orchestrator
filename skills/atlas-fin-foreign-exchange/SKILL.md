---
name: atlas-fin-foreign-exchange
description: FX management — câmbio BR (BCB), hedging, IOF, IRS, declaração CBE. Triggers em "câmbio", "FX management", "IOF câmbio", "DCE Bacen", "CBE", "remessa internacional", "Wise", "Remessa Online".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [bcb_compliance_gate, audit_immutable]
jurisdiction: Brasil + Global
---

# ATLAS-FIN-FOREIGN-EXCHANGE

## Marco BR
- **Lei 14.286/2021** — novo marco câmbio BR (substitui Decreto-Lei 4.595)
- **Resolução BCB 277/2022** + posteriores
- **IOF Câmbio** — alíquotas variáveis (0%-6.38%)
- **CBE (Capitais Brasileiros no Exterior)** — declaração Bacen quando >US$ 1M
- **DCE (Declaração Conjunta sobre Exportação)** — exportadores

## Operações típicas
- **Remessa internacional:** Wise, Remessa Online, BS2
- **Importação:** fechamento câmbio + DI
- **Exportação:** ACC/ACE financing
- **Hedge:** NDF (Non-Deliverable Forward), swap
- **Investimento exterior:** declaração CBE

## IOF Câmbio alíquotas (2026)
- **Aquisição moeda papel/cartão:** 3.5%
- **Importação:** 0.38%
- **Empréstimo externo curto prazo:** 6%
- **Remessa para residente exterior:** 0.38%
- **Transferência conta própria exterior:** 1.1%
- **Convergência tax reform:** progressive harmonization

## Templates
1. FX integration architecture (Bacen reporting)
2. Hedging strategy template (cash flow vs balance sheet)
3. IOF calculator (per operation type)
4. CBE annual declaration
5. ACC/ACE workflow (export financing)
6. NDF hedging playbook

## Cross-references
- [[atlas-fin-regulatory-reporting-bcb]] · [[nomos-mifid-ii-pt]] · [[zenith-sensitivity-analysis]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-fin-foreign-exchange** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-fin-foreign-exchange:**

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
