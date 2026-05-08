---
name: builder-smart-context
description: >
  Seleccao inteligente de contexto para builder skills. Em vez de enviar todo o projecto
  ao LLM, score ficheiros por relevancia e inclui apenas os necessarios. Reduz tokens 60-80%.
  Inspirado em Dyad (8K stars). Use quando: optimizar contexto, reduzir tokens, smart context.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Smart Context Selector (Dyad pattern)

## Proposito
Quando um builder skill precisa de contexto do projecto, NAO enviar tudo.
Score ficheiros por relevancia e incluir apenas os top-N. Savings: 60-80% tokens.

## Como funciona

### 1. Recebe pedido do builder skill
```
Skill: builder-landing-page
Task: "Gerar hero section para SaaS de contabilidade"
```

### 2. Score ficheiros do projecto por relevancia
```
tailwind.config.ts     → 0.95 (design tokens — ESSENTIAL)
package.json           → 0.80 (dependencies — IMPORTANT)
app/layout.tsx         → 0.75 (root layout — IMPORTANT)
components/ui/button.tsx → 0.60 (existing component — RELEVANT)
db/schema.ts           → 0.15 (database — NOT RELEVANT for hero)
lib/auth.ts            → 0.10 (auth — NOT RELEVANT)
```

### 3. Include top-N ate token budget
```
Token budget: 4000 tokens
Include: tailwind.config.ts + package.json + app/layout.tsx + button.tsx
Skip: db/schema.ts, lib/auth.ts (irrelevant to hero section)
Savings: ~70% vs including everything
```

### Scoring Rules
| Factor | Weight | Description |
|---|---|---|
| Filename match | 0.4 | File name contains task keywords |
| Import chain | 0.3 | File is imported by target file |
| Recency | 0.2 | Recently modified = more relevant |
| Size penalty | 0.1 | Very large files scored down |

## Integration
- Runs BEFORE every builder skill prompt assembly
- Configurable token budget per skill (default 4000)
- Caches scores per session (same project = same scores)

## Inspired by
- **dyad-sh/dyad** (8K stars) — Smart Context auto-selection
