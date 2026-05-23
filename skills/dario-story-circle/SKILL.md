---
name: dario-story-circle
description: Brand story / about page / origin narrative generator using Dan Harmon's Story Circle (8 beats), Campbell's Hero's Journey, and Park Howell's ABT. Produces the brand's core narrative for website, decks, and campaigns. Triggers on "brand story", "origin story", "about page", "story circle", "narrativa", "quem somos", "história da marca".
license: MIT
---

# DARIO Skill — Story Circle

Crafts the brand's core narrative — the story that lives on the About page, opens the pitch deck, anchors the email welcome sequence, and gives the founder something to say in interviews.

## When to activate
- About page writing or redesign
- Brand story for new client
- Founder story for authority building
- Brand video script
- After `dario-brand` (archetype + positioning exist, now need the story)

## Workflow

### 1. RAG consult
```
mcp__dario-rag__search_kb(query: "dan harmon story circle 8 beats", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "joseph campbell heros journey monomyth", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "park howell abt and but therefore", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "matthew dicks five second moment storyworthy", collection: "dario", limit: 5)
```

### 2. Gather story ingredients
- **The founder** — who are they, where did they come from
- **The inciting incident** — what happened that made them start this
- **The struggle** — what was hard, what they almost gave up on
- **The insight** — the "aha moment" that changed everything
- **The mission** — what they now believe and fight for
- **The transformation** — what changed for their customers
- **The proof** — evidence it works (results, testimonials, milestones)

### 3. Apply Dan Harmon's Story Circle (8 beats)

```
    1. YOU (comfort zone)
   /                        \
  8. CHANGE                  2. NEED
  |   (return, transformed)  |   (something is missing)
  |                          |
  7. RETURN                  3. GO
  |   (bring it back)       |   (enter unfamiliar territory)
  |                          |
  6. TAKE                    4. SEARCH
   \  (pay the price)      /   (adapt, struggle)
    5. FIND (the insight)
```

Map the brand story to these 8 beats:
1. **YOU:** Founder in their previous world
2. **NEED:** The gap they noticed, the frustration
3. **GO:** Decision to do something about it (leave comfort)
4. **SEARCH:** Early struggles, failures, learning
5. **FIND:** The breakthrough insight / methodology / product
6. **TAKE:** The cost paid (risk, money, time, reputation)
7. **RETURN:** Bringing the solution to the world (the brand)
8. **CHANGE:** How the founder (and customers) are transformed

### 4. Distill to ABT (And, But, Therefore)
One sentence that captures the whole story:

> **[Founder/Brand] was [doing X] AND [things were Y], BUT [problem/insight], THEREFORE [brand/mission exists].**

### 5. Write 3 versions

#### Version 1: Micro (50 words) — for bios, social media, email signatures
#### Version 2: Medium (200-300 words) — for About page hero, pitch intros
#### Version 3: Full (600-1000 words) — for full About page, brand video script

### 6. StoryBrand integration (if `dario-brand` ran)
Map the brand story to the SB7 framework:
- The CUSTOMER is the Hero (not the founder)
- The BRAND is the Guide (empathetic authority)
- The story proves why the Guide is qualified

So the founder story = the Guide's origin story that builds trust and empathy.

## Output template
```markdown
# Brand Story — <Client>

## Story Ingredients
- Founder: ...
- Inciting incident: ...
- Struggle: ...
- Insight: ...
- Mission: ...
- Transformation: ...
- Proof: ...

## Story Circle (8 beats)
1. YOU: ...
2. NEED: ...
3. GO: ...
4. SEARCH: ...
5. FIND: ...
6. TAKE: ...
7. RETURN: ...
8. CHANGE: ...

## ABT One-liner
> ...

## Version 1 — Micro (50 words)
...

## Version 2 — Medium (200-300 words)
...

## Version 3 — Full (600-1000 words)
...

## Usage guide
- About page: Version 3 + hero image
- Pitch deck slide 4: Version 2
- Email welcome E1: Version 2 adapted
- Social bio: Version 1
- Video script: Version 3 with visual cues
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Brand Story.md`

