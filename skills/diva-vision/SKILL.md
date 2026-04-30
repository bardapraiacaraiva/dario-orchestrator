---
name: diva-vision
description: "Multimodal space analysis — analyzes photos of rooms, construction sites, floor plans, materials, and sketches. Extracts spatial data, identifies patologias, evaluates design potential, checks construction progress, and can generate 2D floor plans from images. Triggers on \"analisa esta foto\", \"analisa este espaco\", \"o que ves nesta imagem\", \"foto da obra\", \"foto do espaco\", \"analise visual\", \"imagem\", \"planta desta foto\", \"antes depois\", \"identifica material\"."
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# DIVA Vision — Multimodal Space Analysis

Analyze photos, sketches, and floor plans using Claude's vision capabilities. Extract spatial data, identify issues, evaluate potential, and generate 2D plans.

## When to activate

Invoke `/diva-vision` when:
- User shares a photo of a room, facade, or construction site
- User uploads a floor plan scan, sketch, or CAD screenshot
- User shares a material sample photo for identification
- User wants before/after comparison
- User wants to generate a 2D plan from a photo
- User shares a render for critique

## 7 Analysis Modes

### Mode 1: SPACE ANALYSIS (foto de divisao)
When user shares a photo of an existing room/space:

**Extract:**
- Room type (sala, quarto, WC, cozinha, corredor)
- Estimated dimensions (from visual cues — doors 2.10m, janelas, mobiliario standard)
- Ceiling height (from proportions)
- Natural light: orientation estimate, window size, quality
- Current materials: pavimento, paredes, tecto (identify type)
- Current furniture and layout
- Condition: bom / razoavel / mau / ruina
- Patologias visiveis: humidade, fissuras, bolor, descascamento

**Deliver:**
- Diagnostico do espaco (strengths + weaknesses)
- Potencial de design (3 direccoes possiveis)
- Estimativa orcamental de intervencao
- Designer/arquitecto recomendado (do squad)
- Quick wins visiveis

### Mode 2: FLOOR PLAN EXTRACTION (foto → planta)
When user shares a photo of a space and wants a floor plan:

**Process:**
1. Identify walls, doors, windows from the photo
2. Estimate dimensions using visual references:
   - Standard door: 0.80-0.90m largura, 2.10m altura
   - Standard janela: 1.00-1.40m largura
   - Bancada cozinha: 0.60m profundidade
   - Sanita: 0.40x0.70m
   - Banheira: 0.70x1.70m
   - Cama casal: 1.60x2.00m
3. Generate SVG/HTML floor plan (see Mode 7)

### Mode 3: PLAN ANALYSIS (planta existente)
When user shares a scan/photo of an existing floor plan:

**Extract:**
- Room count and types
- Areas por divisao (from scale or cotas visiveis)
- Circulation flow analysis
- RGEU compliance check (areas minimas)
- Natural light access per room
- Structural walls vs divisorias (if identifiable)

**Deliver:**
- Tabela de areas vs RGEU minimos
- Pontos fortes do layout
- Problemas identificados (circulacao, luz, proporcoes)
- 2-3 sugestoes de optimizacao

### Mode 4: CONSTRUCTION PROGRESS (foto de obra)
When user shares construction site photos:

**Evaluate:**
- Phase identification (demolicao/estrutura/alvenaria/MEP/acabamentos)
- Quality assessment (prumo, planeza, alinhamento, limpeza)
- Safety check (EPI visivel, guarda-corpo, estaleiro)
- Issues identification (fissuras, desalinhamentos, humidades)
- Progress vs expected timeline

**Deliver:**
- Fase actual identificada
- Issues encontrados (com localizacao na foto)
- Recomendacoes imediatas
- Ticket PlanRadar sugerido (se issue encontrado)

### Mode 5: MATERIAL IDENTIFICATION (foto de material)
When user shares a photo of a material or finish:

**Identify:**
- Material type (ceramica, pedra, madeira, microcimento, metal, textil)
- Possible references (marca, coleccao — se reconhecivel)
- Acabamento (matt, polished, structured, aged)
- Condicao (novo, usado, danificado)
- Formato/dimensoes estimados

**Deliver:**
- Identificacao do material
- Fornecedores PT similares com precos
- Alternativas por tier (economico/recomendado/premium)
- Compatibilidade (piso radiante, zonas humidas, exterior)

### Mode 6: BEFORE/AFTER COMPARISON
When user shares 2 photos (antes e depois):

**Analyze:**
- Mudancas identificadas por categoria (layout, materiais, iluminacao, mobiliario)
- Qualidade de execucao
- Valorizacao estimada
- O que ficou bem vs o que poderia melhorar

### Mode 7: 2D FLOOR PLAN GENERATION (foto/descricao → SVG)
Generate a humanized 2D floor plan as SVG/HTML:

**Input:** Photo of space, rough sketch, or verbal description
**Output:** Interactive HTML file with SVG floor plan

