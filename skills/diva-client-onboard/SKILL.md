---
name: diva-client-onboard
description: "Mega-orchestrator for new architecture/design/construction client onboarding. Runs diva-diagnose + diva-briefing + agent-memory project file + RAG indexing + Obsidian context save + quick wins list. One command = new client fully onboarded. Triggers on \"novo cliente\", \"onboard client\", \"client kickoff\", \"comecar projeto novo\", \"novo projecto DIVA\", \"onboard DIVA\"."
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# DIVA Client Onboard — Mega-Orchestrator

One command onboards a new architecture/design/construction client. Chains: diagnose + briefing + memory + RAG + Obsidian + quick wins.

## When to activate

Invoke `/diva-client-onboard` when:
- New client/project arrives for architecture, interiores, or obra
- User says "novo cliente", "novo projecto", "comecar projecto"
- First contact with any design/construction project
- User wants full setup in one go

Do NOT use when:
- Project already onboarded (use `/diva-projeto` to switch)
- User just wants one specific skill (use that skill directly)

## Workflow — 8 Steps

### Step 1: Gather minimum context
Ask (or infer from input):
- **Quem:** Nome do cliente, contacto
- **O que:** Tipo de projecto (remodelacao, construcao nova, interiores, obra)
- **Onde:** Morada ou zona (Lisboa, Porto, Algarve, etc.)
- **Quanto:** Orcamento indicativo (se disponivel)
- **Quando:** Timeline desejada
- **Porquê agora:** O que motivou o contacto

If critical info missing, ask — don't assume.

### Step 2: Check existing context
```
mcp__dario-rag__search_kb(query: "<client name> <project type>", limit: 5)
mcp__dario-rag__search_kb(query: "<address or zone>", collection: "diva", limit: 3)
```
Check agent memory: `~/.claude/agent-memory/diva-v1-design-architect/`
Check Obsidian: `D.I.V.A vault/05 - Claude - IA/Contextos/`

### Step 3: Run `/diva-diagnose`
Execute diagnostic workflow:
- Avaliar espaco/projecto holisticamente
- Arquitectura + Design + Obras + Regulamentacao + Orcamento
- Classificar: CRITICO / IMPORTANTE / OPTIMIZACAO
- Gerar roadmap 4 milestones

### Step 4: Run `/diva-briefing`
Capture structured briefing:
- Lifestyle, necessidades, desejos
- Orcamento e prioridades
- Preferencias de estilo
- Constrains tecnicos e regulamentares

### Step 5: Create project memory file
Write to `~/.claude/agent-memory/diva-v1-design-architect/project_<slug>.md`:

```markdown
---
name: <Client/Project Name>
description: <one-line project summary>
type: project
---

**Projecto:** <nome>
**Tipo:** <remodelacao/construcao nova/interiores/obra>
**Localizacao:** <morada/zona>
**Area:** <m2>
**Orcamento:** <EUR range>
**Timeline:** <desejada>
**Estilo:** <direccao identificada>
**Estado:** Onboarded <date>

**Why:** <motivacao do cliente>
**How to apply:** <como este contexto deve influenciar recomendacoes>

**Decisoes tomadas:**
- (nenhuma ainda)

**Proximos passos:**
- [ ] <accao 1>
- [ ] <accao 2>
```

Update MEMORY.md index.

### Step 6: Ingest into RAG
```
mcp__dario-rag__ingest_text(
  name: "Projecto <Client> — Contexto Inicial",
  content: <briefing + diagnostico resumido>,
  collection: "diva",
  tags: ["project", "<client-slug>", "<project-type>", "<location>"]
)
```

### Step 7: Save to Obsidian
Save 3 documents:
1. `YYYY-MM-DD - <Client> - Contexto Inicial.md` → `05 - Claude - IA/Contextos/`
2. `YYYY-MM-DD - <Client> - Diagnostico DIVA.md` → `05 - Claude - IA/Outputs/`
3. `YYYY-MM-DD - <Client> - Quick Wins.md` → `05 - Claude - IA/Outputs/`

### Step 8: Generate Quick Wins
List 5-10 accoes imediatas que o cliente pode executar enquanto o projecto avanca:
- Quick wins de design (ex: pintar uma parede, trocar luminarias)
- Quick wins de planeamento (ex: pedir certidao predial, verificar PDM online)
- Quick wins de orcamento (ex: consultar 3 empreiteiros, visitar showroom X)

## Output — Onboarding Complete Summary

```markdown
## Onboarding Completo — <Client>

**Projecto:** <tipo> em <localizacao>
**Area:** <m2> | **Orcamento:** <EUR> | **Timeline:** <meses>

### Diagnostico
- CRITICO: <N items>
- IMPORTANTE: <N items>
- OPTIMIZACAO: <N items>

### Estilo Identificado
- Direccao: <style> (Primary: <designer>, Secondary: <designer>)

### Documentos Criados
- [x] Memory file: project_<slug>.md
- [x] RAG indexed: <chunk ID>
- [x] Obsidian: Contexto + Diagnostico + Quick Wins

### Quick Wins (fazer ja)
1. <accao>
2. <accao>
3. <accao>

### Proximas Skills a Usar
- `/diva-floor-plan` — se tiver planta
- `/diva-materials` — para comecar a definir paleta
- `/diva-budget` — orcamento detalhado
- `/diva-licensing` — verificar necessidade de licenciamento
```

## Red flags
- Never skip RAG check for existing context
- Never skip memory file creation
- Never proceed without minimum context (tipo + localizacao + orcamento indicativo)
- Never forget to save to Obsidian
- Never skip quick wins — high perceived value for client

## Interactions
- Chains: `/diva-diagnose` → `/diva-briefing` → memory → RAG → Obsidian
- After onboard: `/diva-floor-plan`, `/diva-materials`, `/diva-budget`, `/diva-licensing`
- For existing project: `/diva-projeto` instead
