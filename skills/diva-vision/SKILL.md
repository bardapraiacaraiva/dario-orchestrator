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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Modo correcto activado e declarado

- [ ] Output abre identificando explicitamente qual dos 7 modos foi activado (ex: "**Mode 4: Construction Progress**")
- [ ] Trigger da activação está alinhado com o input do utilizador (foto de obra ≠ Mode 1)
- [ ] Se imagem é ambígua, modo escolhido está justificado com evidências visuais concretas
- [ ] Não activaste Mode 7 (geração SVG) quando utilizador pediu apenas diagnóstico

❌ NOT delivery-ready: "Analisei a imagem e vejo um espaço com potencial..."
✅ Delivery-ready: "**Mode 1 — Space Analysis** activado. Foto mostra sala de estar ~25m², pé-direito estimado 2.70m, pavimento vinílico em estado razoável, patologia de humidade visível no canto NE."

---

### Gate 2 — Dimensões estimadas com referência visual explícita

- [ ] Toda estimativa dimensional cita o elemento de referência usado (porta, bancada, sanita, cama)
- [ ] Dimensões estão em metros com uma casa decimal (ex: 3.8m × 5.2m, não "uns 4 metros")
- [ ] Área total calculada está presente quando aplicável (L × C = XX m²)
- [ ] Incerteza alta está sinalizada com "±" ou nota "estimativa visual — confirmar com medição"

❌ NOT delivery-ready: "A sala parece ter uns 20 metros quadrados..."
✅ Delivery-ready: "Largura estimada 3.8m (referência: porta standard 0.90m visível à direita × escala proporcional). Comprimento 6.0m. Área estimada: **22.8m²** ±15% — confirmar com fita."

---

### Gate 3 — Patologias e issues com localização na imagem

- [ ] Cada patologia identificada tem localização precisa (canto SE, parede Norte, tecto junto à janela)
- [ ] Severidade classificada: Crítico / Moderado / Estético
- [ ] Causa provável indicada (infiltração, condensação, assentamento, uso)
- [ ] Action item sugerido por cada issue (ticket PlanRadar se obra, intervenção se espaço)

❌ NOT delivery-ready: "Existem algumas manchas de humidade nas paredes."
✅ Delivery-ready: "**Patologia 1 — Humidade** [Canto NE, parede exterior, ~0.8m × 0.6m] Severidade: **Moderado**. Causa provável: ponte térmica ou infiltração pela caixilharia. Acção: inspeção impermeabilização exterior antes de acabamentos. → Ticket PlanRadar sugerido: 'Humidade canto NE — verificar antes de estuque.'"

---

### Gate 4 — Entregáveis do modo completos e sem omissões

- [ ] Todos os bullets da secção "Deliver" do modo activado estão presentes no output
- [ ] Se Mode 7 foi activado: ficheiro HTML/SVG gerado (não apenas descrito)
- [ ] Se Mode 5 (materiais): pelo menos 2 fornecedores PT com preço por m² ou unidade
- [ ] Se Mode 3 (planta): tabela areas vs RGEU presente com ✅/❌ por divisão

❌ NOT delivery-ready: "Aqui estão algumas sugestões de design para o espaço..."
✅ Delivery-ready: "**Tabela RGEU — Apartamento Rua do Ouro 47, Lisboa:** | Divisão | Área est. | RGEU mínimo | Status | | Quarto 1 | 11.2m² | 10.5m² | ✅ | | WC | 3.1m² | 3.5m² | ❌ |"

---

### Gate 5 — Potencial de design com 3 direcções distintas e orçamento

- [ ] 3 direcções de intervenção nomeadas com conceito claro (não "moderna", "clássica", "minimalista" genérico)
- [ ] Cada direcção tem estimativa orçamental em €/m² ou total (economico / recomendado / premium)
- [ ] Squad member recomendado está nomeado (arquiteto/designer específico se disponível)
- [ ] Quick wins separados de intervenção estrutural (o que resolve em <1 semana vs obra)

