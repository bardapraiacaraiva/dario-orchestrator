---
name: diva-materials
description: Material specification and palette creation for architecture and interior design projects in Portugal. Creates material boards with exact references (brand/model/color/finish), price per m2, Portuguese suppliers, and alternatives by price tier (economico/recomendado/premium). Covers pavimentos, revestimentos, bancadas, caixilharia, ferragens, and texteis. Triggers on "materiais", "materials", "acabamentos", "paleta", "revestimentos", "ceramica", "pedra", "madeira".
license: MIT
---

# DIVA Skill — Material Specification & Palette

Creates comprehensive material specification documents with exact product references, pricing, Portuguese suppliers, and tiered alternatives. Ensures material choices align with the project briefing, budget, and regulatory requirements while maintaining design coherence across all surfaces and finishes.

## When to activate

Invoke `/diva-materials` (or trigger automatically) when:
- User needs to specify materials for a project
- User asks about finishes, surfaces, or material options
- User wants a material palette or mood board specification
- User asks "what material should I use for..."
- After `diva-floor-plan` defines the layout and `diva-briefing` captures style preferences
- User needs to compare material options across price tiers

Do NOT use when:
- User needs only a budget without material details (use `diva-budget`)
- Project is in early diagnostic phase (use `diva-diagnose` first)
- User needs structural material engineering (steel, concrete specs)

## Workflow

### 1. Gather material context
From briefing and floor plan, determine:
- **Style direction:** from `diva-briefing` Section C
- **Rooms to specify:** from `diva-floor-plan` or briefing program
- **Budget tier:** from briefing Section E
- **Technical constraints:** humidity zones, floor heating compatibility, weight limits
- **Client preferences:** loved/hated materials from briefing
- **Existing elements to match:** if partial renovation, what stays

