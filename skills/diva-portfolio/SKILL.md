---
name: diva-portfolio
description: "Generate a professional case study / portfolio page from a completed architecture or design project. Includes before/after, concept, materials, budget summary, timeline, team, and client testimonial. Output as Markdown or HTML for website/social. Triggers on \"portfolio\", \"case study\", \"projecto concluido\", \"showcase\", \"publicar projecto\", \"antes depois\", \"portfolio entry\"."
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# DIVA Portfolio — Project Case Study Generator

Transform a completed project into a professional case study for portfolio, website, social media, or publication submission.

## When to activate

Invoke `/diva-portfolio` when:
- Project is complete and client approved for publication
- User wants to showcase work on website or social
- User preparing submission for design award/publication
- User building portfolio for new client pitch

## Workflow

### 1. Gather project data
Search all sources:
```
mcp__dario-rag__search_kb(query: "<project name>", collection: "diva", limit: 10)
```
Check agent memory, Obsidian vault outputs, briefing, moodboard, renders.

### 2. Structure the case study

**A. Hero Section**
- Project name + location
- Typology (remodelacao T3 / moradia nova / hotel boutique)
- Area (m2)
- Year completed
- 1 hero image/render (or Midjourney prompt to generate)

**B. The Brief**
- What the client wanted (3-5 bullets)
- Key challenges identified
- Budget range (if client approves sharing)

**C. The Concept**
- Design direction chosen (style + designer reference)
- Key design decisions and why
- Moodboard reference (if exists)

**D. Before & After** (if renovation)
- Before: description of original state
- Challenges: patologias, layout issues, regulatory constraints
- After: transformation highlights
- (Photo pairs if available, or Midjourney prompts for conceptual before/after)

**E. Design Details**
Room-by-room or area-by-area highlights:
- Key material choices with brand/reference
- Lighting concept
- Furniture selections
- Custom elements (carpintaria, serralharia)
- Colour palette with hex codes

**F. Technical Highlights**
- Structural interventions (if any)
- MEP innovations (piso radiante, domotica, solar)
- Energy certification achieved (classe)
- Sustainability features

**G. The Numbers**
| Metrica | Valor |
|---|---|
| Area intervencionada | X m2 |
| Duracao obra | X meses |
| Orcamento final | EUR X (se autorizado) |
| Valorizacao estimada | +X% |

**H. Team**
- Arquitecto:
- Designer interiores:
- Empreiteiro:
- Fotografo:

**I. Client Testimonial**
Template para pedir ao cliente:
"O que mais gostou no processo? O que mais o surpreendeu no resultado? Recomendaria?"

### 3. Generate outputs

**Format 1: Markdown (Obsidian/Blog)**
Complete case study in markdown with frontmatter.

**Format 2: HTML (Website/Social)**
Use `mcp__aidesigner__generate_design` para criar:
- Landing page visual do case study
- Grid layout com imagens + texto
- Responsive, pronto para website

**Format 3: Instagram Carousel**
10 slides texto para Instagram:
1. Hero image + nome projecto
2. O desafio
3. O conceito
4. Antes (se aplicavel)
5. Depois — sala
6. Depois — cozinha
7. Depois — WC
8. Detalhe material
9. Os numeros
10. CTA ("Quer transformar o seu espaco?")

**Format 4: Award Submission**
Estrutura para submissao a premios:
- Project description (500 words)
- Design intent
- Innovation/sustainability
- Technical data
- Image selection guide

## Output template

```markdown
---
project: <nome>
date: <YYYY-MM-DD>
type: portfolio
location: <morada>
area_m2: <N>
year: <YYYY>
style: <direccao>
designer_ref: <designer squad>
tags: [portfolio, case-study, <tipo>]
---

# [Project Name] — [Location]

> [One-line tagline that captures the essence]

## The Brief
[3-5 bullets]

## The Concept
[Design narrative — 150-200 words]

## Design Highlights

### [Room/Area 1]
[Description + materials + key decisions]

### [Room/Area 2]
[...]

## Materials Palette
| Material | Application | Reference |
|---|---|---|
| [pavimento] | [sala] | [marca + referencia] |

## The Numbers
| | |
|---|---|
| Area | X m2 |
| Duracao | X meses |
| Equipa | [nomes] |

## Photography
[Credits + image descriptions for social/web]
```

## Save location
- Obsidian: `05 - Claude - IA/Outputs/YYYY-MM-DD - [Projecto] - Portfolio Case Study.md`
- HTML: `[projecto]-portfolio.html`

