---
name: dario-client-onboard
description: Mega-orchestrator for new client onboarding — runs dario-diagnose + initial audit (wp-audit if applicable) + agent-memory project file + RAG indexing + Obsidian context save + quick wins list. One command = new client onboarded. Triggers on "novo cliente", "onboard client", "client kickoff", "comecar projeto novo".
license: MIT
---

# DARIO Skill — Client Onboard (Orchestrator)

The "new client kickoff" mega-skill. Chains multiple DARIO skills into a single flow that takes a new client from "we just signed them" to "we have a full context, a diagnosis, a plan, and everything is saved + indexed".

## When to activate

- User says "novo cliente [name]" or "onboard [name]"
- After contract signed, before any work starts
- Re-onboarding an old client after a long pause
- Rebuilding context for a client whose project state is unclear

## Orchestration flow

The skill is a **planner** that invokes other skills in order and stitches outputs together. Each step is a clear handoff.

### Step 1: Gather initial brief
Prompt the user for (or extract from provided input):
- **Client name** + industry + size
- **Contact info** (primary contact, email, phone)
- **Website URL** (production + staging if any)
- **Stack** (as far as known)
- **Main goal** (why they hired us)
- **Timeline / budget constraints**
- **Known pain points**
- **Success criteria** (what "done well" looks like)
- **Data access** (GA, GSC, WP admin, etc.)

If critical info is missing, STOP and ask. Do not proceed with guesses.

### Step 2: Check existing agent-memory
Before diagnosing, read `~/.claude/agent-memory/dario-v2-digital-ceo/project_*.md` to see if this client already has context. If yes:
- Merge and update
- Flag what changed

### Step 3: RAG reconnaissance
```
mcp__dario-rag__search_kb(query: "<client name>", limit: 10)
mcp__dario-rag__search_kb(query: "<industry> <stack>", collection: "dario", limit: 5)
```

Ingest any new information that came up in Step 1 that's not yet in the RAG via `dario-rag-ingest`.

### Step 4: Run `dario-diagnose`
Full diagnostic:
- Holistic analysis (technical, SEO, conversion, content, legal, brand)
- Prioritization (CRÍTICO / IMPORTANTE / OTIMIZAÇÃO)
- 4-milestone roadmap
- Confidence level

### Step 5: Run relevant specialized audit(s)
Based on stack detected:
- WordPress / Woo → `dario-wp-audit`
- SEO deep dive → `seo-audit`
- If paid ads running → review current campaigns
- If legal risk flagged → check `spec/pt-legal-compliance` and produce risk summary

### Step 6: Quick Wins list
Distill the findings into a **"first 7 days" action list**:
- 3-5 actions the client or agency can do immediately
- Each with effort estimate (hours) and impact (high/med/low)
- Prioritize high-impact + low-effort first

### Step 7: Create agent-memory project file
Write to `C:\Users\barda\.claude\agent-memory\dario-v2-digital-ceo\project_<slug>.md` with:

```markdown
---
name: <Client> — Project Context
description: <1-line>
type: project
---

## Client
- Name, industry, size
- Contacts

## Stack
- Technical stack detected / declared

## Goals
- Main business goal
- Success criteria

## Baseline Metrics
- Traffic, conversions, CWV, whatever is available

## TIER 0 blockers (from diagnose)
1. ...

## Roadmap (high level)
M1 / M2 / M3 / M4

## Decisions taken during onboarding
- ...

## Pending data from client
- ...

## RAG refs
- Search with: <relevant queries>

## Last updated
YYYY-MM-DD
```

Add an entry to `MEMORY.md` under "Projetos Ativos":
```markdown
- [Client Name](project_<slug>.md) — 1-line hook
```

### Step 8: Save to Obsidian vault
Call `dario-obsidian-save` for:
1. **Client context** → `05 - Claude - IA/Contextos/YYYY-MM-DD - <Client> - Contexto Inicial.md`
2. **Diagnose output** → `05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Diagnostico DARIO.md`
3. **Audit output (if ran)** → `05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Auditoria <Tipo>.md`
4. **Quick wins** → `05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Quick Wins Semana 1.md`

### Step 9: Ingest all saved files into RAG
Call `dario-rag-ingest` for each saved file into the `clients` collection so they're immediately searchable.

### Step 10: Report to user (final summary)
- Files created (with paths)
- RAG sources added (count)
- Agent memory updated
- TIER 0 blockers surfaced
- Quick wins list (5 items)
- Next 3 actions the user should take

## Output template (final report to user)

```markdown
# 🎯 Client Onboard Completo — <Client Name>

## Contexto
- **Indústria:** ...
- **Stack:** ...
- **Goal principal:** ...

## Diagnóstico (resumo)
- **Score global:** X.X/10
- **TIER 0 blockers:** N
- **Confidence:** 🟢 Alta | 🟡 Média | 🔴 Baixa

## TIER 0 — Resolver IMEDIATAMENTE
1. ...
2. ...

## Quick Wins (Semana 1)
| # | Ação | Effort | Impact |
|---|---|---|---|
| 1 | ... | 2h | Alto |

## Ficheiros Criados
- [Contexto Inicial](<path>)
- [Diagnóstico DARIO](<path>)
- [Auditoria WP](<path>)
- [Quick Wins](<path>)

## Agent Memory
- `project_<slug>.md` criado em `~/.claude/agent-memory/dario-v2-digital-ceo/`
- MEMORY.md atualizado

## RAG
- N sources ingested em collection `clients`
- Próxima query útil: `mcp__dario-rag__search_kb(query: "<client>", limit: 10)`

## Próximos 3 Passos
1. <most urgent>
2. <second>
3. <third>

## Pendente do cliente
- <list of data/approvals needed from client>
```

## Interactions — the chain
```
dario-client-onboard
  ├── Agent-memory read (existing context)
  ├── dario-rag-ingest (new brief)
  ├── dario-diagnose
  ├── dario-wp-audit (if WP)
  ├── dario-obsidian-save (x4)
  ├── dario-rag-ingest (x4 saved files)
  └── Agent-memory write (project_<slug>.md + MEMORY.md update)
```

## Red flags — don't run this skill when
- Client brief is incomplete (ask first)
- No website URL to analyze
- User says "just give me a quick answer" (this is NOT quick)
- Technical access not granted (can't run real audits)

## Why this skill exists
- Takes the 30-60 min of context + diagnosis + save + index work and makes it one command
- Ensures every new client leaves the onboard with the SAME rigor and baseline
- Agent memory stays fresh automatically — no drift across sessions
- RAG always has latest client context → future DARIO queries know this client

## Red Flags
- Never skip the baseline diagnostic (Step 4) — without a measured starting point, you cannot prove improvement or justify your work to the client
- Never start any deliverable work without verified access credentials (WP admin, GA4, GSC, hosting) — guessing or working blind produces incomplete audits that miss critical issues
- Always create the agent-memory project file (Step 7) before ending onboard — skipping this means the next session starts from zero and the client pays for re-discovery
- Never proceed with onboarding if the client brief is missing critical fields (URL, goal, stack) — an incomplete onboard produces a flawed diagnosis that leads to wrong priorities
- Always ingest onboard outputs into RAG (Step 9) — un-indexed deliverables are invisible to future DARIO queries, creating knowledge silos between sessions
