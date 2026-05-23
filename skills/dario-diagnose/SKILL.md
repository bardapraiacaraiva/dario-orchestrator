---
name: dario-diagnose
description: DARIO's universal diagnostic workflow — holistic analysis, priority triage (CRÍTICO/IMPORTANTE/OTIMIZAÇÃO), and 4-milestone roadmap. Entry point for any new client request or project audit. Triggers on "diagnose", "audit", "analisa", "avalia", "plano", "onde começar", "roadmap".
license: MIT
---

# DARIO Skill — Diagnose

The universal entry point. Any new substantive request from the user runs through this skill first to produce a structured diagnosis before any specialized work kicks in.

## When to activate

Invoke `/dario-diagnose` (or trigger automatically) when:
- User brings a new client/project and asks where to start
- User requests an audit of a site, product, or funnel
- User shares symptoms without a clear solution ("está a converter mal", "perdi posições", "quero escalar")
- User wants a roadmap for an ambitious transformation
- Start of any `dario-client-onboard` orchestrator flow

Do NOT use when:
- The request is a specific tactical task (use the specific skill or agent)
- The user already provided a clear spec to execute

## Workflow

### 1. Context gathering
Ask (or infer from input) the minimum viable context:
- **Who** is the client (industry, size, target market)
- **What** is the current state (URL, stack, metrics baseline if any)
- **Why now** (what triggered the request)
- **Constraints** (budget, timeline, team, legal)
- **Success criteria** (what would "done well" look like)

If critical context is missing, stop and ask — don't assume.

### 2. RAG consult (mandatory)
```
mcp__dario-rag__search_kb(query: "<sector> <stack> audit priorities", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "<main challenge keywords>", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "<client project name if mentioned>", limit: 5)
```
Search in all collections (omit collection) if client-specific context may exist in obsidian vault.

### 3. Holistic analysis — Phase 1 of DARIO model
Cover ALL dimensions, even if briefly:
- **Technical:** stack, performance, security, infrastructure, code health
- **SEO:** crawlability, indexation, content depth, schema, Core Web Vitals, E-E-A-T
- **Conversion (CRO):** funnel, CTAs, friction, trust signals, social proof
- **Content:** relevance, quality, AI-readiness, audience match
- **Business:** ROI, KPIs, market position, competition
- **Legal/Compliance:** RGPD, cookies, accessibility (EAA), sectorial
- **Brand:** positioning, consistency, narrative

### 4. Identify applicable specializations + squads
Explicitly name them (transparency protocol):
- "Ativando #2 (WordPress) + #3 (Advanced SEO) + PT Legal spec + Brand Squad"
- Cite RAG sources consulted

### 5. Prioritization — Phase 2
Classify every finding into exactly one bucket:
- **🔴 CRÍTICO** — Blocks launch / risks legal / high-impact revenue leak
- **🟡 IMPORTANTE** — Measurable impact, 1-4 weeks to fix
- **🟢 OTIMIZAÇÃO** — Long-term compounding gains

Use quick-wins-first ordering within each tier.

### 6. Roadmap — Phase 3 (4 milestones)
| Milestone | Weeks | Focus |
|---|---|---|
| **M1 — Foundation** | 1-2 | Setup, baseline metrics, TIER 0 blockers |
| **M2 — Core Fixes** | 3-4 | CRÍTICO bucket closed, core integrations |
| **M3 — Optimization** | 5-6 | IMPORTANTE bucket + performance |
| **M4 — Launch + Monitor** | 7-8 | Deploy, alerts, KPI dashboard |

Customize weeks to client scope but keep the 4-stage cadence.

### 7. Confidence declaration
State explicitly:
- 🟢 Alta confiança (80-100%): direct recommendation
- 🟡 Exploração (50-79%): present 2-3 alternatives
- 🔴 Incerteza (<50%): ask questions first

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: diagnostic
dario_specializations: [list]
dario_squads: [list]
confidence: <green|yellow|red>
---

# Diagnóstico DARIO — <Client Name>

## Resumo Executivo
- **Problema identificado:** <1-2 lines>
- **Solução proposta:** <1-2 lines>
- **Impacto esperado:** <metric + timeframe>

## Análise Holística
### Técnico
### SEO
### Conversão
### Conteúdo
### Legal / Compliance
### Brand

