---
name: dario-obsidian-save
description: Save a generated output to the Obsidian vault with correct folder, naming convention (YYYY-MM-DD - Tema - Titulo.md) and frontmatter. Used after any substantive DARIO deliverable. Triggers on "save to vault", "guarda no obsidian", or called implicitly by orchestrator skills.
license: MIT
---

# DARIO Skill — Obsidian Save

Persists deliverables to the user's Obsidian vault using canonical folder structure and naming. Respects the PARA-adapted layout of the vault.

## When to activate

- After generating a plan, strategy, audit, diagnosis, benchmark or decision
- User explicitly says "guarda isto" / "save this"
- At the end of `dario-diagnose`, `dario-wp-audit`, `dario-offer`, `dario-sales-letter`, etc.
- Whenever a file is worth surviving beyond this chat session

Do NOT use for:
- Trivial chat responses
- Intermediate drafts (save the final only)
- Content already saved (avoid duplication)

## Vault structure (reference)

```
C:\Users\barda\OneDrive\Documents\VCHOME segundo cerebro\
├── 00 - Inbox\              ← quick notes, unsorted
├── 01 - Projetos\           ← active projects
├── 02 - Areas\              ← permanent areas of responsibility
├── 03 - Recursos\           ← reference library
├── 04 - Arquivo\            ← inactive
└── 05 - Claude - IA\        ← Claude-generated content
    ├── Outputs\             ← deliverables (audits, plans, reports)
    ├── Decisoes\            ← decision records
    ├── Contextos\           ← project contexts
    └── sessoes.md           ← session end log (hook)
```

## Workflow

### 1. Determine content type
- **Audit / Plan / Benchmark / Strategy / Report** → `05 - Claude - IA/Outputs/`
- **Technical or business decision** → `05 - Claude - IA/Decisoes/`
- **Project context / canonical brief** → `05 - Claude - IA/Contextos/`
- **Rough notes** → `00 - Inbox/`

### 2. Build filename
Convention: `YYYY-MM-DD - <Client or Tema> - <Titulo>.md`

Today's date via today's ISO date (no `-` prefix, 10 chars). Examples:
- `2026-04-15 - Atrium Golden Visa - DARIO Pre-Publish Audit.md`
- `2026-04-15 - Vivenda Creative Home - Plano Remodelacao Total WordPress.md`
- `2026-04-15 - LUSOconta - Decisao Migrar Gemini Pro Para Sonnet.md`

Rules:
- No accents in title portion (evitar `.md` metadata issues em alguns plugins)
- Max 120 chars
- ASCII safe

### 3. Build frontmatter

Minimum required:
```yaml
---
project: <client or project name>
date: 2026-04-15
type: audit|plan|decision|context|benchmark|strategy
status: draft|delivered|implemented
tags: [...relevant tags...]
---
```

Additional optional fields per type:
- `audit`: `score_global`, `tier0_count`, `tier1_count`
- `plan`: `milestones`, `timeline_weeks`
- `decision`: `decision_by`, `alternatives`, `rollback_plan`
- `benchmark`: `competitors_analyzed`, `position`

### 4. Write the file
Use the Write tool directly, not via the Python watcher (which would then re-ingest via Obsidian watcher). The watcher will pick it up on next save.

Path example:
```
C:\Users\barda\OneDrive\Documents\VCHOME segundo cerebro\05 - Claude - IA\Outputs\2026-04-15 - Atrium Golden Visa - Audit.md
```

### 5. Trigger RAG ingest (optional but recommended)
If the file is substantive and should be searchable immediately (not waiting for the watcher), call:
```
mcp__dario-rag__ingest_text(
  content: "<full content>",
  name: "obsidian/05 - Claude - IA/<subfolder>/<filename without .md>",
  source_type: "markdown",
  collection: "obsidian",
  tags: [...]
)
```

### 6. Confirm to user
- Path where saved
- File size / line count
- 1-line reminder: "indexado na RAG, pesquisável via DARIO search_kb"

## Naming edge cases

