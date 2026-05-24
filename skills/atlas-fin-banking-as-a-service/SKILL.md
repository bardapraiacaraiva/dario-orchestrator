---
name: atlas-fin-banking-as-a-service
description: BaaS architecture — white-label banking, embedded accounts, card issuing, Dock, QI Tech, Swap. Triggers em "BaaS", "Banking as a Service", "white-label banking", "Dock", "QI Tech", "Swap fintech", "card issuing".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [bcb_compliance_gate, audit_immutable]
---

# ATLAS-FIN-BANKING-AS-A-SERVICE

## Quando usar
- Non-financial company quer oferecer financial products (super-app)
- Fintech sem charter (não autorizada Bacen)
- Time-to-market reduzir 18 meses → 2 meses
- Marketplace que quer wallet/escrow
- Vertical SaaS adding embedded finance

## Stack BR
- **Dock** — líder BR, processadora + emissora
- **QI Tech** — credit + payments BaaS
- **Swap** — cards + payments
- **Pismo** — banking core
- **CloudWalk (InfinitePay)** — payments BaaS
- **Conductor (Pague Veloz)** — emissor cartões

## Stack global
- **Unit** — US líder
- **Synapse** (turbulent 2024)
- **Treasury Prime** — embedded banking US
- **Solaris (DE)** — European líder (em recovery)
- **ClearBank (UK)** — UK BaaS líder

## Products típicos BaaS
- **Conta digital** — checking equivalent
- **Cartão pré-pago / débito** — Visa/Mastercard rails
- **Cartão crédito** — emissor white-label
- **PIX integration** — accept + send
- **Empréstimos** — credit-as-a-service
- **Seguros** — insurance-as-a-service

## Templates
1. BaaS provider selection scorecard
2. Charter vs BaaS decision framework
3. Integration architecture (BaaS APIs)
4. Compliance responsibility matrix
5. Cost modeling (per-transaction, monthly fees)
6. Exit strategy planning (migration to own charter)

## Cross-references
- [[atlas-fin-embedded-finance]] · [[atlas-fin-instant-payments]] · [[nomos-bdp-banking-pt]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-fin-banking-as-a-service** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-fin-banking-as-a-service:**

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
