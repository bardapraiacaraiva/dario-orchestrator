---
name: diva-briefing
description: Structured client briefing template for architecture, interior design, and construction projects. Captures lifestyle, needs, desires, budget, timeline, style preferences, technical constraints, and regulatory situation. Triggers on "briefing", "brief", "requisitos", "o que o cliente quer", "captar necessidades".
license: MIT
---

# DIVA Skill — Client Briefing

Structured interview and document generator that captures everything needed to start an architecture, interior design, or construction project. Transforms a conversation into a complete, actionable briefing document that serves as the single source of truth for the entire project.

## When to activate

Invoke `/diva-briefing` (or trigger automatically) when:
- User is starting a new project and needs to capture client requirements
- User says "the client wants..." and needs structure
- After a `diva-diagnose` confirms viability, to detail the brief
- User needs a template to send to a client for self-completion
- User is preparing for a first client meeting

Do NOT use when:
- Project already has a complete brief and needs execution
- User needs only a budget or floor plan (use specific skills)
- It's a purely technical question with no client context

## Workflow

### 1. Identify briefing mode
- **Interactive:** Claude asks questions one section at a time, adapts follow-ups
- **Template:** Generate a blank briefing document for the client to fill
- **From notes:** User pastes meeting notes/messages, Claude structures them into the briefing format

Ask which mode the user prefers. Default to interactive if unclear.

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "architecture briefing client requirements questionnaire", limit: 5)
mcp__dario-rag__search_kb(query: "interior design style preferences lifestyle analysis", limit: 5)
```

### 3. Section A — Identificacao do projecto
- **Client name(s):** who are the decision makers
- **Property address:** full address or location description
- **Property type:** apartment, house, commercial, mixed
- **Current use vs intended use:** residential, commercial, tourism (AL), mixed
- **Ownership:** owned, buying (CPCV signed?), inherited, rented (landlord approval?)
- **Project scope:** cosmetic, medium renovation, full gut, new build, extension
- **Key dates:** possession date, desired completion, hard deadlines (wedding, baby, lease end)

### 4. Section B — Quem vai viver/trabalhar no espaco
- **Household composition:** adults, children (ages), pets, elderly, visitors frequency
- **Daily routines:** morning flow, cooking habits, work-from-home, entertainment
- **Special needs:** mobility, allergies, sensory sensitivities, home office requirements
- **Storage needs:** wardrobes, pantry, garage, hobby storage, seasonal items
- **Future changes:** planning children, aging in place, possible sale in X years

### 5. Section C — Estilo e preferencias
- **Style direction:** modern, contemporary, classico, rustico, industrial, minimalista, mediterraneo, nordico, eclectico
- **Reference images:** ask for Pinterest boards, Instagram saves, magazine clippings
- **Color preferences:** warm/cool palette, specific colors loved/hated
- **Material preferences:** wood (type), stone (type), metal, glass, textiles
- **Lighting mood:** bright and airy, cozy and warm, dramatic, task-oriented
- **Must-haves:** specific elements they dream about (island kitchen, walk-in closet, freestanding bath, fireplace)
- **Absolutely-not:** things they hate or refuse (carpet, wallpaper, open shelving, etc.)

### 6. Section D — Programa funcional (room by room)
For each space, capture:
- **Function:** primary and secondary uses
- **Priority:** essential, desired, nice-to-have
- **Specific requirements:** dimensions, equipment, fixtures
- **Adjacency:** what should be near/far from this space

Standard rooms to cover:
- Entrada/hall
- Sala de estar
- Sala de jantar (or combined)
- Cozinha (open/closed, gas/induction, dishwasher, laundry in kitchen?)
- Suite principal (ensuite requirements)
- Quartos adicionais (function: child, guest, office)
- Casa(s) de banho (bath vs shower, double vanity, bidet)
- Lavandaria/tratamento de roupa
- Arrumos/despensa
- Espaco exterior (varanda, terraco, jardim)
- Garagem/estacionamento
- Home office/estudio
- Other: gym, cinema, wine cellar, etc.

### 7. Section E — Orcamento e prioridades
- **Total budget:** range (min-max), including or excluding fees/furniture
- **Budget breakdown awareness:** do they understand the split (construction vs finishes vs furniture vs fees)?
- **Priority allocation:** where to spend more vs where to save
  - "Invest in kitchen, save on secondary bathroom"
- **Furniture situation:** keeping existing? buying new? mix?
- **Appliance preferences:** brands, built-in vs freestanding
- **Payment capacity:** phased payments? financing? all cash?

### 8. Section F — Condicionantes tecnicas e legais
- **Known structural issues:** from diva-diagnose or own knowledge
- **Infrastructure state:** electrical, plumbing, gas, HVAC
- **Condominium rules:** if apartment, known restrictions
- **Heritage/conservation:** is the building classified?
- **Energy goals:** energy certificate improvement, solar panels, heat pump
- **Smart home:** automation level desired (none, basic, full)
- **Security:** alarm, CCTV, reinforced door, safe

### 9. Section G — Gestao do projecto
- **Decision process:** one person decides, couple, family, committee
- **Communication preference:** email, WhatsApp, video calls, in-person
- **Involvement level:** hands-off (trust the designer), collaborative, very hands-on
- **Previous renovation experience:** first time, experienced, bad past experience
- **Contractor preference:** client has one, needs recommendation, open
- **Living situation during works:** staying, moving out, partial occupation

### 10. Consolidation and validation
- Summarize all captured information
- Highlight gaps or contradictions ("you want premium finishes but budget suggests medium tier")
- Flag unrealistic expectations early
- Confirm priorities ranking with client

## Output template

```markdown
---
project: <client/property>
date: <YYYY-MM-DD>
type: diva-briefing
client: <name>
property: <address/description>
scope: <cosmetic|medium|full-gut|new-build>
budget_range: <min-max EUR>
---

