---
name: seo-hreflang
description: >
  Hreflang and international SEO audit, validation, and generation. Detects
  common mistakes, validates language/region codes, and generates correct
  hreflang implementations. Use when user says "hreflang", "i18n SEO",
  "international SEO", "multi-language", "multi-region", or "language tags".
user-invokable: true
argument-hint: "[url]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# Hreflang & International SEO

Validate existing hreflang implementations or generate correct hreflang tags
for multi-language and multi-region sites. Supports HTML, HTTP header, and
XML sitemap implementations.

## Validation Checks

### 1. Self-Referencing Tags
- Every page must include an hreflang tag pointing to itself
- The self-referencing URL must exactly match the page's canonical URL
- Missing self-referencing tags cause Google to ignore the entire hreflang set

### 2. Return Tags
- If page A links to page B with hreflang, page B must link back to page A
- Every hreflang relationship must be bidirectional (A→B and B→A)
- Missing return tags invalidate the hreflang signal for both pages
- Check all language versions reference each other (full mesh)

### 3. x-default Tag
- Required: designates the fallback page for unmatched languages/regions
- Typically points to the language selector page or English version
- Only one x-default per set of alternates
- Must also have return tags from all other language versions

### 4. Language Code Validation
- Must use ISO 639-1 two-letter codes (e.g., `en`, `fr`, `de`, `ja`)
- Common errors:
  - `eng` instead of `en` (ISO 639-2, not valid for hreflang)
  - `jp` instead of `ja` (incorrect code for Japanese)
  - `zh` without region qualifier (ambiguous; use `zh-Hans` or `zh-Hant`)

### 5. Region Code Validation
- Optional region qualifier uses ISO 3166-1 Alpha-2 (e.g., `en-US`, `en-GB`, `pt-BR`)
- Format: `language-REGION` (lowercase language, uppercase region)
- Common errors:
  - `en-uk` instead of `en-GB` (UK is not a valid ISO 3166-1 code)
  - `es-LA` (Latin America is not a country; use specific countries)
  - Region without language prefix

### 6. Canonical URL Alignment
- Hreflang tags must only appear on canonical URLs
- If a page has `rel=canonical` pointing elsewhere, hreflang on that page is ignored
- The canonical URL and hreflang URL must match exactly (including trailing slashes)
- Non-canonical pages should not be in any hreflang set

### 7. Protocol Consistency
- All URLs in an hreflang set must use the same protocol (HTTPS or HTTP)
- Mixed HTTP/HTTPS in hreflang sets causes validation failures
- After HTTPS migration, update all hreflang tags to HTTPS

### 8. Cross-Domain Support
- Hreflang works across different domains (e.g., example.com and example.de)
- Cross-domain hreflang requires return tags on both domains
- Verify both domains are verified in Google Search Console
- Sitemap-based implementation recommended for cross-domain setups

## Common Mistakes

| Issue | Severity | Fix |
|-------|----------|-----|
| Missing self-referencing tag | Critical | Add hreflang pointing to same page URL |
| Missing return tags (A→B but no B→A) | Critical | Add matching return tags on all alternates |
| Missing x-default | High | Add x-default pointing to fallback/selector page |
| Invalid language code (e.g., `eng`) | High | Use ISO 639-1 two-letter codes |
| Invalid region code (e.g., `en-uk`) | High | Use ISO 3166-1 Alpha-2 codes |
| Hreflang on non-canonical URL | High | Move hreflang to canonical URL only |
| HTTP/HTTPS mismatch in URLs | Medium | Standardize all URLs to HTTPS |
| Trailing slash inconsistency | Medium | Match canonical URL format exactly |
| Hreflang in both HTML and sitemap | Low | Choose one method (sitemap preferred for large sites) |
| Language without region when needed | Low | Add region qualifier for geo-targeted content |

## Implementation Methods

### Method 1: HTML Link Tags
Best for: Sites with <50 language/region variants per page.

```html
<link rel="alternate" hreflang="en-US" href="https://example.com/page" />
<link rel="alternate" hreflang="en-GB" href="https://example.co.uk/page" />
<link rel="alternate" hreflang="fr" href="https://example.com/fr/page" />
<link rel="alternate" hreflang="x-default" href="https://example.com/page" />
```

Place in `<head>` section. Every page must include all alternates including itself.

### Method 2: HTTP Headers
Best for: Non-HTML files (PDFs, documents).

```
Link: <https://example.com/page>; rel="alternate"; hreflang="en-US",
      <https://example.com/fr/page>; rel="alternate"; hreflang="fr",
      <https://example.com/page>; rel="alternate"; hreflang="x-default"
```

Set via server configuration or CDN rules.

