---
name: oraculo-model-card-generation
description: Model cards (Mitchell et al.), datasheets for datasets. Triggers em "model card", "datasheet for datasets", "model documentation", "responsible AI documentation", "AI Act conformity".
license: MIT
parent_agent: oraculo-director
compliance: [audit_immutable, ai_governance]
---

# ORACULO-MODEL-CARD-GENERATION

## Marco
- **Model Cards (Mitchell et al., 2019)** — Google standard
- **Datasheets for Datasets (Gebru et al., 2018)** — dataset documentation
- **EU AI Act Annex IV** — high-risk model technical documentation
- **NIST AI RMF** — model risk management
- **Hugging Face model card spec** — implementation

## Model card sections
1. **Model details:** developer, date, type, license
2. **Intended use:** primary + downstream + out-of-scope
3. **Factors:** subgroups, environments
4. **Metrics:** performance + caveats
5. **Evaluation data:** datasets used
6. **Training data:** datasets + biases
7. **Quantitative analyses:** results per subgroup
8. **Ethical considerations:** risks, mitigations
9. **Caveats:** known limitations
10. **References + contact**

## Datasheets for Datasets sections
- Motivation (why created)
- Composition (what's in it)
- Collection process
- Preprocessing
- Uses (intended + unintended)
- Distribution (license, IP)
- Maintenance

## Stack
- **Hugging Face Model Cards** — standard implementation
- **Google Model Card Toolkit** — automated generation
- **Card creation forms** — guided wizards
- **DAGsHub model registry** — versioned cards

## Templates
1. Model card template (Mitchell format)
2. Datasheet template (Gebru format)
3. EU AI Act Annex IV doc
4. Model card automation (CI)
5. Bias evaluation section
6. Carbon footprint disclosure

## Cross-references
- [[oraculo-ai-safety-research]] · [[nomos-eu-ai-act-pt]] · [[lex-ai-governance]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **oraculo-model-card-generation** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in oraculo-model-card-generation:**

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
