---
name: atlas-fin-payment-orchestration
description: Payment orchestration — multi-acquirer routing, retry logic, decline recovery, smart routing. Triggers em "payment orchestration", "smart routing", "multi-acquirer", "payment routing", "decline recovery", "ProcessOut", "Primer".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [pci_dss_scope, audit_immutable]
---

# ATLAS-FIN-PAYMENT-ORCHESTRATION

## Princípio
**1 acquirer = single point of failure.** Multi-acquirer + smart routing = approval rate +5-15%.

## Quando usar
- E-commerce com >€1M/ano payment volume
- Marketplace (multi-merchant, multi-currency)
- LATAM expansion (acquirers locais)
- Decline rate >10%
- Conversion optimization checkout

## Smart routing logic
- **BIN-based:** rotear por country/issuer do cartão
- **Performance-based:** auto-route ao acquirer com melhor approval rate
- **Cost-based:** menor MDR (Merchant Discount Rate)
- **Currency-based:** local acquirer para evitar FX
- **Retry logic:** falhou? tentar outro acquirer com delay

## Stack
- **Primer** — payment orchestration líder
- **ProcessOut** — open-source-friendly
- **Spreedly** — vault + orchestration
- **Adyen** — built-in orchestration
- **Gr4vy** — payment ops
- **BR-specific:** Pagar.me, Pagseguro, Stone (cada um próprio rail)

## Templates
1. Payment orchestration architecture
2. Smart routing rules matrix
3. Decline reason analysis + remediation
4. PCI-DSS scope reduction strategy
5. Acquirer scorecard (cost, approval, latency)
6. A/B testing payment flows

## Cross-references
- [[atlas-fin-fraud-prevention]] · [[atlas-fin-chargeback-management]] · [[atlas-fin-foreign-exchange]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-fin-payment-orchestration** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-fin-payment-orchestration:**

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
