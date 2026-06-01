---
name: orion-feature-flags
description: Feature flags / progressive delivery — LaunchDarkly, GrowthBook, Unleash, Statsig. Canary, rollback, A/B integration. Triggers em "feature flag", "LaunchDarkly", "GrowthBook", "progressive delivery", "canary release".
license: MIT
parent_agent: orion-director
compliance: [data_privacy_by_design, feature_flag_audit]
---

# ORION-FEATURE-FLAGS

## Quando usar
- Setup feature flag system (greenfield)
- Migration de hardcoded toggles → managed system
- Trunk-based development sem long-running branches
- Safe deploys (deploy != release)
- A/B testing integration

## Stack
- **LaunchDarkly** (enterprise líder)
- **GrowthBook** (open-source, integra A/B)
- **Unleash** (open-source enterprise)
- **Statsig** (real-time + experimentation)
- **Flagsmith** (self-hostable)
- **ConfigCat** (developer-friendly, cheaper)

## Tipos de flag
- **Release flag:** dark launch + canary rollout (short-lived)
- **Experiment flag:** A/B testing (medium-lived)
- **Ops flag:** kill switch, circuit breaker (permanent)
- **Permission flag:** beta access, paid tier gating (permanent)

## Princípios
- **Lifecycle clear:** cada flag tem dono + remove date
- **Clean up religiously:** flags antigos = tech debt
- **Targeting rules versionadas:** audit trail
- **Default safe:** off por defeito quando em dúvida

## Templates
1. Feature flag governance doc (naming, lifecycle, ownership)
2. LaunchDarkly project setup (envs, segments, roles)
3. Canary rollout playbook (1% → 10% → 50% → 100%)
4. Flag cleanup audit script
5. Incident response: kill switch playbook

## Cross-references
- [[orion-product-launch]] · [[demeter-ab-testing]] · [[builder-ci-cd]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **orion-feature-flags** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in orion-feature-flags:**

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
