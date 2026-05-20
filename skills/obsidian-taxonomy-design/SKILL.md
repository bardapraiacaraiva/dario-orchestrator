---
name: obsidian-taxonomy-design
description: Taxonomy design — controlled vocabularies, faceted classification, hierarchical vs flat. Triggers em "taxonomy", "controlled vocabulary", "faceted classification", "tagging strategy".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification]
---

# OBSIDIAN-TAXONOMY-DESIGN

## Quando usar
- Tag system from chaos to structure
- E-commerce product categorization
- Content management taxonomy
- Search facet design
- Migration: free-tagging → controlled vocab

## Princípios (ANSI/NISO Z39.19)
- **Mutually exclusive:** termo X não fica em 2 categorias
- **Collectively exhaustive:** cobre todo o universo
- **Hierarchical:** broader/narrower/related (BT/NT/RT)
- **Synonym control:** "preferred term" + variants
- **Faceted:** múltiplas dimensões ortogonais

## Estruturas
- **Hierarchical (tree):** clássico, profundidade variável
- **Faceted:** múltiplas dimensões (color × size × material)
- **Polyhierarchy:** termo em múltiplos parents
- **Flat (folksonomy):** tags livres com normalization

## Templates
1. Taxonomy spec template (terms + definitions + synonyms + relations)
2. Faceted classification spec (facets × values)
3. Controlled vocab governance (Term Council, RFC process)
4. Tag normalization workflow (free → controlled)
5. SKOS export (RDF-compatible)

## Cross-references
- [[obsidian-ontology-modeling]] · [[obsidian-knowledge-graph]] · [[obsidian-search-relevance]]
