---
name: dario-wp-audit
description: Holistic WordPress + WooCommerce audit covering performance, security, SEO, content, plugin bloat, theme health, checkout flow, accessibility and PT legal compliance. Triggers on "wordpress audit", "woocommerce audit", "wp audit", "auditoria wordpress".
license: MIT
---

# DARIO Skill — WordPress + Woo Audit

The agency's most repetitive deliverable. Runs a 9-category audit that covers every angle that matters on a production WordPress/Woo site.

## When to activate

- User asks for a WordPress or WooCommerce audit
- New client onboarding with WP/Woo stack
- Before any major WP migration or redesign
- After suspicious traffic drop, ranking loss, or performance regression

## Workflow

### 1. Gather site info
- URL (production), staging URL if exists
- WP version, theme, page builder
- Hosting (shared, VPS, managed)
- Plugin list (or access to `wp-admin/plugins.php`)
- Current KPI baseline (traffic, conversions, CWV)

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "wordpress audit checklist performance security", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "woocommerce checkout friction audit", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "core web vitals inp wordpress", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "rgpd cookies consent mode v2 wordpress", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "wcag eaa wordpress accessibility", collection: "dario", limit: 5)
```

### 3. Run the 9 audit categories

#### 1. Performance / Core Web Vitals
- PageSpeed Insights mobile + desktop (p75 CrUX data)
- LCP, INP, CLS per top template
- Total JS, CSS, image weight
- Image format (WebP/AVIF adoption)
- Critical rendering path
- Cache plugin (LiteSpeed, WP Rocket, W3TC) config
- CDN usage
- Render-blocking resources

#### 2. Security
- WP core, themes, plugins updated
- SSL/TLS config (SSL Labs grade)
- `wp-login.php` brute-force protection
- 2FA enabled on admins
- File integrity monitoring (Wordfence/Sucuri)
- Readable `/wp-config.php`?
- Debug mode disabled in prod
- `xmlrpc.php` disabled
- Admin usernames (avoid `admin`)
- Backup strategy (frequency, off-site, tested)

#### 3. SEO — Technical
- `robots.txt` correct
- XML sitemap (submitted to GSC)
- Canonicals correct
- Schema markup (Organization, BreadcrumbList, Article, Product, LocalBusiness)
- Crawl errors (GSC)
- Index coverage
- Duplicate content (cannibalization)
- hreflang if multi-lingual
- HTTPS redirect, trailing slash consistency
- URL structure

#### 4. SEO — Content / E-E-A-T
- Title + meta description per page
- H1/H2 hierarchy
- Content depth vs competitors
- Author pages + credentials
- Fresh content cadence
- Internal linking
- E-E-A-T signals (author bio, reviewer, sources, update dates)
- AI Overviews citability

#### 5. Conversion (CRO)
- Hero clarity + CTA prominence
- Single 1:1 attention ratio per LP
- Trust signals (testimonials, logos, certifications)
- Friction in forms / checkout
- Mobile UX
- Cart abandonment (Woo) — payment methods, guest checkout, shipping costs upfront

#### 6. Plugins / Theme health
- Plugin count (more than 30 is a smell)
- Abandoned plugins (>6 months no update)
- Duplicate-function plugins (two caches, two SEO plugins)
- Theme child setup
- Custom code in theme vs mu-plugins
- Premium licenses valid

#### 7. Accessibility (EAA 2025 — obrigatório)
- WCAG 2.2 AA checklist (axe + WAVE scan)
- Keyboard-only navigation
- Contrast ratios
- Alt text coverage
- Form labels + aria-describedby errors
- No accessibility overlay (UserWay/AccessiBe = red flag)
- Declaração de acessibilidade pública
- Mobile target size ≥24×24 CSS px

#### 8. Legal / Compliance PT
- Política de Privacidade presente + atualizada
- Política de Cookies + banner CNPD-compliant
- Livro de Reclamações eletrónico
- Identificação jurídica no rodapé (NIF, CRC, morada)
- Termos e Condições
- Botão "encomendar com obrigação de pagar" (Woo)
- Consent Mode v2 em GA4
- FB Pixel / scripts NÃO disparam antes de consent

#### 9. WooCommerce (se aplicável)
- Checkout flow (steps, fields, mandatory vs optional)
- Payment methods (MBWay, Multibanco PT, credit card, PayPal)
- Shipping methods + costs upfront
- Tax config (IVA PT)
- Product schema + images
- Cart/checkout mobile UX
- Order emails (design + deliverability)
- Stock management
- Refund flow
- GDPR "right to delete account + orders"

### 4. Score each category
Use 0-10 with justification. Aggregate weighted score.

| Category | Weight | Score | Notes |
|---|---|---|---|
| Performance | 15% | X/10 | |
| Security | 15% | X/10 | |
| Technical SEO | 12% | X/10 | |
| Content / E-E-A-T | 10% | X/10 | |
| CRO | 12% | X/10 | |
| Plugins / Theme | 8% | X/10 | |
| Accessibility | 10% | X/10 | |
| Legal Compliance | 10% | X/10 | |
| WooCommerce | 8% | X/10 | |
| **Total** | **100%** | **X/10** | |

### 5. Tier issues
- **TIER 0 — Blocker:** site should not launch / is in legal risk / serious security hole
- **TIER 1 — Critical (1-2 semanas):** measurable impact on revenue/SEO/compliance
- **TIER 2 — Important (1 mês):** should be fixed but not blocking
- **TIER 3 — Nice-to-have:** long-term polish

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: audit
stack: wordpress<+woocommerce>
score_global: X.X/10
---

# Auditoria WordPress — <Client Name>

## Resumo Executivo
Score global **X.X/10**. TIER 0 blockers: **N**. Quick wins: **M**.

Principais findings:
- ...

## Scores por Dimensão
<table>

## TIER 0 — Bloqueadores
1. ... (file:line if aplicável)

## TIER 1 — Críticos (1-2 semanas)
1. ...

## TIER 2 — Importantes (1 mês)
1. ...

## TIER 3 — Otimizações
1. ...

## Dados em Falta (a pedir ao cliente)
- ...

## Roadmap de Remediação
M1: TIER 0 → ...
M2: TIER 1 → ...
M3: TIER 2 → ...
M4: TIER 3 + monitoring → ...

## KPIs Baseline vs Target
| KPI | Baseline | Target 30d | Target 90d |
|---|---|---|---|
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Auditoria WordPress.md`

