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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

---

### Gate 1 — Camera setup completo (cada view)

- [ ] Viewpoint, lens (mm), composition type e focus mode especificados por view
- [ ] Posição exacta da câmara descrita em linguagem de floor plan ("from doorway looking toward north window wall, 1.5m height")
- [ ] Aspect ratio alinhado com plataforma de destino declarada
- [ ] Mínimo de 2 views, máximo definido pelo número de views acordado com cliente

❌ NOT delivery-ready: `"câmara no canto da sala, lente normal, vista geral"`  
✅ Delivery-ready: `View 1 — Hero shot: eye-level 1.5m, 24mm wide, 2-point perspective, deep focus, 16:9 landscape. Posição: canto SW do living, orientação NE para fachada de vidro. View 2 — Detail: 85mm, shallow focus (f/2.8), 3:2 editorial, bancada de calcário Moleanos em destaque.`

---

### Gate 2 — Lighting com hora do dia + temperatura de cor

- [ ] Time of day explicitamente declarado (não "luz natural bonita")
- [ ] Direcção solar especificada (N/S/E/W + ângulo estimado se golden hour)
- [ ] Temperatura de cor em Kelvin ou no range (2700K / 4000K / 5500K)
- [ ] Modo de exposição (bright & airy / balanced / moody) alinhado com brief de marca/propósito

❌ NOT delivery-ready: `"luz quente ao entardecer, ambiente acolhedor"`  
✅ Delivery-ready: `Golden hour 18h45, sol a SW (225°, altitude 12°), sombras longas para NE. Temperatura interior: 2700K (candeeiro Flos Kelvin + LED strips escondidas) + 5000K entrada de luz natural. Exposição: bright & airy, sem clipping nas janelas.`

---

### Gate 3 — Material spec com finish + reflectividade

- [ ] Cada superfície visível tem: material nomeado + tom/cor + finish + nível de reflectividade (%)
- [ ] Materiais especiais (pedra, madeira) têm nota de veio / textura visível
- [ ] Nenhum material descrito com adjectivos vagos sem referência ("moderno", "claro", "bonito")
- [ ] Metais e vidros têm reflectividade numérica (% ou IOR se para V-Ray/Corona)

❌ NOT delivery-ready: `"chão de madeira clara, paredes brancas, bancada em pedra natural"`  
✅ Delivery-ready: `Chão: carvalho europeu mel médio, mate acetinado, veio natural visível, reflectividade 5-8%. Paredes: estuco tradicional branco quente NCS S 0502-Y, mate, textura irregular subtil, 0%. Bancada: Calcário Moleanos amaciado, bege claro, reflectividade 10-12%, sem polimento especular.`

---

### Gate 4 — Styling e props com quantidade e assimetria

- [ ] Têxteis especificados com número concreto (almofadas: quantidade, cores, tamanhos)
- [ ] Plantas com altura mínima e tipo (não "plantas decorativas")
- [ ] Props de lifestyle contextualizados ao uso do espaço (não genéricos)
- [ ] Indicação de negative space intencional (áreas deliberadamente vazias)

❌ NOT delivery-ready: `"almofadas no sofá, plantas, alguns livros e objectos decorativos"`  
✅ Delivery-ready: `Sofá: 3 almofadas linho areia 50x50cm + 1 almofada accent terracota 40x40cm (disposição assimétrica, 1 inclinada). Manta bouclé branca drapeada no braço esquerdo. Plantas: Ficus Lyrata 1.6m canto NW, Sansevieria média aparador. Props: livro aberto + chávena espresso Jansen+co mesa de apoio direita — sem toque humano visível, mas presença implícita.`

---

### Gate 5 — AI prompts prontos a copiar (se deliverable inclui Midjourney/DALL-E)

- [ ] Prompt inclui: style, renderer simulado, room type, materials, lighting, aspect ratio flag
- [ ] Negative prompt presente com exclusões relevantes (sem pessoas, sem cartazes, sem distorção)
- [ ] Versão do Midjourney declarada (--v 6.1 ou superior para architectural viz)
- [ ] Prompt testado mentalmente: sem ambiguidade que gere resultados aleatórios

❌ NOT delivery-ready: `"living room moderno, luz natural, fotorrealista --v 6"`  
✅ Delivery-ready: `photorealistic interior render, Portuguese apartment living room, European oak floors warm honey tone, white stucco walls, Moleanos limestone countertop, Flos Kelvin pendant, golden hour soft southwest light, 24mm wide angle, 2-point perspective, deep focus, bright and airy exposure, architectural photography, V-Ray quality --ar 16:9 --v 6.1 --style raw --q 2` + negative: `--no people, text, watermark, fisheye distortion, oversaturated, CGI plastic look`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder

