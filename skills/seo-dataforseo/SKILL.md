---
name: seo-dataforseo
description: >
  Live SEO data via DataForSEO MCP server. SERP analysis (Google, Bing, Yahoo,
  YouTube), keyword research (volume, difficulty, intent, trends), backlink
  profiles, on-page analysis (Lighthouse, content parsing), competitor analysis,
  content analysis, business listings, AI visibility (ChatGPT scraper, LLM
  mention tracking), and domain analytics. Requires DataForSEO extension
  installed. Use when user says "dataforseo", "live SERP", "keyword volume",
  "backlink data", "competitor data", "AI visibility check", "LLM mentions",
  or "real search data".
user-invokable: true
argument-hint: "[command] [query]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# DataForSEO: Live SEO Data (Extension)

Live search data via the DataForSEO MCP server. Provides real-time SERP results,
keyword metrics, backlink profiles, on-page analysis, content analysis, business
listings, AI visibility checking, and LLM mention tracking across
9 API modules with 79 MCP tools.

## Prerequisites

This skill requires the DataForSEO extension to be installed:
```bash
./extensions/dataforseo/install.sh
```

**Check availability:** Before using any DataForSEO tool, verify the MCP server
is connected by checking if `serp_organic_live_advanced` or any DataForSEO tool
is available. If tools are not available, inform the user the extension is not
installed and provide install instructions.

## API Credit Awareness

