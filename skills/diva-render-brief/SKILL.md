---
name: diva-render-brief
description: 3D rendering brief for visualization teams or AI tools. Captures camera angle, lighting, materials, furniture, styling, atmosphere, and includes Midjourney/DALL-E prompts for quick AI concepts. Triggers on "render", "3D", "visualizacao", "render brief", "fotorrealismo", "imagem 3D", "Midjourney arquitectura".
license: MIT
---

# DIVA Skill — 3D Render Brief Generator

Creates a detailed brief for 3D architectural visualization, whether for a professional rendering team (V-Ray, Corona, Enscape, Lumion) or for AI-generated concept images (Midjourney, DALL-E, Stable Diffusion). Captures every parameter a visualization artist needs: camera setup, lighting conditions, material specifications, furniture placement, styling details, and atmosphere. Includes ready-to-use AI prompts calibrated for architectural visualization quality.

## When to activate

- Designer/architect needs renders for client presentation
- Marketing team needs visuals for property listing or campaign
- Client asks "como vai ficar?" and needs to see the space
- Social media content creation for portfolio
- Competition/tender submission requiring visualizations
- Quick AI concept needed before commissioning full 3D renders
- Briefing an external visualization studio

## Workflow

### 1. Gather inputs

- **Space:** which room/area to render (reference floor plan if available)
- **Source material:** floor plan, moodboard (from `diva-moodboard`), material specs, furniture list
- **Purpose:** client presentation / marketing / social media / competition / internal review
- **Deliverable format:** still image / 360 panorama / animation / virtual tour
- **Resolution:** 4K (3840x2160) / Full HD (1920x1080) / social media (1080x1080 or 1080x1920)
- **Number of views:** how many angles/scenes
- **Deadline:** when needed
- **Budget:** affects level of detail (AI concept vs studio render vs photorealistic)
- **Reference images:** any existing renders or photos the client likes

