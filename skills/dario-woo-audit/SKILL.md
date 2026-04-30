---
name: dario-woo-audit
description: WooCommerce-specific deep audit — checkout flow, payment gateways (MBWay/Multibanco), tax config, product schema, cart UX, shipping, refunds, GDPR delete. Complements dario-wp-audit with Woo-only dimensions. Triggers on "woocommerce audit", "checkout audit", "loja online audit", "ecommerce audit".
license: MIT
---

# DARIO Skill — WooCommerce Audit

Deep dive into WooCommerce-specific issues beyond what `dario-wp-audit` covers. Use when the client's main product is an online store.

## When to activate
- Client has a WooCommerce store
- Checkout abandonment is high
- Payment integration issues (PT gateways)
- Tax / IVA configuration review
- Product catalog SEO review

## Workflow

### 1. RAG consult
```
mcp__dario-rag__search_kb(query: "woocommerce checkout payment audit", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "ecommerce cro friction cart abandonment", collection: "dario", limit: 5)
```

### 2. Audit categories (6)

#### 1. Checkout flow
- Steps count (ideal: 1-2 pages max)
- Guest checkout enabled
- Field count (minimize: name, email, address, payment)
- Progress indicator visible
- Mobile UX (thumb-friendly buttons, autocomplete)
- Error handling (inline, specific)
- "Encomendar com obrigação de pagar" button (DL 24/2014 mandatory)

#### 2. Payment gateways (PT market)
- **MBWay** — integration working, error handling, timeout
- **Multibanco** — reference generation, ifthenpay/eupago/easypay integration
- **Credit card** — Stripe/PayPal/HiPay, 3D Secure 2.0
- **PayPal** — express checkout, guest checkout
- **Apple Pay / Google Pay** — if applicable
- **SEPA DD** — for recurring/subscription
- Gateway redundancy (if primary fails, fallback exists?)

#### 3. Tax / IVA config
- IVA 23% standard rate correct
- Reduced rates (6%, 13%) for applicable products
- Tax class mapping per product
- Tax display (inc. or exc. IVA) — B2C must show inc.
- Invoice generation (integration with billing software: InvoiceXpress, PHC, Sage)
- EU VAT compliance (OSS for cross-border B2C)

#### 4. Product catalog & schema
- Product schema (Schema.org Product, Offer, AggregateRating)
- Image quality + alt text
- Price display (from/to, sale price, currency)
- Stock status (in stock / out of stock / backorder)
- Product categories + attributes structured
- Related/upsell products configured
- Reviews enabled + moderated

#### 5. Shipping & delivery
- Shipping zones correct (PT continental, Açores, Madeira, EU, international)
- Free shipping threshold (conversion lever)
- Shipping costs visible BEFORE checkout (DL 24/2014)
- Delivery time estimates shown
- Tracking integration (CTT, DPD, GLS)
- Click & Collect option (if applicable)

#### 6. Post-purchase & compliance
- Order confirmation email (design, info, next steps)
- Shipping notification email
- Return/refund policy page (14 days DL 24/2014)
- GDPR "right to delete account + order data" mechanism
- Livro de Reclamações link in footer
- Invoice download from My Account

### 3. Score per category

| Category | Weight | Score Guide |
|----------|--------|------------|
| Checkout flow | 25% | 10: 1-step, guest, mobile-perfect. 5: 2-step, some friction. 0: multi-step, no guest |
| Payment gateways | 20% | 10: MBWay+MB+Card+PayPal, redundancy. 5: 2 methods only. 0: card only or broken |
| Tax / IVA | 15% | 10: correct rates, invoicing integrated. 5: basic correct. 0: wrong rates or no invoicing |
| Product catalog | 15% | 10: full schema, images, reviews, structured. 5: basic products. 0: missing schema, no images |
| Shipping | 15% | 10: zones correct, visible costs, tracking. 5: basic flat rate. 0: costs hidden or wrong zones |
| Post-purchase | 10% | 10: emails, returns, GDPR, livro reclamacoes. 5: basic emails. 0: no return policy, no GDPR |

**Overall score** = weighted average (0-100)

### 4. TIER Classification

| Tier | Score | Meaning | Action |
|------|-------|---------|--------|
| TIER 0 | 0-30 | Store broken — losing sales daily | Emergency fixes within 48h |
| TIER 1 | 31-55 | Functional but leaking revenue | Fix critical in 1 week, rest in 2 weeks |
| TIER 2 | 56-75 | Working but not optimized | Optimization sprint over 4 weeks |
| TIER 3 | 76-100 | Well-optimized | Maintenance mode, quarterly review |

## Output Template

```markdown
# Auditoria WooCommerce — <Client>

## Score Global: XX/100 (TIER X)

### 1. Checkout Flow — X/10
- [findings...]
- **CRITICO:** [if any]
- **FIX:** [specific action]

### 2. Payment Gateways — X/10
...

### 3. Tax / IVA — X/10
...

### 4. Product Catalog — X/10
...

### 5. Shipping — X/10
...

### 6. Post-Purchase — X/10
...

## Prioridades
### CRITICO (fazer agora)
1. ...

### IMPORTANTE (1-2 semanas)
1. ...

### OTIMIZACAO (quando possivel)
1. ...

## Roadmap 4 Semanas
| Semana | Acoes | Responsavel |
|--------|-------|------------|
| 1 | TIER 0 fixes | ... |
| 2 | Payments + Tax | ... |
| 3 | Catalog + Shipping | ... |
| 4 | Post-purchase + QA | ... |
```

## Integration

- Runs AFTER `dario-wp-audit` (general WP health first, then Woo deep-dive)
- Product schema pairs with `seo-schema` for validation
- Checkout UX findings feed into CRO recommendations
- Tax config findings feed into `lucas-finance` for compliance

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Auditoria WooCommerce.md`

## Red Flags

- Never skip MBWay/Multibanco check for PT stores — it's 60%+ of online payments
- Never approve a store without "encomendar com obrigação de pagar" button (DL 24/2014)
- Never ignore Livro de Reclamações link — it's legally required
- Always check IVA rates per product category — errors here mean AT fines
- Always verify GDPR account deletion works — test with a real account
