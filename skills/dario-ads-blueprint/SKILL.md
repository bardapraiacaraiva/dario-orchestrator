---
name: dario-ads-blueprint
description: Paid traffic campaign blueprint for Facebook / Google / YouTube ads. Covers audiences, creative framework, funnel structure, tracking, budget allocation, and KPIs. Based on Pittman / Burns / Kasim / Breeze / Sobral frameworks. Triggers on "ads", "tráfego pago", "facebook ads", "google ads", "youtube ads", "campanha", "media buying".
license: MIT
---

# DARIO Skill — Paid Ads Blueprint

Designs a ready-to-execute paid traffic campaign. Does not write creative copy itself (pairs with `dario-sales-letter` + creatives brief) — it builds the **structure, targeting, and flow**.

## When to activate

- Client wants to start paid traffic (first campaign)
- Existing campaigns underperforming (audit + rebuild)
- Launch campaign for a new offer (pair with `dario-offer`)
- Planning quarterly ads budget

## Workflow

### 1. Gather inputs
- **Offer** — what's being sold, price, margin
- **Target avatar** — demographics, psychographics, interests
- **Dream outcome** — what the customer wants
- **Current baseline** (if any): CAC, ROAS, conversion rate
- **Budget** — monthly or per campaign
- **Platforms** — where the avatar lives (FB/IG, Google, YouTube, TikTok, LinkedIn)
- **Conversion event** — what's the north star metric
- **Tracking stack** — sGTM? Meta CAPI? Enhanced Conversions? GA4?

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "molly pittman facebook ads campaign structure", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "ralph burns facebook ads scale", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "kasim aslam google ads performance max", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "tom breeze youtube ads creative", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "pedro sobral BPM method facebook ads", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "consent mode v2 meta capi tracking", collection: "dario", limit: 5)
```

### 3. Platform selection matrix

| Goal | Best Platform | Why |
|---|---|---|
| Low-intent discovery | Meta (FB/IG) | interest + LAL audiences |
| High-intent capture | Google Search | keyword intent |
| Brand + education | YouTube | long-form trust |
| B2B SaaS | LinkedIn + Google | buyer intent |
| Visual product | TikTok + IG Reels | short video |
| Local service | Google LSA + Maps | geo intent |

**Rule:** start with ONE platform. Master it before expanding. Avoid multi-platform dilettantism.

### 4. Campaign structure

#### Meta (Facebook / Instagram)
```
Account
├── Campaign: COLD — Prospecting (CBO ou ABO?)
│   ├── AdSet: Broad targeting (Advantage+)
│   │   └── 3-5 Ad creatives (different angles)
│   ├── AdSet: Interest stack (1-3 stacks)
│   │   └── 3-5 Ad creatives
│   └── AdSet: LAL 1% from purchasers
│       └── 3-5 Ad creatives
├── Campaign: WARM — Engaged (retargeting)
│   └── AdSet: 7d engagers + website visitors
│       └── 2-3 Ad creatives
└── Campaign: HOT — Cart abandoners / Non-converters
    └── AdSet: 14d website add-to-cart, no purchase
        └── 2-3 Ad creatives + urgency
