---
name: diva-diagnose
description: DIVA's universal diagnostic for architecture, design, and construction projects. Structural assessment, design potential, regulatory compliance (RGEU/RJUE), budget feasibility, timeline estimation, and 4-milestone roadmap. Triggers on "diagnose", "diagnostico", "avaliar espaco", "analise projecto", "onde comecar", "roadmap obra".
license: MIT
---

# DIVA Skill — Project Diagnostic

The universal entry point for any architecture, interior design, or construction project. Produces a structured diagnosis covering structural condition, design potential, regulatory compliance, budget feasibility, and a phased roadmap before any specialized work begins.

## When to activate

Invoke `/diva-diagnose` (or trigger automatically) when:
- User brings a new space/property to evaluate (apartment, house, commercial)
- User asks "where do I start" with a renovation or construction project
- User shares photos, floor plans, or descriptions of a space
- User wants a roadmap for a remodeling or construction project
- User mentions regulatory concerns (licensing, RGEU, RJUE)
- Start of any architecture/design project workflow

Do NOT use when:
- User already has a diagnosis and needs a specific deliverable (use diva-floor-plan, diva-materials, diva-budget)
- Request is purely about material selection or budget without project context

## Workflow

### 1. Context gathering
Collect (or infer from input) the minimum viable context:
- **Property type:** apartment (T0-T5+), moradia, commercial, mixed-use
- **Location:** concelho, freguesia (affects CML/CMO/CM* regulations)
- **Current state:** original, already renovated, in ruins, new construction
- **Area:** total m2, useful m2 (if known)
- **Year of construction:** pre-1951 (no license needed for some work), 1951-1990, post-1990
- **Ownership situation:** own, buying, inherited, rented
- **What they want:** renovation level (cosmetic/structural/total gut), new build, expansion
- **Photos/plans available:** yes/no, quality

If critical context is missing (especially property type, location, and renovation scope), stop and ask.

### 2. RAG consult (mandatory)
```
mcp__dario-rag__search_kb(query: "RGEU regulamento geral edificacoes urbanas minimum areas", limit: 5)
mcp__dario-rag__search_kb(query: "RJUE licenciamento comunicacao previa obras", limit: 5)
mcp__dario-rag__search_kb(query: "<property type> <renovation type> portugal", limit: 5)
```

### 3. Structural assessment
Evaluate (from description/photos/plans):
- **Structural system:** masonry, concrete frame, mixed, wood (pre-1755, pombalino, gaioleiro, placa, modern)
- **Visible pathologies:** cracks (structural vs cosmetic), humidity, efflorescence, deformation
- **Floors/ceilings:** wood (soalho), concrete slab, mixed
- **Walls:** load-bearing identification (critical before any demolition)
- **Roof:** condition if applicable (telha, terraço, cobertura plana)
- **Infrastructure age:** electrical (pre/post RTIEBT), plumbing (chumbo/ferro/PPR/PEX), gas

Flag anything that requires structural engineering (projeto de estabilidade).

### 4. Design potential analysis
- **Natural light:** orientation (N/S/E/W), window count and size, obstructions
- **Ceiling height:** standard 2.70m, high ceilings (>3m = design opportunity), low (<2.40m = RGEU non-compliant)
- **Flow potential:** open plan viability, circulation optimization
- **Views/outdoor space:** balcony, terrace, garden, courtyard
- **Character elements worth preserving:** azulejos, moldings, soalho original, ironwork
- **Spatial constraints:** columns, shafts, structural walls that limit layout

### 5. Regulatory compliance check (RGEU/RJUE)
- **RGEU minimums:** room dimensions, ceiling heights, ventilation, natural light (1/8 of floor area)
- **RJUE classification:** what type of procedure is needed?
  - Isenta (exempt): interior works not affecting structure/facade
  - Comunicacao previa: minor exterior changes, some interior restructuring
  - Licenciamento: structural changes, use changes, facade alterations
  - Autorizacao de utilizacao: change of use (commercial to residential, etc.)
- **PDM/PMOT:** local zoning, max height, max density, heritage zones (ARU, ACRRU)
- **Heritage constraints:** DGPC classification, zona tampao, imovel de interesse
- **Condominium rules:** if apartment, what requires condominium approval
- **EAA/accessibility:** applicable if commercial or >4 units

