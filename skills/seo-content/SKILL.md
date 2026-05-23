---
name: seo-content
description: >
  Content quality and E-E-A-T analysis with AI citation readiness assessment.
  Use when user says "content quality", "E-E-A-T", "content analysis",
  "readability check", "thin content", or "content audit".
user-invokable: true
argument-hint: "[url]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# Content Quality & E-E-A-T Analysis

## E-E-A-T Framework (updated Sept 2025 QRG)

Read `seo/references/eeat-framework.md` for full criteria.

### Experience (first-hand signals)
- Original research, case studies, before/after results
- Personal anecdotes, process documentation
- Unique data, proprietary insights
- Photos/videos from direct experience

### Expertise
- Author credentials, certifications, bio
- Professional background relevant to topic
- Technical depth appropriate for audience
- Accurate, well-sourced claims

### Authoritativeness
- External citations, backlinks from authoritative sources
- Brand mentions, industry recognition
- Published in recognized outlets
- Cited by other experts

### Trustworthiness
- Contact information, physical address
- Privacy policy, terms of service
- Customer testimonials, reviews
- Date stamps, transparent corrections
- Secure site (HTTPS)

## Content Metrics

### Word Count Analysis
Compare against page type minimums:
| Page Type | Minimum |
|-----------|---------|
| Homepage | 500 |
| Service page | 800 |
| Blog post | 1,500 |
| Product page | 300+ (400+ for complex products) |
| Location page | 500-600 |

> **Important:** These are **topical coverage floors**, not targets. Google has confirmed word count is NOT a direct ranking factor. The goal is comprehensive topical coverage; a 500-word page that thoroughly answers the query will outrank a 2,000-word page that doesn't. Use these as guidelines for adequate coverage depth, not rigid requirements.

### Readability
- Flesch Reading Ease: target 60-70 for general audience

> **Note:** Flesch Reading Ease is a useful proxy for content accessibility but is NOT a direct Google ranking factor. John Mueller has confirmed Google does not use basic readability scores for ranking. Yoast deprioritized Flesch scores in v19.3. Use readability analysis as a content quality indicator, not as an SEO metric to optimize directly.
- Grade level: match target audience
- Sentence length: average 15-20 words
- Paragraph length: 2-4 sentences

### Keyword Optimization
- Primary keyword in title, H1, first 100 words
- Natural density (1-3%)
- Semantic variations present
- No keyword stuffing

### Content Structure
- Logical heading hierarchy (H1 -> H2 -> H3)
- Scannable sections with descriptive headings
- Bullet/numbered lists where appropriate
- Table of contents for long-form content

### Multimedia
- Relevant images with proper alt text
- Videos where appropriate
- Infographics for complex data
- Charts/graphs for statistics

### Internal Linking
- 3-5 relevant internal links per 1000 words
- Descriptive anchor text
- Links to related content
- No orphan pages

### External Linking
- Cite authoritative sources
- Open in new tab for user experience
- Reasonable count (not excessive)

## AI Content Assessment (Sept 2025 QRG addition)

Google's raters now formally assess whether content appears AI-generated.

### Acceptable AI Content
- Demonstrates genuine E-E-A-T
- Provides unique value
- Has human oversight and editing
- Contains original insights

### Low-Quality AI Content Markers
- Generic phrasing, lack of specificity
- No original insight
- Repetitive structure across pages
- No author attribution
- Factual inaccuracies

> **Helpful Content System (March 2024):** The Helpful Content System was merged into Google's core ranking algorithm during the March 2024 core update. It no longer operates as a standalone classifier. Helpfulness signals are now weighted within every core update. The same principles apply (people-first content, demonstrating E-E-A-T, satisfying user intent), but enforcement is continuous rather than through separate HCU updates.

## AI Citation Readiness (GEO signals)

Optimize for AI search engines (ChatGPT, Perplexity, Google AI Overviews):

- Clear, quotable statements with statistics/facts
- Structured data (especially for data points)
- Strong heading hierarchy (H1->H2->H3 flow)
- Answer-first formatting for key questions
- Tables and lists for comparative data
- Clear attribution and source citations

### AI Search Visibility & GEO (2025-2026)

