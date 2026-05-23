---
name: dario-rag-ingest
description: Smart ingest into the DARIO RAG — takes a file path, URL, or text, auto-chunks, tags based on content, and posts to localhost:8420. Handles PDFs, Markdown, URLs, raw text. Triggers on "ingerir RAG", "index this", "add to RAG", "guarda na RAG", "save to KB".
license: MIT
---

# DARIO Skill — RAG Ingest

Takes any piece of knowledge (a file, a URL, a text block, a conversation) and adds it to the DARIO RAG with appropriate metadata so it's retrievable later.

## When to activate

- User says "save this to the RAG" / "guarda isto na RAG"
- User pastes content and says "lembra-te disto"
- A substantive output is worth preserving beyond the Obsidian save
- User wants to ingest a competitor's content, a PDF book, or a blog post
- After completing a diagnostic / audit that has reusable patterns

## Workflow

### 1. Identify source type
- **File path** — existing `.md`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.txt`, `.py`, `.js`, `.json`, etc.
- **URL** — web page, blog post, documentation
- **Raw text** — user pasted content
- **Conversation output** — save current Claude-generated content

### 2. Derive metadata
- **Name:** `<collection>/<topic>/<slug>` format (e.g. `spec/accessibility-wcag-22`, `client/atrium/audit-2026-04`)
- **Collection:** one of
  - `dario` — DARIO internal knowledge (specs, squads, frameworks)
  - `obsidian` — auto-ingest from vault
  - `clients` — client-specific briefs, audits, outputs
  - `web` — external web content
  - `books` — canonical books / long-form
  - `notes` — quick notes
- **Source type:** `markdown` / `pdf` / `web` / `note` / `code` / `docx` / `excel` / `csv`
- **Tags:** derived from content — topic, client name, squad/spec, date, author if applicable. Max 10.

### 3. Call the ingest endpoint

#### For text / notes:
```
mcp__dario-rag__ingest_text(
  content: "<full markdown>",
  name: "<collection>/<slug>",
  source_type: "markdown",
  collection: "<collection>",
  tags: ["tag1", "tag2", ...]
)
```

#### For URLs:
```
mcp__dario-rag__ingest_url(
  url: "https://...",
  collection: "web",
  tags: [...],
  name: "<optional friendly name>"
)
```

#### For files (use direct POST):
```bash
curl -X POST http://localhost:8420/ingest/file \
  -F "file=@path/to/file.pdf" \
  -F "collection=<col>" \
  -F "tags=tag1,tag2"
```

### 4. Verify
- Check response has `status: "ok"` and `chunks: N > 0`
- If `status: "duplicate"`, content is unchanged — OK
- If error, diagnose (engine up? file readable?)

### 5. Confirm to user
- 1-line summary: "Ingerido em <collection> como <name> (N chunks)"
- Provide next-step suggestion: "Agora podes pesquisar com `mcp__dario-rag__search_kb(query: '...')` "

## Naming conventions (canonical)

| Collection | Name prefix | Example |
|---|---|---|
| `dario` | `spec/<topic>` | `spec/rag-engineering-evaluation` |
| `dario` | `xquads/<squad>-squad` | `xquads/ai-engineering-squad` |
| `dario` | `xquads/<squad>/agents-<names>` | `xquads/hormozi-squad/agents-core-chief-offers-leads` |
| `obsidian` | `obsidian/<folder>/<file>` | `obsidian/05 - Claude - IA/Outputs/2026-04-15 - ...` |
| `clients` | `client/<client-slug>/<type>` | `client/atrium/audit-2026-04-15` |
| `web` | hostname + path slug | `simonwillison.net/blog/2025/hyde` |
| `books` | `book/<author>/<title>` | `book/hormozi/100m-offers` |

## Tagging conventions

Always include:
- 1 **type tag:** `spec`, `squad`, `agent`, `audit`, `plan`, `decision`, `brief`, `contract`, `research`
- 1-3 **topic tags:** e.g. `wordpress`, `wcag`, `ga4`, `rgpd`
- 1 **client/project tag** if applicable: `atrium`, `lucas`, `vivenda`
- 1 **language tag** if relevant: `pt`, `en`

## Red flags — don't ingest

- Secrets (.env, credentials, API keys)
- Client confidential data without explicit permission
- Unparseable content (scan-only PDFs without OCR — run OCR first)
- Content shorter than 50 chars (no value)
- Binary files that aren't in the supported types

## Interactions
- Called by `dario-obsidian-save` (which saves file then ingests it)
- Called by `dario-client-onboard` to index new client context
- Called manually when user shares worth-preserving content

## Health check before ingesting (optional but recommended)
```
mcp__dario-rag__kb_health()
```
If not "ok", the ingest will fail — tell the user to start the engine first (`cd /c/dario-rag/engine && .venv/Scripts/python.exe main.py &`).

## Red Flags
- Never ingest content without first checking for duplicates via `search_kb` — duplicate ingestion creates redundant chunks that dilute search relevance and waste storage
- Never skip tagging when ingesting — untagged content is nearly impossible to filter, audit, or clean up later, and degrades the quality of every future RAG query
- Always verify the RAG engine is running (`kb_health`) before attempting ingest — ingesting into a stopped engine fails silently and the user assumes the content is indexed when it is not
- Never ingest secrets, credentials, or client-confidential data without explicit permission — RAG content persists indefinitely and may surface in future queries across different sessions
- Always use the canonical naming convention (`collection/topic/slug`) — inconsistent names make it impossible to locate, update, or delete specific sources later

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

---

### Gate 1 — Source type identificado e endpoint correto

- [ ] Source é um dos 4 tipos válidos: file path, URL, raw text, conversation output
- [ ] Endpoint chamado corresponde ao source type (`ingest_text` / `ingest_url` / `curl POST /ingest/file`)
- [ ] File extension está na lista de suportados (`.md`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.txt`, `.py`, `.js`, `.json`)
- [ ] Se source é PDF de scan, OCR verificado antes de ingestão

