---
name: diva-obsidian-save
description: Save DIVA architecture/design/construction outputs to the Obsidian vault with correct folder, naming convention (YYYY-MM-DD - Tema - Titulo.md), and DIVA-specific frontmatter (project, type, specializations, squads). Triggers on "save to vault", "guarda no obsidian", "guardar", "obsidian save".
license: MIT
---

# DIVA Skill — Obsidian Save (Architecture/Design/Construction)

Persists DIVA deliverables to the user's Obsidian vault using canonical folder structure and naming. Same structural pattern as dario-obsidian-save but specialized for architecture, interior design, and construction content with DIVA-specific metadata.

## When to activate

- After generating any DIVA deliverable (energy cert, smart home spec, material schedule, project brief, site analysis, etc.)
- User explicitly says "guarda isto" / "save this" / "guardar" in context of architecture/design content
- At the end of DIVA skill executions: `diva-energy`, `diva-smart-home`, `diva-projeto`, etc.
- When a DIVA output is worth surviving beyond this chat session

Do NOT use for:
- Non-DIVA content (marketing, SEO, SaaS) — use `dario-obsidian-save` instead
- Trivial chat responses or intermediate drafts
- Content already saved (check before duplicating)
- Files that contain only links or references without substantive content

## Vault structure (reference)

```
C:\Users\barda\OneDrive\Documents\VCHOME segundo cerebro\
├── 00 - Inbox\              ← quick notes, unsorted
├── 01 - Projetos\           ← active projects
├── 02 - Areas\              ← permanent areas of responsibility
├── 03 - Recursos\           ← reference library
├── 04 - Arquivo\            ← inactive
└── 05 - Claude - IA\        ← Claude-generated content
    ├── Outputs\             ← deliverables (specs, audits, reports, schedules)
    ├── Decisoes\            ← design decisions, material selections, technical choices
    ├── Contextos\           ← project briefs, site analyses, client requirements
    └── sessoes.md           ← session end log (hook)
```

## Workflow

### 1. Determine content type and destination

| Content type | Destination folder | Examples |
|---|---|---|
| Spec / Audit / Report / Schedule | `05 - Claude - IA/Outputs/` | Energy cert prep, smart home spec, material takeoff, site audit |
| Design decision / Material selection | `05 - Claude - IA/Decisoes/` | Stone vs porcelain decision, HVAC system choice, structural option |
| Project context / Brief / Requirements | `05 - Claude - IA/Contextos/` | Client brief, site analysis, program of requirements, budget envelope |
| Quick notes / References | `00 - Inbox/` | Supplier contact, regulation note, site photo notes |

### 2. Build filename

Convention: `YYYY-MM-DD - <Project or Tema> - <Titulo>.md`

Examples:
- `2026-04-21 - Vila Cascais - Especificacao Domotica Premium.md`
- `2026-04-21 - Apartamento Alfama - Certificacao Energetica SCE Prep.md`
- `2026-04-21 - Moradia Sintra - Decisao Sistema AVAC.md`
- `2026-04-21 - DIVA - Analise Materiais Fachada Ventilada.md`

Rules:
- No accents in filename (avoid metadata issues in some Obsidian plugins)
- Max 120 chars
- ASCII safe
- Use project name as tema when client-specific; use "DIVA" for generic architecture content

### 3. Build DIVA-specific frontmatter

Minimum required:
```yaml
---
project: <project name>
date: YYYY-MM-DD
type: <content type>
status: draft|delivered|approved|implemented
specializations: [<list of DIVA specializations involved>]
squads: [<list of DIVA squads involved>]
tags: [<relevant tags>]
---
```

**Type values** (DIVA-specific):
- `energy-cert` — SCE certification preparation
- `smart-home-spec` — Domotica specification
- `material-schedule` — Material quantities and specifications
- `site-analysis` — Site survey and analysis
- `design-brief` — Client requirements and program
- `construction-spec` — Construction methodology and details
- `budget-estimate` — Cost estimation and budget
- `renovation-plan` — Renovation scope and phasing
- `structural-report` — Structural assessment or recommendations
- `landscape-design` — Garden and exterior design
- `lighting-design` — Lighting layout and specification
- `acoustic-report` — Acoustic analysis and treatment
- `decision` — Technical or design decision record
- `context` — Project context document
- `regulation-check` — Regulatory compliance review