# Briefing DIVA — <Client Name> — <Property>

## A. Identificacao do Projecto
| Campo | Detalhe |
|---|---|
| Cliente | ... |
| Morada | ... |
| Tipologia | ... |
| Uso atual / pretendido | ... |
| Propriedade | ... |
| Ambito | ... |
| Data pretendida conclusao | ... |

## B. Perfil do Utilizador
### Composicao do agregado
### Rotinas diarias
### Necessidades especiais
### Armazenamento
### Evolucao futura

## C. Estilo e Preferencias
### Direcao estilistica
### Referencias visuais
### Paleta de cores
### Materiais preferidos
### Must-haves
### Absolutely-not

## D. Programa Funcional
| Espaco | Funcao | Prioridade | Requisitos especificos |
|---|---|---|---|
| Entrada | ... | Essencial | ... |
| Sala | ... | ... | ... |
| Cozinha | ... | ... | ... |
| Suite | ... | ... | ... |
| Quartos | ... | ... | ... |
| WC | ... | ... | ... |
| Lavandaria | ... | ... | ... |
| Exterior | ... | ... | ... |

## E. Orcamento
| Componente | Range EUR |
|---|---|
| Obra | ... |
| Acabamentos premium | ... |
| Mobiliario | ... |
| Honorarios | ... |
| **Total** | **...** |
### Prioridades de investimento

## F. Condicionantes
### Estruturais
### Infraestruturas
### Legais/condominio
### Energia e sustentabilidade
### Domonica/smart home
### Seguranca

## G. Gestao
| Aspecto | Detalhe |
|---|---|
| Decisor(es) | ... |
| Comunicacao | ... |
| Envolvimento | ... |
| Experiencia anterior | ... |
| Empreiteiro | ... |
| Habitacao durante obra | ... |

## Sintese e Validacao
### Pontos fortes do briefing
### Gaps a esclarecer
### Contradicoes identificadas
### Expectativas a gerir

