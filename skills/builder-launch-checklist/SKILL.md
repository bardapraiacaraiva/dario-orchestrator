---
name: builder-launch-checklist
description: >
  Checklist pre-launch completa: SEO, analytics, monitoring, backups, legal, performance,
  security, social, email. Nada esquecido no dia do lancamento.
  Use quando: launch, lancamento, pre-launch checklist, ir para producao, go-live.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Launch Checklist

## Pre-Launch (1 semana antes)

### Technical
- [ ] All pages load without errors (200 status)
- [ ] Forms submit correctly (test each one)
- [ ] Auth flow works (register → verify → login → dashboard)
- [ ] Payment flow works (if applicable — test with Stripe test mode)
- [ ] Mobile responsive (test on real devices: iPhone, Android)
- [ ] Core Web Vitals: LCP < 2.5s, CLS < 0.1, INP < 200ms
- [ ] Error boundaries catch crashes gracefully
- [ ] 404 page exists and is helpful

### SEO
- [ ] Title tags unique per page (< 60 chars)
- [ ] Meta descriptions per page (< 160 chars)
- [ ] OG image + title + description (test with opengraph.xyz)
- [ ] Sitemap.xml generated and submitted to GSC
- [ ] Robots.txt correct (not blocking important pages)
- [ ] Schema markup (Organization + FAQ minimum)
- [ ] Canonical URLs set

### Analytics & Monitoring
- [ ] GA4 installed and receiving data
- [ ] Key events tracked (signup, CTA click, form submit)
- [ ] Conversion funnels configured
- [ ] Uptime monitoring active (UptimeRobot / Better Stack)
- [ ] Error tracking active (Sentry or equivalent)

### Security
- [ ] HTTPS enforced (no mixed content)
- [ ] Security headers (X-Frame-Options, CSP, HSTS)
- [ ] Rate limiting on auth endpoints
- [ ] CORS configured (whitelist only)
- [ ] Environment variables NOT in client bundle
- [ ] SQL injection tested (if applicable)

### Legal
- [ ] Privacy Policy page (RGPD compliant)
- [ ] Terms of Service page
- [ ] Cookie consent banner (if tracking)
- [ ] Data processing agreement (if B2B)

### Content
- [ ] All placeholder text replaced with real copy
- [ ] Images optimized (WebP, lazy loaded)
- [ ] Favicon set (all sizes: 16, 32, 180, 512)
- [ ] Social media profiles linked
- [ ] Contact information correct

### Backup & Recovery
- [ ] Database backup automated (daily minimum)
- [ ] Backup restore tested at least once
- [ ] Rollback procedure documented

## Launch Day
- [ ] Deploy to production
- [ ] Verify all pages live
- [ ] Test critical flows one more time
- [ ] Monitor error logs (first 2 hours)
- [ ] Announce (social media, email, Product Hunt if applicable)

## Post-Launch (first week)
- [ ] Monitor analytics daily
- [ ] Check error rates
- [ ] Collect user feedback (first 5 users)
- [ ] Fix critical bugs within 24h
- [ ] Plan V1.1 based on real usage data

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Technical completeness
- [ ] Todos os items técnicos têm critérios mensuráveis (ex: LCP < 2.5s, não "site rápido")
- [ ] Auth flow, payment flow e forms testados com resultado documentado (pass/fail + data)
- [ ] Core Web Vitals com valores reais medidos (Lighthouse score ou PageSpeed URL)
- ❌ NOT delivery-ready: `- [ ] Site funciona bem no mobile`
- ✅ Delivery-ready: `- [x] Mobile responsive testado em iPhone 14 (iOS 17) e Samsung A54 (Android 13) — 2024-11-15`

### Gate 2 — SEO items preenchidos com dados reais
- [ ] Title tags listadas por página com character count real
- [ ] OG image URL confirmada (não placeholder) e testada em opengraph.xyz
- [ ] Sitemap.xml URL verificada e submetida no Google Search Console (screenshot ou data)
- [ ] Robots.txt copiado ou linkado — não apenas "exists"
- ❌ NOT delivery-ready: `- [ ] OG tags configuradas`
- ✅ Delivery-ready: `- [x] OG image: cuidai.pt/og-home.png (1200×630px) — testado opengraph.xyz 2024-11-14 ✓`

### Gate 3 — Analytics & Monitoring activos com confirmação
- [ ] GA4 Measurement ID real documentado (ex: G-XXXXXXX) e evento de teste visible no DebugView
- [ ] Uptime monitor URL confirmada (UptimeRobot/Better Stack link) + alertas para email real
- [ ] Sentry DSN configurado e erro de teste enviado com sucesso
- [ ] Funis de conversão nomeados com os eventos reais tracked
- ❌ NOT delivery-ready: `- [ ] Analytics instalado`
- ✅ Delivery-ready: `- [x] GA4 G-4K29MXLQ81 activo — signup + cta_click confirmados DebugView 2024-11-15`

