---
name: medik-mental-health-digital
description: Saúde mental digital — telepsiquiatria, telepsicologia, RDC ANVISA, segurança específica. Triggers em "saúde mental", "telepsiquiatria", "telepsicologia", "Zenklub", "Vittude", "CRP", "CFP".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [cfm_205_2021_gate, lgpd_healthcare_marker, zdr_healthcare, privilege_clinical]
jurisdiction: Brasil
---

# MEDIK-MENTAL-HEALTH-DIGITAL

## Marco
- **Resolução CFP 11/2018** — Atendimento psicológico online
- **Resolução CFM 2.314/2022** — Telemedicina (inclui psiquiatria)
- **Lei 10.216/2001** — Lei da Reforma Psiquiátrica
- **Portaria GM/MS 3.088/2011** — RAPS (Rede Atenção Psicossocial)
- **LGPD Art. 11** — saúde mental = dado sensível

## Quando usar
- Plataforma telepsicologia/psiquiatria (Zenklub, Vittude tipo)
- B2B EAP (Employee Assistance Program)
- Compliance específica saúde mental (consentimento + risco suicídio + emergência)
- CRP/CFP audit
- Programa SUS RAPS digital

## Riscos específicos
- **Risco de suicídio:** protocolo Columbia + escalation
- **Crise / emergência:** workflow específico (não-presencial limitada)
- **Sigilo profissional reforçado** (CFP Art. 7-8)
- **Menor de idade:** consentimento responsável
- **Cross-border:** profissional precisa CRP/CFP brasileiro

## Templates
1. Termo consentimento telepsicologia (CFP 11)
2. Protocolo risco suicídio (Columbia Protocol)
3. Workflow emergência (escalonamento CAPS/SAMU)
4. Política de matching paciente-profissional
5. Auditoria CFP/CRP compliance

## Cross-references
- [[medik-telemedicine]] · [[medik-cfm-resolutions]] · [[medik-lgpd-healthcare]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **medik-mental-health-digital** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in medik-mental-health-digital:**

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
