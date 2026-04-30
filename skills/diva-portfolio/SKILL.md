---
name: diva-portfolio
description: "Generate a professional case study / portfolio page from a completed architecture or design project. Includes before/after, concept, materials, budget summary, timeline, team, and client testimonial. Output as Markdown or HTML for website/social. Triggers on \"portfolio\", \"case study\", \"projecto concluido\", \"showcase\", \"publicar projecto\", \"antes depois\", \"portfolio entry\"."
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# DIVA Portfolio — Project Case Study Generator

Transform a completed project into a professional case study for portfolio, website, social media, or publication submission.

## When to activate

Invoke `/diva-portfolio` when:
- Project is complete and client approved for publication
- User wants to showcase work on website or social
- User preparing submission for design award/publication
- User building portfolio for new client pitch

## Workflow

### 1. Gather project data
Search all sources:
```
mcp__dario-rag__search_kb(query: "<project name>", collection: "diva", limit: 10)
```
Check agent memory, Obsidian vault outputs, briefing, moodboard, renders.

### 2. Structure the case study

**A. Hero Section**
- Project name + location
- Typology (remodelacao T3 / moradia nova / hotel boutique)
- Area (m2)
- Year completed
- 1 hero image/render (or Midjourney prompt to generate)

**B. The Brief**
- What the client wanted (3-5 bullets)
- Key challenges identified
- Budget range (if client approves sharing)

**C. The Concept**
- Design direction chosen (style + designer reference)
- Key design decisions and why
- Moodboard reference (if exists)

**D. Before & After** (if renovation)
- Before: description of original state
- Challenges: patologias, layout issues, regulatory constraints
- After: transformation highlights
- (Photo pairs if available, or Midjourney prompts for conceptual before/after)

**E. Design Details**
Room-by-room or area-by-area highlights:
- Key material choices with brand/reference
- Lighting concept
- Furniture selections
- Custom elements (carpintaria, serralharia)
- Colour palette with hex codes

**F. Technical Highlights**
- Structural interventions (if any)
- MEP innovations (piso radiante, domotica, solar)
- Energy certification achieved (classe)
- Sustainability features

**G. The Numbers**
| Metrica | Valor |
|---|---|
| Area intervencionada | X m2 |
| Duracao obra | X meses |
| Orcamento final | EUR X (se autorizado) |
| Valorizacao estimada | +X% |

**H. Team**
- Arquitecto:
- Designer interiores:
- Empreiteiro:
- Fotografo:

**I. Client Testimonial**
Template para pedir ao cliente:
"O que mais gostou no processo? O que mais o surpreendeu no resultado? Recomendaria?"

### 3. Generate outputs

**Format 1: Markdown (Obsidian/Blog)**
Complete case study in markdown with frontmatter.

**Format 2: HTML (Website/Social)**
Use `mcp__aidesigner__generate_design` para criar:
- Landing page visual do case study
- Grid layout com imagens + texto
- Responsive, pronto para website

**Format 3: Instagram Carousel**
10 slides texto para Instagram:
1. Hero image + nome projecto
2. O desafio
3. O conceito
4. Antes (se aplicavel)
5. Depois — sala
6. Depois — cozinha
7. Depois — WC
8. Detalhe material
9. Os numeros
10. CTA ("Quer transformar o seu espaco?")

**Format 4: Award Submission**
Estrutura para submissao a premios:
- Project description (500 words)
- Design intent
- Innovation/sustainability
- Technical data
- Image selection guide

## Output template

```markdown
---
project: <nome>
date: <YYYY-MM-DD>
type: portfolio
location: <morada>
area_m2: <N>
year: <YYYY>
style: <direccao>
designer_ref: <designer squad>
tags: [portfolio, case-study, <tipo>]
---

# [Project Name] — [Location]

> [One-line tagline that captures the essence]

## The Brief
[3-5 bullets]

## The Concept
[Design narrative — 150-200 words]

## Design Highlights

### [Room/Area 1]
[Description + materials + key decisions]

### [Room/Area 2]
[...]

## Materials Palette
| Material | Application | Reference |
|---|---|---|
| [pavimento] | [sala] | [marca + referencia] |

## The Numbers
| | |
|---|---|
| Area | X m2 |
| Duracao | X meses |
| Equipa | [nomes] |

## Photography
[Credits + image descriptions for social/web]
```

## Save location
- Obsidian: `05 - Claude - IA/Outputs/YYYY-MM-DD - [Projecto] - Portfolio Case Study.md`
- HTML: `[projecto]-portfolio.html`

## Red flags
- NUNCA publicar sem autorizacao escrita do cliente
- NUNCA revelar orcamento sem aprovacao
- NUNCA usar fotos sem creditos ao fotografo
- SEMPRE pedir testimonial antes de publicar
- SEMPRE verificar se ha acordo de confidencialidade
