---
name: diva-timeline
description: Construction project timeline/Gantt generator for architecture and renovation projects in Portugal. Phases from projecto through entrega with dependencies and critical path. Triggers on "cronograma", "timeline", "quanto tempo", "duracao obra", "gantt", "planeamento obra".
license: MIT
---

# DIVA Skill — Construction Timeline / Gantt Generator

Generates a detailed construction timeline for architecture, renovation, and new-build projects in Portugal. Covers all phases from design through handover, with realistic durations, dependencies, critical path identification, and parallel activity mapping. Calibrated for Portuguese construction market realities (licensing delays, holiday periods, subcontractor availability).

## When to activate

- Client asks "quanto tempo demora a obra?"
- Project kickoff requiring a construction schedule
- Contractor coordination meeting preparation
- Client presentation needing a visual timeline
- Budget planning requiring phase-by-phase cost allocation
- Comparing fast-track vs standard timelines
- Renovation vs new-build scheduling

## Workflow

### 1. Gather inputs

- **Project type:** new build / full renovation / partial renovation / interior fit-out
- **Scope:** total area (m2), number of floors, complexity level (simple/medium/complex)
- **Location:** municipality (affects licensing times)
- **Heritage zone?** yes/no (DGPC involvement adds 2-4 months)
- **Structural work?** yes/no (affects licensing type and duration)
- **MEP complexity:** standard / complex (underfloor heating, HVAC, home automation)
- **Client constraints:** hard deadline? phased occupancy? budget-driven pace?
- **Season start:** month/year (winter = rain delays on exterior work)
- **Known risks:** asbestos removal, archaeological finds, neighbor disputes

If project type or scope is missing, stop and ask.

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "construction timeline phases duration Portugal", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "licenciamento prazos camara municipal RJUE", collection: "dario", limit: 5)
```

### 3. Define phases with default durations

Apply these baseline durations, then adjust per project inputs:

| # | Phase | Duration (weeks) | Depends on | Parallel with |
|---|---|---|---|---|
| 1 | Projecto (design + engineering) | 4-8 | -- | -- |
| 2 | Licenciamento (permits) | 4-12 | 1 | -- |
| 3 | Concurso / selecao empreiteiro | 2-3 | 1 | 2 (partial) |
| 4 | Preparacao de obra (site setup) | 2 | 2, 3 | -- |
| 5 | Demolicao / strip-out | 1-2 | 4 | -- |
| 6 | Estrutura (structural) | 2-4 | 5 | -- |
| 7 | Alvenaria (masonry/partitions) | 2-3 | 6 | -- |
| 8 | MEP rough-in (canalizacao, electricidade, AVAC) | 2-3 | 7 | 7 (partial overlap) |
| 9 | Impermeabilizacao + isolamento | 1-2 | 8 | -- |
| 10 | Acabamentos (revestimentos, pinturas) | 3-4 | 9 | -- |
| 11 | Carpintaria (portas, armarios, cozinha) | 2-3 | 10 | 10 (partial overlap) |
| 12 | Equipamentos (sanitarios, iluminacao, electrodomesticos) | 1-2 | 11 | 11 (partial overlap) |
| 13 | Remates e correcoes | 1-2 | 12 | -- |
| 14 | Limpeza final + entrega | 1 | 13 | -- |

### 4. Adjust durations

Apply multipliers based on inputs:
- **Heritage zone:** +50% on phases 2, 5, 6
- **Complex MEP (AVAC/domotic):** +50% on phase 8
- **Area > 200m2:** +25% on phases 6-12
- **Winter start (Nov-Feb):** +20% on exterior phases (5, 6, 9)
- **Full renovation of old building:** +30% on phases 5, 6 (unknowns in existing structure)
- **Interior fit-out only (no structure):** skip phases 5, 6; reduce total by 40%

### 5. Identify critical path

Mark the longest sequential chain. Typically:
`Licenciamento -> Preparacao -> Demolicao -> Estrutura -> Alvenaria -> MEP -> Acabamentos -> Remates -> Entrega`

Highlight phases where delays cascade most (usually licenciamento and estrutura).

### 6. Map parallel activities

- Furniture procurement can start during phase 7
- Kitchen manufacturing starts during phase 8 (6-8 week lead time)
- Custom joinery orders placed during phase 7
- Client material selections must be finalized before phase 10

### 7. Add milestones and decision gates

- **M1:** Project approved / design signed off
- **M2:** License granted (alvara / comunicacao previa aceite)
- **M3:** Contractor selected, contract signed
- **M4:** Structure complete (structural sign-off)
- **M5:** MEP rough-in complete (pre-wall-close inspection)
- **M6:** Finishes complete (pre-punch-list walkthrough)
- **M7:** Handover (auto de recepcao)

## Output template

```markdown
---
project: <project name>
date: <YYYY-MM-DD>
type: construction-timeline
total_duration_weeks: <N>
critical_path_weeks: <N>
---

