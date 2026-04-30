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
