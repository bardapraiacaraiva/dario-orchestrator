---
name: medik-cfm-resolutions
description: CFM resolutions — Código Ética Médica, telemedicina (2.314/2022), prontuário, publicidade médica. Triggers em "CFM", "Conselho Federal Medicina", "Código Ética Médica", "CRM", "Resolução CFM", "prontuário médico".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [cfm_205_2021_gate, audit_cfm]
jurisdiction: Brasil
---

# MEDIK-CFM-RESOLUTIONS

## Quando usar
- Setup compliance de clínica/consultório
- Análise de publicidade médica (Resolução 1.974/2011)
- Pareceres CFM/CRM
- Telemedicina protocol (2.314/2022)
- Prontuário eletrônico requirements
- Conflito ético profissional

## Marco principal
- **Resolução CFM 2.217/2018** — Código de Ética Médica
- **Resolução CFM 2.314/2022** — Telemedicina
- **Resolução CFM 1.974/2011** — Publicidade médica
- **Resolução CFM 1.638/2002** — Prontuário médico
- **Resolução CFM 2.227/2018** — Telemedicina (revogada parcial)

## Templates
1. Checklist compliance consultório (publicidade + sigilo + prontuário)
2. Termo de consentimento telemedicina (Res. 2.314)
3. Auditoria de site/Instagram médico
4. Modelo de prontuário (Res. 1.638)
5. Parecer ético interno

## Compliance built-in
- ✓ Sigilo médico (Art. 73-77 Código)
- ✓ Vedações de publicidade
- ✓ Identificação do responsável técnico (CRM visível)
- ✓ LGPD compatibilidade (Art. 11)

## Cross-references
- [[medik-telemedicine]] · [[medik-lgpd-healthcare]] · [[medik-emr-integration]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **medik-cfm-resolutions** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in medik-cfm-resolutions:**

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