# Cronograma de Obra -- <Project Name>

## Resumo
- **Tipo:** <new build / full renovation / partial renovation / fit-out>
- **Area:** <N> m2
- **Duracao total estimada:** <N> semanas (<N> meses)
- **Caminho critico:** <N> semanas
- **Inicio previsto:** <date>
- **Entrega prevista:** <date>

## Timeline (Gantt simplificado)

| Semana | 1-4 | 5-8 | 9-12 | 13-16 | 17-20 | 21-24 | 25-28 | 29-32 |
|--------|-----|-----|------|-------|-------|-------|-------|-------|
| Projecto | ████ | | | | | | | |
| Licenciamento | | ████ | ████ | | | | | |
| Selecao empreiteiro | | ████ | | | | | | |
| Preparacao obra | | | | ██ | | | | |
| Demolicao | | | | ██ | | | | |
| Estrutura | | | | | ████ | | | |
| Alvenaria | | | | | | ███ | | |
| MEP rough-in | | | | | | ███ | | |
| Acabamentos | | | | | | | ████ | |
| Carpintaria | | | | | | | ███ | |
| Equipamentos | | | | | | | | ██ |
| Remates | | | | | | | | ██ |
| Limpeza + entrega | | | | | | | | █ |

## Fases detalhadas

### Fase 1: Projecto (<N> semanas)
- **Actividades:** projecto de arquitectura, especialidades (estrutura, MEP, termica, acustica)
- **Decisoes necessarias:** layout final, materiais-chave, orcamento aprovado
- **Entregaveis:** projecto completo para licenciamento

### Fase 2: Licenciamento (<N> semanas)
- **Tipo de procedimento:** <comunicacao previa / licenciamento / isento>
- **Entidade:** Camara Municipal de <municipio>
- **Risco:** aprovacao tacita apos <N> dias se sem resposta

[... repeat for each phase ...]

## Caminho critico
<Sequence of phases that determine minimum project duration>

## Actividades paralelas
| Actividade | Iniciar durante fase | Lead time |
|---|---|---|
| Encomenda cozinha | Fase 8 | 6-8 semanas |
| Encomenda carpintaria | Fase 7 | 4-6 semanas |
| Selecao mobiliario | Fase 7 | 4-8 semanas |
| Selecao materiais acabamentos | Fase 8 | 2-4 semanas |

## Milestones
| Marco | Data prevista | Criterio |
|---|---|---|
| M1 - Projecto aprovado | <date> | Cliente assina projecto final |
| M2 - Licenca obtida | <date> | Alvara emitido pela camara |
| M3 - Empreiteiro contratado | <date> | Contrato assinado |
| M4 - Estrutura completa | <date> | Vistoria estrutural aprovada |
| M5 - MEP rough-in completo | <date> | Inspecao pre-fecho paredes |
| M6 - Acabamentos completos | <date> | Walkthrough pre-punch-list |
| M7 - Entrega | <date> | Auto de recepcao assinado |

## Riscos e contingencias
| Risco | Probabilidade | Impacto (semanas) | Mitigacao |
|---|---|---|---|
| Atraso licenciamento | Alta | +4-8 | Submeter completo, follow-up semanal |
| Chuva em fase exterior | Media | +2-3 | Planear exteriores para primavera/verao |
| Subcontratador indisponivel | Media | +2-4 | Reservar com antecedencia, ter alternativa |
| Descoberta de amianto | Baixa | +3-4 | Inspecao pre-obra, orcamento contingencia |

## Proximos passos
- [ ] Validar cronograma com empreiteiro
- [ ] Confirmar prazos de licenciamento com camara
- [ ] Alinhar encomendas de materiais com lead times
- [ ] Agendar reunioes de obra semanais
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Project> - Cronograma de Obra.md`

## Red Flags
- Never ignore the critical path — if licenciamento or estrutura slips, every downstream phase cascades and the client loses weeks they cannot recover
- Never forget camara municipal lead times (30-45 dias uteis minimum, often 3-4 months in practice) — submitting incomplete documentation resets the clock entirely
- Always include a buffer of 15-20% on total duration for weather delays, subcontractor no-shows, and material lead times — Portuguese construction routinely overruns and clients must plan cash flow accordingly
- Never overlap incompatible phases (e.g., structure and MEP rough-in without structural sign-off, or finishing and wet trades) — rework from premature phase starts costs more than the time saved
- Never schedule exterior work or critical deliveries during August or between Christmas and New Year — Portugal effectively shuts down and supply chains halt
- Always flag the rain season (October-March) as a risk multiplier for any exterior or foundation work — a two-week rain stretch can push the schedule by a month

## Interactions

- Pair with `diva-licensing` for detailed permit timeline within phase 2
- Pair with `diva-inspection` for quality gates at each milestone
- Follow up with `dario-proposal` for client-facing timeline in commercial proposal
- Save via `dario-obsidian-save` to vault
