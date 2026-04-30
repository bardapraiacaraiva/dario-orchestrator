---
name: diva-render
description: "Generate architectural and interior design visualizations using AI. Creates renders via Gemini (nanobanana MCP), moodboard visuals via AI Designer, and optimized Midjourney prompts. Covers living rooms, bedrooms, bathrooms, kitchens, facades, terraces, offices, restaurants, and Portuguese architecture contexts. Triggers on \"render\", \"gerar imagem\", \"visualizacao\", \"moodboard visual\", \"fotorrealismo\", \"imagem 3D\", \"render interior\", \"render fachada\", \"gerar render\", \"criar visual\"."
argument-hint: "[interior|exterior|moodboard|midjourney] <description>"
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# DIVA Render — AI Visualization for Architecture & Design

Generate production-ready architectural and interior design visualizations using available AI tools.

## Architecture — 3 Rendering Pipelines

### Pipeline 1: Gemini Image Gen (nanobanana MCP)
- **Tool:** `gemini_generate_image` via banana extension
- **Best for:** Quick concept renders, material previews, colour studies
- **Output:** PNG, configurable resolution
- **Cost:** ~$0.04/image (Gemini Imagen 3)
- **Workflow:** Set aspect ratio → Generate with architectural prompt → Save

### Pipeline 2: AI Designer MCP (HTML moodboards)
- **Tool:** `mcp__aidesigner__generate_design`
- **Best for:** Interactive moodboards, material palettes, presentation boards
- **Output:** HTML artifact (viewable in browser, exportable)
- **Workflow:** Generate moodboard HTML → Refine → Extract

### Pipeline 3: Midjourney/DALL-E Prompt Generator
- **Tool:** Text output (user copies to Midjourney/DALL-E)
- **Best for:** Photorealistic renders, hero images, client presentations
- **Output:** Optimized prompt text ready to paste
- **Workflow:** Describe scene → Generate calibrated prompt → User pastes externally

## When to activate

Invoke `/diva-render` when:
- User wants a visual representation of a design concept
- User needs a moodboard with actual images/colours
- User needs a render of a room, facade, or space
- User wants Midjourney prompts for architectural visualization
- User needs material/colour palette visualization

## Workflow

### 1. Determine scene type and pipeline

| Request | Pipeline | Tool |
|---|---|---|
| "gera um render da sala" | Gemini | gemini_generate_image |
| "cria um moodboard visual" | AI Designer | generate_design |
| "preciso de prompts para Midjourney" | Prompt Gen | Text output |
| "render fotorrealista para cliente" | Prompt Gen | Midjourney (best quality) |
| "paleta de materiais visual" | AI Designer | generate_design |
| "quick concept do quarto" | Gemini | gemini_generate_image |

### 2. Gather scene parameters
- **Room type:** sala, quarto, WC, cozinha, fachada, terraco, escritorio, restaurante
- **Style direction:** (from Interior Design Squad) — Warm Minimalism, Mediterranean, etc.
- **Key materials:** pavimento, paredes, mobiliario, iluminacao
- **Lighting:** natural (hora do dia), artificial (warm/neutral)
- **Camera:** eye-level, bird's eye, corner wide, detail close-up
- **Atmosphere:** acolhedor, dramatico, sereno, luminoso, sofisticado

### 3A. Execute — Gemini Pipeline
```
Step 1: Set aspect ratio
  - Interior room: 16:9 (landscape)
  - Facade: 16:9 or 4:3
  - Detail/material: 1:1 (square)
  - Vertical/staircase: 9:16

Step 2: Generate with architectural prompt structure:
  "Interior photograph of a [room type] in [style] style.
   [Key materials and finishes].
   [Furniture and objects].
   [Lighting description].
   [Camera angle and composition].
   Shot by [photographer reference]. 8K, editorial quality."

Step 3: Save to project folder or Obsidian
```

