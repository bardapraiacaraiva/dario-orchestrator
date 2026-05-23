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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Pipeline correto selecionado para o pedido

- [ ] Identificou tipo de pedido (render rápido / moodboard interativo / prompt externo)
- [ ] Mapeou para pipeline correto (Gemini / AI Designer / Midjourney prompt)
- [ ] Não usou Gemini para pedidos explícitos de fotorrealismo de cliente
- [ ] Não gerou prompt Midjourney quando o utilizador pediu moodboard HTML

❌ NOT delivery-ready: Gerou prompt Midjourney para um pedido de "moodboard visual da sala"
✅ Delivery-ready: Pedido "moodboard visual com paleta" → executou `mcp__aidesigner__generate_design` com grid de materiais, strip de cor #D4A87A / #F2EDE4 / #2C3E2D, e 5 referências de mobiliário

---

### Gate 2 — Parâmetros de cena completos e concretos

- [ ] Room type explícito (sala / quarto / WC / cozinha / fachada / terraço / escritório)
- [ ] Style direction definido (Warm Minimalism / Mediterranean / Contemporary Portuguese / etc.)
- [ ] Materiais-chave listados (pavimento, paredes, mobiliário, iluminação)
- [ ] Camera angle e lighting especificados antes de gerar
- [ ] Atmosphere escolhida (acolhedor / dramático / sereno / luminoso)

❌ NOT delivery-ready: Prompt gerado sem especificar câmara, luz, ou estilo — resultado genérico inutilizável
✅ Delivery-ready: `quarto, Warm Minimalism, pavimento carvalho natural, parede estuque branco, iluminação difusa manhã, câmara eye-level canto largo, atmosfera serena` — todos os 5 campos preenchidos antes de executar

---

### Gate 3 — Qualidade do prompt arquitetural (Midjourney / Gemini)

- [ ] Segue fórmula: [scene] + [style] + [materials] + [lighting] + [camera/lens] + [photographer ref] + [quality tags]
- [ ] Inclui referência de fotógrafo ou publicação real (François Halard / Ricardo Labougle / Matthieu Salvaing / Gentl & Hyers)
- [ ] Parâmetros Midjourney corretos: `--ar`, `--v 6.1`, `--s`, `--q 2`
- [ ] Aspect ratio adequado ao tipo de espaço (16:9 interior / 9:16 vertical / 1:1 detalhe)
- [ ] Prompt em inglês para Midjourney/DALL-E, independentemente do idioma do pedido

❌ NOT delivery-ready: `"uma sala bonita em estilo moderno com luz natural"` — sem materiais, sem referência, sem parâmetros
✅ Delivery-ready: `Interior photograph of a warm minimalist living room, Lisbon apartment, white plaster walls, light oak herringbone floor, bouclé sofa in oat, Flos Arco lamp, afternoon golden light, shot by François Halard, Architectural Digest --ar 16:9 --v 6.1 --s 250 --q 2`

---

### Gate 4 — Moodboard HTML tem estrutura completa

- [ ] Grid contém: título do projeto, palette strip com hex codes, mínimo 4 imagens de material/mobiliário
- [ ] Inclui descrição de mood em texto (2-3 frases)
- [ ] Referência de designer ou projeto de inspiração presente
- [ ] HTML renderizável no browser sem erros (sem tags incompletas)
- [ ] Cores da palette alinhadas com o estilo definido na briefing

❌ NOT delivery-ready: Moodboard com só 2 imagens e sem palette strip — não serve para apresentação a cliente
✅ Delivery-ready: Moodboard Cuidai escritório Lisboa — grid 3×2, palette `#E8E0D5 / #8B7355 / #2D4A3E / #F5F0EB`, 6 referências (cadeira Muuto, secretária carvalho, luminária Artek, planta monstera, parede musgo, pavimento microcimento), mood: "Ambiente clínico-acolhedor que transmite confiança e bem-estar"

---

### Gate 5 — Contexto português arquitetural respeitado

- [ ] Materiais portugueses referenciados quando pertinente (Calcário Moca, Pedra Lioz, azulejo, cortiça, estuque)
- [ ] Tipologia local adequada (apartamento Lisboa, vivenda Algarve, escritório Porto, restaurante Bairro Alto)
- [ ] Não aplicou estética Scandinavian pura em projetos com briefing mediterrânico ou atlântico
- [ ] Iluminação calibrada para luz portuguesa (mais quente, mais intensa que norte europeu)

