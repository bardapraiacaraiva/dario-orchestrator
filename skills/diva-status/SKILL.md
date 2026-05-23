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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — RAG Engine Health reportado com dados reais
- [ ] Status explícito: OK ou DOWN (não "verificando...")
- [ ] Sources totais e chunks totais com número concreto (ex: 847 chunks)
- [ ] Collection "diva" confirmada acessível com sample result devolvido
- [ ] Modelo RAG identificado (ex: `text-embedding-3-small`)

❌ NOT delivery-ready: `RAG Status: <OK/DOWN> — Sources: <N>`  
✅ Delivery-ready: `RAG Status: OK — 23 sources, 1.204 chunks — Collection "diva": acessível (sample: "Arquitetos Modernistas — Le Corbusier principles…")`

---

### Gate 2 — Skills Inventory completo 19/19 com line counts
- [ ] Todos os 19 skills listados nominalmente (não "...")
- [ ] Cada skill tem status OK/MISSING e número de linhas real
- [ ] Contagem `ls ~/.claude/skills/diva-*/SKILL.md | wc -l` executada e resultado visível
- [ ] Se count < 19, skills em falta identificados por nome

❌ NOT delivery-ready: `Skills: <N>/19 — | diva-diagnose | OK | <N> |`  
✅ Delivery-ready: `Skills: 19/19 — | diva-diagnose | OK | 312 | … | diva-status | OK | 198 |`

---

### Gate 3 — Squads RAG verificados individualmente
- [ ] Todos os 8 squads testados (não assumidos OK)
- [ ] Cada squad com status OK ou MISSING (não em branco)
- [ ] Knowledge areas secundárias (Custos m2, Fornecedores, Feiras, Contratos, etc.) reportadas por grupo
- [ ] Se MISSING: path de re-ingestão sugerido

❌ NOT delivery-ready: `Squads na RAG: <N>/8 — Architecture Masters: <OK/MISSING>`  
✅ Delivery-ready: `Squads: 7/8 — Architecture Masters: OK | Interior Design: OK | MEP: MISSING → re-ingest from /c/diva-kb/mep/`

---

### Gate 4 — Agent + Memory State com dados concretos
- [ ] Agent file line count real (deve ser >600; se <600, flag vermelho)
- [ ] Número de memory files listado
- [ ] Projects tracked listados por nome (não "lista")
- [ ] Data do último update de MEMORY.md reportada

❌ NOT delivery-ready: `Agent: <N> linhas — Memory files: <N> — Projects: <list>`  
✅ Delivery-ready: `Agent: 643 linhas ✅ — Memory: 3 files — Projects: Moradia Sintra T4, Reabilitação Bairro Alto, Showroom Lisboa — Last update: 2025-01-14`

---

### Gate 5 — Integrations e Obsidian com estado binário real
- [ ] Obsidian vault path testado (`ls` executado, não assumido)
- [ ] Gemini/AI Designer: AVAILABLE ou UNAVAILABLE (tool lookup feito)
- [ ] CCA-F plugin: versão real reportada ou MISSING
- [ ] Eval Suite: pass rate real N/30 com data do último teste

❌ NOT delivery-ready: `Obsidian: <EXISTS/MISSING> — Gemini: <AVAILABLE> — CCA-F: <INSTALLED v1.0.0>`  
✅ Delivery-ready: `Obsidian: EXISTS — C:/Users/barda/OneDrive/Documents/D.I.V.A/ — 4 folders, 87 files — Gemini: UNAVAILABLE — CCA-F: v1.0.2 — Eval: 27/30 (2025-01-10)`

---

### Gate 6 — Output usa nome DIVA + dados reais, sem angle-brackets por preencher
- [ ] Todos os `<placeholders>` substituídos por valores reais
- [ ] Health Score calculado com critério explícito (não `<N>/100`)
- [ ] Data/hora real no header (`2025-01-15 09:47`, não `<YYYY-MM-DD HH:MM>`)
- [ ] Red flags ativos (se existirem) listados com comando de remedição exacto

❌ NOT delivery-ready: `Health Score: <N>/100 — Data: <YYYY-MM-DD>`  
✅ Delivery-ready: `Health Score: 84/100 — Data: 2025-01-15 09:47 — ⚠️ MEP Squad MISSING, Gemini UNAVAILABLE`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# D.I.V.A. V1.0 — System Status
## Data: 2025-01-15 09:47

### RAG Engine
- Status: ✅ OK
- Sources totais: 23
- Chunks totais: 1.204
- Modelo: text-embedding-3-small
- Collection "diva": 23 sources, 1.204 chunks
- Sample test: "Squad Arquitetura — Le Corbusier: modulor como base proporcional…" ✅