**Google AI Mode** launched publicly in May 2025 as a separate tab in Google Search, available in 180+ countries. Unlike AI Overviews (which appear above organic results), AI Mode provides a fully conversational search experience with **zero organic blue links**, making AI citation the only visibility mechanism.

**Key optimization strategies for AI citation:**
- **Structured answers:** Clear question-answer formats, definition patterns, and step-by-step instructions that AI systems can extract and cite
- **First-party data:** Original research, statistics, case studies, and unique datasets are highly cited by AI systems
- **Schema markup:** Article, FAQ (for non-Google AI platforms), and structured content schemas help AI systems parse and attribute content
- **Topical authority:** AI systems preferentially cite sources that demonstrate deep expertise. Build content clusters, not isolated pages
- **Entity clarity:** Ensure brand, authors, and key concepts are clearly defined with structured data (Organization, Person schema)
- **Multi-platform tracking:** Monitor visibility across Google AI Overviews, AI Mode, ChatGPT, Perplexity, and Bing Copilot, not just traditional rankings. Treat AI citation as a standalone KPI alongside organic rankings and traffic.

**Generative Engine Optimization (GEO):**
GEO is the emerging discipline of optimizing content specifically for AI-generated answers. Key GEO signals include: quotability (clear, concise extractable facts), attribution (source citations within your content), structure (well-organized heading hierarchy), and freshness (regularly updated data). Cross-reference the `seo-geo` skill for detailed GEO workflows.

## Content Freshness

- Publication date visible
- Last updated date if content has been revised
- Flag content older than 12 months without update for fast-changing topics

## Output

### Content Quality Score: XX/100

### E-E-A-T Breakdown
| Factor | Score | Key Signals |
|--------|-------|-------------|
| Experience | XX/25 | ... |
| Expertise | XX/25 | ... |
| Authoritativeness | XX/25 | ... |
| Trustworthiness | XX/25 | ... |

### AI Citation Readiness: XX/100

### Issues Found
### Recommendations

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, use `kw_data_google_ads_search_volume` for real keyword volume data, `dataforseo_labs_bulk_keyword_difficulty` for difficulty scores, `dataforseo_labs_search_intent` for intent classification, and `content_analysis_summary` for content quality analysis.

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable (DNS failure, connection refused) | Report the error clearly. Do not guess page content. Suggest the user verify the URL and try again. |
| Content behind paywall (402/403, login wall) | Report that the content is not publicly accessible. Analyze only the visible portion (meta tags, headers) and note the limitation. |
| Thin content (fewer than 100 words retrievable) | Report the findings as-is rather than guessing. Flag the page as potentially JavaScript-rendered or gated, and suggest the user provide the full text directly. |

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — E-E-A-T scoring é específico, não genérico
- [ ] Cada dimensão (Experience, Expertise, Authoritativeness, Trustworthiness) tem score explícito (ex: 3/5) com justificação baseada no conteúdo real
- [ ] Sinais presentes **e ausentes** estão identificados com exemplos da página
- [ ] Não usa linguagem vaga como "o conteúdo demonstra alguma expertise"
- ❌ NOT delivery-ready: "A página tem boa autoridade e demonstra expertise no tema."
- ✅ Delivery-ready: "Expertise: 2/5 — Sem bio de autor, sem credenciais, sem fontes citadas. A secção 'Como funciona' usa linguagem genérica sem referência a metodologia própria."

### Gate 2 — Word count e cobertura temática são avaliados em conjunto
- [ ] Word count real da página está registado (ex: "812 palavras")
- [ ] Floor relevante para o page type está citado (ex: "service page: mínimo 800")
- [ ] Conclusão distingue entre "abaixo do floor" e "cobre o tópico adequadamente"
- [ ] Não trata word count como ranking factor direto — menciona cobertura temática como critério real
- ❌ NOT delivery-ready: "A página tem poucas palavras e precisa de mais conteúdo para rankear."
- ✅ Delivery-ready: "647 palavras (service page floor: 800). Conteúdo abaixo do floor E com gaps temáticos: não aborda preços, processo de onboarding nem FAQs — subcobertura real, não apenas contagem."