```

Budget split: 70% cold, 20% warm, 10% hot (starting). Adjust per Pittman BPM method.

#### Google Ads
```
Account
├── Campaign: Branded Search (must exist, low budget, high ROAS)
├── Campaign: High-intent Search (commercial keywords)
│   ├── AdGroup: service-A keywords
│   ├── AdGroup: service-B keywords
│   └── AdGroup: competitor branded (careful)
├── Campaign: Performance Max (aggregate)
└── Campaign: YouTube Ads (for awareness/retargeting)
```

### 5. Creative framework (Pittman / Depesh 3-2-1)

For each offer, produce:
- **3 creative angles** (emotional × problem × mechanism)
- **2 creative formats** per angle (static, video, carousel, UGC)
- **1 offer** consistent across all

Creative patterns that work:
- **Problem-Solution** (30s video or static)
- **Testimonial-driven** (UGC-style)
- **Before/After** (visual result)
- **"Watch this first"** pattern (stop-scroll)
- **Founder-to-camera** (authenticity)
- **Proof stacking** (numbers, logos, results)

### 6. Funnel structure
```
Ad → Landing Page → Lead Magnet / Booking / Purchase → Email nurture → Retarget
```

Every step needs conversion tracking:
- Ad click → pageview
- Scroll depth (90%)
- Form start → form submit
- Purchase / lead event
- Post-conversion upsell / cross-sell

### 7. Tracking stack (must be compliant)
- **sGTM** ou client-side GTM
- **Consent Mode v2** — mandatório EU
- **Meta CAPI** (Conversions API) — bypass browser blockers
- **Google Enhanced Conversions**
- **GA4** como source of truth
- **Event deduplication** client/server

### 8. Budget allocation rule

Starting budget per campaign:
- **Cold / prospecting:** 5x to 10x the target CPA (to exit learning phase in 7 days)
- **Warm / retargeting:** 10-20% of cold
- **Hot:** 5-10% of cold

**Don't split budget across 15 adsets day 1** — Meta learning phase needs ~50 conversions/week/adset.

### 9. KPI targets

| KPI | Meta | Google Search | YouTube |
|---|---|---|---|
| CTR | 1-2% | 5-8% | 0.5-1.5% (view rate 20%+) |
| CPC | €0.30-€1.50 | €0.80-€3 (sector-dep) | €0.05-€0.20 per view |
| CVR (LP) | 2-5% | 3-6% | 1-3% |
| ROAS | 2-4x cold / 5-10x warm | 3-8x | 1.5-3x (brand+direct) |
| CPA | ≤40% margin | ≤30% margin | — |

Customize for sector. HNW B2B tolerates higher CPA; e-commerce under 30%.

### 10. Testing & iteration
- **Creative refresh:** every 7-14 days
- **Winning creative:** scale +20-50% per day max
- **Losing creative:** kill after 100-200 clicks no conv
- **Copy test:** headline, hook, CTA
- **Audience test:** cold, LAL, interest, broad
- **Placement test:** Reels only, feed only, all placements

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: ads-blueprint
platforms: [meta, google, youtube]
budget_monthly: €X
---

# Paid Ads Blueprint — <Client>

## Strategic Context
- Offer: ...
- Avatar: ...
- Dream outcome: ...
- Baseline CAC / ROAS: ...
- Budget: €X / mês
- North star event: ...

## Platform Choice + Rationale
Primary: <...>
Secondary: <...>
Why: ...

## Campaign Architecture
<diagram or tree>

## Creative Framework (3-2-1)
| Angle | Format | Lead copy | Visual |
|---|---|---|---|

## Landing Page Requirements
- ...

## Tracking Stack
- GTM / sGTM: ...
- Consent Mode v2: ...
- Meta CAPI: ...
- Enhanced Conversions: ...
- Events: ...

## Budget Allocation
| Campaign | Daily | Monthly | % |
|---|---|---|---|

## KPI Targets (30/60/90d)
| Metric | D30 | D60 | D90 |
|---|---|---|---|
| CPA | | | |
| ROAS | | | |
| CTR | | | |
| CVR | | | |

## Weekly Optimization Checklist
- [ ] Creative refresh cadence
- [ ] Audience review
- [ ] Killbox (lost creatives)
- [ ] Scale winners

## Risks & Mitigations
- ...

## Roadmap 90d
- Semana 1-2: ...
- Semana 3-4: ...
- Mês 2-3: ...
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Ads Blueprint.md`

## Red flags / anti-patterns
- No conversion tracking in place (fix this FIRST)
- Running ads to homepage instead of dedicated LP (Oli Gardner violation)
- 15 adsets on day 1 (budget fragmentation)
- No creative refresh cadence (fatigue)
- Scaling winners too aggressively (>50%/day)
- Using Meta without CAPI in 2026 EU traffic (loses 40% of events)
- Zero brand search campaign (competitors steal clicks)
- Performance Max without exclusion lists (cannibalizes brand search)
- Tracking conversions without consent (illegal PT)

