---
name: orion-product-ops
description: Product Ops — tooling, rituals, documentation, scaling product orgs. Triggers em "product ops", "product operations", "PM tooling", "product rituals", "scaling product team".
license: MIT
parent_agent: orion-director
compliance: [data_privacy_by_design]
---

# ORION-PRODUCT-OPS

## Quando usar
- Product team scaling (5 PMs → 20 PMs)
- Tool sprawl audit (Jira + Linear + Notion + Productboard?)
- Rituals overhaul (too many meetings? too few?)
- PM onboarding/playbook
- Cross-functional process improvement

## Pillars (Melissa Perri framework)
1. **Business + customer insights:** data + research access
2. **Communication + alignment:** stakeholder management
3. **Practices + governance:** consistent PM standards

## Stack típico
- **Backlog/roadmap:** Linear, Jira, Productboard, ProdPad
- **Docs:** Notion, Confluence, Coda
- **Research repo:** Dovetail, Notably
- **Analytics:** Mixpanel/Amplitude (defined elsewhere)
- **Feedback:** Productboard, Canny, UserVoice
- **Whiteboard:** Miro, FigJam, Mural

## Rituals (recommended cadence)
- **Daily:** PM standup (15 min, opcional)
- **Weekly:** discovery review (Teresa Torres style)
- **Weekly:** team product review
- **Bi-weekly:** sprint planning + retro
- **Monthly:** customer review (top accounts)
- **Quarterly:** OKR check + roadmap review
- **Annual:** strategy + planning offsite

## Templates
1. PM onboarding playbook (first 30/60/90 days)
2. Tool selection scorecard
3. PM career ladder (junior → principal)
4. Product review template (weekly)
5. Quarterly business review (QBR) template

## Cross-references
- [[orion-product-strategy]] · [[orion-roadmap-planning]] · [[pessoa-orgdesign]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **orion-product-ops** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in orion-product-ops:**

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
