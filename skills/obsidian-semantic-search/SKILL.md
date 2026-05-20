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
