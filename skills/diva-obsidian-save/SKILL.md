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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

---

### Gate 1 — Destination folder correto

- [ ] Conteúdo classificado como Spec/Audit/Report/Schedule → pasta `05 - Claude - IA/Outputs/`
- [ ] Design decision ou material selection → pasta `05 - Claude - IA/Decisoes/`
- [ ] Brief, site analysis, requirements → pasta `05 - Claude - IA/Contextos/`
- [ ] Quick note ou supplier contact → pasta `00 - Inbox/`
- [ ] Nenhuma pasta inventada fora da vault structure canónica

❌ NOT delivery-ready: `03 - Recursos/Domotica/especificacao.md` — pasta errada para um output gerado por Claude  
✅ Delivery-ready: `C:\Users\barda\OneDrive\Documents\VCHOME segundo cerebro\05 - Claude - IA\Outputs\2026-04-21 - Vila Cascais - Especificacao Domotica Premium.md`

---

### Gate 2 — Filename segue convenção exacta

- [ ] Formato `YYYY-MM-DD - <Tema> - <Titulo>.md` respeitado (3 partes separadas por ` - `)
- [ ] Zero acentos no filename (`Decisao` não `Decisão`, `Certificacao` não `Certificação`)
- [ ] Tema é nome do projecto quando client-specific; `DIVA` quando genérico
- [ ] Comprimento ≤ 120 chars, apenas ASCII safe
- [ ] Extensão `.md` presente

❌ NOT delivery-ready: `especificacao domotica vila cascais.md`  
✅ Delivery-ready: `2026-04-21 - Vila Cascais - Especificacao Domotica Premium.md`

---

### Gate 3 — Frontmatter DIVA completo e válido

- [ ] Campos obrigatórios presentes: `project`, `date`, `type`, `status`, `specializations`, `squads`, `tags`
- [ ] `type` é um valor da lista canónica (`smart-home-spec`, `energy-cert`, `material-schedule`, etc.) — sem valores livres inventados
- [ ] `specializations` e `squads` são arrays YAML válidos com valores da lista canónica
- [ ] Campos opcionais do type incluídos quando aplicável (ex.: `protocol`, `tier`, `estimated_cost` para `smart-home-spec`)
- [ ] `status` tem valor válido: `draft | delivered | approved | implemented`

❌ NOT delivery-ready: `type: especificacao domotica` — valor livre não canónico; `squads: engineering` — não é um squad válido  
✅ Delivery-ready: `type: smart-home-spec`, `squads: [engineering-squad, construction-squad]`, `estimated_cost: 18500€`, `protocol: KNX`, `tier: premium`

---

### Gate 4 — Conteúdo substantivo, não duplicado

- [ ] Ficheiro contém conteúdo substantivo (não apenas links, referências ou rascunhos intermédios)
- [ ] Verificado que ficheiro com mesmo nome não existe já na vault (sem duplicação silenciosa)
- [ ] Output corresponde ao que foi efectivamente gerado no contexto DIVA (não conteúdo genérico)
- [ ] Corpo do documento inclui o deliverable completo, não um resumo truncado

❌ NOT delivery-ready: ficheiro salvo com apenas `Ver conversa anterior` ou body vazio após o frontmatter  
✅ Delivery-ready: frontmatter + secções completas (ex.: `## Dispositivos`, `## Orçamento Estimado`, `## Protocolo KNX — Zona A`) com dados reais do projecto

---

### Gate 5 — Skill scope respeitado (não usar para conteúdo non-DIVA)

- [ ] Conteúdo é inequivocamente de arquitectura / design de interiores / construção / domótica / energia / paisagismo
- [ ] Se conteúdo for marketing, SEO, SaaS ou DARIO-geral → usar `dario-obsidian-save` em vez deste skill
- [ ] Specializations e squads fazem sentido para o conteúdo (ex.: output de certificação energética inclui `energy` + `engineering-squad`)
- [ ] Não foram misturadas specializations non-DIVA (ex.: `marketing`, `seo`) no frontmatter

❌ NOT delivery-ready: usar `diva-obsidian-save` para guardar um plano de conteúdo Instagram da Cuidai  
✅ Delivery-ready: usar `diva-obsidian-save` para `Moradia Sintra - Relatorio Acustico SCE` com `specializations: [acoustics, energy]`

---

### Gate 6 — Output usa NOME DO PROJECTO REAL + dados reais, zero placeholders

- [ ] Path completo escrito com nome de projecto real (ex.: `Vila Cascais`, `Apartamento Alfama`, `Moradia Sintra`)
- [ ] Nenhum `<project name>`, `<Titulo>`, `<YYYY-MM-DD>` ou `<list of squads>` visível no output final
- [ ] `date` é a data actual real, não `YYYY-MM-DD` literal
- [ ] Valores numéricos reais presentes onde aplicável (`building_area_m2: 187`, `estimated_cost: 18500€`, `device_count: 34`)
- [ ] Frontmatter fechado correctamente com `---` no início e no fim

❌ NOT delivery-ready: `project: <project name>`, `date: YYYY-MM-DD`, `tags: [<relevant tags>]`  
✅ Delivery-ready: `project: Vila Cascais`, `date: 2026-04-21`, `tags: [domotica, KNX, premium, moradia-unifamiliar]`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / memória / dados do cliente
- 🟡 **assumed** — plausível mas precisa de confirmação do cliente antes de entregar
- 🟢 **projection** — estimativa por design (não verificável no momento do save)

