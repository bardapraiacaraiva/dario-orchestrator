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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **obsidian-taxonomy-design** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in obsidian-taxonomy-design:**

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
