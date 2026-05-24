---
name: medik-lgpd-healthcare
description: LGPD para saúde — Art. 11 (dados sensíveis), Art. 13 (estudos), AIPD healthcare, DPO. Triggers em "LGPD saúde", "Art 11", "dado sensível saúde", "AIPD saúde", "DPO clínica".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [lgpd_healthcare_marker, zdr_healthcare]
jurisdiction: Brasil
---

# MEDIK-LGPD-HEALTHCARE

## Marco
- **Lei 13.709/2018 (LGPD)** Art. 11 — dados sensíveis (saúde)
- **Lei 13.709/2018** Art. 13 — pesquisa em saúde pública
- **Lei 13.709/2018** Art. 26 — uso compartilhado de dados pelo Poder Público
- **Resolução CFM 1.821/2007** — armazenamento prontuário
- **ANPD Resolução CD/ANPD 2/2022** — agentes pequeno porte

## Quando usar
- Setup DPO/LGPD em clínica (greenfield)
- AIPD para novo sistema (EMR, app paciente)
- Resposta a titular DSR (acesso/portabilidade/eliminação)
- Incidente de dados — comunicação ANPD + titulares
- Contrato compartilhamento dados (Operador-Controlador)

## Bases legais Art. 11 (dados sensíveis)
1. Consentimento específico
2. Tutela da saúde (preferida em emergência)
3. Estudos por órgão de pesquisa
4. Exercício regular de direitos
5. Proteção da vida
6. Cumprimento de obrigação legal

## Templates
1. AIPD healthcare template (15 seções)
2. Política de Privacidade pacientes
3. Contrato Operador-Controlador (clínica + EMR vendor)
4. DSR response workflow
5. Incident response playbook (72h ANPD)

## Compliance built-in
- ✓ Rodapé LGPD automático em outputs externos
- ✓ Anonimização (PCD ANPD) em datasets de pesquisa
- ✓ Logs de acesso prontuário (auditoria)

## Cross-references
- [[medik-emr-integration]] · [[lex-lgpd]] · [[risco-rgpd]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **medik-lgpd-healthcare** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in medik-lgpd-healthcare:**

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
