---
name: atlas-fin-pix-rules-bcb
description: PIX rules BCB — limites, fraude, MED, MED-PIX, PIX Internacional, PIX Saque/Troco. Triggers em "PIX", "PIX Bacen", "MED PIX", "PIX Internacional", "PIX Saque", "PIX por aproximação", "Bacen PIX".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [bcb_compliance_gate, audit_immutable]
jurisdiction: Brasil
---

# ATLAS-FIN-PIX-RULES-BCB

## Marco
- **Resolução BCB 1/2020** — instituição arranjo PIX
- **Resolução BCB 19/2020** — funcionamento PIX
- **Circular BCB 4.027/2020** + posteriores
- **Resolução BCB 103/2021** — MED (Mecanismo Especial Devolução)
- **PIX Internacional 2026** — em implementação

## Quando usar
- Fintech integração PIX
- PSP (Provedor Serviços Pagamento) autorização
- Fraud rules PIX-specific
- MED (chargeback PIX equivalente) workflow
- PIX por aproximação (NFC) 2026
- PIX Cobrança (boleto-substitute)

## Modalidades PIX
- **PIX comum** — entre pessoas
- **PIX Cobrança** — substituto boleto, recorrência
- **PIX Saque/Troco** — saque em estabelecimentos
- **PIX por aproximação** — NFC contactless 2026
- **PIX Internacional** — cross-border 2026+

## Limites + fraude
- Conta PF: ≤ R$ 1.000/transação noturno (20h-6h)
- Limite mensal noturno: R$ 1.000 ajustável
- MED ≤ R$ 70.000 → 80 dias para iniciar
- Fraude marker → bloqueio cautelar

## Templates
1. PIX integration architecture
2. Fraud detection rules PIX
3. MED workflow (chargeback equivalent)
4. PIX QR Code generation (estático + dinâmico)
5. Pix Cobrança recorrência integration
6. Customer dispute UI

## Cross-references
- [[atlas-fin-fraud-prevention]] · [[atlas-fin-chargeback-management]] · [[atlas-fin-instant-payments]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-fin-pix-rules-bcb** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-fin-pix-rules-bcb:**

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