### Skills: 19/19 ✅
| Skill | Status | Linhas |
|---|---|---|
| diva-diagnose | ✅ OK | 312 |
| diva-brief | ✅ OK | 287 |
| diva-concept | ✅ OK | 341 |
| diva-technical-review | ✅ OK | 298 |
| diva-cost-estimate | ✅ OK | 263 |
| diva-schedule | ✅ OK | 274 |
| diva-procurement | ✅ OK | 251 |
| diva-site-report | ✅ OK | 289 |
| diva-render-brief | ✅ OK | 218 |
| diva-bim | ✅ OK | 234 |
| diva-planradar | ✅ OK | 196 |
| diva-code-check | ✅ OK | 322 |
| diva-materials | ✅ OK | 267 |
| diva-mep | ✅ OK | 243 |
| diva-landscape | ✅ OK | 201 |
| diva-subcontractors | ✅ OK | 188 |
| diva-safety | ✅ OK | 214 |
| diva-eval | ✅ OK | 276 |
| diva-status | ✅ OK | 198 |

### Squads na RAG: 7/8 ⚠️
| Squad | Status |
|---|---|
| Architecture Masters | ✅ OK |
| Interior Design (12 designers) | ✅ OK |
| Construction Management | ✅ OK |
| PT Building Code (RGEU/RJUE/SCE) | ✅ OK |
| Materials & Innovation | ✅ OK |
| MEP & Smart Home | ❌ MISSING — re-ingest: `/c/diva-kb/mep/` |
| Visualization | ✅ OK |
| Landscape & Exterior | ✅ OK |

### Knowledge Areas Adicionais
- Custos m2 Portugal 2026: ✅ OK
- Fornecedores Portugal: ✅ OK
- Feiras Internacionais: ✅ OK
- Contratos Empreitada: ✅ OK
- Subempreiteiros: ✅ OK
- Patologias Construção: ✅ OK
- Templates Cronograma: ✅ OK
- Segurança SHST: ✅ OK
- RCD Resíduos: ✅ OK
- Medições ProNIC: ✅ OK
- Software Gestão Obra: ✅ OK
- Eval Suite (30 queries): ✅ OK

### Agent
- Definition: 643 linhas ✅ (>600 threshold OK)
- Memory files: 3
- Projects tracked: Moradia Sintra T4, Reabilitação Bairro Alto, Showroom Lisboa Oriente
- Last MEMORY.md update: 2025-01-14 18:22

### Obsidian Vault
- Path: C:/Users/barda/OneDrive/Documents/D.I.V.A/
- Status: ✅ EXISTS
- Folders: Projetos, Templates, Referencias, Fornecedores (4 total)
- Files: 87

### Integrations
- Gemini render: ❌ UNAVAILABLE (tool `gemini_generate_image` não detectado)
- AI Designer: ✅ AVAILABLE
- PlanRadar: ✅ SKILL READY (diva-planradar 196 linhas)
- BIM: ✅ SKILL READY (diva-bim 234 linhas)
- CCA-F: ✅ INSTALLED v1.0.2

### Eval Suite
- Queries: 30
- Last test: 2025-01-10
- Pass rate: 27/30 (90%) ✅

### ⚠️ Red Flags Ativos
1. MEP Squad MISSING → `cd /c/dario-rag/engine && python ingest.py --folder /c/diva-kb/mep/`
2. Gemini render UNAVAILABLE → verificar API key `GEMINI_API_KEY` em `.env`

### Health Score: 84/100
> -10 MEP Squad MISSING | -6 Gemini UNAVAILABLE
> Todos os 19 skills OK | RAG online | Agent >600L | Vault presente
```

---

## Output anti-patterns

- Entregar output com qualquer `<placeholder>` por preencher — angle-brackets são falha automática
- Reportar Health Score sem breakdown dos pontos deduzidos (ex: "84/100" sem explicar os −16)
- Assumir squad OK sem executar search_kb — squads "parecem estar lá" não é verificação
- Listar skills como `| ... | ... | ...` em vez de todos os 19 nomes reais
- Omitir comandos de remediação quando há red flags — identificar problema sem solução é meio output
- Reportar Agent como OK sem confirmar line count real (threshold >600 deve ser verificado, não assumido)
- Misturar status AVAILABLE/UNAVAILABLE com "não testado" — cada integração exige lookup activo
- Omitir data/hora real no header — status sem timestamp é inútil para rastreio de sessão