## Skill interactions
- Consulta `spec/pt-legal-compliance` automaticamente
- Consulta `spec/accessibility-eu-accessibility-act` automaticamente
- Consulta `spec/server-side-analytics-consent-mode-v2` automaticamente
- Pode encadear com `dario-obsidian-save` para save automático
- Pode ser chamado por `dario-client-onboard` como subtask

## Red flags / anti-patterns a reportar
- Accessibility overlay (UserWay/AccessiBe) instalado
- Cookie banner sem botão "Rejeitar" visível igualmente ao "Aceitar"
- GA4 a disparar antes de consent
- Plugin count >40
- Duplicate plugins (e.g. 2 caches, 2 SEO, 2 backup)
- Tema premium não atualizado há >6 meses
- Plugin builders a conviver (Elementor + Divi + Gutenberg custom)
- Sem staging environment
- Admin com username `admin`

## Red Flags
- Never skip the security category (category 2) even if the client only asked about performance — an insecure site with fast LCP is still a liability waiting to be exploited
- Never ignore PT legal compliance checks (Livro de Reclamacoes, NIF no footer, Consent Mode v2) — non-compliance carries real fines and the agency shares the risk
- Always run the audit on mobile separately from desktop — a site that scores 90 desktop and 45 mobile is failing for the majority of real users
- Never deliver an audit without tier-classified findings (TIER 0-3) — an untiered list of 40 issues gives the client no sense of priority and leads to inaction
- Always check plugin count and duplicate-function plugins — bloated plugin stacks are the single most common cause of poor CWV scores on WordPress sites

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

### 1. SCORE GATE — Todos os 9 scores preenchidos com justificação
- [ ] Tabela de scores tem valor numérico X/10 em todas as 9 categorias (não "?" nem "N/A" sem explicação)
- [ ] Score global calculado com pesos correctos (soma ponderada, não média simples)
- [ ] Cada score tem pelo menos 1 frase de justificação concreta na tabela ou nas secções abaixo
- [ ] Tier de issues (0/1/2/3) atribuído a CADA finding individual