## Proximos Passos
- [ ] Cliente valida este briefing
- [ ] Seguir com `diva-floor-plan` para estudo de layout
- [ ] Seguir com `diva-materials` para paleta de materiais
- [ ] Seguir com `diva-budget` para orcamento detalhado
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Briefing DIVA.md`

## Red flags — don't do this
- Never proceed with design without a validated briefing
- Never assume household composition (always ask)
- Never ignore budget-scope misalignment (flag it immediately)
- Never skip the "absolutely-not" question (avoids costly mistakes)
- Never forget to ask about living situation during works
- Never accept "I don't know my style" — use reference images to guide
- Never let one partner dominate when both are decision makers (capture both views)
- Never ignore future plans (a 2-year plan vs 20-year plan changes everything)

## Interactions
- Usually follows `diva-diagnose` (diagnostic first, then detailed brief)
- Feeds into `diva-floor-plan` for layout development
- Feeds into `diva-materials` for material palette aligned with preferences
- Feeds into `diva-budget` with validated budget expectations
- Save via `dario-obsidian-save` to vault

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Identificação do projecto está completa e sem placeholders

- [ ] Cliente nomeado (nome real, não "o cliente" ou `[NOME]`)
- [ ] Morada ou localização concreta do imóvel (não "Lisboa" genérico)
- [ ] Scope definido: cosmético / remodelação média / gut / nova construção / extensão
- [ ] Regime de posse claro: próprio, CPCV assinado, herança, arrendado
- [ ] Pelo menos uma data-chave registada (entrega, casamento, fim de arrendamento)

❌ NOT delivery-ready: "Cliente quer renovar o apartamento em Lisboa. Prazo a confirmar."
✅ Delivery-ready: "Ana Ferreira — Rua Rodrigues Sampaio 14, 2ºDto, Lisboa. Remodelação integral. CPCV assinado a 3/Jun/2025. Prazo duro: 15/Dez/2025 (filha nasce em Jan/2026)."

---

### Gate 2 — Quem habita o espaço está especificado com detalhe de rotinas

- [ ] Composição do agregado: adultos + crianças (idades) + animais
- [ ] Pelo menos 2 rotinas diárias registadas (ex.: trabalha em casa 4 dias/semana, cozinha todos os dias)
- [ ] Necessidades especiais sinalizadas ou explicitamente descartadas ("sem mobilidade reduzida, sem alergias")
- [ ] Horizonte temporal capturado (venda em X anos? aging-in-place?)

❌ NOT delivery-ready: "Casal com filhos. Precisam de escritório."
✅ Delivery-ready: "Mariana (38) + Paulo (41) + Tomás (6) + Inês (3) + gato. Paulo WFH 5 dias, precisa de isolamento acústico. Mariana cozinha diariamente, quer cozinha fechada. Horizonte: ficam 10+ anos, possível aging-in-place."

---

### Gate 3 — Estilo e preferências têm referências verificáveis, não adjectivos vagos

- [ ] Estilo nomeado com pelo menos um qualificador concreto (ex.: "contemporâneo quente, sem minimalismo frio")
- [ ] Must-haves listados (mínimo 2 elementos específicos)
- [ ] Absolutely-not listados (mínimo 1 recusa clara)
- [ ] Referência de imagem ou direcção de paleta indicada (board Pinterest, revista, projecto de referência)

❌ NOT delivery-ready: "Gostam de moderno mas aconchegante. Paleta neutra."
✅ Delivery-ready: "Estilo: contemporâneo mediterrâneo. Must-haves: ilha de cozinha em madeira de carvalho, banheira free-standing na suite, lareira a gás na sala. Absolutely-not: carpetes, prateleiras abertas na cozinha. Referência: board Pinterest 'Casa de Comporta' partilhado por Ana."

---

### Gate 4 — Programa funcional cobre todos os espaços com prioridade atribuída

- [ ] Cada divisão listada com função primária + secundária (se aplicável)
- [ ] Prioridade explícita: essencial / desejado / nice-to-have
- [ ] Pelo menos um requisito específico por espaço prioritário (dimensão, equipamento, adjacência)
- [ ] Espaços recusados ou fundidos registados explicitamente (ex.: "sem sala de jantar separada, espaço open-plan")

❌ NOT delivery-ready: "3 quartos, 2 casas de banho, cozinha open-space."
✅ Delivery-ready: "Suite (essencial): ensuite com duche walk-in 120×90 + duplo lavatório. Quarto 2 (essencial): Tomás, 12m² mín., secretária integrada. Quarto 3 (desejado): Inês agora, escritório em 8 anos. WC serviço (nice-to-have): apenas se orçamento permitir. Lavandaria: separada da cozinha, adjacente à suite."

---

### Gate 5 — Orçamento está estruturado com breakdown de consciência e prioridades de alocação

- [ ] Range min-max explícito em euros (não "orçamento médio" ou "razoável")
- [ ] Clarificado se inclui/exclui honorários, mobiliário, electrodomésticos
- [ ] Pelo menos uma prioridade de alocação: "investir em X, poupar em Y"
- [ ] Situação de mobiliário existente: o que fica, o que sai, o que compra

❌ NOT delivery-ready: "Orçamento à volta de 80K. Querem qualidade mas sem exageros."
✅ Delivery-ready: "Budget total: 95K–115K (inclui obra e acabamentos, exclui honorários e mobiliário). Investir: cozinha (25K+) e suite. Poupar: casas de banho secundárias (sanitários Roca linha Debba). Mobiliário: guardar sofá Cassina, cama suite e roupeiros — resto novo. Pagamento: 40% entrada, restante faseado por autos de medição."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets nem placeholders

- [ ] Nenhuma ocorrência de `[NOME]`, `[MORADA]`, `[DATA]`, `[VALOR]` ou equivalente no documento final
- [ ] Nome do cliente aparece no cabeçalho do briefing e na secção de gestão de projecto
- [ ] Datas no formato DD/Mês/AAAA ou Mês/AAAA (não "TBD" nem "a confirmar" em campos obrigatórios)
- [ ] Decisor principal identificado pelo nome (não "o cliente" ou "eles")

❌ NOT delivery-ready: "Briefing para [CLIENTE] — Projecto [LOCALIZAÇÃO] — Budget [VALOR]"
✅ Delivery-ready: "Briefing — Ana & Paulo Ferreira | Rua Rodrigues Sampaio 14, 2ºDto, Lisboa | Versão 1.0 — 10/Jun/2025 | Decisor principal: Ana Ferreira"

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via notas de reunião, documentos do cliente, ou sessão anterior
- 🟡 **assumed** — plausível com base no contexto, mas requer confirmação do cliente antes de entregar o briefing final
- 🟢 **projection** — estimativa de design por construção (não verificável até execução)

Output checklist upfront mostra ao leitor exactly o que é trust-as-is vs o que precisa de verify. **Honest transparency > briefing inflado.**

❌ NOT delivery-ready:
> "Cliente tem orçamento de 80 000 €, quer cozinha aberta, obra começa em março."
> *(sem labels — o projectista assume tudo como facto; pode avançar com premissas erradas)*

✅ Delivery-ready:
> - 🔵 **verified** — Titular do imóvel: Ana Ferreira (CPCV assinado, confirmado doc)
> - 🟡 **assumed** — Orçamento total: 80 000 € (cliente mencionou verbalmente; sem breakdown construção/honorários/mobiliário confirmado)
> - 🟡 **assumed** — Prazo desejado: obra concluída antes de setembro (referência informal; hard deadline não confirmada)
> - 🟢 **projection** — Custo estimado requalificação cozinha: 18 000–24 000 € (baseado em m² e nível de acabamento indicado; sujeito a medições e consulta empreiteiro)

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir assumptions com actuals (ex: orçamento validado com breakdown, prazo com data firme)
- [ ] All 🔵 citations added — documento de suporte referenciado por item (CPCV, planta, registo predial, notas assinadas)
- [ ] All 🟢 projections labeled as such ao cliente — expectativas claras de que estimativas de custo/prazo são provisórias até medições e consultas técnicas

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# BRIEFING DE PROJECTO
**Cliente:** Mariana Costa & Rui Teixeira
**Imóvel:** Av. Almirante Reis 210, 4ºEsq, Lisboa 1150-020
**Tipo:** Apartamento T3 — 98m² — Edifício anos 60
**Scope:** Remodelação integral (gut)
**Data do briefing:** 12/Jun/2025
**Decisor principal:** Mariana Costa (Rui valida orçamento)
**Próxima reunião:** 19/Jun/2025 — visita ao imóvel com arquitecta

---

## A — Identificação do Projecto
- **Posse:** Próprio — escritura lavrada a 5/Maio/2025
- **Uso actual:** Devoluto (herança)
- **Uso pretendido:** Habitação permanente
- **Data de entrega desejada:** 28/Fev/2026
- **Prazo duro:** Antes de Mar/2026 (contrato de arrendamento actual termina a 28/Fev/2026)
- **Condicionantes conhecidas:** Condomínio proíbe obras com ruído antes das 9h e ao fim-de-semana

---

## B — Agregado e Rotinas
- **Residentes:** Mariana (35), Rui (38), Benedita (7 anos), Afonso (4 anos)
- **Animais:** 1 cão (Labrador, porte grande)
- **Routinas-chave:**
  - Mariana trabalha em casa 3 dias/semana — precisa de escritório com porta
  - Rui sai às 7h30 — duche rápido, não partilha WC com as crianças de manhã
  - Benedita tem aulas de piano — espaço para piano vertical na sala
  - Jantares familiares frequentes (pais de ambos, ~8 pessoas, bi-semanais)
- **Necessidades especiais:** Afonso tem asma leve — sem alcatifas, preferência por materiais fáceis de limpar
- **Horizonte:** 15+ anos. Possível venda quando as crianças saírem (não antes)

---

## C — Estilo e Preferências
- **Direcção:** Contemporâneo quente. Influências escandinavas + pontos de cor mediterrâneos
- **Referências:** Board Pinterest "Casa Nova" (link partilhado) + projecto Casa em Melides (Architectural Digest PT, Jan/2025)
- **Paleta:** Branco quente base, madeira de carvalho natural, verde-salva como cor de acento
- **Must-haves:**
  1. Cozinha em U com ilha — granito cinza Pietra Grey
  2. Suite com closet walk-in (mínimo 4m²)
  3. Banheira de encastrar na casa de banho das crianças
  4. Espaço piano na sala (parede norte, 160×70cm livre)
- **Absolutely-not:** Alcatifas (asma Afonso), prateleiras abertas em qualquer cozinha, armários de espelho em corredores, tons de bege/creme

---

## D — Programa Funcional

| Espaço | Prioridade | Requisitos-chave |
|---|---|---|
| Cozinha | Essencial | Cozinha em U + ilha. Gás (manter ramal). Lava-louça Bosch. Frigorífico americano. Roupa: fora da cozinha |
| Sala estar/jantar | Essencial | Open-plan. Mesa para 8 (extensível). Zona piano parede norte |
| Suite principal | Essencial | Ensuite com duche 120×80 + closet walk-in ≥4m² |
| Quarto Benedita | Essencial | 10m² mín. Secretária integrada. Tomadas USB |
| Quarto Afonso | Essencial | 9m² mín. Convertível a escritório em ~10 anos |
| WC crianças | Essencial | Banheira encastrar + duche separado. Duplo lavatório |
| Escritório Mariana | Essencial | Porta com fecho. Mínimo 7m². Fibra dedicada (ponto de rede) |
| Lavandaria | Desejado | Separada. Máquina + secador sobrepostos. Teto alto (varal eléctrico) |
| Arrumos entrada | Nice-to-have | Cacifo para cão + bengaleiro embutido |

---

## E — Orçamento
- **Budget total:** 130K–155K
- **Inclui:** Obra, acabamentos, cozinha (móveis + electrodomésticos), casas de banho
- **Exclui:** Honorários de arquitectura, mobiliário sala/quartos, decoração
- **Prioridade de alocação:**
  - Investir: Cozinha (≥30K) + Suite (≥18K)
  - Poupar: WC serviço (sanitários linha básica), pintura quartos (cor única)
- **Mobiliário existente:** Sofá Roche Bobois (fica), cama suite (fica), resto novo
- **Electrodomésticos:** Marca preferida Bosch/Siemens. Forno a vapor desejado
- **Pagamento:** 30% no início da obra, 50% a meio, 20% na conclusão

---

## F — Condicionantes Técnicas e Legais
- **Diagnóstico prévio:** diva-diagnose realizado a 8/Jun/2025 — instalação eléctrica a substituir integralmente (monofásico → trifásico), canalizações em ferro (substituir), tecto falso a remover
- **Condomínio:** Regulamento proíbe obras ruidosas antes das 9h e ao sábado/domingo
- **Classificação:** Edifício sem classificação patrimonial
- **Energia:** Querem subir de certificado D para B. Solar fotovoltaico a avaliar (cobertura partilhada — aguarda aprovação condominial)
- **Smart home:** Básico — domótica de estores e iluminação (Shelly ou equivalente)
- **Segurança:** Porta blindada (já orçamentada à parte), alarme DSC com app

---

## G — Gestão do Projecto
- **Decisão:** Mariana decide estilo/acabamentos. Rui valida orçamento acima de 5K/item
- **Comunicação:** WhatsApp para updates rápidos + reunião quinzenal por videochamada (Thursdays 20h)
- **Envolvimento:** Colaborativo — querem aprovar cada selecção de material antes de encomendar
- **Experiência prévia:** Remodelação de cozinha em 2019 (experiência positiva, empreiteiro de confiança disponível)
- **Empreiteiro:** Têm contacto (Jorge Ferreira Construções, Loures) — aguardam recomendação da arquitecta para comparar
- **Situação durante obras:** Arrendamento actual até 28/Fev/2026 — obra tem de terminar ANTES dessa data

---

## Gaps e Contradições a Resolver
⚠️ **Gap 1:** Closet walk-in ≥4m² na suite pode conflituar com área disponível — validar na visita de 19/Jun
⚠️ **Gap 2:** Solar fotovoltaico dependente de aprovação de condomínio — prazo de resposta?
⚠️ **Gap 3:** Piano vertical na sala — confirmar dimensões exactas do instrumento para garantir circulação
```

