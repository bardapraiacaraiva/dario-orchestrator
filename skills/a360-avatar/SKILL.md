---
name: "A360 Ideal Customer Avatar"
description: "Build a hyper-detailed ideal customer avatar — demographics, psychographics, pain points, desires, day-in-the-life narrative, buying triggers, objections map, and congregation analysis."
version: "1.0"
agent: "A360 — Accelera 360"
category: "Phase 1 — Discovery"
license: SEE-LICENSE
parent_agent: a360-director
compliance: [audit_immutable]
---

# A360 Ideal Customer Avatar

## Triggers

Activate this skill when the user says any of:
- "customer avatar", "avatar de cliente", "buyer persona"
- "ideal customer", "cliente ideal", "ICP"
- "who is my customer?", "quem e o meu cliente?"
- "target audience", "publico-alvo"
- "pain points", "dores do cliente"
- "psychographics", "demographics"
- Any request to define or profile the target customer for a business

## Frameworks & References

- **Alex Hormozi** ($100M Offers) — dream outcome, pain/desire mapping, "starving crowd" principle
- **Russell Brunson** (DotCom Secrets) — dream customer, Attractive Character, Epiphany Bridge
- **Ryan Levesque** (Ask Method) — deep dive survey, segmentation by self-identified bucket
- **Eugene Schwartz** (Breakthrough Advertising) — awareness levels, sophistication levels
- **Donald Miller** (StoryBrand) — customer as hero, guide positioning
- **Adele Revella** (Buyer Personas) — 5 Rings of Buying Insight

## Workflow

### Step 1: Gather Inputs
Collect from user or from a360-nicho output:
- Niche / market category
- Product or service concept
- Geographic focus
- Price range (low/mid/high ticket)
- B2B or B2C (or both)

### Step 2: Demographic Profile

| Attribute | Detail |
|-----------|--------|
| **Age range** | Primary: X-Y, Secondary: X-Y |
| **Gender** | Predominant or balanced |
| **Location** | City/region/country, urban vs rural |
| **Income level** | Annual range, disposable income |
| **Education** | Level, field of study |
| **Occupation** | Job title, industry, seniority |
| **Family status** | Single/married/kids, household size |
| **Tech savviness** | Low/medium/high, devices used |
| **Language** | Primary, secondary |

### Step 3: Psychographic Deep Dive

**Values & Beliefs:**
- What do they believe about themselves?
- What do they believe about the world?
- What do they value most (time, money, status, security, freedom)?
- What identity do they aspire to?

**Personality Traits:**
- Risk tolerance (conservative vs adventurous)
- Decision-making style (analytical vs emotional vs impulsive)
- Information consumption (reader vs watcher vs listener)
- Social orientation (leader vs follower vs independent)

**Lifestyle:**
- How do they spend their weekends?
- What brands do they already buy?
- What subscriptions do they pay for?
- What communities do they belong to?

### Step 4: Pain Points Hierarchy

Map pains across 4 dimensions (Hormozi framework):

| Pain Category | Specific Pain | Intensity (1-10) | Frequency |
|---------------|--------------|-------------------|-----------|
| **Financial** | Losing money on X | /10 | Daily/Weekly/Monthly |
| **Time** | Wasting hours doing Y | /10 | Daily/Weekly/Monthly |
| **Status** | Embarrassed by Z | /10 | Ongoing |
| **Health/Energy** | Stressed/exhausted by W | /10 | Daily/Weekly/Monthly |