❌ NOT delivery-ready: "O espaço tem potencial para uma remodelação moderna ou clássica, dependendo do gosto."
✅ Delivery-ready: "**Direcção A — Loft Industrial** (demolir tecto falso, expor laje, pavimento microcimento) ~€18.000–22.000 total. **Direcção B — Escandinavo Quente** (manter estrutura, madeira clara, iluminação embutida) ~€9.000–12.000. **Direcção C — Quick Win Sem Obra** (pintura, iluminação, mobiliário) ~€2.500–4.000. Squad recomendado: **Sofia Andrade** (interiores residencial mid-range)."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder

- [ ] Nenhum `[PROJECTO]`, `[CLIENTE]`, `[ENDEREÇO]`, `[DATA]` visível no output final
- [ ] Nome do projecto ou morada usada no título do plano/análise
- [ ] Se SVG/HTML gerado: `<title>` e cabeçalho têm nome real
- [ ] Datas de obra (se Mode 4) são datas reais ou "data não fornecida — inserir"

❌ NOT delivery-ready: "Planta — [Projecto] | Cliente: [Nome do Cliente]"
✅ Delivery-ready: "Planta — Apartamento T3, Rua Castilho 112, 3º Esq., Lisboa | Análise: 14 Jun 2025"

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output de análise visual deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado por referência técnica conhecida (RGEU, dimensões standard, materiais identificados com certeza)
- 🟡 **assumed** — estimativa plausível a partir de pistas visuais, requer confirmação do cliente antes de usar em projecto
- 🟢 **projection** — previsão de potencial ou custo gerada por design (não verificável sem medição/orçamento real)

Output checklist upfront mostra ao cliente exactamente o que é trust-as-is vs o que precisa validar antes de avançar. **Honest transparency > inflated delivery.**

---

❌ NOT delivery-ready:
> "Sala com ~18m², teto a 2.60m, pavimento em carvalho maciço, intervenção estimada €8.000–12.000."
*(reader assume que tudo foi medido/confirmado — nada está labelado)*

✅ Delivery-ready:
> - 🔵 **verified** — Porta de entrada: largura standard 0.90m (referência RGEU usada para escala)
> - 🟡 **assumed** — Área estimada: ~18m² (derivada de proporções visuais; confirmar com fita/laser antes de projecto)
> - 🟡 **assumed** — Pavimento identificado como soalho de madeira maciça (possível carvalho; confirmar espécie e estado estrutural in situ)
> - 🟡 **assumed** — Tecto estimado a 2.60m (proporcionalidade com mobiliário visível; medir antes de orçamentar pladur/iluminação)
> - 🟢 **projection** — Potencial de intervenção: €8.000–12.000 (estimativa fase conceptual ±30%; valida com empreiteiro antes de compromisso)

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — dimensões medidas in situ, materiais validados, patologias inspeccionadas fisicamente
- [ ] All 🔵 citations added — referência RGEU, norma ou dimensão standard usada explicitada no output
- [ ] All 🟢 projections labeled as such ao cliente — estimativas orçamentais e potencial de design comunicados com margem de erro clara (ex: "±30%, fase conceptual")

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## 🔍 DIVA Vision — Mode 1: Space Analysis
**Foto recebida:** Cozinha Cuidai HQ, Rua Filipe Folque 12, Lisboa — 12 Jun 2025

---

### Identificação do Espaço
- **Tipo:** Cozinha de apoio / copa (uso escritório)
- **Dimensões estimadas:** 2.8m × 3.6m = **10.1m²** ±12%
  - Referência: frigorífico standard 0.60m profundidade × escala proporcional
- **Pé-direito estimado:** 2.50m (proporção janela/parede)
- **Orientação luz natural:** Janela Oeste (~0.90m × 1.10m) — luz de tarde, sem luz matinal direta

---

### Estado e Materiais