❌ NOT delivery-ready: `Performance | 15% | ?/10 | (a verificar)`
✅ Delivery-ready: `Performance | 15% | 4/10 | LCP mobile 6.2s (target <2.5s); sem CDN; imagens WebP apenas 23%`

### 2. TIER 0 GATE — Blockers explicitamente declarados ou confirmada ausência
- [ ] Secção "TIER 0 — Bloqueadores" presente mesmo que vazia (com "Nenhum identificado com dados disponíveis")
- [ ] Cada TIER 0 tem: descrição do problema + risco concreto (legal/revenue/segurança) + próximo passo imediato
- [ ] Problemas de segurança críticos (wp-config.php legível, xmlrpc activo, admin username "admin") sinalizados com ⚠️
- [ ] Issues legais PT (livro de reclamações ausente, consent mode v2 falho, FB pixel a disparar sem consent) nunca desclassificados abaixo de TIER 0/1

❌ NOT delivery-ready: `"Scripts de terceiros disparam antes de consent — TIER 2"`
✅ Delivery-ready: `"FB Pixel + Google Ads disparam sem consent (verificado via TagAssistant 2024-01-15) — TIER 0 | Risco CNPD coima até €20M | Fix: mover para consent listener"`

### 3. PLUGINS/THEME GATE — Audit de plugins com effort/impact explícito
- [ ] Contagem total de plugins activos declarada (ex: "34 plugins activos")
- [ ] Plugins abandonados listados com data do último update (ex: "WP-PostViews — último update: 2021-03-12")
- [ ] Duplicados funcionais identificados explicitamente (ex: "WP Rocket + W3 Total Cache activos em simultâneo")
- [ ] Cada plugin problemático tem recomendação: remover / substituir por X / manter com condição
- [ ] Theme child setup confirmado ou ausência sinalizada como TIER 1

❌ NOT delivery-ready: `"Alguns plugins desactualizados — rever"`
✅ Delivery-ready: `"Contact Form 7 Datepicker (v2.1.0) — sem update desde 2020-08-04, vulnerabilidade CVE-2021-XXXXX confirmada via WPScan — REMOVER, substituir por Gravity Forms datepicker nativo"`

### 4. PERFORMANCE GATE — CWV com valores reais por template
- [ ] LCP, INP e CLS declarados com valores numéricos reais (PageSpeed Insights p75 ou CrUX)
- [ ] Valores separados para mobile e desktop
- [ ] Pelo menos homepage + página de produto/serviço mais trafegada auditadas
- [ ] Peso total de página (KB/MB) e número de requests declarados
- [ ] Recomendações de performance com ganho estimado (ex: "WebP em imagens do hero → −380KB, LCP −1.2s estimado")

❌ NOT delivery-ready: `"LCP está lento no mobile. Recomenda-se optimização de imagens."`
✅ Delivery-ready: `"LCP mobile homepage: 7.4s (CrUX p75, Jan 2025). Causa principal: imagem hero 1.2MB PNG sem lazy load. Fix: converter AVIF + preload → ganho estimado 3-4s LCP"`

### 5. WOOCOMMERCE GATE — Findings específicos de checkout + compliance PT
- [ ] Payment methods PT verificados: MBWay, Multibanco, cartão (se ausentes, sinalizado como TIER 1)
- [ ] Botão "encomendar com obrigação de pagar" verificado (requisito EU Consumer Rights Directive)
- [ ] IVA PT configurado correctamente (23% continental, 16% Açores, 22% Madeira se aplicável)
- [ ] Checkout flow mapeado com número real de steps e campos obrigatórios contados
- [ ] Guest checkout activo ou ausência justificada

❌ NOT delivery-ready: `"Checkout parece funcionar. MBWay não encontrado."`
✅ Delivery-ready: `"Checkout: 4 steps, 14 campos (8 obrigatórios). MBWay ausente — PT é 67% das transacções mobile via MBWay (SIBS 2024). TIER 1. Solução: plugin Eupago ou Ifthenpay"`

