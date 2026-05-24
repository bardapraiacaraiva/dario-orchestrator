---
name: atlas-fin-instant-payments
description: Instant payments — PIX BR, SEPA Instant EU, FedNow US, RTP networks. Triggers em "instant payments", "PIX integration", "SEPA Instant", "FedNow", "RTP", "real-time payments", "MIR".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [bcb_compliance_gate, ecb_compliance_gate, audit_immutable]
---

# ATLAS-FIN-INSTANT-PAYMENTS

## Networks globais
- **PIX (BR)** — 24/7, R$ 26 trilhões/ano, líder global per capita
- **SEPA Instant (EU)** — 10 sec, ≤€100K
- **FedNow (US)** — launched Jul 2023, growing
- **RTP (US)** — The Clearing House, alternative to FedNow
- **UK Faster Payments** — desde 2008
- **MIR (Russia)** — geopolitical context
- **PromptPay (Thailand)** — RTP líder ASEAN

## PIX BR específico
- **Volume diário:** ~250M transações
- **Custo:** zero p/ PF, baixo p/ PJ
- **Crescimento:** 130%+ YoY
- **PIX por aproximação (NFC):** 2026 rollout
- **PIX Internacional:** 2026 launch (BR ↔ países selecionados)

## Integration patterns
- **PSP direct** — fintechs como Pagar.me, Stone integração direta Bacen
- **Indirect via BaaS** — Dock, QI Tech, Swap
- **White-label** — banco parceiro empresta charter

## Templates
1. PIX integration roadmap
2. SEPA Instant API spec
3. Instant payment UX best practices
4. Reconciliation real-time
5. Failed payment retry logic
6. Cross-border instant strategy

## Cross-references
- [[atlas-fin-pix-rules-bcb]] · [[atlas-fin-open-banking-br]] · [[atlas-fin-banking-as-a-service]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-fin-instant-payments** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-fin-instant-payments:**

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
