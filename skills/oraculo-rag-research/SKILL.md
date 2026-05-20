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
