---
name: diva-floor-plan
description: Floor plan analysis and optimization for architecture and interior design projects. Analyzes circulation flow, functional zones, RGEU dimensional compliance, natural light, ventilation, and privacy gradient. Proposes 2-3 layout alternatives with pros/cons. Triggers on "planta", "floor plan", "layout", "circulacao", "optimizar espaco", "distribuicao".
license: MIT
---

# DIVA Skill — Floor Plan Analysis & Optimization

Analyzes existing floor plans and proposes optimized layout alternatives. Evaluates circulation flow, functional zoning, dimensional compliance with Portuguese regulations (RGEU), natural light distribution, ventilation paths, and privacy gradients. Produces 2-3 layout alternatives with comparative analysis.

## When to activate

Invoke `/diva-floor-plan` (or trigger automatically) when:
- User shares a floor plan (image, description, or dimensions)
- User asks to optimize a layout or redistribute spaces
- User wants to evaluate if a space works for their program
- User is deciding between layout options
- User mentions circulation problems, wasted space, or poor flow
- After `diva-briefing` defines the functional program

Do NOT use when:
- No floor plan or dimensional information is available (do `diva-diagnose` first)
- User only needs material or budget information
- The project is purely exterior/facade work

## Workflow

### 1. Capture existing plan data
From image, description, or measurements:
- **External dimensions:** total footprint
- **Structural elements:** load-bearing walls (mark as IMMOVABLE), columns, shafts
- **Fixed points:** risers (prumadas), wet areas stack, stairwell, elevator
- **Window positions:** size, orientation (N/S/E/W), height from floor
- **Door positions:** entry door(s), interior doors
- **Ceiling height:** uniform or variable
- **Current room layout:** with approximate dimensions

If a floor plan image is provided, extract dimensions. If dimensions are missing, ask for key measurements.

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "RGEU minimum areas rooms apartment residential", limit: 5)
mcp__dario-rag__search_kb(query: "floor plan circulation flow functional zoning", limit: 5)
mcp__dario-rag__search_kb(query: "natural light ventilation apartment layout", limit: 5)
```

### 3. RGEU dimensional compliance audit
Check every space against Portuguese minimums:

**Minimum areas (RGEU Art. 65-67):**
| Space | Min area (m2) | Min dimension (m) |
|---|---|---|
| Sala (T0-T1) | 10 | 2.10 |
| Sala (T2+) | 12 | 2.70 |
| Quarto casal | 10.50 | 2.60 |
| Quarto individual | 6.50 | 2.10 |
| Cozinha | 6 | 1.70 |
| WC | 3.50 | 1.30 |
| Despensa | - | 0.80 |
| Corredor | - | 0.90 (1.10 recommended) |

**Minimum ceiling height:** 2.40m (habitavel), 2.20m (WC, arrumos, garagem)

**Natural light:** each habitable room must have window area >= 1/8 of floor area

**Ventilation:** cross-ventilation path, kitchen and WC must have extraction

Flag every non-compliance as CRITICO (if new work) or EXISTENTE (if pre-existing and grandfathered).

### 4. Circulation flow analysis
- **Entry sequence:** from front door, what do you see/access first
- **Public-private gradient:** entry > social zones > private zones (ideal flow)
- **Kitchen triangle:** sink-stove-fridge distances (ideal: 3.6-7.9m perimeter)
- **Corridor efficiency:** percentage of total area used for circulation (target: <15%)
- **Dead-end spaces:** rooms accessible only through other rooms (avoid for bedrooms)
- **Service flow:** laundry path, garbage path, grocery unloading
- **Emergency egress:** code-compliant exit routes

### 5. Functional zone mapping
Divide the plan into zones:
- **Social zone:** sala, dining, kitchen (ideally connected, near entry)
- **Private zone:** bedrooms, suites (ideally away from entry, quieter side)
- **Service zone:** laundry, storage, technical (can be windowless)
- **Wet zone:** bathrooms, kitchen (stack vertically for plumbing efficiency)
- **Transition zone:** corridors, hall (minimize but don't eliminate)

Evaluate adjacency quality:
- Kitchen near dining (essential)
- Suite bathroom accessible from bedroom (essential)
- Guest WC accessible from social zone without crossing private zone
- Laundry near bedrooms OR kitchen (cultural: PT traditionally near kitchen)

### 6. Natural light and orientation analysis
- **South-facing rooms:** prioritize living areas (maximum winter sun)
- **North-facing rooms:** suitable for offices, storage, service areas
- **East-facing rooms:** good for bedrooms (morning light)
- **West-facing rooms:** afternoon sun, can overheat in summer (consider shading)
- **Light penetration depth:** max ~6m from window without borrowed light
- **Borrowed light strategies:** interior windows, glass partitions, clerestories
- **Light well/saguao:** if present, maximize its use

### 7. Generate layout alternatives
Produce 2-3 options:

**Option A — Conservative:**
- Minimal structural changes
- Respects existing plumbing positions
- Lower cost, faster execution
- Best for: budget constraints, rental properties

**Option B — Optimized:**
- Strategic wall removals (non-structural only)
- May relocate some wet areas within reason
- Better flow and space utilization
- Best for: medium renovations, most clients

**Option C — Transformative:**
- Maximum structural intervention (within regulatory limits)
- Possible plumbing relocation, new openings in structural walls (with engineering)
- Completely reimagined layout
- Best for: full gut renovations, high budgets

For each option provide:
- Textual floor plan description with dimensions
- Walls removed (with load-bearing confirmation)
- Walls added
- Plumbing moves (and cost implications)
- Pros and cons
- Estimated cost tier impact
- RGEU compliance status

### 8. Comparative analysis
| Criteria | Option A | Option B | Option C |
|---|---|---|---|
| Circulation efficiency | ... | ... | ... |
| Natural light | ... | ... | ... |
| Privacy gradient | ... | ... | ... |
| RGEU compliance | ... | ... | ... |
| Structural impact | ... | ... | ... |
| Plumbing impact | ... | ... | ... |
| Cost impact | ... | ... | ... |
| WOW factor | ... | ... | ... |

### 9. Recommendation
State the recommended option with rationale tied to the client's briefing priorities.

## Output template

```markdown
---
project: <client/property>
date: <YYYY-MM-DD>
type: diva-floor-plan
area_total_m2: <number>
area_util_m2: <number>
typology_current: <T0-T5>
typology_proposed: <T0-T5>
options_count: <2-3>
---

