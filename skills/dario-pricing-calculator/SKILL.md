---
name: dario-pricing-calculator
description: Service pricing calculator for agencies — calculates real cost/hour, utilization-adjusted rates, project pricing with margins, retainer values. Uses Agency Business Model spec. Triggers on "pricing", "quanto cobrar", "rate hora", "preço do serviço", "margem", "utilization".
license: MIT
---

# DARIO Skill — Pricing Calculator

## Workflow
1. RAG: `search_kb("agency pricing utilization rate margin", collection: "dario")`
2. Gather: monthly costs, target income, hours available, utilization target
3. Calculate: real cost/hour, minimum rate, recommended rate, project pricing
4. Present 3 pricing tiers (Good/Better/Best)
5. Compare: hourly vs project vs retainer vs value-based

## Formulas
- Cost/hour = (Total monthly costs) / (Hours available × Utilization%)
- Min rate = Cost/hour × 1.3 (30% margin)
- Recommended rate = Cost/hour × 1.5-2.0
- Project price = (Estimated hours × Internal rate) × 1.5-2.0 markup

## Input Gathering

Collect the following inputs before running any calculation. Use defaults if the client does not provide a value:

| Input | Description | Default |
|---|---|---|
| **Monthly fixed costs** | Rent, software, subscriptions, insurance, accountant, tools, utilities | 3.000€ |
| **Owner target salary** | What the owner needs/wants to take home monthly (gross, before IRS) | 4.000€ |
| **Employee costs** | Total salaries + SS (23.75%) for all staff, or 0 if solo | 0€ |
| **Hours available/month** | Working hours per month (22 days x 8h = 176h, or adjusted) | 160h |
| **Utilization target** | % of hours that are billable (not admin, sales, learning) | 65% |
| **Profit margin target** | Desired net profit margin after all costs | 30% |
| **Annual one-off costs** | Training, conferences, equipment, divided by 12 | 500€/month |

## Calculation Engine

### Step-by-step with worked example (using defaults)

**Step 1: Total monthly cost**
```
Fixed costs:          3.000€
Owner salary:         4.000€
Employee costs:           0€
Annual one-offs/12:     500€
─────────────────────────────
Total monthly cost:   7.500€
```

**Step 2: Cost per available hour**
```
7.500€ / 160h = 46,88€/hour
```
This is your raw cost — if you charge this, you break even with 100% utilization (impossible).

**Step 3: Cost per billable hour (utilization-adjusted)**
```
160h × 65% utilization = 104 billable hours/month
7.500€ / 104h = 72,12€/hour
```
This is the real cost of each billable hour — the minimum to break even.

**Step 4: Minimum rate (with margin)**
```
72,12€ / (1 - 0.30) = 103,03€/hour
```
At this rate, with 65% utilization, you cover all costs + 30% profit margin.

**Step 5: Recommended rate**
```
Minimum rate × 1.3 = 133,94€ ≈ 135€/hour
```
Adds a buffer for scope creep, slow months, and investment in growth.

**Step 6: Premium rate**
```
Minimum rate × 1.8 = 185,45€ ≈ 185€/hour
```
For specialist work, urgent timelines, or high-value strategic projects.

### Summary table
| Metric | Value |
|---|---|
| Total monthly cost | 7.500€ |
| Billable hours/month | 104h |
| Break-even rate | 72€/h |
| Minimum rate (30% margin) | 103€/h |
| Recommended rate | 135€/h |
| Premium rate | 185€/h |
| Monthly revenue target (recommended) | 14.040€ |
| Annual revenue target | 168.480€ |

## Project Pricing Guide

Use this table to sanity-check project quotes. Ranges assume the recommended rate (~100-135€/h for a mid-level PT agency):