### Gate 4 — Security checklist com evidências
- [ ] Security headers verificados via securityheaders.com (grade mínimo B+)
- [ ] HTTPS sem mixed content confirmado (Chrome DevTools → Console limpa)
- [ ] Rate limiting testado (endpoint auth com >10 req/min → 429 recebido)
- [ ] `.env` não exposto — verificado no bundle final (grep ou Network tab)
- ❌ NOT delivery-ready: `- [ ] Security headers configurados`
- ✅ Delivery-ready: `- [x] securityheaders.com: Grade A — HSTS, CSP, X-Frame-Options ✓ (2024-11-15)`

### Gate 5 — Legal com datas e conformidade RGPD
- [ ] Privacy Policy com data de última actualização e DPO contact visível
- [ ] Cookie banner testado: accept/reject funcionais, preferências guardadas
- [ ] Se B2B: DPA assinado ou template linkado com nome do cliente
- [ ] Terms of Service com jurisdição e lei aplicável explícitos (ex: Lei Portuguesa)
- ❌ NOT delivery-ready: `- [ ] Privacy Policy existe`
- ✅ Delivery-ready: `- [x] Privacy Policy cuidai.pt/privacidade — última actualização 2024-11-10, conforme RGPD Art. 13, DPO: legal@cuidai.pt`

### Gate 6 — Output uses CLIENT NAME + REAL data, no placeholder angle-brackets
- [ ] Zero ocorrências de `<client>`, `<url>`, `<date>`, `[INSERT]` ou similar
- [ ] Nome real do produto/empresa em todos os headers e exemplos
- [ ] URLs reais (não `https://example.com`) em todos os items verificáveis
- [ ] Datas reais de teste documentadas (formato YYYY-MM-DD)
- ❌ NOT delivery-ready: `- [ ] Sitemap submetido para <GSC_PROPERTY>`
- ✅ Delivery-ready: `- [x] Sitemap saquei.pt/sitemap.xml submetido GSC property saquei.pt — 2024-11-14`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / memória / dados reais do cliente
- 🟡 **assumed** — plausível mas precisa confirmação do cliente antes da entrega
- 🟢 **projection** — forecast by design (não verificável no momento)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs o que precisa verify. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready:
```
- [x] Core Web Vitals passaram — LCP 1.8s, CLS 0.04
- [x] GA4 activo com eventos signup e cta_click
- [x] Uptime monitor activo, alertas configurados
```
*(reader assume que tudo é verified — pode ser assumption ou test environment)*

