---
name: seo-geo
description: >
  Optimize content for AI Overviews (formerly SGE), ChatGPT web search,
  Perplexity, and other AI-powered search experiences. Generative Engine
  Optimization (GEO) analysis including brand mention signals, AI crawler
  accessibility, llms.txt compliance, passage-level citability scoring, and
  platform-specific optimization. Use when user says "AI Overviews", "SGE",
  "GEO", "AI search", "LLM optimization", "Perplexity", "AI citations",
  "ChatGPT search", or "AI visibility".
user-invokable: true
argument-hint: "[url]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# AI Search / GEO Optimization (February 2026)

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| AI Overviews reach | 1.5 billion users/month across 200+ countries | Google |
| AI Overviews query coverage | 50%+ of all queries | Industry data |
| AI-referred sessions growth | 527% (Jan-May 2025) | SparkToro |
| ChatGPT weekly active users | 900 million | OpenAI |
| Perplexity monthly queries | 500+ million | Perplexity |

## Critical Insight: Brand Mentions > Backlinks

**Brand mentions correlate 3x more strongly with AI visibility than backlinks.**
(Ahrefs December 2025 study of 75,000 brands)

| Signal | Correlation with AI Citations |
|--------|------------------------------|
| YouTube mentions | ~0.737 (strongest) |
| Reddit mentions | High |
| Wikipedia presence | High |
| LinkedIn presence | Moderate |
| Domain Rating (backlinks) | ~0.266 (weak) |

**Only 11% of domains** are cited by both ChatGPT and Google AI Overviews for the same query, so platform-specific optimization is essential.

---

## GEO Analysis Criteria (Updated)

### 1. Citability Score (25%)

**Optimal passage length: 134-167 words** for AI citation.

**Strong signals:**
- Clear, quotable sentences with specific facts/statistics
- Self-contained answer blocks (can be extracted without context)
- Direct answer in first 40-60 words of section
- Claims attributed with specific sources
- Definitions following "X is..." or "X refers to..." patterns
- Unique data points not found elsewhere

**Weak signals:**
- Vague, general statements
- Opinion without evidence
- Buried conclusions
- No specific data points

### 2. Structural Readability (20%)

**92% of AI Overview citations come from top-10 ranking pages**, but 47% come from pages ranking below position 5, demonstrating different selection logic.

**Strong signals:**
- Clean H1->H2->H3 heading hierarchy
- Question-based headings (matches query patterns)
- Short paragraphs (2-4 sentences)
- Tables for comparative data
- Ordered/unordered lists for step-by-step or multi-item content
- FAQ sections with clear Q&A format

**Weak signals:**
- Wall of text with no structure
- Inconsistent heading hierarchy
- No lists or tables
- Information buried in paragraphs

### 3. Multi-Modal Content (15%)

Content with multi-modal elements sees **156% higher selection rates**.

**Check for:**
- Text + relevant images
- Video content (embedded or linked)
- Infographics and charts
- Interactive elements (calculators, tools)
- Structured data supporting media

### 4. Authority & Brand Signals (20%)

**Strong signals:**
- Author byline with credentials
- Publication date and last-updated date
- Citations to primary sources (studies, official docs, data)
- Organization credentials and affiliations
- Expert quotes with attribution
- Entity presence in Wikipedia, Wikidata
- Mentions on Reddit, YouTube, LinkedIn

**Weak signals:**
- Anonymous authorship
- No dates
- No sources cited
- No brand presence across platforms

### 5. Technical Accessibility (20%)

**AI crawlers do NOT execute JavaScript.** Server-side rendering is critical.

**Check for:**
- Server-side rendering (SSR) vs client-only content
- AI crawler access in robots.txt
- llms.txt file presence and configuration
- RSL 1.0 licensing terms

---

## AI Crawler Detection

Check `robots.txt` for these AI crawlers:

| Crawler | Owner | Purpose |
|---------|-------|---------|
| GPTBot | OpenAI | ChatGPT web search |
| OAI-SearchBot | OpenAI | OpenAI search features |
| ChatGPT-User | OpenAI | ChatGPT browsing |
| ClaudeBot | Anthropic | Claude web features |
| PerplexityBot | Perplexity | Perplexity AI search |
| CCBot | Common Crawl | Training data (often blocked) |
| anthropic-ai | Anthropic | Claude training |
| Bytespider | ByteDance | TikTok/Douyin AI |
| cohere-ai | Cohere | Cohere models |

