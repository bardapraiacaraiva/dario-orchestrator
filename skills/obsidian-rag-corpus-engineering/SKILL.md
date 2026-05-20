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