If space or purpose is missing, stop and ask.

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "3D render visualization architectural photography composition", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "Midjourney prompt architecture interior design photorealistic", collection: "dario", limit: 5)
```

### 3. Define camera setup

For each view, specify:

| Parameter | Options | Notes |
|---|---|---|
| **Viewpoint** | Eye-level (1.5m) / Low (0.8m) / Elevated (2.5m) / Bird's eye | Eye-level = most natural/relatable |
| **Lens** | 18mm ultra-wide / 24mm wide / 35mm standard / 50mm detail / 85mm vignette | 24mm is industry standard for interiors |
| **Composition** | 1-point perspective / 2-point perspective / diagonal / symmetrical | 2-point most natural, symmetrical most dramatic |
| **Focus** | Deep (everything sharp) / Shallow (bokeh on background) | Deep for architecture, shallow for details |
| **Aspect ratio** | 16:9 landscape / 3:2 editorial / 1:1 social / 9:16 stories / 4:5 Instagram | Match deliverable platform |
| **Camera position** | Describe exact location in room (e.g., "from doorway looking toward window wall") | Reference floor plan coordinates |

Standard view set for a room:
1. **Hero shot** -- wide angle from best corner, capturing maximum space
2. **Detail shot** -- close-up on key design feature (fireplace, kitchen island, custom joinery)
3. **Lifestyle shot** -- styled with human activity context (book on sofa, coffee on table)
4. **Window view** -- showing interior-exterior relationship

### 4. Define lighting conditions

| Parameter | Options | Mood effect |
|---|---|---|
| **Time of day** | Golden hour (magic hour) / Midday / Blue hour / Night | Golden hour = warmth; Blue hour = drama |
| **Sun direction** | North / South / East / West + angle | Determines shadow direction |
| **Natural light intensity** | Bright / Soft / Overcast / Dramatic (hard shadows) | Overcast = even, flattering |
| **Artificial lighting** | All on / Selective (accent only) / Off | Night renders need all artificial |
| **Mood lighting** | Candles / Fireplace / LED strips / Table lamps only | Adds atmosphere layers |
| **Color temperature** | Warm (2700K) / Neutral (4000K) / Cool (5500K) / Mixed | Warm = residential; neutral = commercial |
| **Exposure** | Bright and airy / Balanced / Moody and dark | Match brand/style direction |

Recommended combinations:
- **Residential presentation:** Golden hour, south-facing sun, warm, bright and airy
- **Luxury/hotel:** Blue hour exterior + warm interior lighting, moody
- **Commercial/office:** Midday, overcast, neutral, balanced
- **Restaurant/bar:** Night, artificial only, warm, moody

### 5. Material specifications

For each visible material, provide:

| Surface | Material | Color/Tone | Finish | Texture detail | Reflection |
|---|---|---|---|---|---|
| Floor | Carvalho europeu | Mel medio | Mate acetinado | Veio natural visivel | Low (5-10%) |
| Walls | Estuco traditional | Branco quente | Mate | Textura irregular subtil | None |
| Ceiling | Gesso pintado | Branco puro | Mate | Liso | None |
| Bancada | Calcario Moleanos | Bege claro | Amaciado | Veio natural | Low (10%) |
| Sofa | Linho | Areia | Texturado | Weave visivel | None |
| Metal accents | Latao | Dourado envelhecido | Escovado | Micro-riscos | Medium (30%) |

### 6. Furniture and object placement

Reference the floor plan and specify:
- **Key pieces:** exact model/reference + position + orientation
- **Scale verification:** ensure furniture dimensions match room proportions
- **Grouping:** conversation area, dining setup, work zone
- **Negative space:** intentional empty areas (essential for minimalist styles)

### 7. Styling and props

The details that make a render feel "lived in":

| Category | Items | Placement |
|---|---|---|
| **Texteis** | Almofadas (3-5, odd numbers), manta no sofa, tapete | Asymmetric, natural draping |
| **Plantas** | 1 grande (1.5m+), 2-3 medias, 1-2 pequenas | Corners, bancadas, prateleiras |
| **Livros** | Stack of 3-5 coffee table books | Horizontal stack + 1 object on top |
| **Arte** | 1 large statement or gallery wall | Eye level (center at 1.5m) |
| **Objectos** | Ceramica, vela, bandeja, vaso | Groups of 3, triangle composition |
| **Cozinha** | Tabua de corte, fruta, garrafa de azeite | Casual, not staged |
| **WC** | Toalhas dobradas, sabonete, planta | Minimal, hotel-style |
| **Exterior visivel** | Vegetacao, cidade, mar | Slightly overexposed for depth |

### 8. Atmosphere and post-processing

| Effect | Level | Notes |
|---|---|---|
| **Depth of field** | Subtle / None / Strong | Subtle for heroes, strong for details |
| **Volumetric light** | Yes / No | Dust particles in sunbeams = warmth |
| **Chromatic aberration** | Subtle / None | Adds photographic realism |
| **Vignette** | Light / None | Draws eye to center |
| **Color grading** | Warm editorial / Clean neutral / Moody dark / Film-like | Match brand aesthetic |
| **Grain** | None / Light film grain | Adds analog warmth |

### 9. Generate AI prompts

**Midjourney -- Hero shot:**
```
Photorealistic interior photograph of [space], [style] design, [key materials list], [color palette], [furniture pieces], [time of day] natural light streaming from [direction] windows, [atmosphere words], styled with [props], [camera specs], architectural photography by [photographer reference], editorial quality --ar [ratio] --v 6.1 --style raw --s 200
```

**Midjourney -- Detail shot:**
```
Close-up interior design detail photograph, [specific feature], [materials in focus], [lighting], shallow depth of field, Canon EOS R5 85mm f/1.8, warm tones, editorial styling --ar 4:5 --v 6.1 --style raw --s 250
```

**Midjourney -- Exterior/facade:**
```
Architectural photograph of [building type] in [location], [facade materials], [time of day] lighting, [landscaping], street-level perspective, [weather], architectural photography, Archdaily quality --ar 16:9 --v 6.1 --style raw --s 200
```

**DALL-E -- Concept visualization:**
```
A photorealistic architectural interior photograph of [detailed space description]. Materials include [list]. The color palette features [description]. Furniture: [key pieces]. Natural [time] light enters from [direction]. Styled with [props]. Shot at eye level with a 24mm lens. Professional interior design photography, editorial quality, soft and warm atmosphere.
```

**Photographer references for Midjourney:**
- Interiors: Stephan Julliard, Ricardo Labougle, Simon Brown, Douglas Friedman
- Architecture: Iwan Baan, Fernando Guerra, Hufton+Crow
- Detail: Ditte Isager, Gentl & Hyers

## Output template

```markdown
---
project: <project name>
date: <YYYY-MM-DD>
type: render-brief
views: <number>
purpose: <client presentation / marketing / social>
---

