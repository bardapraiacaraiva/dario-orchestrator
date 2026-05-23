---
name: dario-sales-letter
description: Long-form sales letter generator using Halbert / Schwartz / Kennedy / Brunson frameworks. Takes a Grand Slam Offer and produces full sales copy with headline sweep, body, CTA. Triggers on "sales letter", "carta de vendas", "long-form copy", "VSL script", "landing page copy".
license: MIT
---

# DARIO Skill — Sales Letter

Writes high-conversion long-form sales copy for a product or service. Pairs naturally after `dario-offer`. Works for written sales pages, VSL scripts, and email long-form.

## When to activate

- User has a Grand Slam Offer ready and wants copy
- Rewrite of underperforming sales page
- Launch copy for new service
- VSL script needed
- Long-form email (Solo broadcast, newsletter deep-dive)

## Workflow

### 1. Gather inputs
- **The offer** (output of `dario-offer` ideally)
- **Target avatar** (as specific as possible)
- **Awareness level** (Schwartz):
  - 1. Unaware (don't know they have a problem)
  - 2. Problem-aware (know problem, not solution)
  - 3. Solution-aware (know solutions exist)
  - 4. Product-aware (know your product)
  - 5. Most-aware (just need offer/push)
- **Market sophistication** (Schwartz):
  - Stage 1: first to make the claim
  - Stage 2: bigger claim than competitors
  - Stage 3: mechanism ("here's HOW we do it")
  - Stage 4: bigger mechanism
  - Stage 5: identification / experience (most mature)
- **Dominant emotion** (fear, greed, guilt, shame, pride, hope)
- **Proof elements** (testimonials, results, screenshots, credentials)

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "eugene schwartz awareness levels sophistication", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "gary halbert sales letter structure", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "dan kennedy 3ms market message media", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "russell brunson epiphany bridge vsl", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "hopkins claude scientific advertising", collection: "dario", limit: 5)
```

### 3. Choose framework based on awareness level

| Awareness | Framework | Pattern |
|---|---|---|
| 1 (unaware) | Halbert problem-entry | Lead with a story of someone similar to avatar hitting the problem |
| 2 (problem-aware) | PAS + amplification | Problem → Agitate → Solve |
| 3 (solution-aware) | Unique Mechanism | "Others try X, we do Y because..." |
| 4 (product-aware) | Proof-stacking | Case studies, side-by-sides, direct comparison |
| 5 (most-aware) | Offer-first + urgency | Get straight to the deal + scarcity |

### 4. Headline sweep (20 minimum)
Generate at least 20 headline variations covering:
- News / Curiosity
- Benefit-driven (specific outcome + timeframe)
- Question-based
- Shock / bold claim
- Testimonial-style
- "How to" / "Why"
- Negative framing ("stop doing X")
- Numbers / list-style
Pick top 3 for A/B consideration.

### 5. Body structure (Halbert 22-step condensed)
1. **Headline** — grab attention
2. **Subheadline** — extend the promise
3. **Lead** — hook the reader (story / stat / question)
4. **Problem amplification** — make them feel the cost of inaction
5. **Transition: story of discovery** — "I was in the same place until..."
6. **Introduce the mechanism** — why this is different
7. **Social proof** — testimonials, case studies
8. **Specific benefits** — bullet list (fascination bullets)
9. **The offer** — what you get
10. **Bonus stack** — total value
11. **Price reveal** — anchor high, reveal "real" price
12. **Guarantee** — reverse risk
13. **Urgency / scarcity** — why now
14. **CTA** — specific, action-oriented
15. **P.S.** — restate key promise + CTA

### 6. Fascination bullets (Lampropoulos / Makepeace style)
Each bullet:
- Promises a specific outcome
- Creates curiosity (open loop)
- Is specific (number, time, place)
- Example: "The 'weird Tuesday trick' that saved me €4,200 in legal fees — page 47"

Generate 15-25 of these. Keep best 10-15 for the page.

### 7. CTA
- Specific verb + outcome ("Apply Now — See If You Qualify")
- Not generic ("Submit", "Click Here")
- Accompanied by risk-reversal ("100% money back if...")
- First CTA after ~40% of the read, again at 70%, final at end

### 8. Proof elements placement
- Above fold: 1 social proof element (logo bar, testimonial snippet, result number)
- Middle: deep case study (1-2)
- Near CTA: risk-reversal + guarantee
- Before price: "others who tried this" montage

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: sales-letter
awareness_level: <1-5>
sophistication_stage: <1-5>
framework: <halbert|pas|unique-mechanism|proof-stack|offer-first>
---

# Sales Letter — <Product / Service>

## Strategic Context
- Avatar: ...
- Awareness: ...
- Sophistication: ...
- Dominant emotion: ...
- Dream outcome: ...

## Headline Options (Top 3)
1. ...
2. ...
3. ...

## Subheadline
...

---

## FULL COPY

[HEADLINE]

[SUBHEADLINE]

<opening hook — 150-300 words>

<problem amplification — 300-500 words>

<transition + discovery story — 300-500 words>

<introduce unique mechanism — 200-400 words>

<social proof block 1>

<specific benefits — fascination bullets>
- ...
- ...
- (15+ bullets)

<deep case study>

[CTA 1 — mid-page]

<more proof / objection handling>

<offer reveal>

<bonus stack>

<price anchor + reveal>

<guarantee>

<urgency / scarcity>

[CTA 2 — final]

<P.S. — restate main promise + CTA>

---

## Versions to A/B test
1. Headline variant A vs B
2. Guarantee wording
3. Price anchor style
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Sales Letter.md`