**Recommendation:** Allow GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot for AI search visibility. Block CCBot and training crawlers if desired.

---

## llms.txt Standard

The emerging **llms.txt** standard provides AI crawlers with structured content guidance.

**Location:** `/llms.txt` (root of domain)

**Format:**
```
# Title of site
> Brief description

## Main sections
- [Page title](url): Description
- [Another page](url): Description

## Optional: Key facts
- Fact 1
- Fact 2
```

**Check for:**
- Presence of `/llms.txt`
- Structured content guidance
- Key page highlights
- Contact/authority information

---

## RSL 1.0 (Really Simple Licensing)

New standard (December 2025) for machine-readable AI licensing terms.

**Backed by:** Reddit, Yahoo, Medium, Quora, Cloudflare, Akamai, Creative Commons

**Check for:** RSL implementation and appropriate licensing terms.

---

## Platform-Specific Optimization

| Platform | Key Citation Sources | Optimization Focus |
|----------|---------------------|-------------------|
| **Google AI Overviews** | Top-10 ranking pages (92%) | Traditional SEO + passage optimization |
| **ChatGPT** | Wikipedia (47.9%), Reddit (11.3%) | Entity presence, authoritative sources |
| **Perplexity** | Reddit (46.7%), Wikipedia | Community validation, discussions |
| **Bing Copilot** | Bing index, authoritative sites | Bing SEO, IndexNow |

---

## Output

Generate `GEO-ANALYSIS.md` with:

1. **GEO Readiness Score: XX/100**
2. **Platform breakdown** (Google AIO, ChatGPT, Perplexity scores)
3. **AI Crawler Access Status** (which crawlers allowed/blocked)
4. **llms.txt Status** (present, missing, recommendations)
5. **Brand Mention Analysis** (presence on Wikipedia, Reddit, YouTube, LinkedIn)
6. **Passage-Level Citability** (optimal 134-167 word blocks identified)
7. **Server-Side Rendering Check** (JavaScript dependency analysis)
8. **Top 5 Highest-Impact Changes**
9. **Schema Recommendations** (for AI discoverability)
10. **Content Reformatting Suggestions** (specific passages to rewrite)

---

## Quick Wins

1. Add "What is [topic]?" definition in first 60 words
2. Create 134-167 word self-contained answer blocks
3. Add question-based H2/H3 headings
4. Include specific statistics with sources
5. Add publication/update dates
6. Implement Person schema for authors
7. Allow key AI crawlers in robots.txt

## Medium Effort

1. Create `/llms.txt` file
2. Add author bio with credentials + Wikipedia/LinkedIn links
3. Ensure server-side rendering for key content
4. Build entity presence on Reddit, YouTube
5. Add comparison tables with data
6. Implement FAQ sections (structured, not schema for commercial sites)

## High Impact

1. Create original research/surveys (unique citability)
2. Build Wikipedia presence for brand/key people
3. Establish YouTube channel with content mentions
4. Implement comprehensive entity linking (sameAs across platforms)
5. Develop unique tools or calculators

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, use `ai_optimization_chat_gpt_scraper` to check what ChatGPT web search returns for target queries (real GEO visibility check) and `ai_opt_llm_ment_search` with `ai_opt_llm_ment_top_domains` for LLM mention tracking across AI platforms.

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable (DNS failure, connection refused) | Report the error clearly. Do not guess site content. Suggest the user verify the URL and try again. |
| AI crawlers blocked by robots.txt | Report exactly which crawlers are blocked and which are allowed. Provide specific robots.txt directives to add for enabling AI search visibility. |
| No llms.txt found | Note the absence and provide a ready-to-use llms.txt template based on the site's content structure. |
| No structured data detected | Report the gap and provide specific schema recommendations (Article, Organization, Person) for improving AI discoverability. |

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — GEO Readiness Score é fundamentado, não estimado

- [ ] Score XX/100 tem breakdown explícito por componente (Citability 25%, Structural 20%, Multi-Modal 15%, Authority 20%, Technical 20%)
- [ ] Cada sub-score tem evidência específica da URL analisada (não "parece ter boa estrutura")
- [ ] Pontuações não são todas redondas (49/100, não 50/100; 17/25, não 15/25)
- [ ] Score final é acompanhado de benchmark de contexto ("acima da mediana para SaaS PT")

