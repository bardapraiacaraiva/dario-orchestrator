---
name: nomos-eu-ai-act-pt
description: EU AI Act — Regulamento (UE) 2024/1689, classificação sistemas IA, conformity assessment, GPAI obligations. Triggers em "EU AI Act", "AI Act", "Regulamento UE 2024/1689", "GPAI", "high-risk AI system", "AI system classification".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [ai_act_risk_classification, audit_immutable]
jurisdiction: Portugal + EU
---

# NOMOS-EU-AI-ACT-PT

## Marco
- **Regulamento (UE) 2024/1689 (AI Act)** — published Aug 2024
- **Entry into force:** 1 Aug 2024
- **Prohibited practices:** 2 Feb 2025 ✓
- **GPAI obligations:** 2 Aug 2025 ✓
- **High-risk systems:** 2 Aug 2026 (current focus)
- **All provisions:** 2 Aug 2027

## Risk categories
1. **Prohibited (Art. 5):** social scoring, untargeted facial recognition, manipulation, emotion recognition workplace/education
2. **High-risk (Annex III):** biometric ID, critical infra, education, employment, essential services, law enforcement, migration, justice
3. **Limited risk (Art. 50):** chatbots, deepfakes (transparency obligations)
4. **Minimal risk:** voluntary codes

## GPAI (General-Purpose AI) tiers
- **GPAI without systemic risk:** transparency + copyright compliance
- **GPAI with systemic risk:** >10^25 FLOPS training, additional obligations (red-teaming, incident reporting, cybersec)

## Quando usar
- AI system classification (which risk tier?)
- High-risk system conformity assessment
- GPAI obligations (Foundation models providers)
- AI literacy programme (mandatory Art. 4)
- Fundamental rights impact assessment
- Post-market monitoring system

## Templates
1. AI system risk classification decision tree
2. High-risk system technical documentation (Annex IV)
3. GPAI model card (capability + limitations)
4. Conformity assessment procedure
5. Post-market monitoring plan
6. Serious incident reporting (Art. 73)
7. EU database registration (Art. 71)
8. AI literacy curriculum

## Coimas (Art. 99)
- **Prohibited practices:** até €35M ou 7% global revenue
- **High-risk obligations:** até €15M ou 3% global revenue
- **Incorrect info:** até €7.5M ou 1.5% global revenue

## Cross-references
- [[lex-ai-governance]] · [[nomos-rgpd-pt-marker]] · [[aegis-secure-sdlc]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-eu-ai-act-pt** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-eu-ai-act-pt:**

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
