---
name: euterpe-mmm-modeling
description: Marketing Mix Modeling — Bayesian MMM, Robyn (Meta), LightweightMMM (Google). Triggers em "MMM", "Marketing Mix Modeling", "Robyn", "LightweightMMM", "Bayesian MMM", "media attribution", "carryover effects".
license: MIT
parent_agent: euterpe-director
compliance: [lgpd_marketing, audit_trail]
---

# EUTERPE-MMM-MODELING

## Quando usar
- Cookie deprecation forced (no more MTA)
- Multi-channel budget allocation
- Brand vs performance trade-off
- TV/OOH/Print + Digital combined
- Annual planning + ROI by channel

## Frameworks/tools
- **Robyn (Meta open-source):** R-based, Bayesian
- **LightweightMMM (Google):** Python, JAX
- **PyMC-Marketing:** modern Bayesian Python
- **Nielsen, Analytic Partners, Marketing Science:** enterprise consultancies
- **Recast, Lifesight:** modern SaaS MMM

## Conceitos chave
- **Adstock (carryover):** media decay function
- **Saturation:** diminishing returns (Hill/Michaelis-Menten)
- **Hierarchical Bayesian:** prior + posterior
- **Geo-experiments:** validate MMM with holdout
- **Calibration:** geo lift tests inform priors

## Outputs típicos
- Channel ROI/ROAS by spend level
- Optimal budget allocation
- Saturation curves per channel
- Carryover effects (TV: 4-8 weeks; digital: 1-2 weeks)
- Baseline vs incremental sales

## Templates
1. MMM data requirements (2y weekly minimum)
2. Robyn project setup (R + reticulate)
3. Calibration with geo-lift experiments
4. Budget optimization scenarios
5. MMM stakeholder presentation
6. Refresh cadence (quarterly + ad-hoc)

## Cross-references
- [[euterpe-attribution-multi-touch]] · [[demeter-ml-pipelines]] · [[zenith-monte-carlo]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **euterpe-mmm-modeling** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in euterpe-mmm-modeling:**

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