### 6. Prioritization
Classify every finding into exactly one bucket:
- **CRITICO** — Structural safety, legal risk, blocks all other work (load-bearing wall issues, no license when needed, electrical danger, asbestos)
- **IMPORTANTE** — Affects project viability, must be addressed in planning (RGEU non-compliance, infrastructure replacement, waterproofing)
- **OPTIMIZACAO** — Enhances quality but not blocking (better materials, smart home, energy upgrade)

### 7. Roadmap — 4 milestones
| Milestone | Phase | Focus |
|---|---|---|
| **M1 — Projecto** | 4-8 weeks | Architecture project, engineering specialties, material selection |
| **M2 — Licenciamento** | 4-16 weeks | CM submission, approval wait, contractor selection |
| **M3 — Obra** | 8-24 weeks | Construction execution, site management, quality control |
| **M4 — Entrega** | 2-4 weeks | Snag list, final inspection, habitability license, handover |

Customize durations based on project scope and municipality (Lisbon CM is slower than smaller municipalities).

### 8. Budget feasibility range
Provide a rough cost/m2 range based on scope:
- **Cosmetic refresh:** 200-400 EUR/m2
- **Medium renovation:** 500-800 EUR/m2
- **Full gut renovation:** 800-1,200 EUR/m2
- **Premium renovation:** 1,200-2,000+ EUR/m2
- **New construction:** 1,200-2,500 EUR/m2

Flag if budget expectations are misaligned with scope.

## Output template

```markdown
---
project: <client/property>
date: <YYYY-MM-DD>
type: diva-diagnostic
property_type: <type>
location: <concelho>
area_m2: <number>
construction_year: <year/decade>
confidence: <green|yellow|red>
---

# Diagnostico DIVA — <Property/Client>

## Resumo Executivo
- **Espaco:** <type, area, location>
- **Estado atual:** <condition summary>
- **Ambicao:** <what the client wants>
- **Viabilidade:** <green/yellow/red + 1 line>
- **Estimativa custo:** <range EUR/m2 x area = total range>
- **Timeline estimada:** <months>

## Avaliacao Estrutural
### Sistema construtivo
### Patologias identificadas
### Infraestruturas (eletrica/hidrosanitaria/gas)
### Elementos a preservar

## Potencial de Design
### Luz natural e orientacao
### Pe-direito e volumetria
### Fluxo e circulacao
### Espaco exterior
### Elementos de caracter

## Conformidade Regulamentar
### RGEU — Areas minimas e pe-direito
### RJUE — Tipo de procedimento necessario
### PDM/Zonamento
### Condicionantes patrimoniais
### Condominio (se aplicavel)

## Priorizacao
### CRITICO (bloqueia projecto / risco seguranca)
1. ...
### IMPORTANTE (afeta viabilidade)
1. ...
### OPTIMIZACAO (melhoria de qualidade)
1. ...

## Roadmap
### M1 — Projecto (Sem 1-8)
- [ ] ...
### M2 — Licenciamento (Sem 9-24)
- [ ] ...
### M3 — Obra (Sem 25-48)
- [ ] ...
### M4 — Entrega (Sem 49-52)
- [ ] ...

## Estimativa Orcamental
| Categoria | Range EUR |
|---|---|
| Custo/m2 estimado | X - Y |
| Area util | Z m2 |
| **Total estimado** | **A - B** |
| Honorarios projecto (~10%) | ... |
| Licenciamento | ... |
| Contingencia (10-15%) | ... |

## Proximos Passos
- [ ] Seguir com `diva-briefing` para captar necessidades detalhadas
- [ ] Seguir com `diva-floor-plan` para analise de planta
- [ ] Seguir com `diva-budget` para orcamento detalhado

## Questoes Pendentes
- <information needed from client>
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Diagnostico DIVA.md`

## Red flags — don't do this
- Never recommend demolishing walls without confirming they are not load-bearing
- Never skip regulatory check for Portuguese projects (RGEU/RJUE always apply)
- Never provide a single-number budget estimate (always a range)
- Never assume pre-1951 buildings are exempt from licensing without checking scope
- Never ignore asbestos risk in buildings from 1960-1990 (fibrocimento)
- Never forget condominium approval requirements for apartment projects
- Never skip the structural assessment even for "cosmetic" renovations

## Interactions
- Follow up with `diva-briefing` for detailed client requirements
- Follow up with `diva-floor-plan` for layout analysis
- Follow up with `diva-materials` for material specification
- Follow up with `diva-budget` for detailed budget breakdown
- Save via `dario-obsidian-save` to vault

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Contexto mínimo viável está completo