✅ Delivery-ready:
```
- [x] 🔵 LCP 1.8s, CLS 0.04 — medido PageSpeed URL producao 2024-11-15
- [x] 🟡 GA4 G-XXXXXXX eventos signup/cta_click — visíveis em dev, assumido igual em prod (confirmar DebugView pós-deploy)
- [x] 🟢 Error rate < 0.5% na primeira semana — projecção baseada em load test, não tráfego real
- [x] 🟡 Privacy Policy RGPD-compliant — template aplicado, DPO contact assume-se correcto (cliente deve validar)
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir assumptions com actuals (ex: GA4 Measurement ID real, dispositivos reais testados, DPO contact validado)
- [ ] All 🔵 items têm data + fonte citada (ex: Lighthouse URL, securityheaders.com grade, Sentry test event)
- [ ] All 🟢 projections comunicadas explicitamente ao cliente como forecast — não como resultados garantidos

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# CUIDAI — Launch Checklist | Target Launch: 2024-11-20

## Pre-Launch (semana de 2024-11-13)

### Technical
- [x] All pages load 200: /, /cuidadores, /familia, /sobre, /contacto — verificado 2024-11-15
- [x] Form "Encontrar Cuidador" testado: submissão → email recebido ops@cuidai.pt ✓
- [x] Auth flow: register → email Resend verificado → login → dashboard ✓ (2024-11-14)
- [x] Mobile: iPhone 14 iOS 17 ✓ | Samsung Galaxy A54 Android 13 ✓ (2024-11-15)
- [x] Core Web Vitals (PageSpeed cuidai.pt): LCP 1.8s ✓ | CLS 0.04 ✓ | INP 140ms ✓
- [x] 404 page activa em cuidai.pt/pagina-que-nao-existe — redireciona para /

### SEO
- [x] Title tags: Homepage "Cuidadores em Portugal | Cuidai" (42 chars) ✓
- [x] Meta descriptions: todas < 155 chars — revisado Screaming Frog 2024-11-14
- [x] OG image: cuidai.pt/og-home.png 1200×630px — testado opengraph.xyz 2024-11-15 ✓
- [x] Sitemap: cuidai.pt/sitemap.xml — submetido GSC property cuidai.pt (2024-11-13)
- [x] Robots.txt: /robots.txt — permite Googlebot, bloqueia /dashboard/ ✓
- [x] Schema: Organization (cuidai.pt) + FAQ (página /como-funciona) — validado Rich Results Test ✓
- [x] Canonicals: configurados next-seo em todas as páginas ✓

### Analytics & Monitoring
- [x] GA4 G-8XMKP39V2C instalado — eventos signup + cta_cuidador_click confirmados DebugView ✓
- [x] Funil "Registo Família": landing → /registar → /dashboard — configurado GA4 2024-11-14
- [x] UptimeRobot: monitor cuidai.pt activo, alertas → ops@cuidai.pt + Slack #incidents ✓
- [x] Sentry DSN configurado, erro de teste enviado e recebido dashboard Sentry 2024-11-15 ✓

### Security
- [x] securityheaders.com: Grade A (HSTS, CSP, X-Frame-Options, Referrer-Policy) — 2024-11-15
- [x] HTTPS: Chrome DevTools Console limpa, zero mixed content ✓
- [x] Rate limiting /api/auth/login: 429 recebido ao 11º request/min — testado 2024-11-14
- [x] .env não exposto: grep "SUPABASE_KEY" bundle/chunks → 0 resultados ✓
- [x] CORS: whitelist [cuidai.pt, www.cuidai.pt] — testado origem maliciosa → bloqueada ✓

### Legal
- [x] Privacy Policy: cuidai.pt/privacidade — actualizada 2024-11-10, RGPD Art. 13 ✓
- [x] Terms of Service: cuidai.pt/termos — jurisdição PT, lei portuguesa, data 2024-11-01 ✓
- [x] Cookie banner: accept/reject funcional, preferências em localStorage ✓ — Cookiebot
- [x] DPA template disponível para parceiros B2B (clínicas) — linkado em /parceiros

### Content
- [x] Zero texto placeholder — Screaming Frog "Lorem ipsum" scan: 0 resultados ✓
- [x] Imagens WebP + lazy load: todas < 150KB, Lighthouse images score 94 ✓
- [x] Favicon: 16×16, 32×32, 180×180 (apple-touch), 512×512 — testado Chrome + Safari ✓
- [x] Contacto: info@cuidai.pt | +351 910 000 000 — verificado página /contacto ✓

### Backup & Recovery
- [x] Supabase backups diários activos (plano Pro) — confirmado dashboard 2024-11-13
- [x] Restore testado 2024-11-12: restaurado BD de staging em 4 min ✓
- [x] Runbook rollback documentado: Notion "Cuidai > Ops > Rollback Procedure" ✓

## Launch Day — 2024-11-20
- [ ] Deploy Vercel production branch main → cuidai.pt (09:00)
- [ ] Smoke test: /, /registar, /cuidadores, form submit (09:15)
- [ ] Monitor Sentry + UptimeRobot primeiras 2h (09:00–11:00)
- [ ] Anúncio LinkedIn + Instagram 10:00 | Email lista 847 subscritores 10:30

## Post-Launch (semana 2024-11-20 a 2024-11-27)
- [ ] Analytics daily review 09:00 (funil registo + bounce rate homepage)
- [ ] Recolher feedback primeiros 5 utilizadores (form Typeform linkado no dashboard)
- [ ] Bugs críticos: SLA 24h → fix + deploy hotfix Vercel
- [ ] Plano V1.1 com base em dados reais: reunião 2024-11-27
```

---

## Output anti-patterns

- Checklist com items binários sem critério mensurável — "funciona" não é critério, "LCP 1.8s < 2.5s ✓" é
- Datas ausentes nos items testados — cada verificação precisa de timestamp, sem data é inválida para auditoria
- URLs genéricas tipo `https://example.com` ou `yoursite.pt` — sempre o domínio real do cliente
- Gate de segurança sem evidência externa — "headers configurados" sem grade securityheaders.com ou similar não passa
- Analytics "instalado" sem Measurement ID real e evento confirmado no DebugView
- Legal sem data de actualização e jurisdição explícita — "Privacy Policy existe" é insuficiente para RGPD
- Launch Day sem hora — "deploy to production" sem timestamp cria ambiguidade em rollbacks e post-mortems
- Backup "activo" sem teste de restore documentado — backup nunca testado = backup inexistente
- OG image sem dimensões e sem teste em ferramenta (opengraph.xyz / Twitter Card Validator)
- Mistura de items não-aplicáveis sem marcação explícita — se payment não existe, marcar `N/A — sem pagamentos nesta versão` não omitir silenciosamente
