---
name: seo-plan
description: >
  Strategic SEO planning for new or existing websites. Industry-specific
  templates, competitive analysis, content strategy, and implementation
  roadmap. Use when user says "SEO plan", "SEO strategy", "content strategy",
  "site architecture", or "SEO roadmap".
user-invokable: true
argument-hint: "[business-type]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# Strategic SEO Planning

## Process

### 1. Discovery
- Business type, target audience, competitors, goals
- Current site assessment (if exists)
- Budget and timeline constraints
- Key performance indicators (KPIs)

### 2. Competitive Analysis
- Identify top 5 competitors
- Analyze their content strategy, schema usage, technical setup
- Identify keyword gaps and content opportunities
- Assess their E-E-A-T signals
- Estimate their domain authority

### 3. Architecture Design
- Load industry template from `assets/` directory
- Design URL hierarchy and content pillars
- Plan internal linking strategy
- Sitemap structure with quality gates applied
- Information architecture for user journeys

### 4. Content Strategy
- Content gaps vs competitors
- Page types and estimated counts
- Blog/resource topics and publishing cadence
- E-E-A-T building plan (author bios, credentials, experience signals)
- Content calendar with priorities

### 5. Technical Foundation
- Hosting and performance requirements
- Schema markup plan per page type
- Core Web Vitals baseline targets
- AI search readiness requirements
- Mobile-first considerations

### 6. Implementation Roadmap (4 phases)

#### Phase 1: Foundation (weeks 1-4)
- Technical setup and infrastructure
- Core pages (home, about, contact, main services)
- Essential schema implementation
- Analytics and tracking setup

#### Phase 2: Expansion (weeks 5-12)
- Content creation for primary pages
- Blog launch with initial posts
- Internal linking structure
- Local SEO setup (if applicable)

#### Phase 3: Scale (weeks 13-24)
- Advanced content development
- Link building and outreach
- GEO optimization
- Performance optimization

#### Phase 4: Authority (months 7-12)
- Thought leadership content
- PR and media mentions
- Advanced schema implementation
- Continuous optimization

## Industry Templates

Load from `assets/` directory:
- `saas.md`: SaaS/software companies
- `local-service.md`: Local service businesses
- `ecommerce.md`: E-commerce stores
- `publisher.md`: Content publishers/media
- `agency.md`: Agencies and consultancies
- `generic.md`: General business template

## Output

### Deliverables
- `SEO-STRATEGY.md`: Complete strategic plan
- `COMPETITOR-ANALYSIS.md`: Competitive insights
- `CONTENT-CALENDAR.md`: Content roadmap
- `IMPLEMENTATION-ROADMAP.md`: Phased action plan
- `SITE-STRUCTURE.md`: URL hierarchy and architecture

### KPI Targets
| Metric | Baseline | 3 Month | 6 Month | 12 Month |
|--------|----------|---------|---------|----------|
| Organic Traffic | ... | ... | ... | ... |
| Keyword Rankings | ... | ... | ... | ... |
| Domain Authority | ... | ... | ... | ... |
| Indexed Pages | ... | ... | ... | ... |
| Core Web Vitals | ... | ... | ... | ... |

### Success Criteria
- Clear, measurable goals per phase
- Resource requirements defined
- Dependencies identified
- Risk mitigation strategies

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, use `dataforseo_labs_google_competitors_domain` and `dataforseo_labs_google_domain_intersection` for real competitive intelligence, `dataforseo_labs_bulk_traffic_estimation` for traffic estimates, `kw_data_google_ads_search_volume` and `dataforseo_labs_bulk_keyword_difficulty` for keyword research, and `business_data_business_listings_search` for local business data.

## Error Handling

| Scenario | Action |
|----------|--------|
| Unrecognized business type | Fall back to `generic.md` template. Inform user that no industry-specific template was found and proceed with the general business template. |
| No website URL provided | Proceed with new-site planning mode. Skip current site assessment and competitive gap analysis that require a live URL. |
| Industry template not found | Check `assets/` directory for available templates. If the requested template file is missing, use `generic.md` and note the missing template in output. |

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Competitive Analysis tem dados reais, não placeholders

