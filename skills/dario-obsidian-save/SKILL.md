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