DataForSEO charges per API call. Be efficient:
- Prefer bulk endpoints over multiple single calls
- Use default parameters (US, English) unless user specifies otherwise
- Cache results mentally within a session; don't re-fetch the same data
- Warn user before running expensive operations (full backlink crawls, large keyword lists)

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo dataforseo serp <keyword>` | Google organic SERP results |
| `/seo dataforseo serp-youtube <keyword>` | YouTube search results |
| `/seo dataforseo youtube <video_id>` | YouTube video deep analysis |
| `/seo dataforseo keywords <seed>` | Keyword ideas and suggestions |
| `/seo dataforseo volume <keywords>` | Search volume for keywords |
| `/seo dataforseo difficulty <keywords>` | Keyword difficulty scores |
| `/seo dataforseo intent <keywords>` | Search intent classification |
| `/seo dataforseo trends <keyword>` | Google Trends data |
| `/seo dataforseo backlinks <domain>` | Full backlink profile |
| `/seo dataforseo competitors <domain>` | Competitor domain analysis |
| `/seo dataforseo ranked <domain>` | Ranked keywords for domain |
| `/seo dataforseo intersection <domains>` | Keyword/backlink overlap |
| `/seo dataforseo traffic <domains>` | Bulk traffic estimation |
| `/seo dataforseo subdomains <domain>` | Subdomains with ranking data |
| `/seo dataforseo top-searches <domain>` | Top queries mentioning domain |
| `/seo dataforseo onpage <url>` | On-page analysis (Lighthouse + parsing) |
| `/seo dataforseo tech <domain>` | Technology stack detection |
| `/seo dataforseo whois <domain>` | WHOIS registration data |
| `/seo dataforseo content <keyword/url>` | Content analysis and trends |
| `/seo dataforseo listings <keyword>` | Business listings search |
| `/seo dataforseo ai-scrape <query>` | ChatGPT web scraper for GEO |
| `/seo dataforseo ai-mentions <keyword>` | LLM mention tracking for GEO |

---

## SERP Analysis

### `/seo dataforseo serp <keyword>`

Fetch live Google organic search results.

**MCP tools:** `serp_organic_live_advanced`

**Default parameters:** location_code=2840 (US), language_code=en, device=desktop, depth=100

**Also supports:** The `serp_organic_live_advanced` tool supports Google, Bing, and Yahoo via the `se` parameter. Specify "bing" or "yahoo" to switch search engines.

**Output:** Rank, URL, title, description, domain, featured snippets, AI overview references, People Also Ask.

### `/seo dataforseo serp-youtube <keyword>`

Fetch YouTube search results. Valuable for GEO. YouTube mentions correlate most strongly with AI citations.

**MCP tools:** `serp_youtube_organic_live_advanced`

**Output:** Video title, channel, views, upload date, description, URL.

### `/seo dataforseo youtube <video_id>`

Deep analysis of a specific YouTube video: info, comments, and subtitles. YouTube mentions have the strongest correlation (0.737) with AI visibility, making this critical for GEO analysis.

**MCP tools:** `serp_youtube_video_info_live_advanced`, `serp_youtube_video_comments_live_advanced`, `serp_youtube_video_subtitles_live_advanced`

**Parameters:** video_id (the YouTube video ID, e.g., "dQw4w9WgXcQ")

**Output:** Video metadata (title, channel, views, likes, description), top comments with engagement, subtitle/transcript text.

---

## Keyword Research

### `/seo dataforseo keywords <seed>`

Generate keyword ideas, suggestions, and related terms from a seed keyword.

**MCP tools:** `dataforseo_labs_google_keyword_ideas`, `dataforseo_labs_google_keyword_suggestions`, `dataforseo_labs_google_related_keywords`

**Default parameters:** location_code=2840 (US), language_code=en, limit=50

**Output:** Keyword, search volume, CPC, competition level, keyword difficulty, trend.

### `/seo dataforseo volume <keywords>`

Get search volume and metrics for a list of keywords.

**MCP tools:** `kw_data_google_ads_search_volume`

**Parameters:** keywords (array, comma-separated), location_code, language_code

**Output:** Keyword, monthly search volume, CPC, competition, monthly trend data.

### `/seo dataforseo difficulty <keywords>`

Calculate keyword difficulty scores for ranking competitiveness.

**MCP tools:** `dataforseo_labs_bulk_keyword_difficulty`

**Parameters:** keywords (array), location_code, language_code

**Output:** Keyword, difficulty score (0-100), interpretation (Easy/Medium/Hard/Very Hard).

### `/seo dataforseo intent <keywords>`

Classify keywords by user search intent.

**MCP tools:** `dataforseo_labs_search_intent`

**Parameters:** keywords (array), location_code, language_code

**Output:** Keyword, intent type (informational, navigational, commercial, transactional), confidence score.

### `/seo dataforseo trends <keyword>`

Analyze keyword trends over time using Google Trends data.

**MCP tools:** `kw_data_google_trends_explore`

**Parameters:** keywords (array), location_code, date_from, date_to, language_code

**Output:** Keyword, time series data, trend direction, seasonality signals.

---

## Domain & Competitor Analysis

### `/seo dataforseo backlinks <domain>`

Comprehensive backlink profile analysis.

**MCP tools:** `backlinks_summary`, `backlinks_backlinks`, `backlinks_anchors`, `backlinks_referring_domains`, `backlinks_bulk_spam_score`, `backlinks_timeseries_summary`

**Default parameters:** limit=100 per sub-call

**Output:** Total backlinks, referring domains, domain rank, spam score, top anchors, new/lost backlinks over time, dofollow ratio, top referring domains.

### `/seo dataforseo competitors <domain>`

Identify competing domains and estimate traffic.

**MCP tools:** `dataforseo_labs_google_competitors_domain`, `dataforseo_labs_google_domain_rank_overview`, `dataforseo_labs_bulk_traffic_estimation`

**Output:** Competitor domains, keyword overlap %, estimated traffic, domain rank, common keywords.

### `/seo dataforseo ranked <domain>`

List keywords a domain ranks for with positions and page data.

**MCP tools:** `dataforseo_labs_google_ranked_keywords`, `dataforseo_labs_google_relevant_pages`

**Default parameters:** limit=100, location_code=2840

**Output:** Keyword, position, URL, search volume, traffic share, SERP features.

### `/seo dataforseo intersection <domain1> <domain2> [...]`

Find shared keywords and backlink sources across 2-20 domains.

**MCP tools:** `dataforseo_labs_google_domain_intersection`, `backlinks_domain_intersection`

**Parameters:** domains (2-20 array)

**Output:** Shared keywords with positions per domain, shared backlink sources, unique keywords per domain.

### `/seo dataforseo traffic <domains>`

Estimate organic search traffic for one or more domains.

**MCP tools:** `dataforseo_labs_bulk_traffic_estimation`

**Parameters:** domains (array)

**Output:** Domain, estimated organic traffic, estimated traffic cost, top keywords.

### `/seo dataforseo subdomains <domain>`

Enumerate subdomains with their ranking data and traffic estimates.

**MCP tools:** `dataforseo_labs_google_subdomains`

**Parameters:** target (domain), location_code, language_code

**Output:** Subdomain, ranked keywords count, estimated traffic, organic cost.

### `/seo dataforseo top-searches <domain>`

Find the most popular search queries that mention a specific domain in results.

**MCP tools:** `dataforseo_labs_google_top_searches`

**Parameters:** target (domain), location_code, language_code

**Output:** Query, search volume, domain position, SERP features, traffic share.

---

## Technical / On-Page

### `/seo dataforseo onpage <url>`

Run on-page analysis including Lighthouse audit and content parsing.

**MCP tools:** `on_page_instant_pages`, `on_page_content_parsing`, `on_page_lighthouse`

**Usage:**
- `on_page_instant_pages`:Quick page analysis (status codes, meta tags, content size, page timing, broken links, on-page checks)
- `on_page_content_parsing`:Extract and parse page content (plain text, word count, structure)
- `on_page_lighthouse`:Full Lighthouse audit (performance score, accessibility, best practices, SEO, Core Web Vitals)

**Output:** Pages crawled, status codes, meta tags, titles, content size, load times, Lighthouse scores, broken links, resource analysis.

### `/seo dataforseo tech <domain>`

Detect technologies used on a domain.

**MCP tools:** `domain_analytics_technologies_domain_technologies`

**Output:** Technology name, version, category (CMS, analytics, CDN, framework, etc.).

### `/seo dataforseo whois <domain>`

Retrieve WHOIS registration data.

**MCP tools:** `domain_analytics_whois_overview`

**Output:** Registrar, creation date, expiration date, nameservers, registrant info (if public).

---

## Content & Business Data

### `/seo dataforseo content <keyword/url>`

Analyze content quality, search for content by topic, and track phrase trends.

**MCP tools:** `content_analysis_search`, `content_analysis_summary`, `content_analysis_phrase_trends`

**Parameters:** keyword (for search/trends) or URL (for summary)

**Output:** Content matches with quality scores, sentiment analysis, readability metrics, phrase trend data over time.

### `/seo dataforseo listings <keyword>`

Search business listings for local SEO competitive analysis.

**MCP tools:** `business_data_business_listings_search`

**Parameters:** keyword, location (optional)

**Output:** Business name, description, category, address, phone, domain, rating, review count, claimed status.

---

## AI Visibility / GEO

### `/seo dataforseo ai-scrape <query>`

Scrape what ChatGPT web search returns for a query. Real GEO visibility check: see which sources ChatGPT cites for your target keywords.

**MCP tools:** `ai_optimization_chat_gpt_scraper`

**Parameters:** query, location_code (optional), language_code (optional). Use `ai_optimization_chat_gpt_scraper_locations` to look up available locations.

**Output:** ChatGPT response content, cited sources/URLs, referenced domains.

### `/seo dataforseo ai-mentions <keyword>`

Track how LLMs mention brands, domains, and topics. Critical for GEO. Measures actual AI visibility across multiple LLM platforms.

**MCP tools:** `ai_opt_llm_ment_search`, `ai_opt_llm_ment_top_domains`, `ai_opt_llm_ment_top_pages`, `ai_opt_llm_ment_agg_metrics`

**Parameters:** keyword, location_code (optional), language_code (optional). Use `ai_opt_llm_ment_loc_and_lang` for available locations/languages and `ai_optimization_llm_models` for supported LLM models.

**Workflow:**
1. Search LLM mentions with `ai_opt_llm_ment_search` (find mentions of a brand/keyword across LLM responses)
2. Get top cited domains with `ai_opt_llm_ment_top_domains` (which domains are most cited for this topic)
3. Get top cited pages with `ai_opt_llm_ment_top_pages` (which specific pages are most cited)
4. Get aggregate metrics with `ai_opt_llm_ment_agg_metrics` (overall mention volume, trends)

**Output:** LLM mention count, top cited domains with frequency, top cited pages, mention trends over time, cross-platform visibility scores.

**Advanced:** Use `ai_opt_llm_ment_cross_agg_metrics` for cross-model comparison (how mentions differ across ChatGPT, Claude, Perplexity, etc.).

---

## Available Utility Tools

These DataForSEO tools are available for internal use by the agent but do not have dedicated commands:

- `serp_locations`:Location code lookups for SERP queries
- `serp_youtube_locations`:Location code lookups for YouTube queries
- `kw_data_google_ads_locations`:Location lookups for keyword data
- `kw_data_dfs_trends_demography`:Demographic data for trend analysis
- `kw_data_dfs_trends_subregion_interests`:Subregion interest data for trends
- `kw_data_dfs_trends_explore`:DFS proprietary trends data
- `kw_data_google_trends_categories`:Google Trends category lookups
- `dataforseo_labs_google_keyword_overview`:Quick keyword metrics overview
- `dataforseo_labs_google_historical_serp`:Historical SERP results for a keyword
- `dataforseo_labs_google_serp_competitors`:Competitors for a specific SERP
- `dataforseo_labs_google_keywords_for_site`:Keywords a site ranks for (alternative to ranked)
- `dataforseo_labs_google_page_intersection`:Page-level intersection analysis
- `dataforseo_labs_google_historical_rank_overview`:Historical domain rank data
- `dataforseo_labs_google_historical_keyword_data`:Historical keyword metrics
- `dataforseo_labs_available_filters`:Available filter options for Labs endpoints
- `backlinks_competitors`:Find domains with similar backlink profiles
- `backlinks_bulk_backlinks`:Bulk backlink counts for multiple targets
- `backlinks_bulk_new_lost_referring_domains`:Bulk new/lost referring domains
- `backlinks_bulk_new_lost_backlinks`:Bulk new/lost backlinks
- `backlinks_bulk_ranks`:Bulk rank overview for multiple targets
- `backlinks_bulk_referring_domains`:Bulk referring domain counts
- `backlinks_domain_pages_summary`:Summary of pages on a domain
- `backlinks_domain_pages`:List pages on a domain with backlink data
- `backlinks_page_intersection`:Shared backlink sources at page level
- `backlinks_referring_networks`:Referring network analysis
- `backlinks_timeseries_new_lost_summary`:Track new/lost backlinks over time
- `backlinks_bulk_pages_summary`:Bulk page summaries
- `backlinks_available_filters`:Available filter options for Backlinks endpoints
- `domain_analytics_whois_available_filters`:WHOIS filter options
- `domain_analytics_technologies_available_filters`:Technology detection filter options
- `ai_opt_kw_data_loc_and_lang`:AI optimization keyword data locations/languages
- `ai_optimization_keyword_data_search_volume`:AI-specific keyword volume data
- `ai_optimization_llm_response`:Direct LLM response analysis
- `ai_optimization_llm_mentions_filters`:Available filters for LLM mentions
- `ai_optimization_chat_gpt_scraper_locations`:Available locations for ChatGPT scraper

## Cross-Skill Integration

When DataForSEO MCP tools are available, other claude-seo skills can leverage live data:

- **seo-audit**:Spawn `seo-dataforseo` agent for real SERP, backlink, on-page, and listings data
- **seo-technical**:Use `on_page_instant_pages` / `on_page_lighthouse` for real crawl data, `domain_analytics_technologies_domain_technologies` for stack detection
- **seo-content**:Use `kw_data_google_ads_search_volume`, `dataforseo_labs_bulk_keyword_difficulty`, `dataforseo_labs_search_intent` for real keyword metrics, `content_analysis_summary` for content quality
- **seo-page**:Use `serp_organic_live_advanced` for real SERP positions, `backlinks_summary` for link data
- **seo-geo**:Use `ai_optimization_chat_gpt_scraper` for real ChatGPT visibility, `ai_opt_llm_ment_search` for LLM mention tracking
- **seo-plan**:Use `dataforseo_labs_google_competitors_domain`, `dataforseo_labs_google_domain_intersection`, `dataforseo_labs_bulk_traffic_estimation` for real competitive intelligence

## Error Handling

- **MCP server not connected**: Report that DataForSEO extension is not installed or MCP server is unreachable. Suggest running `./extensions/dataforseo/install.sh`
- **API authentication failed**: Report invalid credentials. Suggest checking DataForSEO API login/password in MCP config
- **Rate limit exceeded**: Report the limit hit and suggest waiting before retrying
- **No results returned**: Report "no data found" for the query rather than guessing. Suggest broadening the query or checking location/language codes
- **Invalid location code**: Report the error and suggest using the locations lookup tool to find the correct code

## Output Formatting

Match existing claude-seo output patterns:
- Use tables for comparative data
- Prioritize issues as Critical > High > Medium > Low
- Include specific, actionable recommendations
- Show scores as XX/100 where applicable
- Note data source as "DataForSEO (live)" to distinguish from static analysis

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — SERP data é live e atribuído a data/hora concreta
- [ ] Resultados SERP incluem timestamp da fetch (ex: "dados recolhidos em 2025-01-23 14:32 UTC")
- [ ] Rank positions são números reais, não estimativas ("posição #3" não "top results")
- [ ] Featured snippets e AI Overviews identificados explicitamente se presentes
- [ ] Search engine especificado (Google/Bing/Yahoo) e location_code declarado

❌ NOT delivery-ready: "O site aparece bem posicionado no Google para este keyword."
✅ Delivery-ready: "tributario.ai ocupa posição #4 no Google US (location_code 2840) para 'AI tax compliance Portugal' — fetch 2025-01-23 14:32 UTC. Featured snippet em #0: domínio concorrente taxjar.com."

---

### Gate 2 — Keyword metrics são numéricos e com fonte DataForSEO declarada
- [ ] Volume de pesquisa é número exato ou range (ex: "2.400/mês"), nunca "alto/baixo"
- [ ] Keyword difficulty score 0-100 presente com classificação (Easy/Medium/Hard/Very Hard)
- [ ] CPC em USD declarado quando relevante para contexto comercial
- [ ] Intent classificado (Informational/Navigational/Transactional/Commercial) com % de confiança se disponível

❌ NOT delivery-ready: "'gestão financeira PME' tem bastante volume e dificuldade moderada."
✅ Delivery-ready: "'gestão financeira PME' — volume: 1.900/mês, KD: 42/100 (Medium), CPC: $1.20, intent: Informational. Fonte: DataForSEO Labs Google, PT, 2025-01-23."

---

### Gate 3 — Backlink profile tem métricas de domínio concretas
- [ ] Número total de backlinks e referring domains são valores absolutos
- [ ] Domain Rating / authority score presente se tool o devolveu
- [ ] Top 3 referring domains nomeados com anchor text real
- [ ] Aviso de créditos API incluído se foi corrida análise de backlink completa (crawl intensivo)

❌ NOT delivery-ready: "O perfil de backlinks do cuidai.pt é razoável com alguns links de qualidade."
✅ Delivery-ready: "cuidai.pt — 847 backlinks totais, 134 referring domains. Top linkers: sapo.pt (anchor: 'cuidado sénior'), publico.pt (anchor: 'startup saúde'), dn.pt (anchor: 'cuidai'). Fonte: DataForSEO Backlinks, 2025-01-23."

---

### Gate 4 — Competitor analysis identifica domínios reais com gaps accionáveis
- [ ] Mínimo 3 competitor domains nomeados explicitamente (não "os seus concorrentes")
- [ ] Keyword intersection mostra keywords onde competitor rankeia e client não
- [ ] Traffic estimation em visitas/mês declarado para cada domínio comparado
- [ ] Gap keywords priorizadas por volume + KD, não apenas listadas

❌ NOT delivery-ready: "A análise de concorrentes mostra que há oportunidades de keywords por explorar."
✅ Delivery-ready: "LUSOconta.pt vs concorrentes: n26.com (est. 42.000 visitas/mês), revolut.com/pt (est. 78.000/mês). Gap keywords exclusivas dos concorrentes: 'conta bancária sem comissões' (vol 3.600, KD 38) — LUSOconta.pt não rankeia no top 100."

---

### Gate 5 — AI Visibility / GEO data distinguido de SEO tradicional
- [ ] ai-scrape e ai-mentions resultados apresentados em secção própria "GEO / AI Visibility"
- [ ] YouTube correlation (0.737) referenciada quando video data é incluído
- [ ] LLM mentions tracking mostra plataformas específicas (ChatGPT, Perplexity, etc.) e contagem
- [ ] Recomendações GEO separadas de recomendações SEO clássico

❌ NOT delivery-ready: "A marca tem alguma presença em motores de IA."
✅ Delivery-ready: "SAQUEI.pt — GEO check 2025-01-23: 0 menções LLM detetadas em ChatGPT scraper para 'adiantamento de salário Portugal'. YouTube: 2 vídeos relevantes no top-10 de concorrentes (Coverflex, 180K views combinadas). Ação prioritária: criar conteúdo YouTube antes de outreach editorial."

---

### Gate 6 — Output usa NOME DO CLIENT + dados reais, sem angle-brackets placeholder
- [ ] Zero instâncias de `<client_name>`, `<domain>`, `<keyword>`, `<insert here>`
- [ ] Nome da empresa/domínio real presente no título e em cada secção de dados
- [ ] Data da recolha de dados DataForSEO declarada (não "dados recentes")
- [ ] Se extensão DataForSEO não estava disponível, output diz isso explicitamente — não inventa dados

❌ NOT delivery-ready: "Para `<client_domain>`, os resultados de `<target_keyword>` mostram `<ranking_position>`."
✅ Delivery-ready: "Atrium.pt — SERP analysis para 'escritório de advogados Lisboa' (Google PT, 2025-01-23): posição #7, CTR estimado 3.2%. Acima: mlgts.pt (#1), plmj.pt (#2), cuatrecasas.com (#3)."

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# SEO Report — Tributario.AI
**DataForSEO live pull: 2025-01-23 15:04 UTC | Google PT (location_code 2616) | Desktop**

---

## 1. SERP Snapshot — "software fiscal Portugal"

| Pos | Domínio | Título | Snippet |
|-----|---------|--------|---------|
| #1 | primavera-bss.com | "Software de Gestão Fiscal..." | Featured Snippet ✓ |
| #2 | sage.com/pt | "Sage 50 — Contabilidade e Fiscal" | — |
| #3 | totvs.com | "ERP Fiscal para Portugal" | — |
| #7 | tributario.ai | "IA para Compliance Fiscal PT" | — |

**AI Overview presente:** Sim — cita primavera-bss.com e sage.com/pt. tributario.ai não citado.
**People Also Ask:** "Qual o melhor software de contabilidade em Portugal?", "O que é o SAF-T?"

---

## 2. Keyword Research — Seed: "compliance fiscal"

| Keyword | Volume/mês | KD | Intent | CPC |
|---------|-----------|-----|--------|-----|
| compliance fiscal portugal | 880 | 31 (Easy) | Informational | $2.10 |
| software fiscal pme | 590 | 44 (Medium) | Commercial | $3.80 |
| saf-t portugal obrigações | 1.300 | 28 (Easy) | Informational | $1.40 |
| automação fiscal ia | 210 | 22 (Easy) | Commercial | $4.20 |
| declaração ies prazo 2025 | 2.900 | 19 (Easy) | Navigational | $0.90 |

**Quick win identificado:** "automação fiscal ia" — volume baixo mas KD 22, intent Commercial, zero concorrência AI-native. tributario.ai pode rankear #1 em 60-90 dias com 1 artigo optimizado.

---

## 3. Backlink Profile — tributario.ai

- **Total backlinks:** 312
- **Referring domains:** 47
- **Top 3 linkers:**
  - jornal-negocios.pt — anchor: "inteligência artificial fiscal"
  - contabilidade.pt — anchor: "tributario ai review"
  - startupportugal.com — anchor: "startup fiscal portuguesa"
- **Gap vs primavera-bss.com:** 4.200 RDs vs 47 RDs — oportunidade de link building significativa via press/PR

---

## 4. Competitor Traffic Estimation

| Domínio | Visitas/mês (est.) | Top keyword |
|---------|-------------------|-------------|
| primavera-bss.com | 68.000 | "software contabilidade" (vol 8.100) |
| sage.com/pt | 41.000 | "sage 50 portugal" (vol 3.600) |
| totvs.com/pt | 12.000 | "erp fiscal" (vol 1.200) |
| tributario.ai | 1.800 | "tributario ai" (branded) |

**Gap keywords onde concorrentes rankeiam, tributario.ai não (top 100):**
- "automação contabilidade pme" — vol 720, KD 35
- "ia para contabilistas" — vol 480, KD 27
- "relatório fiscal automático" — vol 390, KD 29

---

## 5. GEO / AI Visibility — tributario.ai

**ChatGPT scraper (2025-01-23):** 0 menções para "software fiscal IA Portugal"
**LLM mentions tracking:**
- ChatGPT: 0 menções diretas | concorrentes citados: primavera-bss.com (3x), sage.com (2x)
- Perplexity: 0 menções diretas

**YouTube — "compliance fiscal portugal":**
- #1: "SAF-T Explicado 2024" — Canal ContabilidadePT, 34.000 views (sem menção a tributario.ai)
- #2: "Obrigações Fiscais PME" — Canal GestãoPT, 18.000 views

**Correlação YouTube→LLM (0.737):** tributario.ai sem presença YouTube = baixíssima probabilidade de citação em LLMs.

**Recomendação GEO prioritária:** Produzir 1 vídeo YouTube "IA para Compliance Fiscal Portugal 2025" antes de qualquer outreach editorial. Estimativa de impacto em citações LLM: +40-60% em 90 dias (benchmark DataForSEO GEO studies).

---

## 6. Próximos Passos (prioridade decrescente)

1. **[Semana 1]** Publicar artigo "automação fiscal ia" (KD 22, commercial intent) — alvo posição #1-3
2. **[Semana 2]** Produzir vídeo YouTube sobre SAF-T/compliance — GEO pipeline
3. **[Mês 1]** Link building: pitch para 5 publishers PT onde primavera-bss.com tem links (jornal-negocios.pt, dinheiro-vivo.pt, economico.pt)
4. **[Mês 2]** Optimizar on-page para "saf-t portugal obrigações" (vol 1.300, KD 28) — quick traffic win
```

---

## Output anti-patterns

- Usar "alto volume" / "boa dificuldade" / "forte presença" sem números — DataForSEO devolve valores exatos, usá-los é obrigatório
- Misturar dados cached/estimados com dados live sem distinguir a fonte e data de cada um
- Fazer recomendações SEO e GEO na mesma lista como se fossem equivalentes — são canais distintos com mécanismos diferentes
- Inventar métricas quando a extensão DataForSEO não está instalada em vez de dizer explicitamente "extensão não disponível"
- Listar gap keywords sem ordenar por accionabilidade (volume × KD × intent) — listas não priorizadas não têm valor estratégico
- Reportar backlinks sem referir referring domains — link count sozinho é métrica enganosa
- Omitir location_code e language_code do report — os mesmos dados variam drasticamente por mercado
- Apresentar AI Visibility como extensão de SEO clássico em vez de canal autónomo com correlações próprias (YouTube 0.737, Reddit 0.681)
- Usar angle-brackets `<domain>` ou `<keyword>` no output final entregue ao cliente
