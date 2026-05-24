---
name: nomos-rgpd-pt-marker
description: RGPD Portugal — Regulamento (UE) 2016/679 + Lei 58/2019 + CNPD orientações. Triggers em "RGPD", "GDPR", "Lei 58/2019", "CNPD", "DPO Portugal", "direitos titulares".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [cnpd_consultation_marker, audit_immutable]
jurisdiction: Portugal + EU
---

# NOMOS-RGPD-PT-MARKER

## Marco
- **Regulamento (UE) 2016/679 (RGPD)** — directamente aplicável
- **Lei 58/2019** — execução RGPD em Portugal (DPO, IDs, sanções)
- **Lei 41/2004** — privacidade comunicações electrónicas
- **CNPD orientações** — pareceres + decisões CNPD
- **Lei 27/2024** — vigilância electrónica
- **EU AI Act 2024/1689** — convergence com RGPD Art. 22 (decisão automatizada)

## Quando usar
- Setup DPO (Data Protection Officer) — obrigatório se >250 employees ou high-risk
- AIPD (Avaliação Impacto Proteção Dados) — high-risk processing
- Comunicação CNPD (incidente ≤ 72h)
- DSR (Direitos titulares) workflow
- Transferências internacionais (EU-US Data Privacy Framework)
- CCTV / vigilância electrónica

## Diferenças PT vs BR
- **Regulator:** CNPD PT vs ANPD BR
- **Lei base:** Lei 58/2019 PT vs Lei 13.709/18 BR
- **DPO:** obrigatório critérios diferentes
- **Sanções:** até 4% revenue PT/EU; até 2% (R$ 50M cap) BR

## Templates
1. AIPD template (DPIA) PT
2. Política privacidade RGPD-aligned
3. DPA (Data Processing Agreement) Art. 28
4. ROPA (Record of Processing Activities) Art. 30
5. Incident response 72h CNPD
6. DSR (acesso/eliminação/portabilidade) workflow
7. Transferência internacional (SCC 2021)
8. CNPD consultation template (prévia)

## Compliance gates
- AIPD obrigatória para high-risk (biometria, geo-tracking, scoring)
- DPO designação > 250 employees
- ROPA mandatory > 250 employees
- Breach notification ≤ 72h CNPD + ≤ "sem demora indevida" titulares

## Cross-references
- [[nomos-cnpd-consultation]] · [[lex-lgpd]] · [[medik-lgpd-healthcare]] · [[risco-rgpd]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-rgpd-pt-marker** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-rgpd-pt-marker:**

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
