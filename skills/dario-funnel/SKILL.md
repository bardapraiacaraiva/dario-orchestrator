---
name: dario-funnel
description: Sales funnel builder using Russell Brunson's Value Ladder, DotCom Secrets funnels, and Epiphany Bridge storytelling. Designs the full funnel structure (lead magnet → tripwire → core → profit maximizer). Triggers on "funnel", "funil", "value ladder", "tripwire", "lead magnet", "upsell sequence".
license: MIT
---

# DARIO Skill — Funnel Builder

Designs a complete multi-step sales funnel from lead magnet to profit maximizer. Based on Brunson's DotCom Secrets + Expert Secrets + Traffic Secrets trilogy.

## When to activate
- Client wants "a funnel" (often vague — this skill structures it)
- After `dario-offer` (offer exists, now needs a delivery mechanism)
- E-commerce upsell/cross-sell flow design
- Webinar/challenge funnel planning
- SaaS trial-to-paid conversion flow

## Workflow

### 1. RAG consult
```
mcp__dario-rag__search_kb(query: "brunson value ladder funnel epiphany bridge", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "funnel lead magnet tripwire profit maximizer", collection: "dario", limit: 5)
```

### 2. Identify funnel type
| Funnel | Use when |
|---|---|
| **Lead Magnet → Tripwire → Core** | First-time customer acquisition |
| **Webinar** | High-ticket ($1K+), education-based |
| **Challenge** (5/7 day) | Community, transformation-based |
| **Product Launch (PLF)** | Seasonal launch, waitlist |
| **Ascension** | Existing customers → higher tier |
| **SaaS Trial** | Free trial → paid conversion |

### 3. Design Value Ladder
```
[Lead Magnet — FREE]     → builds trust, captures email
     ↓
[Tripwire — $7-$47]     → converts to buyer, lowers acquisition cost
     ↓
[Core Offer — $97-$997] → main revenue, solves main problem
     ↓
[Profit Maximizer — $997+] → high-ticket, done-for-you, continuity
     ↓
[Return Path]            → email nurture, retargeting, community
```

### 4. Map pages + copy needs
For each step:
- **Landing page** (pairs with `dario-sales-letter`)
- **Thank you / confirmation page** (next step CTA)
- **Email sequence** (pairs with `dario-email-seq`)
- **Upsell page** (one-click, time-limited)
- **Downsell page** (if upsell refused, offer lighter version)

### 5. Tracking + metrics per step
| Step | KPI | Target |
|---|---|---|
| Lead Magnet LP | Opt-in rate | 25-45% |
| Tripwire page | Purchase rate | 5-10% of leads |
| Core offer | CVR from nurture | 2-5% |
| Upsell | Take rate | 15-30% |
| Downsell | Take rate | 10-20% |

## Output template
```markdown
# Funnel Blueprint — <Client / Offer>

## Value Ladder
<visual ladder>

## Step-by-step flow
### Step 1: Lead Magnet
- Page: ...
- Offer: ...
- Email: welcome sequence (5 emails)

### Step 2: Tripwire
...

## Pages needed (with copy briefs)
## Email sequences needed
## Tracking events
## Tech stack (ClickFunnels / WordPress / custom)
## Budget estimate + expected metrics
```

## Epiphany Bridge (Brunson's Storytelling Framework)

Every funnel step needs a story to bridge the gap between "I don't need this" and "I must have this":

1. **Backstory** — Where were you before the transformation?
2. **Wall** — What obstacle did you hit?
3. **Epiphany** — What did you realize / discover?
4. **Plan** — What did you do about it?
5. **Result** — What happened? (specific, measurable)
6. **Transformation** — Who are you now?

Apply this in: lead magnet LP copy, webinar intro, email sequences, sales page.

## Integration