## Red Flags
- Never make the brand the hero of the story — the customer is always the hero, the brand is the guide; violating this turns the narrative into self-congratulation that repels rather than attracts
- Never skip the epiphany moment (beat 5: FIND) — a story without a breakthrough insight is just a chronological resume with no emotional payoff
- Always produce all 3 output formats (micro/medium/full) — a single version cannot serve bios, About pages, and pitch decks, and the client will ask for the others anyway
- Never write a brand story without first gathering the real inciting incident from the founder — fabricated origin stories ring hollow and crumble under interview questions
- Always connect the story back to the customer's transformation (beat 8: CHANGE) — a founder story that ends with the founder's success instead of the customer's outcome misses the entire point

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Story Ingredients são reais e verificáveis
- [ ] Inciting incident tem data ou contexto temporal concreto (não "um dia percebi que…")
- [ ] Luta/struggle inclui detalhe específico (produto chumbou, cliente recusou, runway acabou)
- [ ] Proof section tem pelo menos 1 métrica, data, ou nome verificável
- [ ] Insight (beat 5: FIND) é uma ideia distinta — não um platitude genérico
- ❌ NOT delivery-ready: `"O fundador sempre soube que havia um problema no mercado e decidiu agir."`
- ✅ Delivery-ready: `"Em março de 2021, após a terceira recusa de investidores e 14 meses a bootstrapear, Margarida percebeu que o problema não era o produto — era que os lares nunca tinham visto cuidados ao domicílio explicados em linguagem simples."`

### Gate 2 — Story Circle (8 beats) mapeado por completo
- [ ] Todos os 8 beats estão preenchidos, sem nenhum em branco ou com placeholder
- [ ] Beat 1 (YOU) e beat 8 (CHANGE) são contrastantes — há transformação visível
- [ ] Beat 5 (FIND) é o pico emocional, não apenas "lançámos o produto"
- [ ] Beat 6 (TAKE) nomeia o custo real pago — risco, dinheiro, reputação, tempo
- ❌ NOT delivery-ready: `"5. FIND: Desenvolvemos uma solução inovadora para o problema."`
- ✅ Delivery-ready: `"5. FIND: Ao acompanhar a própria mãe após uma cirurgia, Ricardo percebeu que nenhuma plataforma mostrava o cuidador como pessoa — apenas como serviço. Essa tarde de outubro de 2022 mudou tudo."`

### Gate 3 — ABT One-liner está estruturalmente correto
- [ ] Segue rigorosamente a estrutura AND / BUT / THEREFORE (nenhuma palavra substituída)
- [ ] Encapsula TODA a história em 1 frase — funciona fora de contexto
- [ ] Não contém jargão técnico — legível por qualquer pessoa em 5 segundos
- [ ] Pode ser dito em voz alta sem soar artificial
- ❌ NOT delivery-ready: `"A Cuidai existe para transformar o setor e criar valor para todos os stakeholders."`
- ✅ Delivery-ready: `"Ricardo cuidava da mãe e sabia que havia cuidadores excelentes por todo o país, AND a família precisava deles, BUT nunca conseguia encontrá-los nem confiar neles sem referência pessoal, THEREFORE criou a Cuidai — a rede onde cada cuidador tem rosto, história e avaliação real."`

### Gate 4 — Brand é o Guide, Cliente é o Herói
- [ ] Em nenhuma versão o fundador/marca "salva o dia" — é o cliente que transforma
- [ ] A narrativa inclui pelo menos 1 frase que coloca o cliente no centro da transformação
- [ ] O fundador aparece como "alguém que passou por isso e por isso guia" — não como protagonista triunfante
- [ ] Beat 8 (CHANGE) menciona explicitamente o que muda para o cliente, não só para a empresa
- ❌ NOT delivery-ready: `"Hoje a Cuidai é líder de mercado com 500 cuidadores registados e crescimento de 3x ao ano."`
- ✅ Delivery-ready: `"Hoje, famílias como a da Ana encontram em menos de 48 horas o cuidador certo — e dormem descansadas pela primeira vez em meses."`

