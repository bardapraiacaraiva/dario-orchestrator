---
name: diva-ffe
description: Furniture, Fixtures & Equipment (FF&E) specification and procurement management for architecture and interior design projects. Room-by-room schedules with exact product references, dimensions, quantities, lead times, supplier tracking, budget control, and delivery coordination. Covers loose furniture, decorative lighting, textiles, accessories, art, and appliances. Triggers on "mobiliario", "furniture", "FF&E", "equipamento", "lista mobiliario", "procurement", "furniture schedule", "decoracao", "o que comprar".
license: MIT
---

# DIVA Skill — FF&E Schedule & Procurement

Creates comprehensive Furniture, Fixtures & Equipment schedules for architecture and interior design projects. Goes beyond the conceptual furniture references in `diva-moodboard` to produce actionable procurement documents: room-by-room item lists with exact specifications, dimensions, quantities, pricing across tiers, supplier contacts, lead times, delivery coordination, and budget tracking.

## When to activate

Invoke `/diva-ffe` (or trigger automatically) when:
- Project moves from design concept to procurement phase
- Client asks "what furniture do I need to buy?"
- Interior designer needs a procurement list for client approval
- Client wants to understand furniture + decoration budget
- Coordinating deliveries with construction completion timeline
- Client needs alternatives at different price points
- Staging a property for sale or short-term rental (AL)
- Hotel, restaurant, or office fit-out requiring FF&E schedule

Do NOT use when:
- Still in concept phase (use `diva-moodboard` first)
- Only need built-in furniture (kitchen, wardrobes — covered in `diva-budget` construction chapters)
- Structural or construction equipment

## FF&E categories

### Category 1: Loose Furniture (Mobiliario solto)
Sofas, armchairs, poufs, dining tables, chairs, coffee tables, side tables, consoles, beds, bedside tables, desks, office chairs, bookshelves, sideboards, TV units, outdoor furniture

### Category 2: Decorative Lighting (Iluminacao decorativa)
Table lamps, floor lamps, decorative pendants, decorative wall lights, candle holders

### Category 3: Textiles (Texteis)
Curtains, blinds (if not construction), rugs, cushions, throws, bed linen (hospitality), bath textiles

### Category 4: Decorative Accessories (Decoracao)
Vases, sculptures, decorative objects, picture frames, mirrors (decorative), clocks, trays, indoor plants and planters, candles, diffusers

### Category 5: Art (Arte)
Paintings, prints, photographs, art commissions, framing, hanging hardware

### Category 6: Appliances (Electrodomesticos)
Kitchen appliances (if not in construction), laundry, small appliances, TV, audio, home office equipment

### Category 7: Fixtures (Equipamento fixo — non-construction)
Curtain hardware (varoes, calhas), bathroom accessories, kitchen accessories, hooks, door stops, house numbers

## Workflow

### 1. Gather FF&E inputs

