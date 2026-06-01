---
name: oraculo-benchmarking
description: Benchmark design — dataset curation, leaderboard creation, anti-contamination. Triggers em "benchmark design", "leaderboard", "dataset curation", "data contamination", "GLUE", "SuperGLUE", "BIG-Bench design".
license: MIT
parent_agent: oraculo-director
compliance: [research_integrity, audit_immutable]
---

# ORACULO-BENCHMARKING

## Quando usar
- New domain → no benchmark exists
- Existing benchmark saturated (>95% accuracy)
- Custom enterprise eval
- Specialty (BR PT legal, healthcare, etc.)
- Multimodal benchmark

## Anti-contamination
- **Test set leakage:** model trained on test data (common!)
- **Held-out validation:** never used during training
- **Time-based split:** train < cutoff date
- **Canary strings:** detect contamination
- **Private test sets:** API-only, no public release

## Datasets curation
- **Source diversity:** multiple sources
- **Annotator agreement:** inter-rater kappa ≥ 0.7
- **Difficulty distribution:** easy/medium/hard
- **Demographic balance:** avoid bias
- **License clarity:** CC, Apache, MIT
- **Versioning:** semver

## Leaderboard infrastructure
- **Hugging Face Open LLM Leaderboard**
- **PapersWithCode**
- **Chatbot Arena (LMSYS):** human preferences
- **HELM (Stanford)** — controlled
- **Custom:** Streamlit + Postgres

## Templates
1. Benchmark design document
2. Dataset card (Mitchell et al.)
3. Annotation guidelines
4. Leaderboard rules + submission process
5. Anti-contamination audit
6. Benchmark retirement criteria (saturation)

## Cross-references
- [[oraculo-model-evaluation]] · [[oraculo-evaluation-frameworks]] · [[oraculo-replication-studies]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **oraculo-benchmarking** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in oraculo-benchmarking:**

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