### Gate 5 — 3 Versões entregues, cada uma no formato correto
- [ ] Versão Micro está entre 45–55 palavras (contadas)
- [ ] Versão Média está entre 190–320 palavras e pode ser lida em 90 segundos
- [ ] Versão Completa está entre 580–1050 palavras e inclui os 8 beats reconhecíveis
- [ ] Usage guide está preenchido com contexto real do cliente (não genérico)
- ❌ NOT delivery-ready: `"Versão 1 (micro): A nossa empresa nasceu para resolver um problema real no mercado de cuidados."`
- ✅ Delivery-ready: `"Versão 1 (micro, 51 palavras): Ricardo Fonseca passou 14 meses a tentar encontrar ajuda para a mãe depois de uma operação. Não havia plataforma em Portugal que mostrasse o cuidador como pessoa real. Em 2022 criou a Cuidai. Hoje, 1.200 famílias encontram cuidadores de confiança em menos de 48 horas."`

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero angle-brackets
- [ ] Nenhum `<Client>`, `<Founder>`, `<Date>`, `<Metric>` ou placeholder visível no output
- [ ] Nome do cliente aparece no título e pelo menos 3× no corpo
- [ ] Datas, nomes de fundadores e métricas são os fornecidos pelo cliente — ou marcados com `[VERIFICAR COM CLIENTE]` se não confirmados
- [ ] Save location tem data real (YYYY-MM-DD do dia da entrega) e nome do cliente
- ❌ NOT delivery-ready: `"# Brand Story — <Client>" / "Fundador: <nome do fundador>"`
- ✅ Delivery-ready: `"# Brand Story — Cuidai" / "Fundador: Ricardo Fonseca, Lisboa, 2022"`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Brand Story — Cuidai

## Story Ingredients
- Founder: Ricardo Fonseca, Lisboa — ex-gestor de operações em saúde corporativa
- Inciting incident: Outubro 2022 — mãe de Ricardo opera à anca; Ricardo passa 3 semanas
  a tentar encontrar cuidador domiciliário de confiança sem conseguir referência concreta
- Struggle: 11 plataformas testadas, nenhuma mostrava perfil humano do cuidador;
  primeiro MVP rejeitado por 4 investidores ("mercado pequeno"); runway de 8 meses
- Insight: "O problema não é falta de cuidadores — é falta de confiança. E confiança
  só existe com cara, história e avaliação real."
- Mission: Tornar invisível o atrito entre famílias e cuidadores de qualidade em Portugal
- Transformation: Famílias passam de semanas de busca ansiosa para match em 48 horas;
  cuidadores passam de invisíveis a profissionais com perfil, reputação e rendimento estável
- Proof: 1.200 famílias ativas, 430 cuidadores certificados, NPS 71, desde jan 2023

## Story Circle (8 beats)
1. YOU: Ricardo, gestor experiente em saúde, vida organizada, mãe saudável em Cascais
2. NEED: Mãe opera à anca; Ricardo percebe que não existe forma digna de encontrar
   ajuda ao domicílio — só grupos de Facebook e boca-a-boca
3. GO: Abandona projeto de consultoria, investe €18.000 próprios, começa a entrevistar
   cuidadores e famílias durante 4 meses
4. SEARCH: MVP rejeitado por investidores; primeiro cuidador da plataforma desiste na
   véspera; Ricardo aprende que o produto técnico é secundário — o produto é a confiança
5. FIND: Em março de 2023, ao ler o perfil que uma cuidadora escreveu sobre si própria
   (incluindo a história da avó que cuidou em criança), Ricardo vê a primeira família
   escolher sem hesitar. O diferencial é a humanidade visível.
6. TAKE: €18k poupanças investidos, 9 meses sem salário, projeto de consultoria
   encerrado, 4 rejeições de investidores, 2 co-fundadores que saíram no primeiro ano
7. RETURN: Cuidai lança publicamente em setembro de 2023 com 80 cuidadores perfilados
   e sistema de avaliação transparente — o primeiro em Portugal com vídeo de apresentação
8. CHANGE: Famílias como a de Ana Rodrigues, Braga, encontram cuidador ideal em 31 horas;
   cuidadoras como Fátima Silva têm perfil profissional e rendimento 40% acima da média
   do setor; Ricardo tem a plataforma que queria ter tido para a própria mãe

