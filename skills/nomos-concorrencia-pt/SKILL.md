---
name: nomos-concorrencia-pt
description: Autoridade da Concorrência PT — abuso posição dominante, cartel, M&A control, leniency. Triggers em "Autoridade Concorrência", "AdC", "cartel PT", "abuso posição dominante", "concentração merger PT", "leniency PT".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [audit_immutable]
jurisdiction: Portugal + EU
---

# NOMOS-CONCORRENCIA-PT

## Marco
- **Lei 19/2012 (Regime Jurídico Concorrência)** — RJC
- **TFUE Arts. 101-102** — EU competition law
- **Regulamento EU 1/2003** — enforcement
- **Regulamento EU 139/2004** — merger control
- **Lei 23/2018** — private enforcement (damages actions)
- **Communications AdC + ECN+**

## Quando usar
- M&A concentration notification (thresholds AdC + EU)
- Cartel investigation defense
- Leniency programme application (avoid fines)
- Abuse of dominance investigation
- Vertical restraints (distribution, franchising)
- Dawn raids preparation
- Damages claims (private enforcement)

## Thresholds notificação AdC
- Combined turnover PT > €100M AND each party > €5M
- OU market share > 50% in PT
- OU acquisition de control of undertaking

## Coimas
- **Cartel:** até 10% global revenue ano anterior
- **Abuse:** até 10% global revenue
- **Pessoa singular:** até €5.000.000 + inibição cargos directivos
- **Settlement:** redução até 10%
- **Leniency Type 1A:** imunidade total (primeiro a denunciar)

## Templates
1. Merger notification Form CO (EU) ou PT
2. Cartel risk audit (vertical price-fixing, info exchange)
3. Leniency application strategy
4. Dawn raid playbook (legal + IT response)
5. Compliance programme competitive
6. Settlement procedure assessment
7. Private damages claim strategy

## Cross-references
- [[nomos-cmvm-compliance]] · [[lex-corporate]] · [[zenith-ma-evaluation]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-concorrencia-pt** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-concorrencia-pt:**

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
