---
name: seo-competitor-pages
description: >
  Generate SEO-optimized competitor comparison and alternatives pages. Covers
  "X vs Y" layouts, "alternatives to X" pages, feature matrices, schema markup,
  and conversion optimization. Use when user says "comparison page", "vs page",
  "alternatives page", "competitor comparison", or "X vs Y".
user-invokable: true
argument-hint: "[url or generate] [competitor]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# Competitor Comparison & Alternatives Pages

Create high-converting comparison and alternatives pages that target
competitive intent keywords with accurate, structured content.

## Page Types

### 1. "X vs Y" Comparison Pages
- Direct head-to-head comparison between two products/services
- Balanced feature-by-feature analysis
- Clear verdict or recommendation with justification
- Target keyword: `[Product A] vs [Product B]`

### 2. "Alternatives to X" Pages
- List of alternatives to a specific product/service
- Each alternative with brief summary, pros/cons, best-for use case
- Target keyword: `[Product] alternatives`, `best alternatives to [Product]`

### 3. "Best [Category] Tools" Roundup Pages
- Curated list of top tools/services in a category
- Ranking criteria clearly stated
- Target keyword: `best [category] tools [year]`, `top [category] software`

### 4. Comparison Table Pages
- Feature matrix with multiple products in columns
- Sortable/filterable if interactive
- Target keyword: `[category] comparison`, `[category] comparison chart`

## Comparison Table Generation

### Feature Matrix Layout
```
| Feature          | Your Product | Competitor A | Competitor B |
|------------------|:------------:|:------------:|:------------:|
| Feature 1        | ✅           | ✅           | ❌           |
| Feature 2        | ✅           | ⚠️ Partial   | ✅           |
| Feature 3        | ✅           | ❌           | ❌           |
| Pricing (from)   | $X/mo        | $Y/mo        | $Z/mo        |
| Free Tier        | ✅           | ❌           | ✅           |
```

### Data Accuracy Requirements
- All feature claims must be verifiable from public sources
- Pricing must be current (include "as of [date]" note)
- Update frequency: review quarterly or when competitors ship major changes
- Link to source for each competitor data point where possible

## Schema Markup Recommendations

### Product Schema with AggregateRating
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "[Product Name]",
  "description": "[Product Description]",
  "brand": {
    "@type": "Brand",
    "name": "[Brand Name]"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[Rating]",
    "reviewCount": "[Count]",
    "bestRating": "5",
    "worstRating": "1"
  }
}
```

### SoftwareApplication (for software comparisons)
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "[Software Name]",
  "applicationCategory": "[Category]",
  "operatingSystem": "[OS]",
  "offers": {
    "@type": "Offer",
    "price": "[Price]",
    "priceCurrency": "USD"
  }
}
```

### ItemList (for roundup pages)
```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Best [Category] Tools [Year]",
  "itemListOrder": "https://schema.org/ItemListOrderDescending",
  "numberOfItems": "[Count]",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "[Product Name]",
      "url": "[Product URL]"
    }
  ]
}
```

## Keyword Targeting

### Comparison Intent Patterns
| Pattern | Example | Search Volume Signal |
|---------|---------|---------------------|
| `[A] vs [B]` | "Slack vs Teams" | High |
| `[A] alternative` | "Figma alternatives" | High |
| `[A] alternatives [year]` | "Notion alternatives 2026" | High |
| `best [category] tools` | "best project management tools" | High |
| `[A] vs [B] for [use case]` | "AWS vs Azure for startups" | Medium |
| `[A] review [year]` | "Monday.com review 2026" | Medium |
| `[A] vs [B] pricing` | "HubSpot vs Salesforce pricing" | Medium |
| `is [A] better than [B]` | "is Notion better than Confluence" | Medium |

### Title Tag Formulas
- X vs Y: `[A] vs [B]: [Key Differentiator] ([Year])`
- Alternatives: `[N] Best [A] Alternatives in [Year] (Free & Paid)`
- Roundup: `[N] Best [Category] Tools in [Year], Compared & Ranked`

### H1 Patterns
- Match title tag intent
- Include primary keyword naturally
- Keep under 70 characters

## Conversion-Optimized Layouts

