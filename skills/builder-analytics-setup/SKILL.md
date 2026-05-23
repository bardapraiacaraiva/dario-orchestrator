---
name: builder-analytics-setup
description: >
  Setup completo de analytics: GA4, GTM, eventos custom, conversoes, funnels, dashboards KPI.
  Gera codigo de tracking, data layer, event schemas. Mede tudo desde o dia 1.
  Use quando: analytics, GA4, google analytics, tracking, eventos, conversoes, metricas, KPIs.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Analytics Setup

## Proposito
Configurar analytics COMPLETO desde o dia 1 — nao "vamos medir depois".

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-analytics-setup [app]` | Setup GA4 + GTM completo |
| `/builder-analytics-setup events [app]` | Event schema apenas |
| `/builder-analytics-setup dashboard [app]` | KPI dashboard design |

## Workflow

### 1. Define KPIs
Por tipo de produto:
- **SaaS:** MRR, churn, activation rate, time-to-value, DAU/MAU
- **E-commerce:** revenue, AOV, cart abandonment, conversion rate
- **Lead gen:** leads, cost/lead, qualified rate, time-to-close
- **Content:** pageviews, time-on-page, bounce, scroll depth

### 2. GA4 Config
```javascript
// Google Analytics 4 setup (Next.js)
// app/layout.tsx
import Script from 'next/script'

const GA_ID = process.env.NEXT_PUBLIC_GA_ID

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <Script src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`} strategy="afterInteractive" />
        <Script id="google-analytics" strategy="afterInteractive">
          {`window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${GA_ID}');`}
        </Script>
      </head>
      <body>{children}</body>
    </html>
  )
}
```

### 3. Custom Events
```typescript
// lib/analytics.ts
export function trackEvent(name: string, params?: Record<string, any>) {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', name, params)
  }
}

// Events to track
trackEvent('sign_up', { method: 'email' })
trackEvent('cta_click', { location: 'hero', text: 'Start Free' })
trackEvent('pricing_view', { plan: 'pro' })
trackEvent('form_submit', { form: 'contact' })
trackEvent('scroll_depth', { percentage: 75 })
```

### 4. Conversion Funnel
```
Visit → View Pricing → Start Trial → Activate → Convert to Paid
  |         |              |            |           |
  100%      35%            12%          8%          4%
```

## Output
1. GA4 setup code (Next.js compatible)
2. Event tracking utility (`lib/analytics.ts`)
3. Event schema (all events documented)
4. Conversion funnel map
5. KPI dashboard wireframe

## Red Flags
- Sem analytics no launch — zero dados para decisoes
- Tracking sem consent banner (RGPD) — coima
- Eventos sem naming convention — dados inconsistentes
- Sem funnel definido — nao sabe onde perde users

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — KPIs definidos para o tipo de produto correcto
- [ ] Produto classificado (SaaS / e-commerce / lead gen / content) e KPIs correspondentes listados
- [ ] Mínimo 4 KPIs primários com definição concreta (não só o nome)
- [ ] KPIs têm baseline esperado ou benchmark do sector
- [ ] North Star Metric identificada e justificada

❌ NOT delivery-ready: `"KPIs: conversions, traffic, engagement"`
✅ Delivery-ready: `"North Star: Activation Rate (user completa 1ª reserva em 7 dias). KPIs: DAU/MAU target 0.4, Churn <3%/mês, Trial→Paid >12%"`

---

### Gate 2 — GA4 + GTM configurados com Measurement ID real
- [ ] `NEXT_PUBLIC_GA_ID` preenchido com ID real do projecto (G-XXXXXXXXXX), não placeholder
- [ ] Strategy `afterInteractive` confirmada para não bloquear LCP
- [ ] `gtag('config')` inclui parâmetros relevantes (`send_page_view`, `cookie_flags`, etc.)
- [ ] Environment variables documentadas no `.env.example` do projecto

❌ NOT delivery-ready: `GA_ID = 'G-XXXXXXXXXX'` ou `process.env.NEXT_PUBLIC_GA_ID` sem valor documentado
✅ Delivery-ready: `NEXT_PUBLIC_GA_ID=G-4K9MR27TQV  # Cuidai Production — criado 2024-11-03`

