---
name: "A360 Business Model Design"
description: "Design a complete business model — revenue streams, pricing strategy, unit economics, cost structure, value chain, competitive moat, and scalability assessment. From idea to viable business architecture."
version: "1.0"
agent: "A360 — Accelera 360"
category: "Phase 2 — Validation"
license: SEE-LICENSE
parent_agent: a360-director
compliance: [audit_immutable]
---

# A360 Business Model Design

## Triggers

Activate this skill when the user says any of:
- "business model", "modelo de negocio"
- "revenue model", "modelo de receita"
- "pricing strategy", "estrategia de precos"
- "unit economics", "economia unitaria"
- "how will I make money?", "como vou ganhar dinheiro?"
- "cost structure", "estrutura de custos"
- "scalability", "escalabilidade"
- Any request to design the financial and operational backbone of a business

## Frameworks & References

- **Alex Osterwalder** (Business Model Canvas) — 9 building blocks
- **Alex Hormozi** ($100M Offers) — pricing based on value, not cost
- **Eric Ries** (Lean Startup) — validated learning, pivot points, innovation accounting
- **Peter Thiel** (Zero to One) — monopoly characteristics, 10x value
- **Hamilton Helmer** (7 Powers) — counter-positioning, switching costs, network effects, scale economies, branding, cornered resource, process power
- **Patrick Campbell** (ProfitWell) — pricing methodology, value metrics

## Workflow

### Step 1: Business Model Canvas (Osterwalder)

Fill each of the 9 blocks:

| Block | Description | Your Answer |
|-------|-------------|-------------|
| **Customer Segments** | Who are you serving? | [from a360-avatar] |
| **Value Propositions** | What unique value? | [from a360-oferta or hypothesis] |
| **Channels** | How do you reach them? | [from a360-funil] |
| **Customer Relationships** | How do you retain? | [self-serve/personal/automated] |
| **Revenue Streams** | How do you earn? | [see Step 2] |
| **Key Resources** | What assets needed? | [tech/people/IP/capital] |
| **Key Activities** | What must you do daily? | [development/marketing/delivery] |
| **Key Partnerships** | Who do you need? | [suppliers/affiliates/platforms] |
| **Cost Structure** | What are the costs? | [see Step 4] |

### Step 2: Revenue Model Selection

Choose and design the primary revenue model:

| Model | Description | Best For | Scalability |
|-------|-------------|----------|-------------|
| **One-time sale** | Single purchase | Physical products, courses | Low |
| **Subscription/SaaS** | Recurring payment | Software, content, services | Very High |
| **Freemium** | Free tier + paid upgrade | SaaS, apps, platforms | High |
| **Marketplace/Commission** | % of transactions | Platforms, directories | Very High |
| **Advertising** | Monetize attention | Media, content, apps | High (at scale) |
| **Licensing** | Charge for IP usage | Software, frameworks, content | High |
| **Service retainer** | Monthly recurring service | Agencies, consulting | Medium |
| **Usage-based** | Pay per use | API, cloud, utilities | High |
| **Affiliate** | Commission on referrals | Content creators, influencers | Medium |
| **Hybrid** | Combination of above | Mature businesses | Varies |

**Recommended for 0-to-revenue speed**: Start with service/one-time, transition to recurring.

### Step 3: Pricing Strategy

**Value-Based Pricing (Hormozi method):**
1. What is the dream outcome worth to the customer? = $X
2. Your price should be 10-20% of that value = $Y
3. Test 3 price points: Low ($Y x 0.7), Mid ($Y), High ($Y x 1.5)

**Pricing Tiers:**

| Tier | Name | Price | Includes | Target % |
|------|------|-------|----------|----------|
| **Basic** | [Name] | $X/mo | [Core features] | 60% |
| **Pro** | [Name] | $X/mo | [Core + advanced] | 30% |
| **Premium** | [Name] | $X/mo | [Everything + VIP] | 10% |

**Price Anchoring**: Always show the highest tier first. Use a "decoy" tier to push toward your target tier.

**Pricing Psychology:**
- Charm pricing ($97 vs $100) for consumer
- Round pricing ($500, $1000) for B2B / high-ticket
- Annual discount (2 months free) to reduce churn
- Founding member pricing for launch validation

