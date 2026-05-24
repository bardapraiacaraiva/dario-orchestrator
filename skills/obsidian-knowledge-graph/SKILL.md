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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **obsidian-knowledge-graph** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in obsidian-knowledge-graph:**

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
