---
name: seo-local
description: >
  Local SEO analysis covering Google Business Profile optimization, NAP
  consistency, citation health, review signals, local schema markup,
  location page quality, multi-location SEO, and industry-specific
  recommendations. Detects business type (brick-and-mortar, SAB, hybrid)
  and industry vertical (restaurant, healthcare, legal, home services,
  real estate, automotive). Use when user says "local SEO", "Google
  Business Profile", "GBP", "map pack", "local pack", "citations",
  "NAP consistency", "local rankings", "service area", "multi-location",
  or "local search".
user-invokable: true
argument-hint: "[url]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# Local SEO Analysis (March 2026)

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| GBP signals share of local pack weight | 32% | Whitespark 2026 |
| Proximity share of ranking variance | 55.2% | Search Atlas ML study |
| Review signals share (up from 16%) | ~20% | Whitespark 2026 |
| Google searches seeking local info | 46% | Industry data |
| Mobile "near me" searches leading to visit in 24h | 76% | Google confirmed |
| ChatGPT/AI usage for local recommendations | 45% (up from 6%) | BrightLocal LCRS 2026 |
| ChatGPT local conversion rate | 15.9% | Seer Interactive |
| Google organic local conversion rate | 1.76% | Seer Interactive |
| Local pack ads growth (Jan 2025 to Jan 2026) | 1% to 22% | Sterling Sky |

---

## Business Type Detection

Detect from page signals before analysis. This determines which checks apply.

### Brick-and-Mortar
- Physical street address visible in page content or footer
- Google Maps embed with pin/directions
- "Visit us at", "Located at", "Come see us"
- Structured address in LocalBusiness schema

### Service Area Business (SAB)
- No visible physical address
- Service area mentions: "serving [city/region]", "service area includes"
- "We come to you", "On-site service", "Mobile [service]"
- `areaServed` in schema without `address.streetAddress`

### Hybrid
- Both physical address AND service area language present
- "Visit our showroom" combined with "We also serve [areas]"

**Impact on checks**: SABs skip embedded map verification and physical address consistency. Brick-and-mortar gets full NAP + map checks.

---

## Industry Vertical Detection

Detect from page signals and GBP category patterns. Routes to industry-specific checks from `references/local-schema-types.md`.

| Vertical | Detection Signals |
|----------|------------------|
| **Restaurant** | /menu, menu items, reservations, cuisine types, food ordering, "dine-in", "takeout" |
| **Healthcare** | insurance accepted, patients, appointments, NPI, medical terms, "Dr.", HIPAA notice |
| **Legal** | attorney, lawyer, practice areas, bar admission, case results, "free consultation" |
| **Home Services** | service area, emergency service, "free estimate", licensed/insured/bonded, "24/7" |
| **Real Estate** | listings, MLS, properties for sale/rent, agent bio, brokerage, "open house" |
| **Automotive** | inventory, VIN, test drive, dealership, service department, "new/used/certified" |

If no vertical detected, use generic `LocalBusiness` analysis path.

---

## Analysis Dimensions

### 1. GBP Signals (25%)