- [ ] Property type explicitado (T2/moradia/comercial — nunca "espaço" ou "imóvel")
- [ ] Localização com concelho e freguesia (não apenas "Lisboa" ou "Porto")
- [ ] Ano de construção ou intervalo identificado (afeta regime RJUE aplicável)
- [ ] Área em m² presente ou estimada com base em referência concreta
- [ ] Se contexto crítico ausente: output pede dados antes de diagnosticar

❌ NOT delivery-ready: `"A moradia localiza-se numa zona urbana de Lisboa."`
✅ Delivery-ready: `"Moradia T3 no Bairro de Alvalade, Lisboa (CML), ~140 m² brutos, construção estimada 1960-1970 (pré-placa)."`

---

### Gate 2 — Avaliação estrutural com sistema construtivo identificado

- [ ] Sistema construtivo nomeado (pombalino / gaioleiro / placa / betão armado / alvenaria moderna)
- [ ] Patologias visíveis classificadas (fissura estrutural vs cosmética, humidade, deformação)
- [ ] Infraestruturas avaliadas: elétrica (pré/pós RTIEBT), canalização (chumbo/PPR/PEX), gás
- [ ] Paredes resistentes identificadas ou flag de "requer verificação por engenheiro de estabilidade"
- [ ] Pavimento e cobertura com condição estimada (soalho original, laje, terraço plano)

❌ NOT delivery-ready: `"As paredes podem ser estruturais. A instalação elétrica parece antiga."`
✅ Delivery-ready: `"Estrutura gaioleira (pré-1930). Fissuras diagonais em cunhal — flag CRÍTICO, requer projeto de estabilidade. Canalização em chumbo — substituição obrigatória. Elétrica pré-RTIEBT (monofásica aparente, sem terra)."`

---

### Gate 3 — Compliance RGEU/RJUE com regime de procedimento definido

- [ ] Regime RJUE explicitado: isento / comunicação prévia / licenciamento / autorização de utilização
- [ ] RGEU checado nos pontos críticos: pé-direito (≥2,40 m), iluminação natural (1/8 da área), áreas mínimas
- [ ] PDM/PMOT referenciado se obra exterior ou alteração de uso
- [ ] Zonas de proteção patrimonial verificadas (ARU, DGPC, ACRRU) se localização histórica
- [ ] Condomínio ou regime de propriedade horizontal flaggeado se apartamento

❌ NOT delivery-ready: `"É necessário verificar as licenças junto da câmara municipal."`
✅ Delivery-ready: `"Obras interiores sem alteração de estrutura nem fachada → Comunicação Prévia (CML). Pé-direito de 2,35 m na cozinha existente — incumprimento RGEU art.º 65.º, requer solução técnica. Imóvel em ARU Mouraria — fachada sujeita a aprovação DGPC."`

---

### Gate 4 — Potencial de design com dados observáveis

- [ ] Orientação solar identificada (N/S/E/W) e impacto na luz natural avaliado
- [ ] Pé-direito com valor numérico (oportunidade se >3 m, problema se <2,40 m)
- [ ] Elementos de carácter listados com decisão: preservar / recuperar / remover
- [ ] Viabilidade de planta aberta avaliada face às paredes resistentes identificadas
- [ ] Constrangimentos espaciais (colunas, shafts, paredes fixas) mapeados

❌ NOT delivery-ready: `"O espaço tem bom potencial e elementos interessantes a preservar."`
✅ Delivery-ready: `"Orientação SO — salas com boa luz de tarde. Pé-direito 3,20 m → oportunidade para soppalco/mezanino. Soalho de pinho original em ~70% da área — recuperação viável. Shaft de ventilação central bloqueia abertura para open-plan total."`

---

### Gate 5 — Roadmap com durações personalizadas e orçamento fundamentado

- [ ] 4 milestones presentes (M1 Projecto / M2 Licenciamento / M3 Obra / M4 Entrega)
- [ ] Durações ajustadas ao município real (CML mais lenta que CM menor) e escopo
- [ ] Range de orçamento €/m² com categoria nomeada (cosmético / médio / total / premium)
- [ ] Alerta explícito se expectativa de cliente está desalinhada com escopo identificado
- [ ] Total estimado em EUR com intervalo (mínimo–máximo) e premissas declaradas

