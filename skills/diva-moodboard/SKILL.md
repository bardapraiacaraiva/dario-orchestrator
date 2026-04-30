---
name: diva-moodboard
description: Moodboard generation for interior design concepts. Defines style direction, color palette with Pantone/NCS references, materials board, furniture references, lighting concept, and AI image generation prompts. Triggers on "moodboard", "mood board", "conceito", "concept board", "inspiracao", "estilo interiores", "paleta de cores".
license: MIT
---

# DIVA Skill — Moodboard / Interior Design Concept Generator

Creates a comprehensive interior design moodboard document from a client briefing. Goes beyond aesthetics to include actionable specifications: color references (Pantone/NCS), material selections with suppliers, furniture references with dimensions, lighting layering, and ready-to-use AI prompts for visual concept generation via Midjourney or DALL-E.

## When to activate

- Client provides a design brief or says "quero um conceito para..."
- Starting a new interior design project (residential or commercial)
- Client shares inspiration images and wants a cohesive direction
- Architect/designer needs to formalize style direction for team
- Preparing a concept presentation for client approval
- Client says "nao sei o que quero" -- use this to guide the conversation

## Workflow

### 1. Gather inputs

- **Space type:** living room / bedroom / kitchen / bathroom / office / restaurant / hotel / retail
- **Client profile:** age range, lifestyle, family composition
- **Preferences stated:** any styles, colors, materials mentioned
- **Anti-preferences:** "nao quero nada rustico", "odeio cinzento"
- **Budget level:** economico / medio / premium / luxo
- **Location context:** apartment in Lisboa / moradia no Algarve / escritorio no Porto
- **Existing constraints:** architectural features to keep, fixed elements (floor, structure)
- **Functional requirements:** storage needs, entertaining, work-from-home, kids, pets
- **Mood words:** (ask client to pick 3-5) acolhedor, sofisticado, minimalista, dramatico, organico, luminoso, intimo, cosmopolita, atemporal, ousado

If no mood words provided, present the list and ask client to choose.

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "interior design style direction moodboard concept", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "color palette materials specification interior", collection: "dario", limit: 5)
```

### 3. Define style direction

Select primary style + secondary influence from:

| Style | Characteristics | Best for |
|---|---|---|
| Contemporaneo Portugues | Natural materials, azulejo accents, warm neutrals, craft details | Residencial PT |
| Mediterraneo Moderno | Lime/stone textures, terracotta, linen, arched forms | Sul PT, coastal |
| Minimalista Quente | Clean lines, warm wood, soft textiles, few objects | Apartamentos urbanos |
| Mid-Century Moderno | Organic curves, teak, brass, bold accents | Apartamentos 60s-70s |
| Japandi | Japanese minimalism + Scandi warmth, wabi-sabi | Espacos pequenos |
| Industrial Refinado | Exposed elements + warm materials, metal + wood | Lofts, escritorios |
| Classico Contemporaneo | Traditional proportions, modern finishes, mouldings | Moradias, casas senhoras |
| Maximalista Curado | Pattern mixing, collected look, art-heavy, layered | Personalidades fortes |
| Biophilic | Plants, natural light, organic shapes, earth tones | Wellness, escritorios |
| Art Deco Revival | Geometric patterns, velvet, brass, jewel tones | Hoteis, restauracao |

State: "Primary: [X] with [Y] influences" and explain why this suits the client.

### 4. Build color palette

Define 5-7 colors with professional references:

| Role | Color | Pantone | NCS | Hex | Usage |
|---|---|---|---|---|---|
| Base (60%) | <name> | <PANTONE ref> | <NCS ref> | #XXXXXX | Paredes, tectos, grandes superficies |
| Secondary (25%) | <name> | <PANTONE ref> | <NCS ref> | #XXXXXX | Mobiliario grande, cortinas, tapetes |
| Accent 1 (10%) | <name> | <PANTONE ref> | <NCS ref> | #XXXXXX | Almofadas, arte, objectos decorativos |
| Accent 2 (5%) | <name> | <PANTONE ref> | <NCS ref> | #XXXXXX | Detalhes metalicos, pequenos acentos |
| Neutral dark | <name> | <PANTONE ref> | <NCS ref> | #XXXXXX | Molduras, detalhes, ancoragem visual |
| Neutral light | <name> | <PANTONE ref> | <NCS ref> | #XXXXXX | Fundos, transicoes |
| Wood tone | <name> | -- | -- | #XXXXXX | Pavimento, mobiliario em madeira |

Apply the 60-30-10 rule. Verify contrast accessibility for commercial spaces.

### 5. Materials board

Define 8-12 key materials:

| Material | Application | Finish | Reference/Supplier | Budget tier |
|---|---|---|---|---|
| Pedra natural (ex: calcario Moleanos) | Bancada cozinha, WC | Amaciado | Solancis / Marmetal | Premium |
| Ceramica (ex: Mutina Mews) | Pavimento WC | Mate | Revigrés / Margres | Medio-premium |
| Madeira (ex: carvalho europeu) | Pavimento geral | Mate, 3 demaos verniz | Jular / Wicanders | Medio |
| Metal (ex: latao escovado) | Torneiras, puxadores | Escovado | Bruma /DERA | Premium |
| Tecido (ex: linho belga) | Cortinas, almofadas | Natural | Designers Guild / Dedar | Premium |
| Papel de parede | Parede destaque | Texturado | Cole & Son / Pierre Frey | Premium |
| Microcimento | Pavimento continuo | Mate | Topcret / Microbel | Medio |
| Vidro | Divisorias, espelhos | Transparente/fumado | Vidraria local | Medio |

Include Portuguese suppliers where possible.

### 6. Furniture references

For each key piece, provide:
- **Piece name + designer/brand**
- **Dimensions (LxWxH)**
- **Material/upholstery**
- **Price range**
- **Alternative at lower price point**
- **Portuguese brand alternative** (if exists: Wewood, AROUNDtheTREE, DAM, Gualter, etc.)

### 7. Lighting concept

Layer the lighting plan:

| Layer | Purpose | Type | Example | Color temp |
|---|---|---|---|---|
| Ambiente | General illumination | Indirect cove / pendente central | Flos IC / Vibia Wireflow | 2700-3000K |
| Tarefa | Functional (ler, cozinhar) | Candeeiro mesa / suspensao direccionada | Artemide Tolomeo | 3000-3500K |
| Destaque | Art, texturas, architectural features | Spots encastrados / projetores | Modular Qbini | 2700-3000K |
| Decorativo | Mood, personalidade | Candeeiro escultura / velas | Tom Dixon Melt | 2200-2700K |
| Natural | Daylight strategy | Cortinas, espelhos, superficies reflectivas | -- | -- |

### 8. Generate AI visualization prompts

Create 3 prompts for concept visualization:

**Midjourney prompt format:**
```
Interior design photograph of [space type], [style direction], [key materials], [color palette description], [lighting mood], [key furniture pieces], [atmosphere words], professional interior photography, editorial quality, soft natural light from [direction], Canon EOS R5, 24mm lens --ar 16:9 --v 6.1 --style raw
```

**DALL-E prompt format:**
```
A photorealistic interior design photograph showing [detailed description]. The space features [materials and finishes]. Color palette centers on [colors]. Furniture includes [key pieces]. Natural light enters from [direction], creating [mood]. Professional architectural photography style.
```

Create prompts for: (a) wide shot, (b) detail/vignette, (c) atmospheric/mood shot.

## Output template

```markdown
---
project: <project name>
date: <YYYY-MM-DD>
type: moodboard
style: <primary style>
spaces: <list of spaces>
---

