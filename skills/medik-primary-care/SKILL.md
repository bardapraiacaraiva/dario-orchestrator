---
name: medik-primary-care
description: Atenção primária — ESF, NASF, PCDT, modelo de cuidado crônico. Triggers em "atenção primária", "APS", "ESF", "NASF", "saúde da família", "primary care", "cuidado longitudinal".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [lgpd_healthcare_marker, cfm_resolutions]
jurisdiction: Brasil
---

# MEDIK-PRIMARY-CARE

## Quando usar
- Setup UBS/ESF greenfield
- Linha de cuidado para condição crônica
- Vinculação populacional + território
- Coordenação com média/alta complexidade
- E-SUS APS integration

## Marco
- **PNAB 2017** — Política Nacional Atenção Básica
- **CONITEC PCDT** — diretrizes terapêuticas
- **Carteira de Serviços APS**
- **PNAB 2024** — atualização

## Funções APS (Starfield)
1. **Primeiro contacto:** porta de entrada
2. **Longitudinalidade:** vínculo no tempo
3. **Integralidade:** prevenção + promoção + tratamento
4. **Coordenação:** integração com restante sistema

## Templates
1. Diagnóstico territorial (mapa risco + caracterização)
2. Linha de cuidado HAS/DM (PNS + e-SUS)
3. Visita domiciliar protocolo
4. Reunião de equipe multiprofissional
5. Coordenação especialidades (referência/contrarreferência)

## Cross-references
- [[medik-clinical-protocols]] · [[medik-mental-health-digital]] · [[medik-emr-integration]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **medik-primary-care** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in medik-primary-care:**

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
