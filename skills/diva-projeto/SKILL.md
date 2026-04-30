---
name: diva-projeto
description: Project context switcher for architecture/design/construction projects — loads all memory, RAG context, and audit history for a specific DIVA project. Displays project summary, last decisions, pending items, budget status, timeline status. Triggers on "projeto", "projecto", "switch project", "mudar projeto", "contexto do", "carrega projeto", "projeto DIVA".
license: MIT
---

# DIVA Skill — Project Context Switcher (Architecture/Design/Construction)

Loads the complete context for a specific architecture, design, or construction project in one command. Searches agent-memory, DIVA RAG collection, and Obsidian vault to assemble a comprehensive project briefing. Specialized for building projects with budget tracking, timeline phases, regulatory status, and technical decisions.

## When to activate

- User says "projeto DIVA Vila Cascais" or "projecto Moradia Sintra"
- User switches between architecture projects mid-session
- Start of session when user wants to resume work on a building project
- Before any DIVA skill execution for a specific project
- User asks "onde estamos com o projeto X?"
- User says "contexto do projeto" or "carrega projeto"

Do NOT use for:
- Non-architecture projects (websites, SaaS, marketing) — use `dario-projeto` instead
- Creating a new project from scratch (use project brief workflow instead)
- Generic architecture questions without a specific project

## Workflow

### 1. Identify the project

Match user input against known projects. Search in this order:

**a) Agent-memory files:**
Search `~/.claude/agent-memory/` and `~/.claude/plugins/` for project files:
```
Glob(pattern: "**/project_*.md", path: "C:/Users/barda/.claude")
Glob(pattern: "**/MEMORY.md", path: "C:/Users/barda/.claude")
```

Look for DIVA/architecture project entries containing:
- Building type (moradia, apartamento, edificio, loja, escritorio)
- Location references (Portuguese cities, addresses)
- Architecture terms (projeto, obra, remodelacao, construcao)

**b) RAG search:**
```
mcp__dario-rag__search_kb(query: "<project name>", collection: "diva", limit: 10)
```

**c) Obsidian vault:**
```
Glob(pattern: "**/*<project>*", path: "C:/Users/barda/OneDrive/Documents/VCHOME segundo cerebro/05 - Claude - IA")
Glob(pattern: "**/*<project>*", path: "C:/Users/barda/OneDrive/Documents/VCHOME segundo cerebro/01 - Projetos")
```

If no exact match found, list available DIVA projects and ask user to clarify.

### 2. Load project memory

Read the matching project file(s) and extract:
- **Project name and type** (new build, renovation, interiors, mixed)
- **Client name and contacts**
- **Location** (address, municipality, parish)
- **Building type** (moradia, apartamento, edificio comercial, etc.)
- **Area** (gross, net, plot)
- **Current phase** (programa, estudo previo, projeto base, projeto execucao, obra, conclusao)
- **Stack/team** (architect, engineers, contractor, subcontractors)
- **Budget** (approved, spent, remaining, contingency)
- **Timeline** (milestones, current phase dates, delays)
- **Regulatory status** (licenciamento, PIP, comunicacao previa, alvara)
- **Pending items and blockers**

### 3. Load technical decisions history

Search for decision records:
```
Glob(pattern: "**/*<project>*Decisao*", path: "C:/Users/barda/OneDrive/Documents/VCHOME segundo cerebro/05 - Claude - IA/Decisoes")
```

And in RAG:
```
mcp__dario-rag__search_kb(query: "<project name> decision", collection: "diva", limit: 5)
```

Extract key decisions:
- Material selections (finishes, structure, insulation)
- System choices (HVAC, domotica, security)
- Design decisions (layout changes, program adjustments)
- Budget decisions (value engineering, scope changes)

### 4. Load recent outputs

Search Obsidian for DIVA outputs related to this project:
```
Glob(pattern: "**/*<project>*", path: "C:/Users/barda/OneDrive/Documents/VCHOME segundo cerebro/05 - Claude - IA/Outputs")
```

List the 5 most recent with dates and types.

### 5. Check regulatory status

If project has licensing/regulatory context, summarize:
- **RJUE phase:** PIP submitted? Comunicacao previa? Alvara de construcao?
- **SCE status:** Energy certification submitted? Class achieved?
- **Especialidades:** Structural project approved? MEP projects approved?
- **Municipal PDM/PP constraints:** Max height, COS, afastamentos

### 6. Present comprehensive context

Output format:

