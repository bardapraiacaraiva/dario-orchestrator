---
name: nomos-anti-fraude-pt
description: Anti-fraude PT — Lei 35/2010 anti-corrupção, Lei 5/2002 branqueamento, Regime Anticorrupção (Lei 109/2021). Triggers em "anticorrupção PT", "Lei 109/2021", "Lei 35/2010", "branqueamento capitais", "corrupção PT", "compliance anticorrupção".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [audit_immutable]
jurisdiction: Portugal
---

# NOMOS-ANTI-FRAUDE-PT

## Marco
- **Lei 109/2021** — Regime Geral Anti-Corrupção PT
- **DL 109-E/2021** — Mecanismo Anti-Corrupção (ENPC + MENAC)
- **Lei 83/2017** — BC/FT (branqueamento + financiamento terrorismo)
- **DL 27/2024** — actualização BC/FT
- **Lei 5/2002** — medidas combate criminalidade organizada
- **Código Penal PT Arts. 372-374** — corrupção pública/privada

## Quando usar
- Programa Anticorrupção (PCC) — obrigatório > 50 employees
- Canal denúncias (whistleblower) — obrigatório > 50 employees
- Plano Prevenção Riscos Corrupção e Infrações Conexas (PPRCIC)
- KYC/AML em entidades obrigadas (Lei 83/2017)
- Due diligence política (pessoas politicamente expostas - PEPs)
- Investigação interna fraude

## PPRCIC obrigatório (Lei 109/2021)
- Empresas com > 50 employees
- Identificação de riscos por área
- Medidas mitigação
- Plano formação anticorrupção
- Canal denúncias confidencial
- Designação Responsável Cumprimento Normativo (RCN)
- Comunicação anual MENAC

## Templates
1. PCC (Programa Cumprimento Normativo) template
2. PPRCIC structure (mandatory chapters)
3. Code of Conduct anticorrupção
4. Whistleblower channel setup (anonymous + non-retaliation)
5. PEP screening checklist
6. Internal investigation playbook
7. Comunicação MENAC anual
8. Training curriculum anticorrupção

## Coimas
- Falta PPRCIC: €1.000-44.890
- Crime corrupção (pessoa colectiva): até 1.500 dias-multa
- BC/FT entidades obrigadas: até €5.000.000

## Cross-references
- [[nomos-kyc-aml-pt]] · [[gaia-governance-frameworks]] · [[lex-corporate]] · [[lex-criminal]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-anti-fraude-pt** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-anti-fraude-pt:**

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
