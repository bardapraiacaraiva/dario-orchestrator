---
name: obsidian-knowledge-graph
description: Knowledge graph design — nodes, edges, ontology, graph traversal. Neo4j, Memgraph, RDF, property graphs. Triggers em "knowledge graph", "Neo4j", "graph database", "ontology", "RDF", "SPARQL".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification, access_control]
---

# OBSIDIAN-KNOWLEDGE-GRAPH

## Quando usar
- Greenfield knowledge graph (concept extraction + relations)
- Migrar tabelas relacionais → graph (quando relacionamentos complexos)
- GraphRAG (RAG potenciado por graph traversal)
- Entity resolution + deduplication
- Recommendation engines (similar nodes)

## Stack
- **Neo4j** (líder property graph)
- **Memgraph** (Cypher-compatible, faster)
- **TigerGraph** (analytics)
- **Amazon Neptune** (managed, RDF + property)
- **Apache TinkerPop / Gremlin** (graph traversal)
- **GraphRAG (Microsoft)** — RAG + community detection

## Princípios
- **Schema clarity:** node types + edge types nomeados
- **Edge direction matters:** semântica clara
- **Properties on edges:** "weight", "created_at", "confidence"
- **Indexing strategy:** lookup vs traversal vs full-text

## Templates
1. Neo4j schema design (Cypher CREATE CONSTRAINT)
2. Entity extraction pipeline (NER + relation extraction)
3. GraphRAG retrieval pattern
4. Graph algorithms (PageRank, community detection)
5. Visualization with Bloom / yWorks

## Cross-references
- [[obsidian-ontology-modeling]] · [[obsidian-rag-corpus-engineering]] · [[obsidian-semantic-search]]
