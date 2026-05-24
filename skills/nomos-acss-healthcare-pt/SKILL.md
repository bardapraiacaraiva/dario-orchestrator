---
name: nomos-acss-healthcare-pt
description: ACSS healthcare PT — Serviço Nacional Saúde, convenções, SNS digital, INFARMED prescription. Triggers em "ACSS", "SNS", "convencionado", "INFARMED", "Ordem dos Médicos PT", "medicamentos PT".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [cnpd_consultation_marker, audit_immutable]
jurisdiction: Portugal
---

# NOMOS-ACSS-HEALTHCARE-PT

## Marco
- **Lei 95/2019** — Lei de Bases da Saúde PT
- **DL 11/2017** — SNS digital
- **DL 113/2011** — ACSS attributions
- **DL 176/2006** — medicamentos uso humano
- **Despacho 2596/2025** — desburocratização
- **Lei 12/2005** — informação genética + saúde
- **Ordem dos Médicos** — Código Deontológico

## Quando usar
- Hospital privado convencionado SNS
- Clínica autorização ERS (Entidade Reguladora Saúde)
- Telemedicina PT (vs CFM 2.314 BR)
- e-Saúde / RSE (Registo Saúde Electrónico)
- Prescrição electrónica
- Farmácia hospitalar + ambulatório
- Ensaios clínicos INFARMED

## Templates
1. Convenção SNS application
2. Autorização ERS (regulator saúde)
3. Telemedicina PT compliance (DGS orientações)
4. e-Receita médica padrão SNS
5. Termo consentimento informado PT
6. Ensaio clínico INFARMED submission
7. Farmacovigilância notification

## Diferenças PT vs BR healthcare
- **Regulator:** ERS PT vs ANS BR
- **Single-payer:** SNS quase universal PT vs SUS+saúde suplementar BR
- **Compliance órgão:** Ordem dos Médicos PT vs CFM BR
- **Med billing:** SIIMA PT vs TUSS BR
- **e-Saúde:** RSE PT vs RNDS BR

## Cross-references
- [[nomos-rgpd-pt-marker]] · [[medik-cfm-resolutions]] · [[medik-emr-integration]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-acss-healthcare-pt** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-acss-healthcare-pt:**

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