- [ ] Nome do projecto/cliente aparece no cabeçalho do brief (ex: "Render Brief — Vivenda Comporta, Quarto Principal")
- [ ] Nenhum campo contém `<nome do cliente>`, `<inserir material>`, `<TBD>` ou equivalente
- [ ] Deadline real declarada (data específica, não "em breve" ou "urgente")
- [ ] Referências a ficheiros reais quando existem (ex: "Floor plan: Piso1_Rev03.dwg", "Moodboard: MB_Sala_v2.pdf")

❌ NOT delivery-ready: `"Projeto: <nome do projeto>, prazo: <inserir deadline>, materiais conforme <moodboard>"`  
✅ Delivery-ready: `Render Brief — Cuidai HQ Lisboa, Sala de Reuniões Principal. Deadline: 14 Fev 2025 (apresentação ao board). Floor plan: CuidaiHQ_Piso2_Rev04.dwg. Moodboard: gerado por diva-moodboard sessão 2024-01-28.`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Render Brief — Vivenda Comporta · Suite Principal (Piso 1)

**Cliente:** Vivenda Comporta  
**Criado por:** DIVA  
**Data:** 2025-02-10  
**Deadline entrega renders:** 2025-02-24 (apresentação ao comprador Herdade do Pinheirinho)  
**Propósito:** Marketing premium + listagem Idealista Luxe + redes sociais @vivenda.comporta  
**Budget render:** Estúdio externo (Corona Renderer) — nível fotorrealista completo  
**Referência floor plan:** VivComp_SuitePrincipal_Rev02.dwg

---

## Views solicitadas (3 vistas)

### View 1 — Hero Shot (wide, living area da suite)
- **Posição:** canto SW do quarto, altura 1.5m, orientação NE para parede de janelas floor-to-ceiling
- **Lens:** 24mm wide angle
- **Composição:** 2-point perspective, eixo ligeiramente descentrado para direita (+15cm)
- **Focus:** deep focus, tudo nítido f/8
- **Aspect ratio:** 16:9 (3840×2160 / 4K)
- **Plataforma:** apresentação PDF + Idealista header

### View 2 — Detail Shot (cabeceira + nicho leitura)
- **Posição:** lateral esquerda da cama, altura 0.9m, orientação E
- **Lens:** 50mm standard
- **Composição:** 1-point perspective, simetria ligeira da cabeceira
- **Focus:** shallow, f/2.8, bokeh suave nas almofadas traseiras
- **Aspect ratio:** 4:5 (1080×1350 — Instagram feed)

### View 3 — Window View (interior-exterior)
- **Posição:** interior, 2m da janela principal, altura 1.5m, orientação S (para dunas)
- **Lens:** 35mm
- **Composição:** diagonal natural guiada pelo caixilho
- **Focus:** deep, equilíbrio interior/exterior exposição (HDR blend)
- **Aspect ratio:** 3:2 editorial (para revista/press)

---

## Lighting

| Parâmetro | Especificação |
|---|---|
| Time of day | Golden hour 18h30, final de Setembro |
| Sol direcção | SW (225°), altitude 8° — sombras longas para NE |
| Luz natural | Soft golden, ligeira névoa costeira (reduz harshness) |
| Temperatura natural | 4200K luz difusa + 2800K raios directos janela |
| Artificial | Candeeiro leitura Flos 265 (2700K) + LED strip escondida cabeceira (2400K dimmado 40%) |
| Exposição | Bright & airy — highlights controladas, sem clipping céu |
| Exterior (View 3) | Céu pós-sol, gradiente rosa-laranja, vegetação dunar em silhueta |

---

## Material Specifications

| Superfície | Material | Cor/Tom | Finish | Textura | Reflectividade |
|---|---|---|---|---|---|
| Pavimento | Calcário Moleanos Bege | NCS S 2010-Y10R | Amaciado | Veio natural subtil | 8% |
| Paredes | Estuco Marmorino | Branco concha OC-17 Benjamin Moore | Polido subtil | Variação manual visível | 3% |
| Tecto | Gesso liso | Branco puro | Mate | Liso | 0% |
| Cabeceira | Linho belga | Areia dourada | Texturado | Weave visível | 0% |
| Cama lençóis | Percal algodão 400TC | Branco puro | Levemente brilhante | Dobras naturais | 4% |
| Pernas cama | Carvalho fumado | Castanho escuro | Mate oleado | Veio horizontal | 2% |
| Candeeiro | Latão | Dourado envelhecido | Escovado | Micro-riscos direccionais | 35% |
| Janelas caixilho | Alumínio termolacado | Antracite RAL 7021 | Mate | Liso | 15% |