❌ NOT delivery-ready: `GEO Score: 60/100 — o site tem boa estrutura mas pode melhorar a autoridade.`
✅ Delivery-ready: `GEO Score: 63/100 — Citability: 14/25 (sem blocos self-contained <167 palavras), Structural: 16/20 (H1→H2 correto, sem FAQ), Multi-Modal: 7/15 (0 vídeos, 2 imagens sem alt-text), Authority: 14/20 (sem Wikipedia, Reddit: 0 menções), Technical: 12/20 (GPTBot bloqueado em robots.txt, sem llms.txt).`

---

### Gate 2 — Análise de robots.txt e AI crawlers é concreta

- [ ] Lista exata dos crawlers permitidos/bloqueados encontrados no robots.txt real do cliente
- [ ] GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot têm status explícito (Allow / Disallow / Ausente)
- [ ] Impacto de cada bloqueio é quantificado em termos de plataforma afetada
- [ ] Recomendação de acção é específica (linha exacta a adicionar/remover do robots.txt)

❌ NOT delivery-ready: `O robots.txt pode estar a bloquear alguns crawlers de IA. Recomendamos verificar.`
✅ Delivery-ready: `robots.txt de cuidai.pt (fetch 2026-02-14): GPTBot → Disallow (❌ bloqueia ChatGPT Search), PerplexityBot → ausente (não explicitamente permitido), ClaudeBot → Allow ✅. Acção: adicionar \`User-agent: GPTBot\nAllow: /\` — remove bloqueio a 900M utilizadores ChatGPT.`

---

### Gate 3 — Citability Score tem exemplos de passagens reais do site

- [ ] Pelo menos 2 passagens reais extraídas do URL do cliente são avaliadas (com quote literal)
- [ ] Comprimento de cada passagem é medido contra benchmark 134-167 palavras
- [ ] Identificado se resposta directa aparece nos primeiros 40-60 palavras da secção
- [ ] Pelo menos 1 passagem "forte" e 1 "fraca" exemplificadas com texto real

❌ NOT delivery-ready: `O conteúdo não tem passagens citáveis claras. Recomendamos adicionar estatísticas e factos.`
✅ Delivery-ready: `Passagem fraca (saquei.pt/como-funciona): "O SAQUEI é uma plataforma inovadora que ajuda os portugueses a gerir melhor o seu dinheiro." — 18 palavras, sem dados, sem padrão "X is...", citability: 2/10. Passagem forte (saquei.pt/taxas): "O SAQUEI cobra 2,9% por transação, sem mensalidade. Para saque de €1.000 o custo total é €29." — 22 palavras, dado concreto, self-contained, citability: 8/10.`

---

### Gate 4 — Platform breakdown é diferenciado (não genérico para todas as plataformas)

- [ ] Google AIO, ChatGPT, Perplexity e Bing Copilot têm análise separada
- [ ] Cada plataforma tem probabilidade de citação baseada em sinais reais encontrados no site
- [ ] Presença em fontes-chave por plataforma é verificada (Wikipedia para ChatGPT 47.9%, Reddit para Perplexity 46.7%)
- [ ] Quick wins são ordenados por plataforma com maior ROI potencial para o cliente primeiro

❌ NOT delivery-ready: `O site tem potencial para aparecer em AI Overviews, ChatGPT e Perplexity com as melhorias recomendadas.`
✅ Delivery-ready: `ChatGPT visibility: BAIXA — Tributario.AI ausente na Wikipedia PT (47.9% das citações ChatGPT vêm de lá), 0 menções Reddit r/financaspessoais. Perplexity visibility: MÉDIA — 3 menções Reddit identificadas, sem thread própria. Google AIO: ALTA — ranking #4 para "irc portugal 2025", dentro dos top-10 que geram 92% das citações AIO.`

---

### Gate 5 — llms.txt e RSL 1.0 têm diagnóstico accionável

- [ ] Verificação real de `[domínio]/llms.txt` com resultado (200 OK / 404 / redirect)
- [ ] Se existir, conteúdo actual é avaliado contra formato padrão (secções, links, descrições)
- [ ] Se ausente, template mínimo funcional é gerado para o cliente (não descrito — escrito)
- [ ] RSL 1.0 status verificado; implicação para treino de modelos é explicada em 1 frase