# Analise de Planta DIVA — <Property/Client>

## Planta Existente
### Dimensoes gerais
### Elementos estruturais (imoveis)
### Pontos fixos (prumadas, shafts)
### Programa atual

## Auditoria RGEU
| Espaco | Area atual | Min RGEU | Conforme? |
|---|---|---|---|
| Sala | ... | 12 m2 | ... |
| Quarto 1 | ... | 10.5 m2 | ... |
| Cozinha | ... | 6 m2 | ... |
| WC | ... | 3.5 m2 | ... |

### Nao-conformidades identificadas

## Analise de Circulacao
### Fluxo entrada-social-privado
### Eficiencia de corredor (% da area)
### Triangulo de cozinha
### Fluxos de servico

## Mapa de Zonas Funcionais
### Zona social
### Zona privada
### Zona de servico
### Zona humida

## Luz Natural e Orientacao
### Orientacao por fachada
### Profundidade de penetracao
### Espacos deficitarios

## Opcao A — Conservadora
### Descricao do layout
### Alteracoes estruturais: nenhuma/minimas
### Pros
### Contras
### Impacto custo: baixo

## Opcao B — Optimizada
### Descricao do layout
### Alteracoes estruturais
### Pros
### Contras
### Impacto custo: medio

## Opcao C — Transformadora
### Descricao do layout
### Alteracoes estruturais
### Pros
### Contras
### Impacto custo: alto

## Comparacao
| Criterio | Opcao A | Opcao B | Opcao C |
|---|---|---|---|
| Circulacao | ... | ... | ... |
| Luz natural | ... | ... | ... |
| Privacidade | ... | ... | ... |
| RGEU | ... | ... | ... |
| Custo | ... | ... | ... |

## Recomendacao
<Recommended option + rationale>