| Elemento | Material identificado | Estado |
|---|---|---|
| Pavimento | Vinílico em régua, imitação madeira clara | Razoável — 2 juntas abertas junto ao rodapé |
| Paredes | Tinta lavável branco fosco | Mau — marcas de gordura zona fogão, descascamento junto ao tecto |
| Tecto | Tecto falso gesso cartonado | Bom |
| Bancada | Estratificado bege | Razoável — canto junto ao lava-loiça com início de inchamento |
| Frentes | MDF lacado branco mate | Razoável — 1 dobradiça partida (porta inferior direita) |

---

### Patologias Identificadas

**P1 — Inchamento bancada [canto NE, junto ao lava-loiça]**
Severidade: **Moderado** | Causa: infiltração água por vedante degradado
Acção imediata: substituir vedante silicone perimetral lava-loiça (DIY, <€15, 2h)

**P2 — Descascamento tinta [parede Norte, zona superior, ~40cm faixa]**
Severidade: **Estético** | Causa provável: condensação vapor sem extracção adequada
Acção: instalar extractor (ausente na foto) + repintura zona após limpeza fungicida

**P3 — Dobradiça partida [frente inferior direita]**
Severidade: **Estético** | Acção: substituição dobradiça Blum €4 — peça idêntica visível nas outras portas

---

### Potencial de Design — 3 Direcções

**Direcção A — Renovação Express (sem obra)**
Frentes lacadas cinza antracite, puxadores barra latão, bancada laminam pedra, iluminação LED fita sob armários
Estimativa: **€2.800–3.500** | Prazo: 5 dias úteis
Squad: João Ferreira (marceneiro parceiro, disponível Julho)

**Direcção B — Remodelação Intermédia**
Nova bancada Dekton Sirius 2cm, lava-loiça undermount, frentes PVC hidrofugado, azulejo metro branco brilhante, extractor encastrado
Estimativa: **€7.500–9.000** | Prazo: 3 semanas
Squad: Sofia Andrade (projecto) + Obra Cuidai parceiro

**Direcção C — Substituição Total**
Layout optimizado (bancada em L), electrodomésticos Bosch Serie 4 encastrados, pavimento microcimento contínuo, iluminação Flos
Estimativa: **€18.000–22.000** | Prazo: 6–8 semanas

---

### Quick Wins (esta semana, sem obra)
1. ✅ Substituir vedante lava-loiça — €15, evita dano progressivo bancada
2. ✅ Reparar dobradiça — €4 + 20min
3. ✅ Instalar extractor portátil provisório — €45 Leroy Merlin, elimina condensação imediata
4. ✅ Limpeza gordura parede com Mr. Muscle cozinha — repintura local com tinta restante

---

*Análise DIVA Vision — Cuidai | 12 Jun 2025 | Foto: Copa RFF12 | Confiança estimativas: Média (foto única, sem medições)*
```

---

## Output anti-patterns

- Activar Mode 7 (gerar SVG) e entregar apenas descrição textual da planta — "ficaria assim: sala à esquerda, quarto à direita..."
- Dimensões sem referência visual — "a sala tem aproximadamente 20m²" sem citar o elemento de escala usado
- Patologias sem localização — "há humidade" sem indicar parede, canto, área afectada ou severidade
- Materiais identificados sem fornecedor PT nem preço — identificação académica sem utilidade comercial
- 3 direcções de design com nomes genéricos e sem orçamento — "moderno", "clássico", "rústico" como entregável
- Planta gerada com `[PROJECTO]` ou `[CLIENTE]` não substituídos no título HTML/SVG
- Mode 4 (obra) sem verificação safety e sem sugestão de ticket PlanRadar quando issue encontrado
- Incerteza dimensional mascarada como precisão — dar "3.80m × 5.20m" sem ±% quando é estimativa visual de foto
- Análise sem squad member recomendado — diagnóstico sem próximo passo humano atribuído
- Before/after comparison sem categorização das mudanças — comentário impressionista em vez de tabela estruturada por categoria
