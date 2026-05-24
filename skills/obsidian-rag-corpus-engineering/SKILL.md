---
name: obsidian-rag-corpus-engineering
description: RAG corpus engineering — chunking strategies, embedding model selection, retrieval evaluation. Triggers em "RAG corpus", "chunking", "retrieval evaluation", "RAG engineering", "vector database".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification, access_control, audit_trail]
---

# OBSIDIAN-RAG-CORPUS-ENGINEERING

## Quando usar
- Greenfield RAG system (chunking + embed + retrieve)
- Auditar RAG existente (qual é recall@10?)
- Chunking strategy tuning
- Embedding model A/B
- Hybrid retrieval (BM25 + vector)

## Chunking strategies
- **Fixed size:** 512/1024 tokens (simples, perde context)
- **Semantic:** por parágrafo/section (mantém coerência)
- **Recursive:** split por marker → menor unit (LangChain RecursiveCharacterTextSplitter)
- **Late chunking (Jina):** embed full → chunk depois (preserva long-context)
- **Contextual retrieval (Anthropic):** chunk + summary do contexto

## Embedding models
- **OpenAI text-embedding-3-large:** 3072 dims, GA standard
- **Cohere embed-multilingual-v3:** multilingual líder
- **BGE-m3 (BAAI):** multilingual + multi-functionality
- **nomic-embed-text:** open-source, local, 768 dims
- **mxbai-embed-large:** open-source SOTA

## Evaluation
- **Recall@K:** % relevant chunks no top-K
- **MRR (Mean Reciprocal Rank):** posição da primeira relevante
- **NDCG:** ranking-aware metric
- **Faithfulness:** answer fundamentado no chunk (LLM-as-judge)

## Templates
1. Chunking strategy decision tree
2. RAG eval pipeline (TREC-style)
3. Embedding A/B test framework
4. Hybrid retrieval setup (BM25 + vector + reranking)
5. RAG observability dashboard

## Cross-references
- [[obsidian-semantic-search]] · [[obsidian-embedding-models]] · [[obsidian-search-relevance]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **obsidian-rag-corpus-engineering** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in obsidian-rag-corpus-engineering:**

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