### Step 4: Cost Structure

| Cost Category | Monthly | Annual | Type |
|---------------|---------|--------|------|
| **Fixed Costs** | | | |
| Hosting / Infrastructure | $X | $X | Fixed |
| Tools / Software | $X | $X | Fixed |
| Team / Freelancers | $X | $X | Fixed |
| Office / Workspace | $X | $X | Fixed |
| **Variable Costs** | | | |
| Customer acquisition (CAC) | $X | $X | Variable |
| Payment processing fees | $X | $X | Variable |
| Delivery / Fulfillment | $X | $X | Variable |
| Support | $X | $X | Semi-variable |
| **Total Monthly Burn** | **$X** | **$X** | |

### Step 5: Unit Economics

Calculate the fundamental health metrics:

| Metric | Formula | Your Number | Healthy Range |
|--------|---------|-------------|---------------|
| **CAC** (Customer Acquisition Cost) | Total marketing / new customers | $X | Varies |
| **LTV** (Lifetime Value) | ARPU x avg. lifespan (months) | $X | >3x CAC |
| **LTV:CAC Ratio** | LTV / CAC | X:1 | >3:1 |
| **Gross Margin** | (Revenue - COGS) / Revenue | X% | >60% (SaaS), >40% (services) |
| **Payback Period** | CAC / monthly ARPU | X months | <12 months |
| **Break-even** | Fixed costs / (price - variable cost per unit) | X units | |
| **Monthly Burn Rate** | Total monthly expenses | $X | |
| **Runway** | Cash / burn rate | X months | >6 months |

**Unit Economics Health Check:**
- LTV:CAC > 3:1 = Healthy
- LTV:CAC 1-3:1 = Survivable but tight
- LTV:CAC < 1:1 = Unsustainable (losing money per customer)

### Step 6: Value Chain Analysis

Map where you create and capture value:

```
[Input] → [Activity 1] → [Activity 2] → [Activity 3] → [Output/Customer]
  $cost      $cost           $cost          $cost          $revenue
```

For each activity:
- Build vs Buy vs Partner decision
- Core competency? (keep in-house)
- Commodity? (outsource/automate)
- Differentiator? (invest heavily)

### Step 7: Competitive Moat Assessment (Hamilton Helmer's 7 Powers)

| Power | Applicability | Score (1-5) | Strategy to Build |
|-------|--------------|-------------|-------------------|
| **Scale Economies** | Cost advantages from size | /5 | [action] |
| **Network Effects** | Product improves with more users | /5 | [action] |
| **Counter-Positioning** | Incumbents can't copy without hurting themselves | /5 | [action] |
| **Switching Costs** | Painful for customers to leave | /5 | [action] |
| **Branding** | Willingness to pay premium | /5 | [action] |
| **Cornered Resource** | Exclusive access to asset | /5 | [action] |
| **Process Power** | Superior operational ability | /5 | [action] |

**Moat Score: X/35**
- 25-35: Strong defensibility
- 15-24: Moderate, needs strengthening
- 0-14: Weak, vulnerable to competition

### Step 8: Scalability Assessment

| Dimension | Current | At 10x Scale | Bottleneck? |
|-----------|---------|--------------|-------------|
| **Revenue** | $X/mo | $X/mo | |
| **Team size** | X | X | Y/N |
| **Tech infrastructure** | [description] | [needed] | Y/N |
| **Delivery capacity** | X units/mo | X units/mo | Y/N |
| **Customer support** | [method] | [needed] | Y/N |
| **Cash requirements** | $X | $X | Y/N |

**Scalability Score:**
- Product scales with zero marginal cost (SaaS, digital) = 10/10
- Product scales with low marginal cost (templates, courses) = 7/10
- Product scales linearly with headcount (services) = 4/10
- Product doesn't scale (1-on-1 custom work) = 2/10

### Step 9: Revenue Projections (3 Scenarios)

| Month | Conservative | Base Case | Optimistic |
|-------|-------------|-----------|------------|
| 1 | $X | $X | $X |
| 3 | $X | $X | $X |
| 6 | $X | $X | $X |
| 12 | $X | $X | $X |
| 18 | $X | $X | $X |
| 24 | $X | $X | $X |