## Red flags
- NUNCA publicar sem autorizacao escrita do cliente
- NUNCA revelar orcamento sem aprovacao
- NUNCA usar fotos sem creditos ao fotografo
- SEMPRE pedir testimonial antes de publicar
- SEMPRE verificar se ha acordo de confidencialidade

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Autorização e dados verificados antes de qualquer publicação

- [ ] Existe confirmação escrita do cliente para publicação (referenciada no output)
- [ ] Orçamento: indicado APENAS se autorizado, com nota explícita "publicação aprovada pelo cliente"
- [ ] Fotógrafo creditado por nome/studio; sem imagens de stock apresentadas como do projecto
- [ ] NDA ou acordo de confidencialidade verificado (mencionado ou descartado explicitamente)

❌ NOT delivery-ready: `"Orçamento: €X (se autorizado)"` — placeholder sem resolução  
✅ Delivery-ready: `"Orçamento total: €187.000 — publicação autorizada por Ana Costa, email 14 Jan 2025"` ou `"Orçamento: omitido a pedido do cliente (email 09 Fev 2025)"`

---

### Gate 2 — Hero section com dados reais e completos

- [ ] Nome do projecto não genérico (não "Projecto X" ou `<nome>`)
- [ ] Localização real (pelo menos cidade/freguesia, ex: "Príncipe Real, Lisboa")
- [ ] Tipologia + área m² + ano de conclusão preenchidos com números concretos
- [ ] Tagline de uma linha captura a identidade do projecto (não é uma frase-template)

❌ NOT delivery-ready: `"# [Project Name] — [Location]"` ou `"> [One-line tagline that captures the essence]"`  
✅ Delivery-ready: `"# Casa Mouraria 42 — Mouraria, Lisboa"` + `"> Uma T2 de 1910 transformada em loft contemporâneo sem apagar 114 anos de história"`

---

### Gate 3 — Narrativa de conceito e brief com substância real

- [ ] Brief tem 3-5 bullets com pedidos reais do cliente (não genéricos)
- [ ] Conceito tem 150-200 palavras com direcção de estilo nomeada + designer de referência específico
- [ ] Decisões de design justificadas ("escolhemos X porque Y", não apenas "escolhemos X")
- [ ] Se renovação: estado original descrito com problemas concretos (ex: "laje rebaixada a 2,30m, cozinha fechada de 7m²")

❌ NOT delivery-ready: `"O cliente queria um espaço moderno e funcional"` — sem especificidade  
✅ Delivery-ready: `"Cliente queria: (1) abrir cozinha para sala preservando IVV; (2) suite com WC encastrado em 12m²; (3) paleta neutra, sem branco puro — referência fornecida: Axel Vervoordt Wabi"`

---

### Gate 4 — Paleta de materiais e detalhes técnicos com referências verificáveis

- [ ] Tabela de materiais preenchida: material + aplicação + marca/referência real (não `[marca + referencia]`)
- [ ] Pelo menos 1 elemento técnico especial documentado (piso radiante, domotica, classe energética, etc.)
- [ ] Código hex da paleta de cores incluído (mínimo 3 cores)
- [ ] Elementos custom (carpintaria, serralharia) descritos com dimensão ou detalhe diferenciador

❌ NOT delivery-ready: `"Pavimento: madeira natural | Sala | [marca + referência]"`  
✅ Delivery-ready: `"Pavimento: carvalho europeu fumado 180mm | Sala + corredor | Bauwerk Colour 'Frei' | #6B5B47"`

---

### Gate 5 — The Numbers e Team sem vazios

- [ ] Tabela de números completa: área, duração obra, equipa — sem células vazias ou "X meses"
- [ ] Valorização estimada: incluída COM fonte/método ou explicitamente omitida com razão
- [ ] Equipa: pelo menos arquitecto + empreiteiro nomeados (nome real ou "confidencial a pedido do cliente")
- [ ] Data de conclusão real no frontmatter (não `YYYY-MM-DD`)

❌ NOT delivery-ready: `"Duração obra: X meses"` / `"Valorização estimada: +X%"` — literais do template  
✅ Delivery-ready: `"Duração obra: 11 meses (Abr 2024 – Mar 2025)"` / `"Valorização: +22% vs. avaliação pré-obra (fonte: avaliação bancária Fev 2025)"`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets ou placeholders

