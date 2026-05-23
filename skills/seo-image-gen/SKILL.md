---
name: seo-image-gen
description: "AI image generation for SEO assets: OG/social preview images, blog hero images, schema images, product photography, infographics. Powered by Gemini via nanobanana-mcp. Requires banana extension installed. Use when user says \"generate image\", \"OG image\", \"social preview\", \"hero image\", \"blog image\", \"product photo\", \"infographic\", \"seo image\", \"create visual\", \"image-gen\", \"favicon\", \"schema image\", \"pinterest pin\", \"generate visual\", \"banner\", or \"thumbnail\"."
argument-hint: "[og|hero|product|infographic|custom|batch] <description>"
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# SEO Image Gen: AI Image Generation for SEO Assets (Extension)

Generate production-ready images for SEO use cases using Gemini's image generation
via the banana Creative Director pipeline. Maps SEO needs to optimized domain modes,
aspect ratios, and resolution defaults.

## Architecture Note

This extension is built on [Claude Banana](https://github.com/AgriciDaniel/banana-claude),
the standalone AI image generation skill for Claude Code.

This skill has two components with distinct roles:
- **SKILL.md** (this file): Handles interactive `/seo image-gen` commands for generating images
- **Agent** (`agents/seo-image-gen.md`): Audit-only analyst spawned during `/seo audit` to assess existing OG/social images and produce a generation plan (never auto-generates)

## Prerequisites

This skill requires the banana extension to be installed:
```bash
./extensions/banana/install.sh
```

**Check availability:** Before using any image generation tool, verify the MCP server
is connected by checking if `gemini_generate_image` or `set_aspect_ratio` tools are
available. If tools are not available, inform the user the extension is not installed
and provide install instructions.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo image-gen og <description>` | Generate OG/social preview image (1200x630 feel) |
| `/seo image-gen hero <description>` | Blog hero image (widescreen, dramatic) |
| `/seo image-gen product <description>` | Product photography (clean, white BG) |
| `/seo image-gen infographic <description>` | Infographic visual (vertical, data-heavy) |
| `/seo image-gen custom <description>` | Custom image with full Creative Director pipeline |
| `/seo image-gen batch <description> [N]` | Generate N variations (default: 3) |

## SEO Image Use Cases

Each use case maps to pre-configured banana parameters:

| Use Case | Aspect Ratio | Resolution | Domain Mode | Notes |
|----------|-------------|------------|-------------|-------|
| **OG/Social Preview** | `16:9` | `1K` | Product or UI/Web | Clean, professional, text-friendly |
| **Blog Hero** | `16:9` | `2K` | Cinema or Editorial | Dramatic, atmospheric, editorial quality |
| **Schema Image** | `4:3` | `1K` | Product | Clean, descriptive, schema ImageObject |
| **Social Square** | `1:1` | `1K` | UI/Web | Platform-optimized square |
| **Product Photo** | `4:3` | `2K` | Product | White background, studio lighting |
| **Infographic** | `2:3` | `4K` | Infographic | Data-heavy, vertical layout |
| **Favicon/Icon** | `1:1` | `512` | Logo | Minimal, scalable, recognizable |
| **Pinterest Pin** | `2:3` | `2K` | Editorial | Tall vertical card |

## Generation Pipeline

For every generation request:

1. **Identify use case** from command or context (og, hero, product, etc.)
2. **Apply SEO defaults** from the use cases table above
3. **Set aspect ratio** via `set_aspect_ratio` MCP tool
4. **Construct Reasoning Brief** using the banana Creative Director pipeline:
   - Load `references/prompt-engineering.md` for the 6-component system
   - Apply domain mode emphasis (Subject 30%, Style 25%, Context 15%, etc.)
   - Be SPECIFIC and VISCERAL: describe what the camera sees
5. **Generate** via `gemini_generate_image` MCP tool
6. **Post-generation SEO checklist** (see below)

### Check for Presets

If the user mentions a brand or has SEO presets configured:
```bash
python3 ~/.claude/skills/seo-image-gen/scripts/presets.py list
```
Load matching preset and apply as defaults. Also check `references/seo-image-presets.md`
for SEO-specific preset templates.

## Post-Generation SEO Checklist

After every successful generation, guide the user on:

1. **Alt text**:Write descriptive, keyword-rich alt text for the generated image
2. **File naming**:Rename to SEO-friendly format: `keyword-description-widthxheight.webp`
3. **WebP conversion**:Convert to WebP for optimal page speed:
   ```bash
   magick output.png -quality 85 output.webp
   ```
4. **File size**:Target under 200KB for hero images, under 100KB for thumbnails
5. **Schema markup**:Suggest `ImageObject` schema for the generated image:
   ```json
   {
     "@type": "ImageObject",
     "url": "https://example.com/images/keyword-description.webp",
     "width": 1200,
     "height": 630,
     "caption": "Descriptive caption with target keyword"
   }
   ```
6. **OG meta tags**:For social preview images, remind about:
   ```html
   <meta property="og:image" content="https://example.com/images/og-image.webp" />
   <meta property="og:image:width" content="1200" />
   <meta property="og:image:height" content="630" />
   <meta property="og:image:alt" content="Descriptive alt text" />
   ```

## Cost Awareness

Image generation costs money. Be transparent:
- Show estimated cost before generating (especially for batch)
- Log every generation: `python3 ~/.claude/skills/seo-image-gen/scripts/cost_tracker.py log --model MODEL --resolution RES --prompt "brief"`
- Run `cost_tracker.py summary` if user asks about usage

Approximate costs (gemini-3.1-flash):
- 512: ~$0.02/image
- 1K resolution: ~$0.04/image
- 2K resolution: ~$0.08/image
- 4K resolution: ~$0.16/image

## Model Routing

| Scenario | Model | Why |
|----------|-------|-----|
| OG images, social previews | `gemini-3.1-flash-image-preview` @ 1K | Fast, cost-effective |
| Hero images, product photos | `gemini-3.1-flash-image-preview` @ 2K | Quality + detail |
| Infographics with text | `gemini-3.1-flash-image-preview` @ 2K, thinking: high | Better text rendering |
| Quick drafts | `gemini-2.5-flash-image` @ 512 | Rapid iteration |

## Error Handling

| Error | Resolution |
|-------|-----------|
| MCP not configured | Run `./extensions/banana/install.sh` |
| API key invalid | New key at https://aistudio.google.com/apikey |
| Rate limited (429) | Wait 60s, retry. Free tier: ~10 RPM / ~500 RPD |
| `IMAGE_SAFETY` | Rephrase prompt - see `references/prompt-engineering.md` Safety section |
| MCP unavailable | Fall back: `python3 ~/.claude/skills/seo-image-gen/scripts/generate.py --prompt "..." --aspect-ratio "16:9"` |
| Extension not installed | Show install instructions: `./extensions/banana/install.sh` |

## Cross-Skill Integration

- **seo-images** (analysis) feeds into **seo-image-gen** (generation): audit results from `/seo images` identify missing or low-quality images; use those findings to drive `/seo image-gen` commands
- **seo-audit** spawns the seo-image-gen **agent** (not this skill) to analyze OG/social images across the site and produce a prioritized generation plan
- **seo-schema** can consume generated images: after generation, suggest `ImageObject` schema markup pointing to the new assets

## Reference Documentation

Load on-demand. Do NOT load all at startup:
- `references/prompt-engineering.md`:6-component system, domain modes, templates
- `references/gemini-models.md`:Model specs, rate limits, capabilities
- `references/mcp-tools.md`:MCP tool parameters and responses
- `references/post-processing.md`:ImageMagick/FFmpeg pipeline recipes
- `references/cost-tracking.md`:Pricing, usage tracking
- `references/presets.md`:Brand preset management
- `references/seo-image-presets.md`:SEO-specific preset templates

## Response Format

After generating, always provide:
1. **Image path**:where it was saved
2. **Crafted prompt**:show what was sent to the API (educational)
3. **Settings**:model, aspect ratio, resolution
4. **SEO checklist**:alt text suggestion, file naming, WebP conversion
5. **Schema snippet**:ImageObject or og:image markup if applicable

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Use case identificado e parâmetros SEO aplicados
- [ ] Tipo de imagem explícito (og, hero, product, infographic, schema, favicon, pinterest)
- [ ] Aspect ratio correto aplicado via `set_aspect_ratio` antes da geração (não depois)
- [ ] Resolução do defaults table usada (512/1K/2K/4K), não inventada
- [ ] Domain mode mapeado ao use case (ex: hero → Cinema ou Editorial, nunca Product)
- ❌ NOT delivery-ready: "Gerei a imagem com as configurações padrão"
- ✅ Delivery-ready: "OG image gerada: `set_aspect_ratio 16:9` + resolução 1K + domain mode UI/Web — parâmetros da tabela SEO defaults"

### Gate 2 — Reasoning Brief construído com o pipeline Creative Director
- [ ] 6 componentes do `references/prompt-engineering.md` presentes (Subject, Style, Context, etc.)
- [ ] Prompt é ESPECÍFICO e VISCERAL: descreve o que a câmara vê, não intenções abstratas
- [ ] Pesos de domínio respeitados (Subject 30%, Style 25%, Context 15%...)
- [ ] Presets verificados via `presets.py list` se cliente com brand conhecida
- ❌ NOT delivery-ready: "Uma imagem profissional para o blog sobre finanças"
- ✅ Delivery-ready: "Overhead shot of a worn leather notebook open on a marble desk, single espresso cup casting long shadow, warm 5600K key light from left, shallow DOF, editorial texture — LUSOconta blog hero 16:9 2K"

### Gate 3 — Post-generation SEO checklist completa e entregue
- [ ] Alt text escrito (keyword-rich, descritivo, não genérico)
- [ ] Nome de ficheiro sugerido em formato SEO: `keyword-descricao-1200x630.webp`
- [ ] Comando WebP de conversão incluído com `-quality 85`
- [ ] Target de file size mencionado (≤200KB hero, ≤100KB thumbnail)
- ❌ NOT delivery-ready: "Lembra-te de otimizar a imagem para SEO"
- ✅ Delivery-ready: "Alt: `Conta poupança LUSOconta com juro de 4.2% ao ano` · Ficheiro: `conta-poupanca-lusoconta-1200x630.webp` · Converter: `magick output.png -quality 85 conta-poupanca-lusoconta-1200x630.webp` · Target: <200KB"

### Gate 4 — Schema markup e OG meta tags fornecidos (quando aplicável)
- [ ] `ImageObject` schema JSON-LD incluído para schema images e hero images
- [ ] `url`, `width`, `height`, `caption` populados com valores reais (não `example.com`)
- [ ] OG meta tags HTML incluídas para social preview images
- [ ] `og:image:width` e `og:image:height` com valores numéricos corretos
- ❌ NOT delivery-ready: `"url": "https://example.com/images/og-image.webp"`
- ✅ Delivery-ready: `"url": "https://lusoconta.pt/images/conta-poupanca-lusoconta-1200x630.webp", "width": 1200, "height": 630`

### Gate 5 — Custo transparente e logging executado
- [ ] Custo estimado mostrado ANTES de gerar (especialmente batch)
- [ ] `cost_tracker.py log` executado após geração com model, resolution e prompt
- [ ] Para batch: custo total = N × custo unitário explicitamente calculado
- [ ] Se extensão banana não disponível: erro claro + instrução `./extensions/banana/install.sh`
- ❌ NOT delivery-ready: (silêncio sobre custos, geração directa sem aviso)
- ✅ Delivery-ready: "Estimativa: 3 variações × $0.08 (2K) = **$0.24** — confirmas? · Após geração: `cost_tracker.py log --model gemini-3.1-flash-image-preview --resolution 2K --prompt 'Atrium hero blog'`"

### Gate 6 — Output usa CLIENT NAME + dados reais, sem angle-brackets placeholder
- [ ] URL do cliente real (não `example.com` nem `<your-domain>`)
- [ ] Keywords reais do negócio do cliente no alt text e caption
- [ ] Nome de ficheiro contém termos do produto/serviço real, não `image-1` ou `output`
- [ ] Schema `caption` contém keyword target real, não `Descriptive caption with target keyword`
- ❌ NOT delivery-ready: `"caption": "Descriptive caption with target keyword"`, URL `example.com`
- ✅ Delivery-ready: `"caption": "Armazém ARRECADA.GOV Lisboa — aluguer de box desde 29€/mês"`, URL `arrecada.gov.pt/images/...`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## Geração de OG Image — Cuidai

**Use case detectado:** OG/Social Preview
**Parâmetros SEO aplicados:**
- Aspect ratio: `16:9` → `set_aspect_ratio 16:9` ✓
- Resolução: `1K` ($0.04)
- Domain mode: UI/Web (clean, text-friendly)

**Custo estimado: $0.04 — confirmas a geração?**

---

### Reasoning Brief (Creative Director Pipeline)

```
[Subject 30%] Caring professional caregiver holding hands of elderly woman
in bright home setting, warm eye contact, genuine smile
[Style 25%] Clean editorial photography, flat-lay impossible here — 
soft bokeh background, pastel palette #F7F3EF dominant
[Context 15%] Portuguese home care service, trustworthy, family-oriented
[Mood 15%] Warmth, safety, relief — the feeling of "mãe está bem"
[Technical 10%] 1200×630px final crop, text-safe margins 120px each side
[Negative 5%] No stock-photo stiffness, no hospital aesthetic, no blue tones
```

**Gerado via:** `gemini_generate_image` — `gemini-3.1-flash-image-preview` @ 1K ✓

---

### Post-Generation SEO Checklist

**Alt text:**
`Cuidadora Cuidai a acompanhar idosa em casa — serviço de apoio domiciliário em Lisboa`

**Nome de ficheiro:**
`apoio-domiciliario-cuidai-1200x630.webp`

**Conversão WebP:**
```bash
magick output.png -quality 85 apoio-domiciliario-cuidai-1200x630.webp
```
Target: **<100KB** ✓ (OG images devem ser leves)

**Schema ImageObject:**
```json
{
  "@type": "ImageObject",
  "url": "https://cuidai.pt/images/apoio-domiciliario-cuidai-1200x630.webp",
  "width": 1200,
  "height": 630,
  "caption": "Serviço de apoio domiciliário Cuidai — cuidadores certificados em Lisboa e Grande Lisboa"
}
```

**OG Meta Tags:**
```html
<meta property="og:image" content="https://cuidai.pt/images/apoio-domiciliario-cuidai-1200x630.webp" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="Cuidadora Cuidai a acompanhar idosa em casa — apoio domiciliário Lisboa" />
```

**Cost log executado:**
```bash
python3 ~/.claude/skills/seo-image-gen/scripts/cost_tracker.py log \
  --model gemini-3.1-flash-image-preview \
  --resolution 1K \
  --prompt "caregiver holding hands elderly woman Portuguese home care"
```
```

---

## Output anti-patterns

- Gerar imagem sem confirmar custo estimado primeiro, especialmente em batch (3 imagens = $0.24 a $0.48 sem aviso)
- Post-generation checklist omitida ou resumida a "lembra-te de otimizar" sem alt text, filename e WebP command concretos
- Schema e OG tags com `example.com` ou `<your-domain>` em vez do domínio real do cliente
- Aspect ratio definido DEPOIS da geração ou não chamado via `set_aspect_ratio` MCP tool
- Reasoning Brief vago: "imagem profissional de cuidados" sem Subject/Style/Context/Mood/Technical/Negative
- Resolução inventada (ex: `3K`) em vez das opções documentadas (512/1K/2K/4K)
- Não verificar disponibilidade do banana MCP antes de tentar gerar — falha silenciosa confunde o utilizador
- `caption` no schema igual ao alt text — devem ser distintos (schema é para indexação, alt é para acessibilidade)
- Batch sem especificar N explicitamente e sem custo total calculado antes de executar
