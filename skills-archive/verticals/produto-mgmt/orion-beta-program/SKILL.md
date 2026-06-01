---
name: orion-beta-program
description: Beta/alpha programs — recruitment, onboarding, feedback loops, NDA, graduation criteria. Triggers em "beta program", "alpha tester", "early access", "closed beta", "private beta".
license: MIT
parent_agent: orion-director
compliance: [user_consent_explicit, nda_when_required]
---

# ORION-BETA-PROGRAM

## Quando usar
- Lançar closed beta antes de GA
- Open beta com gating progressivo
- Alpha testing interno + extended team
- Customer advisory board (CAB) setup
- Graduate beta → GA decision

## Tipos
- **Alpha (private):** dogfooding + 5-10 trusted users
- **Closed beta:** 50-200 invited users, NDA, weekly feedback
- **Open beta:** signup público, sem NDA, feature complete
- **Limited GA:** GA com cap (e.g., first 1000 customers)

## Templates
1. Beta application/screener form
2. Onboarding email sequence (welcome + expectations + Slack invite)
3. NDA template (when applicable)
4. Weekly feedback cadence (survey + interviews)
5. Graduation criteria (signal that beta → GA é seguro)
6. Beta exit communication (transition to GA pricing)

## Métricas
- **Adoption:** % beta users que ativam em D7
- **Retention:** % active em W4
- **NPS beta:** signal de market fit
- **Critical bugs found:** absoluto + trend
- **Quote bank:** quotes para landing page

## Cross-references
- [[orion-product-launch]] · [[orion-feature-flags]] · [[client-onboard]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **orion-beta-program** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in orion-beta-program:**

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