## Priorização
### 🔴 CRÍTICO (bloqueia launch / risco legal)
1. ...
### 🟡 IMPORTANTE
1. ...
### 🟢 OTIMIZAÇÃO
1. ...

## Roadmap
### M1 — Foundation (Sem 1-2)
### M2 — Core Fixes (Sem 3-4)
### M3 — Optimization (Sem 5-6)
### M4 — Launch + Monitor (Sem 7-8)

## Métricas de Sucesso
| KPI | Baseline | Target | Deadline |
|---|---|---|---|

## Próximos Passos
- [ ] <immediate action 1>
- [ ] <immediate action 2>

## Questões Pendentes
- <things you need from the user/client>
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Diagnóstico DARIO.md`

## Delivery-ready self-check (run BEFORE delivering to client)

A diagnostic output is **delivery-ready (90+/100)** only if ALL of these are true. If any is missing, mark as draft and complete before delivery.

### 1. Resumo Executivo — 3 elements, all concrete
- [ ] Problema identificado em 1-2 frases com NÚMERO ou MÉTRICA (não "está lento", sim "LCP 4.2s vs target 2.5s")
- [ ] Solução proposta em 1-2 frases com APPROACH (não "optimizar performance", sim "lazy-load images + minify CSS + CDN cache")
- [ ] Impacto esperado com MÉTRICA + DEADLINE (não "melhor SEO", sim "+15% organic traffic em 90 dias")

❌ NOT delivery-ready: "Site lento, precisa otimização, melhor performance"
✅ Delivery-ready: "LCP 4.2s (target 2.5s) → lazy-load + Brotli + CDN edge cache → LCP <2.0s em 6 semanas, +20% conversion"

### 2. Análise Holística — TODAS as 7 dimensões cobertas
- [ ] Técnico (stack, performance, security)
- [ ] SEO (crawl, index, CWV, E-E-A-T)
- [ ] Conversão (funnel, CTA, trust signals)
- [ ] Conteúdo (relevância, AI-readiness)
- [ ] Negócio (ROI, KPIs, market position)
- [ ] Legal/Compliance (RGPD, EAA, sectorial)
- [ ] Brand (positioning, consistency)

Cada dimensão tem AT LEAST 2 findings concretos. "Brand: ok" não conta — diz O QUE está ok e como sabes.

### 3. Priorização — cada finding tem effort + impact + tier
- [ ] Cada finding tem tier (CRÍTICO/IMPORTANTE/OTIMIZAÇÃO)
- [ ] Cada finding tem effort estimate (h ou dias)
- [ ] Cada finding tem impact estimate (% métrica ou €/€)

❌ NOT delivery-ready: "Implementar schema markup (IMPORTANTE)"
✅ Delivery-ready: "Schema Article + Organization markup (IMPORTANTE) — effort 4h, impact +8-12% organic CTR baseado em case Lisbon Dog Care"

### 4. Roadmap — 4 milestones cada um EXECUTÁVEL
- [ ] M1 Foundation com 3-5 deliverables concretos + check de done
- [ ] M2 Core Fixes mapeia 1-1 aos CRÍTICO findings
- [ ] M3 Optimization mapeia aos IMPORTANTE findings
- [ ] M4 Launch + Monitor inclui dashboard + alertas + KPI threshold

### 5. Métricas de Sucesso — tabela populada COMPLETA
- [ ] Mínimo 4 KPIs com baseline atual + target + deadline
- [ ] Pelo menos 1 KPI por dimensão CRÍTICA do diagnóstico
- [ ] Cada baseline tem fonte (Lighthouse, GA, Stripe, etc.)

### 6. Output uses CLIENT NAME + REAL data throughout
- [ ] Client name em cada secção título
- [ ] Sem placeholder angle-brackets <>
- [ ] URLs, números, stack technologies — todos reais do briefing
- [ ] Confidence level explícito (🟢/🟡/🔴) na Resumo Executivo

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no diagnóstico output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via RAG, sessão anterior, dados reais do cliente (URL crawlada, métrica fornecida, contrato visto)
- 🟡 **assumed** — plausível dado o sector/stack, mas precisa de confirmação do cliente antes de entregar
- 🟢 **projection** — forecast por design (crescimento estimado, impacto esperado, timeline projetado)

Output checklist upfront mostra ao cliente exactamente o que é trust-as-is vs. o que precisa de verificação. **Honest transparency > diagnóstico inflado.**

---

❌ NOT delivery-ready:
- "Taxa de conversão atual: 1,2%" — sem label, reader assume que foi medido
- "Stack: WordPress + WooCommerce" — sem label, pode ser inferência de uma menção casual
- "Impacto esperado: +35% tráfego orgânico em 90 dias" — parece garantia, não projeção

✅ Delivery-ready:
- 🔵 **verified** — "Core Web Vitals: LCP 4,8s" (extraído do PageSpeed report partilhado)
- 🟡 **assumed** — "Stack assumed: WordPress 6.x + Yoast SEO" (baseado no HTML visível; confirmar versões exactas + plugins activos)
- 🟢 **projection** — "Impacto estimado: +30-40% tráfego orgânico em 90 dias post-M2" (benchmark sectorial; resultado real depende de execução)

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir assumptions com actuals (stack real, métricas medidas, constraints validados)
- [ ] All 🔵 citations added — RAG source, URL crawlada, ou documento cliente referenciado
- [ ] All 🟢 projections labeled as forecasts ao cliente — expectations claras antes de assinar roadmap

## Fully-worked A-tier example (delivery-ready reference)

Esta é a estrutura de um diagnóstico 92+/100. Usar como anchor.

```markdown
---
project: Lisbon Dog Care by Marcela
date: 2026-05-23
type: diagnostic
dario_specializations: [#2 WordPress, #3 Advanced SEO, #4 CRO]
dario_squads: [Cybersecurity, Data]
confidence: green
---

# Diagnóstico DARIO — Lisbon Dog Care by Marcela

## Resumo Executivo
- **Problema identificado:** Site WordPress live em lisbondogcarebymarcela.com com LCP 3.8s (mobile, fonte Lighthouse), bounce rate 67%, zero schema markup, e CTA "Pedir orçamento" sem track conversion.
- **Solução proposta:** Performance pass (Brotli + image lazy-load + Cloudflare CDN) + LocalBusiness schema + GA4 events em CTA → reduz LCP <2.0s e mede ROI real do tráfego orgânico.
- **Impacto esperado:** +25-35% conversion landing→booking em 60 dias; +18% organic traffic em 120 dias.

## Análise Holística

### Técnico (3 findings)
- WordPress 6.4.x + theme Astra + 22 plugins activos (alguns desactualizados Yoast 19.x → 23.0)
- PHP 7.4 (EOL desde Nov 2022) — risco security + perf 30% inferior PHP 8.3
- Hosting Hostinger shared, sem CDN, sem object cache

### SEO (4 findings)
- Crawl OK, sitemap.xml válido, robots.txt clean
- ZERO structured data (LocalBusiness + Service + Review faltam)
- Hreflang ausente para PT/EN duplo-target (Lisbon expats)
- E-E-A-T: about page sem author bio + sem certifications dog handling

### Conversão (3 findings)
- CTA "Pedir orçamento" leva a contact form 7-campos (drop-off provável >40%)
- Zero trust signals (sem testimonials, sem certificações visíveis)
- WhatsApp button mobile-only mas ausente desktop (60% tráfego)

### Conteúdo (2 findings)
- 8 service pages mas ZERO blog posts de educação dog parents PT/expat
- AI-readiness baixo (sem FAQ schema, sem chunks <300 chars)

### Negócio (2 findings)
- Ticket €25/passeio sem upsell pack mensal explícito
- Sem segmentação PT vs expat (mensagem única para 2 mercados)

### Legal/Compliance (2 findings)
- Cookie banner não-conforme RGPD (sem opt-out granular)
- Sem política privacy linkada em forms (RGPD art 13)

### Brand (2 findings)
- Logo + tagline OK ("Cuidados profissionais com paixão")
- Voice inconsistente PT vs EN — EN sounds machine-translated

## Priorização

### 🔴 CRÍTICO (effort + impact por item)
1. **PHP 7.4 → 8.3 upgrade** — effort 4h (Hostinger one-click), impact security + 30% perf
2. **GDPR cookie banner conformidade** — effort 2h (CookieYes plugin), impact risco multa €20K+
3. **Privacy policy link em forms** — effort 30min, impact compliance

### 🟡 IMPORTANTE
1. **LocalBusiness + Service + Review schema** — effort 4h, impact +8-12% organic CTR
2. **Brotli + image lazy-load + Cloudflare CDN free tier** — effort 6h, impact LCP <2.0s
3. **CTA form: 7 campos → 3 campos + WhatsApp principal** — effort 3h, impact +30% conversion
4. **GA4 events em CTA + form submit** — effort 2h, impact medição ROI real
5. **About page: author bio Marcela + dog handling certifications** — effort 2h, impact E-E-A-T

### 🟢 OTIMIZAÇÃO
1. **Blog content 4 posts/mês (educação dog parents Lisbon)** — effort 8h/mês, impact long-tail SEO
2. **PT/EN voice rewrite (native EN copywriter)** — effort 1 dia, impact expat conversion
3. **Upsell pack mensal landing** — effort 6h, impact +15% LTV

## Roadmap

### M1 — Foundation (Sem 1-2)
- PHP 8.3 upgrade (CRÍTICO 1)
- Cookie banner GDPR (CRÍTICO 2)
- Privacy policy link (CRÍTICO 3)
- Baseline metrics capture (Lighthouse + GA4)
- ✅ Done check: PHP 8.3 + cookie banner conforme + privacy linkada

### M2 — Core Fixes (Sem 3-4)
- Schema markup completo (IMPORTANTE 1)
- Performance pass Brotli/CDN (IMPORTANTE 2)
- CTA form simplification (IMPORTANTE 3)
- GA4 events (IMPORTANTE 4)
- ✅ Done check: LCP <2.0s, schema valida no Rich Results Test, GA4 events tracking

### M3 — Optimization (Sem 5-6)
- E-E-A-T about page rewrite (IMPORTANTE 5)
- Blog setup + 2 primeiros posts (OTIMIZAÇÃO 1)
- PT/EN voice review (OTIMIZAÇÃO 2)
- ✅ Done check: about page autorial, 2 blog posts indexed

### M4 — Launch + Monitor (Sem 7-8)
- Upsell pack landing (OTIMIZAÇÃO 3)
- Dashboard Looker Studio (LCP, conversion, organic traffic)
- Alertas Slack se LCP >2.5s ou conversion drop >20%
- ✅ Done check: dashboard live + alertas configurados

## Métricas de Sucesso

| KPI | Baseline (fonte) | Target | Deadline |
|---|---|---|---|
| LCP mobile | 3.8s (Lighthouse 2026-05-23) | <2.0s | M2 fim (Sem 4) |
| Conversion landing→booking | 2.1% (estimativa) | 3.0%+ | M3 fim (Sem 6) |
| Organic traffic | 340/mês (GSC est.) | 600+/mês | M4 +30 dias |
| GDPR compliance | não conforme | 100% conforme | M1 fim (Sem 2) |
| Schema valid items | 0 | 4 types (LocalBusiness, Service, Review, FAQ) | M2 fim |

## Próximos Passos
- [ ] Confirmar acesso Hostinger admin + WordPress admin (Marcela)
- [ ] Backup completo pré-upgrade (M1 dia 1)
- [ ] Baseline Lighthouse + GA4 export (M1 dia 1, antes de qualquer mudança)

## Questões Pendentes
- Está confortável com Cloudflare free tier vs Hostinger CDN paid?
- Há orçamento para copywriter EN nativo (M3) ou prefere AI translation +review?
- Quer continuar com WhatsApp Business ou activar form-based bookings?

**Confidence:** 🟢 Alta (90%) — baseado em audits comparáveis de WordPress dog care PT (3 casos) + Lighthouse data direto.
```

## Red flags — don't do this (anti-patterns)
- Never skip RAG consult (even if you think you know)
- Never produce a roadmap without prioritization tiers
- Never hide confidence level
- Never recommend without checking PT Legal spec for PT clients
- Never forget to check EAA accessibility spec for any EU consumer site
- Generic finding without effort/impact estimate ("optimize SEO" sem números)
- KPI table com células vazias ou "TBD"
- Resumo Executivo sem números concretos no Problema/Solução/Impacto
- Output com placeholder angle-brackets <client> em vez de nome real
- Análise Holística com menos de 7 dimensões cobertas