## Proximos Passos
- [ ] Cliente escolhe opcao preferida
- [ ] Seguir com `diva-materials` para especificacao de materiais
- [ ] Seguir com `diva-budget` para orcamento da opcao escolhida
- [ ] Projeto de especialidades (estabilidade, redes)
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Analise Planta DIVA.md`

## Red flags — don't do this
- Never propose removing a wall without confirming it is NOT load-bearing
- Never ignore RGEU minimum dimensions for new layouts
- Never forget to check plumbing stack positions before moving wet areas
- Never propose a layout where a bedroom is only accessible through another bedroom
- Never ignore the kitchen work triangle
- Never place a WC door opening directly onto the kitchen or dining area
- Never forget cross-ventilation requirements
- Never assume window positions can be moved (structural + facade implications)
- Never propose more than 3 options (decision paralysis)
- Never skip the comparative table (clients need side-by-side to decide)

## Interactions
- Usually follows `diva-diagnose` + `diva-briefing`
- Feeds into `diva-materials` for material specification per chosen layout
- Feeds into `diva-budget` for cost estimation of chosen option
- May trigger engineering consultation if structural changes are proposed
- Save via `dario-obsidian-save` to vault

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Dados da planta capturados e completos
- [ ] Dimensões externas do footprint registadas (ex: 11.40m × 8.20m)
- [ ] Paredes estruturais marcadas como IMOVÁVEL com justificação (ex: "parede de betão 20cm — IMOVÁVEL")
- [ ] Prumadas e zonas húmidas fixas identificadas por posição real
- [ ] Orientação solar indicada (N/S/E/O) com ao menos uma fachada dominante
- [ ] Pé-direito declarado (uniforme ou variável por zona)

❌ NOT delivery-ready: "A planta tem alguns quartos e uma sala, com janelas a sul."
✅ Delivery-ready: "Footprint 9.80m × 11.20m = 109.76m². Parede central em betão armado 20cm — IMOVÁVEL. Prumada WC fixada no canto NE. Janelas sul: 3× 1.20m × 1.40m. Pé-direito 2.65m uniforme."

---

### Gate 2 — Auditoria RGEU executada e flagada
- [ ] Cada divisão habitable verificada contra áreas mínimas (Art. 65-67)
- [ ] Área de janela calculada vs. 1/8 da área do piso para cada quarto
- [ ] Não-conformidades classificadas como CRITICO ou EXISTENTE (grandfathered)
- [ ] Pé-direito mínimo 2.40m (habitável) / 2.20m (WC/arrumos) confirmado

❌ NOT delivery-ready: "O espaço cumpre os regulamentos em geral."
✅ Delivery-ready: "Quarto 2: 5.80m² — CRITICO, abaixo do mínimo RGEU 6.50m². Janela sala: 1.44m² para 14.20m² de área → ratio 1/9.9 — CRITICO (mínimo 1/8 = 1.78m²). WC: 3.60m², conforme."

---

### Gate 3 — Análise de circulação com métricas reais
- [ ] Percentagem de área de circulação calculada (corredor + hall / área total)
- [ ] Sequência entrada → zona social → zona privada avaliada explicitamente
- [ ] Kitchen triangle perimeter calculado em metros (target 3.6–7.9m)
- [ ] Dead-ends identificados ou confirmados como ausentes
- [ ] Percurso de serviço (roupa, lixo, compras) descrito

❌ NOT delivery-ready: "A circulação é razoável mas pode melhorar."
✅ Delivery-ready: "Corredores: 8.40m² de 72.00m² total = 11.7% — dentro do target <15%. Kitchen triangle: 6.20m — ótimo. Quarto 3 acessível apenas via Quarto 2 — DEAD-END, endereçado na Opção B."

---

### Gate 4 — 2-3 alternativas estruturadas com dados comparativos
- [ ] Cada opção tem dimensões textuais das divisões principais (ex: "sala 14.80m² → 18.20m²")
- [ ] Paredes removidas identificadas como estruturais/não-estruturais com implicação de custo
- [ ] Movimentos de plumbing declarados com tier de custo (ex: "deslocação prumada +€3.500–5.000")
- [ ] Tabela comparativa preenchida com critérios reais, não genéricos

❌ NOT delivery-ready: "Opção A é mais conservadora, Opção B é melhor para a maioria."
✅ Delivery-ready: "Opção A: sala passa de 11.20m² para 14.60m² (remoção parede gesso 3.80m — não-estrutural). Custo incremental: €800–1.200. Opção B: relocalização WC social 1.20m norte, sala 18.40m² — custo adicional vs A: +€4.200 prumada."

---

### Gate 5 — Orientação solar e luz natural quantificadas
- [ ] Cada divisão habitable mapeada para orientação (N/S/E/O)
- [ ] Estratégia de luz emprestada proposta se profundidade > 6m da janela
- [ ] Quartos privados alocados a orientação favorável (E para quartos, S para sala)
- [ ] Risco de sobreaquecimento Oeste identificado com solução (ex: palas, 60cm)

❌ NOT delivery-ready: "A sala tem boa luz natural por estar a sul."
✅ Delivery-ready: "Sala principal: fachada sul, 3 vãos × 1.20m = ratio 1/6.5 — excelente. Quarto principal: Oeste — risco sobreaquecimento Jul/Ago, recomenda-se pala horizontal 55cm ou estores blackout exteriores. Quarto 2: Norte, sem risco térmico, adequado para escritório."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] Nome do cliente/projeto aparece no cabeçalho ou título (ex: "Apartamento Cuidai — Rua X, Lisboa")
- [ ] Nenhum placeholder `<cliente>`, `<endereço>`, `<área>`, `<tipologia>` visível
- [ ] Tipologia declarada explicitamente (ex: T2 renovação total, 72m², Lisboa 1900)
- [ ] Referência ao briefing DIVA anterior se skill `diva-briefing` foi executado

❌ NOT delivery-ready: "Análise para `<nome do cliente>`, apartamento T`<X>` com `<área>`m²."
✅ Delivery-ready: "Análise de Planta — Apartamento Vivenda · Rua Tomás da Anunciação 14, 2ºDt, Lisboa · T2 · 74.30m² · Renovação Completa · Briefing DIVA: 12 Jan 2025."

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Análise de Planta — Apartamento Vivenda
**Rua Tomás da Anunciação 14, 2ºDt — Lisboa, Campolide**
Tipologia: T2 | Área bruta: 74.30m² | Área útil estimada: 68.80m²
Construção: 1962 | Orientação dominante: Sul + Nascente
Briefing DIVA executado: 14 Jan 2025 | Programa: casal sem filhos, WFH 1 pessoa

---

## 1. Estado existente

**Footprint:** 10.60m (frente) × 7.20m (fundo)
**Pé-direito:** 2.72m uniforme (habitável) — conforme RGEU mínimo 2.40m ✅

| Divisão | Área existente | Orientação | Observações |
|---|---|---|---|
| Sala/jantar | 11.20m² | Sul | Infrared solar direto Nov–Mar |
| Cozinha | 5.40m² | Norte | **CRITICO: abaixo mín. 6.00m²** |
| Quarto principal | 10.80m² | Sul | Conforme ✅ |
| Quarto 2 | 5.90m² | Nascente | **CRITICO: abaixo mín. 6.50m²** |
| WC único | 3.60m² | Interior | Conforme ✅ |
| Hall/corredor | 7.20m² | — | 10.5% área total |

**Prumadas:** coluna de água/esgotos fixada parede Norte (cozinha + WC empilhados)
**Estrutural:** 2 paredes em alvenaria resistente identificadas — parede mestra N-S central + parede tardoz

---

## 2. Auditoria RGEU

| Não-conformidade | Severity | Artigo | Dimensão atual | Mínimo exigido |
|---|---|---|---|---|
| Cozinha 5.40m² | CRITICO | Art. 66 | 5.40m² | 6.00m² |
| Quarto 2 5.90m² | CRITICO | Art. 65 | 5.90m² | 6.50m² |
| Luz sala: ratio 1/10.7 | CRITICO | Art. 71 | 1.05m² janela | 1.40m² mínimo |
| Ventilação cozinha | EXISTENTE | Art. 76 | Sem extração | Extração mecânica |

**Nota:** não-conformidades EXISTENTE são grandfathered se não houver alteração de uso.

---

## 3. Análise de circulação

- **Hall → Social → Privado:** ✅ sequência correta, entrada direta para hall
- **Circulação total:** 7.20m² / 68.80m² = **10.5%** — dentro do target <15% ✅
- **Kitchen triangle:** frigorífico–lava-louça–fogão = **7.80m perimeter** — CRITICO acima de 7.90m (marginal)
- **Dead-end:** nenhum ✅
- **Percurso serviço:** máquina roupa em cozinha → corredor 3.20m até WC único — aceitável mas subótimo

---

## 4. Luz natural e orientação

| Divisão | Orientação | Ratio janela/área | Status |
|---|---|---|---|
| Sala | Sul | 1/10.7 | ❌ CRITICO |
| Quarto principal | Sul | 1/6.8 | ✅ Excelente |
| Quarto 2 | Nascente | 1/8.4 | ✅ Conforme |
| Cozinha | Norte | Sem janela direta | ❌ Luz emprestada apenas |

**Profundidade crítica:** sala tem 5.40m de profundidade → dentro do limite 6m ✅
**Risco térmico:** nenhuma fachada Oeste significativa — sem risco sobreaquecimento

---

## 5. Alternativas de layout

### Opção A — Conservadora (sem obras estruturais)
**Intervenção:** remoção parede tabique cozinha/sala (não-estrutural, 3.20m)

- Cozinha integrada em open-plan: **6.80m²** ✅ (resolve CRITICO RGEU)
- Sala/jantar ampliada: **19.60m²** (de 11.20m²)
- Ratio luz sala: 1/6.6 ✅ (janela existente agora serve área maior contígua)
- Kitchen triangle: 5.40m ✅ (reorganização bancada em L)
- Quarto 2 permanece 5.90m² — CRITICO mantido (não endereçável sem estrutural)

**Custo incremental:** €1.800–2.400 (demolição tabique + acabamentos)
**Prazo:** 3–4 semanas
**RGEU:** resolve 2 de 4 não-conformidades

✅ Pros: mínimo investimento, open-plan moderno, cozinha conforme
❌ Cons: Quarto 2 sub-dimensionado mantém-se, kitchen triangle marginal

---

### Opção B — Optimizada (intervenção média)
**Intervenção:** Opção A + expansão Quarto 2 por absorção de 0.70m do corredor

- Quarto 2: **6.60m²** ✅ (resolve CRITICO RGEU)
- Corredor: **5.80m²** → 8.4% área total ✅
- Largura corredor residual: **1.05m** — acima mínimo RGEU 0.90m ✅
- Instalação extração mecânica cozinha (parede Norte, 3.80m de distância a shaft)

**Custo incremental vs A:** +€2.200 (reconstrução parede corredor + extração)
**Custo total:** €4.000–5.200
**Prazo:** 5–6 semanas
**RGEU:** resolve 3 de 4 não-conformidades

✅ Pros: todos os quartos conformes, corredor mais eficiente, cozinha ventilada
❌ Cons: corredor ligeiramente apertado, requer licença de obras de alteração

---

### Opção C — Transformativa (intervenção completa)
**Intervenção:** Opções A+B + relocalização WC para zona interior central + suite no Quarto principal

- WC deslocado 1.40m sul (novo shaft, prumada existente serve como âncora)
- Quarto principal com WC en-suite: **12.20m²** quarto + **4.80m²** WC privativo
- WC social standalone: **3.80m²** (acessível do hall, sem cruzar zona privada) ✅
- Programa WFH: Quarto 2 convertido em escritório/quarto hóspedes: **6.60m²**

**Custo incremental vs B:** +€8.500–11.000 (deslocação prumada, novo shaft, 2 WC novos)
**Custo total:** €13.000–17.000
**Prazo:** 10–14 semanas
**RGEU:** conformidade total ✅

✅ Pros: suite resolve programa do casal, WC social correto, adequado ao briefing WFH
❌ Cons: investimento significativo, risco de derrapagem em deslocação de prumadas

---

## 6. Tabela comparativa

| Critério | Opção A | Opção B | Opção C |
|---|---|---|---|
| Conformidade RGEU | 2/4 resolvidas | 3/4 resolvidas | 4/4 ✅ |
| Eficiência circulação | 10.5% | 8.4% | 7.8% |
| Luz natural (sala) | 1/6.6 ✅ | 1/6.6 ✅ | 1/6.6 ✅ |
| Kitchen triangle | 5.40m ✅ | 5.40m ✅ | 5.40m ✅ |
| Adequação ao briefing | Parcial | Boa | Excelente |
| Custo estimado | €1.800–2.400 | €4.000–5.200 | €13.000–17.000 |
| Prazo | 3–4 sem | 5–6 sem | 10–14 sem |

**Recomendação DIVA:** Opção B para o programa e orçamento declarado no briefing de 14 Jan 2025.
Opção C indicada se decisão de venda ou arrendamento premium for tomada.
```

---

## Output anti-patterns

- Listar não-conformidades RGEU sem classificar CRITICO vs EXISTENTE — cria falsa urgência ou falsa segurança
- Descrever paredes removidas sem confirmar se são estruturais — risco de erro construtivo e responsabilidade legal
- Apresentar opções sem custo estimado por tier — cliente não consegue decidir sem âncora financeira
- Calcular kitchen triangle como distância linear entre dois pontos em vez de perímetro dos três vértices
- Omitir o ratio janela/área para cada divisão habitável e apenas dizer "boa luz natural"
- Recomendar deslocação de prumada sem notar implicação de custo (+€3.500–5.000 típico em PT)
- Produzir tabela comparativa com células "melhor / médio / pior" sem valores concretos
- Ignorar a orientação solar ao propor onde colocar quartos vs. zonas sociais
- Apresentar Opção C como "melhor" sem a qualificar com o orçamento declarado no briefing
- Usar placeholders `<tipologia>`, `<nome>`, `<área>` no output final entregue ao cliente
