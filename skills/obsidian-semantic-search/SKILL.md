---
name: obsidian-semantic-search
description: Semantic search — vector databases, ANN algorithms (HNSW, IVF), Pinecone, Weaviate, Qdrant, pgvector. Triggers em "semantic search", "vector search", "vector database", "Pinecone", "Weaviate", "Qdrant", "pgvector", "HNSW".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification, access_control]
---

# OBSIDIAN-SEMANTIC-SEARCH

## Quando usar
- Greenfield semantic search system
- Migration: Elasticsearch only → hybrid (lexical + vector)
- Vector database selection
- ANN tuning (recall vs latency)
- Embedding refresh strategy

## Vector DB landscape
- **Pinecone** (managed, líder)
- **Weaviate** (open-source, hybrid)
- **Qdrant** (Rust, fast, open-source)
- **Milvus** (massive scale)
- **pgvector** (Postgres extension, simple stack)
- **Chroma** (developer-friendly)
- **LanceDB** (embedded, OLAP-friendly)

## ANN algorithms
- **HNSW (Hierarchical Navigable Small World):** SOTA recall/latency trade-off
- **IVF (Inverted File):** memory-efficient, slower
- **PQ (Product Quantization):** compression, lossy
- **DiskANN (Microsoft):** disk-based, large-scale

## Princípios
- **Choose by access pattern:** real-time query vs batch
- **Hybrid > pure vector:** lexical handles exact terms
- **Index choice:** HNSW for <100M, DiskANN for billions
- **Embedding refresh:** Monthly+ é OK; daily só se rápida-mudança
- **Multi-tenancy:** namespace per tenant

## Templates
1. Vector DB selection matrix (use case × tool)
2. HNSW parameter tuning (M, efConstruction, efSearch)
3. Hybrid retrieval setup (RRF / weighted sum)
4. Index migration playbook
5. Performance benchmarking suite

## Cross-references
- [[obsidian-rag-corpus-engineering]] · [[obsidian-embedding-models]] · [[obsidian-search-relevance]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **obsidian-semantic-search** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in obsidian-semantic-search:**

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