---

## Furniture & Placement (ref. VivComp_SuitePrincipal_Rev02.dwg)

- **Cama:** King 180×200cm, centrada parede N, cabeceira a 15cm da parede
- **Mesa cabeceira E:** Fritz Hansen Nap Table, carvalho, x=4.2m y=2.1m planta
- **Mesa cabeceira W:** idem espelhado, x=2.6m y=2.1m
- **Cadeira leitura:** HAY Soft Edge, linho, canto SE junto janela, orientação SW
- **Chaise longue:** B&B Italia, frente janela S, orientação paralela à fachada
- **Negative space intencional:** corredor livre entre porta e cama (1.2m mínimo)

---

## Styling & Props

| Categoria | Items | Detalhe |
|---|---|---|
| Almofadas | 4×50×50cm linho areia + 2×40×40cm areia-terrracota + 2×60cm cilíndricas brancas | Disposição assimétrica, 1 tombada |
| Mantas | 1 manta bouclé branca, drapeada organicamente braço esq chaise | Não dobrada, natural |
| Plantas | Strelitzia 1.4m canto NW; Sansevieria 60cm mesa junto janela | Vasos terracota fosco |
| Props cama | Livro aberto "Comporta" ed. Taschen face down mesa E; chávena espresso vazia | Sem pessoa visível |
| Props janela | Tule linho branco semi-corrido, movimento leve (simular brisa) | Não bloquear vista dunas |
| Artwork | Fotografia P&B Comporta 80×60cm parede W, frame latão escovado | Não centrada — offset 20cm acima centro visual |

---

## AI Concept Prompts (Midjourney — para aprovação rápida antes de render full)

**View 1 Hero:**
```
photorealistic interior render, luxury Portuguese beach house master bedroom, Comporta, 
Moleanos limestone floors warm beige, marmorino plaster walls oyster white, Belgian linen 
headboard sandy gold, smoked oak bed frame, Flos 265 brass reading lamp, golden hour 
southwest light 18:30 September, soft coastal haze, 24mm wide angle 2-point perspective, 
deep focus, bright and airy, Corona Renderer quality, architectural photography --ar 16:9 
--v 6.1 --style raw --q 2
```
*Negative:* `--no people, text, watermark, fisheye distortion, oversaturated, plastic CGI, 
purple shadows, extra furniture`

**View 3 Window:**
```
photorealistic luxury bedroom interior looking through floor-to-ceiling anthracite aluminum 
windows toward Comporta sand dunes, golden hour sunset gradient pink orange sky, dune 
grasses silhouette, interior warm 2700K lamp glow visible, 35mm diagonal composition, 
HDR balanced exposure, architectural photography editorial --ar 3:2 --v 6.1 --style raw
```

---

**Formato entrega estúdio:** TIFF 16-bit + JPEG 95% qualidade  
**Ficheiros de referência:** VivComp_SuitePrincipal_Rev02.dwg · MB_Suite_Comporta_v3.pdf · MaterialBoard_Calcario_Linho_Lato.pdf
```

---

## Output anti-patterns

- Lighting descrito com adjectivos de mood sem parâmetros técnicos: "luz quente e acolhedora" sem hora, direcção, Kelvin ou exposição
- Materiais com "pedra natural clara" ou "madeira escura" — sem nome, tom NCS/RAL, finish ou reflectividade numérica
- Views nomeadas sem posição de câmara: "vista do quarto" não é brief, é intenção
- AI prompts sem `--ar`, `--v` e negative prompt — geram resultados não-arquitectónicos por default
- Styling com "decoração adequada ao estilo" — o artista 3D não é stylist, precisa de lista de props com quantidades
- Brief sem deadline real — "o mais rápido possível" cria conflito de prioridades no estúdio externo
- Número de views deixado aberto ("quantas forem necessárias") sem tecto acordado com cliente
- Furniture placement sem referência ao floor plan — proporcões erradas invalidam o render inteiro
- Misturar especificações de AI concept com especificações de render de estúdio no mesmo campo sem separação clara
- Placeholders `<inserir cor>` ou `<ver moodboard>` enviados para estúdio — causa re-trabalho e custos extra