❌ NOT delivery-ready: `"O projeto pode demorar entre 6 meses a 1 ano e custar entre 50.000€ e 150.000€."`
✅ Delivery-ready: `"M1 6 sem / M2 12 sem (CML — histórico de atrasos) / M3 20 sem (remodelação total 120 m²) / M4 3 sem. Budget range: 800–1.000 €/m² × 120 m² = 96.000–120.000 €, excluindo honorários (10–15%) e contingência (10%)."`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets ou placeholders

- [ ] Cabeçalho YAML sem `<angle-brackets>` — todos os campos preenchidos
- [ ] Nome do cliente/projeto presente (ex: `Cuidai — Clínica Benfica`, `Família Rodrigues — T3 Alvalade`)
- [ ] Data real no formato `YYYY-MM-DD` (não `<YYYY-MM-DD>`)
- [ ] Nenhum campo deixado como template literal (`<type>`, `<number>`, `<yes/no>`)
- [ ] Classificações CRÍTICO/IMPORTANTE/OPTIMIZAÇÃO aplicadas a achados reais, não genéricos

❌ NOT delivery-ready: `project: <client/property>` / `area_m2: <number>`
✅ Delivery-ready: `project: "Família Costa — Moradia T4 Cascais"` / `area_m2: 187`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
---
project: "Atrium Boutique Offices — Piso 2, Av. da República 45, Lisboa"
date: 2025-01-28
type: diva-diagnostic
property_type: escritório / conversão residencial-para-comercial
location: Lisboa — Avenidas Novas (CML)
area_m2: 210
construction_year: 1958
---

# DIVA Diagnostic — Atrium Boutique Offices

## Resumo executivo

Fracção de 210 m² num edifício de placa dos anos 50 em zona ARU das Avenidas Novas.
Alteração de uso (habitacional → serviços) com remodelação total. Projeto viável mas com
3 condicionantes críticas que determinam cronograma e budget.

---

## 1. Avaliação estrutural

**Sistema construtivo:** Betão armado — estrutura de placa (1955–1975). Paredes de
alvenaria de tijolo furado não estruturais na maioria, exceto núcleo central de caixas de
elevador e escadas (betão).

**Patologias identificadas:**
- Fissuras horizontais em parede norte (provável assentamento diferencial) → **CRÍTICO**
  — requer inspeção de engenheiro de estabilidade antes de qualquer demolição
- Humidade ascensional na zona de WC existentes (eflorescências visíveis) → **IMPORTANTE**
- Teto falso de gesso cartonado com manchas de infiltração (cobertura plana acima) → **IMPORTANTE**

**Infraestruturas:**
- Elétrica: quadro de 1998, monofásico, subcalibers para uso de escritório intensivo — **substituição total**
- Canalização: PPR (renovada ~2010) — **reutilizável com extensões**
- AVAC: inexistente — **instalação nova obrigatória** para licença de utilização comercial
- Gás: ramal existente mas desativado

---

## 2. Potencial de design

| Atributo | Valor | Avaliação |
|---|---|---|
| Orientação | SO | ★★★★ — luz natural de tarde nas salas de reunião |
| Pé-direito | 3,10 m | ★★★★★ — permite teto técnico + instalações ocultas |
| Planta aberta | Viável em 70% | Shaft central e 2 pilares 40×40 cm condicionam layout |
| Elementos a preservar | Soalho de parquet original (60% área) | Recuperação viável — lixagem + envernizamento |
| Fachada | Caixilharia de alumínio anos 90 | Substituição recomendada (eficiência + ARU) |

**Oportunidade chave:** pé-direito de 3,10 m permite instalação técnica completa (AVAC,
cabos estruturados, sprinklers) sem comprometer altura útil mínima exigida para escritórios
(2,70 m — RGEU art.º 66.º).

---

## 3. Compliance RGEU / RJUE

**Procedimento aplicável:** Licenciamento (alteração de uso + obras estruturais em ARU)
→ submissão à CML, estimativa de aprovação: **10–14 semanas** (histórico ARU Avenidas Novas)

**RGEU — checklist:**
- [x] Pé-direito 3,10 m ≥ 2,70 m (art.º 66.º) ✅
- [x] Iluminação natural: janelas = 28 m² ≈ 13% da área útil ≥ 1/8 (12,5%) ✅
- [ ] Ventilação mecânica: obrigatória para open-space >50 m² → **projeto AVAC necessário**
- [ ] Acessibilidade EAA: edifício com elevador existente, mas WC acessível ausente → **CRÍTICO** para licença comercial