---

### Gate 3 — Event schema completo com naming convention
- [ ] Todos os eventos seguem `snake_case` consistente
- [ ] Cada evento tem: nome, parâmetros, trigger, valor de negócio
- [ ] Eventos de conversão marcados como `conversion: true` no GA4
- [ ] Sem eventos duplicados ou sobrepostos no mesmo trigger

❌ NOT delivery-ready: `trackEvent('CTAClick')`, `trackEvent('cta-click')`, `trackEvent('CtaClicked')` no mesmo projecto
✅ Delivery-ready:
```
sign_up        | method: 'email'|'google'  | após submit form  | conversão principal
trial_start    | plan: 'starter'|'pro'     | clique "Start Trial" | conversão secundária
feature_used   | feature_name: string      | 1ª acção na feature  | activation proxy
```

---

### Gate 4 — Funnel de conversão mapeado com percentagens reais ou estimadas
- [ ] Funnel tem mínimo 4 etapas com labels claros
- [ ] Percentagens de drop-off anotadas (mesmo que estimativas de benchmark)
- [ ] Etapa de maior drop identificada como "priority fix"
- [ ] Cada etapa tem evento GA4 correspondente mapeado

❌ NOT delivery-ready: Funnel genérico sem percentagens — `Visit → Signup → Convert`
✅ Delivery-ready:
```
Visit → View Pricing → Start Trial → Activate → Paid
100%      28%  (⬇72%)   9% (⬇67%)   6%(⬇33%)   3.5%
                ↑ PRIORITY: melhorar pricing page copy
```

---

### Gate 5 — Consent banner + RGPD compliance verificados
- [ ] Consent banner implementado ANTES de qualquer gtag/GA4 disparar
- [ ] Modo de consentimento GA4 (`gtag('consent', 'default', {...})`) configurado
- [ ] Política de privacidade referencia GA4 e cookies de analytics
- [ ] Opção de opt-out funcional e testada

❌ NOT delivery-ready: GA4 a disparar no page load sem verificar consentimento — coima RGPD até €20M
✅ Delivery-ready:
```javascript
gtag('consent', 'default', {
  analytics_storage: 'denied',  // default denied até user aceitar
  wait_for_update: 500
})
// só após consentimento:
gtag('consent', 'update', { analytics_storage: 'granted' })
```

---

### Gate 6 — Output usa CLIENT NAME + dados reais, sem angle-brackets
- [ ] Nenhum `<YOUR_APP>`, `<GA_ID>`, `<CLIENT>`, `<EVENT_NAME>` no output final
- [ ] Measurement ID real ou placeholder explicitamente marcado como "substituir antes do deploy"
- [ ] Nome do projecto/produto aparece nos comentários do código
- [ ] Dashboard KPI tem nome do cliente no título

❌ NOT delivery-ready: `// Setup para <APP_NAME>` ou `GA_ID = '<measurement_id>'`
✅ Delivery-ready: `// SAQUEI — Analytics Setup v1.0 — 2024-11-15` com `GA_ID = 'G-8XN3KP01MZ'`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Analytics Setup — Cuidai (SaaS B2C, cuidadores)
**Data:** 2024-11-15 | **Stack:** Next.js 14, App Router | **GA4 ID:** G-4K9MR27TQV

---

## KPIs — Cuidai
| KPI | Definição | Target Mês 1 | Benchmark Sector |
|-----|-----------|-------------|-----------------|
| Activation Rate | User cria 1º pedido em 7 dias | >25% | 20-30% |
| Trial→Paid | Free → plano pago | >10% | 8-15% SaaS B2C |
| DAU/MAU | Engagement ratio | >0.25 | 0.2 aceitável |
| Caregiver Match Rate | Pedido com match aceite | >70% | interno |

**North Star:** Successful Matches por semana (cuidador aceita + família confirma)

---

## GA4 Config — Next.js 14 App Router

