---
name: orion-prd-writing
description: PRDs production-grade. Problem, solution, success metrics, edge cases, rollout. Triggers em "PRD", "product requirements", "spec", "feature spec", "product brief".
license: MIT
parent_agent: orion-director
compliance: [data_privacy_by_design]
---

# ORION-PRD-WRITING

## Quando usar
- Escrever PRD para nova feature
- Refactor PRDs legados (sem success metrics? sem edge cases?)
- Template de PRD para a empresa toda
- One-pager vs full PRD decision
- RFC technical para mudanças arquiteturais

## Estrutura PRD (production-grade)
```
1. Problem statement (the WHY)
2. Target users + JTBD
3. Success metrics (leading + lagging)
4. Solution overview
5. User stories + acceptance criteria
6. Edge cases + error states
7. Out of scope (explicit)
8. Dependencies + risks
9. Rollout plan (flag, %, segments)
10. Launch checklist
```

## Princípios
- **WHY antes de WHAT:** problem clarity > solution detail
- **Success metrics explícitas:** "ship it when X = Y"
- **Edge cases listados:** ambiguity = bugs
- **Out of scope explícito:** previne scope creep
- **Single owner:** nome do PM no top

## Templates
1. PRD full (Notion/Confluence)
2. One-pager (RFC-style)
3. Mini-PRD para experiments
4. PRD template específico para growth experiments
5. RFC técnico para arquitetura

## Cross-references
- [[orion-product-discovery]] · [[orion-prioritization]] · [[builder-prd-complete]]