**ARU Avenidas Novas:**
- Fachada: alteração de caixilharia requer aprovação CML/DGPC
- Cor de fachada: manter paleta existente ou aprovação prévia
- Sem classificação DGPC direta — zona tampão não aplicável

---

## 4. Priorização de achados

### 🔴 CRÍTICO
1. **Fissuras em parede norte** — inspeção de estabilidade obrigatória pré-projeto
2. **WC acessível ausente** — bloqueia licença de utilização comercial (Dec.-Lei 163/2006)
3. **Quadro elétrico subdimensionado** — risco de incêndio, não conformidade para ocupação comercial

### 🟡 IMPORTANTE
4. Humidade ascensional nos WCs existentes — impermeabilização antes de revestimentos
5. Infiltração em cobertura plana — reparação antes de obra interior (condomínio responsável — acionar)
6. AVAC inexistente — projeto de especialidade obrigatório para licença

### 🟢 OPTIMIZAÇÃO
7. Substituição de caixilharia → ganho térmico/acústico + valorização imóvel
8. Recuperação de parquet original → identidade premium para boutique office
9. Automação (iluminação DALI + controlo AVAC centralizado) — viável com pé-direito disponível

---

## 5. Roadmap — 4 milestones

| Milestone | Fase | Duração estimada | Entregáveis chave |
|---|---|---|---|
| **M1 — Projeto** | Arquitetura + especialidades | **7 semanas** | Projeto de arquitetura, estabilidade, AVAC, elétrico, acessibilidades |
| **M2 — Licenciamento** | Submissão CML + aprovação | **12 semanas** | Licença de obras CML, aprovação ARU fachada, caderno de encargos |
| **M3 — Obra** | Execução | **18 semanas** | Demolições, estrutura, MEP, acabamentos, mobiliário fixo |
| **M4 — Entrega** | Vistoria + handover | **3 semanas** | Licença de utilização (serviços), telas finais, manual de manutenção |

**Total estimado: 40 semanas** (≈ 10 meses) da data de arranque do projeto.

---

## 6. Budget feasibility

**Categoria:** Remodelação total + alteração de uso + instalações novas

| Item | €/m² | Total estimado |
|---|---|---|
| Obra civil + acabamentos | 850–1.050 | 178.500–220.500 € |
| MEP (elétrico, AVAC, canalizações) | 150–200 | 31.500–42.000 € |
| **Subtotal construção** | **1.000–1.250** | **210.000–262.500 €** |
| Honorários projeto (12%) | — | 25.200–31.500 € |
| Contingência (10%) | — | 21.000–26.250 € |
| **Total projeto** | | **256.200–320.250 €** |

**Nota:** Orçamento exclui mobiliário solto e equipamentos IT/AV.
Se expectativa do cliente for <200.000 € total → **desalinhamento crítico** — renegociar
escopo antes de avançar para M1.

---

*Diagnóstico preparado por DIVA | Atrium Boutique Offices | 2025-01-28*
*Próximo passo recomendado: `/diva-floor-plan` para estudo de layouts alternativos*
```

---

## Output anti-patterns

- Usar `<angle-brackets>` no output final — o template YAML é ponto de partida, não entrega
- Escrever "é necessário verificar junto da câmara municipal" sem identificar o regime RJUE aplicável
- Fornecer range de budget sem multiplicar pelo m² real do projeto (ex: só "500–800 €/m²" sem total)
- Listar patologias sem classificação CRÍTICO/IMPORTANTE/OPTIMIZAÇÃO — o cliente não sabe o que priorizar
- Roadmap com durações fixas copiadas do template (M2 sempre "4–16 semanas") sem ajuste ao município
- Mencionar "paredes estruturais" sem identificar o sistema construtivo que determina quais o são
- Descrever potencial de design sem dados observáveis (orientação, pé-direito numérico, m² de janelas)
- Omitir flag de desalinhamento de budget quando expectativa do cliente é claramente abaixo do escopo
- Output sem nome de projeto/cliente — diagnósticos genéricos não são entregáveis
- Concluir diagnóstico sem indicar o próximo skill DIVA recomendado (`/diva-floor-plan`, `/diva-budget`, etc.)
