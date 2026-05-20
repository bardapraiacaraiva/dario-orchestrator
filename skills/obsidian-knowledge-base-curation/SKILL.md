---
name: obsidian-knowledge-base-curation
description: KB maintenance — content decay detection, quality scoring, dedup, governance. Triggers em "knowledge base", "KB curation", "content decay", "knowledge governance", "dedup".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification, audit_trail, retention_policies]
---

# OBSIDIAN-KNOWLEDGE-BASE-CURATION

## Quando usar
- KB com 1000+ docs, qualidade unknown
- Customer-facing help center
- Internal wiki cleanup
- AI-readable docs (RAG-source)
- Documentation governance program

## Curation pillars
1. **Freshness:** detectar stale content (>180d sem update)
2. **Quality:** completeness + accuracy + clarity scores
3. **Coverage:** gap analysis (what's missing)
4. **Dedup:** near-duplicates merge
5. **Findability:** internal search works?
6. **Governance:** owner per doc, review cadence

## Templates
1. Doc metadata schema (owner + reviewer + last_review + ttl)
2. Content audit dashboard (freshness + quality + traffic)
3. Quality rubric (0-100 score)
4. Dedup detection (MinHash / SimHash)
5. Doc lifecycle workflow (draft → review → publish → archive)
6. Knowledge gaps report (queries com 0 results)

## Métricas chave
- **Coverage:** % search queries with relevant results
- **Freshness:** mediana de days-since-update
- **Quality:** % docs com all metadata + review recent
- **Trust:** % usuários que dão upvote em answer
- **Reduction:** support tickets evitados por self-service

## Cross-references
- [[obsidian-search-relevance]] · [[demeter-data-quality]] · [[risco-rgpd]]
