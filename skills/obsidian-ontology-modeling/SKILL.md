---
name: obsidian-ontology-modeling
description: Ontology modeling — RDF, OWL, classes, properties, axioms. Schema.org, FOAF, SKOS. Triggers em "ontology", "OWL", "RDF", "Schema.org", "FOAF", "SKOS", "semantic web".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification, audit_trail]
---

# OBSIDIAN-ONTOLOGY-MODELING

## Quando usar
- Domain model formal (saúde, finance, manufacturing)
- Data integration cross-system
- Schema.org SEO markup
- Linked Data publication
- Reasoning sobre dados (inference)

## Stack
- **RDF/RDFS:** triple-based data model
- **OWL 2:** ontology logic (DL profile = decidable)
- **SHACL:** shape constraint validation
- **SKOS:** thesauri + concept schemes
- **Schema.org:** web-scale ontology (Google/Bing-aligned)
- **Protégé:** desktop editor

## Princípios
- **Reuse over reinvent:** Schema.org first, FOAF, Dublin Core
- **Conservative axioms:** disjointness sparing
- **Naming conventions:** CamelCase classes, lowerCamelCase properties
- **Ontology metadata:** version + license + owner
- **Modular:** import sub-ontologies

## Templates
1. RDFS ontology skeleton (classes + properties)
2. Schema.org JSON-LD com BlogPosting + Person + Organization
3. SHACL shape para validação
4. SKOS thesaurus structure (Concept + broader/narrower)
5. OWL 2 DL ontology com restrições

## Cross-references
- [[obsidian-taxonomy-design]] · [[obsidian-knowledge-graph]] · [[seo-schema]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **obsidian-ontology-modeling** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in obsidian-ontology-modeling:**

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