- Runs AFTER `dario-offer` (need a defined offer to build a funnel around)
- Landing page copy pairs with `dario-sales-letter`
- Email sequences pair with `dario-email-seq`
- Traffic plan pairs with `dario-ads-blueprint`
- Tracking/metrics feed into `lucas-analytics`

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Funnel Blueprint.md`

## Red Flags

- Never build a funnel without a validated offer first (use `dario-offer`)
- Never skip the downsell — it recovers 10-20% of lost upsell revenue
- Never launch a funnel without email sequences in place (lead magnet without nurture = wasted leads)
- Always include exit-intent or abandoned cart recovery for paid steps
- Always test the full path (mobile + desktop) before going live
- Value Ladder must have at least 3 levels — a single-product funnel isn't a funnel

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Value Ladder tem ≥3 níveis com preços reais

- [ ] Lead Magnet definido com formato concreto (PDF, mini-curso, quiz, ferramenta)
- [ ] Tripwire tem preço no range €7–€47 (não "preço a definir")
- [ ] Core Offer tem preço real e proposta de valor em 1 frase
- [ ] Profit Maximizer existe, mesmo que como "fase 2 do roadmap"
- [ ] Return Path descrito (email nurture, retargeting ou comunidade)

❌ NOT delivery-ready: `Core Offer — €XXX — resolve o problema principal`
✅ Delivery-ready: `Core Offer — €297 — Consultoria 90min + Plano de Arrecadação Fiscal personalizado (ARRECADA.GOV)`

---

### Gate 2 — Tipo de funnel justificado para o contexto do cliente

- [ ] Funnel type escolhido (Lead Magnet→Tripwire, Webinar, Challenge, PLF, Ascension, SaaS Trial)
- [ ] Justificação explícita: "Usamos Webinar porque ticket médio é €1.200 e audiência precisa de educação"
- [ ] Funnel alternativo descartado com razão (ex: "Challenge descartado — cliente não tem comunidade activa")
- [ ] Adequação ao estágio do negócio (aquisição nova vs. ascension de clientes existentes)

❌ NOT delivery-ready: `Recomendamos um funil de lead magnet para a Cuidai`
✅ Delivery-ready: `Funil Lead Magnet→Tripwire porque Cuidai está em fase de aquisição (0 lista de email), ticket core €197 não justifica webinar`

---

### Gate 3 — Cada step tem página + copy brief + email mapeados

- [ ] Para cada step: nome da página, headline sugerida, CTA principal
- [ ] Thank you / confirmation page tem next-step CTA explícito (não é um beco sem saída)
- [ ] Upsell page descrita com oferta e mecanismo (one-click, timer)
- [ ] Downsell definido (versão lighter da oferta ou payment plan)
- [ ] Sequências de email referenciadas por step (welcome, nurture, sales, pós-compra)

❌ NOT delivery-ready: `Step 2: Página de vendas do tripwire com copy persuasivo`
✅ Delivery-ready: `Step 2: Página tripwire "Kit Contratos Caninos" €17 — headline: "Protege o teu negócio em 10 minutos" — CTA: "Descarregar agora" — upsell: Consulta 30min €47 — downsell: template único €9 (Lisbon Dog Care)`

---

### Gate 4 — Epiphany Bridge aplicado a ≥1 step com estrutura completa

- [ ] Backstory identificada com contexto específico do avatar do cliente
- [ ] Wall descrito como obstáculo real (não genérico)
- [ ] Epiphany é uma "descoberta" concreta, não uma feature do produto
- [ ] Resultado inclui métrica ou timeframe verificável
- [ ] Transformação posiciona o cliente como "novo eu" — aplicada no copy do Lead Magnet LP ou webinar intro

❌ NOT delivery-ready: `Usa storytelling para conectar com a audiência e aumentar conversões`
✅ Delivery-ready: `Epiphany Bridge — SAQUEI: Backstory: "Trabalhei 3 anos a tentar crédito bancário, sempre recusado" → Wall: "IHAB score bloqueava tudo" → Epiphany: "Descobri que haveres penhorados valem mais do que pensei" → Resultado: "€23.000 em 11 dias" → Transformação: "Agora nego, não peço"`

---

### Gate 5 — KPIs por step com benchmarks e stack técnico definido

- [ ] Opt-in rate target no Lead Magnet LP (benchmark: 25–45%)
- [ ] Purchase rate Tripwire (benchmark: 5–10% dos leads)
- [ ] Upsell take rate (benchmark: 15–30%) e downsell take rate (benchmark: 10–20%)
- [ ] Tracking events listados (ex: `lead`, `purchase`, `upsell_accepted`, `downsell_accepted`)
- [ ] Stack técnico escolhido: ClickFunnels / Systeme.io / WordPress+WooCommerce / custom — com justificação de custo/prazo

❌ NOT delivery-ready: `Monitorizar as conversões em cada etapa do funil`
✅ Delivery-ready: `Atrium — Stack: Systeme.io (€27/mês, limite 2k contactos adequado para fase 1) — eventos GA4: lead_captured, tripwire_purchased, upsell_shown, upsell_accepted — target Q1: opt-in 32%, tripwire CVR 7%`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero placeholders com angle-brackets

- [ ] `<Client / Offer>` substituído por nome real do cliente e nome da oferta
- [ ] Nenhum `<preencher>`, `<a definir>`, `<inserir preço>` no documento final
- [ ] Budget estimate inclui número real (€ ou range justificado), não "a orçamentar"
- [ ] Save location tem data real e nome do cliente (ex: `2025-06-15 - Tributario.AI - Funnel Blueprint.md`)
- [ ] Red flags do skill verificadas: offer validado antes do funnel, downsell presente, email sequences referenciadas

❌ NOT delivery-ready: `# Funnel Blueprint — <Client> / <Offer Name>`
✅ Delivery-ready: `# Funnel Blueprint — Tributario.AI / "Auditoria Fiscal Express" — Junho 2025`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Funnel Blueprint — Pupli / "Primeiro Ano Sem Stress"

