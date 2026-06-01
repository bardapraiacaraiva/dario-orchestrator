---
name: oraculo-paper-writing
description: Academic paper writing — LaTeX, citations, Overleaf, arXiv. Triggers em "academic writing", "paper writing", "LaTeX", "Overleaf", "arXiv", "ACL", "NeurIPS submission".
license: MIT
parent_agent: oraculo-director
compliance: [research_integrity]
---

# ORACULO-PAPER-WRITING

## Estrutura ML paper standard
1. **Abstract** (250 words: motivation/contribution/method/results)
2. **Introduction** (5-10% of length)
3. **Related Work**
4. **Method** (most detail)
5. **Experiments** (datasets + setup + ablations)
6. **Results + Analysis** (tables + figures)
7. **Discussion** (limitations, future)
8. **Conclusion** (short, no new info)
9. **References**
10. **Appendix** (proofs, additional results)

## Stack
- **Overleaf** — collaborative LaTeX líder
- **arXiv** — preprint server
- **Hugging Face Papers** — discoverability
- **Connected Papers** — citation visualization
- **Mendeley, Zotero** — reference mgmt
- **Grammarly Premium** — editing

## Conferences ML
- **NeurIPS** — top ML conf (Dec)
- **ICML** — second top (Jul)
- **ICLR** — top deep learning (May)
- **ACL** — NLP (Aug)
- **EMNLP** — NLP empirical (Nov)
- **CVPR** — vision (Jun)
- **AAAI** — broad AI (Feb)

## Acceptance rates típicas
- NeurIPS: 25-30%
- ICML: 25-28%
- ICLR: 30-35%
- ACL: 20-25%

## Templates
1. ML paper LaTeX template (NeurIPS style)
2. Ablation table design
3. Reproducibility checklist (NeurIPS 2024+)
4. Camera-ready checklist
5. Author response strategy (rebuttal)
6. Press release template (impact paper)

## Cross-references
- [[oraculo-peer-review]] · [[oraculo-conference-tracking]] · [[oraculo-model-card-generation]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **oraculo-paper-writing** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in oraculo-paper-writing:**

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