If no briefing exists, ask for: style direction, budget tier, and rooms to specify.

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "interior design materials specification portugal", limit: 5)
mcp__dario-rag__search_kb(query: "<style direction> materials palette finishes", limit: 5)
mcp__dario-rag__search_kb(query: "portuguese suppliers ceramics stone wood", limit: 5)
```

### 3. Material categories — specify each
For every category, provide 3 tiers: Economico / Recomendado / Premium.

#### 3.1 Pavimentos (flooring)
- **Zonas secas (sala, quartos, corredor):**
  - Wood: soalho macico (carvalho, nogueira, faia), multicamada/engineered, flutuante
  - Ceramic: porcelanico retificado (efeito madeira, cimento, pedra)
  - Stone: calcario, marmore, granito, ardosia
  - Vinyl/SPC: para orcamentos baixos ou arrendamento
- **Zonas humidas (WC, cozinha, lavandaria):**
  - Ceramic: porcelanico antiderrapante (R10/R11), mosaico hidraulico
  - Stone: tratado para agua, quartz composite
  - Microcimento: continuo, sem juntas (sobre existente)
- **Exterior (varanda, terraco):**
  - Ceramico exterior (R11+, resistencia gelo se necessario)
  - Deck composito ou madeira tratada (IPE, pinho tratado)
  - Pedra natural

#### 3.2 Revestimentos paredes
- **Tintas:** marca, acabamento (mate, acetinado, satinado), lavabilidade
  - Standard PT: Robbialac, CIN, Barbot, Dyrup
  - Premium: Farrow & Ball, Little Greene, Flamant
- **Ceramica parede:** formato, cor, assentamento (alinhado, espinha, metro)
- **Pedra natural/reconstituida:** para feature walls
- **Papel de parede:** vinilico lavavel para zonas humidas
- **Paineis:** ripado madeira, MDF lacado, cortica
- **Microcimento/beton cire:** paredes continuas
- **Azulejo portugues:** artesanal, reproduces historicas, contemporaneo

#### 3.3 Bancadas (countertops)
- **Cozinha:** quartzito, granito, Silestone/Dekton (Cosentino), Neolith, Lapitec, inox, madeira macica
- **WC:** mesmos materiais, adicionar Corian/solid surface, ceramica
- **Espessura:** standard 20mm, premium 30mm, ultrafino 12mm
- **Acabamento:** polido, amaciado, bruto, veined

#### 3.4 Caixilharia (windows & doors)
- **Material:** aluminio (com/sem corte termico), PVC, madeira, misto (madeira+aluminio)
- **Vidro:** duplo (4+16+4), triplo, baixo emissivo, controlo solar
- **Certificacao:** classe de permeabilidade ao ar, estanquidade agua
- **Marcas PT:** Cortizo, Extrusal, Reynaers, Technal, Schuco (premium)
- **Interior doors:** macicas, semi-macicas, ocas, correr, pivotantes
- **Ferragens porta:** marcas (Tupai, Olivari, FSB), acabamento (inox, preto, latio)

#### 3.5 Louca sanitaria e torneiras
- **Louca:** Sanindusa (PT), Roca, Duravit, Villeroy & Boch, Flaminia
- **Torneiras:** Grohe, Hansgrohe (Axor), Bruma (PT), Dornbracht (premium)
- **Bases de duche:** resina, ceramica, pedra natural, nivel do chao (walk-in)
- **Banheiras:** encastrar, freestanding, acrilico, ferro fundido, solid surface

#### 3.6 Iluminacao
- **Encastrada:** downlights LED, perfis embutidos
- **Suspensa:** pendentes, candeeiros de teto
- **Parede:** apliques, balizadores
- **Decorativa:** candeeiros de pe, mesa
- **Fita LED:** indirecta, nichos, mobiliario
- **Marcas:** FLOS, Vibia, Artemide (premium), SLV, Eglo (standard)

#### 3.7 Ferragens e acessorios
- **Puxadores:** tipo (embutido, barra, concha), material, acabamento
- **Dobradicas:** standard, soft-close, push-to-open
- **Corrediceas gavetas:** telescopica, full-extension, soft-close (Blum, Hettich, Grass)
- **Acessorios WC:** porta-toalhas, dispensers, espelhos (marcas: Geesa, Inda, Gessi)
- **Tomadas e interruptores:** series (Legrand Niloe/Valena, Schneider Unica, Jung LS990, BTicino)

#### 3.8 Texteis e soft furnishing
- **Cortinas/estores:** blackout, screen, rolo, painel japones, cortinados
- **Estofos:** tecidos (linho, veludo, boucle), pele, outdoor fabrics
- **Tapetes:** material, dimensao por zona

### 4. Material board construction
For each room/zone, create a cohesive palette:
- 1 dominant material (60% of surfaces)
- 1-2 secondary materials (30%)
- 1 accent material (10%)
- Ensure harmony between adjacent spaces (transitions)

### 5. Portuguese supplier mapping
For each specified material, provide:
- **Brand and reference:** exact product name/code
- **Price per m2/unit:** approximate 2026 market price
- **Where to buy in Portugal:**
  - Ceramica: Revigrés, Love Tiles, Margres (PT manufacturers), Porcelanosa, Marazzi
  - Pedra: Solancis, Moca Stone, Estremoz marble quarries
  - Madeira: Jular, Woodriver, Gamaobra
  - Bancadas: Cosentino (Dekton/Silestone), Margraf, Levantina
  - Generalistas: Leroy Merlin, AKI, Bricomarche,DERA
  - Premium: Cristacer, Sonas, Bartolomeu (Lisboa), Simonetta Capecchi
- **Lead time:** standard stock vs custom order
- **Sample availability:** where to get physical samples

### 6. Technical compatibility check
- Floor heating compatibility (ceramic/stone OK, some woods not)
- Humidity resistance for wet zones
- Slip resistance classification (R9-R13 per zone)
- UV resistance for sun-exposed areas
- Maintenance requirements (sealed stone, oiled wood, etc.)
- Weight per m2 (important for elevated floors and old buildings)

## Output template

```markdown
---
project: <client/property>
date: <YYYY-MM-DD>
type: diva-materials
style: <style direction>
budget_tier: <economico|recomendado|premium>
rooms_specified: <count>
---

# Especificacao de Materiais DIVA — <Client/Property>

## Direcao Estetica
<Brief description of the material palette concept and rationale>

## Paleta Geral
| Elemento | Material | Cor/Acabamento | Referencia |
|---|---|---|---|
| Dominante (60%) | ... | ... | ... |
| Secundario (30%) | ... | ... | ... |
| Accent (10%) | ... | ... | ... |

## Pavimentos
### Zonas secas
| Tier | Material | Referencia | EUR/m2 | Fornecedor |
|---|---|---|---|---|
| Economico | ... | ... | ... | ... |
| Recomendado | ... | ... | ... | ... |
| Premium | ... | ... | ... | ... |

### Zonas humidas
| Tier | Material | Referencia | EUR/m2 | Fornecedor |
|---|---|---|---|---|

### Exterior
| Tier | Material | Referencia | EUR/m2 | Fornecedor |
|---|---|---|---|---|

