---
name: medik-ans-compliance
description: ANS compliance — operadoras saúde, Rol de Procedimentos, RN 465 (geriatria), RN 488 (RPS), RN 593 (cobertura). Triggers em "ANS", "operadora saúde", "Rol procedimentos", "RN ANS", "plano de saúde", "coberturas".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [ans_regulatory, lgpd_healthcare, cfm_resolutions]
jurisdiction: Brasil
---

# MEDIK-ANS-COMPLIANCE — Operadoras de Saúde

## Quando usar
- Auditoria de cobertura/contratos de operadora
- Análise de Rol ANS (procedimentos obrigatórios)
- Notificações de Investigação Preliminar (NIP)
- Comunicado/Diretriz ANS implementation
- Reajuste anual operadora compliance

## Marco regulatório
- **Lei 9.656/1998** — Lei dos Planos de Saúde
- **RN 465/2021** — Rol de Procedimentos (lista taxativa)
- **RN 593/2023** — Cobertura para câncer
- **RN 622/2024** — Reajuste 2024
- **STJ Tema 1.069** — Rol como taxativo mas com mitigações
- **Lei 14.454/2022** — Rol exemplificativo retificado

## Templates
1. Análise de cobertura para procedimento off-Rol
2. NIP response template
3. Cláusulas obrigatórias contratuais (RN 565)
4. Reajuste comunicado beneficiário
5. Atendimento à diretriz ANS

## Compliance built-in
- ✓ Sigilo médico (Art. 102 Código Ética Médica)
- ✓ LGPD Art. 11 (dado sensível saúde)
- ✓ Direito à informação clara (CDC + Lei 9656)
- ✓ Boa-fé contratual

## Cross-references
- [[medik-claim-management]] · [[medik-lgpd-healthcare]] · [[lex-consumidor]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **medik-ans-compliance** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in medik-ans-compliance:**

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