❌ NOT delivery-ready: "Chamei `ingest_text` com o conteúdo do ficheiro PDF diretamente."
✅ Delivery-ready: "Source é `atrium-audit-2026-04.pdf` (texto extraível, não scan) → chamei `curl -X POST http://localhost:8420/ingest/file -F 'file=@/c/dario/clients/atrium-audit-2026-04.pdf' -F 'collection=clients' -F 'tags=audit,atrium,wcag,pt'`"

---

### Gate 2 — Naming convention canónica aplicada

- [ ] Nome segue formato `<collection>/<topic>/<slug>` sem espaços nem maiúsculas
- [ ] Collection é uma das 6 válidas: `dario`, `obsidian`, `clients`, `web`, `books`, `notes`
- [ ] Slug é descritivo e inclui data quando relevante (e.g. `audit-2026-04-15`, não `audit-final-v2`)
- [ ] Nomes de cliente usam o slug canónico (`atrium`, `lucas`, `vivenda`, `cuidai`, `saquei`)

❌ NOT delivery-ready: `name: "Atrium Audit April"` ou `name: "client/Atrium/Audit Final V2"`
✅ Delivery-ready: `name: "client/atrium/audit-2026-04-15"`

---

### Gate 3 — Metadata e tags completas e úteis

- [ ] Mínimo 1 type tag (`audit`, `spec`, `plan`, `brief`, `research`, `decision`, `contract`)
- [ ] 1–3 topic tags derivados do conteúdo real (`wcag`, `ga4`, `wordpress`, `rgpd`)
- [ ] Client/project tag presente quando aplicável (`atrium`, `vivenda`, `lucas`)
- [ ] Language tag incluído se conteúdo não é inglês neutro (`pt`, `en`)
- [ ] Total de tags ≤ 10

❌ NOT delivery-ready: `tags: ["content", "document", "important"]`
✅ Delivery-ready: `tags: ["audit", "wcag", "wordpress", "atrium", "pt"]` (5 tags, todas derivadas do conteúdo)

---

### Gate 4 — Health check + duplicate check executados

- [ ] `mcp__dario-rag__kb_health()` chamado antes do ingest — resposta `"ok"` confirmada
- [ ] `search_kb` executado com query relevante para verificar duplicados antes de ingerir
- [ ] Se `status: "duplicate"` → comunicado ao utilizador sem re-ingerir
- [ ] Se engine não está up → instrução de arranque fornecida (`cd /c/dario-rag/engine && .venv/Scripts/python.exe main.py &`)

❌ NOT delivery-ready: Ingerir directamente sem verificar health e sem pesquisar duplicado, assumindo que ficou indexado.
✅ Delivery-ready: "`kb_health()` → `ok`. `search_kb(query: 'atrium wcag audit 2026')` → 0 resultados relevantes. Ingest seguro."