# Moodboard -- <Project Name>

## Conceito
> <2-3 sentence style statement capturing the essence of the concept>

## Direccao de estilo
- **Estilo primario:** <name>
- **Influencia secundaria:** <name>
- **Palavras-chave:** <3-5 mood words>

## Paleta de cores
| Funcao | Cor | Pantone | NCS | Hex | Aplicacao |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

## Materiais
| Material | Aplicacao | Acabamento | Fornecedor | Tier |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Mobiliario de referencia
| Peca | Designer/Marca | Dimensoes | Preco | Alternativa PT |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Conceito de iluminacao
| Camada | Tipo | Referencia | Temp. cor |
|---|---|---|---|
| ... | ... | ... | ... |

## Prompts para visualizacao AI

### Vista geral (Midjourney)
```
<prompt>
```

### Detalhe/vinheta (Midjourney)
```
<prompt>
```

### Atmosfera (DALL-E)
```
<prompt>
```

## Proximos passos
- [ ] Apresentar moodboard ao cliente para aprovacao
- [ ] Apos aprovacao, detalhar especificacoes por divisao
- [ ] Solicitar amostras de materiais aos fornecedores
- [ ] Gerar renders 3D com `diva-render-brief`
- [ ] Iniciar orcamentacao com fornecedores
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Project> - Moodboard.md`

## Red flags -- don't do this

- Never present a moodboard without color references (Pantone/NCS) -- "azul bonito" is not a spec
- Never mix more than 2 style directions -- coherence breaks down
- Never forget to include a budget-appropriate alternative for premium references
- Never ignore the client's anti-preferences (they remember what they hate more than what they like)
- Never specify materials without checking availability in Portugal
- Never create a lighting plan with only one layer -- always minimum 3 layers
- Never use AI prompts without specifying "interior photography" style -- otherwise get CGI look
- Never present Pantone colors without verifying they exist in the current Pantone library

## Interactions

- Follow up with `diva-render-brief` for 3D visualization briefs
- Pair with `diva-timeline` for procurement lead times in project schedule
- Follow up with `dario-proposal` for design fee proposal
- Save via `dario-obsidian-save` to vault