- [ ] 5 concorrentes identificados com domínios reais (ex: `concorrente.pt`, não `[competitor1]`)
- [ ] Domain Authority estimado para cada um (ex: "DA 34 estimado via Moz/Ahrefs")
- [ ] Pelo menos 3 keyword gaps concretos com volumes (ex: "seguro de saúde familiar — 2.400/mês")
- [ ] E-E-A-T signals dos concorrentes descritos (ex: "usam author bios com CRM nº, 4 case studies publicados")
- ❌ NOT delivery-ready: "Competitor A has strong content strategy and good domain authority"
- ✅ Delivery-ready: "DrConsultas.pt — DA 41, 380 páginas indexadas, autor certificado em cada artigo clínico, keyword dominante 'médico online' (8.100/mês)"

### Gate 2 — Arquitectura URL e Content Pillars são específicos do negócio

- [ ] URL hierarchy com caminhos reais, não genéricos (ex: `/seguros/saude/familiar/` não `/category/subcategory/`)
- [ ] Content pillars mapeados a intenção de pesquisa (informacional / transacional / navegacional)
- [ ] Número estimado de páginas por pilar definido (ex: "Pilar Saúde Familiar: 12 páginas core + 24 blog posts/ano")
- [ ] Internal linking strategy descreve pelo menos 3 hub-and-spoke clusters concretos
- ❌ NOT delivery-ready: "Design URL hierarchy based on content pillars aligned with user journey"
- ✅ Delivery-ready: "Cluster 'Consultas Online': hub `/consultas-online/` → spokes `/consultas-online/clinico-geral/`, `/consultas-online/pediatria/`, `/consultas-online/psicologia/` — 9 páginas fase 1"

### Gate 3 — KPI Targets têm números, não reticências

- [ ] Baseline preenchido com dados reais ou estimativa fundamentada (ex: "0 tráfego orgânico — site novo")
- [ ] Targets 3/6/12 meses com valores numéricos específicos e metodologia (ex: "3 meses: 400 sessões/mês orgânicas — estimativa conservadora mercado PT")
- [ ] Core Web Vitals target com valores concretos (LCP < 2.5s, CLS < 0.1, INP < 200ms)
- [ ] Indexed Pages target por fase definido numericamente
- ❌ NOT delivery-ready: KPI table com `...` em todas as células
- ✅ Delivery-ready: "Organic Traffic — Baseline: 0 (site novo, Jan 2025) → 3m: 250 sessões → 6m: 900 sessões → 12m: 3.200 sessões"

### Gate 4 — Content Calendar tem datas e responsáveis reais

- [ ] Calendário com datas específicas (semana ou mês concreto, ex: "Fev W2 2025")
- [ ] Tipo de conteúdo + keyword-alvo + intenção de pesquisa por entrada
- [ ] Cadência de publicação definida (ex: "2 posts/mês em fase 1, 4 posts/mês em fase 2")
- [ ] Estimativa de esforço de produção por tipo de página (ex: "landing service: 3h redação + 1h SEO on-page")
- ❌ NOT delivery-ready: "Publish blog posts regularly about topics relevant to your audience"
- ✅ Delivery-ready: "Mar W1 — 'Como funciona uma consulta online de pediatria' (intenção: informacional, KW: consulta pediatria online 720/mês, 2.500 palavras, autor: Dra. Sofia Mendes)"

### Gate 5 — Technical Foundation e Schema Plan são accionáveis

- [ ] Schema markup especificado por tipo de página (ex: `MedicalOrganization` na homepage, `FAQPage` nos artigos, `Physician` nas páginas de médicos)
- [ ] Hosting/performance requirement com provider ou spec concreta (ex: "VPS NVMe mínimo, PHP 8.2+, CDN Cloudflare free tier suficiente")
- [ ] AI search readiness inclui pelo menos 3 acções específicas (ex: "Adicionar FAQ estruturado em cada serviço, definir entidade da marca no schema, criar página /sobre com NAP+fundadores")
- [ ] Core Web Vitals plano de acção, não só targets
- ❌ NOT delivery-ready: "Implement appropriate schema markup and ensure good Core Web Vitals"
- ✅ Delivery-ready: "Página `/consultas-online/`: `MedicalOrganization` + `Service` + `FAQPage` (5 Qs sobre funcionamento); LCP: optimizar hero image para WebP < 80kb; plugin WP Rocket config incluída no roadmap"

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets

