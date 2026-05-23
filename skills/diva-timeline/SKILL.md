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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Inputs recolhidos e suficientes para gerar cronograma

- [ ] Tipo de projeto especificado (new build / full renovation / partial renovation / fit-out)
- [ ] Área em m² confirmada ou estimada com base em descrição do cliente
- [ ] Município identificado (afeta prazos de licenciamento)
- [ ] Mês/ano de início previsto registado (impacto de sazonalidade)
- [ ] Obra em zona de património ou com estrutura? Respondido explicitamente

❌ NOT delivery-ready: "Licenciamento: 4-12 semanas (dependendo do município)"
✅ Delivery-ready: "Licenciamento: 10 semanas — estimativa para Lisboa (Alvará, zona histórica Mouraria, DGPC envolvida)"

---

### Gate 2 — Durações ajustadas com multiplicadores aplicados

- [ ] Multiplicadores de heritage zone, area >200m², MEP complexo, inverno aplicados e documentados
- [ ] Total de semanas recalculado após ajustes (não os defaults brutos)
- [ ] Fases skipped (ex: fases 5-6 em fit-out) explicitamente indicadas como N/A
- [ ] Ajuste de inverno aplicado se início Nov-Fev

❌ NOT delivery-ready: "Estrutura: 2-4 semanas" (range sem commit)
✅ Delivery-ready: "Estrutura: 5 semanas (base 4 sem × 1,25 por área 220m²) — início Dezembro, +20% exterior = 5,5 sem → arredondado 6 sem"

---

### Gate 3 — Gantt/tabela preenchida com semanas reais, não genéricas

- [ ] Colunas da tabela Gantt correspondem a semanas reais (ex: "Sem 1-4 = Mar 1 – Mar 28")
- [ ] Barras ████ posicionadas de acordo com dependências calculadas, não com template padrão
- [ ] Atividades paralelas (carpintaria, MEP overlap) visíveis na mesma linha de semanas
- [ ] Sem colunas vazias para fases skipped — removidas ou marcadas "N/A"

❌ NOT delivery-ready: Gantt com colunas "1-4 / 5-8 / 9-12" sem datas reais
✅ Delivery-ready: "| Semana 9-14 (Maio–Jun 2025) | | ████████ | | Licenciamento CM Cascais |"

---

### Gate 4 — Caminho crítico identificado e fases de risco nomeadas

- [ ] Critical path explicitamente listado (sequência de fases, total de semanas)
- [ ] Pelo menos 2 fases de risco identificadas com motivo específico ao projeto
- [ ] Impacto de atraso numa fase crítica quantificado ("atraso de 2 semanas em licenciamento → entrega recua para Outubro")
- [ ] Diferença entre caminho crítico e duração total documentada (folga disponível)

❌ NOT delivery-ready: "O licenciamento pode atrasar a obra"
✅ Delivery-ready: "Caminho crítico: 28 semanas. Risco principal: licenciamento CM Sintra — histórico de 10-14 semanas para obras >300m². Atraso de 4 semanas recua entrega de Setembro para Outubro 2025."

---

### Gate 5 — Milestones e encomendas de longo prazo mapeados

- [ ] Os 7 milestones (M1–M7) incluídos com datas estimadas reais
- [ ] Lead times críticos apontados: cozinha (6-8 sem), carpintaria custom, equipamentos especiais
- [ ] Seleções do cliente (materiais, acabamentos) com deadline antes da fase 10 indicada
- [ ] Milestones de inspeção obrigatória (pré-fecho de paredes MEP, auto de receção) presentes

❌ NOT delivery-ready: "M2: Licença concedida — após fase 2"
✅ Delivery-ready: "M2: Alvará concedido — estimativa 15 Mai 2025 (CM Oeiras, comunicação prévia, sem DGPC). Encomenda cozinha IKEA/Snaidero: iniciar em M4 (15 Abr) para entrega semana 22."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets por preencher