| Deliverable | Hour Range | Price Range (€) | Notes |
|---|---|---|---|
| Logo + brand identity basic | 8–20h | 800–2.500€ | Logo, colour palette, typography, basic guidelines |
| Full branding package | 25–50h | 3.000–7.000€ | Logo + identity manual + stationery + social templates |
| Website 5 pages (WordPress) | 40–80h | 3.000–8.000€ | Home, about, services, contact, blog setup |
| Website 10+ pages (custom) | 80–160h | 8.000–18.000€ | Custom design, CMS, integrations, SEO |
| E-commerce (WooCommerce) | 100–200h | 10.000–25.000€ | Product setup, payments (MB/MBWay), shipping |
| Landing page (single) | 10–25h | 1.000–3.000€ | Design + copy + form + analytics |
| SEO monthly retainer | 15–30h/month | 1.500–4.000€/month | Audit, on-page, content, link building, reporting |
| Content marketing monthly | 20–40h/month | 2.000–5.000€/month | Blog posts, social content, email newsletter |
| Social media management | 15–30h/month | 1.200–3.500€/month | Content creation, scheduling, community, reporting |
| Google Ads management | 10–20h/month | 800–2.500€/month + ad spend | Setup, optimization, reporting, excludes ad budget |

> **Rule of thumb:** If a project quote feels too low, it probably is. Always calculate hours honestly, then apply markup. Never price from the client's budget downward.

## Pricing Model Comparison

| Model | How it works | Pros | Cons | When to use |
|---|---|---|---|---|
| **Hourly** | Bill per hour worked, tracked and reported | Transparent, fair for undefined scope, easy to start | Penalises efficiency, client anxiety about hours, income ceiling | Discovery phases, consulting, maintenance, undefined scope |
| **Project-based** | Fixed price for defined deliverables | Predictable for client, rewards efficiency, cleaner scope | Risk if scope grows, requires accurate estimation | Websites, branding, campaigns with clear deliverables |
| **Retainer** | Fixed monthly fee for allocated hours/services | Recurring revenue, deeper client relationship, predictable cash flow | Scope creep risk, client may under-use, harder to raise price | Ongoing SEO, social media, content, support |
| **Value-based** | Price based on business outcome, not hours | Highest margins, aligns with client goals, no hour-tracking | Requires deep understanding of client's business, harder to justify without track record | Strategic projects, revenue-generating assets, clients with clear ROI metrics |

### Hybrid approach (recommended for PT agencies)
- **New clients:** Start project-based to build trust and deliver a clear win
- **Ongoing work:** Move to retainer after the first project succeeds
- **Strategic clients:** Layer value-based pricing for high-impact projects (e.g., e-commerce redesign that will increase conversion by 2x)

## PT Market Context

Typical agency rates in Portugal (2024-2026 reference):

| Level | Hourly Rate | Monthly Retainer (typical) | Profile |
|---|---|---|---|
| **Junior** | 25–40€/h | 800–1.500€/month | 0-2 years experience, execution-focused, needs supervision |
| **Mid-level** | 40–70€/h | 1.500–3.500€/month | 2-5 years, autonomous, manages small projects |
| **Senior** | 70–120€/h | 3.500–7.000€/month | 5-10 years, strategic input, client-facing, leads teams |
| **Specialist** | 100–200€/h | 5.000–12.000€/month | Deep expertise (SEO, performance, security, UX), consulting |
| **Agency blended rate** | 60–100€/h | — | Average across team for project quoting |

### Key PT market notes
- **Lisbon/Porto premium:** Rates 15-25% higher than rest of country
- **International clients:** Can charge 1.5-2x PT rates when working with EU/US clients remotely
- **IVA:** Always quote without IVA (23%) for B2B, with IVA for B2C. Clarify in every proposal.
- **Freelancer vs agency:** Solo freelancers typically charge 60-70% of agency rates but cannot scale
- **Race to the bottom risk:** Many PT agencies undercharge at 30-50€/h blended — this is unsustainable. The calculator above proves why.
- **SS contributions:** Freelancers pay 21.4% SS on 70% of income; factor this into solo pricing. Empresarios em nome individual pay differently from Unipessoal Lda.

## Save Location

Save generated pricing calculations to Obsidian:
- **Path:** `05 - Claude - IA/Outputs/YYYY-MM-DD - Pricing - [ClientOrContext] - Calculator.md`
- Include frontmatter: `type: pricing`, `client:`, `rate_recommended:`, `monthly_target:`, `status: draft`