- **Multiple clients in one doc** → pick the primary, use it
- **Internal DARIO doc (no client)** → use "DARIO" as tema: `2026-04-15 - DARIO - Plano Expansao Skills.md`
- **Recurring doc (weekly review)** → add suffix: `2026-04-15 - Semana - Review.md`
- **Version history** → DO NOT use `-v2`, `-v3`. Save as new file with newer date. Vault history is Git.

## Red flags — don't save when
- Content is less than 20 lines (probably not worth it)
- Content is a direct copy of something already in vault
- User gave explicit "do not save"
- Contains secrets, credentials, PII that shouldn't be persisted

## Interactions
- Called by `dario-diagnose`, `dario-wp-audit`, `dario-offer`, `dario-sales-letter`, `dario-ads-blueprint`, `dario-brand`, `dario-pitch`, `dario-email-seq`, `dario-make-blueprint`, `dario-client-onboard`
- Pairs with `dario-rag-ingest` to make the saved file immediately searchable

## Red Flags
- Never save a file without proper YAML frontmatter (project, date, type, status, tags) — files without frontmatter are invisible to Obsidian queries, Dataview, and RAG tagging
- Never use a naming convention other than `YYYY-MM-DD - Tema - Titulo.md` — inconsistent names break vault search, sorting, and the agent's ability to find previous outputs
- Always verify the vault path exists before writing — writing to a non-existent directory silently fails or creates orphaned files outside the vault structure
- Never save content containing secrets, credentials, or API keys to the vault — Obsidian vaults sync via OneDrive and persisted secrets are a permanent security exposure
- Always check for duplicate content before saving — re-saving identical deliverables clutters the vault and creates confusion about which version is current

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Filename segue convenção canónica

- [ ] Formato exato `YYYY-MM-DD - Tema - Titulo.md` (dois espaços-travessão-espaços)
- [ ] Data é a data de hoje em ISO 8601 (10 chars, sem prefixo)
- [ ] Título sem acentos, sem caracteres non-ASCII, max 120 chars
- [ ] Tema identifica claramente o client ou projeto (não "output" ou "file")

❌ NOT delivery-ready: `audit_atrium_v2_final.md` / `2026-4-5 - Atrium - Audit.md`
✅ Delivery-ready: `2026-04-15 - Atrium Golden Visa - DARIO Pre-Publish Audit.md`

---

### Gate 2 — Pasta correta para o tipo de conteúdo

- [ ] Audit / Plan / Strategy / Benchmark → `05 - Claude - IA/Outputs/`
- [ ] Decisão técnica ou de negócio → `05 - Claude - IA/Decisoes/`
- [ ] Brief canónico / contexto de projeto → `05 - Claude - IA/Contextos/`
- [ ] Nota rápida não estruturada → `00 - Inbox/`
- [ ] Caminho completo escrito e verificável antes de escrever (diretório existe)

❌ NOT delivery-ready: ficheiro guardado em `01 - Projetos/` porque "parece um projeto"
✅ Delivery-ready: `C:\Users\barda\OneDrive\Documents\VCHOME segundo cerebro\05 - Claude - IA\Outputs\2026-04-15 - LUSOconta - Benchmark Contabilidade Online.md`

---

### Gate 3 — Frontmatter completo e válido

- [ ] Bloco `---` abre e fecha corretamente (YAML válido)
- [ ] Campos obrigatórios presentes: `project`, `date`, `type`, `status`, `tags`
- [ ] `type` é um dos valores canónicos: `audit|plan|decision|context|benchmark|strategy`
- [ ] Campos opcionais do tipo preenchidos (`score_global` em audits, `decision_by` em decisions, etc.)
- [ ] `tags` é lista YAML (não string inline)

❌ NOT delivery-ready: `tags: audit, wordpress, cuidai` (string) ou frontmatter sem `status`
✅ Delivery-ready:
```yaml
---
project: Cuidai
date: 2026-04-15
type: audit
status: delivered
tags: [cuidai, wordpress, seo, tier0]
score_global: 61
tier0_count: 3
tier1_count: 7
---
```

---

### Gate 4 — Conteúdo passa os limites de save

- [ ] Ficheiro tem ≥ 20 linhas de conteúdo substantivo
- [ ] Não é cópia de ficheiro já existente no vault (verificado antes de escrever)
- [ ] Não contém secrets, credenciais, API keys, PII persistível
- [ ] Não é rascunho intermédio — é o output final desta sessão