### CTA Placement
- **Above fold**: Brief comparison summary with primary CTA
- **After comparison table**: "Try [Your Product] free" CTA
- **Bottom of page**: Final recommendation with CTA
- Avoid aggressive CTAs in competitor description sections (reduces trust)

### Social Proof Sections
- Customer testimonials relevant to comparison criteria
- G2/Capterra/TrustPilot ratings (with source links)
- Case studies showing migration from competitor
- "Switched from [Competitor]" stories

### Pricing Highlights
- Clear pricing comparison table
- Highlight value advantages (not just lowest price)
- Include hidden costs (setup fees, per-user pricing, overage charges)
- Link to full pricing page

### Trust Signals
- "Last updated [date]" timestamp
- Author with relevant expertise
- Methodology disclosure (how comparisons were conducted)
- Disclosure of own product affiliation

## Fairness Guidelines

- **Accuracy**: All competitor information must be verifiable from public sources
- **No defamation**: Never make false or misleading claims about competitors
- **Cite sources**: Link to competitor websites, review sites, or documentation
- **Timely updates**: Review and update when competitors release major changes
- **Disclose affiliation**: Clearly state which product is yours
- **Balanced presentation**: Acknowledge competitor strengths honestly
- **Pricing accuracy**: Include "as of [date]" disclaimers on all pricing data
- **Feature verification**: Test competitor features where possible, cite documentation otherwise

## Internal Linking

- Link to your own product/service pages from comparison sections
- Cross-link between related comparison pages (e.g., "A vs B" links to "A vs C")
- Link to feature-specific pages when discussing individual features
- Breadcrumb: Home > Comparisons > [This Page]
- Related comparisons section at bottom of page
- Link to case studies and testimonials mentioned in the comparison

## Output

### Comparison Page Template
- `COMPARISON-PAGE.md`: Ready-to-implement page structure with sections
- Feature matrix table
- Content outline with word count targets (minimum 1,500 words)

### Schema Markup
- `comparison-schema.json`: Product/SoftwareApplication/ItemList JSON-LD

### Keyword Strategy
- Primary and secondary keywords
- Related long-tail opportunities
- Content gaps vs existing competitor pages

### Recommendations
- Content improvements for existing comparison pages
- New comparison page opportunities
- Schema markup additions
- Conversion optimization suggestions

## Error Handling

| Scenario | Action |
|----------|--------|
| Competitor URL unreachable | Report which competitor URLs failed. Proceed with available data and note gaps in the comparison. |
| Insufficient competitor data (pricing, features unavailable) | Flag missing data points clearly. Use "Not publicly available" in comparison tables rather than guessing. |
| No product/service overlap found | Report that the products serve different markets. Suggest alternative competitors that share feature overlap, or pivot to a category roundup format. |

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

---

### Gate 1 — Estrutura e tipo de página corretos

- [ ] O tipo de página (vs / alternatives / roundup / comparison table) está explicitamente escolhido e aplicado
- [ ] H1 segue o pattern correto para o tipo (ex: `[N] Best [A] Alternatives in [Year]`)
- [ ] Title tag tem ≤ 60 chars e inclui ano atual ou diferenciador chave
- [ ] Secções above-fold, tabela, social proof e CTA final estão todas presentes

❌ NOT delivery-ready: `"Comparação de ferramentas de gestão de projetos"` — sem ano, sem padrão de intent, sem N produtos
✅ Delivery-ready: `"Cuidai vs Noona: Qual o melhor software de gestão para pet services em 2025"` — tipo explícito, diferenciador, ano

---

### Gate 2 — Tabela de features completa e verificável

- [ ] Todos os concorrentes na tabela têm linha de pricing com data ("as of Jun 2025")
- [ ] Cada ✅/❌/⚠️ é suportável por URL público (site oficial, G2, Capterra)
- [ ] Free tier / trial confirmado ou negado para cada produto
- [ ] Nenhuma célula contém "N/A" sem explicação — omissão injustificada quebra confiança

❌ NOT delivery-ready: `| Faturação automática | ✅ | ❌ |` — sem fonte, sem data de verificação
✅ Delivery-ready: `| Faturação automática | ✅ | ❌ (confirmado em livebeam.io/pricing, Jun 2025) |`

---

### Gate 3 — Schema markup preenchido e válido