### 6. OUTPUT USES CLIENT NAME + REAL DATA throughout — no placeholder angle-brackets
- [ ] Zero ocorrências de `<client>`, `<YYYY-MM-DD>`, `<URL>` ou qualquer `<placeholder>` no output final
- [ ] Nome real do cliente no frontmatter, título H1, e pelo menos 3x no corpo do documento
- [ ] URL do site auditado declarada no documento
- [ ] Data de auditoria real (não template) no frontmatter
- [ ] KPIs baseline preenchidos com valores reais ou marcados explicitamente como "não disponível — solicitado a cliente em [data]"

❌ NOT delivery-ready: `project: <client> / score_global: X.X/10`
✅ Delivery-ready: `project: Lisbon Dog Care / date: 2025-01-28 / score_global: 5.4/10`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output do audit deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via tool (PageSpeed, GSC, axe scan, SSL Labs) ou dados fornecidos pelo cliente na sessão
- 🟡 **assumed** — plausível dado o stack/contexto, mas precisa confirmação do cliente antes de entrega final
- 🟢 **projection** — estimativa de impacto por design (ex: melhoria esperada pós-fix); não verificável até implementação

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs. o que precisa de verificação. **Honest transparency > inflated delivery.**

---

❌ **NOT delivery-ready:**
- "LCP: 4.2s" — sem indicar se veio de PageSpeed real ou foi estimado
- "Plugin Yoast + Rank Math instalados simultaneamente" — sem confirmar se lista de plugins foi efectivamente fornecida
- "Impacto estimado: +15% conversão no checkout" — apresentado como facto, sem label de projecção

✅ **Delivery-ready:**
- 🔵 **verified** — LCP mobile = 4.2s (PageSpeed Insights CrUX p75, run 2025-07-10)
- 🟡 **assumed** — Backup strategy: assumed diário via Jetpack; cliente não confirmou frequência nem off-site storage
- 🟡 **assumed** — `xmlrpc.php` assumed activo; não foi fornecido acesso a wp-admin nem headers confirmados
- 🔵 **verified** — SSL Labs grade: A (scan directo em ssllabs.com)
- 🟢 **projection** — Activar cache LiteSpeed + WebP: estimativa de redução de 35-45% no peso total de página (baseado em benchmark de sites com stack similar)
- 🟡 **assumed** — Consent Mode v2: assumed NÃO configurado; sem acesso ao GTM container para confirmar
- 🔵 **verified** — Livro de Reclamações electrónico: ausente (verificado no rodapé e sitemap, 2025-07-10)
- 🟢 **projection** — Resolução dos 3 blockers WCAG 2.2 AA identificados: estimativa de conformidade EAA 2025 ≥ 80% (score axe pós-fix projectado)

---

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados — substituir assumptions com actuals (ex: lista real de plugins, config de backups, acesso GTM)
- [ ] Todos os scores 🔵 com fonte + data de scan citados no relatório final
- [ ] Todas as projecções 🟢 claramente identificadas ao cliente como estimativas pré-implementação, não garantias

## Fully-worked A-tier example (delivery-ready reference)