## Revestimentos Parede
### Tinta geral
| Tier | Marca | Linha | Cor/Ref | EUR/L |
|---|---|---|---|---|

### Ceramica WC/cozinha
| Tier | Material | Referencia | EUR/m2 | Fornecedor |
|---|---|---|---|---|

### Feature walls
| Tier | Material | Referencia | EUR/m2 | Fornecedor |
|---|---|---|---|---|

## Bancadas
### Cozinha
| Tier | Material | Referencia | EUR/ml | Fornecedor |
|---|---|---|---|---|

### WC
| Tier | Material | Referencia | EUR/ml | Fornecedor |
|---|---|---|---|---|

## Caixilharia
| Tier | Material | Marca | Vidro | EUR/m2 aprox |
|---|---|---|---|---|

## Louca Sanitaria
| Peca | Tier | Marca | Modelo | EUR/unid |
|---|---|---|---|---|

## Torneiras
| Local | Tier | Marca | Modelo | EUR/unid |
|---|---|---|---|---|

## Iluminacao
| Zona | Tipo | Marca | Modelo | EUR/unid |
|---|---|---|---|---|

## Ferragens
### Puxadores
### Dobradicas e corrediceas
### Tomadas e interruptores
### Acessorios WC

## Mapa por Divisao
### <Room 1>
| Superficie | Material escolhido | Referencia |
|---|---|---|
| Pavimento | ... | ... |
| Paredes | ... | ... |
| Teto | ... | ... |
| Bancada | ... | ... |

### <Room 2>
...

## Verificacao Tecnica
| Material | Aquecimento chao | Humidade | Antiderrapante | Manutencao |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Fornecedores e Amostras
| Fornecedor | Materiais | Morada/Contacto | Amostras |
|---|---|---|---|

