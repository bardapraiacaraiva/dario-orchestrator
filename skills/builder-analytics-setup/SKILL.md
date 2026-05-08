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