```
## Projeto DIVA: <Project Name>

**Tipo:** <Moradia / Apartamento / Comercial / Misto>
**Localizacao:** <address>, <municipality>
**Area:** <X> m2 brutos / <Y> m2 uteis / Lote <Z> m2
**Fase actual:** <phase>
**Working dir:** <path if applicable>

### Equipa
- **Arquitecto:** <name>
- **Engenheiro estruturas:** <name>
- **Empreiteiro:** <name>
- **Instalador AVAC:** <name>
- **Instalador domotica:** <name>

### Orcamento
| Rubrica | Aprovado | Gasto | Restante |
|---|---|---|---|
| Construcao | EUR X | EUR Y | EUR Z |
| Especialidades | EUR X | EUR Y | EUR Z |
| Acabamentos | EUR X | EUR Y | EUR Z |
| Equipamento | EUR X | EUR Y | EUR Z |
| Contingencia | EUR X | EUR Y | EUR Z |
| **Total** | **EUR X** | **EUR Y** | **EUR Z** |

### Timeline
| Fase | Previsto | Real | Estado |
|---|---|---|---|
| Programa | MM/YYYY | MM/YYYY | Concluido |
| Estudo previo | MM/YYYY | MM/YYYY | Concluido |
| Projeto base | MM/YYYY | MM/YYYY | Em curso |
| Licenciamento | MM/YYYY | — | Pendente |
| Projeto execucao | MM/YYYY | — | Pendente |
| Obra | MM/YYYY | — | Pendente |
| Conclusao | MM/YYYY | — | Pendente |

### Licenciamento / Regulamentar
- RJUE: <status>
- SCE: <status>
- Especialidades: <status>
- PDM: <constraints>

### Decisoes activas
1. <date> — <decision summary>
2. <date> — <decision summary>
3. ...

### Pendente / Bloqueios
- [ ] <pending item>
- [ ] <pending item>
- ...

### Ultimos outputs (Obsidian)
1. YYYY-MM-DD — <title> (<type>)
2. YYYY-MM-DD — <title> (<type>)
3. ...

### RAG DIVA — contexto disponivel
- N sources, M chunks relevantes
- Temas indexados: <list>

Pronto para trabalhar no projeto. O que precisas?
```

### 7. Set active project context

After presenting, all subsequent DIVA interactions in this session should:
- Auto-include project name in RAG queries (collection: "diva")
- Reference project memory for decisions and constraints
- Save outputs with project name prefix via `diva-obsidian-save`
- Apply project-specific budget and regulatory constraints
- Use project's location for climate zone (energy), municipality (regulations), etc.

## Project phase reference (Portuguese architecture workflow)

| Phase | Description | Key deliverables |
|---|---|---|
| Programa | Requirements gathering | Program of requirements, brief |
| Estudo Previo | Concept design | Concept drawings, area calculations, initial budget |
| Anteprojeto | Developed design | Developed drawings, material palette, preliminary specs |
| Projeto Base | Planning application | Full drawings for licensing, memoria descritiva |
| Licenciamento | Municipal approval | Submitted to CM, awaiting approval |
| Projeto Execucao | Construction docs | Detail drawings, caderno de encargos, BOQ |
| Concurso/Adjudicacao | Tender/contractor selection | Tender docs, contractor evaluation, contract |
| Obra | Construction | Site management, progress tracking, changes |
| Recepcao | Handover | Snag list, telas finais, licenca de utilizacao |

## Quick usage examples

```
User: "projeto DIVA moradia sintra"
DIVA: loads Moradia Sintra context — phase: projeto execucao, budget 85% allocated, 
      pending: HVAC subcontractor selection, domotica spec approval

User: "projecto apartamento alfama"
DIVA: loads Apt Alfama context — phase: obra, 60% complete, budget on track,
      pending: kitchen finishes selection, energy cert scheduling

User: "projetos DIVA"
DIVA: lists all known architecture projects with phase and status summary

User: "contexto do Vila Cascais"
DIVA: loads Vila Cascais — new build, phase: licenciamento submitted 2 months ago,
      waiting CM approval, all especialidades approved
```

## Interactions

- Pairs with all DIVA skills — sets project context before execution
- Uses `diva-rag-ingest` collection for RAG searches
- References files saved by `diva-obsidian-save`
- Can cross-reference with `dario-projeto` if project has both building and digital components
- Updates agent-memory project file if significant new information is loaded

## Red flags — don't do this

- Don't load project context without checking if memory/RAG entries exist — if empty, ask user to provide context
- Don't assume project details — if memory is stale (>60 days without update), flag it and ask for current status
- Don't mix DIVA and DARIO project contexts — keep architecture and digital separate
- Don't display budget numbers without confirming they're current — budgets change frequently in construction
- Don't assume regulatory status — always caveat with "ultimo estado registado em <date>"
- If project has no RAG entries, suggest ingesting key documents: caderno de encargos, memoria descritiva, orcamento
- Don't forget to check for related projects at the same location (e.g., interiors project + landscape project for same property)