## ABT One-liner
> Ricardo Fonseca sabia que Portugal tinha cuidadores extraordinários espalhados por todo
> o país AND que milhares de famílias precisavam urgentemente deles, BUT nenhuma
> plataforma mostrava o cuidador como pessoa real — apenas como serviço anónimo —
> THEREFORE criou a Cuidai, onde cada cuidador tem rosto, história e avaliação genuína,
> e cada família encontra ajuda de confiança em menos de 48 horas.

## Versão 1 — Micro (51 palavras)
Ricardo Fonseca tentou encontrar ajuda para a mãe após uma cirurgia. Onze plataformas
depois, ainda não confiava em ninguém. Em 2022 percebeu porquê: nenhuma mostrava o
cuidador como pessoa. Criou a Cuidai. Hoje, 1.200 famílias portuguesas encontram o
cuidador certo em menos de 48 horas — com cara, história e avaliação real.

## Versão 2 — Média (241 palavras)
Quando a mãe de Ricardo Fonseca operou à anca, em outubro de 2022, ele tinha todos
os recursos para encontrar ajuda. Experiência em saúde corporativa, rede de contactos,
tempo para pesquisar. E ainda assim, três semanas depois, não tinha ninguém em quem
confiasse para cuidar dela.

Testou onze plataformas. Todas mostravam preços e disponibilidade. Nenhuma mostrava
quem era a pessoa do outro lado.

Foi nesse momento que Ricardo percebeu que o problema do cuidado domiciliário em
Portugal não era falta de profissionais — era falta de confiança. E confiança não se
constrói com tabelas de preços. Constrói-se com histórias reais.

Passou os quatro meses seguintes a entrevistar cuidadores e famílias. Investiu as
poupanças. Fechou o projeto de consultoria. Ouviu quatro "não" de investidores.
E continuou.

Em março de 2023, viu a primeira família escolher uma cuidadora da plataforma em
menos de uma hora — depois de ler a história que ela escreveu sobre a avó que cuidou
em criança. Esse foi o momento em que soube que estava no caminho certo.

Hoje, a Cuidai tem 430 cuidadores certificados e 1.200 famílias ativas em todo o país.
O NPS é 71. A média de match é 48 horas.

Mas o que Ricardo mais recorda não são os números. É o WhatsApp da filha da Dona
Helena, de Braga: *"Finalmente dormi uma noite inteira."*

## Versão 3 — Completa (742 palavras)
Outubro de 2022. Ricardo Fonseca tem 38 anos, uma carreira sólida em gestão de
operações de saúde, e uma mãe que acabou de sair do bloco operatório depois de uma
cirurgia à anca.

O médico é claro: vai precisar de apoio domiciliário durante pelo menos três meses.
Fisioterapia, acompanhamento diário, alguém de confiança em casa.

Ricardo conhece o sistema. Sabe como funciona. Vai resolver isto em dois dias.

Não resolve.

Três semanas depois, tinha testado onze plataformas, entrado em quatro grupos de
Facebook, perguntado a toda a rede de contactos, e ainda não tinha ninguém. Não
porque não houvesse cuidadores — havia muitos. Mas porque nenhuma plataforma lhe
mostrava quem eram essas pessoas de verdade. Havia preços. Havia disponibilidade.
Não havia humanidade.

Numa tarde de novembro, enquanto via pela décima vez um perfil com foto genérica e
três linhas de texto, Ricardo fez a pergunta que mudaria tudo: *"Se eu não confiaria
nesta pessoa para cuidar da minha mãe, como é que mais alguém confia?"*

A resposta era simples e devastadora: não confia. E é por isso que o mercado funciona
quase inteiramente por boca-a-boca — que exclui toda a gente que não tem a rede certa.

Ricardo fechou o computador, abriu uma folha em branco, e começou a desenhar outra
coisa.

---

Os quatro meses seguintes não foram fáceis. Encerrou o projeto de consultoria que
estava a desenvolver. Investiu €18.000 de poupanças sem garantia de retorno.
Entrevistou 140 cuidadores e 60 famílias para perceber o que criava — ou destruía —
a confiança. Apresentou o primeiro protótipo a quatro investidores e ouviu quatro
variações de "mercado pequeno demais". Dois co-fundadores iniciais saíram antes do
produto estar pronto.

Houve uma semana de janeiro de 2023 em que Ricardo pensou seriamente em parar.