## Red flags
- Vague benefits ("better results") instead of specific ("add 3.2kg muscle in 90 days")
- Hopium (promising things you can't deliver)
- Walls of text without subheadings / bullets / breaks
- Starting with "we" or "our" (always start with reader)
- Feature list instead of benefit list
- Single CTA at the bottom only
- No P.S.
- Using "exclusive", "secret", "revolutionary" (instant credibility killer)

## Red Flags
- Never write sales copy without first identifying the audience's awareness level (Schwartz 1-5) — copy pitched at the wrong awareness stage either bores or confuses the reader
- Never skip the headline sweep (minimum 20 variations) — the headline accounts for 80% of whether the page gets read, and the first draft is almost never the best
- Always include specific proof elements (testimonials with names, exact numbers, case studies) — vague claims like "amazing results" trigger skepticism and kill conversions
- Never start the copy with "we" or "our company" — the reader only cares about themselves, and self-centered openings signal that you do not understand their world
- Always place at least 3 CTAs throughout the letter (40%, 70%, end) — a single CTA at the bottom means everyone who drops off mid-page never sees the action step
- Never promise outcomes you cannot substantiate — hopium copy generates refunds, chargebacks, and reputation damage that far exceed any short-term revenue

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Strategic inputs documentados e coerentes
- [ ] Avatar definido com especificidade cirúrgica (cargo, dor concreta, situação actual)
- [ ] Awareness level (1-5 Schwartz) e sophistication stage (1-5) declarados no front-matter
- [ ] Dominant emotion identificada e reflectida no lead (fear, greed, guilt, shame, pride, hope)
- [ ] Framework escolhida bate certo com o awareness level da tabela do skill
- ❌ NOT delivery-ready: `Avatar: empreendedores. Awareness: 3. Framework: PAS.`
- ✅ Delivery-ready: `Avatar: fundadores de SaaS B2B, 2-8 FTE, MRR €8k-€25k, bloqueados em churn >6%/mês. Awareness: 3 (sabem que existe software de CS, não sabem do mecanismo). Framework: Unique Mechanism.`

### Gate 2 — Headline sweep com pelo menos 20 variações + top 3 destacados
- [ ] Mínimo 20 headlines geradas cobrindo os 8 tipos (news, benefit, question, shock, testimonial, how-to, negative, numbers)
- [ ] Top 3 escolhidos e justificados (qual tipo, por que encabeça dado o awareness)
- [ ] Nenhum headline com benefício vago — cada um tem número, prazo ou mecanismo concreto
- [ ] Subheadline estende a promessa sem a repetir
- ❌ NOT delivery-ready: `"Transforma o teu negócio com a nossa solução inovadora"`
- ✅ Delivery-ready: `"Como 14 contabilistas portugueses pararam de perder clientes para a AT — sem contratar mais nenhum técnico — em 47 dias"`

### Gate 3 — Body segue estrutura Halbert 15-step com wordcounts respeitados
- [ ] Lead (hook) tem 150-300 palavras, abre com o leitor — não com "nós" ou "a nossa empresa"
- [ ] Problem amplification (300-500 palavras) quantifica o custo de inacção (€, tempo, riscos)
- [ ] Transition + discovery story (300-500 palavras) presente e credível (não genérica)
- [ ] Unique mechanism nomeado e explicado (200-400 palavras) — não é feature, é mecanismo causal
- [ ] P.S. presente e reafirma promessa principal + CTA
- ❌ NOT delivery-ready: Lead começa com "Somos a Tributario.AI, fundada em 2022, e temos uma solução..."
- ✅ Delivery-ready: Lead começa com "Era uma sexta-feira às 17h quando o Miguel percebeu que acabara de perder o terceiro cliente em dois meses por causa de um erro na IES que podia ter sido evitado em 4 minutos..."

### Gate 4 — Fascination bullets (15-25) passam no teste Lampropoulos
- [ ] Cada bullet promete outcome específico + abre curiosidade (open loop)
- [ ] Pelo menos 80% têm número, data, página, nome ou lugar concreto
- [ ] Zero bullets começam com "Aprende como..." ou "Descobre..." genérico sem gancho
- [ ] Best 10-15 seleccionados e ordenados por impacto emocional decrescente
- ❌ NOT delivery-ready: `• Como poupar dinheiro nos impostos com as nossas dicas exclusivas`
- ✅ Delivery-ready: `• O "erro de categoria" que faz 73% dos freelancers portugueses pagar IVA a mais — e como o SAQUEI corrige automaticamente antes do prazo trimestral`

### Gate 5 — Proof stack posicionado correctamente + CTA triplo
- [ ] Prova acima do fold: logo bar, resultado numérico ou snippet de testemunho
- [ ] Case study profundo (mid-body) com antes/depois quantificado
- [ ] Garantia de inversão de risco declarada perto do CTA (não só no rodapé)
- [ ] 3 CTAs presentes: ~40%, ~70%, final — cada um com verbo específico + outcome
- [ ] Urgência/escassez tem razão real declarada (vagas, prazo, cohort) — não "oferta limitada" vazio
- ❌ NOT delivery-ready: `[CTA] Comprar agora` (único, no final, sem garantia visível)
- ✅ Delivery-ready: `[CTA mid-page] "Quero garantir o meu lugar na cohort de Setembro — 4 de 12 vagas disponíveis" + "Garantia total 30 dias: se não reduzires o tempo de fecho em 20%, devolvemos tudo"`

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero angle-brackets de placeholder
- [ ] Front-matter: `project:`, `date:`, `awareness_level:`, `framework:` todos preenchidos — nenhum `<valor>`
- [ ] Nome do produto/serviço real aparece na headline escolhida e nos bullets
- [ ] Testemunhos têm nome próprio + resultado numérico (não "Cliente satisfeito")
- [ ] Save path reflecte data real + nome real do cliente
- ❌ NOT delivery-ready: `project: <client> | "A <product> vai transformar o teu <problema>"`
- ✅ Delivery-ready: `project: Cuidai | date: 2025-06-11 | "Como a Cuidai ajudou 38 famílias de Lisboa a encontrar cuidador sénior em menos de 72h — com contrato, seguro e avaliação diária incluídos"`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
---
project: SAQUEI
date: 2025-06-11
type: sales-letter
awareness_level: 3
sophistication_stage: 3
framework: unique-mechanism
---

# Sales Letter — SAQUEI Pro (Plano Anual)

## Strategic Context
- Avatar: Freelancer português, 28-42 anos, facturação €2k-€6k/mês, recibos verdes,
  gasta 3-5h/mês a tentar perceber quanto deve à AT, já levou pelo menos 1 multa
- Awareness: 3 — sabe que existem apps de gestão, nunca confiou em nenhuma
  o suficiente para pagar
- Sophistication: 3 — já viu "automatiza os teus impostos", precisa do mecanismo real
- Dominant emotion: medo (ser apanhado pela AT, pagar a mais sem saber)
- Dream outcome: acabar cada trimestre a saber exactamente o que deve — sem surpresas

## Headline Options (Top 3)
1. [CHOSEN] "O Único App que Lê os Teus Recibos Verdes e Calcula o IVA Trimestral
   em Tempo Real — Antes que a AT o faça por ti" *(Unique Mechanism + medo implícito)*
2. "Como 2.300 Freelancers Portugueses Pararam de Adivinhar os Impostos
   — e Pouparam em Média €743/ano" *(Prova social + número específico)*
3. "Aviso aos Recibos Verdes: A AT Mudou as Regras do IVA em Janeiro.
   Sabes se Estás em Conformidade?" *(News + urgência real)*

## Subheadline
Sem contabilistas. Sem Excel. Sem sustos no fim do trimestre.
O SAQUEI liga-se ao teu portal das finanças e mantém tudo actualizado — automaticamente.

---

## FULL COPY

# O Único App que Lê os Teus Recibos Verdes e Calcula o IVA Trimestral em Tempo Real — Antes que a AT o faça por ti

### Sem contabilistas. Sem Excel. Sem sustos no fim do trimestre.

---

Era uma segunda-feira de Março quando a Inês — designer freelancer no Porto,
€3.400/mês de facturação média — abriu o portal das Finanças e encontrou
uma dívida de €1.847 que não estava à espera.

Não era fraude. Não era erro da AT.

Era o IVA de dois trimestres acumulado porque ela, como a maioria dos
freelancers em Portugal, calculava "à vista" e ficava sempre um pouco abaixo.

Três semanas depois, a Inês usava o SAQUEI. Hoje fecha cada trimestre
com o valor exacto a pagar — até ao cêntimo — antes do prazo.

**Se já sentiste aquele aperto no estômago quando abres o e-mail da AT,
continua a ler. Isto é para ti.**

---

### O problema não és tu. É o sistema.

Os recibos verdes em Portugal foram desenhados para simplificar.
Na prática, criaram uma armadilha silenciosa para quem trabalha sozinho:

- O regime simplificado aplica coeficientes que mudam consoante a actividade
- O IVA trimestral tem datas que chocam com outros prazos (IRS, segurança social)
- A isenção do artigo 53.º tem limites que nem sempre são comunicados a tempo
- Uma actualização de tabelas em Outubro pode mudar o que deves em Dezembro

O resultado? **73% dos freelancers portugueses pagam IVA a mais ou a menos
em pelo menos um trimestre por ano** — não por descuido, mas por falta de
visibilidade em tempo real.

O custo médio de um erro corrigido pela AT: €340 em juros e coimas.
O custo médio de pagar a mais sem saber: €520/ano que podia ter ficado
no teu bolso.

Soma os dois. São €860 por ano a "usar" um sistema que devia ser simples.

---

### Eu estava no mesmo lugar

Fundámos o SAQUEI depois de o nosso próprio CTO — também freelancer,
também recibos verdes — receber uma notificação da AT a cobrar €2.100
de IVA em atraso de um ano em que tinha facturado "à letra da lei".

O problema não era conhecimento. Era ausência de dados em tempo real.

Consultámos 14 contabilistas. Percebemos que todos eles usavam o mesmo
método: esperar pelo fim do trimestre, exportar dados, calcular.

**Retroactivo. Sempre retroactivo.**

Então construímos o mecanismo inverso.

---

### O Mecanismo SAQUEI: Cálculo Prospectivo em Tempo Real

A diferença entre o SAQUEI e qualquer outra solução no mercado não é
a interface. É a direcção do cálculo.

Todos os outros apps olham para trás: pegam nos teus recibos emitidos
e dizem "deves isto".

O SAQUEI olha para a frente: liga-se ao teu portal das Finanças via API
certificada pela AT, lê os recibos à medida que são emitidos, e actualiza
o teu dashboard fiscal **em tempo real** — com alertas 21 dias antes
de cada prazo trimestral.

Resultado: nunca chegas ao fim do trimestre a adivinhar.

---

### Quem já usa o SAQUEI

> "Fechei o primeiro trimestre de 2025 com €0 de surpresas.
> Literalmente. O app avisou-me em Fevereiro que estava em €1.240
> de IVA acumulado e ajustou quando emiti mais um recibo em Março.
> Paguei €1.318. Era exactamente isso."
> — **Tomás Ferreira, consultor de marketing, Lisboa**

> "Poupei €680 em 2024 só por perceber que estava a aplicar
> o coeficiente errado na minha actividade. O SAQUEI detectou
> ao fim de 3 dias de uso."
> — **Catarina Sousa, copywriter freelance, Porto**

**+2.300 freelancers portugueses. €743 poupados em média no primeiro ano.**

---

### O que o SAQUEI Pro inclui

- ✅ Sincronização automática com o portal das Finanças (AT-certificado)
- ✅ Dashboard IVA em tempo real — actualizado a cada emissão de recibo
- ✅ Alertas 21 dias antes de cada prazo (IVA + IRS + Seg. Social)
- ✅ Detecção automática do regime correcto para a tua actividade CAE
- ✅ Relatório trimestral exportável para o teu contabilista (formato .csv + PDF)
- ✅ Histórico fiscal 5 anos para qualquer inspecção

---

### Fascination bullets — o que vais descobrir

- O "coeficiente fantasma" que faz 1 em cada 3 designers freelance
  pagar IRS a mais — e como o SAQUEI o corrige em 90 segundos
- A data exacta em que deves emitir o último recibo do trimestre
  para não ultrapassar o limiar do artigo 53.º (específico para a tua
  facturação — o app calcula por ti)
- Porque razão pagar o IVA em Fevereiro em vez de Março te pode
  poupar até €180 em juros de mora — e o alerta que o SAQUEI envia
  quando faz sentido fazê-lo
- O erro de categoria de actividade que a AT corrigiu em 2023 e que
  ainda afecta freelancers registados antes de Julho desse ano
- Como exportar o teu relatório fiscal num formato que qualquer
  contabilista entende — sem uma reunião de 1h para explicar o contexto
- A função "E se?" que te deixa simular quanto IVA deves SE emitires
  mais €2.000 este mês — antes de aceitar o projeto

---

### Caso de estudo: Pedro Costa, fotógrafo, Braga

**Antes do SAQUEI:**
- 4-5h/mês a fazer Excel com recibos
- 2 trimestres em 2023 com erro de cálculo → €490 de coima
- Nunca sabia o saldo fiscal real em tempo real

**Depois (3 meses de SAQUEI Pro):**
- 0h de gestão manual (sincronização automática)
- Q1 2024: €0 de surpresas, IVA pago no valor exacto
- Descobriu que podia poupar €340/ano mudando o CAE secundário

**ROI calculado pelo Pedro: 11x o custo anual do SAQUEI no primeiro ano.**

---

**[CTA 1 — 40% da página]**

> ### Activa o SAQUEI Pro Agora — 14 Dias Grátis, Sem Cartão
> *Sincronização com o teu portal das Finanças em menos de 4 minutos*

---

### "Mas já tentei outros apps e não funcionou"

Percebemos. Há três razões pelas quais os outros apps desiludem:

1. **Não sincronizam em tempo real** — importas dados manualmente ou
   esperas pelo fim do mês
2. **Não conhecem as especificidades portuguesas** — são soluções
   internacionais adaptadas, sem lógica dos coeficientes do regime simplificado
3. **Não avisam com antecedência** — mostram o que deves, não o que
   vais dever

O SAQUEI foi construído em Portugal, para recibos verdes portugueses,
pela equipa que processou mais de 180.000 recibos verdes em 2024.

---

### O que tens hoje

| | Valor Individual |
|---|---|
| SAQUEI Pro — acesso anual | €197 |
| Relatórios trimestrais ilimitados | €0 (incluído) |
| Alerta de prazos multi-canal (app + email + SMS) | €0 (incluído) |
| Suporte via chat — resposta <4h dias úteis | €0 (incluído) |
| Migração assistida dos teus dados históricos | €0 (incluído) |
| **Valor total** | **€197** |

**Hoje, como leitor desta página: €147/ano**

*(Equivale a €12,25/mês — menos do que uma consulta de 30 minutos
com um contabilista)*

---

### Garantia Dupla SAQUEI

**Garantia 1 — Precisão ou devolvemos:**
Se o SAQUEI calcular o teu IVA trimestral com erro superior a €10
em relação ao valor real da AT, devolvemos o valor anual completo.

**Garantia 2 — 30 dias sem risco:**
Experimenta o SAQUEI Pro por 30 dias. Se não achares que vale
pelo menos 10x o preço em tempo poupado e tranquilidade,
basta enviares um email — devolução em 48h, sem perguntas.

---

### Por que agora

As declarações de IVA do Q2 2025 vencem a **15 de Agosto**.

Freelancers que activam o SAQUEI Pro hoje têm dados em tempo real
para os recibos de Junho e Julho — os dois meses que mais erros
geram por acumulação.

**Activações com desconto (€147 vs €197): encerram a 30 de Junho.**

---

**[CTA 2 — Final]**

> ### Quero Fechar o Q2 Sem Surpresas — Activar Agora por €147
> *Acesso imediato · Sincronização em 4 min · Garantia 30 dias*

---

**P.S.** — O próximo prazo de IVA é daqui a 65 dias. Os freelancers
que usam o SAQUEI já sabem exactamente o que vão pagar. Os que não
usam vão descobrir no fim de Julho — quando já não dá para ajustar.
Activa hoje, são 4 minutos. Se não ficar satisfeito, devolvemos tudo.
[Garantir o meu acesso agora →]
```

---

## Output anti-patterns

- **Vague benefit lead** — abrir com "somos a empresa X e temos uma solução inovadora" em vez de começar com o leitor ou uma história de avatar
- **Awareness mismatch** — usar framework Offer-First (nível 5) com audiência unaware (nível 1) que ainda não reconhece o problema
- **Bullets de feature disfarçados de benefit** — "Inclui dashboard avançado" em vez de outcome quantificado com mecanismo
- **Single CTA syndrome** — apenas um botão no final, sem CTAs ao ~40% e ~70% do scroll
- **Hopium sem âncora** — prometer "dobra o teu negócio em 30 dias" sem testemunhos, dados ou mecanismo que suporte a claim
- **Urgência fabricada** — "oferta por tempo limitado!" sem razão real (data de cohort, número de vagas, prazo fiscal concreto)
- **Garantia escondida** — mencionada uma vez no final em letra pequena, em vez de posicionada como argumento perto do CTA
- **P.S. ausente ou genérico** — "Obrigado por ler!" em vez de reafirmar a promessa principal + CTA + razão para agir agora
- **Placeholders entregues** — front-matter com `<client>`, `<date>`, `<produto>` não preenchidos no output final
- **Wall of text** — blocos de 500+ palavras sem subheadings, bullets ou quebras visuais que guiem a leitura