**Data:** 2025-06-15
**Funnel type:** Lead Magnet → Tripwire → Core Offer
**Justificação:** Pupli está em aquisição (lista email < 500), ticket core €197,
sem comunidade activa → webinar/challenge descartados para fase 1.

---

## Value Ladder

[FREE] Guia PDF "7 Erros que os Pais de Cachorro Cometem na 1ª Semana"
   ↓  (opt-in 30–40% estimado)
[€17] Pack "Rotina Perfeita" — 3 templates de treino + checklist veterinário
   ↓  (CVR 7% dos leads)
[€197] Programa "Primeiro Ano Sem Stress" — 6 semanas vídeo + suporte WhatsApp
   ↓  (CVR 3% do nurture)
[€497] VIP "Treinador na Tua Casa" — 2 sessões presenciais Lisboa + plano personalizado
   ↓
[Return Path] Newsletter semanal "Pupli Semanal" + retargeting Meta Ads segmento "engajou mas não comprou"

---

## Step-by-step flow

### Step 1 — Lead Magnet (GRÁTIS)
- **Página:** Landing page simples, sem menu
- **Headline:** "7 Erros que os Pais de Cachorro Cometem na 1ª Semana (e como evitá-los)"
- **Sub-headline:** "Guia PDF gratuito — lê em 8 minutos, aplica hoje"
- **CTA:** "Enviar o guia para o meu email"
- **Thank you page:** "O guia está no teu email! Enquanto esperas — vê isto 👇"
  → redireciona para Step 2 (Tripwire) imediatamente
- **Email #1 (imediato):** entrega do guia + teaser do Pack Rotina Perfeita

### Step 2 — Tripwire (€17)
- **Página:** Sales page curta (scroll = 2 ecrãs mobile)
- **Headline:** "Chega de improvisar — a rotina que funciona desde o dia 1"
- **Oferta:** Pack "Rotina Perfeita" — 3 templates editáveis (alimentação, treino,
  vet) + checklist "Primeira Semana"
- **CTA:** "Quero o Pack por €17"
- **Upsell (one-click, imediato pós-compra):** "Adiciona uma consulta de
  30 minutos com treinador certificado por +€47" — timer 15 min
- **Downsell (se recusar upsell):** "Só o template de treino por €9"
- **Thank you page:** acesso imediato + email de boas-vindas comprador

### Step 3 — Core Offer (€197)
- **Trigger:** email nurture (sequência 7 emails, dias 3–14 após lead magnet)
- **Página:** Sales page completa (pairs com dario-sales-letter)
- **Headline:** "O programa que transforma 6 semanas de caos em 1 ano de alegria"
- **CTA:** "Entrar no Programa — €197"
- **Upsell:** upgrade para VIP €497 (diferença €300) — "Adiciona 2 sessões
  presenciais em Lisboa"
- **Downsell:** payment plan 3x €72

### Step 4 — Profit Maximizer (€497)
- **Activação:** pós-compra Core Offer (email dia 7 do programa) + Ascension
  aos leads quentes que não compraram Core
- **Oferta:** 2 sessões presenciais Lisboa + plano personalizado 12 meses
- **Limitação:** "Apenas 6 vagas por mês (agenda do treinador)"

