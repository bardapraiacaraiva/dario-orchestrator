---
name: atlas-fin-regulatory-reporting-bcb
description: Regulatory reporting Bacen — DCAD, SCR, RDR, IF.Data, GIN-SFN. Triggers em "Bacen reporting", "DCAD", "SCR", "RDR Bacen", "IF.Data", "GIN-SFN", "regulatory reporting BR".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [bcb_compliance_gate, audit_immutable]
jurisdiction: Brasil
---

# ATLAS-FIN-REGULATORY-REPORTING-BCB

## Reports Bacen principais
- **DCAD** — Documento Cadastral Análise de Disclosure
- **SCR** — Sistema Informações de Crédito (mensal)
- **RDR** — Risk Data Reporting
- **IF.Data** — IF.Data app (financial data)
- **GIN-SFN** — Gestor Informações Sistema Financeiro Nacional
- **DLO** — Demonstração Limites Operacionais
- **PROFIS** — Programa Fiscalização
- **Circular Letter** — ad-hoc requests

## Frequencies
- **Daily:** liquidity (LCR), large exposures
- **Monthly:** SCR credit, balance sheet
- **Quarterly:** ICAAP-related, stress test
- **Annual:** ICAAP, recovery plan, financial statements
- **Ad-hoc:** Circular Letters, on-site inspection

## Stack
- **Cloudera, SAS** — enterprise banks
- **Wolters Kluwer OneSumX** — global
- **AxiomSL (Adenza)** — risk + compliance reporting
- **BR-specific:** Senior Sistemas, Algar, custom internal

## Templates
1. Bacen reporting calendar (annual)
2. DLO calculation methodology
3. SCR mapping rules
4. RDR data architecture
5. ICAAP report structure
6. Reconciliation framework (general ledger ↔ reports)

## Cross-references
- [[nomos-bdp-banking-pt]] · [[atlas-fin-foreign-exchange]] · [[demeter-data-quality]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-fin-regulatory-reporting-bcb** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-fin-regulatory-reporting-bcb:**

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