**Specialization values:**
- `architecture` — Building design, spatial planning
- `interiors` — Interior design, finishes, furniture
- `construction` — Building methods, site management
- `structural` — Structural engineering
- `mep` — Mechanical, electrical, plumbing
- `energy` — Energy performance, sustainability
- `landscape` — Landscape architecture
- `domotica` — Smart home, automation
- `acoustics` — Sound insulation, room acoustics
- `lighting` — Lighting design
- `regulations` — Portuguese building regulations (RGEU, RJUE, etc.)

**Squad values** (DIVA squad references):
- `architecture-squad` — Design and spatial planning
- `engineering-squad` — Structural, MEP, energy
- `construction-squad` — Building methods, materials, site
- `interiors-squad` — Finishes, furniture, decoration
- `regulations-squad` — Compliance, licensing, certification
- `sustainability-squad` — Energy, environment, materials lifecycle

Additional optional fields per type:
- `energy-cert`: `current_class`, `target_class`, `climate_zone`, `building_area_m2`
- `smart-home-spec`: `protocol`, `tier`, `estimated_cost`, `device_count`
- `material-schedule`: `total_cost`, `supplier_count`, `lead_time_weeks`
- `budget-estimate`: `total_budget`, `cost_per_m2`, `contingency_pct`
- `decision`: `decision_by`, `alternatives`, `selected_option`, `rationale`

### 4. Write the file

Use the Write tool directly. Path construction:
```
C:\Users\barda\OneDrive\Documents\VCHOME segundo cerebro\<destination folder>\<filename>.md
```

Full path example:
```
C:\Users\barda\OneDrive\Documents\VCHOME segundo cerebro\05 - Claude - IA\Outputs\2026-04-21 - Vila Cascais - Especificacao Domotica Premium.md
```

### 5. Trigger RAG ingest (recommended for substantive content)

If the file is substantive and should be searchable immediately, call:
```
mcp__dario-rag__ingest_text(
  content: "<full content>",
  name: "diva/<subfolder>/<slug>",
  source_type: "markdown",
  collection: "diva",
  tags: ["architecture", "<specialization>", "<project>", ...]
)
```

Use collection `diva` (not `dario` or `obsidian`) to keep architecture content separated in RAG.

### 6. Confirm to user

Report:
- Full path where saved
- File size / line count
- Frontmatter summary (type, specializations, squads)
- RAG status: "indexado na RAG DIVA, pesquisavel via search_kb com collection 'diva'"

## Naming edge cases

- **Multiple specializations in one doc** — pick the primary one for the filename, list all in frontmatter
- **Generic DIVA doc (no project)** — use "DIVA" as tema: `2026-04-21 - DIVA - Guia Materiais Fachada.md`
- **Supplier/product research** — use supplier name: `2026-04-21 - Revigrés - Catalogo Porcelanico Grande Formato.md`
- **Regulation notes** — use regulation code: `2026-04-21 - RGEU - Alturas Minimas Pe Direito.md`
- **Version history** — DO NOT use `-v2`, `-v3`. Save as new file with newer date. Vault history is Git.

## Cross-references with DARIO skills

- If content is mixed (e.g., website for architecture firm), use `dario-obsidian-save` for the digital/marketing parts and `diva-obsidian-save` for the architecture content
- When `diva-projeto` loads a project, it searches files saved by this skill
- `diva-rag-ingest` is called by this skill for immediate RAG indexing

## Red flags — don't save when

- Content is less than 20 lines (probably not worth persisting)
- Content is a direct copy of something already in vault (search first)
- User gave explicit "do not save" / "nao guardes"
- Contains client confidential data that shouldn't be in a synced vault (OneDrive)
- Contains pricing from suppliers that may be commercially sensitive
- Draft iterations — save only the final version unless explicitly asked to version