---

## Epiphany Bridge — Lead Magnet LP copy

**Backstory:** "Quando trouxemos a Luna para casa, eu estava convicto de que sabia
o que estava a fazer. Tinha visto os vídeos todos."
**Wall:** "Na terceira noite sem dormir, com a cozinha destruída, percebi que não
fazia ideia nenhuma."
**Epiphany:** "Um amigo treinador mostrou-me que cães novos não precisam de
disciplina rígida — precisam de previsibilidade."
**Plano:** "Criei uma rotina de 3 blocos diários. 20 minutos total."
**Resultado:** "Em 11 dias a Luna dormia a noite toda. Em 3 semanas parou de
morder os móveis."
**Transformação:** "Deixei de ser o dono stressado para ser o dono que os vizinhos
pedem conselhos."

---

## Sequências de email (pairs com dario-email-seq)

| Sequência | Trigger | Nº emails | Objectivo |
|---|---|---|---|
| Welcome | Opt-in Lead Magnet | 5 emails (dias 0–4) | Entregar valor, introduzir Tripwire |
| Nurture→Core | Tripwire comprado | 7 emails (dias 3–14) | Vender Core Offer €197 |
| Pós-compra Core | Core comprado | 3 emails (dias 1,3,7) | Onboarding + upsell VIP |
| Re-engagement | Inactivo 21 dias | 3 emails | Reactivar ou limpar lista |

---

## Tracking events (GA4 + Meta Pixel)

| Evento | Trigger | Valor |
|---|---|---|
| `lead_captured` | Submit opt-in form | — |
| `tripwire_viewed` | Pageview Step 2 | — |
| `tripwire_purchased` | Compra €17 | €17 |
| `upsell_shown` | Thank you page Step 2 | — |
| `upsell_accepted` | Compra upsell €47 | €47 |
| `downsell_accepted` | Compra downsell €9 | €9 |
| `core_purchased` | Compra Core €197 | €197 |

---

## Tech stack

**Stack escolhido:** Systeme.io €27/mês
**Justificação:** Pupli fase 1 (<2.000 contactos), orçamento limitado, Systeme.io
inclui funil + email + checkout numa plataforma — evita integrar 3 ferramentas.
**Alternativa fase 2 (>2k leads):** migrar checkout para Hotmart, manter Systeme
para email.

---

## Budget estimate & métricas esperadas (Q3 2025)

| Item | Custo |
|---|---|
| Systeme.io | €27/mês |
| Copy + design landing pages (3 páginas) | €400 único |
| Guia PDF design | €150 único |
| **Total setup** | **~€550 + €27/mês** |

| KPI | Target |
|---|---|
| Opt-in rate Lead Magnet LP | 32% |
| Tripwire CVR | 7% dos leads |
| Upsell take rate | 20% |
| Core CVR (do nurture) | 3% |
| LTV médio por lead | ~€31 |

---

**Save:** `05 - Claude - IA/Outputs/2025-06-15 - Pupli - Funnel Blueprint.md`
```

---

## Output anti-patterns

- **Value Ladder com 1 ou 2 níveis** — uma oferta + upsell não é um funil; falta o return path e o profit maximizer
- **Preços como placeholders** — `€XX`, `a definir com o cliente`, `preço TBD` tornam o blueprint inutilizável para implementação
- **Epiphany Bridge genérico** — "antes estava perdido, agora estou bem" sem backstory específica, wall concreto ou resultado mensurável
- **Funnel type não justificado** — entregar um webinar funnel a um cliente com ticket de €47 sem explicar a escolha
- **Thank you pages como beco sem saída** — ausência de next-step CTA na confirmation page desperdiça o momento de maior intenção
- **Downsell omitido** — ignorar o downsell pode custar 10–20% da receita do upsell; sempre presente, mesmo que simples
- **Stack técnico não especificado** — "usa uma plataforma de funis" não é accionável; cliente precisa de nome, custo e justificação
- **Email sequences "a criar depois"** — funil entregue sem sequências mapeadas = leads capturados sem nurture = lista fria
- **KPIs sem benchmarks de referência** — targets como "alta taxa de conversão" sem número não permitem avaliar performance real
- **Funnel construído sem offer validado** — blueprint entregue antes de `dario-offer` confirmar que a proposta de valor existe e tem procura
