---
name: diva-status
description: "DIVA system health dashboard — shows RAG stats for collection diva, agent memory state, skills count, squads status, eval baseline, Obsidian vault status, and overall system health. Triggers on \"status diva\", \"diva health\", \"estado diva\", \"system check diva\", \"health check diva\", \"diva status\"."
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# DIVA Status — System Health Dashboard

One-command overview of the entire D.I.V.A. system state.

## When to activate

Invoke `/diva-status` when:
- User wants to see overall DIVA system health
- Start of a new session to verify everything is running
- After updates/modifications to verify integrity
- Debugging issues with RAG, memory, or skills

## Workflow

### 1. RAG Engine Health
```bash
curl -s http://localhost:8420/health
```
Report: status, total sources, total chunks, model.

Then check DIVA-specific:
```
mcp__dario-rag__search_kb(query: "squad diva architecture design", collection: "diva", limit: 1)
```
Report: DIVA collection accessible, sample result returned.

### 2. RAG Collection "diva" Stats
List key knowledge areas and verify each has content:
- Architecture Masters Squad
- Interior Design Squad (12 designers)
- Construction Management Squad
- PT Building Code (RGEU/RJUE/SCE)
- Materials & Innovation Squad
- MEP & Smart Home Squad
- Visualization + Landscape Squads
- Custos m2 Portugal 2026
- Fornecedores Portugal
- Feiras Internacionais (design + construcao)
- Contratos Empreitada
- Subempreiteiros
- Patologias Construcao
- Templates Cronograma
- Seguranca SHST
- RCD Residuos
- Medicoes ProNIC
- Software Gestao Obra
- Eval Suite (30 queries)

### 3. Skills Inventory
```bash
ls ~/.claude/skills/diva-*/SKILL.md | wc -l
```
List all 19 skills with file sizes.

### 4. Agent Definition
```bash
wc -l ~/.claude/agents/diva-v1-design-architect.md
```
Verify agent file exists and is >600 lines.

### 5. Agent Memory State
```bash
ls ~/.claude/agent-memory/diva-v1-design-architect/
cat ~/.claude/agent-memory/diva-v1-design-architect/MEMORY.md
```
Report: number of memory files, projects tracked, last update.

### 6. Obsidian Vault
```bash
ls "C:/Users/barda/OneDrive/Documents/D.I.V.A/" 2>/dev/null || echo "VAULT NOT FOUND"
```
Report: vault exists, folder structure, number of files.

### 7. CCA-F Plugin
```bash
ls ~/.claude/plugins/cache/carolinacherry/claude-certified-architect/
```
Report: installed, version.

### 8. Integrations Check
- Gemini/nanobanana: check if `gemini_generate_image` tool available
- AI Designer: check if `mcp__aidesigner__generate_design` tool available
- PlanRadar: skill exists (no live connection needed)
- BIM: skill exists

## Output Template

```markdown
# D.I.V.A. V1.0 — System Status
## Data: <YYYY-MM-DD HH:MM>

### RAG Engine
- Status: <OK/DOWN>
- Sources totais: <N>
- Chunks totais: <N>
- Collection "diva": <N sources, N chunks>

### Skills: <N>/19
| Skill | Status | Linhas |
|---|---|---|
| diva-diagnose | OK | <N> |
| ... | ... | ... |

### Squads na RAG: <N>/8
| Squad | Status |
|---|---|
| Architecture Masters | <OK/MISSING> |
| Interior Design | <OK/MISSING> |
| Construction Management | <OK/MISSING> |
| PT Building Code | <OK/MISSING> |
| Materials & Innovation | <OK/MISSING> |
| MEP & Smart Home | <OK/MISSING> |
| Visualization | <OK/MISSING> |
| Landscape & Exterior | <OK/MISSING> |

### Agent
- Definition: <N> linhas
- Memory files: <N>
- Projects tracked: <list>

### Obsidian Vault
- Path: <path>
- Status: <EXISTS/MISSING>
- Folders: <list>

### Integrations
- Gemini render: <AVAILABLE/UNAVAILABLE>
- AI Designer: <AVAILABLE/UNAVAILABLE>
- PlanRadar: <SKILL READY>
- BIM: <SKILL READY>
- CCA-F: <INSTALLED v1.0.0>

### Eval Suite
- Queries: 30
- Last test: <date>
- Pass rate: <N/30>

### Health Score: <N>/100
```

## Red flags
- RAG down: restart with `cd /c/dario-rag/engine && .venv/Scripts/python.exe main.py &`
- Collection "diva" empty: re-ingest from /c/diva-kb/
- Skills <19: check for missing SKILL.md files
- Agent memory empty: may need re-initialization