---

## Output anti-patterns

- Usar adjectivos de estilo sem ancoragem: "moderno", "clássico" e "aconchegante" sem must-haves ou referências concretas tornam o briefing inutilizável pelo designer
- Deixar o orçamento como valor único sem breakdown: "80K" sem clarificar o que inclui garante conflito futuro com o cliente
- Omitir o decisor real: escrever "o casal decide em conjunto" sem nomear quem tem voto final em impasses paralisa o projecto
- Preencher campos de data com "TBD" ou "a combinar": datas vagas em campos de prazo duro são o risco de gestão de projecto mais caro do sector
- Listar divisões sem prioridade: sem a coluna essencial/desejado/nice-to-have, o arquitecto não sabe o que cortar quando o orçamento aperta
- Não registar os "absolutely-not": descobrir na fase de projecto que o cliente odeia prateleiras abertas depois de as ter desenhado é retrabalho evitável
- Gerar o briefing em modo template com todos os campos vazios sem perguntar o modo preferido (interactivo vs template vs from notes)
- Misturar informação de diva-diagnose com wishlist do cliente sem distinguir as fontes: condicionantes técnicas e preferências estéticas são secções separadas por razão
- Não sinalizar gaps e contradições: um briefing sem a secção ⚠️ Gaps dá falsa sensação de completude e cria surpresas em fase de projecto
- Usar angle-brackets `[NOME DO CLIENTE]` no documento entregue: qualquer placeholder não substituído invalida o documento como fonte de verdade do projecto