Output checklist upfront mostra ao leitor exatamente o que é trust-as-is vs. o que precisa de verify antes de guardar no vault.  **Honest transparency > inflated delivery.**

---

❌ **NOT delivery-ready:**
```
Filename: 2026-04-21 - Vila Cascais - Especificacao Domotica Premium.md
project: Vila Cascais
specializations: [domotica, mep]
status: delivered
```
*Sem labels — leitor assume que project name, specializations e status estão todos verified. Podem estar errados.*

---

✅ **Delivery-ready:**
```
Filename gerado: 2026-04-21 - Vila Cascais - Especificacao Domotica Premium.md
  🔵 verified   — data confirmada na sessão; "Vila Cascais" vem do brief do cliente
  🟡 assumed    — folder destino "05 - Claude - IA/Outputs/" (confirmar se projeto
                   já tem pasta própria em 01 - Projetos/)
  🟡 assumed    — status: "draft" (cliente ainda não validou entrega formal)
  🟢 projection — specializations: [domotica, mep] (inferido do conteúdo gerado;
                   confirmar squads envolvidos com coordenador de projeto)
```

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — folder de destino validado; status (`draft` / `delivered` / `approved`) confirmado com cliente
- [ ] All 🔵 sources cited — project name, date e brief origin documentados no frontmatter ou body
- [ ] All 🟢 projections labeled como tal ao cliente — specializations e squads marcados como "a confirmar" até validação técnica

## Fully-worked A-tier example (delivery-ready reference)

```markdown
Ficheiro salvo em:
C:\Users\barda\OneDrive\Documents\VCHOME segundo cerebro\05 - Claude - IA\Outputs\2026-04-21 - Vila Cascais - Especificacao Domotica Premium.md

---
project: Vila Cascais
date: 2026-04-21
type: smart-home-spec
status: delivered
specializations: [domotica, mep, lighting]
squads: [engineering-squad, construction-squad, interiors-squad]
protocol: KNX
tier: premium
estimated_cost: 18500
device_count: 34
tags: [domotica, KNX, premium, moradia-unifamiliar, cascais, 2026]
---

# Especificação Domótica Premium — Vila Cascais

## Resumo executivo

Especificação técnica para sistema de domótica KNX em moradia unifamiliar T4+1
(287 m²) em Cascais. Tier Premium. Custo estimado: **18.500€ (materiais + instalação)**.
34 dispositivos distribuídos por 6 zonas funcionais.

## Protocolo e arquitectura

- **Protocolo principal:** KNX (ISO 14543-3)
- **Topologia:** Bus descentralizado, 2 linhas de área
- **Interface central:** Gira X1 + app Gira One (iOS/Android)
- **Integração energia:** Contador smart Schneider PM2220 + PV monitoring

## Zonas e dispositivos

| Zona | Dispositivos | Funções |
|---|---|---|
| Zona A — Hall + Sala | 8 | Iluminação cenas, estores, climatização |
| Zona B — Cozinha | 5 | Iluminação funcional, electrodomésticos smart |
| Zona C — Suite principal | 6 | Iluminação circadiana, blackout, AVAC local |
| Zona D — Quartos (×2) | 6 | Iluminação básica, estores motorizados |
| Zona E — Exterior | 5 | Segurança, iluminação jardim, portão |
| Zona F — Técnica | 4 | Quadro KNX, UPS, router, servidor local |

## Estimativa de custo

| Item | Custo (€) |
|---|---|
| Materiais KNX (actuadores, sensores) | 8.200 |
| Iluminação (Gira, Bega exterior) | 4.100 |
| Instalação e programação | 4.800 |
| Formação cliente (2h) | 400 |
| Contingência 5% | 875 |
| **Total** | **18.375** |

## Notas de implementação

- Cablagem KNX a instalar em paralelo com obra de electricidade (fase estrutural)
- Coordenação com squad de construção obrigatória antes de fechar paredes
- Pré-instalação PV prevista: deixar conduíte 32mm da cobertura ao quadro técnico
- Próximo passo: validação com cliente semana de 28 Abr 2026

## Referências cruzadas

- [[2026-04-15 - Vila Cascais - Brief Cliente]]
- [[2026-04-18 - Vila Cascais - Decisao Protocolo KNX vs Z-Wave]]
```

---

## Output anti-patterns

- Usar `diva-obsidian-save` para conteúdo non-DIVA (marketing, SEO, copy) — usar `dario-obsidian-save`
- Deixar placeholders literais no path ou frontmatter: `<project name>`, `<YYYY-MM-DD>`, `<Titulo>`
- Inventar valores de `type` fora da lista canónica: `type: domótica spec` em vez de `type: smart-home-spec`
- Guardar ficheiro em pasta errada: output de especificação técnica em `03 - Recursos/` em vez de `05 - Claude - IA/Outputs/`
- Filename com acentos: `Decisão-AVAC.md` quebra plugins Obsidian — usar sempre `Decisao-AVAC.md`
- Omitir campos opcionais relevantes: guardar `smart-home-spec` sem `protocol`, `tier`, `estimated_cost`
- Duplicar ficheiro sem verificar existência prévia na vault
- Body vazio ou apenas com links após frontmatter — conteúdo substantivo obrigatório
- `squads` com valores inválidos como `engineering` em vez de `engineering-squad`
- Data hardcoded como `YYYY-MM-DD` literal em vez da data real do dia
