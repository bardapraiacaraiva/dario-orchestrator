---
name: diva-roadmap
description: "Synthesize a complete project roadmap from diagnose + briefing + budget + timeline into one visual deliverable. The 'big picture' document for client presentation. Generates HTML visual roadmap with phases, milestones, budget allocation, team, and key decisions. Triggers on \"roadmap\", \"plano geral\", \"visao geral projecto\", \"mapa do projecto\", \"apresentacao projecto\", \"big picture\", \"plano completo\"."
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# DIVA Roadmap — Complete Project Synthesis

Generate a single, comprehensive project roadmap that synthesizes ALL project data into one client-ready deliverable. This is the "filme completo" — from briefing to entrega.

## When to activate

Invoke `/diva-roadmap` when:
- Client needs to see "the full picture" before approving
- After diagnose + briefing are complete, to present the plan
- Before signing contract, to align expectations
- User says "mostra-me o plano todo", "big picture", "roadmap"

## Workflow

### 1. Gather all existing project data
Search for completed deliverables:
```
mcp__dario-rag__search_kb(query: "<project name> diagnostico briefing", collection: "diva", limit: 5)
```
Check agent memory for project file.
Check Obsidian vault for existing outputs.

### 2. Synthesize 7 sections

**A. Resumo Executivo** (5 linhas max)
- O que: tipo de projecto + localizacao + area
- Quanto: orcamento total (3 cenarios se disponivel)
- Quando: prazo total estimado
- Como: fases principais
- Porquê: objectivo do cliente

**B. Equipa e Responsabilidades**
| Papel | Quem | Responsabilidade |
| Arquitecto | | Projecto, coordenacao |
| Designer interiores | | Conceito, materiais |
| Empreiteiro | | Execucao |
| Fiscal | | Qualidade, conformidade |
| Engenheiros | | Especialidades |

**C. Timeline Visual** (Gantt simplificado em texto/HTML)
```
M1  M2  M3  M4  M5  M6  M7  M8  M9  M10 M11 M12
|===PROJECTO====|
         |==LICEN==|
                    |===DEMOLICAO+ESTRUTURA====|
                              |===MEP+ACABAMENTOS=======|
                                          |===CARPINT+EQUIP==|
                                                    |==ENTREGA|
```

**D. Budget Overview**
| Fase | % | EUR (recomendado) |
| Projecto + honorarios | 12% | |
| Licenciamento | 2% | |
| Construcao | 70% | |
| Equipamentos | 8% | |
| Contingencia | 8% | |

**E. Design Direction**
- Estilo identificado + designer de referencia
- Paleta de cores (3-5 cores com hex)
- Materiais-chave (pavimento, paredes, bancada)
- 1 render conceptual ou Midjourney prompt

**F. Milestones de Decisao**
| # | Decisao | Prazo | Quem decide |
| 1 | Aprovar conceito/moodboard | Semana X | Cliente |
| 2 | Adjudicar empreiteiro | Semana X | Cliente |
| 3 | Aprovar materiais | Semana X | Cliente + Designer |
| 4 | Aprovar cozinha | Semana X | Cliente |
| 5 | Inspeccao pre-acabamentos | Semana X | Fiscal |
| 6 | Punch list final | Semana X | Todos |

**G. Riscos e Mitigacao**
| Risco | Probabilidade | Impacto | Mitigacao |
Top 5 riscos identificados com plano.

### 3. Generate HTML deliverable

Usar `mcp__aidesigner__generate_design` para criar um HTML visual bonito com:
- Header com nome do projecto + morada
- Timeline visual (SVG bars coloridas)
- Budget donut chart (SVG)
- Team cards
- Material palette visual
- Milestone checklist

OU gerar como Markdown premium para Obsidian/PDF.

### 4. Save
- HTML: `[projecto]-roadmap.html`
- Markdown: Obsidian `05 - Claude - IA/Outputs/YYYY-MM-DD - [Projecto] - Roadmap.md`

## Output template

```markdown
---
project: <nome>
date: <YYYY-MM-DD>
type: roadmap
diva_specializations: [all relevant]
budget_total: <EUR>
timeline_months: <N>
---

# Roadmap — <Projecto>

## Resumo Executivo
<5 linhas>

## Equipa
<tabela>

## Timeline
<gantt visual>

## Budget
<breakdown com 3 cenarios>

## Design Direction
<estilo + paleta + materiais + render concept>

## Milestones de Decisao
<tabela com datas e responsaveis>

## Riscos
<top 5 com mitigacao>

## Proximos Passos Imediatos
1. <accao>
2. <accao>
3. <accao>
```

## Red flags
- Nunca apresentar roadmap sem orcamento (mesmo estimado)
- Nunca omitir riscos — honestidade constroi confianca
- Nunca dar datas absolutas sem margem (sempre "Semana X +-1")
- Incluir SEMPRE disclaimer de precos estimados
