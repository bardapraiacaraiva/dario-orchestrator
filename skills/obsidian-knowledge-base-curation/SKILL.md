---
name: obsidian-knowledge-base-curation
description: KB maintenance — content decay detection, quality scoring, dedup, governance. Triggers em "knowledge base", "KB curation", "content decay", "knowledge governance", "dedup".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification, audit_trail, retention_policies]
---

# OBSIDIAN-KNOWLEDGE-BASE-CURATION

## Quando usar
- KB com 1000+ docs, qualidade unknown
- Customer-facing help center
- Internal wiki cleanup
- AI-readable docs (RAG-source)
- Documentation governance program

## Curation pillars
1. **Freshness:** detectar stale content (>180d sem update)
2. **Quality:** completeness + accuracy + clarity scores
3. **Coverage:** gap analysis (what's missing)
4. **Dedup:** near-duplicates merge
5. **Findability:** internal search works?
6. **Governance:** owner per doc, review cadence

## Templates
1. Doc metadata schema (owner + reviewer + last_review + ttl)
2. Content audit dashboard (freshness + quality + traffic)
3. Quality rubric (0-100 score)
4. Dedup detection (MinHash / SimHash)
5. Doc lifecycle workflow (draft → review → publish → archive)
6. Knowledge gaps report (queries com 0 results)

## Métricas chave
- **Coverage:** % search queries with relevant results
- **Freshness:** mediana de days-since-update
- **Quality:** % docs com all metadata + review recent
- **Trust:** % usuários que dão upvote em answer
- **Reduction:** support tickets evitados por self-service

## Cross-references
- [[obsidian-search-relevance]] · [[demeter-data-quality]] · [[risco-rgpd]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **obsidian-knowledge-base-curation** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in obsidian-knowledge-base-curation:**

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
