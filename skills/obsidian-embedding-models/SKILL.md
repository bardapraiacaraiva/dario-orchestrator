---
name: obsidian-embedding-models
description: Embedding model selection, fine-tuning, evaluation. OpenAI, Cohere, BGE, nomic, sentence-transformers. Triggers em "embedding model", "fine-tune embedding", "OpenAI embeddings", "Cohere embed", "BGE", "nomic-embed".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification]
---

# OBSIDIAN-EMBEDDING-MODELS

## Quando usar
- Escolher embedding model (greenfield)
- A/B test models on YOUR data
- Fine-tune model em domain
- Multilingual setup
- Cost vs quality trade-off (managed vs self-host)

## Landscape (2026)
**Managed:**
- OpenAI text-embedding-3-large (3072 dims, $0.13/M tokens)
- Cohere embed-multilingual-v3 (1024 dims, $0.10/M)
- Voyage AI (multimodal, +finance-tuned)

**Open-source SOTA:**
- BGE-m3 (BAAI, multilingual, 1024 dims)
- mxbai-embed-large (1024 dims, English líder)
- nomic-embed-text-v1.5 (768 dims, Matryoshka)
- gte-large (Alibaba, 1024 dims)
- jina-embeddings-v3 (long-context 8K)

## Critérios de seleção
- **MTEB benchmark:** standard reference
- **Domain match:** finance/medical/legal precisam tuned
- **Language coverage:** PT-BR é tricky
- **Dimensions:** 384/768/1024/3072 (storage trade-off)
- **Long-context:** >2K tokens precisa late chunking
- **Cost:** managed vs self-host TCO

## Fine-tuning
- **MTEB benchmark:** standard reference para SOTA
- **MultipleNegativesRankingLoss:** contrastive standard
- **Train data:** anchor-positive pairs (5K-50K) suficiente
- **Hardware:** A100 ~4-8h
- **Eval:** holdout test set + production A/B

## Templates
1. Embedding model selection scorecard
2. Fine-tuning pipeline (sentence-transformers)
3. MTEB evaluation runner
4. Production A/B test setup
5. Embedding version migration plan

## Cross-references
- [[obsidian-semantic-search]] · [[obsidian-rag-corpus-engineering]] · [[demeter-ml-pipelines]]