**Floor Plan SVG Specifications:**
- Scale: 1px = 1cm (or dynamic based on viewport)
- Walls: 15cm exterior (dark grey #333), 10cm interior (grey #666)
- Doors: Arc symbol (90 degree), direction indicated
- Windows: Double line with gap, light blue fill
- Room labels: Name + area in m2 (centered, clean font)
- Dimensions: Arrow lines with measurements in meters
- Furniture: Simple shapes (optional layer)
- Color coding by zone:
  - Social (sala, jantar): warm beige #F5E6D0
  - Privado (quartos): soft blue #E0EAF5
  - Servicos (WC, cozinha, lavandaria): light green #E0F5E6
  - Circulacao (hall, corredor): light grey #F0F0F0
- North arrow indicator
- Scale bar
- RGEU compliance badges (green check / red X per room)

**HTML Template Structure:**
```html
<!DOCTYPE html>
<html>
<head>
  <title>Planta — [Projecto]</title>
  <style>
    body { font-family: 'Segoe UI', sans-serif; background: #fafafa; margin: 40px; }
    .plan-container { background: white; border: 1px solid #ddd; padding: 40px; max-width: 1200px; margin: 0 auto; }
    .plan-title { font-size: 24px; font-weight: 300; margin-bottom: 8px; }
    .plan-subtitle { color: #888; font-size: 14px; margin-bottom: 30px; }
    svg text { font-family: 'Segoe UI', sans-serif; }
    .wall { stroke: #333; stroke-width: 3; fill: none; }
    .wall-interior { stroke: #666; stroke-width: 2; fill: none; }
    .window { stroke: #4A90D9; stroke-width: 2; fill: #E8F4FD; }
    .door-arc { stroke: #999; stroke-width: 1; fill: none; stroke-dasharray: 4,2; }
    .door-leaf { stroke: #333; stroke-width: 2; fill: none; }
    .room-label { font-size: 14px; fill: #333; text-anchor: middle; font-weight: 600; }
    .room-area { font-size: 11px; fill: #888; text-anchor: middle; }
    .dimension { font-size: 9px; fill: #999; text-anchor: middle; }
    .dim-line { stroke: #ccc; stroke-width: 0.5; }
    .dim-arrow { stroke: #ccc; stroke-width: 0.5; fill: #ccc; }
    .furniture { fill: #e8e8e8; stroke: #ccc; stroke-width: 0.5; }
    .zone-social { fill: #F5E6D0; opacity: 0.3; }
    .zone-private { fill: #E0EAF5; opacity: 0.3; }
    .zone-service { fill: #E0F5E6; opacity: 0.3; }
    .zone-circulation { fill: #F0F0F0; opacity: 0.3; }
    .north-arrow { fill: #333; }
    .legend { font-size: 11px; fill: #666; }
    .rgeu-ok { fill: #4CAF50; font-size: 10px; }
    .rgeu-fail { fill: #F44336; font-size: 10px; }
    .info-table { border-collapse: collapse; margin-top: 30px; width: 100%; }
    .info-table th, .info-table td { border: 1px solid #eee; padding: 8px 12px; text-align: left; font-size: 13px; }
    .info-table th { background: #f5f5f5; font-weight: 600; }
  </style>
</head>
<body>
  <div class="plan-container">
    <div class="plan-title">Planta — [Projecto Name]</div>
    <div class="plan-subtitle">[Morada] | Escala 1:100 | Area total: XX m2</div>
    
    <svg viewBox="0 0 [width] [height]" xmlns="http://www.w3.org/2000/svg">
      <!-- Zone fills (background) -->
      <!-- Walls (exterior + interior) -->
      <!-- Windows -->
      <!-- Doors (arc + leaf) -->
      <!-- Room labels + areas -->
      <!-- Dimensions -->
      <!-- Furniture (optional layer) -->
      <!-- North arrow -->
      <!-- Scale bar -->
      <!-- RGEU compliance badges -->
    </svg>

    <!-- Areas table -->
    <table class="info-table">
      <tr><th>Divisao</th><th>Area (m2)</th><th>RGEU Min</th><th>Status</th></tr>
      <!-- rows -->
    </table>
  </div>
</body>
</html>
```

**Furniture Library (simple SVG shapes):**
- Cama casal: rect 160x200, headboard line
- Cama solteiro: rect 90x200
- Sofa 3 lugares: rect 220x90, rounded corners
- Mesa jantar: rect 160x90 or circle r=60
- Mesa escritorio: rect 140x70
- Sanita: ellipse 40x55 + cistern rect
- Lavatorio: semicircle r=25
- Banheira: rect 70x170, rounded
- Base duche: rect 80x80 or 90x90
- Bancada cozinha: rect length x 60, counter indication
- Frigorifico: rect 60x70
- Fogao: rect 60x60, 4 circles
- Roupeiro: rect depth x length, hatched

## Workflow

1. **Receive image** — user provides photo, sketch, or plan
2. **Identify mode** — which of the 7 modes applies
3. **Analyze** — extract all relevant data using vision
4. **RAG consult** — `search_kb("materials suppliers portugal", collection: "diva")`
5. **Generate output** — analysis report + SVG plan if requested
6. **Save** — HTML file to project folder, report to Obsidian

## Output Files
- Floor plan: `[projecto]-planta.html` (openable in any browser)
- Analysis: `YYYY-MM-DD - [Projecto] - Analise Visual.md` → Obsidian
- Photos: reference in `10 - Attachments/Fotos Obra/`

## Red flags
- Never state exact dimensions from photos — always "estimated ~X.Xm"
- Never diagnose structural issues from photos alone — recommend engineer
- Never guarantee RGEU compliance from visual analysis — needs measurement
- Always include disclaimer: "Dimensoes estimadas visualmente. Confirmar com medicao in-situ."
- SVG plans are conceptuais — nao substituem projecto de arquitectura

## Interactions
- After analysis: `/diva-floor-plan` for layout optimization
- After material ID: `/diva-materials` for specification
- After construction check: `/diva-inspection` + `/diva-planradar`
- For render from plan: `/diva-render` with Midjourney prompts