**Hidden pains** (what they won't admit publicly):
- Secret frustrations
- Private fears
- Shame triggers

**Surface pains** (what they openly complain about):
- Forum posts, reviews, social comments
- Common complaints in the industry

### Step 5: Desires & Dream Outcomes

Map desires using Hormozi's Value Equation components:

| Desire | Dream Outcome | Current Barrier |
|--------|---------------|-----------------|
| What they want most | How life looks after transformation | What stops them today |
| Secondary desire | Secondary outcome | Secondary barrier |
| Tertiary desire | Tertiary outcome | Tertiary barrier |

**Transformation statement:**
"My customer goes from [BEFORE STATE] to [AFTER STATE] in [TIMEFRAME] without [SACRIFICE THEY FEAR]."

### Step 6: Day-in-the-Life Narrative

Write a 300-word narrative of a typical day for this avatar. Include:
- Morning routine and first thoughts
- Work/business challenges they face
- Moments of frustration (where your product enters)
- Evening routine and lingering worries
- What they Google at 2am
- What they complain about to their partner/friend

This narrative should make the user FEEL the avatar's reality.

### Step 7: Buying Triggers & Journey

**Trigger Events** (what pushes them to buy NOW):
1. [Event 1] — e.g., got rejected, lost a client, saw a competitor succeed
2. [Event 2] — e.g., life change, new year, financial pressure
3. [Event 3] — e.g., discovered a peer who solved the same problem

**Awareness Level** (Eugene Schwartz):
- Unaware / Problem-aware / Solution-aware / Product-aware / Most-aware
- Marketing approach for their current level

**Buying Process:**
1. Trigger event occurs
2. First search behavior (Google? YouTube? Ask a friend?)
3. Evaluation criteria (price? reviews? speed? brand?)
4. Decision timeline (impulse? days? weeks? months?)
5. Post-purchase behavior (share? review? refer?)

### Step 8: Objections Map

| Objection | Type | Counter-Argument |
|-----------|------|-----------------|
| "Too expensive" | Price | [Value reframe using Hormozi equation] |
| "I don't have time" | Effort | [Time investment vs time saved] |
| "Will this work for me?" | Trust | [Social proof, guarantee] |
| "I've tried before and failed" | Past failure | [Unique mechanism, what's different] |
| "I need to think about it" | Delay | [Cost of inaction, urgency] |
| "My situation is different" | Uniqueness | [Case studies of similar situations] |

### Step 9: Where They Congregate

| Channel | Specific Locations | Activity Level |
|---------|--------------------|---------------|
| **Social media** | Specific groups, pages, hashtags | High/Medium/Low |
| **Forums** | Subreddits, Quora topics, niche forums | High/Medium/Low |
| **YouTube** | Channels they watch, topics they search | High/Medium/Low |
| **Podcasts** | Shows they listen to | High/Medium/Low |
| **Events** | Conferences, meetups, webinars | High/Medium/Low |
| **Influencers** | Who they follow and trust | High/Medium/Low |
| **Publications** | Blogs, newsletters, magazines | High/Medium/Low |
| **Associations** | Professional bodies, clubs | High/Medium/Low |

This directly feeds into traffic strategy for a360-funil.

### Step 10: Avatar Summary Card

Condense everything into a one-page reference card.

## Output Template

```markdown
# A360 Customer Avatar
## Business: [BUSINESS NAME]
## Date: YYYY-MM-DD

### Avatar Name: "[FICTIONAL NAME]"
**One-liner**: [Age] [occupation] in [location] who struggles with [core pain] and wants [dream outcome].

### Demographics
| Attribute | Detail |
|-----------|--------|
| Age | X-Y |
| Gender | |
| Location | |
| Income | |
| Occupation | |
| Family | |

### Top 3 Pains
1. [Pain 1] — Intensity: X/10
2. [Pain 2] — Intensity: X/10
3. [Pain 3] — Intensity: X/10

### Dream Outcome
"[Transformation statement]"

### Day-in-the-Life
[300-word narrative]

### Buying Triggers
1. [Trigger 1]
2. [Trigger 2]
3. [Trigger 3]

### Top Objections & Counters
| Objection | Counter |
|-----------|---------|
| [Objection 1] | [Counter 1] |
| [Objection 2] | [Counter 2] |
| [Objection 3] | [Counter 3] |

### Where They Hang Out
- **Primary**: [channel + specific location]
- **Secondary**: [channel + specific location]
- **Tertiary**: [channel + specific location]

### Awareness Level
[Level] — Marketing implication: [approach]

### Hormozi Starving Crowd Score: X/10
```

## Red Flags

Stop and warn the user if:
- Avatar is too broad ("everyone aged 18-65") — force them to narrow
- No clear pain point with intensity above 7/10 (weak demand)
- Avatar cannot afford the intended price point
- No identifiable congregation points (unreachable audience)
- Avatar description is based purely on assumptions with zero evidence
- User is building for themselves instead of for a real market segment
- Multiple contradictory avatars (signal to segment, not combine)
- The avatar's pain is a "nice to have" not a "must solve"

## Handoff

After completing avatar:
- Route to `a360-validacao` to test assumptions with real people
- Route to `a360-oferta` to build an offer that matches avatar's pains/desires
- Feed congregation data to `a360-funil` for traffic strategy
- Save output to Obsidian: `05 - Claude - IA/Outputs/YYYY-MM-DD - A360 - Avatar - [AvatarName].md`

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Demographic Profile tem dados reais, não ranges genéricos

- [ ] Age range tem primário + secundário com justificação (não apenas "25-45")
- [ ] Income level inclui valor anual concreto em moeda local (€/R$)
- [ ] Occupation especifica cargo, sector e senioridade (não "profissional")
- [ ] Location resolve urbano/rural com cidade ou região concreta
- [ ] Tech savviness alinhado com produto (ex: SaaS → não pode ser "baixo")

❌ NOT delivery-ready: `Idade: 30-50 anos, rendimento médio, profissional qualificado`
✅ Delivery-ready: `Primário: 34-44 anos (donos de clínica veterinária, Lisboa/Porto), rendimento anual €45k-80k, gestor/proprietário de PME, smartphone-first, usa WhatsApp Business e Instagram diariamente`

---

### Gate 2 — Psychographic Deep Dive revela tensão interna específica

- [ ] Pelo menos 1 crença sobre si próprio está formulada na 1.ª pessoa (voz do avatar)
- [ ] Risk tolerance + decision-making style têm implicação directa na copy/oferta
- [ ] Lifestyle inclui ≥2 marcas reais que este avatar já compra
- [ ] Identidade aspiracional é concreta (não "quer ter sucesso")
- [ ] Valores hierarquizados — não apenas listados, ordenados (1.º tempo, 2.º status…)

❌ NOT delivery-ready: `Valoriza a família e a estabilidade financeira. Gosta de tecnologia.`
✅ Delivery-ready: `"Trabalho 60h/semana e não consigo desligar — se não crescer este ano vou ter de fechar." Compra Apple, Audible, Farfetch. Subscreve newsletters como Morning Brew. Decisor analítico com prazo de 7-14 dias. Identidade aspiracional: "CEO que delega".`

---

### Gate 3 — Pain Points Hierarchy tem intensidade numérica + frequência preenchidas

- [ ] Tabela 4 dimensões (Financial/Time/Status/Health) 100% preenchida — sem células vazias
- [ ] Pelo menos 1 dor "hidden" que o avatar não diria publicamente em voz alta
- [ ] Dores "surface" ancoradas em fonte real (ex: comentário tipo Reddit, review Google)
- [ ] Intensidade ≥8/10 em pelo menos 1 dor — se não houver, o niche está errado
- [ ] Dores mapeadas são assimétricas (não todas com intensidade 7/10)

❌ NOT delivery-ready: `Dor financeira: perde dinheiro. Intensidade: alta. Frequência: frequente.`
✅ Delivery-ready: `Dor financeira: "Pago €800/mês a um gestor que me entrega relatórios que não percebo e descubro erros só quando o fisco notifica." Intensidade: 9/10. Frequência: mensal. [fonte: comentários Grupo Facebook "Empreendedores PT", 2024]`

---

### Gate 4 — Day-in-the-Life Narrative passa o "teste do calafrio"

- [ ] Narrativa ≥250 palavras com arco temporal (manhã → tarde → noite → 2am)
- [ ] Produto/serviço do cliente entra na narrativa num momento de frustração concreto
- [ ] Inclui o que o avatar Googla às 2am (frase literal de pesquisa entre aspas)
- [ ] Linguagem usa vocabulário próprio do avatar, não linguagem de marketing
- [ ] Leitor da narrativa consegue nomear 1 emoção dominante do avatar sem ajuda

❌ NOT delivery-ready: `Acorda cedo, vai trabalhar, enfrenta desafios no trabalho, chega a casa cansado e preocupado com as finanças.`
✅ Delivery-ready: `06h47 — Maria apaga o alarme antes de o marido acordar. Já tem 11 notificações do WhatsApp de clientes. Enquanto faz café, abre o Instagram e vê o concorrente a anunciar novo espaço. Fecha o app. Às 23h30, com o portátil na cama, pesquisa: *"como aumentar faturação clínica veterinária sem contratar mais staff"*. O marido pede-lhe para desligar. Ela finge que sim.`

---

### Gate 5 — Objections Map tem contra-argumento accionável, não platitude

- [ ] Todas as 6 objecções da tabela têm Counter-Argument preenchido (sem células "[Value reframe]" por preencher)
- [ ] Objecção "passei por isso antes e falhou" tem mecanismo único explicado (o que é diferente desta vez)
- [ ] Pelo menos 1 objecção foi personalizada ao sector/produto específico (não objecção genérica)
- [ ] "Preciso de pensar" tem custo de inacção quantificado (€ ou tempo perdido)
- [ ] Counter-arguments são curtos o suficiente para usar directamente em copy (≤2 frases)

❌ NOT delivery-ready: `"Muito caro" → Reframe de valor usando equação do Hormozi.`
✅ Delivery-ready: `"Muito caro" → "A Cuidai cobra €297/mês. As clínicas que trabalharam connosco reportaram uma redução média de 4h/semana em tarefas administrativas — a €50/h, isso é €800/mês recuperados. O software paga-se em 11 dias."`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets por preencher

- [ ] Nenhum placeholder `<nome>`, `[INSERIR]`, `[CLIENT]` visível no output final
- [ ] Nome do negócio do cliente aparece ≥3x integrado nos exemplos e narrativa
- [ ] Todos os valores monetários têm moeda e contexto (não "preço alto")
- [ ] Fontes de congregação são URLs ou nomes específicos (não "redes sociais")
- [ ] Transformation Statement está 100% preenchida com Before/After/Timeframe/Sacrifice reais

❌ NOT delivery-ready: `"O meu cliente vai de [BEFORE STATE] para [AFTER STATE] em [TIMEFRAME] sem [SACRIFÍCIO]."`
✅ Delivery-ready: `"A cliente da Cuidai vai de 'clínica veterinária a perder 6h/semana em chamadas e reagendamentos' para 'agenda 90% automatizada e NPS acima de 4,5' em 60 dias sem ter de contratar recepcionista extra."`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Avatar de Cliente Ideal — Cuidai (Gestão de Clínicas Veterinárias)

---

## Perfil Demográfico

| Atributo | Detalhe |
|---|---|
| **Idade** | Primário: 32-44 anos (proprietária/médica-veterinária) · Secundário: 45-55 anos (sócio-gestor não-clínico) |
| **Género** | 68% feminino (dados sector veterinário PT, 2023) |
| **Localização** | Concelhos urbanos e periurbanos: Lisboa, Porto, Braga, Setúbal · clínica física com 2-8 funcionários |
| **Rendimento** | €38k-72k/ano pessoal · faturação clínica €180k-600k/ano |
| **Educação** | Licenciatura/Mestrado Medicina Veterinária (UTAD, FMV Lisboa, ICBAS) |
| **Cargo** | Médica-veterinária proprietária ou Directora Clínica |
| **Família** | 60% casada, 1-2 filhos (0-10 anos) · sente culpa crónica por horas ausente |
| **Tech** | Médio-alto · iPhone, usa Notion ou papel, odeia software com onboarding longo |
| **Língua** | Português PT · consome conteúdo PT e EN |

---

## Psychographic Deep Dive

**O que ela acredita sobre si própria:**
> *"Sou boa médica. Sou má gestora — e tenho medo que os outros descubram."*

**O que ela acredita sobre o mundo:**
> Os tutores de animais são cada vez mais exigentes mas menos compreensivos com atrasos. Uma má review no Google destrói meses de trabalho.

**Hierarquia de valores (ordenada):**
1. Tempo (com filhos, não no Excel)
2. Reputação profissional
3. Estabilidade financeira da clínica
4. Liberdade para tratar sem gerir

**Marcas que já compra:** Apple, Nespresso, Decathlon, Spotify Premium, LinkedIn Premium (ativo mas culpada por não usar)

**Identidade aspiracional:** "Directora de clínica que tem sistema — não é o sistema."

**Risk tolerance:** Baixo-médio. Testou 2 softwares antes e abandonou. Só compra com demo + garantia.

---

## Pain Points Hierarchy

| Categoria | Dor Específica | Intensidade | Frequência |
|---|---|---|---|
| **Financeira** | "Não sei qual dos meus serviços tem margem real — preço pelo feeling" | 8/10 | Mensal |
| **Tempo** | "Passo 2-3h/dia a responder mensagens de agendamento que uma máquina fazia" | 9/10 | Diária |
| **Status** | "Clínica concorrente abriu segundo espaço. Eu ainda não consigo sair de férias uma semana" | 7/10 | Recorrente |
| **Energia** | "Chego a casa e ainda estou 'on-call' mental — nunca desligo completamente" | 9/10 | Diária |

**Hidden pain (não diz em voz alta):**
> Tem medo de que a clínica só funcione porque *ela* está lá — e que se adoecer, tudo para.

**Surface pain (fonte: Grupo Facebook "Veterinários Empreendedores PT", 847 membros):**
> "Alguém tem sugestão de software de gestão que não precise de uma semana de formação para usar?" — post com 34 comentários, Jan 2024

---

## Desires & Dream Outcomes

| Desejo | Dream Outcome | Barreira Actual |
|---|---|---|
| Sair de férias 10 dias sem o telefone tocar | Clínica fatura igual sem ela presente | Não tem processos documentados nem delegação real |
| Perceber a rentabilidade real por serviço | Decisões de preço baseadas em dados, não instinto | Software actual só tem faturação, não margem |
| Agenda sem buracos nem double-booking | 90% da agenda preenchida, 0 conflitos | Agendamento manual via WhatsApp + telefone |

**Transformation Statement:**
> "A cliente da Cuidai vai de 'veterinária presa na operação diária, 60h/semana, agenda caótica e sem dados de gestão' para 'directora com agenda 85% automatizada, margem por serviço visível e 1 tarde livre por semana' em 45 dias sem ter de contratar mais staff nem mudar o software de facturação já existente."

---

## Day-in-the-Life Narrative

É segunda-feira, 07h12. A Ana acorda antes do alarme — tem uma cirurgia às 9h e já está mentalmente a rever o protocolo. Enquanto o café faz, abre o WhatsApp Business: 7 mensagens desde ontem à noite. Dois tutores a pedir marcação, um a cancelar, um a perguntar o resultado de análises que ainda não chegaram. Responde enquanto come torrada de pé.

Na clínica às 8h30, a recepcionista diz-lhe que a agenda de quarta está "um bocado confusa" — dois gatos marcados para o mesmo slot. Outra vez. A Ana suspira. Já aconteceu três vezes este mês.

Entre consultas, alguém toca à campainha sem marcação. Tutor em pânico com cão a coxear. Encaixa. O resto da tarde atrasa 40 minutos.

Às 19h, depois de fechar, senta-se para "só ver os números de março". O Excel que a contabilista lhe enviou tem 14 colunas e não percebe qual o serviço que mais contribuiu para a margem. Fecha. Para amanhã.

23h45 — portátil na cama, pesquisa: *"software gestão clínica veterinária portugal sem mensalidade cara"* e depois *"como automatizar agendamento whatsapp clínica"*. Encontra um artigo. Começa a ler. O marido apaga a luz do lado dele. Ela continua com o brilho do ecrã no rosto.

O que ela não diz a ninguém: se ficasse doente duas semanas, a clínica não sobrevivia. E isso aterra-a.

---

## Buying Triggers

1. **Review negativa no Google** sobre tempo de espera → gatilho imediato de urgência
2. **Ver colega a anunciar expansão** nas redes sociais → dor de status aguda
3. **Recepcionista de baixa** → operação entra em colapso, força decisão de sistematizar
4. **Janeiro/Setembro** → revisão anual de custos, momento de "este ano tem de ser diferente"

**Awareness Level:** Solution-aware (sabe que existe software de gestão, já testou 1-2, desconfiante)
**Abordagem recomendada:** Não vender features — mostrar prova de que esta solução é diferente das que já falhou. Demo com dados dela, não dados fictícios.

**Buying Process:**
1. Trigger (review negativa ou colapso operacional)
2. Pesquisa Google + pergunta no grupo Facebook de veterinários
3. Critérios: integração com software actual, facilidade de uso, suporte em PT
4. Timeline: 2-3 semanas (analítica, pede demo, consulta sócio ou marido)
5. Pós-compra: partilha no grupo se correu bem — fonte de referral de alto valor

---

## Objections Map

| Objecção | Tipo | Counter-Argument |
|---|---|---|
| "Já tentei dois softwares e desisti" | Falha passada | "A Cuidai tem onboarding feito por nós, não por si — migramos a agenda e os contactos em 48h. A Dra. Filipa (Clínica VetSul, Almada) estava live ao 3.º dia." |
| "Não tenho tempo para aprender mais uma ferramenta" | Esforço | "A curva de aprendizagem é 90 minutos. Temos gravação + suporte WhatsApp PT em horário clínico." |
| "É caro para o que é" | Preço | "€197/mês. Se recuperar 2h/dia em agendamentos a €40/h de valor de consulta = €1.760/mês desbloqueados. ROI em 4 dias." |
| "A minha situação é diferente — tenho duas espécies e urgências" | Unicidade | "Temos 14 clínicas mistas PT. Posso mostrar-lhe a agenda da Clínica Fauna (Lisboa) que trata exóticos + urgências." |
| "Preciso de falar com o meu sócio" | Delay | "Claro. Envio-lhe um one-pager com os números do ROI para mostrar — e lembre que cada semana sem sistema custa em média €440 em tempo perdido." |
| "E se mudar de ideia?" | Risco | "30 dias de garantia total. Cancelamento sem justificação, devolvemos tudo." |

---

## Where They Congregate

| Canal | Localização Específica | Actividade |
|---|---|---|
| Facebook | Grupo "Veterinários Empreendedores Portugal" (847 membros) | Alta |
| Instagram | #clínicaveterinária, #veterináriaportugal, contas @omvportugal | Média |
| YouTube | "Gestão de clínicas" (PT), canais de negócio para profissionais de saúde | Baixa |
| Eventos | Congresso APMVEAC (anual), Vet Show Lisboa | Alta (decisores presentes) |
| WhatsApp | Grupos de turma da faculdade ainda activos (referral peer-to-peer) | Muito alta |
```

---

## Output anti-patterns

- **Avatar genérico transplantado** — mesmas dores e demografia para uma clínica veterinária e um e-commerce de roupa; nenhum detalhe é específico ao sector
- **Transformation Statement com placeholders visíveis** — entregar ao cliente com `[BEFORE STATE]` e `[TIMEFRAME]` por preencher
- **Pain intensities todas a 7/10** — ausência de hierarquia real revela que não houve investigação; tudo parece igualmente urgente e nada parece urgente
- **Day-in-the-Life escrito em linguagem de marketing** — "enfrenta desafios no seu percurso empreendedor" em vez da voz interna real do avatar
- **Objections Map com counter-arguments template** — células com "[Value reframe using Hormozi equation]" ainda por preencher são inaceitáveis em entrega final
- **Congregation sem URLs ou nomes concretos** — "está no Instagram e em fóruns da área" não orienta nenhuma campanha de aquisição
- **Hidden pains omitidas** — entregar avatar sem a camada de vergonha/medo privado perde o diferencial psicográfico que a concorrência não vê
- **Awareness Level não diagnosticado** — copy escrita para "Unaware" enviada a avatar "Product-aware" é a causa #1 de anúncios que não convertem
- **Buying trigger sem evento concreto** — "quando sentir necessidade" não é um trigger, é uma não-resposta; cada trigger precisa de um evento nomeável no mundo real
- **Nenhuma fonte citada nas surface pains** — afirmações sobre o que o avatar "se queixa" sem referência a review, fórum ou entrevista são ficção, não pesquisa
