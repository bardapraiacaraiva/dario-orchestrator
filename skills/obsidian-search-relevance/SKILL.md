---
name: obsidian-search-relevance
description: Search relevance — BM25, TF-IDF, learning-to-rank, hybrid search, reranking. Elasticsearch, OpenSearch, Vespa. Triggers em "search relevance", "BM25", "TF-IDF", "Elasticsearch", "ranking", "reranking", "LTR".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification, audit_trail]
---

# OBSIDIAN-SEARCH-RELEVANCE

## Quando usar
- Search quality tuning (top-K not relevant)
- Migration: SQL LIKE → Elasticsearch
- Hybrid search (lexical + vector)
- Personalization (results per user)
- A/B testing of ranking changes

## Stack
- **Elasticsearch / OpenSearch:** lexical SOTA
- **Vespa.ai:** large-scale + ML ranking
- **Solr:** enterprise search legacy
- **Typesense / Meilisearch:** developer-friendly
- **Algolia:** managed instant search
- **LucidWorks Fusion:** enterprise + LTR

## Ranking signals
- **Lexical:** BM25 (term frequency + IDF + length norm)
- **Semantic:** vector similarity (embeddings)
- **Behavioral:** CTR, dwell time, conversions
- **Recency:** freshness boost
- **Authority:** PageRank-style + domain authority

## Templates
1. Elasticsearch mapping production-grade
2. BM25 tuning playbook (k1, b parameters)
3. Hybrid search setup (lexical + vector + RRF)
4. Reranking with cross-encoder (Cohere Rerank, BGE-reranker)
5. LTR (LambdaMART) training pipeline
6. Search relevance eval (NDCG@K, MAP)

## Cross-references
- [[obsidian-semantic-search]] · [[obsidian-rag-corpus-engineering]] · [[demeter-event-tracking]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **obsidian-search-relevance** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in obsidian-search-relevance:**

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
