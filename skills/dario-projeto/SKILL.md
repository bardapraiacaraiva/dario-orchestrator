---
name: dario-projeto
description: Project Context Switcher — loads all memory, RAG context, and audit history for a specific project. Instant context switch between clients. Triggers on "projeto", "projecto", "switch project", "mudar projeto", "contexto do", "carrega projeto".
license: MIT
---

# DARIO Skill — Project Context Switcher

Loads the complete context for a specific project in one command. No more re-explaining — DARIO knows everything about the project instantly.

## When to activate

- User says "projeto Atrium" or "projecto Vivenda"
- User switches between clients mid-session
- Start of session when user wants to resume work on a project
- Before any audit, fix, or deliverable for a specific client

## Workflow

### 1. Identify the project
Match user input against known projects in agent-memory:
- `project_wave74_atrium.md` → "Atrium", "Golden Visa", "Wave74"
- `project_vivenda_creative_home.md` → "Vivenda", "Creative Home"
- `project_lucas_saas_audit.md` → "LUCAS", "LUSOconta", "SaaS"
- `project_clawcode_agent.md` → "claw-code", "agent package"
- Any `project_*.md` file

If no exact match, list available projects and ask.

### 2. Load agent-memory
Read the matching `project_*.md` file from `~/.claude/agent-memory/dario-v2-digital-ceo/`. Extract:
- Stack
- Current status / phase
- Last decisions taken
- Pending items / blockers
- Baseline metrics
- Working directory path

### 3. Search RAG for project context
```
mcp__dario-rag__search_kb(query: "<project name>", limit: 10)
mcp__dario-rag__search_kb(query: "<project name> audit", collection: "obsidian", limit: 5)
```

### 4. Check Obsidian for recent outputs
Look for files in `05 - Claude - IA/Outputs/` matching the project name:
```
Glob(pattern: "**/05 - Claude - IA/Outputs/*<project>*")
```
List the most recent 5 outputs with dates.

### 5. Present context summary
Output a concise brief:

```
## Projeto: <Name>

**Stack:** <stack>
**Status:** <current phase>
**Working dir:** <path>
**Last audit score:** <X/100> (<date>)

### Decisões activas
- ...

### Pendente
- ...

### Últimos outputs (Obsidian)
1. YYYY-MM-DD - <title>
2. ...

### RAG context disponível
- N sources, M chunks relevantes

Pronto para trabalhar. O que precisas?
```

### 6. Set active project context
After presenting, all subsequent DARIO interactions in this session should:
- Auto-consult RAG with project name in queries
- Reference the project memory for decisions
- Save outputs with the project name prefix

## Quick usage examples

```
User: "projeto atrium"
DARIO: loads Atrium context, shows score 92-94/100, pending items, last 5 outputs

User: "projeto vivenda"  
DARIO: loads Vivenda context, shows WP remodelação plan, pending implementation

User: "projeto lucas"
DARIO: loads LUSOconta context, shows 7.2/10, 4 P1 criticals, beta timeline

User: "projetos"
DARIO: lists all known projects with status summary
```

## Red flags
- Don't load project context without checking if memory file exists
- Don't assume — if memory is stale (>30 days), flag it
- If project has no RAG entries, suggest ingesting relevant docs

## Red Flags
- Never switch to a new project context without confirming the current project's state is saved — unsaved decisions, pending items, or in-progress work will be lost on context switch
- Never assume the agent-memory project file is current — always check the "Last updated" field and flag if it is older than 30 days, as stale context leads to wrong decisions
- Always search RAG for project context before starting any work — skipping RAG means ignoring previous audits, decisions, and deliverables that directly affect the current task
- Never proceed if the project memory file does not exist — working without loaded context means re-discovering everything from scratch, wasting time and risking contradicting past decisions
- Always check Obsidian for recent outputs matching the project name — RAG may be incomplete but the vault often contains the latest deliverables that have not yet been ingested
