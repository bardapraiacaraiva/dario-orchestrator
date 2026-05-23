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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

### 1. GATE — Brief completo & sem placeholders críticos
- [ ] Client name, indústria, stack, goal principal e URL estão preenchidos com dados reais
- [ ] Contact info (nome + email do primary contact) presente
- [ ] Success criteria definidos em linguagem mensurável ("aumentar conversões em 20%", não "melhorar resultados")
- [ ] Timeline e budget constraints documentados (mesmo que seja "TBD — pendente cliente")
- [ ] Nenhum campo crítico com `<placeholder>` ou `???`

❌ NOT delivery-ready: "Goal: melhorar o site. Stack: WordPress (acho). Contact: alguém do marketing."
✅ Delivery-ready: "Goal: aumentar leads B2B em 30% até Q3. Stack: WP 6.4 + WooCommerce 8.2 + Elementor. Contact: Ana Ferreira — ana@empresa.pt"

### 2. GATE — Diagnóstico com TIER 0 blockers identificados
- [ ] `dario-diagnose` executado e output presente no relatório final
- [ ] TIER 0 blockers listados com descrição clara (não só labels)
- [ ] Score global atribuído (X.X/10) com confidence level (🟢/🟡/🔴) justificado
- [ ] Roadmap de 4 milestones esboçado, mesmo que de alto nível
- [ ] Se confidence 🔴 Baixa — razão explicitada + dados em falta identificados

❌ NOT delivery-ready: "TIER 0: SEO fraco. Score: baixo. Confidence: média."
✅ Delivery-ready: "TIER 0: (1) SSL expirado em prod — risco de penalização imediata; (2) 0 tag de conversão no GA4. Score: 3.8/10. Confidence: 🟡 Média — sem acesso GSC ainda."

### 3. GATE — Quick Wins Semana 1 accionáveis e priorizados
- [ ] 3–5 quick wins listados em tabela com esforço (horas) e impacto (Alto/Médio/Baixo)
- [ ] Ordenados por high-impact + low-effort primeiro (não por ordem de descoberta)
- [ ] Cada win tem um owner claro: agência, cliente, ou ambos
- [ ] Nenhum quick win requer acesso que ainda não foi concedido (ou está marcado como "bloqueado: aguarda acesso X")
- [ ] Pelo menos 1 win executável nas próximas 24h sem dependências

❌ NOT delivery-ready: "1. Melhorar SEO (Alto impacto). 2. Rever copy (Médio). 3. Instalar analytics."
✅ Delivery-ready: "1. Instalar Redirection plugin + redirecionar 12 URLs 404 identificadas — 1.5h — Alto — Owner: DARIO. 2. Adicionar meta description nas 5 páginas core — 45min — Alto — Owner: DARIO."

### 4. GATE — Agent memory + RAG + Obsidian — tudo salvo e indexado
- [ ] `project_<slug>.md` escrito em `~/.claude/agent-memory/dario-v2-digital-ceo/` com todos os campos do template preenchidos
- [ ] `MEMORY.md` atualizado com entry em "Projetos Ativos"
- [ ] Mínimo 4 ficheiros Obsidian criados (Contexto, Diagnóstico, Auditoria se aplicável, Quick Wins) com paths completos
- [ ] `dario-rag-ingest` executado para cada ficheiro → collection `clients` confirmada
- [ ] Query de teste RAG sugerida no relatório final para validação imediata

❌ NOT delivery-ready: "Memória atualizada." (sem path, sem confirmação RAG)
✅ Delivery-ready: "project_cuidai.md criado. MEMORY.md atualizado. 4 ficheiros Obsidian em 05 - Claude - IA/. 6 sources ingestadas em collection `clients`. Query: `search_kb(query: 'Cuidai onboarding', collection: 'clients', limit: 10)`"

### 5. GATE — Pendentes do cliente explicitamente listados
- [ ] Secção "Pendente do cliente" presente com itens específicos (não vazia)
- [ ] Cada pendente tem formato: "O quê — Porquê é bloqueador — Quem pedir — Urgência"
- [ ] Acessos técnicos em falta identificados (GA4, GSC, WP admin, staging, etc.)
- [ ] Pelo menos um próximo passo concreto endereçado ao utilizador DARIO (não ao cliente)