- [ ] `<project name>`, `<date>`, `<N>` substituídos por valores reais
- [ ] Município real no lugar de `<município>`
- [ ] Datas de início e entrega em formato DD-MMM-AAAA (ex: 03-Mar-2025)
- [ ] Nenhum placeholder `<...>` visível no output final

❌ NOT delivery-ready: "Entrega prevista: `<date>`" ou "Área: `<N>` m²"
✅ Delivery-ready: "Entrega prevista: 12-Set-2025 | Área: 185 m² | Projeto: Remodelação Vivenda Estoril — Família Monteiro"

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
---
project: Remodelação Apartamento T3 — Cuidai Lisboa
date: 2025-03-10
type: construction-timeline
total_duration_weeks: 32
critical_path_weeks: 28
---

# Cronograma de Obra — Apartamento T3, Av. Almirante Reis 114, Lisboa

## Resumo
- **Tipo:** Full renovation (sem obra estrutural)
- **Área:** 145 m²
- **Duração total estimada:** 32 semanas (~8 meses)
- **Caminho crítico:** 28 semanas
- **Início previsto:** 07-Abr-2025
- **Entrega prevista:** 03-Nov-2025
- **Município:** Lisboa (CM Lisboa — Comunicação Prévia, zona não patrimonial)

## Ajustes aplicados
| Fator | Fase afetada | Multiplicador | Semanas base → ajustadas |
|---|---|---|---|
| Inverno (início Abr, exterior mínimo) | N/A | 1,0× | — |
| MEP complexo (AVAC + domótica KNX) | Fase 8 | 1,5× | 2 sem → 3 sem |
| Área 145 m² (<200 m²) | Fases 6-12 | 1,0× | sem ajuste |
| Sem zona patrimonial | Fase 2 | 1,0× | sem ajuste |

Fases 5 e 6 (demolição estrutural, estrutura) reduzidas — apenas strip-out leve,
sem intervenção estrutural.

## Timeline (Gantt simplificado)

| Fase | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov |
|---|---|---|---|---|---|---|---|---|
| Projecto (4 sem) | ████ | | | | | | | |
| Licenciamento CM Lisboa (8 sem) | | ████ | ████ | | | | | |
| Selecção empreiteiro (3 sem) | ███ | | | | | | | |
| Preparação obra (2 sem) | | | | ██ | | | | |
| Strip-out / demolição ligeira (1 sem) | | | | █ | | | | |
| Alvenaria / divisórias (2 sem) | | | | | ██ | | | |
| MEP rough-in AVAC+KNX (3 sem) | | | | | ███ | | | |
| Impermeabilização + isolamento (2 sem) | | | | | | ██ | | |
| Acabamentos / pinturas (4 sem) | | | | | | ████ | | |
| Carpintaria custom Tiago Móveis (3 sem) | | | | | | ███ | | |
| Equipamentos sanitários + iluminação (2 sem) | | | | | | | ██ | |
| Remates e correcções (2 sem) | | | | | | | ██ | |
| Limpeza final + entrega (1 sem) | | | | | | | | █ |

**Paralelas:**
- Encomenda cozinha AEG/Siemens: iniciar 14-Jul (lead time 8 semanas → entrega 08-Set)
- Carpintaria custom Tiago Móveis: encomenda em 28-Jul, fabrico 6 semanas
- Selecções de materiais (pavimento, azulejo, tintas): deadline cliente 30-Jun

## Fases detalhadas

### Fase 1: Projecto (4 semanas | 07-Abr → 02-Mai-2025)
- Projecto de arquitectura + especialidades (MEP, térmica, acústica)
- Inclui: planta cotada, caderno de encargos, mapa de quantidades
- Decisões necessárias do cliente: layout final, localização AVAC, tipo de pavimento
- Entregável: projecto completo para Comunicação Prévia CM Lisboa

### Fase 2: Licenciamento — Comunicação Prévia CM Lisboa (8 semanas | 05-Mai → 27-Jun-2025)
- Tipo: Comunicação Prévia (obra interior, sem alteração de fachada)
- Prazo CM Lisboa: 8 semanas (histórico 2024 para T3 interior)
- Risco: pedido de elementos adicionais (+2-3 semanas) — probabilidade 25%
- Risco aceite incluído no buffer total de 4 semanas