## Interactions
- Depends on `dario-offer` (offer clarity)
- Pair with `dario-sales-letter` for LP copy
- Check `spec/server-side-analytics-consent-mode-v2` before launching
- Check `spec/pt-legal-compliance` for banner setup

## Red Flags
- Never launch ads before the landing page is live, tested, and tracking-verified — sending paid traffic to a broken or untracked page burns budget with zero data
- Never skip installing tracking pixels (Meta CAPI, GA4 events, Enhanced Conversions) before the first ad goes live — without conversion data the algorithm cannot optimize and you fly blind
- Always test new creative with a small budget (5-10% of total) for 48-72h before scaling — untested creative at full budget risks blowing the entire monthly spend on a losing angle
- Never ignore negative keywords on Google Search campaigns — broad match without negatives attracts irrelevant clicks that inflate CPC and destroy ROAS
- Always confirm Consent Mode v2 is active before launching any EU campaign — non-compliant tracking is illegal under GDPR and can result in fines plus ad account suspension
- Never scale a winning ad by more than 50% daily — aggressive scaling resets the learning phase and destabilizes CPAs

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Strategic context completo e específico
- [ ] Offer com preço real e margem estimada (não "serviço X")
- [ ] Avatar com demographics + psychographics concretos (não "adultos interessados em saúde")
- [ ] Dream outcome escrito como o cliente diria, não como descrição de produto
- [ ] Baseline CAC/ROAS preenchido ou marcado explicitamente "sem dados históricos"
- [ ] Plataforma(s) escolhida(s) com justificação da matriz de seleção

❌ NOT delivery-ready: `Offer: serviço de contabilidade. Avatar: PMEs. Budget: €X/mês.`
✅ Delivery-ready: `Offer: Pacote contabilidade para freelancers — €89/mês, margem estimada 60%. Avatar: freelancers tech 28-42 anos, preocupados com IRS e coimas. Budget: €1.200/mês Meta. Sem baseline histórico.`

---

### Gate 2 — Estrutura de campanha com nomes reais e budget alocado
- [ ] Naming convention das campaigns/adsets definida (não genérica)
- [ ] Budget split 70/20/10 (ou variante justificada) com valores em €
- [ ] Número de creatives por adset especificado (3-5 cold, 2-3 warm/hot)
- [ ] CBO vs ABO justificado para o budget disponível
- [ ] Learning phase calculada: budget diário ≥ (CPA target × 7) / 7 dias

❌ NOT delivery-ready: `Campaign: Cold prospecting. Budget: maioritariamente aqui. Creatives: vários por adset.`
✅ Delivery-ready: `Campaign: [LUSOconta]_COLD_Prospecting_Meta_CBO — €840/mês (€28/dia). 3 adsets × 4 creatives. CBO ativo porque budget <€50/dia por adset. Learning phase: alvo CPA €30 → precisa €210/semana total ✓`

---

### Gate 3 — Creative framework 3-2-1 preenchido para este cliente
- [ ] 3 ângulos criativos específicos ao produto/avatar (não "problema, solução, mecanismo" genérico)
- [ ] 2 formatos por ângulo indicados com razão (UGC porque avatar é 25-35 / Founder porque brand trust)
- [ ] Hook de cada ângulo escrito (primeira frase/visual — não apenas descrito)
- [ ] Indicação de assets necessários (vídeo 9:16, foto before/after, screenshot testemunho)

❌ NOT delivery-ready: `Ângulo 1: problema. Ângulo 2: solução. Formato: vídeo e estático.`
✅ Delivery-ready: `Ângulo 1 — Dor IRS: Hook: "Pagaste IRS a mais em 2023 sem saber?" → Formato: Reels 30s founder-to-camera + carrossel estático. Assets: vídeo selfie Diogo (fundador) + 3 slides com números reais poupança.`

