---
name: helios-renewable-financing
description: Renewable project finance — FIDC, debêntures incentivadas, BNDES, project bonds. Triggers em "renewable financing", "FIDC energia", "debêntures incentivadas", "BNDES renewable", "project bonds", "project finance".
license: SEE-LICENSE
parent_agent: helios-director
---

# HELIOS-RENEWABLE-FINANCING

## Estruturas BR
- **BNDES:** linha verde, taxa subsidiada
- **Debêntures incentivadas (Lei 12.431/2011):** isenção IR PF
- **FIDC infra:** Fundo Investimento Direitos Creditórios
- **Project bonds:** issuance via securitization
- **Green bonds:** ICMA Green Bond Principles aligned
- **Sustainability-linked loans:** KPI-tied

## Estruturas globais
- **Tax equity (US):** PTC/ITC (post-IRA)
- **Project finance debt:** 70/30 leverage típico
- **Pre-COD bridge financing:** during construction
- **Refinance pós-COD:** lower rate post-completion

## Métricas chave
- **DSCR (Debt Service Coverage Ratio):** ≥ 1.3x
- **LLCR (Loan Life Coverage Ratio):** ≥ 1.4x
- **IRR equity:** 12-18%
- **Tenor:** 12-20 years (matching PPA)

## Templates
1. Financial model template (project finance)
2. BNDES application checklist
3. Debêntures incentivadas estruturação
4. Green bond framework (ICMA aligned)
5. Sensitivity analysis (PLD, exchange rate, curtailment)
6. Investor pitch (renewable project)

## Cross-references
- [[helios-ppa-power-purchase]] · [[zenith-capital-allocation]] · [[atlas-fin-foreign-exchange]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **helios-renewable-financing** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in helios-renewable-financing:**

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