- [ ] Nome do cliente aparece no título de cada deliverable (ex: `SEO-STRATEGY-Cuidai.md`, não `SEO-STRATEGY-[CLIENT].md`)
- [ ] Zero ocorrências de `[business-type]`, `[competitor]`, `[keyword]`, `[date]` ou variantes
- [ ] Indústria, localização e público-alvo específicos usados em todo o documento
- [ ] DataForSEO data citada se disponível, ou fonte alternativa explicitada se não disponível
- ❌ NOT delivery-ready: "Target audience: [describe target audience here]"
- ✅ Delivery-ready: "Público-alvo: famílias urbanas PT, 28-45 anos, com filhos menores de 12, utilizadores de planos de saúde privados (Multicare/AdvanceCare)"

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# SEO Strategy — Cuidai (cuidai.pt)
*Gerado: Janeiro 2025 | Indústria: Telemedicina / Saúde Digital Portugal*

---

## Competitive Landscape

| Concorrente | Domínio | DA Est. | Páginas Indexadas | Keyword Dominante |
|---|---|---|---|---|
| DrConsultas | drconsultas.pt | 41 | 380 | médico online (8.1K/mês) |
| Médis Online | medis.pt/online | 58 | 1.200 | consulta médica online (5.4K/mês) |
| HelloDoctor | hellodoctor.pt | 29 | 145 | teleconsulta (2.9K/mês) |
| Clínica Lusíadas | lusiadas.pt | 67 | 4.800 | consulta online (12K/mês) |
| MediLine | mediline.pt | 22 | 89 | médico a distância (880/mês) |

**Top 3 Keyword Gaps para Cuidai:**
1. "consulta pediátrica online" — 1.600/mês, KD 28 (baixo) — nenhum concorrente tem página dedicada
2. "teleconsulta saúde mental criança" — 720/mês, KD 19 — oportunidade E-E-A-T alta
3. "médico online sem espera" — 2.400/mês, KD 35 — intenção transacional forte

---

## Arquitectura URL — Fase 1

```
cuidai.pt/
├── /consultas-online/                    (hub principal)
│   ├── /consultas-online/clinico-geral/
│   ├── /consultas-online/pediatria/      ← prioridade gap #1
│   ├── /consultas-online/psicologia/     ← prioridade gap #2
│   └── /consultas-online/ginecologia/
├── /como-funciona/
├── /medicos/                             (hub E-E-A-T)
│   └── /medicos/[nome-dr]/              (perfil individual com schema Physician)
├── /blog/saude-familia/                  (hub conteúdo informacional)
└── /precos/
```

**Content Pillars:**
- Pilar 1 — Consultas Online: 8 páginas core (transacional) + 18 blog posts/ano
- Pilar 2 — Saúde Infantil: 5 páginas core + 24 blog posts/ano (gap primário)
- Pilar 3 — Saúde Mental: 4 páginas core + 12 blog posts/ano

---

## KPI Targets

| Métrica | Baseline (Jan 2025) | 3 Meses (Abr 2025) | 6 Meses (Jul 2025) | 12 Meses (Jan 2026) |
|---|---|---|---|---|
| Organic Traffic | 340 sessões/mês | 900 sessões/mês | 2.800 sessões/mês | 8.500 sessões/mês |
| Keywords Top 10 | 12 KWs | 45 KWs | 130 KWs | 380 KWs |
| Domain Authority | DA 18 | DA 22 | DA 27 | DA 35 |
| Páginas Indexadas | 34 | 65 | 120 | 280 |
| LCP (homepage) | 4.1s ❌ | < 2.5s ✅ | < 2.0s ✅ | < 1.8s ✅ |

*Metodologia: crescimento conservador mercado PT telemedicina; benchmark HelloDoctor (DA 29, 2 anos) como proxy realista.*

---

## Content Calendar — Q1 2025

| Data | Título | Keyword Alvo | Vol/mês | KD | Tipo | Responsável |
|---|---|---|---|---|---|---|
| Jan W3 | "Como funciona uma teleconsulta pediátrica" | teleconsulta pediátrica | 720 | 19 | Blog 2.000w | Redação Cuidai |
| Jan W4 | Landing: Consultas Pediatria Online | consulta pediátrica online | 1.600 | 28 | Service Page | SEO + Dev |
| Fev W2 | "Saúde mental infantil: quando pedir ajuda" | saúde mental criança | 1.100 | 24 | Blog 2.500w | Dra. Ana Costa (autora) |
| Fev W4 | Landing: Psicologia Infantil Online | psicólogo infantil online | 880 | 31 | Service Page | SEO + Dev |
| Mar W2 | "Febre em bebés: guia completo" | febre bebé o que fazer | 4.400 | 22 | Blog 3.000w | Dr. Rui Tavares (autora) |
| Mar W4 | Perfis médicos — 5 pediatras | [nome-dr] + pediatra online | — | — | Physician Pages | Dev + Médicos |