---

### Gate 4 — Tracking stack validado e compliance EU confirmado
- [ ] Consent Mode v2 explicitamente confirmado (obrigatório EU/PT)
- [ ] Meta CAPI ou Google Enhanced Conversions indicados como ativos ou como tarefa pendente
- [ ] Eventos de conversão nomeados exactamente como estão configurados (não "compra" se o evento se chama `Purchase`)
- [ ] Deduplicação client/server mencionada se CAPI activo
- [ ] GA4 como source of truth confirmado ou alternativa justificada

❌ NOT delivery-ready: `Tracking: Google Tag Manager + Meta Pixel. Compliance: verificar RGPD.`
✅ Delivery-ready: `Tracking: sGTM activo (container SAQUEI). Consent Mode v2: implementado via CookieYes. CAPI: activo, event_id passado para deduplicação. Evento norte: Purchase (Receita ≥ €1) — verificado no Events Manager. GA4 como SoT: conversão importada para Google Ads.`

---

### Gate 5 — KPIs customizados ao sector e threshold de decisão definidos
- [ ] KPIs benchmark ajustados ao sector (não usar tabela genérica para B2B SaaS e e-commerce igual)
- [ ] CPA máximo calculado como % da margem real do cliente (não ≤40% abstracto)
- [ ] Threshold "kill creative" com número de cliques/impressões específico ao budget
- [ ] ROAS break-even calculado (não "2-4x genérico")
- [ ] Cadência de revisão definida: quem revê, quando, que acção toma

❌ NOT delivery-ready: `CPA alvo: €30. ROAS: 3x. Matar criativos que não convertem. Rever semanalmente.`
✅ Delivery-ready: `CPA máximo: €35,60 (40% margem €89). ROAS break-even: 1,63x. Kill creative: sem conversão após 150 cliques (≈€105 gasto a CPC €0,70). Revisão: Diogo (media buyer) às 2ªs feiras 09h — decisão escalar/matar — relatório DARIO semana anterior.`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets por preencher
- [ ] Todos os `<client>`, `<YYYY-MM-DD>`, `€X`, `<platform>` substituídos
- [ ] Naming conventions das campaigns incluem sigla/nome do cliente real
- [ ] Datas de início de campanha e fim de teste inicial preenchidas
- [ ] Nenhum placeholder visível no output final (grep por `<` e `>`)
- [ ] Documento auto-suficiente: quem recebe consegue executar sem perguntar nada ao DARIO

❌ NOT delivery-ready: `project: <client> | budget_monthly: €X | date: <YYYY-MM-DD>`
✅ Delivery-ready: `project: LUSOconta | budget_monthly: €1.200 | date: 2025-06-10 | platforms: [meta] | fase_teste: 2025-06-10 → 2025-07-07`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
---
project: LUSOconta
date: 2025-06-10
type: ads-blueprint
platforms: [meta]
budget_monthly: €1.200
fase_teste: 2025-06-10 → 2025-07-07
---

# Paid Ads Blueprint — LUSOconta

## Strategic Context
- **Offer:** Contabilidade digital para freelancers — €89/mês (plano Starter), margem estimada 62%
- **Avatar:** Freelancer tech (dev, designer, consultor) 27-42 anos, PT, rendimento €2k-€6k/mês.
  Dor principal: medo de IRS errado e coimas. Quer simplicidade, não quer lidar com TOC presencialmente.
- **Dream outcome:** "Receber o meu recibo verde, pagar o mínimo legal de IRS e nunca ter surpresas."
- **Baseline:** Sem dados históricos (primeira campanha paga)
- **Budget:** €1.200/mês Meta Ads (apenas Meta — avatar confirmado ativo no Instagram)
- **Conversion event:** Lead qualificada (preencheu form "Quero saber mais" na landing page)
- **CPA máximo:** €35,60 (40% × margem €89)
- **ROAS break-even:** n/a (serviço recorrente — LTV 14 meses → CAC payback ≤ mês 1)