# Render Brief -- <Project Name>

## Overview
- **Espaco:** <room/area>
- **Estilo:** <style direction> (ref: moodboard de <date>)
- **Finalidade:** <purpose>
- **Formato:** <resolution + aspect ratio>
- **Deadline:** <date>
- **Numero de vistas:** <N>

## Vista 1: Hero Shot -- <description>
### Camera
- Posicao: <description + floor plan ref>
- Lente: <mm>
- Composicao: <type>
- Aspect ratio: <ratio>

### Iluminacao
- Hora: <time of day>
- Direcao sol: <direction>
- Intensidade: <level>
- Iluminacao artificial: <on/off/selective>
- Temperatura: <K>

### Materiais visiveis
| Superficie | Material | Cor | Acabamento |
|---|---|---|---|
| ... | ... | ... | ... |

### Mobiliario
| Peca | Referencia | Posicao | Orientacao |
|---|---|---|---|
| ... | ... | ... | ... |

### Styling
<Props and styling details>

### Atmosfera
<Post-processing and mood notes>

### Prompt Midjourney
```
<ready-to-use prompt>
```

### Prompt DALL-E
```
<ready-to-use prompt>
```

[Repeat for each view]

## Notas para o visualizador
- <Special instructions, problem areas, client preferences>

## Ficheiros de referencia
- [ ] Planta cotada (.dwg / .pdf)
- [ ] Moodboard aprovado
- [ ] Lista de materiais com refs
- [ ] Lista de mobiliario com dimensoes
- [ ] Imagens de referencia

## Proximos passos
- [ ] Enviar brief ao estudio de visualizacao
- [ ] Ou gerar conceitos AI com prompts acima
- [ ] Revisao interna antes de apresentar ao cliente
- [ ] Ajustes pos-feedback
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Project> - Render Brief.md`

## Red flags -- don't do this

- Never brief a render without a floor plan reference -- the visualizer needs spatial context
- Never skip material specifications -- "wood floor" is not enough, specify species, tone, finish
- Never forget to specify time of day -- it changes everything about the image
- Never use ultra-wide lens (< 18mm) for residential -- creates unnatural distortion
- Never place furniture without checking real dimensions against room size
- Never style symmetrically -- real spaces have organic, asymmetric arrangements
- Never render without at least one plant -- it's the #1 indicator of "life" in a render
- Never send a brief without reference images -- words are ambiguous, images are not
- Never use "--v 5" in Midjourney prompts -- always use latest version (6.1+)
- Never mix warm and cool light sources unless intentionally creating contrast

## Interactions

- Requires moodboard from `diva-moodboard` for style/material/color direction
- Pair with `diva-timeline` to schedule render production in project timeline
- Follow up with `dario-proposal` for render costs in client proposal
- Save via `dario-obsidian-save` to vault