### Method 3: XML Sitemap (Recommended for large sites)
Best for: Sites with many language variants, cross-domain setups, or 50+ pages.

See Hreflang Sitemap Generation section below.

### Method Comparison
| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| HTML link tags | Small sites (<50 variants) | Easy to implement, visible in source | Bloats `<head>`, hard to maintain at scale |
| HTTP headers | Non-HTML files | Works for PDFs, images | Complex server config, not visible in HTML |
| XML sitemap | Large sites, cross-domain | Scalable, centralized management | Not visible on page, requires sitemap maintenance |

## Hreflang Generation

### Process
1. **Detect languages**: Scan site for language indicators (URL path, subdomain, TLD, HTML lang attribute)
2. **Map page equivalents**: Match corresponding pages across languages/regions
3. **Validate language codes**: Verify all codes against ISO 639-1 and ISO 3166-1
4. **Generate tags**: Create hreflang tags for each page including self-referencing
5. **Verify return tags**: Confirm all relationships are bidirectional
6. **Add x-default**: Set fallback for each page set
7. **Output**: Generate implementation code (HTML, HTTP headers, or sitemap XML)

## Hreflang Sitemap Generation

### Sitemap with Hreflang
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://example.com/page</loc>
    <xhtml:link rel="alternate" hreflang="en-US" href="https://example.com/page" />
    <xhtml:link rel="alternate" hreflang="fr" href="https://example.com/fr/page" />
    <xhtml:link rel="alternate" hreflang="de" href="https://example.de/page" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/page" />
  </url>
  <url>
    <loc>https://example.com/fr/page</loc>
    <xhtml:link rel="alternate" hreflang="en-US" href="https://example.com/page" />
    <xhtml:link rel="alternate" hreflang="fr" href="https://example.com/fr/page" />
    <xhtml:link rel="alternate" hreflang="de" href="https://example.de/page" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/page" />
  </url>
</urlset>
```

Key rules:
- Include the `xmlns:xhtml` namespace declaration
- Every `<url>` entry must include ALL language alternates (including itself)
- Each alternate must appear as a separate `<url>` entry with its own full set
- Split at 50,000 URLs per sitemap file

## Output

### Hreflang Validation Report

#### Summary
- Total pages scanned: XX
- Language variants detected: XX
- Issues found: XX (Critical: X, High: X, Medium: X, Low: X)

#### Validation Results
| Language | URL | Self-Ref | Return Tags | x-default | Status |
|----------|-----|----------|-------------|-----------|--------|
| en-US | https://... | ✅ | ✅ | ✅ | ✅ |
| fr | https://... | ❌ | ⚠️ | ✅ | ❌ |
| de | https://... | ✅ | ❌ | ✅ | ❌ |

### Generated Hreflang Tags
- HTML `<link>` tags (if HTML method chosen)
- HTTP header values (if header method chosen)
- `hreflang-sitemap.xml` (if sitemap method chosen)

### Recommendations
- Missing implementations to add
- Incorrect codes to fix
- Method migration suggestions (e.g., HTML to sitemap for scale)

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable (DNS failure, connection refused) | Report the error clearly. Do not guess site structure. Suggest the user verify the URL and try again. |
| No hreflang tags found | Report the absence. Check for other internationalization signals (subdirectories, subdomains, ccTLDs) and recommend the appropriate hreflang implementation method. |
| Invalid language/region codes detected | List each invalid code with the correct replacement. Provide a corrected hreflang tag set ready to implement. |

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Códigos de língua e região são ISO-válidos
- [ ] Todos os `hreflang` usam ISO 639-1 (2 letras: `en`, `fr`, `pt`) — nunca `eng`, `jp`, `por`
- [ ] Qualificadores de região usam ISO 3166-1 Alpha-2 em maiúsculas: `pt-BR`, `en-GB`, `zh-Hant` — nunca `en-uk`, `es-LA`
- [ ] `zh` sempre qualificado (`zh-Hans` ou `zh-Hant`) — nunca nu
- ❌ NOT delivery-ready: `hreflang="pt"` numa página que serve exclusivamente o mercado brasileiro
- ✅ Delivery-ready: `hreflang="pt-BR"` em `https://luso conta.com.br/conta-digital` + `hreflang="pt-PT"` em `https://lusoconta.pt/conta-digital`

### Gate 2 — Self-referencing tag presente em cada página
- [ ] Cada URL do set inclui um `<link rel="alternate" hreflang="xx-XX" href="[própria URL]" />`
- [ ] A URL da self-reference corresponde **exactamente** ao canonical (trailing slash, protocolo, subdomínio)
- [ ] Verificado em pelo menos 3 páginas distintas do site (homepage, produto, blog)
- ❌ NOT delivery-ready: página `https://cuidai.pt/servicos` sem tag apontando para si mesma
- ✅ Delivery-ready: `<link rel="alternate" hreflang="pt-PT" href="https://cuidai.pt/servicos" />` presente no `<head>` de `https://cuidai.pt/servicos`