---

## Platform Decision
**Meta (FB + IG) — único canal fase 1**
Justificação: avatar freelancer 27-42 anos passa 45+ min/dia no Instagram; produto de descoberta
(não procura "contabilidade digital" no Google activamente). Google Search activar em fase 2
se CAC Meta > €50.

---

## Campaign Structure — Meta

### Fase 1 (semanas 1-4): aprendizagem

```
LUSOconta_Meta
├── [LC]_COLD_Prospecting_CBO — €840/mês (€28/dia)
│   ├── AdSet A: Broad PT 25-44 (Advantage+ Audience, sem interesses)
│   │   ├── Creative 1: Reels 30s — Ângulo Dor IRS (founder Diogo, selfie)
│   │   ├── Creative 2: Carrossel — "3 erros que os freelancers cometem no IRS"
│   │   └── Creative 3: Estático — Before/After recibo verde confuso vs dashboard LUSOconta
│   ├── AdSet B: Interest stack — [Freelancing PT + NHR Portugal + Recibos Verdes]
│   │   ├── Creative 1: (igual AdSet A C1)
│   │   ├── Creative 2: UGC-style testemunho Mariana Santos, dev Lisboa
│   │   └── Creative 3: (igual AdSet A C3)
│   └── AdSet C: LAL 1% email list LUSOconta (482 contactos)
│       ├── Creative 1: Proof stacking — "1.200 freelancers. Zero coimas."
│       └── Creative 2: Founder-to-camera — "Porque criei a LUSOconta"
│
├── [LC]_WARM_Engaged_ABO — €240/mês (€8/dia)
│   └── AdSet: Visitantes landing page 7d + engagers IG 14d (excluir leads)
│       ├── Creative 1: Testemunho vídeo 60s — Carlos M., designer Porto
│       └── Creative 2: Estático urgência — "Experimenta 30 dias grátis — oferta até 30 Jun"
│
└── [LC]_HOT_Retarget_ABO — €120/mês (€4/dia)
    └── AdSet: Form initiators (iniciaram form, não submeteram) 14d
        └── Creative 1: Estático — "Ficaste com dúvidas? Fala connosco" + WhatsApp CTA
```

**Budget split:** 70% / 20% / 10% — rever semana 3 se CPL < €20 em COLD.
**CBO justificado:** budget €28/dia total → Meta distribui melhor que ABO abaixo de €15/adset.
**Learning phase:** alvo 50 leads/semana/adset → precisa €28/dia × 7 = €196/semana ✓ (margem ajustada)

---

## Creative Framework 3-2-1

**Oferta constante:** 30 dias grátis + onboarding dedicado (valor €0 entrada).

| Ângulo | Hook | Formato A | Formato B |
|---|---|---|---|
| 1 — Dor IRS | "Sabes quanto IRS vais pagar este ano?" | Reels 30s Diogo founder | Carrossel 4 slides dados IRS PT |
| 2 — Mecanismo | "O teu recibo verde, automatizado." | Demo screencast 45s | Estático dashboard screenshot |
| 3 — Prova social | "Mariana poupou €340 no IRS em 2024." | UGC vídeo testemunho | Estático quote + foto |

**Assets necessários (briefing para equipa LUSOconta):**
- Vídeo selfie Diogo, 30s, vertical 9:16, sem edição excessiva
- Screenshot dashboard (dados reais anonimizados)
- Vídeo testemunho Mariana Santos (cliente existente, já confirmou)
- 3 fotos "recibo verde papel caótico" vs app LUSOconta

---

## Funnel & Tracking

```
Ad (Meta) → Landing Page lusoconta.pt/freelancers
  → Form "Quero experimentar" (4 campos: nome, email, NIF, €/mês faturação)
  → Thank You Page (event: Lead) → Email sequence 5 dias (Mailchimp)
  → Retarget se não ativou conta ao dia 7
```

