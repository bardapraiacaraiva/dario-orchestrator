---
name: seo-schema
description: >
  Detect, validate, and generate Schema.org structured data. JSON-LD format
  preferred. Use when user says "schema", "structured data", "rich results",
  "JSON-LD", or "markup".
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

# Schema Markup Analysis & Generation

## Detection

1. Scan page source for JSON-LD `<script type="application/ld+json">`
2. Check for Microdata (`itemscope`, `itemprop`)
3. Check for RDFa (`typeof`, `property`)
4. Always recommend JSON-LD as primary format (Google's stated preference)

## Validation

- Check required properties per schema type
- Validate against Google's supported rich result types
- Test for common errors:
  - Missing @context
  - Invalid @type
  - Wrong data types
  - Placeholder text
  - Relative URLs (should be absolute)
  - Invalid date formats
- Flag deprecated types (see below)

## Schema Type Status (as of Feb 2026)

Read `references/schema-types.md` for the full list. Key rules:

### ACTIVE (recommend freely):
Organization, LocalBusiness, SoftwareApplication, WebApplication, Product (with Certification markup as of April 2025), ProductGroup, Offer, Service, Article, BlogPosting, NewsArticle, Review, AggregateRating, BreadcrumbList, WebSite, WebPage, Person, ProfilePage, ContactPage, VideoObject, ImageObject, Event, JobPosting, Course, DiscussionForumPosting

### VIDEO & SPECIALIZED (recommend freely):
BroadcastEvent, Clip, SeekToAction, SoftwareSourceCode

See `schema/templates.json` for ready-to-use JSON-LD templates for these types.

> **JSON-LD and JavaScript rendering:** Per Google's December 2025 JS SEO guidance, structured data injected via JavaScript may face delayed processing. For time-sensitive markup (especially Product, Offer), include JSON-LD in the initial server-rendered HTML.

### RESTRICTED (only for specific sites):
- **FAQ**: ONLY for government and healthcare authority sites (restricted Aug 2023)

### DEPRECATED (never recommend):
- **HowTo**: Rich results removed September 2023
- **SpecialAnnouncement**: Deprecated July 31, 2025
- **CourseInfo, EstimatedSalary, LearningVideo**: Retired June 2025
- **ClaimReview**: Retired from rich results June 2025
- **VehicleListing**: Retired from rich results June 2025
- **Practice Problem**: Retired from rich results late 2025
- **Dataset**: Retired from rich results late 2025
- **Book Actions**: Deprecated then reversed, still functional as of Feb 2026 (historical note)

## Generation

When generating schema for a page:
1. Identify page type from content analysis
2. Select appropriate schema type(s)
3. Generate valid JSON-LD with all required + recommended properties
4. Include only truthful, verifiable data. Use placeholders clearly marked for user to fill
5. Validate output before presenting

## Common Schema Templates

### Organization
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[Company Name]",
  "url": "[Website URL]",
  "logo": "[Logo URL]",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "[Phone]",
    "contactType": "customer service"
  },
  "sameAs": [
    "[Facebook URL]",
    "[LinkedIn URL]",
    "[Twitter URL]"
  ]
}
```

### LocalBusiness
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[Business Name]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Street]",
    "addressLocality": "[City]",
    "addressRegion": "[State]",
    "postalCode": "[ZIP]",
    "addressCountry": "US"
  },
  "telephone": "[Phone]",
  "openingHours": "Mo-Fr 09:00-17:00",
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[Lat]",
    "longitude": "[Long]"
  }
}
```