*Cadência: 2 service pages + 2 blog posts/mês em Q1; aumenta para 4 blog posts/mês a partir de Q2.*

---

## Technical Foundation

**Hosting:** Migração para VPS NVMe (Hetzner CX21 ou equiv.) + Cloudflare Free — estimativa LCP -1.8s.

**Schema por página:**
- Homepage: `MedicalOrganization` + `WebSite` (SearchAction)
- Páginas de Serviço: `MedicalSpecialty` + `Service` + `FAQPage` (5 Qs cada)
- Perfis Médicos: `Physician` + `Person` + `MedicalOrganization` (employer)
- Blog Posts: `Article` + `MedicalWebPage` + `BreadcrumbList` + `Author` com credenciais
- Página Preços: `Offer` + `FAQPage`

**AI Search Readiness (GEO):**
1. Definir entidade Cuidai no schema (founding date, founders, NIF, service area Lisboa+Porto)
2. FAQ estruturado em cada serviço (mínimo 5 perguntas conversacionais)
3. Criar `/sobre/` com NAP completo, história da empresa, fotos equipa fundadora
4. Citações NAP consistentes: Google Business Profile + Sapo Saúde + Páginas Amarelas

---

## Implementation Roadmap

### Fase 1 — Foundation (Jan–Fev 2025)
- [ ] Migração hosting + Cloudflare (semana 1)
- [ ] Core Web Vitals: optimizar imagens homepage para WebP, lazy load (semana 1-2)
- [ ] Schema MedicalOrganization homepage + 4 service pages existentes (semana 2)
- [ ] GA4 + GSC verificados, Search Console sitemap submetido (semana 1)
- [ ] Páginas core: `/sobre/`, `/como-funciona/`, `/precos/` reescritas com E-E-A-T (semana 3-4)

### Fase 2 — Expansion (Mar–Jun 2025)
- [ ] 2 novas service pages/mês (pediatria, psicologia, ginecologia, clínico geral)
- [ ] Blog: 4 posts/mês a partir de Abril, todos com autor médico credenciado
- [ ] 5 perfis médicos com schema Physician completo
- [ ] Google Business Profile optimizado (Lisboa + Porto)

### Fase 3 — Scale (Jul–Dez 2025)
- [ ] Link building: 2 artigos guest/mês em media saúde PT (Saúde Magazine, Notícias Magazine Saúde)
- [ ] GEO: FAQ conversacional em 100% das páginas de serviço
- [ ] Schema avançado: HowTo em posts de sintomas, MedicalCondition nas páginas de especialidade

### Fase 4 — Authority (2026)
- [ ] Thought leadership: relatório anual "Saúde Digital em Portugal"
- [ ] PR: mencionar Cuidai em 3 artigos Público/Expresso sobre telemedicina
- [ ] Schema: adicionar `Review` agregado nas páginas de especialidade (mínimo 50 reviews/página)
```

---

## Output anti-patterns

- KPI table entregue com `...` em todas as células — força o cliente a fazer o trabalho estratégico que pagou
- URL hierarchy com paths genéricos como `/services/service-1/` em vez de slugs reais baseados em keywords-alvo
- Competitive analysis com "Competitor A, B, C" sem domínios, DA ou dados de tráfego verificáveis
- Content calendar sem datas concretas, apenas "Month 1, Month 2" — inutilizável para planeamento real
- Schema plan que lista "implement appropriate schema" sem especificar tipo por página (MedicalOrganization ≠ LocalBusiness ≠ FAQPage)
- Roadmap de 4 fases sem owners ou estimativas de esforço — ninguém sabe quem faz o quê nem quanto demora
- Deliverables com nomes genéricos `SEO-STRATEGY.md` sem nome do cliente (sinal de output de template, não trabalho custom)
- E-E-A-T plan que diz "create author bios" sem definir que credenciais, formato ou onde publicar
- DataForSEO disponível mas não usado — os dados reais foram ignorados em favor de estimativas vagas
- KD e volumes de keyword omitidos no content calendar — impossível priorizar sem estes dados