### 3B. Execute — AI Designer Pipeline (Moodboards)
```
Prompt structure for generate_design:
  "Create a professional interior design moodboard for a [room type].
   Style: [direction]. Color palette: [hex codes].
   Materials: [list with images]. Furniture: [references].
   Layout: grid with title, palette strip, 4-6 material/furniture images,
   mood description, and designer reference."
```

### 3C. Execute — Midjourney Prompt Generator

**Prompt Formula for Architecture/Interiors:**
```
[Scene description], [style keywords], [materials], [lighting],
[camera/lens], [photographer reference], [quality keywords]
--ar [ratio] --v 6.1 --s [stylize] --q 2
```

**20 Ready-to-Use Templates:**

**LIVING ROOMS:**
1. `Interior photograph of a minimalist living room in a Lisbon apartment, white plaster walls, light oak herringbone floor, linen sofa in warm beige, brass floor lamp, afternoon sunlight through tall windows, potted olive tree, shot by François Halard, editorial photography, 8K --ar 16:9 --v 6.1 --s 250`

2. `Luxurious living room in Portuguese contemporary style, deep navy accent wall, Calcário Moca stone fireplace, custom walnut credenza, gold accents, velvet emerald armchair, indirect cove lighting, warm atmosphere, shot by Ricardo Labougle, Architectural Digest --ar 16:9 --v 6.1 --s 300`

3. `Warm minimalist living room, travertine coffee table, bouclé cream sofa, jute rug, terracotta vase with dried pampas, sunset light casting warm shadows, Vincent Van Duysen aesthetic, Cereal Magazine photography --ar 16:9 --v 6.1 --s 200`

**KITCHENS:**
4. `Modern kitchen with dark green shaker cabinets, Calacatta marble island, unlacquered brass hardware, white oak open shelving, pendant lights in smoked glass, morning light, styled with ceramics and olive oil bottles, shot by Gentl & Hyers --ar 16:9 --v 6.1 --s 250`

5. `Mediterranean kitchen in Algarve villa, white stucco walls, hand-painted Portuguese azulejo backsplash, terracotta floor tiles, open shelving with artisan ceramics, wooden beams ceiling, natural daylight, rustic luxury, shot by Matthieu Salvaing --ar 16:9 --v 6.1 --s 300`

**BATHROOMS:**
6. `Spa-like bathroom, floor-to-ceiling Pietra di Vicenza limestone, freestanding oval bathtub, brass rainfall shower, recessed niche with candles, indirect LED lighting at 2700K, steam, shot by Pia Ulin, minimal luxury --ar 4:5 --v 6.1 --s 250`

7. `Contemporary bathroom with micro-cement walls in warm grey, walk-in shower with black steel frame, terrazzo floor, round mirror with brass frame, wall-mounted vanity in dark oak, task lighting, shot by Jonas Bjerre-Poulsen --ar 9:16 --v 6.1 --s 200`

**BEDROOMS:**
8. `Serene bedroom in wabi-sabi style, raw plaster walls, linen bedding in natural tones, aged wooden bedside table, single ceramic vase, morning light through sheer curtains, Axel Vervoordt aesthetic, shot by Laziz Hamani --ar 16:9 --v 6.1 --s 300`

9. `Master bedroom in quiet luxury style, upholstered headboard in oatmeal boucle, cashmere throw, walnut nightstands, symmetrical table lamps, curtains floor to ceiling, warm indirect lighting, shot by Simon Watson --ar 16:9 --v 6.1 --s 250`

**FACADES:**
10. `Contemporary Portuguese villa facade, white rendered walls, large format windows with minimal black aluminium frames, flat roof with green terrace, Calcário Moca stone base, mature olive tree in gravel courtyard, blue sky, architectural photography by Fernando Guerra --ar 16:9 --v 6.1 --s 200`

11. `Renovation of a Porto townhouse, traditional azulejo facade restored, new corten steel balcony addition, contrast old and new, street view perspective, late afternoon golden light, shot by Joao Morgado --ar 3:4 --v 6.1 --s 250`