## Red Flags

Stop and flag to the user if any of these are detected:
- Calculated minimum rate is below 50€/h (agency is structurally unprofitable)
- Utilization target set above 80% (unrealistic — leaves no time for sales, admin, learning)
- Profit margin target below 15% (no buffer for slow months or unexpected costs)
- Client expects project pricing but cannot define scope (use hourly or discovery phase first)
- Quoted price is more than 30% below the Project Pricing Guide range (undercharging risk)
- Owner salary set to 0€ (unsustainable — the business must pay the owner)
- No budget for annual training/tools (agency skills will decay, losing competitiveness)

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

---

### Gate 1 — Inputs recolhidos e explicitados

- [ ] Todos os 7 inputs do Input Gathering estão declarados (ou confirmado que se usam defaults)
- [ ] Se usados defaults, estão sinalizados explicitamente ("A usar valor padrão de 3.000€ para fixed costs")
- [ ] Nenhum campo está vazio ou com `TBD`/`a confirmar` no output final
- [ ] Utilization target está entre 50–85% (fora deste range → alertar o cliente)

❌ NOT delivery-ready: "Custos mensais: a confirmar. Salário alvo: [inserir aqui]."
✅ Delivery-ready: "Fixed costs: 4.200€ (confirmado); owner salary: 5.000€; utilization target: 70% (default aplicado, ajustar se diferente)."

---

### Gate 2 — Cálculos corretos e rastreáveis

- [ ] Step 1–6 executados em ordem, com valores intermédios visíveis
- [ ] Billable hours = Hours available × Utilization% (e.g. 160h × 65% = 104h)
- [ ] Break-even rate = Total monthly cost / Billable hours
- [ ] Minimum rate usa fórmula `break-even / (1 - margin%)`, NÃO `break-even × (1 + margin%)`
- [ ] Revenue target mensal = Recommended rate × Billable hours

❌ NOT delivery-ready: "A taxa mínima é cerca de 100€/h." (sem derivação)
✅ Delivery-ready: "6.800€ / (160h × 0,70) = 60,71€ break-even → 60,71 / (1 – 0,30) = **86,73€/h mínimo**"

---

### Gate 3 — Três tiers de pricing apresentados e distinguíveis

- [ ] Good / Better / Best (ou Mínimo / Recomendado / Premium) estão todos calculados
- [ ] Cada tier tem: rate por hora, justificação/uso ideal, revenue mensal projetado
- [ ] Premium rate ≥ 1,5× minimum rate
- [ ] Os tiers são conectados ao posicionamento do cliente (não genéricos)

❌ NOT delivery-ready: "Podes cobrar entre 80€ e 150€/h dependendo do projeto."
✅ Delivery-ready: "**Mínimo:** 87€/h (break-even + 30% margem) · **Recomendado:** 113€/h (buffer para meses lentos) · **Premium:** 156€/h (projetos urgentes ou estratégicos) — Revenue alvo a 70% util.: 9.128€/mês"

---

### Gate 4 — Comparação de modelos de pricing incluída

- [ ] Pelo menos 3 modelos comparados (hourly / project / retainer + value-based se aplicável)
- [ ] Recomendação explícita de modelo para o contexto específico do cliente
- [ ] Se retainer: calculado valor mínimo do retainer (horas alocadas × internal rate × markup)
- [ ] Se project-based: sanity-check do Project Pricing Guide aplicado ao deliverable concreto

❌ NOT delivery-ready: "Podes usar modelo de projeto ou retainer, ambos têm vantagens."
✅ Delivery-ready: "Para a Cuidai, retainer de social media (20h/mês × 113€ × 1,4 markup) = **3.164€/mês**. Mínimo aceitável: 2.500€/mês. Recomendação: retainer para previsibilidade, com cláusula de scope-cap a 25h."

---

### Gate 5 — Sanity-checks e alertas de risco incluídos

