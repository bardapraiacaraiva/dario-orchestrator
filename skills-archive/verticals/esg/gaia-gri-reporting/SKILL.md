---
name: gaia-gri-reporting
description: GRI Standards — Global Reporting Initiative Universal + Sector + Topic standards. Multi-stakeholder approach. Triggers em "GRI", "Global Reporting Initiative", "GRI Universal", "stakeholder materiality", "sustainability report".
license: SEE-LICENSE
parent_agent: gaia-director
compliance: [audit_immutable, csrd_disclosure_gate]
---

# GAIA-GRI-REPORTING

## Marco
- **GRI Universal Standards (2021):** GRI 1, GRI 2, GRI 3
- **GRI Sector Standards:** Oil & Gas (GRI 11), Coal (GRI 12), Agriculture (GRI 13), more coming
- **GRI Topic Standards:** 33+ topics (GRI 201-418)
- **Multi-stakeholder materiality** (vs SASB financial materiality)

## GRI Universal structure
- **GRI 1 (Foundation):** how to use Standards
- **GRI 2 (General Disclosures):** organizational profile
- **GRI 3 (Material Topics):** materiality determination

## Topic standards categorias
- **Economic (GRI 201-207):** anti-corruption, tax, etc.
- **Environmental (GRI 301-308):** materials, energy, water, biodiversity, emissions, effluents, waste, supplier env assessment
- **Social (GRI 401-418):** employment, labor/management relations, OHS, training, diversity, human rights, communities

## Quando usar
- BR/global companies (GRI is most-adopted globally)
- Multi-stakeholder accountability priority
- ESRS-aligned reporting (GRI 1 + ESRS = good combination)
- CDP supplemental disclosures
- B-Corp aligned reporting

## Templates
1. GRI Content Index template
2. Stakeholder engagement plan (GRI 2-29)
3. Material topics determination workshop (GRI 3-1, 3-2)
4. GRI Index online disclosure
5. Sector-specific disclosure mapping (Oil & Gas, Agriculture)
6. External assurance scope (limited vs reasonable)

## GRI vs CSRD/ESRS
- ESRS double materiality > GRI stakeholder materiality
- ESRS digital tagging mandatory; GRI optional
- ESRS audit mandatory; GRI optional
- **Best practice:** GRI for narrative + ESRS for compliance

## Cross-references
- [[gaia-csrd-reporting]] · [[gaia-sasb-standards]] · [[gaia-sustainability-strategy]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **gaia-gri-reporting** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in gaia-gri-reporting:**

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
