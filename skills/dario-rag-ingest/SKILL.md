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