### Gate 3 — Return tags formam malha completa (full mesh)
- [ ] Para cada par A↔B, a tag existe em A apontando para B **e** em B apontando para A
- [ ] `x-default` tem return tags de **todas** as variantes de língua/região
- [ ] Número de tags em cada página = número total de variantes (incluindo x-default)
- ❌ NOT delivery-ready: `saquei.pt` tem tag para `saquei.com/en` mas `saquei.com/en` não referencia `saquei.pt`
- ✅ Delivery-ready: 4 variantes (`pt-PT`, `pt-BR`, `en`, `x-default`) → cada página tem exactamente 4 tags, auditadas em todas as URLs do set

### Gate 4 — Alinhamento com canonical e protocolo único
- [ ] Nenhuma página com `rel=canonical` apontando para outro URL tem tags hreflang
- [ ] Todas as URLs do set usam HTTPS — zero mixed HTTP/HTTPS
- [ ] Trailing slash consistente em todo o set (ou sempre com `/` ou nunca)
- ❌ NOT delivery-ready: `http://atrium.pt/en/` no hreflang enquanto canonical é `https://atrium.pt/en`
- ✅ Delivery-ready: todos os 6 URLs do set de `atrium.pt` usam `https://` sem trailing slash, verificado por inspecção de source e headers

### Gate 5 — Método de implementação justificado e correcto
- [ ] Método escolhido (HTML / HTTP header / XML sitemap) está documentado com justificação
- [ ] Para sites >50 variantes ou cross-domain: XML sitemap obrigatório, com `<xhtml:link>` correcto
- [ ] Não existe duplicação entre métodos (HTML tags **e** sitemap simultaneamente) sem aviso explícito
- ❌ NOT delivery-ready: site com 3 domínios TLD (`tributario.ai`, `.pt`, `.br`) implementado só via HTML tags sem justificação
- ✅ Delivery-ready: "Recomendado XML sitemap — site cross-domain (3 TLDs) com 120+ páginas; HTML tags removidas do `<head>` para evitar conflito"

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder
- [ ] Zero instâncias de `<url>`, `<language>`, `<site>`, `[INSERT]`, `example.com` no output final
- [ ] URLs são os reais do cliente (verificados por WebFetch ou fornecidos pelo utilizador)
- [ ] Códigos de língua são os reais das páginas existentes, não genéricos de template
- ❌ NOT delivery-ready: `<link rel="alternate" hreflang="<language>" href="<your-url>" />`
- ✅ Delivery-ready: `<link rel="alternate" hreflang="pt-PT" href="https://lusoconta.pt/abrir-conta" />`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via fetch da página / sitemap / HTTP headers analisados nesta sessão
- 🟡 **assumed** — plausível com base nos padrões ISO/Google, mas precisa confirmação do cliente antes de entregar
- 🟢 **projection** — impacto estimado por design (não verificável sem dados reais de Search Console)

Output checklist upfront mostra ao leitor exactamente o que é trust-as-is vs o que precisa de verificação. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready:
```
en-GB implementado em example.co.uk — return tags presentes — impacto esperado: +30% impressões UK
```
*(reader assume que tudo foi verificado ao vivo; impacto não tem label; return tags nunca foram confirmadas no domínio remoto)*

✅ Delivery-ready:
- 🔵 **verified** — `hreflang="en-US"` com self-referencing tag presente em `https://example.com/page` (fetched via WebFetch desta sessão)
- 🟡 **assumed** — return tags em `https://example.co.uk/page` apontam de volta para `en-US`; não foi possível fazer fetch ao domínio `.co.uk` — cliente deve confirmar antes de publicar
- 🟡 **assumed** — `x-default` aponta para `/en/` com base na estrutura de URLs observada; confirmar se é o language selector pretendido
- 🟢 **projection** — corrigir missing return tags deverá resolver invalidação do hreflang set e melhorar cobertura indexada (estimativa baseada em padrões Google — validar via GSC após deploy)

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — return tags verificadas em todos os domínios alternativos (fetch directo ou cliente confirma via GSC / screaming frog)
- [ ] All 🔵 citations added — URLs fetched e códigos ISO validados referenciados no relatório final
- [ ] All 🟢 projections labeled as such ao cliente — impactos de indexação apresentados como estimativas, não garantias

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## Auditoria Hreflang — LUSOconta (lusoconta.pt + lusoconta.com.br)