- [ ] Tipo de schema correto para o page type: `Product` + `AggregateRating` para vs-pages, `ItemList` para roundups
- [ ] Zero angle-brackets `<>` ou placeholders `[Rating]` no JSON-LD final
- [ ] `ratingValue`, `reviewCount` e `url` têm valores reais ou são omitidos (não inventados)
- [ ] Schema testável em schema.org/validator sem erros críticos

❌ NOT delivery-ready: `"ratingValue": "[Rating]", "reviewCount": "[Count]"` — placeholder não substitui dado real
✅ Delivery-ready: `"ratingValue": "4.7", "reviewCount": "312"` — baseado em G2 para SAQUEI, extraído Jun 2025

---

### Gate 4 — Keyword targeting e SEO on-page

- [ ] Keyword primária (ex: `alternativas ao Holded 2025`) aparece em H1, title tag e primeiro parágrafo
- [ ] Pelo menos 2 variantes de long-tail cobertas em H2/H3 (ex: `Holded vs Sage pricing`, `melhor alternativa ao Holded para freelancers`)
- [ ] Meta description ≤ 155 chars com keyword + CTA implícito
- [ ] Não há keyword stuffing — densidade natural, sem repetição mecânica em cada frase

❌ NOT delivery-ready: H1 = `"As melhores ferramentas"` — zero keyword de comparação, indexação genérica
✅ Delivery-ready: H1 = `"7 Melhores Alternativas ao Holded em 2025 (Grátis e Pagas)"` — pattern correto, keyword exata, N explícito

---

### Gate 5 — Fairness, trust signals e divulgação de afiliação

- [ ] Secção "Metodologia" ou nota de rodapé explica como a comparação foi conduzida
- [ ] Afiliação ao produto próprio declarada (ex: "Este artigo é publicado pela equipa da LUSOconta")
- [ ] "Last updated [data real]" visível no topo ou imediatamente abaixo do H1
- [ ] Pontos fortes dos concorrentes estão genuinamente representados (mínimo 1 pro real por concorrente)

❌ NOT delivery-ready: Comparação sem data, sem autor, onde o concorrente só tem ❌ em tudo — parece propaganda
✅ Delivery-ready: `"Atualizado em 15 Jun 2025 pela equipa Tributario.AI | Metodologia: testamos planos pagos de cada ferramenta durante 14 dias"`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem placeholders angle-brackets

- [ ] Nenhum `[Product Name]`, `[Brand Name]`, `[URL]`, `[Year]`, `[Price]` por preencher no output final
- [ ] Nome do cliente ou produto aparece no H1, title tag e pelo menos 2 CTAs
- [ ] Preços têm valores numéricos reais com moeda (€/$ explícito) e data
- [ ] URLs de schema e links de social proof são URLs reais (não `example.com` ou `[competitor-url]`)

❌ NOT delivery-ready: `"Try [Your Product] free — switch from [Competitor] today"`
✅ Delivery-ready: `"Experimenta a ARRECADA.GOV gratuitamente — já migrámos 340 câmaras do sistema anterior"`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
---
title: "Cuidai vs Pawfinity: Qual o Melhor Software para Pet Shops em 2025"
meta_description: "Comparámos Cuidai e Pawfinity em preço, funcionalidades e suporte. Vê qual se adapta melhor ao teu negócio de pet services em 2025."
last_updated: "18 Jun 2025"
author: "Equipa Cuidai (produto próprio — divulgação completa em rodapé)"
schema_type: "Product + AggregateRating"
---

# Cuidai vs Pawfinity: Qual o Melhor Software para Pet Shops em 2025

> Atualizado em 18 Jun 2025 · Testado em planos pagos · Este artigo é publicado
> pela equipa da Cuidai — vê a nossa política de transparência no rodapé.

**Resumo rápido:** Se geres um pet shop ou grooming studio em Portugal, o Cuidai
inclui faturação SAF-T integrada e suporte em PT desde o plano base (€19/mês).
O Pawfinity é mais forte em gestão de boarding multilocal, mas não tem localização
fiscal portuguesa — requer integração manual com contabilista.

---

## Comparação rápida