- [ ] Zero ocorrências de `<nome>`, `<morada>`, `<N>`, `[...]`, `[Project Name]`, `[Location]` no output final
- [ ] Frontmatter YAML completamente preenchido com valores reais
- [ ] Tags incluem tipologia real (ex: `remodelacao-t2`, `moradia-nova`, `hotel-boutique`)
- [ ] Save path tem data real + nome real do projecto (ex: `2025-03-18 - Casa Mouraria 42 - Portfolio Case Study.md`)

❌ NOT delivery-ready: `project: <nome>` / `location: <morada>` / `tags: [portfolio, case-study, <tipo>]`  
✅ Delivery-ready: `project: "Casa Mouraria 42"` / `location: "Mouraria, Lisboa"` / `tags: [portfolio, case-study, remodelacao-t2, lisboa]`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / memória / dados do cliente
- 🟡 **assumed** — plausível mas necessita confirmação do cliente antes de publicar
- 🟢 **projection** — previsão por design (não verificável à data de publicação)

Output checklist upfront mostra ao leitor exactamente o que é trust-as-is vs. precisa verificar. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready:
```
Área intervencionada: 142 m2 | Duração da obra: 8 meses | Valorização estimada: +18%
Empreiteiro: Construções Silva Lda | Testemunho cliente: "Adorámos o resultado."
```
*(sem labels — o reader assume que tudo é verified; orçamento ou testemunho podem nunca ter sido aprovados)*

✅ Delivery-ready:
```
- 🔵 Área intervencionada: 142 m2 (confirmado planta final assinada)
- 🔵 Equipa — Arquitecto: Diva Studio; Fotógrafo: João Matos (@jmfoto)
- 🟡 Duração da obra: 8 meses (indicado pelo cliente verbalmente — aguarda confirmação escrita)
- 🟡 Orçamento final: EUR 95.000 (cliente ainda não aprovou divulgação)
- 🟡 Testemunho: "Adorámos o resultado." (WhatsApp informal — aguarda versão aprovada para publicação)
- 🟢 Valorização estimada: +18% (projecção de mercado; não auditada por perito)
- 🟢 Retorno sobre investimento ao fim de 5 anos: indicativo, baseado em benchmark local
```

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados (substituir assumptions com dados reais aprovados)
- [ ] Todas as fontes 🔵 referenciadas no output (planta, contrato, ficheiro de sessão)
- [ ] Todas as projecções 🟢 comunicadas ao cliente como estimativas, não garantias
- [ ] Testemunho recebido por escrito e aprovado para publicação
- [ ] Orçamento: cliente assinou autorização de divulgação (ou campo removido do output)
- [ ] Fotografias: créditos verificados e fotógrafo autorizado uso no canal de destino

## Fully-worked A-tier example (delivery-ready reference)