### Gate 3 — AI Content Assessment tem diagnóstico concreto
- [ ] Identifica marcadores específicos de AI-generated low-quality presentes/ausentes na página
- [ ] Refere presença ou ausência de author attribution com nome real
- [ ] Avalia se existe insight original ou apenas reformulação genérica
- [ ] Menciona alinhamento com March 2024 core update (Helpful Content integrado no core)
- ❌ NOT delivery-ready: "O conteúdo parece gerado por IA e falta personalização."
- ✅ Delivery-ready: "3 marcadores de AI low-quality detetados: estrutura repetitiva entre parágrafos 2–4, ausência de autor nomeado, zero dados originais. Nenhuma anedota/caso real. Risco de penalização em próximo core update."

### Gate 4 — AI Citation Readiness / GEO tem recomendações acionáveis
- [ ] Avalia se existem statements quotáveis com estatísticas ou factos verificáveis
- [ ] Verifica presença de schema markup relevante (Article, FAQ, Organization, Person)
- [ ] Indica cobertura multi-plataforma: Google AI Overviews, AI Mode, Perplexity, ChatGPT
- [ ] Recomendações são específicas: "adicionar X" não "melhorar structured data"
- ❌ NOT delivery-ready: "A página deveria otimizar para GEO e melhorar a estrutura para AI."
- ✅ Delivery-ready: "0 statements quotáveis com dados numéricos. Sem Article schema. Sem FAQ schema. Recomendação: adicionar bloco resposta-direta após cada H2, implementar FAQPage schema com 4–6 perguntas, adicionar stat original (ex: resultado de cliente com número real)."

### Gate 5 — Keyword optimization e estrutura têm diagnóstico página a página
- [ ] Keyword primária identificada explicitamente com localização na página (título, H1, primeiras 100 palavras)
- [ ] Hierarquia de headings auditada (H1→H2→H3) com problemas específicos listados
- [ ] Internal linking count real vs benchmark (3–5 por 1000 palavras) está calculado
- [ ] Density estimada ou sinalizada como risco (stuffing ou ausência)
- ❌ NOT delivery-ready: "Os headings poderiam ser melhorados e há pouca linkagem interna."
- ✅ Delivery-ready: "Keyword 'software de faturação PME' ausente nas primeiras 100 palavras. H1 presente mas H2s não usam variações semânticas. 1 internal link para 1.200 palavras (benchmark: 3–5). Hierarquia: H1→H3 direto (H2 em falta)."

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] Nome do cliente/marca aparece no output (ex: Cuidai, SAQUEI, Tributario.AI)
- [ ] URL ou página auditada está identificada explicitamente
- [ ] Nenhum placeholder do tipo `[CLIENT NAME]`, `[URL]`, `[INSERT KEYWORD]` sobreviveu
- [ ] Todos os scores, counts e recomendações referem conteúdo real da página analisada
- ❌ NOT delivery-ready: "A página [URL] do cliente [NOME] tem [X] palavras e keyword [KEYWORD] ausente."
- ✅ Delivery-ready: "Página auditada: tributario.ai/blog/irs-2025. 934 palavras. Keyword 'IRS 2025 prazo' presente no H1 mas ausente nas primeiras 100 palavras do body."

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Análise E-E-A-T & Content Quality — Cuidai.pt/blog/cuidadores-idosos-lisboa

**URL:** cuidai.pt/blog/cuidadores-idosos-lisboa
**Data da análise:** 14 junho 2025
**Page type:** Blog post
**Keyword primária:** "cuidadores de idosos Lisboa"

---

## E-E-A-T Scoring

| Dimensão | Score | Justificação |
|---|---|---|
| Experience | 2/5 | Sem casos reais de famílias assistidas, sem fotos de cuidadores em contexto, sem dados de resultados |
| Expertise | 3/5 | Mencionada "equipa especializada" mas sem bio de autor, sem certificações ACSS citadas |
| Authoritativeness | 2/5 | 0 fontes externas citadas, sem menção de parcerias ou reconhecimento sectorial |
| Trustworthiness | 4/5 | HTTPS ✓, morada física ✓, política de privacidade ✓, sem data de publicação visível |

**Score E-E-A-T global: 11/20 — abaixo do threshold recomendado (14/20) para conteúdo YMYL (saúde/cuidados).**

---

## Word Count & Cobertura Temática