## Proximos Passos
- [ ] Obter amostras fisicas dos materiais recomendados
- [ ] Cliente valida paleta antes de encomendar
- [ ] Seguir com `diva-budget` para orcamento com materiais definidos
- [ ] Confirmar lead times antes de iniciar obra
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Materiais DIVA.md`

## Red flags — don't do this
- Never specify materials without checking technical compatibility (humidity, heat, slip)
- Never provide prices without date reference (materials inflate ~5-8%/year in PT)
- Never specify a single option without alternatives (always 3 tiers)
- Never forget transition zones between different floor materials
- Never specify porcelanico without confirming rectified edges for minimal joint
- Never use marble in kitchen countertops without warning about staining/etching
- Never specify wood flooring for wet zones without explicit waterproof certification
- Never ignore weight limits in old buildings (stone floors can be very heavy)
- Never forget to check if specified ceramics are still in production
- Never mix more than 3 different floor materials in one home (visual chaos)

## Interactions
- Usually follows `diva-briefing` (style preferences) and `diva-floor-plan` (rooms to specify)
- Feeds into `diva-budget` for accurate cost calculation
- May loop back to `diva-floor-plan` if material constraints affect layout
- Save via `dario-obsidian-save` to vault

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

### 1. GATE — Referências de produto verificáveis (não genéricas)
- [ ] Cada material inclui: marca + modelo/coleção + referência de cor + acabamento específico
- [ ] Preços por m² indicados com fonte e data (ex: "Leroy Merlin PT, jan 2025")
- [ ] Fornecedores portugueses reais listados com morada ou URL (não "loja de materiais local")
- [ ] Certificações técnicas presentes quando relevantes (R10/R11 para zonas húmidas, classe A1 fogo, etc.)

❌ NOT delivery-ready: "Pavimento em porcelânico cinza, aprox. 25€/m², disponível em lojas de materiais"
✅ Delivery-ready: "Pavimento: Porcelânico Marca Corona — coleção Ritual Grey 60×120cm, ref. RT6012GR, acabamento mate rectificado, 34€/m² (Leroy Merlin PT, jan 2025); alternativa Economica: Novabell Crossover Ash 60×60cm, 18€/m², Tiles & More Lisboa"

---

### 2. GATE — Três tiers completos por categoria (Económico / Recomendado / Premium)
- [ ] Todas as categorias aplicáveis ao projeto têm os 3 tiers preenchidos (não apenas 1 opção)
- [ ] Delta de preço entre tiers é explícito e justificado (ex: "+40% por espessura 30mm e acabamento polido")
- [ ] Tier Recomendado alinha com o budget tier do briefing do cliente
- [ ] Tier Económico não compromete requisitos técnicos mínimos (ex: R10 mantido em WC)

❌ NOT delivery-ready: "Premium: mármore Carrara. Económico: cerâmica tipo mármore."
✅ Delivery-ready: "Premium: Mármore Carrara Bianco polido 60×60cm, 185€/m² (Mármores Galrão, Lisboa) — Recomendado: Silestone Blanco Zeus 20mm, 95€/m² (Cosentino PT, Porto) — Económico: Porcelânico Ragno Marbled White 60×120cm, 28€/m² (AKI PT)"

---

### 3. GATE — Coerência visual da paleta entre divisões
- [ ] Código HEX atribuído a cada cor da paleta (paredes, mobiliário, têxteis, apontamentos)
- [ ] Fio condutor visual explícito: 1 material ou cor âncora repetido em ≥ 2 divisões
- [ ] Contraste e equilíbrio documentado: proporção claro/escuro/neutro por divisão (ex: 70/20/10)
- [ ] Materiais quentes e frios em balanço justificado (não mistura aleatória de acabamentos)
- [ ] Se projeto multi-divisão: tabela de consistência pavimento → parede → teto por zona

❌ NOT delivery-ready: "Paleta neutra com toques de cor quente."
✅ Delivery-ready: "Âncora: carvalho natural #C8A96E em pavimento sala + prateleiras cozinha. Paredes: branco-quente Robbialac Marfim Suave #F5F0E8 (70%). Apontamento: verde-musgo #4A5E4A em painel cabeceira e cortinados (10%). Proporção por divisão: 70/20/10."

---

### 4. GATE — Compatibilidade técnica e regulatória
- [ ] Materiais em zonas húmidas têm classificação antiderrapante ≥ R10 (WC) ou R11 (exterior)
- [ ] Pavimentos compatíveis com piso radiante indicados (se aplicável ao projeto)
- [ ] Caixilharia com classe de desempenho indicada (permeabilidade ar, estanquidade água — EN 12207/12208)
- [ ] Vidros com especificação completa (ex: 4+16Ar+4 baixo emissivo Ug=1.1 W/m²K)
- [ ] Revestimentos exteriores com resistência gelo indicada se projeto em zona de altitude ≥ 500m

❌ NOT delivery-ready: "Pedra natural no WC, bonita e resistente."
✅ Delivery-ready: "WC: Limestone Moca Creme 40×40cm tratado com hidrofugante Fila MP90, R10 certificado, 65€/m² (Margraço, Sintra) — NÃO usar pedra polida (R9, não cumpre requisito antiderrapante WC)."

---

### 5. GATE — Estimativa de custo total estruturada
- [ ] Custo por m² × área de cada divisão calculado explicitamente
- [ ] Subtotal por categoria (pavimentos, revestimentos, bancadas, etc.)
- [ ] Total de materiais separado de mão-de-obra (nota: MO não incluída ou estimada separadamente)
- [ ] Variação de custo entre cenário Económico e Premium expressa em € totais (ex: "delta €4.200")
- [ ] IVA (23%) indicado: valores com e sem IVA

❌ NOT delivery-ready: "Estimativa total: €15.000–€25.000 consoante escolhas."
✅ Delivery-ready: "Pavimentos sala 28m²: Recomendado 34€/m² = €952 s/IVA (€1.171 c/IVA). Revestimento WC 12m²: Recomendado 65€/m² = €780 s/IVA. Total materiais cenário Recomendado: €8.340 s/IVA / €10.258 c/IVA. Delta vs. Premium: +€3.960."

---

### 6. GATE — Output usa NOME DO CLIENTE + dados REAIS em todo o documento — sem angle-brackets placeholder
- [ ] Nome do cliente (ou projeto) aparece no título e cabeçalho do material board
- [ ] Divisões referenciadas pelo nome real do projeto (ex: "Sala de Estar — Apt. Príncipe Real" não "Sala Principal")
- [ ] Nenhum campo contém `<nome>`, `<material>`, `<preço>`, `<fornecedor>` ou similar
- [ ] Todos os preços são de fornecedores PT reais e verificáveis (não valores placeholder)
- [ ] Links ou contactos de fornecedores presentes onde possível

❌ NOT delivery-ready: "Bancada cozinha: `<material premium>` de `<fornecedor>`, aprox. `<preço>`€/m²."
✅ Delivery-ready: "Bancada cozinha — Projeto Ferreira / Apt. Príncipe Real: Dekton Kreta 12mm, ref. DK-KRT-12, 210€/m² (Cosentino PT, Rua Alfredo da Silva 4, Amadora, tel. 214 946 400)."

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Especificação de Materiais — Projeto Cuidai HQ
## Remodelação Escritórios + Sala de Reuniões | Lisboa, Príncipe Real
**Data:** Janeiro 2025 | **Budget tier:** Recomendado (com apontamentos Premium)
**Área total:** 145m² | **Preparado por:** DIVA Materials

---

## PALETA ÂNCORA

| Papel | Cor | HEX | Material âncora |
|---|---|---|---|
| Base neutra | Branco quente | #F2EDE6 | Paredes gerais |
| Estrutura | Carvalho natural | #C9A96E | Pavimento + estantes |
| Apontamento | Verde-floresta | #3B5249 | Mobiliário accent + têxteis |
| Contraste | Grafite mate | #2E2E2E | Caixilharia + ferragens |

Proporção por divisão: 70% base / 20% estrutura / 10% apontamento

---

## 1. PAVIMENTOS

### 1.1 Escritório Open Space (62m²) — Zonas Secas

| Tier | Produto | Referência | Preço/m² s/IVA | Fornecedor PT |
|---|---|---|---|---|
| Económico | Pavimento SPC Classen NEO 2.0 Carvalho Báltico | CLN2-0847 | 18€ | Leroy Merlin PT (leroymerlin.pt) |
| **Recomendado ✓** | **Pavimento Engenharia Bauwerk Parquet Chêne Naturel 14mm** | **BW-CHN-14-NAT** | **52€** | **Soartes, R. Luciano Cordeiro 60, Lisboa** |
| Premium | Soalho Maciço Carvalho Europeu Boleado 20mm, Jular | JUL-CAR-20-BO | 98€ | Jular Madeiras, Alverca (jular.pt) |

**Escolha Recomendado:** 62m² × 52€ = **€3.224 s/IVA (€3.965 c/IVA)**
Nota técnica: Bauwerk compatível com piso radiante (certificado Δ T ≤ 12°C). Assentamento colado sobre betonilha nivelada.

---

### 1.2 WCs (2×) (18m² total) — Zonas Húmidas

| Tier | Produto | Referência | Preço/m² s/IVA | Fornecedor PT |
|---|---|---|---|---|
| Económico | Porcelânico Argenta Klen White 33×66cm R10 | ARG-KLW-3366 | 22€ | AKI Portugal (aki.pt) |
| **Recomendado ✓** | **Porcelânico Mutina Pico Bianco 10×10cm R10, pavimento** | **MT-PC-BIA-1010** | **68€** | **Mosa Tiles Lisboa, Av. 5 Outubro 12** |
| Premium | Mosaico Hidráulico Cimentício Cor Verde #3B5249, Cimenterie de la Tour | CDT-V3B52-20 | 145€ | Cimenterie FR, entrega PT 3 sem. |

**Paredes WC:** Tinta Robbialac Aqua Acetinado Branco Nata ref. 0001, 12€/L (2 dem.), lavabilidade classe 2.
**Escolha Recomendado:** 18m² × 68€ = **€1.224 s/IVA**. Certificação R10 confirmada (EN 13036-4).

---

## 2. REVESTIMENTOS PAREDES

### 2.1 Sala de Reuniões (28m²)

**Parede Focal (feature wall) — 1 parede, 14m²:**

| Tier | Produto | Referência | Preço/m² s/IVA | Fornecedor PT |
|---|---|---|---|---|
| Económico | Painel Ripado MDF Lacado Grafite, Leroy Merlin | LM-RIP-GRF-240 | 35€ | Leroy Merlin PT |
| **Recomendado ✓** | **Ripado Carvalho Natural 30×3000mm, Rehau Brilliant Wood** | **RH-BW-CAR-30** | **85€** | **Madertec, R. Particular à Fábrica dos Pentes 8, Lisboa** |
| Premium | Painel Nogueira Maciço Escovado, Dinesen | DIN-WAL-NOG-ESC | 210€ | Dinesen DK, entrega PT 4 sem. |

**Paredes restantes:** Robbialac Aqua Base Mate Branco Quente #F2EDE6, ref. RB-AQ-01, 8,50€/L (Leroy Merlin PT). Cobertura: 12m²/L, 2 demãos → 5L/parede. Total paredes gerais HQ: €340 s/IVA.

---

## 3. BANCADAS

### 3.1 Copa/Kitchenette (6 m.l. bancada)

| Tier | Produto | Referência | Esp. | Preço/m.l. s/IVA | Fornecedor PT |
|---|---|---|---|---|---|
| Económico | Silestone Blanco Norte 20mm | SIL-BNO-20 | 20mm | 180€ | Cosentino PT, Porto |
| **Recomendado ✓** | **Dekton Kreta Velvet 12mm** | **DK-KRT-VLV-12** | **12mm** | **245€** | **Cosentino PT, Amadora (214 946 400)** |
| Premium | Quartzito Taj Mahal Amaciado 30mm | MAR-TJM-30-AM | 30mm | 420€ | Margraço Pedras, Sintra (219 249 810) |

**Escolha Recomendado:** 6 m.l. × 245€ = **€1.470 s/IVA (€1.808 c/IVA)**
Acabamento: Velvet (mate suave, anti-impressão digital). Ponto de água: +€120 corte encastre cuba.

---

## 4. CAIXILHARIA

### Janelas Escritório (8 vãos, 2,0×1,2m cada)

| Tier | Sistema | Vidro | U vão | Preço/vão s/IVA | Fornecedor PT |
|---|---|---|---|---|---|
| Económico | PVC Deceuninck Elegant 76, branco | Duplo 4+16+4 Ug=1,4 | 1,8 W/m²K | 680€ | Janelux, Lisboa |
| **Recomendado ✓** | **Alumínio Cortizo COR-70 Thermal Break, grafite #2E2E2E** | **4+16Ar+4 BE Ug=1,1** | **1,4 W/m²K** | **1.100€** | **Extrusal, Porto (extrusal.com)** |
| Premium | Alumínio Schüco AWS 90.SI+ | Triplo 4+12Ar+4+12Ar+4 Ug=0,7 | 0,9 W/m²K | 2.200€ | Cortizo Ibérica PT |

**Escolha Recomendado:** 8 vãos × 1.100€ = **€8.800 s/IVA**
Classe desempenho: Permeabilidade ar Classe 4 (EN 12207), Estanquidade água Classe E900 (EN 12208).

---

## 5. RESUMO DE CUSTOS — CENÁRIO RECOMENDADO

| Categoria | Área/Qtd | Preço unit. | Subtotal s/IVA |
|---|---|---|---|
| Pavimento Open Space | 62 m² | 52€/m² | €3.224 |
| Pavimento WCs | 18 m² | 68€/m² | €1.224 |
| Revestimento feature wall | 14 m² | 85€/m² | €1.190 |
| Tintas paredes gerais | — | — | €340 |
| Bancada copa | 6 m.l. | 245€/m.l. | €1.470 |
| Caixilharia (8 vãos) | 8 un. | 1.100€/un. | €8.800 |
| **TOTAL s/IVA** | | | **€16.248** |
| **TOTAL c/IVA (23%)** | | | **€19.985** |

**Delta vs. Económico:** −€6.840 | **Delta vs. Premium:** +€14.320

---

*Preços verificados janeiro 2025. Sujeitos a confirmação de encomenda. Mão-de-obra não incluída.*
```

