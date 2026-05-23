---
name: diva-moodboard
description: Moodboard generation for interior design concepts. Defines style direction, color palette with Pantone/NCS references, materials board, furniture references, lighting concept, and AI image generation prompts. Triggers on "moodboard", "mood board", "conceito", "concept board", "inspiracao", "estilo interiores", "paleta de cores".
license: MIT
---

# DIVA Skill — Moodboard / Interior Design Concept Generator

Creates a comprehensive interior design moodboard document from a client briefing. Goes beyond aesthetics to include actionable specifications: color references (Pantone/NCS), material selections with suppliers, furniture references with dimensions, lighting layering, and ready-to-use AI prompts for visual concept generation via Midjourney or DALL-E.

## When to activate

- Client provides a design brief or says "quero um conceito para..."
- Starting a new interior design project (residential or commercial)
- Client shares inspiration images and wants a cohesive direction
- Architect/designer needs to formalize style direction for team
- Preparing a concept presentation for client approval
- Client says "nao sei o que quero" -- use this to guide the conversation

## Workflow

### 1. Gather inputs

- **Space type:** living room / bedroom / kitchen / bathroom / office / restaurant / hotel / retail
- **Client profile:** age range, lifestyle, family composition
- **Preferences stated:** any styles, colors, materials mentioned
- **Anti-preferences:** "nao quero nada rustico", "odeio cinzento"
- **Budget level:** economico / medio / premium / luxo
- **Location context:** apartment in Lisboa / moradia no Algarve / escritorio no Porto
- **Existing constraints:** architectural features to keep, fixed elements (floor, structure)
- **Functional requirements:** storage needs, entertaining, work-from-home, kids, pets
- **Mood words:** (ask client to pick 3-5) acolhedor, sofisticado, minimalista, dramatico, organico, luminoso, intimo, cosmopolita, atemporal, ousado

