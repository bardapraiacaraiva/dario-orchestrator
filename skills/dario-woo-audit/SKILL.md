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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Checkout Flow auditado com dados reais
- [ ] Número de steps do checkout contados e registados (não estimados)
- [ ] Guest checkout testado (pass/fail explícito, não "aparentemente activo")
- [ ] Botão "Encomendar com obrigação de pagar" confirmado presente/ausente com screenshot ou URL específica
- [ ] Mobile UX avaliada (thumb-friendly, autocomplete, breakpoint testado)
- ❌ NOT delivery-ready: "O checkout parece ter alguns passos e guest checkout deve estar activo"
- ✅ Delivery-ready: "Checkout 3 steps (Cart → Billing → Payment), guest checkout DESACTIVADO, botão DL 24/2014 AUSENTE na página /checkout — CRÍTICO"

### Gate 2 — Payment Gateways PT verificados individualmente
- [ ] MBWay testado (integração activa, timeout handling, mensagem de erro verificada)
- [ ] Multibanco verificado (geração de referência funcional, provider identificado: ifthenpay/eupago/easypay)
- [ ] Gateway de fallback identificado ou ausência documentada
- [ ] 3D Secure 2.0 confirmado no gateway de cartão
- ❌ NOT delivery-ready: "A loja tem MBWay e Multibanco disponíveis"
- ✅ Delivery-ready: "MBWay via Easypay — activo mas sem mensagem de erro quando número inválido. Multibanco via ifthenpay — referências geradas correctamente. FALLBACK: nenhum — se Easypay falhar, loja fica sem pagamento alternativo imediato"

### Gate 3 — Tax / IVA com mapeamento por produto
- [ ] Taxa IVA padrão verificada (23%) e pelo menos 1 produto de taxa reduzida auditado
- [ ] Display price confirmado como IVA incluído (B2C legal requirement)
- [ ] Software de facturação identificado e integração testada (InvoiceXpress / PHC / Sage / outro)
- [ ] OSS flag levantada se loja vende para outros países EU
- ❌ NOT delivery-ready: "IVA parece estar configurado correctamente"
- ✅ Delivery-ready: "IVA 23% correcto nos produtos standard. Produto 'Suplementos alimentares' (ID #441) com taxa 23% — deveria ser 6% (AT Tabela I-1). Facturação: InvoiceXpress integrado mas não emite automaticamente após encomenda — requer trigger manual"

### Gate 4 — Product Catalog & Schema validados
- [ ] Schema.org Product markup verificado (mínimo: name, price, availability, currency)
- [ ] AggregateRating presente se reviews activas
- [ ] Alt text de imagens auditado (sample de 5+ produtos)
- [ ] Upsell/related products configurados em pelo menos 1 categoria principal
- ❌ NOT delivery-ready: "Os produtos têm schema markup e boas imagens"
- ✅ Delivery-ready: "Schema Product presente mas sem 'offers.priceCurrency' — Google Search Console a reportar erro. Alt text ausente em 34/67 imagens de produto. Reviews activas mas AggregateRating não renderiza no schema — plugin Yoast desactualizado (v21.1, current v21.8)"

### Gate 5 — Shipping zones e compliance DL 24/2014 verificados
- [ ] Zonas de envio mapeadas (PT Continental, Açores, Madeira separadas — tarifas CTT diferentes)
- [ ] Custo de envio visível ANTES do checkout (DL 24/2014) confirmado com URL específica
- [ ] Free shipping threshold identificado (valor actual + benchmark recomendado)
- [ ] Carrier de tracking identificado e link de tracking no email de envio verificado
- ❌ NOT delivery-ready: "As zonas de envio estão configuradas e o envio grátis existe"
- ✅ Delivery-ready: "Açores e Madeira na mesma zona que PT Continental — custo subavaliado em ~€4-8/encomenda. Envio grátis a €50 (benchmark sector: €40-45). Custos de envio OCULTOS até step 2 do checkout — violação DL 24/2014. Tracking CTT integrado mas link ausente no email de envio"

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholders
- [ ] `<Client>` substituído pelo nome real do cliente em todos os títulos e referências
- [ ] Score Global preenchido (ex: "Score Global: 54/100 (TIER 1)") — não "XX/100 (TIER X)"
- [ ] Todos os scores por categoria preenchidos com número real
- [ ] Roadmap 4 Semanas tem nomes de responsável reais (não "...")
- [ ] Ficheiro nomeado com data real e cliente real (ex: `2025-01-15 - Cuidai - Auditoria WooCommerce.md`)
- ❌ NOT delivery-ready: "Score Global: XX/100 (TIER X)" ou "### 2. Payment Gateways — X/10"
- ✅ Delivery-ready: "Score Global: 54/100 (TIER 1)" com todos os 6 scores preenchidos e cliente identificado

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Auditoria WooCommerce — Cuidai

## Score Global: 58/100 (TIER 2)

> Auditoria realizada: 2025-01-15 | Plataforma: WooCommerce 8.4.0 | Tema: Flatsome 3.18

