---
name: dario-email-seq
description: Email sequence generator — welcome, soap opera (Chaperon), indoctrination, launch, post-purchase, re-engagement. Uses copy squad frameworks (Chaperon, Settle, Makepeace, Koe). Triggers on "email sequence", "email campaign", "welcome series", "nurture sequence", "launch sequence".
license: MIT
---

# DARIO Skill — Email Sequence

Designs and writes email sequences matched to the business goal: convert new subs, nurture, launch, re-engage, upsell. Based on Chaperon's Soap Opera, Settle's daily sending, Makepeace's emotion, and Koe's creator patterns.

## When to activate

- Client has opt-in list (even small — 50 subs is enough)
- After lead magnet creation
- Pre-launch of a new product/service
- Cart abandonment flow setup
- Re-engage dormant segment
- Post-purchase onboarding / ascension

## Sequence types

| Type | Length | Goal |
|---|---|---|
| **Welcome / Indoctrination** | 5-7 emails | New sub → first purchase + brand trust |
| **Soap Opera Sequence (SOS)** | 5 emails | Bond + first sale within 5 days |
| **Nurture** | 12+ emails | Long-term relationship, education, soft pitches |
| **Launch** | 7-14 emails | Pre-launch → open cart → close cart urgency |
| **Cart Abandonment** | 3-5 emails | Recover abandoned checkouts |
| **Post-Purchase** | 4-8 emails | Onboard + upsell + review request |
| **Re-engagement** | 3 emails | "Are you still interested?" + final purge |
| **Weekly / Daily Broadcast** | ongoing | Ongoing engagement (Settle / Koe style) |

## Workflow

### 1. Gather inputs
- **List source** (what opt-in? lead magnet?)
- **Offer / product**
- **Avatar**
- **Awareness level** (Schwartz)
- **Brand voice** (tone from `dario-brand` if exists)
- **Sequence type + goal**
- **Length preference**
- **Delivery tool** (ActiveCampaign, ConvertKit, Mailchimp, custom)

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "andre chaperon soap opera sequence storytelling", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "ben settle daily email copywriting", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "clayton makepeace dominant emotion email", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "dan koe creator one person business email", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "jeff walker product launch formula", collection: "dario", limit: 5)
```

### 3. Soap Opera Sequence (SOS) template — Chaperon style

**Day 1 — Set the stage**
- Subject line: curiosity + open loop
- Open: personal story beginning
- Close: open loop that forces next email

**Day 2 — High drama**
- Subject line: continuation
- Open: pickup from day 1
- Middle: raise the stakes / conflict
- Close: cliffhanger

**Day 3 — Epiphany**
- Subject line: revelation
- Middle: the breakthrough moment
- Close: soft hint of solution

**Day 4 — Hidden benefits**
- Subject line: benefit-driven
- Middle: reveal what's possible
- Close: transition to offer

**Day 5 — Urgency + pitch**
- Subject line: "last chance" or direct offer
- Middle: the offer
- Close: strong CTA + P.S. with urgency

### 4. Indoctrination sequence — Brunson style

6-email series that transforms a cold sub into a believer:
1. **Who I am** (origin story, why you started)
2. **Why I'm different** (unique mechanism / contrarian view)
3. **What I believe** (beliefs that differentiate)
4. **How it works** (proof + case studies)
5. **Offer introduction** (soft)
6. **Ask** (direct CTA)

### 5. Launch sequence — Jeff Walker PLF

**Pre-launch (1-2 weeks)**
- Email 1: "Something big is coming" + date tease
- Email 2: Content video 1 — the opportunity
- Email 3: Content video 2 — transformation case study
- Email 4: Content video 3 — the experience (how it works)

**Cart open (5-7 days)**
- Email 5: "Doors are open" + offer detail
- Email 6: FAQ + objection handling
- Email 7: Case study / transformation story
- Email 8: Scarcity reminder + bonuses
- Email 9: "24 hours left"
- Email 10: "Final hours" + last CTA

**Post-launch**
- Email 11: Thank you + onboarding (for buyers)
- Email 12: "Cart closed" (for non-buyers — seed next launch)

### 6. Cart abandonment — 3 email minimum

- **Email 1 (1 hour after abandon):** "Forgot something?" soft reminder + item image
- **Email 2 (24 hours):** Address common objection + social proof
- **Email 3 (48-72 hours):** Urgency ("cart expires in X hours") + incentive (free shipping, bonus)

### 7. Writing principles (copy squad distilled)

**Subject lines**
- Open curiosity gap
- Specific > vague ("You were right about X" > "Update")
- Lowercase often outperforms Title Case
- <50 chars preferred
- Emoji: A/B test, often bad for B2B

**Opens (first sentence)**
- Never "Hi [First Name]"
- Start with a story, a question, or a pattern interrupt
- Reference the subject line to validate the click

**Body**
- Short paragraphs (1-3 lines)
- Conversational voice
- One idea per email
- Prove > claim
- Specific > general

**CTAs**
- One primary CTA per email
- Action verb + outcome
- Also text link in P.S.

**P.S.**
- ALWAYS include
- Restate core benefit OR reveal new hook
- Often the most-read part of the email

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: email-sequence
sequence_type: <sos|indoc|launch|cart|post-purchase|reengage>
length: N emails
---

# Email Sequence — <Client / Offer>

## Strategic Context
- Avatar: ...
- Sequence type: ...
- Goal: ...
- Awareness level: ...
- Voice: ...

## Architecture
| Day | Email | Subject | Main beat | CTA |
|---|---|---|---|---|
| 0 | E1 | ... | Open story | Soft |
| 1 | E2 | ... | ... | ... |
| ... |

---

## EMAIL 1

**Send:** Day 0, immediately after opt-in
**Subject:** ...
**Preview text:** ...

<body>

**P.S.** <ps>

---

## EMAIL 2

**Send:** Day 1
**Subject:** ...

<body>

---

(continua para cada email)

## Automation Rules
- Send time: ...
- Timezone: ...
- Skip rules: ...
- Tag on open/click: ...
- Exit conditions (e.g. if buys, exit sequence and enter "customer onboarding")
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Email Sequence.md`