❌ NOT delivery-ready: guardar um `plan` de 8 linhas "para não perder" / re-salvar a mesma estratégia da semana passada com data nova
✅ Delivery-ready: audit completo de 140 linhas sem credenciais, confirmado que `2026-04-14 - Cuidai - Audit.md` não existe no vault

---

### Gate 5 — RAG ingest acionado (quando aplicável)

- [ ] Se o ficheiro é substantivo e deve ser pesquisável imediatamente, `mcp__dario-rag__ingest_text` foi chamado
- [ ] `name` no ingest usa o path relativo: `obsidian/05 - Claude - IA/Outputs/<filename sem .md>`
- [ ] `collection` definido como `"obsidian"`, `tags` alinhadas com frontmatter
- [ ] Se ingest não foi feito, utilizador foi informado que "ficará disponível no próximo ciclo do watcher"

❌ NOT delivery-ready: ingest feito com `name: "audit"` (genérico, colide com outros docs)
✅ Delivery-ready: `name: "obsidian/05 - Claude - IA/Outputs/2026-04-15 - Cuidai - DARIO Pre-Publish Audit"`

---

### Gate 6 — Confirmação ao utilizador usa CLIENT NAME + REAL data, sem placeholders

- [ ] Confirmação inclui path completo real (não `<vault_path>/...`)
- [ ] Inclui nome do client/tema real, data real, contagem de linhas real
- [ ] Indica se RAG ingest foi feito ou se aguarda watcher
- [ ] Zero angle-brackets `< >` visíveis ao utilizador

❌ NOT delivery-ready: "Ficheiro guardado em `<path>/<filename>.md`. Indexado com tags `<tags>`."
✅ Delivery-ready: "Guardado em `05 - Claude - IA/Outputs/2026-04-15 - Vivenda Creative Home - Plano Remodelacao WordPress.md` (87 linhas). Indexado na RAG — pesquisável via DARIO search_kb com tag `vivenda`."

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / memória / dados do cliente
- 🟡 **assumed** — plausível mas precisa confirmação do cliente antes de entregar
- 🟢 **projection** — decisão de design ou inferência futura (não verificável agora)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs o que precisa de verificação. **Honest transparency > inflated delivery.**

---

❌ NOT delivery-ready:
```
date: 2026-04-15
project: Atrium Golden Visa
type: audit
status: delivered
tags: [seo, wordpress, golden-visa]
score_global: 74
```
*Nenhum label → reader assume que tudo está verified. Data pode estar errada, score pode ser estimativa, status pode não refletir realidade do cliente.*

---

✅ Delivery-ready:
```
date: 2026-04-15            🔵 verified — ISO date do sistema no momento do save
project: Atrium Golden Visa 🔵 verified — confirmado em sessão anterior (client onboard)
type: audit                 🔵 verified — output gerado por dario-wp-audit
status: delivered           🟡 assumed — marcado como delivered mas cliente ainda não confirmou recepção
tags: [seo, wordpress]      🟡 assumed — tags inferidas do conteúdo; confirmar se vault usa taxonomia diferente
score_global: 74            🟢 projection — score calculado por heurística DARIO, não auditoria manual
vault_path: 05 - Claude - IA/Outputs/  🔵 verified — path existe e foi validado antes do write
```

---

**Ship checklist post-cliente-sync:**
- [ ] Todos os 🟡 items confirmados (ex: `status` actualizado para `delivered` só após cliente confirmar recepção; `tags` validadas contra taxonomia real do vault)
- [ ] Todos os 🔵 sources citados no frontmatter ou no body do ficheiro (ex: data de sessão de origem)
- [ ] Todos os 🟢 projections sinalizados explicitamente ao cliente (ex: `score_global` é estimativa DARIO — não auditoria certificada)

## Fully-worked A-tier example (delivery-ready reference)

