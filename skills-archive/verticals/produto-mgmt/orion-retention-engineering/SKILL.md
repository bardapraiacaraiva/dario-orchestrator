---
name: orion-retention-engineering
description: Retention engineering — habit formation, lifecycle, churn prevention, re-engagement, hooks. Triggers em "retention", "churn", "engagement", "lifecycle", "habit formation", "Hooked model".
license: MIT
parent_agent: orion-director
compliance: [user_consent_explicit, no_dark_patterns]
---

# ORION-RETENTION-ENGINEERING

## Filosofia
**Retention é THE metric.** Sem retention, growth é leaky bucket. Foca em comportamentos que predizem retention, não em features.

## Quando usar
- Retention curve flat ou decay rápido
- Churn investigation (porquê estão a sair?)
- Activation → retention bridge
- Win-back campaigns (lapsed users)
- Habit formation design

## Frameworks
- **Hooked Model (Eyal):** trigger → action → variable reward → investment
- **Fogg Behavior Model:** B = MAT
- **L7 / L28:** users active 7/28 dias dos últimos N
- **Power user curve (Jonathan Hsu):** % users with daily intensity
- **Resurrection rate:** % churned users que voltam

## Métricas
- **Retention curve:** D1/7/30/90 por cohort
- **L7/L28 (Facebook):** % users active 7+ dias dos últimos 28
- **Resurrected MAU:** lapsed users que voltam
- **Churn rate:** logo + revenue
- **NRR / GRR:** Net + Gross Revenue Retention

## Templates
1. Retention curve dashboard (cohort heatmap)
2. Churn investigation playbook (exit survey + cancellation flow)
3. Lifecycle email sequences (D0/3/7/14/30)
4. Win-back campaign (lapsed users sequence)
5. Habit formation audit (qual o "hook" do produto?)

## Cross-references
- [[orion-growth-product]] · [[demeter-cohort-analysis]] · [[demeter-predictive]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **orion-retention-engineering** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in orion-retention-engineering:**

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
