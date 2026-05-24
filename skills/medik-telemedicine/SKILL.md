---
name: medik-telemedicine
description: Telemedicina BR — CFM 2.314/2022, ANVISA RDC SaMD, prescrição digital, teleconsulta. Triggers em "telemedicina", "teleconsulta", "telessaúde", "CFM 2314", "prescrição digital", "Memed", "Doctoralia".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [cfm_205_2021_gate, lgpd_healthcare_marker, zdr_healthcare]
jurisdiction: Brasil
---

# MEDIK-TELEMEDICINE

## Marco
- **Resolução CFM 2.314/2022** — Define telemedicina (define modalidades + requisitos)
- **Lei 13.989/2020** — Autoriza telemedicina (durante pandemia, prorrogada)
- **Lei 14.510/2022** — Telemedicina permanente
- **RDC ANVISA 751/2022** — Software como dispositivo médico

## Modalidades CFM 2.314
1. **Teleconsulta** — médico ↔ paciente
2. **Teleinterconsulta** — médico ↔ médico
3. **Telediagnóstico** — análise de exames remoto
4. **Telecirurgia** — robótica
5. **Telemonitoramento** — wearables, monitoramento crônico
6. **Tele-orientação** — triagem

## Requisitos
- Identificação inequívoca de paciente e médico
- Consentimento livre e esclarecido
- Prontuário eletrônico
- Padrões mínimos de qualidade técnica
- Sigilo e segurança da informação
- Receita digital (ICP-Brasil ou validação CRM)

## Templates
1. Termo de consentimento teleconsulta
2. Compliance checklist plataforma telemedicina
3. Workflow prescrição digital ICP-Brasil
4. Auditoria de plataforma (Doctoralia/Memed integration)
5. Disaster recovery (consulta interrompida)

## Cross-references
- [[medik-cfm-resolutions]] · [[medik-lgpd-healthcare]] · [[medik-emr-integration]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **medik-telemedicine** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in medik-telemedicine:**

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