```markdown
---
project: "Casa Príncipe Real 78"
date: 2025-03-18
type: portfolio
location: "Príncipe Real, Lisboa"
area_m2: 94
year: 2024
style: "contemporâneo orgânico"
designer_ref: "Axel Vervoordt + Vincent Van Duysen"
tags: [portfolio, case-study, remodelacao-t3, lisboa, principe-real]
client_approved: true
client_approval_ref: "email Marta Figueiredo 02 Mar 2025"
---

# Casa Príncipe Real 78 — Príncipe Real, Lisboa

> Um T3 de 1934 despido até à estrutura e recomposto em torno da luz que sempre existiu, mas nunca foi deixada entrar.

## The Brief

- Remover três divisórias interiores para criar sala-cozinha integrada de 42m²
- Manter tecto de estuque original do corredor (cota 3,10m) como elemento nobre
- Suite principal com closet encastrado em parede de betão aparente — sem portas visíveis
- Paleta total de neutros quentes; referência explícita da cliente: apartamento Rijksmuseum de Piet Boon
- Orçamento fechado: €210.000 (publicação autorizada pela cliente)

## The Concept

A intervenção partiu de uma lógica de subtracção: em vez de acrescentar, removemos tudo o que impedia
a casa de ser o que a sua estrutura pedia. As paredes interiores da década de 1970 — uma adição
infeliz — escondiam um pé-direito de 3,40m na sala e uma janela de sacada voltada a poente que
mal se via. Retiradas essas camadas, surgiu o projecto.

A direcção estética segue Axel Vervoordt na relação entre rugosidade e refinamento: betão
desempenado a lado de linho natural; ferro preto mate em caixilharia nova com perfil de 38mm;
pavimento contínuo de microcimento Mortex em toda a área social. O resultado é uma casa que
parece ter sempre sido assim — o sinal mais certo de que o trabalho correu bem.

## Design Highlights

### Sala + Cozinha (42 m²)
Piso contínuo Mortex cor 'Ash Grey' (#8C8378) elimina transições visuais. Ilha de cozinha em
betão polido com tampo de quartzite 'Taj Mahal' 20mm (Antolini). Armários lacados em tom
'Jotun Burlywood 2287' — uma leitura da pedra, não um branco.

### Suite Principal (18 m²)
Parede de closet em betão aparente texturado com sistema de calha oculta Häfele Slido.
Portadas de madeira de carvalho fumado sem puxadores (abertura por toque). WC encastrado
resolvido com parede de gesso curvo que não toca o tecto — efeito de volume flutuante.

### Casa de Banho Social (6 m²)
Parede inteira em mármore Estremoz 'Rosado' em lâminas horizontais 600×1200mm com veio
corrido (bookmatched). Torneiras Fantini 'Aboutwater' by Boffi. Lavatório de encastrar
Cielo 'Fluid' em cerâmica bruta.

## Materials Palette

| Material | Aplicação | Referência | Cor/Código |
|---|---|---|---|
| Mortex microcimento | Pavimento social + WC | Beal Mortex 'Ash Grey' | #8C8378 |
| Carvalho europeu fumado | Suite + quartos | Bauwerk Colour 'Frei' 180mm | #5C4B3A |
| Betão aparente texturado | Parede closet | Execução in-situ, textura juta | — |
| Quartzite 'Taj Mahal' | Ilha cozinha | Antolini, 20mm polido | natural |
| Mármore Estremoz Rosado | WC social | Moleanos & Filhos, bookmatched | natural |
| Ferro preto mate | Caixilharia nova | Perfil 38mm, tratamento epóxi | RAL 9005M |

## Technical Highlights

- **Estrutura:** remoção de 3 paredes com colocação de perfis HEB 140 + HEB 100
- **MEP:** piso radiante eléctrico Thermaflex em suite e WC social
- **Domótica:** sistema KNX básico (iluminação + estores) com app Gira
- **Classe energética:** B+ (certificado SCE n.º SCE-QD-123847, Dez 2024)
- **Caixilharia:** alumínio Cortizo 4500 com corte térmico, vidro duplo 6/16/6 Low-E

## The Numbers

| Métrica | Valor |
|---|---|
| Área intervencionada | 94 m² |
| Duração obra | 9 meses (Mar – Nov 2024) |
| Orçamento final | €210.000 (aprovado para publicação) |
| Valorização estimada | +31% vs. avaliação pré-obra (Caixa Geral, Jan 2025) |
| Classe energética | B+ |

## Team

| Função | Nome |
|---|---|
| Arquitecta responsável | Diva Antunes |
| Empreiteiro geral | Construções Palmeira & Filhos, Lda. |
| Serralharia custom | Ferro & Arte — João Marques |
| Carpintaria | Atelier Mogno — Ricardo Esteves |
| Fotografia | © Ivo Tavares Studio |

## Client Testimonial

> "Entregámos uma casa que nunca nos tinha convencido e recebemos de volta algo que não sabíamos
> que queríamos — mas que agora não consigo imaginar de outra forma. A Diva ouviu o que não
> conseguimos dizer."
> — Marta Figueiredo, proprietária, Fevereiro 2025

---
*Publicação autorizada por escrito pela cliente (email 02 Mar 2025). Fotografia © Ivo Tavares Studio — uso editorial condicionado a crédito.*
```

---

## Output anti-patterns

- Entregar output com qualquer `<placeholder>` ou `[campo]` por preencher — é um template devolvido, não um case study
- Mencionar orçamento sem nota de autorização explícita do cliente com data e forma de confirmação
- Escrever "Design moderno e funcional" ou "o cliente queria uma casa bonita" — taglines sem identidade não vendem portfólio
- Tabela de materiais sem marcas reais: `"pedra natural | casa de banho | pedreira local"` é inútil para diferenciação
- Omitir crédito fotográfico ou apresentar renders Midjourney como fotografia real sem disclaimer
- Instagram carousel com slides 4–7 todos a dizer "Depois — [divisão]" sem copy diferenciador por slide
- Frontmatter YAML com `date: YYYY-MM-DD` ou `year: YYYY` — são literais do template, não dados
- Case study sem testimonial nem nota explicando porque está ausente (em revisão / cliente recusou / projecto confidencial)
- "Valorização estimada: +X%" sem fonte — é afirmação de marketing sem substância; omitir ou citar fonte bancária/avaliador
- Publicar antes de verificar NDA — RED FLAG que o skill indica mas o output deve confirmar ter verificado