**Tracking stack:**
- GTM client-side (container GTM-XXXX — implementar antes de 10 Jun)
- Consent Mode v2: CookieYes já activo no site ✓
- Meta Pixel ID: 1234567890 + CAPI via GTM server (event_id deduplicação activo)
- Evento principal: `Lead` com parâmetros `content_name: freelancers_form`
- GA4 property: G-XXXXXXX — conversão `generate_lead` importada para Meta
- **Compliance:** RGPD PT — dados form não saem da EU (Mailchimp EU endpoint)

---

## KPIs & Decisões — Fase 1

| KPI | Benchmark sector | Target LUSOconta |
|---|---|---|
| CTR (link) | 1-2% | ≥1,2% |
| CPC | €0,40-€1,20 | ≤€0,90 |
| CVR landing page | 2-5% | ≥3% (form simples) |
| CPL (custo por lead) | — | ≤€25 |
| Lead → Activação | — | ≥30% (nurture email) |
| CAC real | — | ≤€35,60 |

**Kill creative:** sem lead após 120 cliques (≈€108 a CPC €0,90) → pausar, não apagar.
**Escalar creative winner:** +30% budget cada 48h se CPL < €20.
**Refresh criativo:** semanas 3 e 6 (mesmo se a ganhar — evitar ad fatigue com audiência PT pequena).

---

## Calendário Fase 1

| Semana | Acção | Responsável |
|---|---|---|
| 10-16 Jun | Setup tracking, upload creatives, lançar | DARIO + equipa LUSOconta |
| 17-23 Jun | Revisão learning phase, kill underperformers | Diogo (2ª feira 09h) |
| 24-30 Jun | Escalar winners, lançar HOT retarget | Diogo + DARIO review |
| 1-7 Jul | Relatório fase 1: CPL real, leads activadas, CAC | DARIO entrega relatório |

---

## Próximos passos (dependências)
1. ⬜ LUSOconta confirma assets criativos até 7 Jun
2. ⬜ CAPI server-side configurado (estimar 4h dev)
3. ⬜ Landing page /freelancers live com form tracking testado
4. ⬜ Ativar campanha 10 Jun 08h00 PT
5. ⬜ Fase 2 (Google Search) — avaliar semana 5 se CAC Meta > €50
```

---

## Output anti-patterns

- **Placeholders vivos no output final** — entregar com `<client>`, `€X`, `<YYYY-MM-DD>` é o anti-pattern mais comum e mais grave; o cliente vê incompetência imediata
- **Estrutura de campanha sem valores em €** — "70% cold" sem dizer "€840/mês (€28/dia)" não permite execução nem aprendizagem
- **KPIs benchmark copiados da tabela genérica sem ajuste ao sector** — CPL €25 faz sentido para SaaS €89/mês, não para e-commerce €12 ou imobiliário €500k
- **Creative framework descrito, não especificado** — listar "ângulo emocional, racional, mecanismo" sem escrever o hook e nomear os assets necessários não é um brief executável
- **Tracking marcado como "a implementar" sem responsável e data** — campanhas lançadas sem CAPI ou Consent Mode v2 em EU são desperdício de budget e risco legal
- **CBO vs ABO não justificado** — escolher um sem explicar o porquê do budget e da fase não educa o cliente nem documenta a decisão
- **Learning phase ignorada** — estrutura com 8 adsets × €5/dia num budget de €40/dia garante que nenhum adset sai da fase de aprendizagem
- **"Rever semanalmente" sem dono, sem hora, sem critério** — revisão sem threshold de decisão é revisão que não acontece
- **Plataformas múltiplas "para cobrir todas as frentes" com budget < €2k/mês** — multi-platform dilettantism diluí signal, prolonga aprendizagem, atrasa resultados
- **Blueprint sem indicar o par de skills necessário** — ads blueprint sem mencionar que precisa de landing page (dario-sales-letter) e oferta (dario-offer) validadas entrega estrutura sem combustível