Assumptions for each scenario documented clearly.

## Output Template

```markdown
# A360 Business Model Design
## Business: [NAME]
## Date: YYYY-MM-DD

### Business Model Canvas
[9-block summary]

### Revenue Model: [TYPE]
[Description of how money is earned]

### Pricing
| Tier | Price | Includes |
|------|-------|----------|
| Basic | $X | [features] |
| Pro | $X | [features] |
| Premium | $X | [features] |

### Unit Economics
| Metric | Value | Health |
|--------|-------|--------|
| CAC | $X | [status] |
| LTV | $X | [status] |
| LTV:CAC | X:1 | [status] |
| Gross Margin | X% | [status] |
| Break-even | X units/mo | [status] |

### Competitive Moat: X/35
[Top 3 powers to develop]

### Scalability: X/10
[Key bottlenecks and solutions]

### 12-Month Revenue Projection
[Base case with key assumptions]

### Critical Risks
1. [Risk 1] — Mitigation: [action]
2. [Risk 2] — Mitigation: [action]
3. [Risk 3] — Mitigation: [action]
```

## Red Flags

Stop and warn the user if:
- LTV:CAC ratio is below 1:1 (business loses money on every customer)
- Break-even requires more than 18 months at current burn rate
- Gross margins below 30% with no path to improvement
- No identifiable moat and operating in a crowded market
- Revenue model depends entirely on advertising (high risk at small scale)
- Pricing is based on cost-plus instead of value (leaving money on the table)
- User is planning to be the cheapest option (race to the bottom)
- No clear path from current model to scalable model
- Cash requirements exceed available capital with no funding plan

## Handoff

After business model design:
- Route to `a360-oferta` to construct the irresistible offer
- Route to `a360-metricas` to set up the metrics dashboard
- Route to `a360-pitch` if seeking investment/partners
- Save output to Obsidian: `05 - Claude - IA/Outputs/YYYY-MM-DD - A360 - Business Model - [BusinessName].md`

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Business Model Canvas preenchido com dados reais (não placeholders)

- [ ] Todos os 9 blocos têm conteúdo específico do negócio do cliente (não "[from a360-avatar]")
- [ ] Customer Segments inclui dimensão de mercado estimada (ex: "PMEs tech em PT, ~4.200 empresas")
- [ ] Value Proposition articula 1 diferenciador concreto, não adjetivos genéricos
- [ ] Revenue Streams ligados ao modelo selecionado no Step 2

❌ NOT delivery-ready: "Customer Segments: [from a360-avatar] — quem são os clientes"
✅ Delivery-ready: "Customer Segments: Donos de cães em Lisboa, 25-45 anos, rendimento >€2.000/mês, ~38.000 potenciais em área metropolitana (INE 2023)"

---

### Gate 2 — Revenue Model selecionado e justificado

- [ ] Modelo principal escolhido com justificação explícita (não apenas listado)
- [ ] Velocidade até primeira receita estimada (ex: "primeiros €500 em 30 dias via serviço direto")
- [ ] Transição para recorrente mapeada se modelo inicial for one-time/service

❌ NOT delivery-ready: "Modelo: Subscription/SaaS — alta escalabilidade"
✅ Delivery-ready: "Cuidai usa Subscription: €29/mês (básico) + €79/mês (pro). Primeiros 90 dias: serviço direto a €150/onboarding para validar willingness-to-pay antes de automatizar."

---

### Gate 3 — Pricing com 3 tiers populados e lógica Hormozi aplicada

- [ ] Dream outcome do cliente quantificado em € (base do cálculo Hormozi)
- [ ] 3 price points calculados (Low / Mid / High) com percentagem-alvo de mix
- [ ] Pelo menos 1 elemento de pricing psychology aplicado (charm, anchor, founding member)
- [ ] Preços em moeda e periodicidade correctas para o mercado (€/mês, €/ano, €/unidade)