❌ NOT delivery-ready: "Pendente: dados do cliente."
✅ Delivery-ready: "Pendente: (1) Acesso GSC — necessário para análise de keywords — pedir a Miguel Sousa — CRÍTICO esta semana; (2) Credenciais WP staging — bloqueador para wp-audit completo — urgência média."

### 6. GATE — Output usa CLIENT NAME + dados REAIS em todo o documento — zero angle-brackets
- [ ] Zero instâncias de `<Client Name>`, `<slug>`, `<stack>`, `<path>`, `<industry>` ou similares no output final
- [ ] Todos os paths de ficheiro são reais e completos (com nome do cliente no slug)
- [ ] Métricas baseline são reais ou marcadas explicitamente como "não disponível — a recolher"
- [ ] Relatório final lê-se como entregável cliente-ready, não como template preenchido a metade

❌ NOT delivery-ready: "project_`<slug>`.md criado. Goal: `<main goal>`. Contact: `<email>`."
✅ Delivery-ready: "project_tributario-ai.md criado. Goal: aumentar sign-ups trial em 40% até Set 2025. Contact: Ricardo Luz — ricardo@tributario.ai."

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# 🎯 Client Onboard Completo — Cuidai

## Contexto
- **Indústria:** Health-tech / Cuidados domiciliários para idosos (B2C + B2B2C)
- **Stack:** WordPress 6.5 + WooCommerce 8.3 + Elementor Pro + WP Rocket + Cloudflare
- **URL Produção:** cuidai.pt | **Staging:** staging.cuidai.pt
- **Primary Contact:** Margarida Costa — margarida@cuidai.pt — +351 912 345 678
- **Goal principal:** Aumentar leads qualificados (famílias a contratar cuidadores) em 35% até Q4 2025
- **Success criteria:** CPL < €18, taxa de conversão formulário > 4.5%, NPS onboarding > 7
- **Budget:** €2.800/mês retainer | Timeline: início imediato, revisão Q3
- **Known pain points:** Formulário de contacto com taxa de abandono de 73%, zero tracking de conversões, página de pricing confusa

## Diagnóstico (resumo)
- **Score global:** 4.2/10
- **TIER 0 blockers:** 3
- **Confidence:** 🟡 Média — sem acesso GA4 ainda; estimativas de tráfego via Semrush

## TIER 0 — Resolver IMEDIATAMENTE

1. **Zero tracking de conversões** — GA4 instalado mas sem eventos; impossível medir ROI de qualquer campanha. Fix: instalar GTM + configurar eventos form_submit, phone_click, cta_click. Esforço: 3h.
2. **Formulário com 73% abandono** — 6 campos obrigatórios desnecessários (NIF, data de nascimento, morada completa) antes de qualquer contacto humano. Fix: reduzir para 3 campos (nome, telefone, concelho). Esforço: 1h.
3. **SSL staging expirado** — staging.cuidai.pt devolve ERR_CERT_DATE_INVALID; bloqueia testes e aprovações de cliente. Fix: renovar via Cloudflare. Esforço: 20 min.

## Quick Wins — Semana 1

| # | Ação | Esforço | Impacto | Owner | Status |
|---|---|---|---|---|---|
| 1 | Simplificar formulário: 6 campos → 3 campos | 1h | Alto | DARIO | Pronto para executar |
| 2 | GTM + GA4 eventos de conversão básicos | 3h | Alto | DARIO | Aguarda acesso GTM |
| 3 | Renovar SSL staging | 20min | Médio | DARIO | Pronto para executar |
| 4 | Adicionar CTA "Pedir orçamento grátis" ao hero mobile (ausente) | 45min | Alto | DARIO | Pronto para executar |
| 5 | Criar/optimizar Google Business Profile (incompleto, 0 fotos) | 1.5h | Médio | DARIO + Cliente (fotos) | Cliente envia fotos |

## Ficheiros Criados