Não parou. Porque nessa mesma semana recebeu uma mensagem de uma cuidadora chamada
Fátima, que tinha escrito o perfil mais honesto que já tinha lido: a história da avó
que cuidou em criança, o motivo pelo qual escolheu esta profissão, o que a faz levantar
de manhã. Ricardo publicou esse perfil como teste.

Em 4 horas, três famílias entraram em contacto. Uma contratou Fátima nesse mesmo dia.

Esse foi o momento do FIND — o instante em que a hipótese se torna certeza. O
diferencial não era tecnologia. Era humanidade tornada visível.

---

A Cuidai lançou publicamente em setembro de 2023. Oitenta cuidadores com perfis
completos: fotografia real, vídeo de apresentação de 90 segundos, história pessoal,
avaliações verificadas de famílias anteriores. Uma interface que trata o cuidador
como profissional, não como commodity.

O que aconteceu a seguir surpreendeu até Ricardo.

As famílias não precisavam de ser convencidas. Precisavam apenas de ver. Quando
viam a pessoa real — a história, o rosto, a razão pela qual fazia este trabalho —
a decisão tornava-se fácil. A média de match caiu para 48 horas. O NPS fixou-se
em 71 nos primeiros seis meses.

Hoje, a Cuidai tem 430 cuidadores certificados, 1.200 famílias ativas em Portugal
continental, e está a expandir para os Açores no primeiro trimestre de 2025.

Mas o que define o sucesso da Cuidai não são os números de crescimento.

É a filha da Dona Helena, de Braga, que enviou uma mensagem às 7h32 de uma
segunda-feira: *"Finalmente dormi uma noite inteira desde que a minha mãe veio
para casa."*

É a Fátima, que passou de trabalho informal mal pago para rendimento 40% acima
da média do setor, com agenda preenchida e clientes que a recomendam pelo nome.

É o Ricardo, que tem hoje a plataforma que queria ter tido para a própria mãe —
e que sabe, todos os dias, que o produto que está a construir não é tecnologia.

É confiança. E confiança começa sempre com uma história real.

---

*A Cuidai não é o herói desta história. As famílias que finalmente dormem
descansadas são. Os cuidadores que finalmente têm o reconhecimento que merecem são.
A Cuidai é apenas o caminho entre eles.*

## Usage guide
- About page (cuidai.pt/sobre): Versão 3 completa + fotografia de Ricardo com equipa
- Pitch deck slide 4 ("Porquê a Cuidai?"): Versão 2 média
- Email de boas-vindas E1 (famílias): Versão 2 adaptada na 2.ª pessoa ("quando a sua
  família precisa de ajuda…")
- Bio de Ricardo para imprensa/podcasts: Versão 1 micro
- Script de vídeo institucional (90 seg): Versão 3 com cortes em beats 2, 5 e 8
```

---

## Output anti-patterns

- **Fundador como herói triunfante** — narrar o sucesso da empresa em vez da transformação do cliente; o leitor identifica-se com a jornada, não com o troféu
- **Beat 5 (FIND) vazio ou genérico** — "percebemos que havia uma oportunidade" não é epifania, é consultoria; o insight tem de ter momento, lugar e gatilho emocional concreto
- **ABT estruturalmente errado** — substituir AND/BUT/THEREFORE por sinónimos ("porém", "assim") destrói a cadência testada por Pixar e South Park; usar a estrutura literal
- **Versão única entregue** — entregar só a versão longa e dizer "adapta conforme necessário" é deixar trabalho a meias; micro/média/completa servem canais diferentes e o cliente vai pedir as outras
- **Story Circle com beats misturados** — colocar o custo (beat 6: TAKE) antes do insight (beat 5: FIND) colapsa a tensão dramática; a ordem dos 8 beats é estrutural, não decorativa
- **Placeholder `<Client>` visível no output final** — indica que o template foi preenchido parcialmente; zero angle-brackets no output entregue ao cliente
- **Prova sem números ou nomes** — "centenas de clientes satisfeitos" é invisível; "1.200 famílias, NPS 71, desde janeiro de 2023" é verificável e credível
- **Struggle inventado ou suavizado** — origem stories sem custo real (dinheiro, tempo, rejeição) soam a marketing; o beat 6 (TAKE) tem de doer ligeiramente para ser verdadeiro
