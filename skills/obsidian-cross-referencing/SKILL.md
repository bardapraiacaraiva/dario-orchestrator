---
name: obsidian-cross-referencing
description: Backlinks, citations, link integrity. Wikilinks, bibliographic citations (Zotero, BibTeX), broken link detection. Triggers em "backlinks", "citations", "Zotero", "BibTeX", "Wikilinks", "broken links".
license: MIT
parent_agent: obsidian-director
compliance: [audit_trail]
---

# OBSIDIAN-CROSS-REFERENCING

## Quando usar
- Bootstrap citation system (academic/research)
- Backlink hygiene em vault grande
- Migration: footnotes → Zotero integration
- Broken link detection
- Citation export para papers/posts

## Stack
- **Zotero:** open-source reference manager (líder acadêmico)
- **Better BibTeX:** export para LaTeX/Pandoc
- **Obsidian Citations plugin:** Zotero ↔ Obsidian bridge
- **Pandoc:** convert formats with citations
- **Hypothes.is:** web annotation + collaborative

## Princípios
- **Cite everything:** mesmo notes pessoais
- **Capture metadata at source:** Zotero connector browser
- **Stable IDs:** DOI > URL > author-year
- **Citation style consistency:** APA / Chicago / Vancouver
- **Backlink density:** notas órfãs são red flag

## Templates
1. Zotero → Obsidian setup (Better BibTeX + Obsidian Citations)
2. Literature note template com `@cite-key`
3. Bibliography export (BibTeX, CSL-JSON)
4. Broken link audit script
5. Backlink density report (orphan notes detection)

## Cross-references
- [[obsidian-atomic-notes]] · [[obsidian-zettelkasten-method]] · [[obsidian-knowledge-base-curation]]
