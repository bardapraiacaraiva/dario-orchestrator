---
name: nomos-cmvm-compliance
description: CMVM compliance — Código dos Valores Mobiliários, prospetos, OPVs, disclosures, governance issuers. Triggers em "CMVM", "Código Valores Mobiliários", "prospeto", "OPV", "OPA", "issuer governance", "MAR market abuse".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [cmvm_disclosure_gate, audit_immutable]
jurisdiction: Portugal
---

# NOMOS-CMVM-COMPLIANCE

## Marco
- **CVM (Código dos Valores Mobiliários)** — DL 486/99
- **Regulamento CMVM 3/2018** — prospetos
- **MAR (Market Abuse Regulation)** EU 596/2014 — diretamente aplicável PT
- **MAR Lei 28/2017** — transposição PT
- **Regulamento CMVM 4/2013** — governance societário
- **Regulamento CMVM 7/2018** — assembleia geral
- **DL 357-A/2007** — intermediação financeira

## Quando usar
- Prospeto OPV/IPO Euronext Lisbon
- OPA (Oferta Pública de Aquisição)
- Disclosure de informação privilegiada (MAR Art. 17)
- Insider lists management
- PDMR (Persons Discharging Managerial Responsibilities) reporting
- Manipulação de mercado investigação

## Templates
1. Prospeto OPV structure (Annex I-XX EU Prospectus Regulation)
2. MAR information privileged decision tree
3. Insider list template (MAR Art. 18)
4. PDMR transaction notification (MAR Art. 19)
5. Relatório governance societário (anual)
6. Comunicado ao mercado template
7. MAR investigation response

## Compliance gates
- Disclosure privileged info ≤ 24h
- Insider list maintenance audit trail
- PDMR transaction blackout periods (30d pré-results)
- MAR closed period enforcement

## Cross-references
- [[nomos-mifid-ii-pt]] · [[nomos-concorrencia-pt]] · [[lex-corporate]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-cmvm-compliance** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-cmvm-compliance:**

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