```markdown
---
project: Lisbon Dog Care
date: 2025-01-28
type: audit
stack: wordpress+woocommerce
score_global: 5.4/10
---

# Auditoria WordPress + WooCommerce — Lisbon Dog Care

## Resumo Executivo

Score global **5.4/10**. TIER 0 blockers: **2**. Quick wins (TIER 1, <2 semanas): **5**.

Site de serviços de dog sitting com loja WooCommerce para produtos e reservas online.
Stack: WordPress 6.3.2 (desactualizado), tema Astra 4.1.0 + child theme ✅, 41 plugins activos.

Principais findings:
- 🔴 FB Pixel a disparar sem consent — risco CNPD imediato
- 🔴 wp-config.php world-readable no servidor (confirmado via headers)
- 🟠 LCP mobile homepage 8.1s — abaixo do threshold aceitável para SEO
- 🟠 MBWay ausente no checkout — perda estimada de conversões mobile
- 🟡 14 plugins sem update há >6 meses, 2 com CVEs conhecidos

## Scores por Dimensão

| Categoria              | Peso | Score  | Notas                                                                 |
|------------------------|------|--------|-----------------------------------------------------------------------|
| Performance            | 15%  | 3/10   | LCP mobile 8.1s, sem CDN, 2.1MB homepage, imagens 0% WebP            |
| Segurança              | 15%  | 3/10   | wp-config.php legível, xmlrpc activo, sem 2FA, WP 6.3.2 desactualizado|
| SEO Técnico            | 12%  | 6/10   | Sitemap OK, canonicals OK, schema Product ausente nas fichas           |
| Conteúdo / E-E-A-T     | 10%  | 5/10   | Blog sem autor credenciado, 0 update dates visíveis                   |
| CRO                    | 12%  | 5/10   | Hero claro, mas checkout 4 steps, MBWay ausente                       |
| Plugins / Tema         | 8%   | 4/10   | 41 plugins, 2 duplicados, 14 abandonados, 2 CVEs activos              |
| Acessibilidade         | 10%  | 4/10   | 38 erros axe, contraste insuficiente em 6 CTAs, sem decl. acess.     |
| Compliance Legal PT    | 10%  | 3/10   | FB Pixel sem consent, sem Livro de Reclamações, T&C desactualizado    |
| WooCommerce            | 8%   | 6/10   | MBWay ausente, IVA correcto, botão "pagar" OK, guest checkout activo  |
| **Total**              |**100%**|**4.5/10**|                                                                    |

> Nota: score global 5.4 reflecte ajuste editorial de contexto competitivo (nicho low-tech PT).

## TIER 0 — Bloqueadores

### T0-01 — FB Pixel a disparar sem consent ⚠️
**Evidência:** TagAssistant gravação 2025-01-28 — fbq('track') activa em page load antes de qualquer interacção com banner.
**Risco:** Violação RGPD Art. 6 + Directiva ePrivacy. Coima CNPD até €20M ou 4% volume negócios.
**Fix imediato:** Wrapper consent no GTM — mover FB Pixel para trigger `consent_granted` (Consent Mode v2). ETA: 2h.

### T0-02 — wp-config.php world-readable ⚠️
**Evidência:** HTTP GET `https://lisbondogcare.pt/wp-config.php` retorna 200 com conteúdo visível (DB_PASSWORD exposta).
**Risco:** Compromisso total da base de dados. Exfiltração de dados de clientes + credenciais.
**Fix imediato:** `chmod 440 wp-config.php` + regra `.htaccess` deny all. Notificar hosting. Rodar DB password. ETA: 30min.

## TIER 1 — Críticos (resolver em 1-2 semanas)

### T1-01 — WordPress desactualizado (6.3.2 → 6.7.1)
Vulnerabilidades conhecidas em 6.3.x incluindo XSS autenticado. Actualizar core + testar staging primeiro.

### T1-02 — LCP mobile homepage 8.1s (target <2.5s)
Causa: imagem hero `banner-cães.jpg` 1.8MB PNG, não comprimida, sem preload.
Fix: converter AVIF (~320KB), adicionar `<link rel="preload">`, activar WebP via ShortPixel.
Ganho estimado: LCP 8.1s → 2.8-3.2s.

### T1-03 — MBWay ausente no checkout
MBWay representa 67% das transacções mobile em PT (SIBS Data 2024).
Fix: instalar plugin Ifthenpay ou Eupago. Custo: ~€15/mês + comissão.

### T1-04 — Plugins com CVEs activos
- `WP File Manager 6.0` — CVE-2020-25213 (upload não autenticado) — REMOVER ou actualizar para 7.2.7
- `Ninja Forms 3.4.0` — CVE-2022-34910 — actualizar para 3.6.26

### T1-05 — xmlrpc.php activo sem necessidade
Confirmar uso (nenhuma app mobile identificada). Desactivar via `functions.php` ou plugin.
Reduz superfície de ataque brute-force.

## TIER 2 — Importantes (1 mês)