---

## Output anti-patterns

- **Materiais sem referência de produto real:** escrever "cerâmica cinza tipo cimento" sem marca/coleção/referência é inaceitável — o cliente não consegue encomendar
- **Preços "a partir de" ou "aproximadamente":** intervalos vagos sem fonte datada criam desconfiança; usar sempre valor específico + fornecedor + data
- **Apenas um tier por categoria:** omitir Económico ou Premium impede o cliente de tomar decisões informadas dentro do budget real
- **Cores descritas em palavras sem HEX:** "verde-água", "bege quente" sem código HEX não permite reprodução fiel na paleta
- **Ignorar compatibilidade técnica com piso radiante:** especificar soalho maciço espesso sem verificar compatibilidade térmico é um erro de projeto grave
- **Fornecedores genéricos ou inexistentes em PT:** citar "grandes superfícies" ou marcas sem presença verificável em Portugal obriga o cliente a pesquisa adicional
- **Custo total sem separação s/IVA vs. c/IVA:** em Portugal, IVA 23% é substancial — omiti-lo cria surpresas no orçamento final
- **Feature wall sem fio condutor à paleta âncora:** materiais de destaque desconexos da paleta geral criam incoerência visual que compromete o projeto
- **Certificações de segurança omitidas em zonas húmidas:** não indicar classe R10/R11 em pavimentos de WC ou exterior é uma falha técnica e de responsabilidade profissional
- **Angle-brackets no output final:** entregar documento com `<nome do cliente>`, `<referência>` ou `<a confirmar>` não é um documento de trabalho — é um rascunho incompleto