```markdown
**[Internal DARIO action — Obsidian Save]**

Tipo detectado: **plan** (output de dario-wp-audit para Vivenda Creative Home)
Pasta: `05 - Claude - IA/Outputs/`
Filename: `2026-04-15 - Vivenda Creative Home - Plano Remodelacao WordPress.md`

---

Conteúdo a escrever:

---
project: Vivenda Creative Home
date: 2026-04-15
type: plan
status: draft
tags: [vivenda, wordpress, remodelacao, woocommerce, performance]
milestones: [auditoria-tecnica, migracao-tema, otimizacao-wc, go-live]
timeline_weeks: 8
---

# Plano de Remodelação WordPress — Vivenda Creative Home

**Data:** 2026-04-15
**Gerado por:** DARIO / dario-wp-audit
**Status:** Draft — aguarda aprovação cliente

## Resumo executivo

O site atual da Vivenda (vivenda.pt) opera em WordPress 6.3 com tema Flatsome 3.14
e WooCommerce 8.2. A auditoria identificou 3 bloqueadores Tier-0 e 11 issues Tier-1.
Este plano define o caminho de remodelação em 8 semanas.

## Bloqueadores Tier-0 (resolução imediata)

1. **Core Web Vitals reprovados** — LCP 6.2s (target < 2.5s); origem: imagens sem lazy-load
2. **SSL misto** — 14 assets servidos via HTTP em páginas HTTPS → alerta browser ativo
3. **WooCommerce 8.2 → 8.9 pending** — 3 CVEs críticos não patchados (CVE-2024-XXXX)

## Roadmap (8 semanas)

| Semana | Milestone | Owner |
|--------|-----------|-------|
| 1-2 | Auditoria técnica completa + staging clone | DARIO + Dev |
| 3-4 | Migração tema → GeneratePress + ACF | Dev |
| 5-6 | Otimização WooCommerce + Stripe checkout | Dev |
| 7 | QA + testes de regressão | DARIO |
| 8 | Go-live + monitorização 72h | Dev + Cliente |

## Próximos passos imediatos

- [ ] Cliente aprova orçamento até 2026-04-18
- [ ] Dev configura staging em staging.vivenda.pt
- [ ] DARIO agenda check-in semanal às sextas

---

**[Write tool executado]**
Path: `C:\Users\barda\OneDrive\Documents\VCHOME segundo cerebro\05 - Claude - IA\Outputs\2026-04-15 - Vivenda Creative Home - Plano Remodelacao WordPress.md`

**[RAG ingest executado]**
`mcp__dario-rag__ingest_text` → name: `obsidian/05 - Claude - IA/Outputs/2026-04-15 - Vivenda Creative Home - Plano Remodelacao WordPress`, collection: `obsidian`, tags: `[vivenda, wordpress, remodelacao]`

---

✅ **Guardado com sucesso.**
📄 `05 - Claude - IA/Outputs/2026-04-15 - Vivenda Creative Home - Plano Remodelacao WordPress.md` (52 linhas)
🔍 Indexado na RAG — pesquisável via DARIO search_kb com tags `vivenda`, `wordpress`, `remodelacao`.
```

---

## Output anti-patterns

- Usar `<client_name>`, `<date>`, `<path>` na confirmação final — o utilizador vê placeholders e perde confiança no sistema
- Guardar sem frontmatter completo — ficheiros sem `project`/`type`/`status` são invisíveis ao Dataview e ao RAG tagging
- Nomear com acentos ou caracteres especiais no filename (`Remodelação.md`) — quebra plugins Obsidian e sort alfabético
- Usar `-v2`, `-v3` em vez de nova data — contradiz o modelo de versioning por data e cria ambiguidade sobre qual é o "current"
- Escrever para diretório sem verificar que existe — falha silenciosa cria ficheiros órfãos fora do vault
- Fazer RAG ingest com `name` genérico (`"audit"`, `"plano"`) — colisões de namespace tornam docs irrecuperáveis por search
- Guardar rascunhos intermédios ou outputs < 20 linhas — polui o vault e dilui o sinal de pesquisa
- Persistir secrets, API keys ou PII no vault — vault sincroniza via OneDrive, exposição permanente e irrecuperável
- Ignorar o passo de verificação de duplicados — re-salvar o mesmo deliverable com data nova cria confusão sobre versão vigente
- Confirmar "guardado" sem fornecer path completo e contagem de linhas — utilizador não consegue verificar nem navegar para o ficheiro