If no mood words provided, present the list and ask client to choose.

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "interior design style direction moodboard concept", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "color palette materials specification interior", collection: "dario", limit: 5)
```

### 3. Define style direction

Select primary style + secondary influence from:

| Style | Characteristics | Best for |
|---|---|---|
| Contemporaneo Portugues | Natural materials, azulejo accents, warm neutrals, craft details | Residencial PT |
| Mediterraneo Moderno | Lime/stone textures, terracotta, linen, arched forms | Sul PT, coastal |
| Minimalista Quente | Clean lines, warm wood, soft textiles, few objects | Apartamentos urbanos |
| Mid-Century Moderno | Organic curves, teak, brass, bold accents | Apartamentos 60s-70s |
| Japandi | Japanese minimalism + Scandi warmth, wabi-sabi | Espacos pequenos |
| Industrial Refinado | Exposed elements + warm materials, metal + wood | Lofts, escritorios |
| Classico Contemporaneo | Traditional proportions, modern finishes, mouldings | Moradias, casas senhoras |
| Maximalista Curado | Pattern mixing, collected look, art-heavy, layered | Personalidades fortes |
| Biophilic | Plants, natural light, organic shapes, earth tones | Wellness, escritorios |
| Art Deco Revival | Geometric patterns, velvet, brass, jewel tones | Hoteis, restauracao |

State: "Primary: [X] with [Y] influences" and explain why this suits the client.

### 4. Build color palette

Define 5-7 colors with professional references:

| Role | Color | Pantone | NCS | Hex | Usage |
|---|---|---|---|---|---|
| Base (60%) | <name> | <PANTONE ref> | <NCS ref> | #XXXXXX | Paredes, tectos, grandes superficies |
| Secondary (25%) | <name> | <PANTONE ref> | <NCS ref> | #XXXXXX | Mobiliario grande, cortinas, tapetes |
| Accent 1 (10%) | <name> | <PANTONE ref> | <NCS ref> | #XXXXXX | Almofadas, arte, objectos decorativos |
| Accent 2 (5%) | <name> | <PANTONE ref> | <NCS ref> | #XXXXXX | Detalhes metalicos, pequenos acentos |
| Neutral dark | <name> | <PANTONE ref> | <NCS ref> | #XXXXXX | Molduras, detalhes, ancoragem visual |
| Neutral light | <name> | <PANTONE ref> | <NCS ref> | #XXXXXX | Fundos, transicoes |
| Wood tone | <name> | -- | -- | #XXXXXX | Pavimento, mobiliario em madeira |

Apply the 60-30-10 rule. Verify contrast accessibility for commercial spaces.

### 5. Materials board

Define 8-12 key materials:

| Material | Application | Finish | Reference/Supplier | Budget tier |
|---|---|---|---|---|
| Pedra natural (ex: calcario Moleanos) | Bancada cozinha, WC | Amaciado | Solancis / Marmetal | Premium |
| Ceramica (ex: Mutina Mews) | Pavimento WC | Mate | Revigrés / Margres | Medio-premium |
| Madeira (ex: carvalho europeu) | Pavimento geral | Mate, 3 demaos verniz | Jular / Wicanders | Medio |
| Metal (ex: latao escovado) | Torneiras, puxadores | Escovado | Bruma /DERA | Premium |
| Tecido (ex: linho belga) | Cortinas, almofadas | Natural | Designers Guild / Dedar | Premium |
| Papel de parede | Parede destaque | Texturado | Cole & Son / Pierre Frey | Premium |
| Microcimento | Pavimento continuo | Mate | Topcret / Microbel | Medio |
| Vidro | Divisorias, espelhos | Transparente/fumado | Vidraria local | Medio |

Include Portuguese suppliers where possible.

### 6. Furniture references

For each key piece, provide:
- **Piece name + designer/brand**
- **Dimensions (LxWxH)**
- **Material/upholstery**
- **Price range**
- **Alternative at lower price point**
- **Portuguese brand alternative** (if exists: Wewood, AROUNDtheTREE, DAM, Gualter, etc.)

### 7. Lighting concept

Layer the lighting plan:

| Layer | Purpose | Type | Example | Color temp |
|---|---|---|---|---|
| Ambiente | General illumination | Indirect cove / pendente central | Flos IC / Vibia Wireflow | 2700-3000K |
| Tarefa | Functional (ler, cozinhar) | Candeeiro mesa / suspensao direccionada | Artemide Tolomeo | 3000-3500K |
| Destaque | Art, texturas, architectural features | Spots encastrados / projetores | Modular Qbini | 2700-3000K |
| Decorativo | Mood, personalidade | Candeeiro escultura / velas | Tom Dixon Melt | 2200-2700K |
| Natural | Daylight strategy | Cortinas, espelhos, superficies reflectivas | -- | -- |

### 8. Generate AI visualization prompts

Create 3 prompts for concept visualization:

**Midjourney prompt format:**
```
Interior design photograph of [space type], [style direction], [key materials], [color palette description], [lighting mood], [key furniture pieces], [atmosphere words], professional interior photography, editorial quality, soft natural light from [direction], Canon EOS R5, 24mm lens --ar 16:9 --v 6.1 --style raw
```

**DALL-E prompt format:**
```
A photorealistic interior design photograph showing [detailed description]. The space features [materials and finishes]. Color palette centers on [colors]. Furniture includes [key pieces]. Natural light enters from [direction], creating [mood]. Professional architectural photography style.
```

Create prompts for: (a) wide shot, (b) detail/vignette, (c) atmospheric/mood shot.

## Output template

```markdown
---
project: <project name>
date: <YYYY-MM-DD>
type: moodboard
style: <primary style>
spaces: <list of spaces>
---

# Moodboard -- <Project Name>

## Conceito
> <2-3 sentence style statement capturing the essence of the concept>

## Direccao de estilo
- **Estilo primario:** <name>
- **Influencia secundaria:** <name>
- **Palavras-chave:** <3-5 mood words>

## Paleta de cores
| Funcao | Cor | Pantone | NCS | Hex | Aplicacao |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

## Materiais
| Material | Aplicacao | Acabamento | Fornecedor | Tier |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Mobiliario de referencia
| Peca | Designer/Marca | Dimensoes | Preco | Alternativa PT |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Conceito de iluminacao
| Camada | Tipo | Referencia | Temp. cor |
|---|---|---|---|
| ... | ... | ... | ... |

## Prompts para visualizacao AI

### Vista geral (Midjourney)
```
<prompt>
```

### Detalhe/vinheta (Midjourney)
```
<prompt>
```

### Atmosfera (DALL-E)
```
<prompt>
```

