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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Projecto identificado sem ambiguidade

- [ ] O nome do projecto foi matched contra um ficheiro `project_*.md` existente (não inventado)
- [ ] Se houve ambiguidade, DARIO listou as opções e pediu confirmação antes de carregar
- [ ] O path `~/.claude/agent-memory/dario-v2-digital-ceo/project_<name>.md` foi confirmado como existente

❌ NOT delivery-ready: "Carregando contexto do projecto Atrium..." (sem confirmar que o ficheiro existe)
✅ Delivery-ready: "Ficheiro encontrado: `project_wave74_atrium.md` — a carregar contexto."

---

### Gate 2 — Agent-memory carregada e validada

- [ ] Todos os campos obrigatórios extraídos: Stack, Status, Last decisions, Pending, Baseline metrics, Working dir
- [ ] Campo "Last updated" verificado — se `> 30 dias`, flag explícita apresentada ao utilizador
- [ ] Nenhum campo mostrado como `<placeholder>` ou vazio sem explicação

❌ NOT delivery-ready: "**Status:** \<current phase\> | **Stack:** \<stack\>"
✅ Delivery-ready: "**Status:** Beta fechado, onboarding 3 clientes-piloto | **Stack:** Next.js 14, Supabase, Stripe | **Last updated:** 2025-06-01 (14 dias — contexto fresco)"

---

### Gate 3 — RAG consultado com queries relevantes

- [ ] Pelo menos 2 queries RAG executadas: `"<project name>"` + `"<project name> audit"`
- [ ] Número de sources e chunks retornados apresentado no sumário
- [ ] Se RAG retorna 0 resultados, sugestão de ingestão de docs apresentada

❌ NOT delivery-ready: "RAG context disponível — N sources, M chunks" (sem valores reais)
✅ Delivery-ready: "RAG context disponível — 7 sources, 23 chunks relevantes (última ingestão: 2025-05-28)"

---

### Gate 4 — Outputs Obsidian listados com datas reais

- [ ] Glob executado contra `**/05 - Claude - IA/Outputs/*<project>*`
- [ ] Até 5 outputs mais recentes listados com data `YYYY-MM-DD` e título real
- [ ] Se 0 outputs encontrados, dito explicitamente (não omitido em silêncio)

❌ NOT delivery-ready: "Últimos outputs: 1. \<title\> 2. \<title\>"
✅ Delivery-ready: "1. 2025-06-08 — LUSOconta_SaaS_Audit_P1_Criticals.md  2. 2025-05-31 — LUSOconta_Pricing_Revision_v2.md  3. 2025-05-20 — LUSOconta_Beta_Roadmap_Q3.md"

---

### Gate 5 — Context switch seguro (sessão anterior protegida)

- [ ] Se havia um projecto activo na sessão, DARIO confirmou/alertou antes de fazer switch
- [ ] Decisões pendentes ou work-in-progress da sessão anterior foram sinalizados
- [ ] Sessão nova (sem projecto activo) não dispara aviso de switch desnecessariamente

❌ NOT delivery-ready: Trocar de Atrium para Vivenda silenciosamente a meio de uma auditoria
✅ Delivery-ready: "⚠️ Projecto activo: Atrium (auditoria em curso, score 87/100 não guardado). Confirmas switch para Vivenda? Dados actuais serão perdidos."

---

### Gate 6 — Output usa CLIENT NAME + dados REAIS, sem angle-brackets

- [ ] Nenhum `<Name>`, `<stack>`, `<path>`, `<X/100>`, `<date>` no output final
- [ ] Nome do cliente aparece no título do sumário (`## Projeto: LUSOconta`)
- [ ] Last audit score inclui valor numérico real e data (`87/100 — 2025-05-14`)
- [ ] Working dir é path real (`~/Dev/lusoconta-saas/`) não placeholder

❌ NOT delivery-ready: "**Last audit score:** \<X/100\> (\<date\>)"
✅ Delivery-ready: "**Last audit score:** 7.2/10 — 2025-05-14 | 4 P1 criticals activos"

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no context summary deve ter label EXPLÍCITO:

- 🔵 **verified** — lido directamente do `project_*.md` ou ficheiro Obsidian confirmado
- 🟡 **assumed** — inferido/estimado, precisa confirmação do cliente antes de entregar
- 🟢 **projection** — forecast/target por design (não verificável no momento)