- **Project phase:** moodboard approved? construction timeline?
- **Rooms to furnish:** complete list from `diva-floor-plan`
- **Style direction:** from `diva-moodboard`
- **Budget for FF&E:** separate from construction budget
- **Existing furniture:** what client keeps, what gets replaced
- **Priority rooms:** which rooms to furnish first
- **Lifestyle:** kids, pets (durable fabrics), entertaining (extra seating)
- **Timeline:** construction completion date, move-in target
- **Delivery constraints:** elevator (LxWxH), stairwell, doorway widths

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "furniture specification interior design procurement FF&E schedule", limit: 5)
mcp__dario-rag__search_kb(query: "Portuguese furniture brands suppliers design contemporary", limit: 5)
```

### 3. Room-by-room specification

For each item, specify:
- **Item name:** descriptive (e.g., "Sofa 3 lugares, tecido boucle creme")
- **Quantity:** count
- **Dimensions:** LxWxH (cm) — MUST fit the floor plan
- **Material/Finish:** fabric type, wood species, metal finish
- **Color:** specific reference where possible
- **Option 1 (Recomendado):** brand, model, price
- **Option 2 (Economico):** lower price alternative
- **Option 3 (Premium):** upgrade option
- **Portuguese brand option:** if exists
- **Supplier:** store name, location, or URL
- **Lead time:** stock vs made-to-order (weeks)
- **Notes:** care, assembly, delivery conditions

### 4. Portuguese furniture sources

**Portuguese design brands:**

| Brand | Specialty | Tier | Location |
|---|---|---|---|
| Wewood | Solid wood, Portuguese design | Premium | Porto |
| AROUNDtheTREE | Tables, storage, solid wood | Premium | Lisboa |
| DAM | Contemporary Portuguese furniture | Medium-Premium | Porto |
| De La Espada | International quality, PT production | Luxury | Porto |
| Branca Lisboa | Marble furniture, objects | Premium | Lisboa |
| Gual | Upholstery, sofas, custom | Medium | Parede |
| Laskasas | Full home furnishing | Medium | Porto |
| Boca do Lobo | Statement luxury | Luxury | Porto |
| FJ Collection | Contract and residential | Medium | Lisboa |
| Fenabel | Chairs, contract seating | Medium | Pacos Ferreira |
| Pergamo | Tables, sideboards | Medium | Pacos Ferreira |

**Retail chains:**

| Store | Tier | Strengths | Delivery |
|---|---|---|---|
| IKEA | Economico | Immediate, basics, functional | Self or home |
| Kave Home | Econ-Medio | Good design/price online | 2-4 weeks |
| La Redoute Interieurs | Econ-Medio | Textiles, soft furnishing | 2-6 weeks |
| Maisons du Monde | Medio | Decorative, eclectic | 1-4 weeks |
| Area Store | Medio | Curated contemporary | In-store/delivery |
| Tracos Interiores | Medio-Premium | Curated design brands | 2-8 weeks |

**Design showrooms (premium):**

| Showroom | Brands | Location |
|---|---|---|
| Minotti Lisboa | Minotti | Lisboa |
| B&B Italia | B&B Italia, Maxalto | Lisboa |
| Boffi | Boffi, De Padova | Lisboa |
| Roche Bobois | Roche Bobois | Lisboa |

**Online (ships to PT):**

| Platform | Tier | Delivery | Notes |
|---|---|---|---|
| Made.com | Medio | 4-8 weeks | Good value design |
| Westwing | Medio-Premium | 2-6 weeks | Flash sales |
| 1stDibs | Premium-Luxury | Variable | Vintage, designer |
| Hem | Medio-Premium | 3-6 weeks | Scandinavian |

### 5. Budget framework

**FF&E as percentage of construction cost:**

| Project type | FF&E % of construction |
|---|---|
| Budget renovation | 15-25% |
| Medium renovation | 25-40% |
| Premium renovation | 40-60% |
| Luxury | 60-100%+ |
| Hospitality (hotel/AL) | 30-50% |

**Budget split within FF&E:**

| Category | % of FF&E |
|---|---|
| Loose furniture | 45-55% |
| Lighting (decorative) | 8-12% |
| Textiles (curtains, rugs, cushions) | 12-18% |
| Accessories and decor | 5-10% |
| Art | 5-15% |
| Appliances | 10-15% |
| Fixtures/hardware | 3-5% |

### 6. Procurement timeline

Align with construction phases:

| Timing | Action | Lead time |
|---|---|---|
| Design phase (month 1-2) | FF&E schedule created and approved | -- |
| Construction start (month 3) | Order custom/long-lead items (sofas, tables) | 8-16 weeks |
| Mid-construction (month 5) | Order medium-lead items (rugs, lighting, curtains) | 4-8 weeks |
| Pre-completion (month 7) | Order stock items (accessories, small items) | 1-2 weeks |
| Post-construction (month 8) | Receive deliveries, stage, style | 1-2 weeks |

**Critical path items (longest lead):**
- Custom upholstery: 8-16 weeks
- Custom curtains/blinds: 4-8 weeks
- Made-to-order rugs: 6-12 weeks
- Imported designer furniture: 8-16 weeks
- Art commissions: 4-12 weeks

### 7. Delivery coordination

- Measure all access points: doorways (min width), elevator (LxWxH), stairwell turns
- Confirm delivery address and parking for trucks
- Schedule deliveries room by room over 2-3 days
- Protect finished floors during delivery (temporary covering)
- Inspect every item on delivery (photograph any damage immediately)
- Keep packaging 48h for hidden damage claims
- Coordinate with construction team to ensure rooms are clean and ready

## Output template

```markdown
---
project: <project name>
date: <YYYY-MM-DD>
type: diva-ffe
rooms_count: <number>
total_items: <number>
budget_ffe: <EUR X>
tags: [mobiliario, FF&E, procurement, <project>]
---