❌ NOT delivery-ready: "Tier Pro: $X/mo — Core + advanced features"
✅ Delivery-ready: "Cuidai Pro: €79/mês. Dream outcome = cão saudável + dono sem stress = valor percebido ~€600/ano. Preço = ~13% desse valor. Founding member: €59/mês para primeiros 50 utilizadores."

---

### Gate 4 — Cost Structure com números reais e burn total calculado

- [ ] Todas as categorias têm valores mensais preenchidos (mesmo que estimativa fundamentada)
- [ ] Custos fixos vs variáveis separados correctamente
- [ ] Total Monthly Burn somado e visível
- [ ] Fonte dos números indicada (ex: "Stripe fees: 1,4% + €0,25 por transação — tabela PT 2024")

❌ NOT delivery-ready: "Hosting: $X | Tools: $X | Total: $X"
✅ Delivery-ready: "Hosting (Railway): €25/mês | Stripe fees: ~€47/mês (@200 transações) | Suporte (freelancer 10h): €300/mês | **Total burn: €892/mês**"

---

### Gate 5 — Unit Economics calculados com LTV:CAC health verdict

- [ ] CAC calculado com canal específico (não hipotético genérico)
- [ ] LTV calculado com churn rate assumido explicitamente
- [ ] LTV:CAC ratio com verdict: Healthy / Survivable / Unsustainable
- [ ] Payback period em meses, com interpretação accionável
- [ ] Break-even em unidades/clientes com data estimada

❌ NOT delivery-ready: "LTV:CAC: X:1 — verificar se >3:1"
✅ Delivery-ready: "CAC (Instagram ads): €38 | LTV (churn 4%/mês → 25 meses médio x €29 ARPU): €725 | LTV:CAC = 19:1 ✅ HEALTHY | Payback: 1,3 meses | Break-even: 31 clientes pro (~mês 4)"

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero angle-brackets

- [ ] Nenhum `[placeholder]`, `$X`, `[Name]`, `[from a360-avatar]` visível no output final
- [ ] Nome do negócio do cliente aparece no título e em pelo menos 3 secções
- [ ] Todos os valores monetários em moeda correcta para o mercado do cliente
- [ ] Datas/timelines em formato concreto (ex: "Q2 2025", "mês 3", "até 30 Jun 2025")

❌ NOT delivery-ready: "Tier Premium: $X/mo | Inclui: [Everything + VIP] | Target: 10%"
✅ Delivery-ready: "ARRECADA.GOV Premium: €499/mês | Inclui: API ilimitada + SLA 99,9% + gestor dedicado | Target mix: 8% da base"

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Business Model Design — Cuidai
**Gerado por A360 | Fase 2 — Validação | Maio 2025**

---

## 1. Business Model Canvas

| Bloco | Conteúdo |
|-------|----------|
| **Customer Segments** | Donos de cães em Lisboa + Porto, 28-45 anos, rendimento >€2.000/mês. TAM estimado: 420.000 famílias com cão em PT (INE 2023). Foco inicial: 38.000 em área metropolitana de Lisboa. |
| **Value Propositions** | Cuidado veterinário preventivo por subscrição — sem surpresas de fim de mês. "Sabe sempre quanto vai gastar." |
| **Channels** | Instagram orgânico (principal), parcerias com clínicas veterinárias Lisboa (3 acordadas), boca-a-boca com referral program |
| **Customer Relationships** | App self-serve + check-in mensal automatizado + grupo WhatsApp para tier Premium |
| **Revenue Streams** | Subscrição mensal (79% da receita) + consultas avulsas pay-per-use (21%) |
| **Key Resources** | App mobile, rede de 12 veterinários parceiros em Lisboa, marca Cuidai |
| **Key Activities** | Gestão de rede veterinária, onboarding de novos clientes, CS proactivo |
| **Key Partnerships** | Clínicas VetPoint (Lisboa), Royal Canin (produto complementar), Stripe (pagamentos) |
| **Cost Structure** | Ver Secção 4 — burn mensal: €1.840 |

---

## 2. Revenue Model

**Modelo escolhido: Subscription + Usage-based (híbrido)**

Justificação: Recorrência maximiza LTV e reduz CAC amortizado.
Consultas avulsas criam upsell natural e testam elasticidade de preço.