**Data:** 2025-06-10  
**Páginas auditadas:** Homepage, /abrir-conta, /tarifario, /contactos  
**Método actual:** HTML link tags  
**Erros encontrados:** 3 críticos, 1 médio

---

### Erros Críticos Detectados

#### 1. Missing return tags — `lusoconta.com.br` não referencia `lusoconta.pt`
`lusoconta.pt/abrir-conta` tem:
```html
<link rel="alternate" hreflang="pt-PT" href="https://lusoconta.pt/abrir-conta" />
<link rel="alternate" hreflang="pt-BR" href="https://lusoconta.com.br/abrir-conta" />
<link rel="alternate" hreflang="x-default" href="https://lusoconta.pt/abrir-conta" />
```
`lusoconta.com.br/abrir-conta` tem apenas:
```html
<link rel="alternate" hreflang="pt-BR" href="https://lusoconta.com.br/abrir-conta" />
```
**Fix:** Adicionar em `lusoconta.com.br/abrir-conta`:
```html
<link rel="alternate" hreflang="pt-PT" href="https://lusoconta.pt/abrir-conta" />
<link rel="alternate" hreflang="pt-BR" href="https://lusoconta.com.br/abrir-conta" />
<link rel="alternate" hreflang="x-default" href="https://lusoconta.pt/abrir-conta" />
```

#### 2. Missing self-referencing tag — `/tarifario` (pt-BR)
`lusoconta.com.br/tarifario` não inclui tag apontando para si mesma.  
Google ignora o set completo desta página.

#### 3. Código inválido — `hreflang="pt"` em vez de `hreflang="pt-BR"`
Encontrado em `lusoconta.com.br/contactos`. Código `pt` sem qualificador
é ambíguo entre mercado PT e BR.

---

### Erro Médio

#### 4. Trailing slash inconsistente
- `lusoconta.pt/abrir-conta` (sem slash) referencia `lusoconta.com.br/abrir-conta/` (com slash)
- Canonical de `.com.br` é sem slash → mismatch

---

### Implementação Corrigida — Página `/abrir-conta`

**Em `lusoconta.pt/abrir-conta`** (sem alterações estruturais, já correcto):
```html
<link rel="alternate" hreflang="pt-PT" href="https://lusoconta.pt/abrir-conta" />
<link rel="alternate" hreflang="pt-BR" href="https://lusoconta.com.br/abrir-conta" />
<link rel="alternate" hreflang="x-default" href="https://lusoconta.pt/abrir-conta" />
```

**Em `lusoconta.com.br/abrir-conta`** (corrigido):
```html
<link rel="alternate" hreflang="pt-PT" href="https://lusoconta.pt/abrir-conta" />
<link rel="alternate" hreflang="pt-BR" href="https://lusoconta.com.br/abrir-conta" />
<link rel="alternate" hreflang="x-default" href="https://lusoconta.pt/abrir-conta" />
```

---

### Recomendação de Método

Site cross-domain (2 TLDs: `.pt` + `.com.br`) com 40 páginas actuais.  
**Manter HTML tags** é viável agora. Se o site crescer para >80 páginas,  
migrar para **XML sitemap centralizado** em `lusoconta.pt/sitemap-hreflang.xml`.

---

### Checklist de Validação Pós-Fix

- [x] ISO 639-1 + ISO 3166-1 válidos (`pt-PT`, `pt-BR`)
- [x] Self-referencing em todas as 8 URLs auditadas
- [x] Full mesh: 3 tags por página em ambos os domínios
- [x] x-default aponta para `lusoconta.pt` (versão PT como fallback)
- [x] 100% HTTPS, zero trailing slash mismatch
- [x] Zero placeholders — todos os URLs verificados via WebFetch em 2025-06-10
```

---

## Output anti-patterns

- Usar `example.com`, `<your-url>` ou `[INSERT LANGUAGE]` no output final entregue ao cliente
- Listar erros sem indicar severidade (Critical / High / Medium) — o cliente não sabe por onde começar
- Gerar tags para apenas uma página sem verificar return tags nas páginas alternativas
- Recomendar XML sitemap para site de 3 páginas, ou HTML tags para site cross-domain com 200 variantes
- Validar códigos de língua apenas visualmente sem cruzar com ISO 639-1 (e.g., aceitar `jp`, `eng`, `zh` sem aviso)
- Omitir x-default com a justificação "o cliente decide depois" — é required na entrega
- Apresentar hreflang correcto sem verificar alinhamento com `rel=canonical` existente
- Misturar HTTP e HTTPS nas URLs geradas sem assinalar o erro
- Entregar implementação sem especificar se deve ir no `<head>`, HTTP headers, ou sitemap
- Auditar só a homepage e assumir que o resto do site está correcto