### Article/BlogPosting
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Title]",
  "author": {
    "@type": "Person",
    "name": "[Author Name]"
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "image": "[Image URL]",
  "publisher": {
    "@type": "Organization",
    "name": "[Publisher]",
    "logo": {
      "@type": "ImageObject",
      "url": "[Logo URL]"
    }
  }
}
```

## Output

- `SCHEMA-REPORT.md`: detection and validation results
- `generated-schema.json`: ready-to-use JSON-LD snippets

### Validation Results
| Schema | Type | Status | Issues |
|--------|------|--------|--------|
| ... | ... | ✅/⚠️/❌ | ... |

### Recommendations
- Missing schema opportunities
- Validation fixes needed
- Generated code for implementation

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable | Report connection error with status code. Suggest verifying URL and checking if the page requires authentication. |
| No schema markup found | Report that no JSON-LD, Microdata, or RDFa was detected. Recommend appropriate schema types based on page content analysis. |
| Invalid JSON-LD syntax | Parse and report specific syntax errors (missing brackets, trailing commas, unquoted keys). Provide corrected JSON-LD output. |
| Deprecated schema type detected | Flag the deprecated type with its retirement date. Recommend the current replacement type or advise removal if no replacement exists. |

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Schema types são válidos e não deprecated
- [ ] Nenhum schema gerado usa tipos deprecated (HowTo, SpecialAnnouncement, ClaimReview, VehicleListing, CourseInfo, EstimatedSalary, LearningVideo, Practice Problem, Dataset)
- [ ] FAQ schema só é recomendado se o site for governo ou saúde autoridade
- [ ] Tipos ACTIVE e VIDEO & SPECIALIZED usados corretamente para o contexto da página
- [ ] Retirement dates citadas quando se flagra tipo deprecated (ex: "HowTo removido em Setembro 2023")
- ❌ NOT delivery-ready: "Aqui está um FAQ schema para a vossa página de produto"
- ✅ Delivery-ready: "FAQ schema está restrito desde Agosto 2023 — apenas gov/saúde. Para a Cuidai, recomendo AggregateRating + Review no lugar."

### Gate 2 — JSON-LD sintaxe válida e completa
- [ ] `@context: "https://schema.org"` presente em cada bloco
- [ ] `@type` com valor reconhecido pelo Google Rich Results
- [ ] Sem trailing commas, sem chaves não fechadas, sem keys sem aspas
- [ ] URLs absolutas (não relativas: `/sobre` → `https://cuidai.pt/sobre`)
- [ ] Datas em formato ISO 8601 (`2025-04-15`, não "15 Abril 2025")
- ❌ NOT delivery-ready: `"datePublished": "April 2025"` ou `"url": "/pricing"`
- ✅ Delivery-ready: `"datePublished": "2025-04-15"`, `"url": "https://lusoconta.pt/precos"`

### Gate 3 — Propriedades required vs recommended declaradas
- [ ] Required properties para o tipo estão todas presentes (ex: Product precisa `name`; Offer precisa `price` + `priceCurrency`)
- [ ] Pelo menos 3 recommended properties incluídas para maximizar rich result eligibility
- [ ] Campos marcados como placeholder são claramente identificados com instrução ao cliente (ex: `"[URL do logo — substituir]"`)
- [ ] AggregateRating inclui `ratingValue`, `reviewCount`, e `bestRating`
- ❌ NOT delivery-ready: Offer gerado sem `price` nem `priceCurrency`
- ✅ Delivery-ready: `"price": "29.90", "priceCurrency": "EUR", "availability": "https://schema.org/InStock"`

### Gate 4 — Alinhamento com conteúdo da página (veracidade)
- [ ] Dados no schema correspondem ao conteúdo visível na página (Google penaliza schema enganoso)
- [ ] `name`, `description`, `telephone`, `address` verificados contra fonte real do cliente
- [ ] Nenhum valor inventado para preencher template — placeholders explícitos se dados não disponíveis
- [ ] Para Product/Offer time-sensitive: confirmado que JSON-LD está no HTML server-rendered (não injetado via JS)
- ❌ NOT delivery-ready: `"telephone": "+351 000 000 000"` ou rating `"ratingValue": "5"` sem reviews reais
- ✅ Delivery-ready: `"telephone": "+351 213 456 789"` confirmado no rodapé do site Atrium

### Gate 5 — SCHEMA-REPORT.md e generated-schema.json bem estruturados
- [ ] Tabela de validação preenchida com Status (✅/⚠️/❌) e Issues concretas por schema detectado
- [ ] Secção "Missing schema opportunities" com pelo menos 1 recomendação justificada
- [ ] `generated-schema.json` contém blocos prontos a copiar, sem erros de sintaxe
- [ ] Erros de conexão/sem markup reportados com cenário específico (status code, URL tentada)
- ❌ NOT delivery-ready: Tabela de validação vazia ou com "N/A" em todas as células
- ✅ Delivery-ready: `| LocalBusiness | LDogCare | ⚠️ | openingHours em formato inválido: "Mon-Fri" → usar "Mo-Fr" |`

### Gate 6 — Output usa CLIENT NAME + dados reais, sem angle-brackets por resolver
- [ ] Zero instâncias de `[Company Name]`, `[Phone]`, `[Logo URL]`, `[Author Name]` não substituídos no output final
- [ ] Nome do cliente aparece em `"name"`, `"publisher"`, `"legalName"` conforme aplicável
- [ ] sameAs URLs são os perfis reais do cliente (LinkedIn, Facebook, etc.), não placeholders
- [ ] Se dados não estão disponíveis, dito explicitamente: "Aguarda confirmação do telefone para preencher contactPoint"
- ❌ NOT delivery-ready: `"name": "[Business Name]"` entregue ao cliente sem substituição
- ✅ Delivery-ready: `"name": "Lisbon Dog Care"`, `"url": "https://lisbondogcare.pt"`, sameAs com Instagram real

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# SCHEMA-REPORT.md — Lisbon Dog Care