# Mapa FF&E DIVA — <Project Name>

## 1. Resumo
- **Divisoes a mobilar:** <N>
- **Total de items:** <N>
- **Orcamento FF&E:** EUR <X>
- **Timeline encomendas:** a partir de <date>
- **Entrega prevista:** <date>

## 2. Mobiliario Existente (mantido)
| Item | Divisao actual | Divisao futura | Estado |
|---|---|---|---|
| ... | ... | ... | Bom/A restaurar |

## 3. Mapa por Divisao

### 3.1 Sala de Estar
| # | Item | Dims (cm) | Recomendado | EUR | Economico | EUR | Lead |
|---|---|---|---|---|---|---|---|
| S01 | Sofa 3 lug | 220x95x80 | <Brand> | X | <Alt> | X | 8-12s |
| S02 | Poltrona | 80x85x75 | <Brand> | X | <Alt> | X | 8-12s |
| S03 | Mesa centro | 120x60x40 | <Brand> | X | <Alt> | X | Stock |
| S04 | Candeeiro pe | -- | <Brand> | X | <Alt> | X | Stock |
| S05 | Tapete | 300x200 | <Brand> | X | <Alt> | X | 4-6s |
| S06 | Cortinas par | 280x260 | <Fabric> | X | <Alt> | X | 4-6s |
| S07 | Almofadas 4x | 50x50 | <Fabric> | X | <Alt> | X | Stock |
**Subtotal Sala:** EUR <recomendado> / EUR <economico>

### 3.2 Sala de Jantar
| # | Item | Dims | Recomendado | EUR | Economico | EUR | Lead |
|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... |

### 3.3 Cozinha (solto + electrodomesticos)
### 3.4 Suite Principal
### 3.5 Quarto 2
### 3.6 Quarto 3
### 3.7 Casa de Banho (acessorios)
### 3.8 Hall / Corredor
### 3.9 Escritorio / Home Office
### 3.10 Exterior

## 4. Resumo Orcamental

### Por divisao
| Divisao | Recomendado | Economico | Premium |
|---|---|---|---|
| Sala estar | ... | ... | ... |
| Sala jantar | ... | ... | ... |
| Suite | ... | ... | ... |
| ... | ... | ... | ... |
| **Total** | **EUR X** | **EUR X** | **EUR X** |

### Por categoria
| Categoria | EUR | % |
|---|---|---|
| Mobiliario solto | ... | 50% |
| Iluminacao decorativa | ... | 10% |
| Texteis | ... | 15% |
| Decoracao e acessorios | ... | 8% |
| Arte | ... | 7% |
| Electrodomesticos | ... | 10% |
| **Total** | **EUR X** | **100%** |

## 5. Calendario de Encomendas

### Prioridade 1 — Encomendar ja (>8 semanas lead)
| Item | Divisao | Fornecedor | Lead | Deposito |
|---|---|---|---|---|
| ... | ... | ... | ... | EUR X |

### Prioridade 2 — Encomendar em <mes> (4-8 semanas)
| Item | Divisao | Fornecedor | Lead |
|---|---|---|---|

### Prioridade 3 — Pre-conclusao obra (stock)
| Item | Divisao | Fornecedor |
|---|---|---|

## 6. Acessos e Entregas
- Porta entrada: <X> cm largura
- Elevador: <L>x<W>x<H> cm
- Restricoes: <escadas/rua estreita/horarios condominio>
- Protecao pavimentos: <tipo>

## 7. Fornecedores e Contactos
| Fornecedor | Items | Contacto | Pagamento |
|---|---|---|---|
| ... | ... | ... | ... |