❌ NOT delivery-ready: `Recomendamos criar um ficheiro llms.txt para melhorar a visibilidade em AI search.`
✅ Delivery-ready: `lusoconta.pt/llms.txt → 404. Template gerado: \`# LUSOconta\n> Conta bancária portuguesa sem comissões para emigrantes.\n## Principais páginas\n- [Como abrir conta](https://lusoconta.pt/abrir-conta): Processo 100% digital, 3 passos.\n- [Taxas e comissões](https://lusoconta.pt/taxas): Tabela comparativa actualizada 2026.\`  RSL 1.0: ausente — sem declaração machine-readable de licença, modelos podem excluir conteúdo por incerteza legal.`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero placeholders entre angle-brackets

- [ ] Nenhum `[client name]`, `[URL]`, `[inserir aqui]`, `<domain>` ou variante no output final
- [ ] Data de análise é explícita (ex: "fetch realizado 2026-02-14")
- [ ] Todas as métricas citadas (527% crescimento, correlação 0.737) são atribuídas à fonte original, não apresentadas como dados do cliente
- [ ] Nome do produto/marca do cliente aparece em cada secção do relatório

❌ NOT delivery-ready: `A análise de [CLIENT WEBSITE] mostra que [METRIC] precisa de melhorias.`
✅ Delivery-ready: `Análise Atrium.pt — GEO-ANALYSIS.md gerado 2026-02-14. Score 71/100. Citability 19/25 · Structural 15/20 · Multi-Modal 9/15 · Authority 16/20 · Technical 12/20.`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# GEO-ANALYSIS.md — Cuidai.pt
*Análise realizada: 2026-02-14 | Analista: DARIO seo-geo skill*

---

## GEO Readiness Score: 61/100

| Componente         | Peso | Score   | Evidência                                              |
|--------------------|------|---------|--------------------------------------------------------|
| Citability         | 25%  | 13/25   | Sem blocos self-contained; maior secção: 312 palavras  |
| Structural         | 20%  | 14/20   | H1→H2 correto; 0 FAQ sections; 0 tabelas comparativas  |
| Multi-Modal        | 15%  | 9/15    | 14 imagens (8 sem alt-text); 0 vídeos; 0 calculadoras |
| Authority          | 20%  | 13/20   | Sem Wikipedia; 2 menções Reddit; LinkedIn ativo        |
| Technical          | 20%  | 12/20   | GPTBot bloqueado; llms.txt ausente; SSR confirmado     |

**Benchmark:** Média sector healthtech PT = 58/100. Cuidai está ligeiramente acima.
**Gap para top quartile:** +17 pontos (necessário: 78/100).

---

## Platform Breakdown

### 🔵 Google AI Overviews — Probabilidade: MÉDIA (estimativa 35%)
- Ranking #6 para "cuidados domiciliários Lisboa" → dentro dos top-10 (92% AIO citations)
- Passagem mais citável encontrada: *"A Cuidai oferece cuidadores certificados em 48h, disponíveis 7 dias por semana em Lisboa e Porto."* (19 palavras — abaixo do óptimo 134-167, mas self-contained ✅)
- Bloqueador principal: secções de serviços em parágrafos densos sem headers de pergunta

### 🟠 ChatGPT Search — Probabilidade: BAIXA (estimativa 12%)
- Wikipedia PT: **ausente** (ChatGPT cita Wikipedia em 47.9% dos casos)
- Wikidata entity: **ausente**
- GPTBot: **Disallow** em robots.txt → bloqueio directo a indexação ChatGPT
- Acção prioritária: desbloquear GPTBot + criar stub Wikipedia "Cuidai (empresa)"

### 🟣 Perplexity — Probabilidade: MÉDIA-BAIXA (estimativa 22%)
- Reddit: 2 menções em r/portugal (thread "melhores cuidadores idosos LX 2024") ✅
- Sem presença em r/saudeportugal ou r/envelhecimento
- PerplexityBot: **ausente** em robots.txt (não bloqueado, mas não explicitamente permitido)
- Acção: adicionar `User-agent: PerplexityBot\nAllow: /`