**URL analisada:** https://lisbondogcare.pt  
**Data análise:** 2025-11-03  
**Formato detectado:** Nenhum schema markup encontrado (zero JSON-LD, Microdata, RDFa)

---

## Validation Table

| Schema | Type | Status | Issues |
|--------|------|--------|--------|
| — | — | ❌ | Nenhum schema detectado na página principal |

---

## Missing Schema Opportunities

1. **LocalBusiness** — Negócio físico em Lisboa com morada, horários e telefone visíveis na página → elegível para rich result de negócio local no Google Maps e Search
2. **Service** — Páginas /passeios e /creche descrevem serviços com preço → adicionar Service com Offer aumenta CTR em resultados de serviços
3. **AggregateRating** — 47 reviews Google visíveis no widget embebido → importar para schema aumenta star snippet

---

## Generated Schema — generated-schema.json

### 1. LocalBusiness (página principal)

{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Lisbon Dog Care",
  "url": "https://lisbondogcare.pt",
  "logo": "https://lisbondogcare.pt/assets/logo-ldc.png",
  "image": "https://lisbondogcare.pt/assets/hero-dogs.jpg",
  "description": "Creche, hotel e passeios para cães em Lisboa. Equipa certificada, espaço exterior 300m².",
  "telephone": "+351 912 345 678",
  "email": "geral@lisbondogcare.pt",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Rua das Amoreiras, 42",
    "addressLocality": "Lisboa",
    "addressRegion": "Lisboa",
    "postalCode": "1250-020",
    "addressCountry": "PT"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 38.7223,
    "longitude": -9.1393
  },
  "openingHours": ["Mo-Fr 07:30-20:00", "Sa 08:00-18:00"],
  "priceRange": "€€",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "47",
    "bestRating": "5",
    "worstRating": "1"
  },
  "sameAs": [
    "https://www.instagram.com/lisbondogcare",
    "https://www.facebook.com/lisbondogcare",
    "https://g.page/lisbondogcare"
  ]
}

### 2. Service — Passeios Urbanos (página /passeios)

{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Passeios Urbanos para Cães — Lisboa",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Lisbon Dog Care",
    "url": "https://lisbondogcare.pt"
  },
  "areaServed": {
    "@type": "City",
    "name": "Lisboa"
  },
  "offers": {
    "@type": "Offer",
    "price": "15.00",
    "priceCurrency": "EUR",
    "availability": "https://schema.org/InStock",
    "url": "https://lisbondogcare.pt/passeios"
  }
}

---

## Notas de Implementação

- JSON-LD deve ser inserido no <head> do HTML server-rendered (não via JS)  
  → Per Google JS SEO guidance Dezembro 2025: markup injetado via JS pode ter delayed processing
- FAQ schema NÃO recomendado (restrito desde Agosto 2023 — apenas gov/saúde)
- Rever telephone e email com cliente antes de deploy — valores acima extraídos do rodapé do site
```

---

## Output anti-patterns

- Entregar JSON-LD com angle-brackets `[Company Name]` não substituídos — o cliente copia e publica schema inválido
- Recomendar FAQ schema para e-commerce, SaaS ou serviços locais — restrito desde Agosto 2023
- Usar HowTo, ClaimReview ou SpecialAnnouncement sem alertar que foram deprecated/retired
- Gerar `"datePublished": "2025"` ou `"telephone": "00000"` — datas e contactos têm de ser verídicos
- Omitir `@context` ou usar URL relativa no `@context` (ex: `"schema.org"` em vez de `"https://schema.org"`)
- Colocar JSON-LD numa nota "para implementar via Google Tag Manager" sem alertar risco de delayed processing para Product/Offer
- Validar visualmente sem verificar se `ratingValue` e `reviewCount` correspondem a reviews reais visíveis na página
- Gerar schema para tipo certo mas página errada (ex: Article schema na homepage corporativa)
- Listar "oportunidades de schema" sem justificar qual rich result se torna elegível e porquê vale a pena
- Ignorar a presença de Microdata ou RDFa legado — sempre reportar e recomendar migração para JSON-LD
