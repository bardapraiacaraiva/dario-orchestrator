---
name: oraculo-rag-research
description: RAG research — chunking, hybrid retrieval, reranking, evaluation. Triggers em "RAG research", "retrieval augmented generation", "chunking strategies", "RAG evaluation", "RAGAS", "contextual retrieval", "GraphRAG".
license: MIT
parent_agent: oraculo-director
---

# ORACULO-RAG-RESEARCH

## RAG evolution (2023-2026)
- **Vanilla RAG (2023):** simple chunk + embed + retrieve
- **Hybrid RAG (2024):** + BM25 + reranking
- **Contextual Retrieval (Anthropic 2024):** chunk + summary
- **Late Chunking (Jina 2024):** embed full → chunk depois
- **GraphRAG (Microsoft 2024):** + knowledge graph
- **Agentic RAG (2025):** multi-hop, planning
- **Multimodal RAG (2025+):** text + images + tables

## Chunking strategies
- **Fixed:** 512/1024 tokens (simples)
- **Recursive:** split by markers
- **Semantic:** by paragraph/section
- **Sliding window:** overlap chunks
- **Late chunking:** embed first, chunk after
- **Document-aware:** by structure

## Retrieval
- **Dense:** vector similarity (Pinecone, Weaviate, Qdrant)
- **Sparse:** BM25 (Elasticsearch)
- **Hybrid:** RRF (Reciprocal Rank Fusion) or weighted
- **Reranking:** cross-encoder (Cohere Rerank, BGE-reranker)
- **HyDE:** Hypothetical Document Embedding

## Eval frameworks
- **RAGAS** — faithfulness, answer relevance, context precision
- **TruLens** — feedback loops
- **DeepEval** — pytest-style RAG eval
- **Tonic Validate** — enterprise

## Templates
1. RAG architecture template
2. Chunking experiment design
3. Hybrid retrieval setup
4. Reranking integration
5. RAG eval pipeline (RAGAS)
6. Production RAG monitoring

## Cross-references
- [[obsidian-rag-corpus-engineering]] · [[obsidian-semantic-search]] · [[oraculo-evaluation-frameworks]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **oraculo-rag-research** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in oraculo-rag-research:**

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