- [Contexto Inicial](C:\Users\barda\.claude\obsidian\05 - Claude - IA\Contextos\2025-06-11 - Cuidai - Contexto Inicial.md)
- [Diagnóstico DARIO](C:\Users\barda\.claude\obsidian\05 - Claude - IA\Outputs\2025-06-11 - Cuidai - Diagnostico DARIO.md)
- [Auditoria WP](C:\Users\barda\.claude\obsidian\05 - Claude - IA\Outputs\2025-06-11 - Cuidai - Auditoria WordPress.md)
- [Quick Wins Semana 1](C:\Users\barda\.claude\obsidian\05 - Claude - IA\Outputs\2025-06-11 - Cuidai - Quick Wins Semana 1.md)

## Agent Memory

- `project_cuidai.md` criado em `C:\Users\barda\.claude\agent-memory\dario-v2-digital-ceo\`
- `MEMORY.md` atualizado — entry adicionada em "Projetos Ativos":
  `- [Cuidai](project_cuidai.md) — Health-tech PT, leads famílias cuidadores, TIER 0 activo, retainer €2.8k/mês`

## RAG

- **8 sources ingestadas** em collection `clients`
  - cuidai-contexto-inicial, cuidai-diagnostico, cuidai-wp-audit, cuidai-quick-wins
  - + 4 docs de referência sector health-tech PT
- **Query de validação:**
  `mcp__dario-rag__search_kb(query: "Cuidai leads formulário conversão", collection: "clients", limit: 10)`

## Próximos 3 Passos

1. **Hoje** — Executar simplificação do formulário (1h, zero dependências, impacto imediato na taxa de conversão)
2. **Esta semana** — Pedir acesso GTM + GA4 à Margarida para desbloquear tracking (sem isto não medimos nada)
3. **Até sexta** — Agendar call de alinhamento roadmap com cliente: apresentar Milestones M1-M4 e confirmar prioridades

## Pendente do Cliente

| Item | Porquê bloqueia | Quem pedir | Urgência |
|---|---|---|---|
| Acesso GA4 (editor) | Sem isto não configuramos eventos nem medimos conversões | Margarida Costa | 🔴 CRÍTICO |
| Acesso GTM (publish) | Bloqueador para todos os eventos de tracking | Margarida Costa | 🔴 CRÍTICO |
| Credenciais WP Admin staging | Necessário para wp-audit completo e testes seguros | TI Cuidai (Pedro?) | 🟡 Esta semana |
| 5-10 fotos equipa/serviço | Google Business Profile + hero redesign | Margarida Costa | 🟢 Até sexta |
| Briefing campanhas Google Ads actuais | Perceber spend actual vs resultados | Margarida Costa | 🟡 Esta semana |
```

---

## Output anti-patterns

- **Avançar sem brief completo** — usar "vou assumir que é WordPress" ou "provavelmente querem mais tráfego" em vez de parar e perguntar o que falta
- **TIER 0 sem acção concreta** — listar "SEO fraco" ou "site lento" sem especificar o fix, o esforço estimado e o owner
- **Quick wins sem owner nem status** — uma tabela com 5 itens todos marcados "equipa" ou sem indicação de dependências bloqueia execução imediata
- **Paths de ficheiros inventados ou com placeholders** — escrever `project_<slug>.md` ou `05 - Claude - IA/Outputs/<filename>.md` em vez dos paths reais com o nome do cliente
- **RAG confirmado sem query de validação** — dizer "ingestado com sucesso" sem fornecer a query de teste que o utilizador pode correr para confirmar
- **Secção "Pendente do cliente" vazia ou genérica** — "aguarda dados do cliente" sem especificar o quê, porquê é bloqueador, e quem exatamente pedir
- **Score de diagnóstico sem confidence level** — um "6.5/10" sem 🟢/🟡/🔴 e sem justificação leva o utilizador a tratar dados parciais como factos
- **Misturar acções DARIO com acções cliente** — os próximos 3 passos devem ser para o utilizador DARIO; acções do cliente pertencem à secção "Pendente"
- **Onboard executado sem verificar agent-memory existente** — criar `project_cuidai.md` do zero quando já existe contexto guardado de um projecto anterior resulta em perda de histórico e decisões
- **Relatório final em formato de rascunho interno** — usar linguagem como "acho que", "provavelmente", "a confirmar" num documento que pode ser partilhado com o cliente ou equipa