---

### Gate 5 — Resposta do endpoint verificada e comunicada

- [ ] Response contém `status: "ok"` e `chunks: N` onde `N > 0`
- [ ] Número de chunks reportado ao utilizador na confirmação
- [ ] Se `chunks: 0`, conteúdo era demasiado curto (<50 chars) ou não parseável — diagnosticado e reportado
- [ ] Próximo passo sugerido com query de exemplo concreta para o conteúdo ingerido

❌ NOT delivery-ready: "Ingerido com sucesso." (sem chunks, sem próximo passo)
✅ Delivery-ready: "Ingerido em `clients` como `client/atrium/audit-2026-04-15` (23 chunks). Pesquisa com `search_kb(query: 'atrium performance core web vitals')`"

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder

- [ ] Nenhum `<collection>`, `<slug>`, `<client-name>`, `<tag1>` no output final
- [ ] Nome do ficheiro/URL é o real, não um placeholder genérico
- [ ] Collection, tags e slug são específicos ao conteúdo ingerido nesta sessão
- [ ] Confirmação de ingestão menciona o nome canónico real e número de chunks real

❌ NOT delivery-ready: `name: "<collection>/<slug>"`, `tags: ["<tag1>", "<tag2>"]`
✅ Delivery-ready: `name: "client/vivenda/brief-seo-2026-05-02"`, `tags: ["brief", "seo", "wordpress", "vivenda", "pt"]`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
**Trigger:** Utilizador partilha o output de auditoria técnica da Atrium (texto colado, ~2 400 palavras)
e diz "guarda isto na RAG".

---

**Step 1 — Source type**
Raw text colado pelo utilizador. Endpoint: `mcp__dario-rag__ingest_text`.

**Step 2 — Health check**
```
mcp__dario-rag__kb_health()
→ { "status": "ok", "chunks_total": 4872, "sources": 61 }
```

**Step 3 — Duplicate check**
```
mcp__dario-rag__search_kb(query: "atrium audit tecnica 2026 wcag performance")
→ 0 resultados com score > 0.75. Sem duplicados.
```

**Step 4 — Derive metadata**
- Collection: `clients`
- Name: `client/atrium/audit-tecnica-2026-04-28`
- Source type: `markdown`
- Tags: `["audit", "wcag", "performance", "ga4", "atrium", "pt"]` (6 tags)

**Step 5 — Ingest**
```
mcp__dario-rag__ingest_text(
  content: "# Auditoria Técnica — Atrium\n**Data:** 2026-04-28\n\n## Core Web Vitals\n...",
  name: "client/atrium/audit-tecnica-2026-04-28",
  source_type: "markdown",
  collection: "clients",
  tags: ["audit", "wcag", "performance", "ga4", "atrium", "pt"]
)
```

**Step 6 — Verify response**
```json
{ "status": "ok", "chunks": 18, "source": "client/atrium/audit-tecnica-2026-04-28" }
```

**Step 7 — Confirm to user**

> ✅ Ingerido em `clients` como **client/atrium/audit-tecnica-2026-04-28** (18 chunks).
>
> Pesquisa agora com:
> `mcp__dario-rag__search_kb(query: "atrium wcag core web vitals recomendações")`
```

---

## Output anti-patterns

- Usar `ingest_text` com conteúdo de um PDF sem verificar se é texto extraível — falha silenciosa ou chunks corrompidos
- Nomear como `client/Atrium/Audit Final V2` — maiúsculas e "final/v2" quebram convenção canónica e impedem localização futura
- Saltar `kb_health()` e assumir que o engine está up — o ingest falha e o utilizador pensa que o conteúdo está indexado quando não está
- Confirmar "ingerido com sucesso" sem reportar número de chunks — impede o utilizador de detectar ingestão vazia (`chunks: 0`)
- Ingerir sem pesquisar duplicados primeiro — cria chunks redundantes que diluem relevância de todas as queries futuras
- Tags genéricas como `["document", "content", "important"]` — inúteis para filtrar, auditar ou limpar a KB mais tarde
- Ingerir ficheiro `.env` ou texto com `sk-`, `Bearer `, `password=` — credenciais persistem na KB indefinidamente e surfaceiam em queries futuras
- Omitir next-step query suggestion — o utilizador não sabe como verificar que o conteúdo está pesquisável