- **Contagem real:** 1.087 palavras
- **Floor para blog post:** 1.500 palavras
- **Gap:** −413 palavras — E com subcobertura real

**Tópicos em falta detetados:**
1. Critérios de seleção/formação dos cuidadores Cuidai
2. Preços ou como funciona o orçamento
3. Diferença cuidados temporários vs. permanentes
4. Perguntas frequentes de famílias (FAQ)

→ Recomendação: expandir para ~1.700 palavras adicionando secções em falta, não padding.

---

## AI Content Assessment

**Marcadores low-quality detetados: 2/5**

- ✅ Ausência de estrutura repetitiva entre parágrafos
- ✅ Tom consistente com voz da marca
- ❌ Zero dados originais (sem números de cuidadores, sem anos de operação, sem casos)
- ❌ Sem autor nomeado (byline ausente)
- ✅ Sem incoerências factuais detetadas

**Diagnóstico:** Conteúdo human-written mas sem prova de experiência direta.
Risco médio num próximo core update por ausência de E-E-A-T signals em página YMYL.

---

## AI Citation Readiness (GEO)

**Score de quotabilidade:** 1/10 statements com dado numérico concreto.

| Signal GEO | Status |
|---|---|
| Statements quotáveis com stats | ❌ 0 detetados |
| Formato answer-first após H2s | ❌ Ausente |
| Article schema | ❌ Não implementado |
| FAQPage schema | ❌ Não implementado |
| Person/Organization schema | ✅ Organization parcial |
| Visibilidade AI Overviews (estimada) | ❌ Baixa — sem dados citáveis |

**Recomendações GEO prioritárias:**
1. Adicionar stat Cuidai real no parágrafo de abertura: ex. "Mais de 340 famílias assistidas em Lisboa desde 2019"
2. Criar bloco resposta-direta após H2 "Quanto custa um cuidador de idosos em Lisboa"
3. Implementar FAQPage schema com 5 perguntas de intenção transacional
4. Monitorizar citações em Perplexity e Google AI Overviews mensalmente como KPI autónomo

---

## Keyword & Estrutura

- **Keyword "cuidadores de idosos Lisboa":** presente no H1 ✓, ausente nas primeiras 100 palavras ❌, density ~0,8% (abaixo de 1%)
- **Variações semânticas detetadas:** "apoio domiciliário", "cuidados geriátricos" — ✓
- **Hierarquia headings:** H1 → H2 → H2 → H3 → H2 — estrutura válida ✓
- **Internal links:** 2 links para 1.087 palavras (benchmark: 3–5 por 1.000 palavras) — ❌ défice

**Internal links em falta sugeridos:**
- → cuidai.pt/servicos/apoio-domiciliario
- → cuidai.pt/como-funciona
- → cuidai.pt/faq

---

## Próximos passos (por prioridade)

1. 🔴 Adicionar author bio com credenciais (nome, formação na área de saúde/cuidados)
2. 🔴 Inserir 1 caso real / testemunho com resultado mensurável
3. 🟡 Expandir para 1.700 palavras com secções em falta
4. 🟡 Implementar Article + FAQPage schema
5. 🟢 Adicionar keyword nas primeiras 100 palavras
6. 🟢 Adicionar 2 internal links adicionais
```

---

## Output anti-patterns

- Dar score E-E-A-T sem justificação por dimensão ("conteúdo com boa autoridade" sem evidência)
- Tratar word count como ranking factor direto ("precisa de mais palavras para rankear melhor")
- Recomendar "melhorar o SEO" ou "otimizar para AI" sem especificar o quê, onde e como
- Usar placeholders `[KEYWORD]`, `[URL]`, `[NOME DO CLIENTE]` no output final
- Misturar diagnóstico com recomendação sem separar o que existe hoje vs. o que deve ser feito
- Não distinguir AI Overviews de AI Mode — são mecanismos distintos com implicações diferentes
- Reportar Flesch Reading Ease como métrica SEO direta sem nota de contexto (não é ranking factor)
- Auditar estrutura de headings sem listar os headings reais encontrados na página
- Omitir o diagnóstico de AI-generated content markers em páginas sem autor atribuído
- Dar recomendações GEO sem identificar se a página tem sequer um statement quotável com dado verificável
