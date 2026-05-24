---
name: kirion-portuguese-renda-vitalicia
description: Renda vitalícia + viager PT — annuity-based RE. Triggers em "renda vitalicia", "viager", "annuity real estate", "reverse mortgage PT", "elderly housing investment".
license: SEE-LICENSE
parent_agent: kirion-director
---

# KIRION-PORTUGUESE-RENDA-VITALICIA

## Conceito
**Renda vitalícia / viager:** owner-occupier sells property mantendo direito de habitação + paga rent ao comprador. Estilo francês adaptado PT.

## Estruturas
- **Viager occupé:** seller stays in property até falecimento; price reduzido
- **Viager libre:** buyer pode ocupar imediatamente; price normal
- **Bouquet + Rente:** down payment + monthly annuity for life
- **Reverse mortgage:** debt structure equivalente (BR + PT raramente)

## PT específico
- **CIRE Lei 7/2009:** não confundir com herança problemas
- **Tax treatment:** capital gains, NHR/RNH implications
- **Família restricted** sem direito legítima clear conflict

## Risks (buyer perspective)
- **Longevity risk:** seller lives long → bad ROI
- **Property damage:** during occupancy
- **Legal disputes:** family contesting
- **Mortality table assumptions:** INE PT mortality

## Templates
1. Viager pricing calculator (longevity-adjusted)
2. Contract structure (Cessão + Direito Habitação)
3. Insurance options (life + property)
4. Tax treatment matrix (buyer + seller perspectives)
5. INE PT mortality tables integration
6. Risk-adjusted IRR

## Cross-references
- [[kirion-golden-visa-pt]] · [[kirion-mortgage-underwriting]] · [[lex-familia]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **kirion-portuguese-renda-vitalicia** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in kirion-portuguese-renda-vitalicia:**

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