### Fase 4: Preparação de obra (2 semanas | 30-Jun → 11-Jul-2025)
- Montagem estaleiro, proteções vizinhos, cobertura pavimentos comuns
- Contrato empreiteiro assinado: empreiteiro Construções Fonseca & Filhos (proposta aceite 20-Jun)

### Fase 8: MEP rough-in — AVAC + KNX Domótica (3 semanas | 28-Jul → 15-Ago-2025)
- AVAC: sistema multi-split Daikin 4 zonas + unidade exterior cobertura
- Domótica: KNX, 12 circuitos, integração persianas + iluminação + AVAC
- Inspeção obrigatória pré-fecho de paredes: 15-Ago (M5)
- Sub-empreiteiro domótica: Smart Home PT (contactar até 14-Jul)

### Fase 10: Acabamentos (4 semanas | 25-Ago → 19-Set-2025)
- Pavimento: soalho carvalho 14mm Boen, instalação flutuante
- Paredes zonas húmidas: cerâmica Mutina 60×120 (encomenda confirmada 01-Ago)
- Pinturas: Cin Supercryl, cor base NCS S 1002-Y (aprovada em M1)

## Milestones

| # | Marco | Data estimada | Responsável |
|---|---|---|---|
| M1 | Projecto aprovado / layout assinado | 02-Mai-2025 | Arquitecta + Cliente |
| M2 | Comunicação Prévia aceite CM Lisboa | 27-Jun-2025 | Arquitecta |
| M3 | Empreiteiro seleccionado, contrato assinado | 20-Jun-2025 | DIVA / Cliente |
| M4 | Strip-out completo | 18-Jul-2025 | Empreiteiro Fonseca |
| M5 | MEP rough-in completo, inspecção pré-paredes | 15-Ago-2025 | MEP + Fiscalização |
| M6 | Acabamentos completos, pré-punch-list | 19-Set-2025 | Empreiteiro + Cliente |
| M7 | Auto de recepção / entrega chaves | 03-Nov-2025 | Empreiteiro + Proprietário |

## Caminho crítico
`Licenciamento (8 sem) → Preparação (2 sem) → Strip-out (1 sem) → Alvenaria (2 sem)
→ MEP AVAC+KNX (3 sem) → Impermeabilização (2 sem) → Acabamentos (4 sem)
→ Carpintaria (3 sem) → Equipamentos (2 sem) → Remates (2 sem) → Entrega (1 sem)`

**Total caminho crítico: 28 semanas**
**Folga disponível: 4 semanas** (buffer para atraso CM Lisboa ou imprevistos estruturais)

> ⚠️ Fase de maior risco: Licenciamento CM Lisboa. Atraso de 4 semanas → entrega recua
> para 01-Dez-2025. Recomendação: submeter projecto completo em 05-Mai, sem iterações.
```

---

## Output anti-patterns

- Entregar Gantt com barras ████ nas posições do template-padrão sem recalcular com as semanas reais do projeto — parece profissional mas está errado
- Deixar ranges de duração sem commit ("4-12 semanas") em vez de escolher um valor justificado para aquele projeto específico
- Omitir os multiplicadores de ajuste (heritage, área, inverno) sem documentar que foram verificados e não aplicados
- Listar milestones M1-M7 sem datas — transforma o cronograma num checklist genérico inútil para o cliente
- Esquecer lead times de encomendas longas (cozinha 6-8 semanas, carpintaria custom) que são frequentemente o real bottleneck pós-obra
- Não quantificar o impacto de atraso no caminho crítico — dizer "pode atrasar" sem "atraso de X semanas → entrega recua para DD-MMM"
- Incluir fase de Estrutura (fase 6) em fit-out interior sem justificar ou marcar como N/A
- Gerar datas de início/entrega sem verificar sobreposição com fecho de Agosto (semanas 33-34) ou férias de Natal, que são blind spots comuns em projetos portugueses