❌ NOT delivery-ready: Fachada "Vivenda Cascais" renderizada com materiais nórdicos (abeto, pedra cinzenta fria) sem contexto
✅ Delivery-ready: Fachada Vivenda Sintra — Calcário Moca nas ombreiras, reboco branco tradicional, caixilharia alumínio lacado bronze, vegetação mimosa e jacarandá, luz de fim de tarde atlântico, `--s 300`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets

- [ ] Nenhum placeholder do tipo `[CLIENT NAME]`, `[ROOM TYPE]`, `[HEX CODE]` permanece no output final
- [ ] Nome do projeto ou cliente real aparece no título do moodboard ou no save path do render
- [ ] Hex codes são valores reais (#D4A87A), não descrições textuais ("warm beige")
- [ ] Ficheiros salvos com nome descritivo real (ex: `vivenda_sintra_sala_render_v1.png`), não `render_output.png`
- [ ] Parâmetros Midjourney completos e sem campos vazios

❌ NOT delivery-ready: Moodboard com título "Projeto [CLIENTE] — [ESTILO]" e palette "#COLOR1 / #COLOR2"
✅ Delivery-ready: Moodboard título "Atrium Lisboa — Sala de Reuniões Principal", palette `#1C2B39 / #C9A96E / #F0EDE8`, save path `atrium/renders/sala_reunioes_moodboard_v2.html`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output de render deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmed from prior session/memory/cliente data
- 🟡 **assumed** — plausible but needs cliente confirm pre-delivery
- 🟢 **projection** — forecast by design (not verifiable)

Output checklist upfront mostra ao cliente exactamente o que é trust-as-is vs o que precisa validar antes de usar o visual em apresentação.  **Honest transparency > inflated delivery.**

---

❌ NOT delivery-ready:
> "Render gerado: sala de estar, pavimento carvalho, paredes branco gesso, sofá linho bege, iluminação tarde, estilo Warm Minimalism."
> *(reader assume que tudo foi confirmado — materiais, estilo, hora do dia — quando pode ser tudo assumption do modelo)*

✅ Delivery-ready:
> - 🔵 **verified** — Estilo Warm Minimalism (confirmado em sessão de briefing)
> - 🔵 **verified** — Pavimento: carvalho em espinha (especificado pelo cliente, ref. board V2)
> - 🟡 **assumed** — Sofá em linho bege (inferido da paleta; cliente não confirmou tecido/cor exactos)
> - 🟡 **assumed** — Iluminação de tarde/natural (escolhida para atmosfera; hora não especificada pelo cliente)
> - 🟢 **projection** — Qualidade fotorrealista do render final em Midjourney (resultado depende de seed/versão externa; não previsível)
> - 🟢 **projection** — Custo estimado ~$0.04/imagem via Gemini Imagen 3 (baseado em pricing actual; sujeito a alteração)

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — materiais, acabamentos e atmosfera validados pelo cliente antes de gerar render final
- [ ] All 🔵 citations added — referencias a briefing, mood board ou sessão anterior documentadas no projecto
- [ ] All 🟢 projections labeled as such ao cliente — expectativas de output externo (Midjourney/DALL-E) e custos comunicados como estimativa, não garantia

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## Render Package — Lisbon Dog Care | Recepção + Espaço Grooming

**Pedido:** Moodboard visual + 2 prompts Midjourney para apresentação a investidor

---

### Pipeline executado

| Entrega | Pipeline | Tool |
|---|---|---|
| Moodboard interativo recepção | AI Designer | generate_design |
| Prompt render fotorrealista recepção | Midjourney Gen | Text output |
| Prompt render espaço grooming | Midjourney Gen | Text output |

---

### Parâmetros de cena recolhidos

- **Tipologia:** Pet care boutique, Lisboa (Príncipe Real)
- **Estilo:** Warm Contemporary — materiais naturais, tom premium sem exagero
- **Palette aprovada:** #F5EFE6 (fundo creme) / #8B6F47 (carvalho mel) / #2E5741 (verde musgo) / #D4C5B0 (linho)
- **Materiais:** pavimento microcimento bege, balcão em carvalho natural, parede estuque texturado, plantas vivas, sinalética em latão
- **Luz:** natural (janelas viradas a sul, Lisboa) + spots embutidos warm 2700K
- **Câmara:** eye-level, ângulo largo 24mm, composição com balcão em primeiro plano

---

### Output 1 — Moodboard HTML (AI Designer)

Prompt enviado ao `mcp__aidesigner__generate_design`:

> "Create a professional interior design moodboard for a boutique pet care reception in Lisbon.
> Style: Warm Contemporary. Color palette: #F5EFE6, #8B6F47, #2E5741, #D4C5B0.
> Materials: beige microcement floor, natural oak reception desk, textured plaster walls,
> live moss wall panel, brass lettering signage.
> Furniture: Muuto Connect chair in oat bouclé, Ferm Living Plant Box in black steel.
> Layout: grid with title 'Lisbon Dog Care — Recepção', horizontal palette strip,
> 6 material/furniture reference images, mood description, and reference to Norm Architects aesthetic."

**Resultado:** HTML salvo em `lisbon_dog_care/renders/recepcao_moodboard_v1.html`

---

### Output 2 — Prompt Midjourney | Recepção

```
Interior photograph of a boutique pet care reception in Lisbon Príncipe Real,
warm contemporary style, beige microcement floor, natural oak reception desk,
textured white plaster walls, live moss wall panel, brass 'Lisbon Dog Care' signage,
Muuto bouclé chairs in oat, large south-facing windows with afternoon Lisbon light,
warm 2700K spotlights, lush indoor plants, serene and premium atmosphere,
shot by Nicole Franzen, Kinfolk Magazine aesthetic, 8K editorial photography
--ar 16:9 --v 6.1 --s 280 --q 2
```

**Aspect ratio:** 16:9 (landscape — recepção horizontal)
**Stylize:** 280 (premium sem hiper-estilização)

---

### Output 3 — Prompt Midjourney | Sala Grooming

```
Interior photograph of a professional pet grooming studio, warm and clinical aesthetic,
white zellige tile walls with oak trim, stainless steel grooming table with leather strap,
wall-mounted brass shower head, warm pendant lighting in smoked glass,
open shelving with glass apothecary jars and dog grooming tools,
potted ficus in terracotta pot, soft natural daylight from skylight,
Lisbon pet boutique, shot by Gentl & Hyers, Architectural Digest
--ar 16:9 --v 6.1 --s 300 --q 2
```

---

### Delivery checklist

- [x] Cliente: Lisbon Dog Care — nome real, sem placeholders
- [x] Hex codes reais em todos os outputs (#F5EFE6, #8B6F47, #2E5741, #D4C5B0)
- [x] Fotógrafos de referência reais (Nicole Franzen, Gentl & Hyers)
- [x] Parâmetros Midjourney completos (`--ar 16:9 --v 6.1 --s 280/300 --q 2`)
- [x] Ficheiro HTML nomeado: `recepcao_moodboard_v1.html`
- [x] Materiais portugueses contextualizados (Lisboa, Príncipe Real, estuque, latão)
- [x] 3 pipelines corretos para 3 pedidos distintos
```

---

## Output anti-patterns

- Gerar prompt Midjourney quando o pedido era explicitamente "moodboard visual" — pipelines não são intercambiáveis
- Deixar `[ROOM TYPE]`, `[CLIENT]`, `[HEX CODE]` ou qualquer angle-bracket no output final entregue
- Usar "warm beige" ou "dark green" em vez de hex codes reais (#C9A96E, #2E5741) na palette do moodboard
- Prompt sem referência de fotógrafo ou publicação — output Midjourney perde 30-40% de qualidade direcional
- Aspect ratio errado: interior horizontal em 9:16, fachada em 1:1 — força regenar sem necessidade
- Aplicar estética escandinava (abeto, pedra cinzenta fria, luz flat nórdica) em projetos com briefing mediterrânico ou atlântico português
- Omitir `--q 2` e `--s [value]` nos prompts Midjourney — entregou prompt incompleto que o cliente não consegue usar diretamente
- Gerar moodboard HTML com menos de 4 referências visuais — não serve para apresentação a cliente ou investidor
- Salvar ficheiro como `render_output.png` ou `moodboard.html` sem nome de projeto — impossível de gerir em contexto multi-cliente
- Descrever materiais em português nos prompts Midjourney/DALL-E — o modelo performa significativamente pior fora de inglês