**Velocidade até €1:** Serviço manual a €150/onboarding nos primeiros 60 dias
→ Transição para subscrição digital no mês 3.

---

## 3. Pricing Strategy

**Dream outcome do cliente:** Cão saudável, sem stress financeiro = €800/ano de valor percebido
**Faixa Hormozi (10-20%):** €80–160/ano → €7–13/mês base

| Tier | Nome | Preço | Inclui | Mix alvo |
|------|------|-------|--------|----------|
| Basic | Cuidai Essencial | €19/mês | 1 consulta/mês + vacinas em dia | 55% |
| Pro | Cuidai Plus | €49/mês | 2 consultas + urgências + app | 35% |
| Premium | Cuidai VIP | €99/mês | Ilimitado + nutricionista + concierge | 10% |

**Anchoring:** Mostrar VIP primeiro na página de pricing.
**Founding Member:** €39/mês para primeiros 100 subscritores (válido até 30 Jun 2025).
**Anual:** 2 meses grátis (€470/ano vs €588 mensal) — activa push em Outubro (renovações de ano).

---

## 4. Cost Structure

| Categoria | Mensal | Tipo |
|-----------|--------|------|
| Hosting (Railway + Supabase) | €45 | Fixo |
| Tools (Notion, Figma, Intercom) | €120 | Fixo |
| Stripe fees (~180 transações x €0,25 + 1,4%) | €82 | Variável |
| Freelancer CS (15h/mês x €18) | €270 | Semi-variável |
| Instagram Ads (validação) | €400 | Variável |
| Veterinários parceiros (comissão 12%) | ~€923 | Variável |
| **Total Monthly Burn** | **€1.840** | |

---

## 5. Unit Economics

| Métrica | Cálculo | Resultado | Saúde |
|---------|---------|-----------|-------|
| CAC (Instagram) | €400 ads / 14 novos clientes | **€28,6** | ✅ |
| ARPU | Mix ponderado tiers | **€43/mês** | |
| Churn assumido | 3,5%/mês (benchmark PT apps) | | |
| LTV | €43 x (1/0,035) = €43 x 28,6 meses | **€1.230** | |
| LTV:CAC | €1.230 / €28,6 | **43:1** ✅ HEALTHY | |
| Payback period | €28,6 / €43 | **0,7 meses** ✅ | |
| Break-even | €1.840 / (€43 - €12 COGS) | **59 clientes** | Mês 5 est. |
| Runway actual | €9.200 caixa / €1.840 burn | **5 meses** ⚠️ | |

**Acção imediata:** Runway <6 meses — priorizar 59 clientes pagantes até Setembro 2025.

---

## 6. Value Chain

```
Dono de cão → App Cuidai → Matching veterinário → Consulta realizada → Follow-up automático
   (lead)      €0 CAC app    €28,6 CAC ads          12% comissão         NPS + upsell
```

**Build:** App + matching algorithm (core IP — manter interno)
**Buy:** Infraestrutura cloud (Railway)
**Partner:** Rede veterinária (outsource delivery — foco em curadoria, não em clínicas próprias)
```

---

## Output anti-patterns

- Entregar tabela de pricing com `$X` ou `[Name]` sem substituir por valores reais do cliente
- Calcular LTV:CAC sem declarar o churn rate assumido — torna o número não auditável
- Copiar o Business Model Canvas com todos os blocos "[from a360-avatar]" sem integrar dados de skills anteriores (a360-avatar, a360-oferta)
- Usar "healthy" / "unhealthy" sem explicar o que o cliente deve fazer a seguir com essa informação
- Apresentar 3 tiers de pricing sem ancoragem visual ou lógica de mix (torna a tabela decorativa)
- Ignorar a moeda e mercado do cliente (output em USD para empresa portuguesa)
- Omitir o runway quando o burn rate é calculado — é a métrica mais accionável para founders early-stage
- Recomendar "transição para recorrente" sem dar timeline e trigger concreto (ex: "quando atingir 30 clientes activos")
- Listar "Key Partnerships" sem indicar se o acordo existe, está em negociação, ou é hipotético
- Entregar unit economics com break-even em "X units" sem converter para data estimada no calendário do cliente