**TERRACES/EXTERIOR:**
12. `Mediterranean rooftop terrace at sunset, white lounge furniture, linen cushions, bougainvillea, infinity view over Lisbon rooftops, Tagus river in background, candle lanterns, shot by Slim Aarons style --ar 16:9 --v 6.1 --s 350`

**OFFICES:**
13. `Biophilic home office, floor to ceiling bookshelf in white oak, large desk in walnut, moss wall panel, Eames lounge chair, pendant light, large window with garden view, calm productive atmosphere, shot by Hiepler Brunier --ar 16:9 --v 6.1 --s 200`

**RESTAURANTS:**
14. `Fine dining restaurant interior, curved banquette in emerald velvet, brass pendant lights, terrazzo floor, arched doorways, warm candlelight, empty table set with white linen, India Mahdavi aesthetic, shot by Adrian Gaut --ar 16:9 --v 6.1 --s 300`

**PORTUGUESE SPECIFIC:**
15. `Alentejo rural house renovation, whitewashed walls, exposed stone accent wall, terracotta tile floor, contemporary furniture against rustic backdrop, fireplace with iron hood, Eduardo Souto de Moura inspired, shot by Nelson Garrido --ar 16:9 --v 6.1 --s 250`

16. `Cascais apartment living room, ocean view through panoramic window, light travertine floor, custom sofa in soft grey, brass console table, large abstract art, Portuguese light flooding the space, CJC Design aesthetic --ar 16:9 --v 6.1 --s 250`

17. `Douro Valley quinta interior, exposed granite walls, dark oak floor, contemporary leather armchair, wool throw, view of vineyards through deep window reveal, warm fire glow, Souto de Moura aesthetic --ar 16:9 --v 6.1 --s 300`

18. `Lisbon Pombalino apartment renovation, original mouldings preserved, herringbone parquet restored, contemporary furniture, tall windows with iron balconies, soft afternoon light, Dirand meets Siza --ar 3:4 --v 6.1 --s 250`

19. `Algarve pool house, white stucco with brise-soleil, infinity pool reflecting blue sky, outdoor shower in natural stone, Mediterranean garden, architectural photography, Tadao Ando influence, shot by Iwan Baan --ar 16:9 --v 6.1 --s 200`

20. `Porto industrial loft conversion, exposed brick and steel, polished concrete floor, open plan kitchen island, mezzanine bedroom, large factory windows, Edison pendants, Patricia Urquiola meets Joanna Gaines --ar 16:9 --v 6.1 --s 250`

### 4. Save and deliver
- Save render/moodboard to Obsidian: `05 - Claude - IA/Outputs/`
- Naming: `YYYY-MM-DD - [Projecto] - Render [Divisao].png`
- Include prompt used for reproducibility

## Photographer References (for prompts)

| Photographer | Known For | Use When |
|---|---|---|
| Fernando Guerra | Portuguese architecture, Siza/Souto de Moura | PT contemporary |
| Joao Morgado | Porto architecture, renovations | PT urban |
| François Halard | Lived-in interiors, warmth | Residential editorial |
| Ricardo Labougle | Latin interiors, colour | Mediterranean luxury |
| Matthieu Salvaing | French/Mediterranean lifestyle | Coastal, villa |
| Slim Aarons | Poolside, golden era luxury | Terraces, outdoor living |
| Iwan Baan | Architectural context, life in buildings | Facades, urban |
| Pia Ulin | Scandinavian interiors, calm | Minimal, Nordic |
| Simon Watson | Warm luxury residential | Bedrooms, living rooms |
| Jonas Bjerre-Poulsen | Norm Architects, tactile minimal | Bathrooms, details |

## Red flags
- Never claim AI renders are real photographs
- Never generate images of real people or copyrighted art
- Always save prompts for client reproducibility
- Gemini has content filters — avoid "luxury brand logos" in prompts
- Midjourney prompts: always include `--v 6.1` for latest model

## Interactions
- After render: `/diva-obsidian-save` to archive
- Before render: `/diva-moodboard` for concept direction
- For materials: `/diva-materials` for exact references
- For full brief: `/diva-render-brief` for comprehensive brief