### ⚪ Bing Copilot — Probabilidade: BAIXA (estimativa 18%)
- IndexNow: **não implementado**
- Bing Webmaster Tools: não verificado
- Autoridade de domínio Bing: DR equivalente 31 (abaixo do threshold recomendado 45+)

---

## Diagnóstico Técnico

### robots.txt (fetch 2026-02-14 — cuidai.pt/robots.txt)
```
User-agent: GPTBot
Disallow: /          ← ❌ BLOQUEIA ChatGPT Search (900M utilizadores)

User-agent: CCBot
Disallow: /          ← ✅ Correto (bloqueia treino Common Crawl)

# ClaudeBot, PerplexityBot, OAI-SearchBot — ausentes (zona cinzenta)
```

**Fix imediato** (adicionar ao robots.txt):
```
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /
```

### llms.txt — 404 Not Found
**Template gerado para implementação imediata:**
```
# Cuidai
> Plataforma portuguesa de cuidadores domiciliários certificados para idosos e
> pessoas com mobilidade reduzida. Operacional em Lisboa, Porto e Braga.

## Serviços principais
- [Cuidadores ao Domicílio](https://cuidai.pt/servicos): Disponibilidade 48h,
  certificação SNS validada.
- [Como funciona](https://cuidai.pt/como-funciona): Processo de 3 passos para
  contratar cuidador.
- [Preços e planos](https://cuidai.pt/precos): Tabela de preços por hora e
  pacotes mensais 2026.

## Factos-chave
- Fundada em 2021, Lisboa
- +1.200 cuidadores certificados na rede
- Cobertura: Lisboa, Porto, Braga, Setúbal
- Certificação: Segurança Social Portuguesa
```

### RSL 1.0 — Ausente
Sem declaração machine-readable de licença. Risco: modelos conservadores podem
omitir conteúdo Cuidai por incerteza legal. Recomendação: implementar RSL com
termo `ai-training: disallow, ai-search: allow`.

---

## Top 5 Quick Wins (ordenados por impacto/esforço)

| # | Acção | Impacto | Esforço | Plataforma |
|---|-------|---------|---------|------------|
| 1 | Desbloquear GPTBot no robots.txt | 🔴 Alto | 15 min | ChatGPT |
| 2 | Criar llms.txt (template acima) | 🔴 Alto | 1h | Todas |
| 3 | Reescrever 3 secções em blocos 134-167 palavras | 🟠 Médio | 3h | Google AIO |
| 4 | Adicionar FAQ com 5 perguntas reais de utilizadores | 🟠 Médio | 2h | Google AIO + Perplexity |
| 5 | Criar stub Wikipedia PT "Cuidai" | 🟡 Médio | 4h | ChatGPT |

---

## Passagens — Antes/Depois

**Passagem actual (fraca):**
> "A Cuidai é uma empresa inovadora no sector dos cuidados. Trabalhamos com
> profissionais de saúde para oferecer os melhores serviços."
*Citability: 2/10 — vago, sem dados, não self-contained.*

**Passagem reescrita (forte):**
> "A Cuidai disponibiliza cuidadores domiciliários certificados em até 48 horas
> em Lisboa, Porto e Braga. Todos os cuidadores passam por verificação de
> antecedentes e formação validada pela Segurança Social Portuguesa. O custo
> médio é €12-18/hora, sem taxas de subscrição."
*Citability: 9/10 — 47 palavras, resposta directa, dados concretos, self-contained.*
```

---

## Output anti-patterns

- Score arredondado suspeito: "60/100" ou "80/100" sem breakdown granular por componente
- Recomendação de llms.txt sem gerar o ficheiro real para o cliente (descrever ≠ entregar)
- Analisar robots.txt "em teoria" sem fazer fetch real ao URL do cliente
- Citar estatísticas do SKILL (527% crescimento, correlação 0.737) como se fossem métricas do site do cliente
- Platform breakdown idêntico para todas as plataformas ("recomendamos melhorar conteúdo para AIO, ChatGPT e Perplexity")
- Passagens de exemplo inventadas em vez de extraídas do URL real analisado
- Ausência de benchmark comparativo (score sem contexto de sector/concorrência é ruído)
- Quick wins sem estimativa de esforço — cliente não consegue priorizar
- Output com `[domain]`, `<client name>`, `[inserir URL]` ou qualquer placeholder não substituído
