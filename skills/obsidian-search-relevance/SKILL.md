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