## 8. Proximos Passos
- [ ] Cliente aprova mapa FF&E e tier orcamental
- [ ] Visitar showrooms para itens prioritarios (solicitar amostras tecido)
- [ ] Encomendar Prioridade 1 (long-lead)
- [ ] Coordenar com `diva-timeline` para alinhar entregas
- [ ] Revisao final pre-entrega com `diva-inspection`
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Project> - Mapa FFE DIVA.md`

## Red flags — don't do this
- Never present an FF&E budget without separating it from the construction budget — clients routinely underestimate furniture costs and face sticker shock when the building is finished and empty
- Never order custom furniture without confirming exact room dimensions from the as-built floor plan — ordering from design drawings can result in pieces that don't fit through doors or overwhelm small rooms
- Never order upholstered furniture without requesting and approving a physical fabric swatch — screen colours never match reality, and texture/durability can only be evaluated in person
- Never forget to measure access points (doors, elevator, stairwell) before ordering large items — a 3-seat sofa that doesn't fit through the front door is a EUR 2,000+ problem
- Never specify white/light fabrics for families with young children or pets without explicit maintenance discussion — even "stain-resistant" treatments have limits
- Never schedule all furniture deliveries on the same day — stagger by room over 2-3 days for proper placement and inspection
- Never accept "pronta entrega" claims without stock verification — in Portugal this can mean anything from same-day to 6 weeks

## Interactions
- Usually follows `diva-moodboard` (design direction) and `diva-floor-plan` (room dimensions)
- Complements `diva-materials` which covers built-in finishes (not loose furniture)
- Feeds into `diva-budget` for total project cost including FF&E
- Coordinates with `diva-timeline` for procurement scheduling
- May trigger `diva-render-brief` for visualization of furnished rooms
- Save via `diva-obsidian-save` to vault

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Room-by-room coverage completa

- [ ] Cada divisão do projecto tem a sua secção no schedule (não "sala + quarto" agrupados)
- [ ] Cada item tem: nome descritivo, quantidade, dimensões LxWxH (cm), material/acabamento, cor
- [ ] Nenhuma dimensão omitida — sofás sem "TBD", mesas sem "ver catálogo"
- [ ] Items marcam se substituem mobiliário existente ou são adições novas

❌ NOT delivery-ready: `Sofá sala — ver opções com cliente, dimensão a confirmar`
✅ Delivery-ready: `Sofá 3 lugares | 240×95×78cm | Tecido bouclé creme | Qty 1 | Substitui sofá actual cor castanha`

---

### Gate 2 — Três tier de opções por item principal

- [ ] Cada peça de mobiliário principal tem Opção 1 (Recomendado), Opção 2 (Económico), Opção 3 (Premium)
- [ ] Cada opção inclui: Marca + Modelo + Preço (€) + Fornecedor + URL ou loja
- [ ] Pelo menos uma opção portuguesa identificada quando aplicável (Wewood, DAM, Branca Lisboa, etc.)
- [ ] Lead time indicado: "stock" / "8 semanas" / "12–16 semanas made-to-order"

❌ NOT delivery-ready: `Cama casal — sugestão: IKEA ou algo parecido, preço médio`
✅ Delivery-ready: `Cama 180×200 | Rec: Wewood Frame Oak €1.890 / Econ: IKEA MALM €399 / Premium: De La Espada Ira €3.200 | Lead: 10 sem / stock / 14 sem`

---

### Gate 3 — Budget tracking e totais por categoria

- [ ] Tabela resumo com subtotal por categoria FF&E (Mobiliário, Iluminação, Têxteis, Decoração, Arte, Electrodomésticos, Fixtures)
- [ ] Total geral em três cenários: Económico / Recomendado / Premium
- [ ] % do orçamento total de obra indicado (FF&E tipicamente 15–30% do total)
- [ ] Contingência de 10% incluída na linha final do budget

❌ NOT delivery-ready: `Total estimado: €15.000–€40.000 dependendo das escolhas`
✅ Delivery-ready: `Mobiliário: €8.400 | Iluminação: €1.200 | Têxteis: €950 | Decoração: €600 | Total Rec: €11.150 + 10% cont. = €12.265`

---

### Gate 4 — Timeline e coordenação de entregas

- [ ] Data de conclusão de obra indicada e usada como âncora do procurement timeline
- [ ] Items com lead time >8 semanas têm data de encomenda calculada (deadline real)
- [ ] Sequência de entregas definida: obra acabada → pisos/pintura secos → móveis → têxteis → decoração
- [ ] Restrições de acesso documentadas: elevador (dim máx), porta de entrada (largura), escadas

❌ NOT delivery-ready: `Encomendar com antecedência, especialmente made-to-order`
✅ Delivery-ready: `Obra conclui 15 Mar 2026 → Sofá made-to-order encomendar até 20 Jan (8 sem) → Entrega prevista 17 Mar → Têxteis e decoração: semana de 23 Mar`

---

### Gate 5 — Fornecedores verificáveis e contactos accionáveis

- [ ] Nome do fornecedor escrito por extenso (não "loja de design em Lisboa")
- [ ] URL, morada ou contacto incluído por cada fornecedor principal
- [ ] Showrooms físicos em PT identificados para itens premium (Minotti Lisboa, B&B Italia, etc.)
- [ ] Alternativas online com envio para PT confirmado (La Redoute, Kave Home, Maisons du Monde)

❌ NOT delivery-ready: `Ver showrooms de design em Lisboa para opções premium`
✅ Delivery-ready: `Minotti Lisboa — Av. da Liberdade 169, Lisboa | minotti.com/pt | Lead 12–16 sem | Pedir cotação a João Ferreira (contacto via showroom)`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets

- [ ] Nenhum `[CLIENT NAME]`, `[INSERT ROOM]`, `[TBD]`, `[ver moodboard]` no output final
- [ ] Nome do projecto/cliente no cabeçalho do schedule (ex: "FF&E Schedule — Apartamento Cuidai, Av. Defensores de Chaves")
- [ ] Todos os preços são €, não "$" ou "price on request" sem contexto
- [ ] Datas são datas reais (DD/MM/AAAA), não "in X weeks" ou "soon"

❌ NOT delivery-ready: `FF&E Schedule — [NOME PROJECTO] | Preço: a consultar | Entrega: a definir`
✅ Delivery-ready: `FF&E Schedule — Vivenda Cascais, Rua das Flores 12 | Rev. 1 — 14 Jan 2026 | Budget Recomendado: €28.400`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# FF&E Schedule — Apartamento Cuidai HQ Lisboa
**Projecto:** Escritório + Sala de Reuniões + Zona de Descanso
**Morada:** Rua Rodrigo da Fonseca 44, 1250-189 Lisboa
**Área:** 120 m² | **Revisão:** 1.0 — 14 Janeiro 2026
**Obra conclui:** 28 Fevereiro 2026 | **Ocupação alvo:** 16 Março 2026
**Budget FF&E aprovado:** €22.000 (Recomendado) | Contingência 10%: €2.200

---

## SALA DE REUNIÕES — 18 m²

### 01 — Mesa de reuniões
**Qtd:** 1 | **Dim:** 280×100×75 cm | **Material:** Carvalho maciço, pés aço preto
| | Marca/Modelo | Preço | Fornecedor | Lead |
|---|---|---|---|---|
| ⭐ Rec | AROUNDtheTREE Tack Table Oak | €2.890 | aroundthetree.pt | 8 sem |
| 💰 Econ | IKEA MÖRBYLÅNGA 280cm | €699 | ikea.com/pt | Stock |
| 💎 Premium | Wewood Branch Table | €4.200 | wewood.eu | 10 sem |
**⚠️ Encomenda Rec até: 2 Janeiro 2026 (8 sem para 28 Fev)**

### 02 — Cadeiras de reunião (x10)
**Qtd:** 10 | **Dim:** 55×55×82 cm | **Material:** Tecido cinza antracite, pés cromados
| | Marca/Modelo | Preço unit | Total (x10) | Lead |
|---|---|---|---|---|
| ⭐ Rec | Fenabel Mia Chair Anthracite | €285 | €2.850 | 6 sem |
| 💰 Econ | Kave Home Shila Chair | €129 | €1.290 | 2–3 sem |
| 💎 Premium | B&B Italia Alphabeta | €680 | €6.800 | 12 sem |
**Fornecedor Rec:** Fenabel — fenabel.pt | T. +351 255 860 430

### 03 — Aparador lateral
**Qtd:** 1 | **Dim:** 180×45×85 cm | **Material:** Carvalho, frentes lacadas branco
| | Marca/Modelo | Preço | Fornecedor | Lead |
|---|---|---|---|---|
| ⭐ Rec | DAM Sideboard S01 Oak/White | €1.650 | dam.pt | 8 sem |
| 💰 Econ | Maisons du Monde Calvi | €449 | maisonsdumonde.com | 3 sem |

---

## ZONA DE DESCANSO — 22 m²

### 04 — Sofá modular
**Qtd:** 1 (config. 3 módulos) | **Dim:** 300×95×78 cm | **Material:** Bouclé cinza claro, pés carvalho
| | Marca/Modelo | Preço | Fornecedor | Lead |
|---|---|---|---|---|
| ⭐ Rec | Gual Modular Boucle Grey | €3.200 | gual.pt / Parede | 10 sem |
| 💰 Econ | La Redoute Miliboo Elysee | €1.190 | laredoute.pt | 4 sem |
| 💎 Premium | Roche Bobois Mah Jong | €7.800 | rochebobois.com | 14 sem |
**⚠️ Encomenda Rec até: 19 Dezembro 2025**
**Acesso elevador Cuidai HQ:** 140×100×220 cm — módulos Gual entram individualmente ✅

### 05 — Mesa de centro
**Qtd:** 1 | **Dim:** 120×70×38 cm | **Material:** Mármore Estremoz branco, pés latão
| | Marca/Modelo | Preço | Fornecedor | Lead |
|---|---|---|---|---|
| ⭐ Rec | Branca Lisboa Slab Table | €1.890 | brancalisboa.com | 6 sem |
| 💰 Econ | Area Store Marble Look | €520 | areastore.pt | 3 sem |

### 06 — Iluminação — Candeeiro de pé (x2)
**Qtd:** 2 | **Material:** Latão envelhecido, abajur linho bege
| | Marca/Modelo | Preço unit | Total | Lead |
|---|---|---|---|---|
| ⭐ Rec | Traços Interiores Arched Brass | €380 | tracosinteriores.com | 4 sem |
| 💰 Econ | IKEA HEKTAR Floor | €79 | ikea.com/pt | Stock |

---

## BUDGET RESUMO — CUIDAI HQ

| Categoria | Econ (€) | Recomendado (€) | Premium (€) |
|---|---|---|---|
| Mobiliário solto | 3.837 | 12.430 | 21.690 |
| Iluminação decorativa | 158 | 760 | 1.400 |
| Têxteis (tapete, almofadas) | 320 | 890 | 1.800 |
| Decoração + plantas | 180 | 450 | 950 |
| **Subtotal** | **4.495** | **14.530** | **25.840** |
| **Contingência 10%** | 450 | 1.453 | 2.584 |
| **TOTAL** | **€4.945** | **€15.983** | **€28.424** |

---

## TIMELINE DE ENCOMENDAS

| Item | Prazo encomenda | Lead time | Entrega prevista |
|---|---|---|---|
| Sofá Gual (10 sem) | 19 Dez 2025 | 10 sem | 28 Fev 2026 |
| Mesa AROUNDtheTREE (8 sem) | 2 Jan 2026 | 8 sem | 28 Fev 2026 |
| Cadeiras Fenabel (6 sem) | 16 Jan 2026 | 6 sem | 27 Fev 2026 |
| Mesa Branca Lisboa (6 sem) | 16 Jan 2026 | 6 sem | 27 Fev 2026 |
| Restantes itens stock | Mar 2026 | Imediato | Semana 16 Mar |

**Sequência de entrega:**
1. 28 Fev — Obra concluída, pisos e pintura secos
2. 1–5 Mar — Mobiliário estrutural (mesa reuniões, sofá, aparador)
3. 6–9 Mar — Iluminação e têxteis
4. 10–15 Mar — Decoração, plantas, arte
5. 16 Mar — Ocupação Cuidai HQ ✅
```

---

## Output anti-patterns

- Listar opções sem preço ("ver website do fornecedor para pricing actualizado") — o cliente não tem tempo para isso
- Dimensões genéricas ("sofá grande, aprox. 3m") sem confirmação de que cabem no espaço do floor plan
- Lead times vagos ("pode demorar algum tempo") sem semanas concretas ou data de encomenda calculada
- Misturar FF&E com obra: especificar cozinha embutida, roupeiros à medida ou iluminação técnica de tecto no schedule de FF&E
- Budget range demasiado amplo sem critério ("€5.000 a €50.000 dependendo das opções") — usar cenários Econ/Rec/Premium com totais reais
- Fornecedores sem localização nem contacto accionável ("marca portuguesa de qualidade, pesquisar online")
- Omitir restrições físicas de entrega — recomendar peça de 3m num apartamento com elevador de 1,2m é erro grave
- Não marcar deadline de encomenda para made-to-order — cliente fica sem móveis na mudança