```env
# .env.local — Cuidai
NEXT_PUBLIC_GA_ID=G-4K9MR27TQV
```

```typescript
// app/layout.tsx — Cuidai Analytics
import Script from 'next/script'

const GA_ID = process.env.NEXT_PUBLIC_GA_ID // G-4K9MR27TQV

export default function RootLayout({ children }) {
  return (
    <html lang="pt">
      <head>
        {/* Consent default — RGPD compliance */}
        <Script id="consent-init" strategy="beforeInteractive">
          {`window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('consent', 'default', {
              analytics_storage: 'denied',
              ad_storage: 'denied',
              wait_for_update: 500
            });`}
        </Script>
        <Script
          src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`}
          strategy="afterInteractive"
        />
        <Script id="ga4-init" strategy="afterInteractive">
          {`gtag('js', new Date());
            gtag('config', '${GA_ID}', {
              send_page_view: true,
              cookie_flags: 'SameSite=None;Secure'
            });`}
        </Script>
      </head>
      <body>{children}</body>
    </html>
  )
}
```

---

## Event Schema — Cuidai

```typescript
// lib/analytics.ts — Cuidai v1.0
export function trackEvent(name: string, params?: Record<string, unknown>) {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', name, params)
  }
}

// --- ACQUISITION ---
trackEvent('sign_up',           { method: 'email' | 'google', role: 'family' | 'caregiver' })
trackEvent('onboarding_start',  { role: 'family' | 'caregiver' })
trackEvent('onboarding_finish', { role: 'family', steps_completed: 4 })

// --- ACTIVATION (North Star proxies) ---
trackEvent('care_request_created', { care_type: 'idoso' | 'crianca' | 'pet', urgency: 'now' | 'planned' })
trackEvent('caregiver_profile_viewed', { profile_id: string, source: 'search' | 'recommendation' })
trackEvent('match_accepted',    { match_id: string, response_time_min: number })

// --- CONVERSION ---
trackEvent('trial_start',       { plan: 'familiar' | 'pro' })          // conversão GA4
trackEvent('subscription_paid', { plan: 'familiar', value: 12.99, currency: 'EUR' }) // receita

// --- ENGAGEMENT ---
trackEvent('message_sent',      { conversation_id: string })
trackEvent('review_submitted',  { rating: number, role: 'family' })
```

---

## Funnel de Conversão — Cuidai

```
Registo → Onboarding → 1º Pedido → Match Aceite → Subscrição Paga
  100%       68%           31%          22%              9%
             ↓32%          ↓37%         ↓9%              ↓13%
                     ↑ PRIORITY        ↑ secondary

Acção: A/B test onboarding step 3 (escolha de cuidador vs. cuidado)
Meta Q1: Onboarding→Pedido de 31% → 40%
```

---

## KPI Dashboard — Cuidai (GA4 Exploration)

**Report:** "Cuidai — Growth Weekly" (partilhar com pedro@cuidai.pt)
- Segmento A: Famílias | Segmento B: Cuidadores
- Métricas: New Users, Activation Rate, Match Rate, Trial Starts
- Dimensão: Source/Medium + Semana
- Alertas: Activation Rate < 20% → notificação Slack #analytics
```

---

## Output anti-patterns

- Entregar com `G-XXXXXXXXXX` ou qualquer `<placeholder>` — o cliente não consegue usar
- KPIs genéricos sem baseline ("vamos medir e ver") — não orienta decisões
- Events em camelCase e snake_case misturados no mesmo projecto — dados inconsistentes no GA4
- Funnel sem percentagens — não identifica onde agir primeiro
- GA4 a disparar antes do consentimento RGPD — violação legal, coima até €20M
- Tracking sem `role` ou `plan` nos eventos de conversão — impossível segmentar no futuro
- Dashboard sem owner/destinatário definido — nunca é consultado
- `send_page_view: true` sem SPA route change handling — pageviews duplicadas no Next.js
- Event schema entregue só como comentários no código, sem tabela legível para o cliente
- Setup sem `.env.example` documentado — próximo dev não sabe quais vars são necessárias