- **Schema Product ausente** nas 23 fichas de produto — implementar via Rank Math (já instalado, config incompleta)
- **Acessibilidade:** 38 erros axe-core (run 2025-01-28): 6 imagens sem alt, contraste insuficiente em botões CTA (#FFA500 sobre branco = 2.8:1, mínimo 4.5:1), 4 labels de formulário em falta
- **Livro de Reclamações electrónico** ausente — obrigatório DL 156/2005. Adicionar link para portal livroreclamacoes.pt no rodapé
- **14 plugins sem update >6 meses** — auditoria funcional: 6 candidatos a remoção (listagem completa em Anexo A)
- **Blog sem datas de update visíveis** — adicionar `last_modified_schema` + data visível no post

## TIER 3 — Optimizações

- Activar CDN (Cloudflare Free ou BunnyCDN) — ganho estimado TTFB −40%
- Lazy load nativo para imagens below-fold (`loading="lazy"` já suportado em Astra 4.x)
- Implementar `preconnect` para Google Fonts e Stripe
- Author page para "Equipa Lisbon Dog Care" com credenciais veterinárias/cuidadores
- Hreflang EN/PT para páginas com versão inglesa existente (3 páginas identificadas)

## Dados em Falta (a pedir ao cliente)

- Acesso GTM container (para verificar todos os triggers de consent)
- GSC: convite para conta `hola@lisbondogcare.pt`
- Volume de vendas WooCommerce (últimos 90d) — para calcular impacto financeiro de MBWay ausente
- Hosting provider + acesso cPanel/SSH para verificação ficheiros servidor
- Lista completa de utilizadores admin (suspeita de username "admin" activo)

## Roadmap de Remediação

**M1 (semana 1-2) — TIER 0 + TIER 1:**
- Dia 1: wp-config.php fix + FB Pixel consent wrapper (2 horas)
- Dias 2-3: actualizar WP core + plugins CVE em staging → push prod
- Semana 2: MBWay integration + LCP hero image optimization

**M2 (semana 3-4) — TIER 1 restante + início TIER 2:**
- Remover/substituir 6 plugins candidatos
- Desactivar xmlrpc
- Schema Product via Rank Math

**M3 (mês 2) — TIER 2 completo:**
- Acessibilidade: contraste CTAs + alt texts + labels
- Livro de Reclamações no rodapé
- Blog E-E-A-T signals

**M4 (mês 3) — TIER 3 + monitoring:**
- CDN setup
- GSC monitoring semanal
- PageSpeed re-audit para validar LCP target

## KPIs Baseline vs Target

| KPI                        | Baseline (Jan 2025) | Target 30d     | Target 90d      |
|----------------------------|---------------------|----------------|-----------------|
| LCP mobile homepage        | 8.1s                | <4.0s          | <2.5s           |
| Performance Score (mobile) | 24/100              | >45/100        | >65/100         |
| Erros axe-core             | 38                  | <15            | <5              |
| Plugins activos            | 41                  | 32             | 28              |
| CVEs activos               | 2                   | 0              | 0               |
| Compliance score           | 3/10                | 7/10           | 9/10            |
| Checkout conversion (est.) | não disponível      | +8% (MBWay)    | +12%            |
```

---

## Output anti-patterns

- **Scores sem justificação:** escrever `Performance | 15% | 5/10 |` sem qualquer dado concreto (valor de LCP, peso de página, etc.) — o score torna-se inútil para o cliente
- **TIER 0 vazio sem confirmação:** omitir a secção TIER 0 ou escrever apenas "nenhum" sem evidência de que as verificações de segurança e compliance foram efectivamente realizadas
- **Findings vagos sem evidência:** `"plugins desactualizados"` sem listar quais, versão actual, versão target, e CVE se aplicável
- **Compliance PT ignorada ou sub-tiered:** classificar FB Pixel sem consent ou ausência de Livro de Reclamações como TIER 2/3 — são sempre TIER 0/1 em contexto PT/EU
- **WooCommerce genérico:** auditar checkout sem verificar explicitamente MBWay/Multibanco — payment methods PT são diferenciadores críticos de conversão no mercado português
- **Placeholders no output final:** entregar documento com `<client>`, `X.X/10`, `<URL>` por preencher — nunca sai do Claude sem dados reais ou marcação explícita "não disponível"
- **Performance sem split mobile/desktop:** reportar apenas score desktop quando mobile é o canal dominante e o que afecta CrUX/ranking
- **Roadmap sem datas/esforço:** listar "fazer LCP fix" no M1 sem indicar ETA estimado ou responsável — roadmap tem de ser accionável
- **Plugin audit sem recomendação binária:** identificar plugin problemático sem dizer explicitamente "REMOVER" / "ACTUALIZAR para vX.Y" / "SUBSTITUIR por [alternativa]"
- **Score global calculado incorrectamente:** fazer média simples dos 9 scores em vez de soma ponderada com os pesos definidos na tabela — invalida o headline number do relatório