---

### 1. Checkout Flow — 6/10

**Configuração actual:**
- 2 steps (Billing/Shipping → Review & Payment) ✅
- Guest checkout: ACTIVO ✅
- Campos no billing: 11 campos (Nome, Apelido, Empresa, País, Morada, Cidade, Código Postal,
  Telefone, Email, NIF, Notas) — empresa e NIF removíveis para B2C puro
- Progress indicator: AUSENTE ❌
- Mobile: botão CTA com 36px height — abaixo do mínimo recomendado 44px ❌
- Autocomplete HTML: atributos `autocomplete` ausentes nos campos morada ❌
- Erro inline: mensagens genéricas ("Campo obrigatório") sem especificidade ❌

**CRÍTICO:** Botão "Encomendar com obrigação de pagar" PRESENTE ✅ (DL 24/2014 — OK)

**FIX:**
- Remover campos Empresa + NIF do fluxo B2C padrão (mover para opcional/colapsável)
- Adicionar progress indicator (plugin: Woo Checkout Progress Bar ou custom CSS)
- Corrigir button height para mínimo 44px no CSS do tema
- Adicionar `autocomplete="address-line1"` etc. nos campos de morada

---

### 2. Payment Gateways — 5/10

**Gateways activos:**
| Gateway | Provider | Estado | Observação |
|---------|----------|--------|------------|
| MBWay | Easypay | ✅ Activo | Timeout 4min — OK. Erro "número inválido" sem mensagem clara ⚠️ |
| Multibanco | ifthenpay | ✅ Activo | Referências geradas OK. Prazo pagamento: 3 dias ✅ |
| Cartão | Stripe | ✅ Activo | 3DS2 activo ✅ |
| PayPal | — | ❌ Ausente | — |
| Apple/Google Pay | — | ❌ Ausente | — |

**CRÍTICO:** Zero redundância — ifthenpay e Easypay no mesmo tier. Se serviços falharem
simultaneamente (raro mas ocorre em manutenções), loja fica só com Stripe.

**FIX:**
- Adicionar PayPal Express como fallback (instalação 2h, cobre ~15% preferência PT)
- Melhorar mensagem de erro MBWay: "Número de telemóvel inválido. Use o formato 9XXXXXXXX"
- Considerar Google Pay via Stripe (já instalado) — activar toggle no dashboard Stripe

---

### 3. Tax / IVA — 6/10

**Configuração:**
- Taxa padrão: 23% ✅
- Display: preços com IVA incluído no storefront ✅ (B2C legal — OK)
- Taxas reduzidas configuradas:

| Produto | Taxa Actual | Taxa Correcta | Diferença |
|---------|------------|---------------|-----------|
| Serviços de apoio domiciliário | 23% | 6% | ⚠️ ERRO |
| Material de higiene adulto | 23% | 6% | ⚠️ ERRO |
| Suplementos vitamínicos | 23% | 23% | ✅ |

**CRÍTICO:** 2 categorias de produto com IVA incorrecto — risco de liquidação adicional AT.
Estimar impacto: ~€X/mês dependendo do volume (calcular com lucas-finance).

**Facturação:** InvoiceXpress integrado ✅ mas emissão manual — fatura não emite
automaticamente após pagamento confirmado. Backlog de 47 faturas por emitir (janeiro).

**FIX:**
- Corrigir tax class dos produtos de apoio domiciliário e higiene para "Reduced Rate" (6%)
- Configurar InvoiceXpress webhook on `woocommerce_payment_complete` para emissão automática
- Validar OSS: Cuidai tem 3 encomendas EU fora PT em 2024 — abaixo do threshold €10k
  (não obrigatório OSS ainda, mas monitorizar)

---

### 4. Product Catalog — 7/10

**Schema markup (via Google Rich Results Test):**
- Schema Product: ✅ Presente em todos os produtos
- `offers.price` + `offers.priceCurrency`: ✅
- `offers.availability`: ✅
- `aggregateRating`: ⚠️ Presente em 12/38 produtos com reviews — ausente nos restantes

**Imagens:**
- Total produtos: 38 | Com imagem principal: 38 ✅
- Alt text preenchido: 31/38 (82%) — 7 produtos sem alt text ❌
- Imagens comprimidas: ✅ (Smush activo)

**Catálogo:**
- Upsell configurados: 14/38 produtos ✅
- Related by category: activo ✅
- Reviews: activas e moderadas ✅ (aprovação manual)