## Proximos passos
- [ ] Apresentar moodboard ao cliente para aprovacao
- [ ] Apos aprovacao, detalhar especificacoes por divisao
- [ ] Solicitar amostras de materiais aos fornecedores
- [ ] Gerar renders 3D com `diva-render-brief`
- [ ] Iniciar orcamentacao com fornecedores
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Project> - Moodboard.md`

## Red flags -- don't do this

- Never present a moodboard without color references (Pantone/NCS) -- "azul bonito" is not a spec
- Never mix more than 2 style directions -- coherence breaks down
- Never forget to include a budget-appropriate alternative for premium references
- Never ignore the client's anti-preferences (they remember what they hate more than what they like)
- Never specify materials without checking availability in Portugal
- Never create a lighting plan with only one layer -- always minimum 3 layers
- Never use AI prompts without specifying "interior photography" style -- otherwise get CGI look
- Never present Pantone colors without verifying they exist in the current Pantone library

## Interactions

- Follow up with `diva-render-brief` for 3D visualization briefs
- Pair with `diva-timeline` for procurement lead times in project schedule
- Follow up with `dario-proposal` for design fee proposal
- Save via `dario-obsidian-save` to vault

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Brief capturado e style direction justificado

- [ ] Space type explicitamente nomeado (living room / quarto / escritório — não "espaço")
- [ ] Perfil do cliente refletido no conceito (idade, lifestyle, composição familiar)
- [ ] Primary + secondary style nomeados com justificação ligada ao brief real
- [ ] Anti-preferências do cliente não aparecem em NENHUM elemento do moodboard
- [ ] Mood words selecionados (3-5) estão visíveis na abertura do documento

❌ NOT delivery-ready: "Optámos por um estilo contemporâneo adequado ao espaço."
✅ Delivery-ready: "Primary: Minimalista Quente com influências Japandi — escolha baseada nos mood words da Ana (acolhedor, luminoso, atemporal) e na restrição do pavimento de carvalho existente no apartamento T3 em Alvalade."

---

### Gate 2 — Paleta de cores com referências profissionais completas

- [ ] 5-7 cores definidas com roles 60/25/10/5 + neutros
- [ ] Cada cor tem Pantone E NCS e Hex (nenhuma coluna vazia)
- [ ] Aplicação descrita por superfície concreta (não "acentos" genéricos)
- [ ] Wood tone incluído se mobiliário em madeira está no projeto
- [ ] Contraste acessibilidade verificado se espaço comercial

❌ NOT delivery-ready: "Base: Off-white quente | Pantone: \<ref\> | Usage: paredes"
✅ Delivery-ready: "Base (60%) — Areia Morna | Pantone 9183 C | NCS S 1005-Y20R | #F2EAD8 | Paredes, tecto, reboco pintado sala e corredor"

---

### Gate 3 — Materials board com fornecedores e budget tier

- [ ] 8-12 materiais listados com aplicação específica (não "pavimentos em geral")
- [ ] Cada material tem fornecedor real (preferencialmente português) + alternativa se premium
- [ ] Finish especificado (mate, escovado, amaciado, polido — nunca em branco)
- [ ] Budget tier alinhado com o nível declarado no brief (economico / medio / premium / luxo)
- [ ] Nenhum material em contradição com anti-preferências ou restrições arquitectónicas

❌ NOT delivery-ready: "Pedra natural para bancadas | Fornecedor: \<supplier\> | Tier: premium"
✅ Delivery-ready: "Calcário Moleanos Amaciado | Bancada ilha cozinha + tampo WC social | Solancis Lisboa | Premium — alternativa media: Marmogres Branco Neve (Revigrés Ref. 3421)"

---

### Gate 4 — Referências de mobiliário com dimensões e alternativas PT

- [ ] Cada peça-chave tem marca/designer + dimensões LxWxH em cm
- [ ] Faixa de preço indicada (€ range, não "a consultar")
- [ ] Alternativa lower-price-point incluída para cada peça premium
- [ ] Alternativa de marca portuguesa presente onde aplicável (Wewood / AROUNDtheTREE / DAM / Gualter)
- [ ] Dimensões verificadas contra planta ou área declarada no brief

❌ NOT delivery-ready: "Sofá modular | Marca: \<brand\> | Alternativa: modelo mais acessível"
✅ Delivery-ready: "Sofá Modular Muuto Connect | 280×160×H72 cm | Lã boucle creme | €3.800–4.200 | Alternativa PT: AROUNDtheTREE Laia Sectional em linho natural, €1.900"

---

### Gate 5 — Conceito de iluminação em camadas com temperatura de cor

- [ ] 3 camadas mínimas (ambiente + tarefa + decorativa/accent)
- [ ] Cada camada tem exemplo de produto real com marca + modelo
- [ ] Temperatura de cor definida em Kelvin para cada camada
- [ ] Nota sobre regulação (dimmer / DALI / on-off) se espaço o exige
- [ ] Coerência estilística: luminárias alinhadas com style direction e paleta metálica

❌ NOT delivery-ready: "Iluminação ambiente: pendente central | 3000K | \<marca\>"
✅ Delivery-ready: "Camada Ambiente — Cove LED indirecto perimetral 2700K + Flos IC Light S1 Ø52cm latão fosco sobre mesa de jantar, dimmer Lutron; Tarefa — Vibia Nude Table 5320 leitura 3000K junto ao sofá"

---

### Gate 6 — Prompts IA prontos a usar e output sem placeholders

- [ ] Mínimo 2 prompts (Midjourney + DALL-E) com style tags e referências de cor reais
- [ ] Prompts incluem aspect ratio, v-number ou quality flags aplicáveis
- [ ] Zero ângulos com `<placeholder>`, `[INSERIR]` ou campos por preencher
- [ ] Nome do cliente / projeto aparece no título e na abertura do documento
- [ ] Todos os dados (datas, referências, fornecedores, preços) são verificáveis e não inventados

❌ NOT delivery-ready: "Midjourney prompt: \<interior style\>, \<color palette\>, \<mood\> --ar 16:9"
✅ Delivery-ready: "**MJ:** `warm minimalist Portuguese apartment living room, oak floor, Pantone 9183 C walls, brushed brass accents, linen sofa, morning light, editorial photography --ar 16:9 --v 6.1 --style raw` | **DALL-E:** `Interior design render, japandi warm minimalist, NCS S1005-Y20R plaster walls, teak furniture, wabi-sabi textures, soft diffuse natural light, architectural digest quality`"

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Moodboard — Apartamento Cuidai Founders Suite | Lisboa, Chiado
**Cliente:** Cuidai — Espaço de acolhimento e reunião para equipa fundadora
**Data:** Junho 2025 | **Nível:** Premium | **Espaço:** Open-plan office-lounge, 48 m²

---

## Style Direction
**Primary: Biophilic** com influências **Contemporâneo Português**
Justificação: A missão da Cuidai (cuidado, bem-estar, humanização da saúde) pede um espaço que
transmita calma activa. Os mood words seleccionados pela equipa — acolhedor, luminoso, orgânico,
atemporal, sofisticado — apontam inequivocamente para formas naturais, materiais vivos e luz
generosa. A herança portuguesa ancora o espaço à identidade da marca sem cair no clichê.

---

## Paleta de Cores

| Role | Cor | Pantone | NCS | Hex | Aplicação |
|---|---|---|---|---|---|
| Base (60%) | Branco Calcário | 9180 C | S 0804-Y20R | #F7F3EC | Paredes, tecto, reboco pintado |
| Secondary (25%) | Verde Salva | 16-0430 TCX | S 3020-G30Y | #8A9E72 | Estante modular, parede destaque |
| Accent 1 (10%) | Terracota Suave | 16-1438 TCX | S 3030-Y50R | #C98060 | Almofadas, vasos cerâmica, arte |
| Accent 2 (5%) | Latão Natural | 14-0846 TCX | S 2030-Y10R | #C9A84C | Puxadores, candeeiros, detalhes |
| Neutral Dark | Grafite Quente | 19-0303 TCX | S 7005-Y50R | #3D3A35 | Molduras, pernas mobiliário |
| Neutral Light | Areia Fina | 9183 C | S 1005-Y20R | #EDE8DC | Fundos, transições, têxteis |
| Wood Tone | Carvalho Médio | — | — | #A0714F | Pavimento, mesa, estante |

Regra 60-30-10 aplicada. Contraste branco/grafite: ratio 12:1 (WCAG AAA ✓).

---

## Materials Board

| Material | Aplicação | Acabamento | Fornecedor | Tier |
|---|---|---|---|---|
| Calcário Vidraço Português | Tampo mesa reunião + recepção | Amaciado | Solancis, Lisboa | Premium |
| Carvalho Europeu 14cm | Pavimento geral | Mate, 3 demãos verniz natural | Jular Madeiras Porto | Médio |
| Azulejo Artesanal 15×15 | Parede destaque entrada | Vidrado branco c/ borda crua | Viúva Lamego, Lisboa | Premium |
| Linho Belga Natural | Cortinas piso-tecto + almofadas | Natural não tratado | Designers Guild ref. F2242/03 | Premium |
| Microcimento Cinza Quente | Ilha central multiusos | Mate selado | Topcret Evoluttion EV-07 | Médio |
| Latão Escovado | Candeeiros, puxadores, suportes | Escovado anti-risco | Bruma Acabamentos, Porto | Premium |
| Cerâmica Margres Concept | WC e kitchenette | Mate 60×60 | Margres ref. 6CT6M | Médio |
| Musgo Estabilizado + Plantas | Parede verde vertical 2×1m | Vivo (rega automática) | Verdical, Lisboa | Premium |
| Tela de Linho Cru | Tecto acústico suspenso | Bruto | Vicaima Acústica | Médio |
| Vidro Fumado Bronze | Divisória lounge/reunião | 10mm laminado | Vidraria Lisbonense | Médio |

---

## Referências de Mobiliário

**Mesa de Reunião**
Wewood Join Table Oval | 220×100×H74 cm | Carvalho natural | €2.100–2.400
Alt. económica: Ethnicraft Bok Table (carvalho, €1.650)

**Sofá Lounge**
Muuto Outline Sofa 3-seater | 220×86×H71 cm | Lã boucle areia | €3.200–3.600
Alt. PT: AROUNDtheTREE Duna Sofa em linho natural cru, 210cm, €1.750

**Cadeiras Reunião (×6)**
HAY About a Chair AAC12 | 52×47×H80 cm | Polipropileno off-white, pernas carvalho | €280 un.
Alt. PT: DAM Cadeira Slow em carvalho e linho, €220 un.

**Estante Modular Parede**
String Furniture System | 200×30×H200 cm | Verde salva RAL + prateleiras carvalho | €890
Alt.: IKEA Kallax repintado + tampos carvalho Jular (DIY premium), €340

**Candeeiro de Pé Lounge**
Flos Arco Floor | H250 cm | Mármore base, arco aço, difusor opal | €2.900
Alt.: Anglepoise Type 75 Giant Floor, €680

---

## Conceito de Iluminação

| Camada | Propósito | Produto | Temp. Cor | Controlo |
|---|---|---|---|---|
| Ambiente | Iluminação geral suave | LED cove perimetral indirecto | 2700K | Dimmer Lutron |
| Focal | Destaque mesa reunião | Vibia Wireflow Round 4-mod. Ø100 latão | 3000K | Dimmer |
| Tarefa | Leitura + trabalho lounge | Artemide Tolomeo Tavolo, 2 un. | 3000K | Interruptor local |
| Decorativa | Parede verde + arte | Spot LED embutido GU10 2W orientável | 2700K | Circuito separado |
| Natural | Maximizar luz diurna | Cortinas linho piso-tecto, trilho oculto | — | Manual |

---

## Prompts IA

**Midjourney:**
`biophilic Portuguese office lounge, Pantone 9180C plaster walls, NCS S3020-G30Y modular shelf,
oak floors, brushed brass details, terracotta accents, linen curtains floor to ceiling, vertical
moss wall, Muuto sofa, soft morning diffuse light, editorial architecture photography,
Architectural Digest quality --ar 16:9 --v 6.1 --style raw --q 2`

**DALL-E 3:**
`Interior design photorealistic render, biophilic warm contemporary Portuguese workspace,
white limestone walls (#F7F3EC), sage green accent wall (#8A9E72), medium oak wood floor,
natural linen textiles, brushed brass fixtures, terracotta ceramic pots, vertical garden panel,
oval meeting table in oak, soft diffuse northern light, 48sqm open plan, ultra detailed,
architectural digest style`
```

---

## Output anti-patterns

- **Pantone/NCS em branco ou com `<ref>`** — cada cor precisa de código real; se incerto, usar o mais próximo verificável e assinalar "aprox."
- **Fornecedores genéricos** ("loja de materiais local", "marca a confirmar") sem alternativa concreta — sempre incluir pelo menos um fornecedor português nomeado
- **Dimensões de mobiliário ausentes** — "sofá grande" não é especificação; LxWxH é obrigatório mesmo que estimado
- **Style direction sem ligação ao brief** — "escolhemos minimalista porque é elegante" não conecta aos mood words nem às restrições reais do cliente
- **Prompts IA com placeholders** — um prompt com `<color>` ou `<style>` é inutilizável; deve poder ser colado directamente no Midjourney
- **Anti-preferências do cliente presentes no output** — se o cliente disse "odeio cinzento", nenhum elemento da paleta, materiais ou mobiliário pode ser cinzento
- **Budget tier inconsistente** — especificar Flos Arco + Mutina + Pierre Frey num brief "económico" sem alternativas é um erro de leitura do brief
- **Camadas de iluminação incompletas** — entregar apenas "candeeiro central + spots" sem temperatura de cor ou sistema de controlo não é conceito de iluminação
- **Wood tone sem Hex** — mesmo sem Pantone/NCS formal, a referência cromática da madeira precisa de Hex para garantir coerência na paleta digital
