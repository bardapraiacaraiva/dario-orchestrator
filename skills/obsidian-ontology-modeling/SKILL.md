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