- [ ] Alertar se utilization target > 80% (burnout risk, não sustentável solo)
- [ ] Alertar se recommended rate está 30%+ abaixo dos benchmarks do Project Pricing Guide
- [ ] Indicar quantos projetos/mês o cliente precisa de fechar para atingir revenue target
- [ ] Revenue target anual calculado e referenciado (×12)

❌ NOT delivery-ready: "Com 90% de utilização, a taxa fica mais baixa e o negócio escala melhor."
✅ Delivery-ready: "⚠️ Utilization a 85% num modelo solo é insustentável — reserva 0h para vendas, formação e imprevistos. Recalculado a 70%: **taxa mínima sobe para 96€/h**. Para atingir 14.800€/mês precisas de ~2 projetos web médios ou 4 retainers de social media."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero placeholders

- [ ] Nome do cliente aparece no cabeçalho e na recomendação final
- [ ] Nenhum `<inserir>`, `[cliente]`, `[valor]`, `TBD` no output entregue
- [ ] Todos os euros são formatados consistentemente (1.200€, não "1200 euros" ou "€1,200")
- [ ] Summary table preenchida com os valores reais calculados, não com os defaults do SKILL.md

❌ NOT delivery-ready: "Calculadora de pricing para [Nome da Agência] — taxa recomendada: [X]€/h"
✅ Delivery-ready: "Calculadora de pricing — **Atrium Studio** (Março 2025) — Taxa recomendada: **118€/h**"

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / dados reais fornecidos pelo cliente
- 🟡 **assumed** — plausível mas precisa de confirmação do cliente antes de entrega
- 🟢 **projection** — previsão por design (não verificável — depende de execução futura)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs o que precisa de verificação. **Honest transparency > inflated delivery.**

---

❌ NOT delivery-ready:
> "O teu break-even rate é 72€/h, o recommended rate é 135€/h e o teu revenue target anual é 168.480€."
→ Reader assume que todos os inputs (custos fixos, salário-alvo, utilization) são reais — mas podem ser defaults.

✅ Delivery-ready:
> - 🔵 **verified** — Custos fixos mensais: 3.200€ (factura partilhada pelo cliente na sessão anterior)
> - 🟡 **assumed** — Utilization target: 65% (default aplicado — confirmar se reflecte o ritmo real de trabalho)
> - 🟡 **assumed** — Salário-alvo do owner: 4.000€ brutos (nunca confirmado explicitamente — validar antes de calcular minimum rate)
> - 🟢 **projection** — Revenue target anual: 168.480€ (projecção baseada em 104h facturáveis/mês × 135€/h × 12 — assume utilization sustentada)

---

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados — substituir defaults (custos fixos, salário, employee costs, horas disponíveis, utilization) com valores reais do cliente
- [ ] Todos os 🔵 sources citados — identificar de onde vieram os dados verificados (sessão X, documento Y)
- [ ] Todos os itens 🟢 comunicados explicitamente ao cliente como projecções condicionais (ex: "este revenue target assume que mantens 65% de utilization todos os meses")

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Calculadora de Pricing — Atrium Studio
**Data:** Março 2025 | **Modelo:** Solo founder + 1 designer part-time

---

## Inputs confirmados

| Input | Valor |
|---|---|
| Fixed costs mensais | 4.200€ (renda 800€, software 400€, contabilidade 150€, seguros 200€, ferramentas 650€, outros 400€, + 1.600€ salário designer PT) |
| Salário alvo fundador | 5.000€ |
| Custos com colaboradores | 1.600€ (designer 20h/semana, custo total c/ SS) |
| Horas disponíveis/mês | 160h (fundador) |
| Utilization target | 70% |
| Margem de lucro alvo | 30% |
| One-offs anuais / 12 | 400€/mês (conferências + equipamento) |

---

## Step-by-step — Atrium Studio

**Step 1: Total monthly cost**
```
Fixed costs:          4.200€
Salário fundador:     5.000€
Colaborador (design): 1.600€
One-offs/12:            400€
──────────────────────────────
Total mensal:        11.200€
```

