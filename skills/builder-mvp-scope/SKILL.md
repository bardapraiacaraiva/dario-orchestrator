---
name: builder-mvp-scope
description: >
  Define o scope minimo viavel: o que entra no MVP, o que fica para depois. Cut ruthlessly.
  Prioritiza por impacto vs esforco. Timeline realista. Tech debt budget.
  Use quando: MVP, scope, o que construir primeiro, priorizar features, minimum viable.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — MVP Scope Definition

## Proposito
Cortar sem piedade. O MVP e o MINIMO que valida a hipotese, nao "a versao 1 com tudo".

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-mvp-scope [produto]` | Scope MVP completo |
| `/builder-mvp-scope cut [feature-list]` | Decidir o que cortar |
| `/builder-mvp-scope ice [features]` | ICE scoring (Impact, Confidence, Ease) |

## Framework: ICE Scoring

| Feature | Impact (1-10) | Confidence (1-10) | Ease (1-10) | ICE Score | Decision |
|---------|--------------|-------------------|-------------|-----------|----------|
| Auth | 10 | 10 | 8 | 800 | MVP |
| Dashboard | 8 | 9 | 7 | 504 | MVP |
| Team collab | 6 | 5 | 3 | 90 | V1.1 |
| AI feature | 9 | 4 | 2 | 72 | V1.2 |

**Rule:** ICE > 300 = MVP. ICE 100-300 = V1.1. ICE < 100 = Backlog.

## MVP Checklist
- [ ] Resolve the #1 pain point (only one!)
- [ ] Can a user complete the core job-to-be-done?
- [ ] Can be built in <= 4 weeks?
- [ ] Has a measurable success metric?
- [ ] Tech debt budget: max 20% of MVP time

## Output
1. Feature priority matrix (ICE scored)
2. MVP cut list (IN vs OUT)
3. V1.1 backlog (what was cut and why)
4. Timeline (realistic, with buffer)
5. Tech debt budget allocation