Primary category is the **single most important local pack factor** (Whitespark #1, score: 193). Incorrect primary category is the **#1 negative factor** (score: 176).

**Check for:**
- GBP embed or reference detectable on page (Maps iframe, place ID, reviews widget)
- Primary category appropriateness (infer from page content vs visible GBP data)
- Evidence of secondary categories (optimal: 4 additional per BrightLocal)
- GBP posts presence (no direct ranking impact per WebFX, but triggers Post Justifications)
- Photos/video evidence (45% more direction requests with photos, Agency Jet)
- Q&A content (deprecated Dec 2025, replaced by Ask Maps Gemini AI -- recommend recreating Q&A content as FAQ sections on website; GBP removed existing Q&A with no export available)
- Google Verified badge eligibility (replaced Guaranteed/Screened in Oct 2025)
- GBP link URL strategy: do NOT link to strongest website page (Sterling Sky Diversity Update -- risks suppressing organic rankings)
- Business hours visibility on page (businesses open at search time rank higher, factor #5)

**Scoring guide:**
- Full: GBP embed present, category signals align, posts active, photos present
- Partial: Some GBP signals present but incomplete
- Low: No visible GBP integration on website

### 2. Reviews & Reputation (20%)

Review velocity matters more than total count. The **18-day rule** (Sterling Sky): rankings cliff if no new reviews for 3 weeks.

**Check for:**
- Total Google review count visible on page or schema (magic threshold: 10, Sterling Sky)
- Star rating (31% of consumers only use 4.5+, 68% only use 4+, BrightLocal 2026)
- Review recency indicators (74% only care about reviews in last 3 months)
- `aggregateRating` in schema (ratingValue, reviewCount, bestRating)
- Third-party review presence (consumers use average of 6 review sites, BrightLocal 2026)
- Owner response patterns (88% would use business that responds, BrightLocal)
- Review gating detection: any pre-screening of satisfaction before directing to review platform is prohibited by Google (fake engagement policy) and FTC ($53,088/violation)

**Industry-specific:**
- Healthcare: HIPAA prohibits confirming/denying reviewer is a patient in responses
- Legal: attorney-client privilege considerations in review responses

**Scoring guide:**
- Full: 10+ reviews, 4.5+ stars, recent activity, owner responses, multi-platform presence
- Partial: Some reviews but gaps in recency, rating, or response rate
- Low: <10 reviews, no recent activity, no responses, single platform only

### 3. Local On-Page SEO (20%)

Dedicated service pages = **#1 local organic factor AND #2 AI visibility factor** (Whitespark 2026).

**Check for:**
- Title tag contains city/service keywords
- H1 tag with local intent (city + service)
- NAP (Name, Address, Phone) visible in page HTML (footer, contact section, header)
- Dedicated service pages (one page per core service)
- Location page quality for multi-location sites:
  - **>60-70% unique content** minimum (industry consensus, no Google-confirmed threshold)
  - **Swap test**: if you can swap the city name and content still makes sense, it's a doorway page (RicketyRoo method). HVAC company lost 80% rankings + 63% traffic after March 2024 Core Update for this pattern
  - Local photos, area-specific testimonials, local FAQs
- Embedded Google Map (geographic signal reinforcement, not direct ranking factor -- lazy-load to mitigate speed impact)
- Click-to-call button (`tel:` link) and contact form above the fold
- Internal linking architecture: hub-and-spoke, every critical page within 3 clicks of homepage
- 2-5 contextual internal links per 1,000 words with descriptive anchor text

**Multi-location specific:**
- Store locator with individual crawlable URLs (SSR/SSG preferred over CSR)
- Subdirectory structure: `domain.com/locations/city-name/` (subdirectories consolidate link equity better, Bruce Clay: 50%+ traffic lift)
- Each location page has unique LocalBusiness schema with `@id`

**Scoring guide:**
- Full: City in title + H1, NAP visible, dedicated service pages, no doorway patterns, good internal linking
- Partial: Some local signals but missing service pages or doorway page risk
- Low: Generic title/H1, NAP not visible, thin location pages

### 4. NAP Consistency & Citations (15%)

Citations declining for traditional pack rankings but **3 of top 5 AI visibility factors are citation-related** (Whitespark 2026). Google's July 2025 documentation update removed "directories" from prominence definition.

**Check for:**
- NAP extraction: compare Name, Address, Phone from:
  1. Visible page HTML (footer, contact page)
  2. LocalBusiness JSON-LD schema
  3. Any visible GBP data
  - Flag any discrepancies between these three sources
- Citation presence on Tier 1 directories (check via WebFetch or site: search patterns):
  - Google Business Profile signals on page
  - Yelp: `site:yelp.com "Business Name"`
  - BBB: `site:bbb.org "Business Name"`
  - Facebook business page references
- Apple Business Connect awareness (usage doubled to 27%, BrightLocal 2026 -- recommend claiming)
- Bing Places awareness (powers ChatGPT, Copilot, Alexa -- recommend claiming and optimizing)
- Industry-specific directory recommendations: load `references/local-schema-types.md` for per-vertical citation sources
- Data aggregator awareness: Data Axle, Foursquare, Neustar/TransUnion (recommend submission for downstream distribution)

**Scoring guide:**
- Full: Consistent NAP across page/schema, Tier 1 citations detected, industry directories present
- Partial: NAP present but inconsistencies, some citations missing
- Low: NAP discrepancies, no detectable citations, no schema address

### 5. Local Schema Markup (10%)

Schema is NOT a direct ranking factor (John Mueller confirmed). But enables rich results (43% CTR increase, Webstix case study) and helps AI systems parse business information.

**Check for:**
- LocalBusiness schema presence (extract JSON-LD blocks)
- Required properties: `name`, `address` with PostalAddress sub-properties
- Recommended properties: `geo` (minimum 5 decimal places, Confirmed), `openingHoursSpecification`, `telephone`, `url`, `priceRange` (<100 chars), `image`, `aggregateRating`
- **Correct subtype for industry** -- load `references/local-schema-types.md`:
  - Restaurant using `Restaurant` not generic `LocalBusiness`
  - Legal using `LegalService` not deprecated `Attorney`
  - Auto dealer using `AutoDealer` not deprecated `VehicleListing`
  - Healthcare using `MedicalClinic`/`Hospital`/`Dentist` not generic `MedicalBusiness`
- SAB-specific: `areaServed` with named cities (recommended, not in Google's official list but Schema.org supported)
- Multi-location: each location page has own LocalBusiness with unique `@id`, linked via `branchOf` to Organization on homepage
- Industry-specific schema patterns (per `references/local-schema-types.md`):
  - Restaurant: Menu + MenuSection + MenuItem + ReserveAction
  - Healthcare: Physician (Person) + MedicalSpecialty + sameAs to NPI
  - Legal: LegalService + Person + Service (practice areas)
  - Home Services: Subtype + areaServed + Service
  - Real Estate: RealEstateAgent + Person + RealEstateListing
  - Automotive: AutoDealer + Car + Offer (separate dept schemas)

**Scoring guide:**
- Full: Correct subtype, all recommended properties, industry-specific patterns, valid JSON-LD
- Partial: LocalBusiness present but generic type or missing recommended properties
- Low: No local schema, or schema with errors/placeholder content

### 6. Local Link & Authority Signals (10%)

Links declining for local pack but remain **~26% of local organic ranking** (Whitespark 2026, #2 factor group). "Best of" list placements = **#1 AI visibility citation factor**.

**Check for:**
- Local backlink indicators detectable from page:
  - Chamber of Commerce mentions or links (high Trust Flow, ~80% more consumer visits, GlueUp)
  - BBB accreditation/badge (Google uses BBB for business verification)
  - Local news/press mentions
  - Community involvement signals (sponsorships, local events, partnerships)
- "Best of" list presence (top AI visibility factor per Whitespark 2026)
- Digital PR signals: 66.2% of PR practitioners now track AI citations as KPI (BuzzStream 2026)
- Brand mentions correlate **3x more strongly** with AI visibility than traditional backlinks (Ahrefs: 0.664 vs 0.218 correlation)
- Link velocity benchmark: 5-10 quality local links/month for small businesses (consensus)

**Scoring guide:**
- Full: Local authority signals visible (chamber, BBB, press), community involvement evident
- Partial: Some authority signals but limited local link indicators
- Low: No detectable local authority signals

---

## AI Search Impact on Local

**Do not duplicate seo-geo analysis.** Provide local-specific AI context and recommend `/seo geo <url>` for full analysis.

Key local AI facts:
- AI Overviews appear on up to 68% of local searches (Whitespark Q2 2025)
- ChatGPT converts at 15.9% vs Google organic at 1.76% (Seer Interactive)
- 3 of top 5 AI visibility factors are citation-related (Whitespark 2026)
- ChatGPT does NOT access GBP directly -- sources from Bing index, Yelp, TripAdvisor, BBB, Reddit
- Bing Places is critical: powers ChatGPT, Copilot, Alexa
- AI-powered local packs (mobile US) show only 1-2 businesses, 32% fewer shown (Sterling Sky)

**Recommendation**: Run `/seo geo <url>` for comprehensive AI search visibility analysis including citability scoring, llms.txt check, and brand mention audit.

---

## Reference Files

Load on-demand as needed:
- `references/local-seo-signals.md`: Ranking factors, review benchmarks, citation tiers, GBP feature status, algorithm updates
- `references/local-schema-types.md`: LocalBusiness subtypes by industry, schema patterns, citation sources per vertical

---

## Output

Generate `LOCAL-SEO-ANALYSIS-{domain}.md` with:

1. **Local SEO Score: XX/100** with dimension breakdown table
2. **Business type**: Brick-and-mortar / SAB / Hybrid
3. **Industry vertical detected** + industry-specific findings
4. **GBP optimization checklist** (detected signals vs missing)
5. **Review health snapshot** (rating, count, velocity indicators, response patterns)
6. **NAP consistency audit** (page vs schema discrepancies, cross-source comparison)
7. **Citation presence check** (Tier 1 directory status)
8. **Local schema status** (present/missing/malformed + ready-to-use fix)
9. **Location page quality** (if multi-location: unique content %, doorway risk, store locator)
10. **Top 10 prioritized actions** (Critical > High > Medium > Low)
11. **Limitations disclaimer**: What this analysis could NOT assess (geo-grid ranking, Domain Authority, comprehensive backlinks, GBP Insights data, real-time local pack position) and which paid tools can fill those gaps

---

## Quick Wins

1. Claim and optimize Apple Business Connect (usage doubled to 27%)
2. Claim and optimize Bing Places (powers ChatGPT, Copilot, Alexa)
3. Fix any NAP discrepancies between page, schema, and GBP
4. Add LocalBusiness schema with correct industry subtype
5. Add `geo` coordinates with 5+ decimal precision
6. Ensure phone number uses `tel:` link for click-to-call
7. Add city + service keyword to title tag and H1

## Medium Effort

1. Create dedicated page for each core service (Whitespark: #1 local organic factor)
2. Build review generation strategy maintaining 18-day minimum cadence
3. Submit to three data aggregators (Data Axle, Foursquare, Neustar/TransUnion) for downstream distribution
4. Claim industry-specific directory listings (per vertical recommendations)
5. Add industry-specific schema patterns (Menu for restaurants, Physician for healthcare, etc.)
6. Implement hub-and-spoke internal linking for service/location pages

## High Impact

1. Build local digital PR strategy targeting "best of" lists (#1 AI visibility factor)
2. Develop unique, non-swappable content for each location page (>60% unique)
3. Establish presence on platforms ChatGPT sources from (Yelp, TripAdvisor, BBB, Reddit)
4. Pursue Chamber of Commerce and BBB membership (authority + verification signals)
5. Create community involvement content (sponsorships, local events, partnerships)

---

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, use `local_business_data` for live GBP data extraction, `google_local_pack_serp` for real-time local pack positions, and `business_listings` for automated citation auditing across directories.

---

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable (DNS failure, connection refused) | Report the error clearly. Do not guess site content. Suggest the user verify the URL and try again. |
| No local signals detected on page | Report that no local business indicators were found. Suggest the user confirm this is a local business and provide the GBP listing URL if available. |
| NAP not found in page HTML | Check schema and meta tags. If still absent, flag as Critical issue. Recommend adding visible NAP to footer and contact page. |
| Industry vertical unclear | Present the top two detected verticals with supporting signals. Ask the user to confirm before applying industry-specific recommendations. |
| Multi-location with 50+ location pages | Apply the quality gates from seo orchestrator: WARNING at 30+ pages (enforce 60%+ unique), HARD STOP at 50+ pages (require user justification before continuing). |

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Business Type & Vertical detectados correctamente

- [ ] Output identifica explicitamente Brick-and-Mortar / SAB / Hybrid com evidence do site
- [ ] Vertical (Restaurant / Healthcare / Legal / Home Services / Real Estate / Automotive / Generic) declarado no início da análise
- [ ] Checks SAB-específicas (sem mapa embed, sem NAP street-level) aplicadas ou explicitamente saltadas com razão
- [ ] Categoria GBP primária avaliada face ao vertical detectado (e não genérica)

❌ NOT delivery-ready: "O negócio parece ser um SAB ou talvez brick-and-mortar, dependendo da área de serviço."
✅ Delivery-ready: "**Cuidai — SAB (Home Services / Healthcare híbrido)**. Sem endereço físico visível no footer; detectado 'Servimos Lisboa, Cascais e Sintra' + 'A equipa desloca-se ao domicílio'. Checks NAP street-level e Maps embed não aplicáveis."

---

### Gate 2 — GBP Signals avaliados com dados concretos (32% de peso local pack)

- [ ] Presença/ausência de GBP embed ou place ID no site documentada com URL ou selector
- [ ] Primary category alignment avaliado (factor #1 Whitespark 2026, score 193) com sugestão de categoria correcta
- [ ] GBP link strategy verificada: output não recomenda linkar para a página mais forte do site (Sterling Sky Diversity Update)
- [ ] Q&A deprecation (Dez 2025) mencionada se relevante — recomendação de migrar para FAQ page
- [ ] Business hours visibilidade no site verificada (factor #5, businesses open at search time rank higher)

❌ NOT delivery-ready: "Recomendamos optimizar o Google Business Profile com fotos e horários."
✅ Delivery-ready: "**Lisbon Dog Care** — GBP embed ausente em lisbon-dog-care.pt/contacto. Primary category detectada como 'Pet Store' (via schema), mas sinais de página apontam 'Dog Day Care Center' (factor #1, score 193 Whitespark). GBP URL aponta para homepage — risco Sterling Sky Diversity Update; redirigir para /servicos. Horários não visíveis em nenhuma página."

---

### Gate 3 — Reviews & Reputation com thresholds numéricos aplicados

- [ ] Contagem de reviews Google reportada (threshold mágico: 10, Sterling Sky) ou indicada como não detectável
- [ ] Star rating avaliado contra benchmarks: 4.5+ (31% consumers), 4.0+ (68% consumers) — BrightLocal 2026
- [ ] 18-day rule verificada: última review datada ou flag de impossibilidade de verificar via WebFetch
- [ ] `aggregateRating` schema (ratingValue, reviewCount, bestRating) presente/ausente confirmado
- [ ] Review gating detection: qualquer pré-triagem de satisfação flagged como violação FTC ($53,088/violação) + Google policy

❌ NOT delivery-ready: "O negócio tem boas reviews e deve continuar a pedir feedback aos clientes."
✅ Delivery-ready: "**SAQUEI** — 23 reviews Google (✅ acima de threshold 10), média 4.2★ (⚠️ abaixo de 4.5★ — 31% consumers excluem negócios abaixo deste valor). Última review detectada: 47 dias atrás — ❌ viola 18-day rule (cliff de rankings após 21 dias, Sterling Sky). `aggregateRating` ausente no schema. Nenhum review gating detectado."

---

### Gate 4 — Local On-Page SEO com páginas de serviço avaliadas individualmente

- [ ] Dedicated service pages identificadas (factor #1 local organic E #2 AI visibility, Whitespark 2026)
- [ ] NAP consistency verificada: nome, morada e telefone idênticos no site, footer e schema — ou SAB flag aplicado
- [ ] Title tags e H1s de páginas de localização/serviço incluem geo-modifier verificável
- [ ] Internal linking entre páginas de localização e homepage avaliado
- [ ] Para multi-location: cada location page avaliada separadamente com dados próprios

❌ NOT delivery-ready: "As páginas de serviço devem incluir palavras-chave locais e informação de contacto."
✅ Delivery-ready: "**Tributario.AI** — 0 dedicated service pages detectadas (apenas /servicos genérica sem geo-targeting). Title tag homepage: 'Tributario.AI | Software Fiscal' — sem geo-modifier. NAP footer: 'Lisboa' apenas, sem morada completa nem telefone. Recomendar criar /software-fiscal-lisboa e /consultoria-fiscal-porto como prioridade #1."

---

### Gate 5 — Schema Markup validado com tipo correcto para vertical

- [ ] Tipo de schema correcto para vertical detectado (ex: `MedicalBusiness` para healthcare, `Attorney` para legal, `Restaurant` com `Menu` para restauração)
- [ ] Campos obrigatórios presentes: `name`, `address` (ou `areaServed` para SAB), `telephone`, `url`, `openingHours`
- [ ] `aggregateRating` nested correctamente ou ausência flagged com impacto estimado
- [ ] Erros críticos de schema (endereço em SAB, tipo genérico `LocalBusiness` quando vertical específico disponível) identificados
- [ ] Local schema types referenciados de `references/local-schema-types.md` quando aplicável

❌ NOT delivery-ready: "O schema está presente mas pode ser melhorado com mais detalhes."
✅ Delivery-ready: "**Atrium** — Schema tipo `Organization` detectado (❌ incorreto para brick-and-mortar com localização física). Deve ser `LocalBusiness` > `ProfessionalService`. Ausentes: `openingHours`, `geo`, `aggregateRating`. `address.streetAddress` presente mas `postalCode` em falta — quebra validação Google Rich Results Test."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets de placeholder

- [ ] Nome do cliente aparece no título da análise e em cada secção principal
- [ ] URLs concretas do site analisado citadas (não "a homepage" ou "a página de contacto")
- [ ] Todos os scores/ratings são números reais detectados ou "não detectável via WebFetch — verificar manualmente"
- [ ] Zero ocorrências de `[CLIENT NAME]`, `[INSERT URL]`, `[YOUR BUSINESS]`, `<placeholder>` no output final
- [ ] Datas de verificação incluídas quando relevante (ex: "última review: 47 dias atrás", "GBP embed verificado em março 2026")

❌ NOT delivery-ready: "O [NOME DO NEGÓCIO] deve optimizar o seu [TIPO DE PÁGINA] para [CIDADE ALVO]."
✅ Delivery-ready: "**Vivenda** (vivenda.pt) — análise Local SEO concluída março 2026. GBP embed detectado em /contacto (place_id: ChIJ...). 18 reviews Google, 4.7★, última há 6 dias ✅."

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Local SEO Analysis — Lisbon Dog Care (lisbon-dog-care.pt)
**Verificado:** Março 2026 | **Business Type:** Brick-and-Mortar + SAB Hybrid | **Vertical:** Pet Care / Home Services

---

## Detecção de Tipo e Vertical
- **Tipo:** Hybrid — endereço físico em /contacto ("Rua Actor Vale 8, 1900-012 Lisboa") + linguagem SAB ("Recolha e entrega ao domicílio em Lisboa e Almada")
- **Vertical:** Pet Care (Dog Daycare / Grooming) — detectado via /servicos: "Dog daycare", "grooming", "dog walking"
- **Schema actual:** `Organization` ❌ — deve ser `AnimalShelter` > `LocalBusiness` com `PetStore` como tipo secundário

---

## 1. GBP Signals — Score: Parcial ⚠️

| Check | Status | Detalhe |
|-------|--------|---------|
| GBP embed no site | ✅ Presente | Maps iframe em /contacto, place_id detectado |
| Primary category | ⚠️ Risco | Schema aponta "Pet Store" — página sugere "Dog Day Care Center" (factor #1, score 193 Whitespark 2026) |
| Secondary categories | ❌ Ausente | Nenhuma evidência de categorias secundárias (óptimo: 4 adicionais) |
| GBP posts | ❌ Sem evidência | Nenhum widget ou feed de posts detectado no site |
| Photos evidence | ✅ Parcial | Galeria em /galeria com 12 imagens (recomendado: 100+, Agency Jet) |
| Q&A (deprecado Dez 2025) | ⚠️ Acção | Q&A GBP removida — criar FAQ page em /faq com conteúdo equivalente |
| GBP link strategy | ❌ Risco | Link GBP aponta para homepage — Sterling Sky Diversity Update: redirigir para /servicos/dog-daycare |
| Business hours no site | ❌ Ausente | Horário não visível em nenhuma página indexável |

**Prioridade imediata:** Corrigir primary category para "Dog Day Care Center" no GBP e adicionar horários ao footer.

---

## 2. Reviews & Reputation — Score: Baixo ❌

- **Total reviews Google:** 8 ❌ — abaixo do threshold de 10 (Sterling Sky magic number)
- **Star rating:** 4.3★ ⚠️ — abaixo de 4.5★ (31% dos consumidores excluem negócios abaixo deste valor, BrightLocal 2026)
- **Última review:** 34 dias atrás ❌ — viola 18-day rule (cliff de rankings após 21 dias sem nova review, Sterling Sky)
- **`aggregateRating` schema:** ❌ Ausente — perda de rich snippet e sinal de confiança
- **Owner responses:** 2 de 8 reviews respondidas (25%) ⚠️ — benchmark: 88% dos consumidores preferem negócios que respondem
- **Plataformas adicionais:** Apenas Google detectado ⚠️ — consumidores usam média de 6 plataformas (BrightLocal 2026)
- **Review gating:** ❌ Não detectado (conforme com Google policy e FTC)

**Acções urgentes:**
1. Campanha activa de pedido de reviews — meta: 10+ em 3 semanas
2. Responder a todas as reviews existentes esta semana
3. Criar perfil em Zomato PT, Facebook e TripAdvisor
4. Adicionar `aggregateRating` ao schema (ratingValue: 4.3, reviewCount: 8, bestRating: 5)

---

## 3. Local On-Page SEO — Score: Baixo ❌

- **Dedicated service pages:** ❌ Apenas /servicos genérica — sem páginas individuais por serviço
  - Criar: /servicos/dog-daycare-lisboa, /servicos/grooming-lisboa, /servicos/dog-walking-lisboa
  - Factor #1 local organic + #2 AI visibility (Whitespark 2026) — prioridade máxima
- **Title tags:**
  - Homepage: "Lisbon Dog Care | Lisboa" — sem keyword primária no início ⚠️
  - /servicos: "Os Nossos Serviços" ❌ — sem geo-modifier
- **H1s:** Homepage H1: "Bem-vindos" ❌ — nenhuma keyword local ou de serviço
- **NAP footer:** ✅ Nome, morada e telefone consistentes em todas as páginas verificadas
- **SAB coverage:** Menção a Almada em /contacto apenas — sem página de área de serviço dedicada

---

## 4. Schema Markup — Score: Crítico ❌

**Tipo actual:** `Organization` — **Tipo correcto:** `LocalBusiness` > `PetStore` + `AnimalShelter`

**Campos em falta:**
```json
{
  "@type": "LocalBusiness",
  "name": "Lisbon Dog Care",
  "address": {
    "streetAddress": "Rua Actor Vale 8",
    "addressLocality": "Lisboa",
    "postalCode": "1900-012",
    "addressCountry": "PT"
  },
  "areaServed": ["Lisboa", "Almada"],
  "telephone": "+351-XXX-XXX-XXX",
  "openingHours": "Mo-Fr 07:00-20:00, Sa 08:00-18:00",
  "aggregateRating": {
    "ratingValue": "4.3",
    "reviewCount": "8",
    "bestRating": "5"
  }
}
```
**Acção:** Implementar schema completo via `<script type="application/ld+json">` no `<head>` de todas as páginas.

---

## Plano de Acção Priorizado

| Prioridade | Acção | Impacto Estimado | Prazo |
|-----------|-------|-----------------|-------|
| 🔴 P1 | Corrigir primary GBP category → "Dog Day Care Center" | Factor #1 local pack | Esta semana |
| 🔴 P1 | Campanha reviews: 10+ em 21 dias | 18-day rule + threshold | 3 semanas |
| 🔴 P1 | Implementar schema `LocalBusiness` completo | Rich snippets + trust | Esta semana |
| 🟡 P2 | Criar 3 dedicated service pages com geo-modifier | Factor #1 local organic | Mês 1 |
| 🟡 P2 | Adicionar horários ao footer e schema `openingHours` | Factor #5 local pack | Esta semana |
| 🟢 P3 | Criar /faq para substituir Q&A GBP (deprecado Dez 2025) | AI visibility | Mês 2 |
| 🟢 P3 | Expandir galeria para 100+ fotos no GBP | +45% direction requests | Mês 2 |
```

---

## Output anti-patterns

- **Análise genérica sem business type declarado** — output não distingue SAB de brick-and-mortar, aplica checks de NAP e mapa a um negócio móvel
- **Thresholds sem fonte** — mencionar "ter mais reviews é melhor" sem citar o threshold de 10, o 18-day rule ou os benchmarks de 4.0/4.5★ da BrightLocal 2026
- **GBP link strategy ignorada** — recomendar linkar GBP para a página mais forte do site sem mencionar o risco Sterling Sky Diversity Update
- **Q&A GBP recomendada como activa** — ignorar a deprecação de Dezembro 2025 e aconselhar optimizar Q&A que já não existe
- **Schema tipo genérico sem vertical** — usar `LocalBusiness` para um restaurante ou médico quando tipos específicos (`Restaurant`, `MedicalBusiness`) estão disponíveis
- **Review gating não verificado** — omitir verificação de pré-triagem de satisfação quando há formulários de feedback no site (risco FTC $53,088/violação)
- **Percentagens locais sem contexto de proximidade** — citar 32% de peso GBP sem notar que proximidade domina 55.2% da variância de ranking (Search Atlas 2026), criando expectativas erradas sobre o que se pode controlar
- **AI visibility omitida** — análise Local SEO em 2026 que não menciona o canal ChatGPT/AI (45% usage, 15.9% conversion rate vs 1.76% Google organic) perde contexto estratégico crítico
- **Placeholders no output final** — entregar com `[NOME DO NEGÓCIO]`, `[INSERIR URL]` ou `<cidade>` visíveis ao cliente