## Red flags
- "Buy now buy now buy now" (dies in spam)
- Corporate voice ("We at [Company]...") vs conversational
- No personalization beyond first name
- Same CTA in every email (gets ignored)
- 10-paragraph emails (loses mobile readers)
- No P.S.
- Hard sell before relationship (SOS needs 4 emails before pitch)
- Ignoring deliverability (sender reputation, authentication SPF/DKIM/DMARC)

## Interactions
- Depends on `dario-offer` (what's being sold)
- Depends on `dario-brand` (voice)
- Pair with `dario-sales-letter` for the main LP

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Sequence type & strategic fit

- [ ] Sequence type está explicitamente nomeado (SOS / Indoc / Launch / Cart / Post-purchase / Re-engagement)
- [ ] Avatar descrito com dor específica + nível de awareness (Schwartz 1-5)
- [ ] Goal da sequência é mensurável ("converter 3% dos subs em compradores do plano €97")
- [ ] Comprimento (N emails) justificado pela fase do funil — não arbitrário

❌ NOT delivery-ready: "Sequência de boas-vindas para novos subscribers, objetivo: vender o produto."
✅ Delivery-ready: "SOS 5 emails para subs vindos do lead magnet 'Guia Fiscal 2024' — avatar: freelancer PT 28-42 anos, awareness nível 2 (problema-aware) — objetivo: 1ª compra do plano Tributario.AI Starter €29/mês até D5."

---

### Gate 2 — Subject lines testáveis

- [ ] Todas as subject lines têm <50 chars (ou desvio justificado)
- [ ] Curiosity gap verificável — sem vague claims ("novidades", "update")
- [ ] Capitalização intencional (lowercase vs Title Case — escolha feita explicitamente)
- [ ] Preview text escrito para cada email (não deixado em branco)

❌ NOT delivery-ready: `Subject: Newsletter de Maio — Novidades Importantes`
✅ Delivery-ready: `Subject: o dia em que perdi €4.200 ao fisco` / `Preview: não era o que eu esperava de um contabilista`

---

### Gate 3 — Corpo dos emails (copy squad principles)

- [ ] Primeiro parágrafo NÃO começa com "Olá [Nome]" ou saudação genérica
- [ ] Cada email tem ONE dominant idea — sem agenda dupla
- [ ] Parágrafos ≤3 linhas; espaçamento para escaneabilidade mobile
- [ ] Pelo menos 1 elemento de prova por email (número, testemunho, caso real, dado)
- [ ] P.S. presente em TODOS os emails com hook novo ou restate do benefício core

❌ NOT delivery-ready: "Email 2: Fala sobre os benefícios do produto e inclui um CTA para comprar."
✅ Delivery-ready: P.S. "P.S. — Amanhã conto-te como a Ana (contabilista, Porto) passou de 23 clientes manuais para 147 automatizados em 6 semanas. Vai direto ao assunto."

---

### Gate 4 — Arquitetura de sequência (tabela + automation rules)

- [ ] Tabela Architecture preenchida: Day / Email # / Subject / Main beat / CTA type
- [ ] Open loops assinalados entre emails (SOS: cada email fecha com cliffhanger)
- [ ] Automation rules escritas: send time, timezone, exit condition (ex: "se comprar → sai da sequência")
- [ ] Skip rules / tag rules definidas (ex: "tag 'abriu_E2' → segmento quente")

❌ NOT delivery-ready: "Enviar os emails ao longo de 5 dias com CTAs para a página de vendas."
✅ Delivery-ready: "E3 → send D2 10h00 WET; exit condition: tag 'compra_starter' ativa → remove de SOS, entra em Post-Purchase; tag 'abriu_E3' → score +10 em AC."

---

### Gate 5 — CTAs e P.S. estruturados

- [ ] Exatamente 1 CTA primário por email — verbo de ação + outcome explícito
- [ ] CTA repetido como texto link no P.S. (não só botão)
- [ ] Urgência/escassez nos emails de pitch é REAL e verificável (data, quantidade, desconto concreto)
- [ ] Emails de nurture/conteúdo têm CTA soft (reply, poll, "responde a este email") — não pitch forçado

❌ NOT delivery-ready: `[Clica aqui para saber mais]`
✅ Delivery-ready: `→ Reserva o teu lugar no Tributario.AI antes de domingo 23h59 — só 47 vagas no plano de fundadores`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets de placeholder

- [ ] `<client>`, `<avatar>`, `<offer>` substituídos por dados concretos do briefing
- [ ] Datas reais (ex: "D0 = 14 Jul 2025") — não `<YYYY-MM-DD>`
- [ ] Nomes fictícios de provas sociais internamente consistentes (mesma Ana em E2 e E5)
- [ ] Ferramenta de delivery nomeada (ActiveCampaign / ConvertKit / Mailchimp) com campo de merge correto (`{{first_name}}` vs `*|FNAME|*`)

❌ NOT delivery-ready: `project: <client> | avatar: <descrever aqui>`
✅ Delivery-ready: `project: Tributario.AI | date: 2025-07-14 | sequence_type: sos | tool: ActiveCampaign | merge: {{contact.first_name}}`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / memória / dados do cliente
- 🟡 **assumed** — plausível mas precisa confirmação do cliente antes da entrega
- 🟢 **projection** — forecast por design (não verificável até execução)

Output checklist upfront mostra ao reader exatamente o que é trust-as-is vs. o que precisa de verify. **Honest transparency > inflated delivery.**

---

❌ NOT delivery-ready:
> "A sequência de 5 emails tem open rate médio de 42%, o avatar é mulher 35-45 anos empreendedora, e esperamos 180 vendas no lançamento."
*(Nenhum label — reader assume que tudo é verified. Open rate pode ser benchmark genérico, avatar pode ser suposição, vendas são projeção. Sem distinção = risco de decisão errada.)*

✅ Delivery-ready:
> - 🔵 **verified** — Sequência SOS de 5 emails (Chaperon framework, confirmado em sessão anterior com cliente)
> - 🟡 **assumed** — Avatar: mulher 35-45 anos, empreendedora digital (baseado no lead magnet descrito — aguarda validação com pesquisa de lista real)
> - 🟡 **assumed** — Delivery tool: ActiveCampaign (mencionado informalmente — confirmar automações disponíveis no plano actual)
> - 🟢 **projection** — Open rate estimado 38-44% nos primeiros 5 dias (benchmark de lista quente pós opt-in; depende de aquecimento de domínio e segmentação)
> - 🟢 **projection** — Email 5 (pitch) gera 2-4% conversão sobre lista activa (projeção por design — não verificável pré-envio)

---

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados (substituir assumptions com actuals: avatar validado, tool confirmada, tom de voz alinhado com `dario-brand`)
- [ ] Todos os 🔵 sources citados (RAG retrieval de Chaperon / Settle / Makepeace / Walker referenciado na entrega)
- [ ] Todos os 🟢 projections comunicados ao cliente como estimativas — não como garantias de performance

## Fully-worked A-tier example (delivery-ready reference)

```markdown
---
project: Tributario.AI
date: 2025-07-14
type: email-sequence
sequence_type: sos
length: 5 emails
tool: ActiveCampaign
merge_tag: {{contact.first_name}}
---

# Email Sequence — Tributario.AI / Plano Starter €29/mês

## Strategic Context
- Avatar: Freelancer português, 28-42 anos, fatura via recibos verdes,
  perde ~3h/semana em IRS + IVA, awareness nível 2 (sabe que tem dor fiscal,
  não conhece a solução)
- Sequence type: Soap Opera Sequence (Chaperon) — 5 emails, D0→D4
- Goal: 1ª compra Plano Starter €29/mês com conversão-alvo 4% dos subs
- Voice: direto, inteligente, ligeiramente irreverente — sem jargão fiscal

## Architecture

| Day | Email | Subject | Main beat | CTA |
|-----|-------|---------|-----------|-----|
| D0  | E1    | o dia em que perdi €4.200 ao fisco | Origem da dor — open loop | Soft: "reply com 'aconteceu-me'" |
| D1  | E2    | (continuação de ontem) | Escalada do conflito + erro que cometi | Curiosity: "amanhã conto o final" |
| D2  | E3    | o que nenhum contabilista me disse | Epifania — mecanismo único | Soft: ver demo 90 seg |
| D3  | E4    | 147 clientes. 6 semanas. sem CA. | Prova social + benefícios ocultos | Médio: página de vendas |
| D4  | E5    | última hipótese (fecho domingo 23h59) | Urgência real + oferta completa | Hard: comprar Starter |

---

## EMAIL 1

**Send:** D0 — imediatamente após opt-in
**Subject:** o dia em que perdi €4.200 ao fisco
**Preview text:** não era descuido. era o sistema.

Em março de 2022 recebi uma carta dos Finanças.

Devia €4.200 em retenções que "não foram comunicadas
a tempo." Eu tinha os recibos. Tinha tudo guardado.
Mas o prazo tinha passado há 11 dias.

Onze dias.

{{contact.first_name}}, isso não foi azar. Foi o
resultado de gerir a minha situação fiscal com
uma folha de Excel e boa vontade.

Se emites recibos verdes — mesmo que só 2 por mês —
provavelmente já sentiste qualquer coisa parecida.
A sensação de que estás sempre a correr atrás.

Amanhã conto-te o que descobri depois disso.
(Não é o que eu esperava.)

— Ricardo, fundador Tributario.AI

**P.S.** Aconteceu-te algo parecido? Responde a
este email com uma palavra. Leio tudo.

---

## EMAIL 2

**Send:** D1 — 10h00 WET
**Subject:** (continuação de ontem)
**Preview text:** a parte que me custou admitir

Ontem parei no momento em que abri a carta.

Aqui está o resto.

Fui a um contabilista — o quinto em três anos.
Disse-me o mesmo que os outros: "precisa de
organização." Cobrou €80 pela consulta.

Continuei a perder tempo. Continuei a pagar multas.

O problema não era eu. Era o modelo inteiro:
reativo, manual, sempre atrasado face à AT.

Amanhã conto-te o que mudou tudo.
Dica: não foi contratar mais ninguém.

— Ricardo

**P.S.** Se ainda não abriste o e-mail de ontem,
começa por lá — faz mais sentido por ordem.

---

## EMAIL 3

**Send:** D2 — 10h00 WET
**Subject:** o que nenhum contabilista me disse
**Preview text:** porque não é do interesse deles dizer-te

A AT disponibiliza uma API.

Atualiza em tempo real. Tem todos os teus dados
fiscais. Qualquer sistema pode ligá-la.

Nenhum contabilista me disse isso em 6 anos.

O Tributario.AI liga essa API à tua atividade,
calcula as tuas obrigações antes dos prazos,
e avisa-te com 15 dias de antecedência.

Sem folha de Excel. Sem surpresas em março.

Deixa-me mostrar-te como funciona em 90 segundos:
→ [Ver demo — sem registo obrigatório]

— Ricardo

**P.S.** Amanhã mostro-te o caso da Ana —
contabilista que automatizou 147 clientes
com isto. Os números são ridículos.

---

## EMAIL 4

**Send:** D3 — 10h00 WET
**Subject:** 147 clientes. 6 semanas. sem CA.
**Preview text:** ela própria não acreditou no primeiro mês

A Ana Rodrigues tem 34 anos e uma carteira
de 147 clientes de recibos verdes no Porto.

Em janeiro de 2025 usou o Tributario.AI para
automatizar os alertas fiscais de todos eles.

Resultado em 6 semanas:
— 3h de trabalho manual eliminadas por dia
— 0 multas por atraso nos seus clientes
— Net Promoter Score subiu de 6 para 9,1

O plano dela custa €87/mês.
O plano que serve a maioria dos freelancers
começa em €29/mês.

{{contact.first_name}}, o link está aqui:
→ [Tributario.AI Plano Starter — €29/mês]

— Ricardo

**P.S.** Amanhã é o último dia a este preço.
Domingo às 23h59 o Starter sobe para €47/mês.
Não é urgência inventada — é o fim do beta.

---

## EMAIL 5

**Send:** D4 — 09h00 WET
**Subject:** última hipótese (fecho domingo 23h59)
**Preview text:** depois disto o preço não volta

{{contact.first_name}},

Esta é a última vez que falo no preço de €29/mês.

Hoje à meia-noite o Plano Starter passa a €47/mês.
São mais €216/ano — pelo mesmo produto.

O que incluis no Starter:
✓ Ligação à AT em tempo real
✓ Alertas 15 dias antes de cada prazo
✓ Dashboard IRS + IVA + Seg. Social
✓ Suporte por email em 24h

→ [Garantir Plano Starter €29/mês — até 23h59]

Se não for para ti, sem problema.
Mas se saíste da lista sem experimentar,
vais continuar a usar a folha de Excel.

(Eu usei 6 anos. Não recomendo.)

— Ricardo

**P.S.** Garantia de 30 dias, devolução total.
O risco é zero. O preço de €29 não volta.
→ [Último link: Tributario.AI Starter]

---

## Automation Rules

- **Send time:** 10h00 WET (E1 imediato pós opt-in)
- **Timezone:** Europe/Lisbon (ActiveCampaign setting)
- **Exit condition:** tag `compra_starter` ou `compra_pro` → remove
  imediatamente da sequência SOS → entra em Post-Purchase (5 emails)
- **Skip rule:** se `compra` ativa em D3 antes de E5 → cancel E5
- **Tag on open E3:** `interesse_demo` → score +15
- **Tag on click E4/E5:** `hot_lead` → notifica Ricardo via Slack
- **Post-SOS (não comprou):** aguarda 14 dias → entra em Nurture 12 emails
```

---

## Output anti-patterns

- Escrever "Email 1: introdução à empresa, fala dos valores e da missão" — beat sem drama, sem open loop, nenhum leitor passa para E2
- Usar placeholder literal `<avatar>` ou `<client>` no output final entregue ao cliente
- Subject line em Title Case genérico: "Bem-vindo À Nossa Newsletter!" — invisível na inbox
- CTA múltiplo num mesmo email ("vê o blog, segue-nos no Instagram, e compra aqui") — dilui a ação
- P.S. ausente ou repetição literal do CTA do corpo sem novo hook — perde o elemento mais lido
- Urgência fabricada sem data real ("só por tempo limitado!") — destrói credibilidade na sequência inteira
- Sequência de launch sem email de "cart closed" para não-compradores — perde o seed para o próximo lançamento
- Automation rules em branco ou "a preencher" — sequência não é implementável sem elas
- Emails com parágrafos de 8+ linhas sem quebra — ilegíveis em mobile, bounce cognitivo imediato
- Tom corporativo/formal em sequência Soap Opera — mata o storytelling e a ligação emocional