Output checklist upfront mostra ao cliente exactamente o que é trust-as-is vs o que precisa de verify antes de agir. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready:
```
## Projeto: Atrium
Last audit score: 92/100
Status: Phase 3 — SEO implementation
Pending: 3 items
```
*(sem labels — o cliente não sabe se o score é do ficheiro de memória, estimado, ou da última sessão)*

✅ Delivery-ready:
```
## Projeto: Atrium
Last audit score: 92/100 (2025-01-14)   🔵 verified — project_wave74_atrium.md
Status: Phase 3 — SEO implementation     🔵 verified — agent-memory, last updated 8 dias
Pending items: 3 criticals               🔵 verified — agent-memory + Obsidian output 2025-01-12
RAG chunks disponíveis: ~47              🟡 assumed — count estimado, colecção pode ter ingestão pendente
Próximo milestone: Go-live Fev 2025      🟢 projection — target definido em sessão anterior, não confirmado recentemente
```

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados — substituir counts/estimates com actuals (ex: re-run RAG search e contar chunks reais)
- [ ] Todos os 🔵 sources com data verificada — se `last_updated > 30 dias`, flag já levantada no Gate 2 e re-confirmada aqui
- [ ] Todos os 🟢 projections comunicados explicitamente ao cliente como targets/forecasts, não como factos entregues

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## Projeto: LUSOconta (SaaS Audit)

**Stack:** Next.js 14, Supabase, Stripe Connect, Vercel
**Status:** Beta fechado — onboarding 3 clientes-piloto (Jun 2025)
**Working dir:** ~/Dev/lusoconta-saas/
**Last audit score:** 7.2/10 — 2025-05-14 | ⚠️ 4 P1 criticals por resolver
**Memory file:** project_lucas_saas_audit.md — Last updated: 2025-06-01 (13 dias — fresco ✅)

---

### Decisões activas
- Pricing fixado: €29/mês Starter, €79/mês Pro (decidido 2025-05-20, não reverter)
- Stripe Connect em modo "Express" — não mudar para Standard sem re-auditoria
- Auth via Supabase Magic Link (OTP removido — decisão 2025-05-18)

### Pendente
- [ ] Resolver P1 #1: Row-level security em `invoices` table (assignado: Lucas)
- [ ] Resolver P1 #2: Webhook Stripe sem validação de signature
- [ ] Resolver P1 #3: API keys expostas em client-side bundle
- [ ] Resolver P1 #4: Missing rate limiting em `/api/auth/login`
- [ ] Definir data de lançamento público (blocker: P1s por fechar)

### Últimos outputs (Obsidian)
1. 2025-05-31 — LUSOconta_P1_Criticals_Remediation_Plan.md
2. 2025-05-28 — LUSOconta_Stripe_Connect_Architecture_v2.md
3. 2025-05-20 — LUSOconta_Pricing_Strategy_Final.md
4. 2025-05-14 — LUSOconta_SaaS_Audit_Full_Report.md
5. 2025-05-10 — LUSOconta_Auth_Flow_Redesign.md

### RAG context disponível
- 9 sources, 31 chunks relevantes
- Última ingestão: 2025-05-31
- Collections: obsidian (6), uploads (3)

---

Pronto para trabalhar. O que precisas?
```

---

## Output anti-patterns

- Apresentar o sumário com campos `<placeholder>` em vez de dados reais extraídos da memória
- Fazer switch de projecto silenciosamente sem alertar sobre work-in-progress da sessão anterior
- Omitir o aviso de memória stale quando `Last updated > 30 dias` — contexto desactualizado gera decisões erradas
- Mostrar "RAG context disponível" sem indicar quantos sources/chunks foram encontrados de facto
- Inventar outputs Obsidian com títulos plausíveis em vez de executar o Glob e listar ficheiros reais
- Prosseguir com o carregamento quando o ficheiro `project_*.md` não existe — deve listar projectos disponíveis e perguntar
- Listar outputs Obsidian sem datas `YYYY-MM-DD` — datas relativas ("esta semana") não são auditáveis
- Não sugerir ingestão de docs quando RAG retorna 0 resultados para o projecto pedido
