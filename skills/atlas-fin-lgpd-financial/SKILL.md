---
name: atlas-fin-lgpd-financial
description: LGPD financial + Resolução 4.658 cybersec. Triggers em "LGPD financial", "Resolução 4658", "cybersec Bacen", "ANPD financial", "data financeira protection".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [bcb_compliance_gate, audit_immutable]
jurisdiction: Brasil
---

# ATLAS-FIN-LGPD-FINANCIAL

## Marco
- **Lei 13.709/2018 (LGPD)** + ANPD enforcement
- **Resolução BCB 4.658/2018** — Política Cybersec instituições financeiras (revisada por Resolução BCB 350/2024)
- **Resolução BCB 85/2021** — sharing data Open Banking
- **Circulares Bacen específicas** — incident reporting

## Resolução 4.658 (cybersec) requisitos
1. Política de cybersec formal
2. Plano de ação + orçamento aprovado board
3. Designação responsável cybersec (CISO equivalent)
4. Avaliação de risco anual
5. Plano de resposta a incidentes
6. Disseminação de cultura (treinamento)
7. Compartilhamento ameaças entre instituições
8. Programa testes (pentest, vulnerability)

## LGPD financeiro specifics
- **Base legal preferencial:** execução de contrato (Art. 7, V)
- **Compartilhamento Open Banking:** consentimento específico
- **PEP / sensible data:** consentimento separado
- **Bureau credit:** LegítimoInteresse + transparência

## Templates
1. Política Cybersec Resolução 4.658 compliant
2. AIPD financial transactions
3. Open Banking consent UX (LGPD-aware)
4. Incident response Bacen (notificação <24h)
5. DPO + RPC (Responsável Cybersec) governance
6. Risk assessment annual template

## Cross-references
- [[nomos-rgpd-pt-marker]] · [[aegis-incident-response]] · [[lex-lgpd]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-fin-lgpd-financial** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-fin-lgpd-financial:**

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