| Feature                        | Cuidai        | Pawfinity         |
|-------------------------------|:-------------:|:-----------------:|
| Agendamento online             | ✅            | ✅                |
| App móvel (iOS + Android)      | ✅            | ✅                |
| Faturação SAF-T (Portugal)     | ✅            | ❌                |
| Gestão de boarding multilocal  | ⚠️ 1 unidade  | ✅ ilimitado      |
| Lembretes SMS automáticos      | ✅            | ✅ (add-on +$15)  |
| Relatórios de receita          | ✅            | ✅                |
| Suporte em Português           | ✅            | ❌ (EN only)      |
| Preço base (as of Jun 2025)    | €19/mês       | $29/mês (~€27)    |
| Free trial                     | 14 dias       | 14 dias           |

*Fontes: cuidai.pt/precos (Jun 2025), pawfinity.com/pricing (Jun 2025)*

---

## Análise detalhada

### Agendamento e calendário

O **Cuidai** oferece calendário visual com drag-and-drop, confirmações automáticas
por email e SMS incluídas no plano base. Testado internamente em Jun 2025 com
simulação de 3 funcionários simultâneos — sem conflitos de agenda detetados.

O **Pawfinity** tem calendário igualmente robusto e destaca-se na gestão de
múltiplos boarders ao mesmo tempo. Para pet shops com apenas um espaço físico,
a vantagem é marginal.

### Faturação e conformidade fiscal

**Ponto crítico para negócios em Portugal:** o Cuidai gera faturas SAF-T/AT
automaticamente, cumprindo a obrigação legal da AT sem passos manuais. O
Pawfinity não tem esta integração — requer exportação manual e software de
contabilidade adicional (ex: Moloni, €15/mês extra).

### Suporte ao cliente

- Cuidai: chat em PT, resposta média < 4h (testado Jun 2025), base de ajuda PT
- Pawfinity: email EN, resposta média 24-48h (fonte: Capterra reviews, Jun 2025)

---

## O que os utilizadores dizem

> "Migrámos do Pawfinity para o Cuidai em março de 2025. A faturação automática
> poupou-nos 3h por semana." — Ana Costa, Petshop Estrela, Lisboa ⭐⭐⭐⭐⭐

Cuidai no Capterra: **4.8/5** (127 reviews, Jun 2025)
Pawfinity no Capterra: **4.6/5** (89 reviews, Jun 2025)

---

## Veredicto

**Escolhe o Cuidai se:** o teu negócio está em Portugal e precisas de conformidade
fiscal SAF-T sem esforço extra, suporte em português e preço mais acessível.

**Escolhe o Pawfinity se:** tens múltiplas unidades de boarding, operas
internacionalmente e a conformidade fiscal portuguesa não é requisito.

[Experimenta o Cuidai grátis 14 dias →](https://cuidai.pt/registo)

---

*Metodologia: Testámos ambas as plataformas em planos pagos durante 14 dias em
Mai–Jun 2025. Preços verificados nos sites oficiais a 18 Jun 2025. Este artigo
é publicado pela Cuidai; mantemos padrões editoriais de precisão sobre
concorrentes.*
```

---

## Output anti-patterns

- **Placeholders não substituídos** — entregar com `[Product Name]`, `[Rating]` ou `[Year]` no corpo do output
- **Tabela de features sem fontes** — ✅/❌ sem URL ou data de verificação são acusações não verificáveis
- **Schema JSON-LD com valores inventados** — `"ratingValue": "4.9"` sem base real em G2/Capterra/Trustpilot
- **Concorrentes só com ❌** — nenhum produto real é fraco em tudo; ausência de pros sinaliza parcialidade e destrói SEO de confiança
- **Preços sem data nem moeda** — `"$29/mês"` sem "as of Jun 2025" fica desatualizado e cria risco legal
- **Title tag sem ano e sem diferenciador** — `"Cuidai vs Pawfinity"` perde para `"Cuidai vs Pawfinity: Faturação SAF-T em 2025"`
- **CTA agressivo na secção do concorrente** — colocar "Muda já!" na descrição do rival reduz credibilidade editorial
- **Zero disclosure de afiliação** — omitir que o autor é o próprio produto viola diretrizes de transparência Google e GDPR
- **Meta description > 155 chars** — truncada no SERP, desperdiça o único espaço de copy no resultado de pesquisa