**Step 2: Cost per available hour**
```
11.200€ / 160h = 70,00€/hora (custo bruto)
```

**Step 3: Cost per billable hour (utilization-adjusted)**
```
160h × 70% = 112 horas faturáveis/mês
11.200€ / 112h = 100,00€/hora (break-even real)
```

**Step 4: Minimum rate (30% margem)**
```
100€ / (1 – 0,30) = 142,86€/hora
```

**Step 5: Recommended rate**
```
142,86€ × 1,25 = 178,57€ ≈ 180€/hora
```

**Step 6: Premium rate**
```
142,86€ × 1,7 = 242,86€ ≈ 245€/hora
```

---

## Summary — Atrium Studio

| Métrica | Valor |
|---|---|
| Total mensal de custos | 11.200€ |
| Horas faturáveis/mês | 112h |
| Break-even rate | 100€/h |
| Taxa mínima (30% margem) | 143€/h |
| Taxa recomendada | 180€/h |
| Taxa premium | 245€/h |
| Revenue mensal alvo (recomendado) | 20.160€ |
| Revenue anual alvo | 241.920€ |

---

## Tiers de pricing — Atrium Studio

| Tier | Rate | Quando usar | Revenue mensal projetado |
|---|---|---|---|
| **Mínimo (Good)** | 143€/h | Clientes recorrentes, projetos longos, fidelização | 16.016€ |
| **Recomendado (Better)** | 180€/h | Projetos de branding, websites, novos clientes | 20.160€ |
| **Premium (Best)** | 245€/h | Projetos urgentes, estratégia, clientes enterprise | 27.440€ |

---

## Sanity-check de projetos típicos — Atrium Studio

| Projeto | Horas estimadas | Preço mínimo | Preço recomendado |
|---|---|---|---|
| Branding completo | 35h | 5.005€ | 6.300€ |
| Website 8 páginas (WordPress) | 60h | 8.580€ | 10.800€ |
| Landing page | 15h | 2.145€ | 2.700€ |
| Social media retainer/mês | 25h | 3.575€ | 4.500€ |

> **Alvo de fecho mensal:** Para 20.160€ de revenue a 180€/h, o Atrium precisa de
> ~1 website médio (10.800€) + 1 branding (6.300€) + 1 retainer ativo (4.500€) = 21.600€ ✅

---

## Recomendação de modelo — Atrium Studio

**Fase atual (0–3 clientes recorrentes):** Híbrido project-based + 1–2 retainers.
- Novo cliente → projeto de branding ou website a preço fixo (recomendado: 6.300–10.800€)
- Pós-entrega → propor retainer de social ou SEO (3.500–4.500€/mês)
- Evitar modelo só hourly: o designer part-time dilui a eficiência e o cliente questiona horas

⚠️ **Alerta:** Utilization a 70% é saudável para solo+part-time. Não aceitar projetos que impliquem >85% — os 30% restantes são vendas, gestão, imprevistos e desenvolvimento do Atrium Studio.
```

---

## Output anti-patterns

- Apresentar apenas a taxa recomendada sem mostrar o cálculo step-by-step — o cliente não consegue ajustar se os inputs mudarem
- Usar `break-even × 1,30` em vez de `break-even / (1 – 0,30)` — subestima a taxa mínima em ~4–6%
- Omitir o número de projetos/mês necessários para atingir o revenue target — o pricing fica desligado da realidade comercial
- Aplicar o mesmo markup a todos os deliverables — branding estratégico e manutenção WordPress têm perfis de risco e valor radicalmente diferentes
- Deixar utilization target a 65% sem questionar o modelo (solo vs. equipa) — um founder com equipa pode sustentar 70–75%; solo raramente passa 60% de forma sustentável
- Formatar o output como texto corrido sem summary table — impossível de rever, partilhar ou usar como referência em reunião com cliente
- Calcular revenue target sem desagregar entre horas do founder e horas de colaboradores — mascara a rentabilidade real do negócio
- Não sinalizar quando o preço recomendado está abaixo dos mínimos do Project Pricing Guide — o cliente acredita que o output valida underselling
