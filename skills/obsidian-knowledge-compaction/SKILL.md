---
name: obsidian-knowledge-compaction
description: Knowledge compaction — summarization, distillation, progressive summarization, abstract generation. Triggers em "summarization", "compaction", "progressive summarization", "distill", "abstract generation".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification, audit_trail]
---

# OBSIDIAN-KNOWLEDGE-COMPACTION

## Quando usar
- Long-form → executive summary
- RAG context window optimization (compactar antes de retrieve)
- Newsletter / digest generation
- Meeting notes → action items
- Research synthesis (N papers → 1 summary)

## Técnicas
- **Progressive summarization (Forte):** highlight → bold → 1-liner
- **Extractive:** top sentences (TextRank, BERT)
- **Abstractive:** LLM-generated novel sentences
- **Hierarchical:** summary of summaries (recursive)
- **Query-focused:** sumariza apenas o relevante para pergunta X
- **Map-reduce:** chunks paralelos → merge final

## Stack
- **LangChain summarization chains** (stuff / map_reduce / refine)
- **LlamaIndex** (response synthesis modes)
- **Anthropic Contextual retrieval:** chunk + situated summary
- **OpenAI GPT-4o** + Claude Opus para abstractive
- **BART / Pegasus** para extractive/abstractive open-source

## Templates
1. Progressive summarization markup convention
2. Map-reduce summarization pipeline
3. Query-focused summarization prompt
4. Meeting notes → action items extractor
5. Research synthesis workflow (N papers → matrix → narrative)

## Métricas
- **ROUGE-1/2/L:** automatic vs reference (limitations)
- **Faithfulness:** factual em relação ao source (LLM-judge)
- **Compression ratio:** input/output token ratio
- **Information retention:** can answer same Qs from summary?

## Cross-references
- [[obsidian-rag-corpus-engineering]] · [[orion-product-discovery]] · [[demeter-data-storytelling]]