**FIX:**
- Preencher alt text nos 7 produtos em falta (IDs: #112, #118, #203, #241, #267, #289, #301)
- Investigar por que AggregateRating não renderiza nos 26 produtos com reviews
  (possível conflict Yoast SEO v21.1 + WooCommerce — actualizar Yoast para v21.8)

---

### 5. Shipping — 5/10

**Zonas configuradas:**
| Zona | Carrier | Custo | Problema |
|------|---------|-------|---------|
| Portugal Continental | CTT | €3.90 | ✅ |
| Ilhas (Açores + Madeira) | CTT | €3.90 | ❌ Deveria ser €7.50-€12 |
| Europa | Correio Normal | €8.00 | ✅ aproximado |

**CRÍTICO:** Açores e Madeira agrupadas com Continental — Cuidai está a subsidiar €3-8
por encomenda para ilhas. Estimar impacto mensal com dados de encomendas.

**DL 24/2014 — custos de envio:** OCULTOS até step 2 do checkout ❌
(utilizador não vê custo de envio na página de produto nem no carrinho sem CEP)

**Free shipping:** €60 threshold. Benchmark sector cuidados: €45-50. Considerar reduzir.

**Tracking:** CTT Expresso integrado ✅ | Link tracking no email: ❌ AUSENTE

**FIX:**
- Separar zona "Ilhas" de "PT Continental" — configurar tarifas CTT correctas
- Mostrar estimativa de envio no carrinho (plugin: WooCommerce Cart Shipping Calculator — activo
  mas desligado — activar em WC > Settings > Shipping > Calculations)
- Adicionar `{tracking_number}` + link CTT no template de email de envio

---

### 6. Post-Purchase — 6/10

**Emails transaccionais:**
- Order confirmation: ✅ Enviado, design com logo Cuidai ✅, info completa ✅
- Shipping notification: ✅ Enviado, MAS sem número de tracking (ver Shipping acima)
- Processing order: ✅
- Cancelled order: ✅

**Compliance:**
- Política de devolução (14 dias DL 24/2014): ✅ Página existe `/politica-de-devolucoes`
  MAS link no footer: ❌ AUSENTE — utilizador tem de a encontrar via pesquisa
- Livro de Reclamações: ❌ AUSENTE no footer — obrigatório por lei
- GDPR delete account: ⚠️ Botão "Apagar conta" existe no My Account MAS dados de encomenda
  não são anonimizados — apenas conta é eliminada (risco RGPD)
- Invoice download (My Account): ✅ via InvoiceXpress plugin

**FIX:**
- Adicionar link "Livro de Reclamações" no footer (widget Footer Links) — urgente
- Adicionar link "Política de Devoluções" no footer
- Corrigir GDPR delete: usar WooCommerce built-in anonymization
  (`wc_maybe_anonymize_order()`) no hook de delete account

---

## Prioridades

### CRÍTICO (fazer esta semana)
1. **Livro de Reclamações no footer** — legal, 1h de trabalho, risco de coima ASAE
2. **IVA 6% nos produtos de apoio domiciliário e higiene** — risco AT, 2h
3. **Separar zonas de envio Ilhas** — perda financeira activa, 1h
4. **GDPR account delete** — anonimizar orders, 3h dev

### IMPORTANTE (semanas 1-2)
1. Activar cart shipping calculator (custos visíveis antes checkout)
2. InvoiceXpress emissão automática via webhook
3. Corrigir mensagem erro MBWay
4. Adicionar PayPal Express como gateway de fallback
5. Preencher alt text 7 produtos

### OTIMIZAÇÃO (quando possível)
1. Reduzir checkout fields (remover Empresa/NIF do fluxo padrão)
2. Progress indicator no checkout
3. Button height 44px mobile
4. Adicionar tracking number nos emails de envio
5. Activar Google Pay via Stripe

---

## Roadmap 4 Semanas

| Semana | Acções | Responsável |
|--------|--------|-------------|
| 1 | Livro Reclamações footer, IVA rates fix, Zonas envio ilhas, GDPR anonymize | Dev Cuidai |
| 2 | InvoiceXpress webhook, PayPal Express, Cart shipping calculator activo | Dev Cuidai + DARIO |
| 3 | Checkout UX (fields, button, progress indicator), Alt text produtos, AggregateRating fix | DARIO |
| 4 | Google Pay activar, Email templates tracking, QA full checkout flow PT+Mobile | Dev Cuidai |
```

---

## Output anti-patterns

- Escrever "MBWay parece estar a funcionar" sem confirmar o flow completo (incluindo mensagem de erro)
- Scores globais calculados sem preencher os 6 scores por categoria primeiro
- Deixar zonas de envio "Portugal" sem verificar se Açores/Madeira estão separadas — é sempre diferente
- Reportar compliance DL 24/2014 sem verificar explicitamente a URL `/checkout` e a página de produto
- Auditoria de tax/IVA sem mapear pelo menos uma categoria de produto contra a tabela AT — "23% correcto" não chega
- Livro de Reclamações marcado como OK por existir algures no site sem confirmar que está no footer
- GDPR "delete account" marcado como OK sem testar se orders ficam anonimizadas (o bug mais comum)
- Roadmap sem responsáveis reais — "..." ou "equipa" não é accionável
- Schema Product validado sem usar Google Rich Results Test — validação visual não detecta erros de `priceCurrency`
- Output entregue com `<Client>`, `XX/100`, `X/10` ou qualquer placeholder angle-bracket por preencher
