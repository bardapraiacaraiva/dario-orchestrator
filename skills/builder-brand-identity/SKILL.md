---
name: builder-brand-identity
description: >
  Gera identidade visual completa: logo brief, color system, typography selection,
  brand guidelines document, social media templates, favicon specs.
  Use quando: identidade visual, logo, brand guidelines, cores da marca, branding visual.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Brand Identity Generator

## Proposito
Gerar identidade visual COMPLETA — nao so cores, mas todo o sistema visual da marca.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-brand-identity [marca]` | Identidade completa |
| `/builder-brand-identity logo-brief [marca]` | Brief para designer/AI gerar logo |
| `/builder-brand-identity guidelines [marca]` | Brand guidelines document |

## Output Deliverable
1. **Logo Brief** — concept direction, mood, do's and don'ts, references
2. **Color System** — primary, secondary, neutral, semantic (with hex, RGB, HSL)
3. **Typography** — font pairing, scale, usage rules
4. **Brand Guidelines PDF** (markdown source) — voice, visual, usage rules
5. **Social Media Specs** — avatar sizes, cover sizes, post templates
6. **Favicon/Icon** — specs for all platforms (16px, 32px, 180px, 512px)

## Integration
- Depende de `dario-brand` para archetype, tom de voz, posicionamento
- Alimenta `builder-design-system` com tokens visuais
- Alimenta `builder-landing-page` com copy e visual direction

## Red Flags
- Cores sem contrast check WCAG — inacessivel
- Logo brief sem versoes (dark/light/mono) — inutilizavel
- Sem guidelines de uso — marca usada inconsistentemente
- Typography sem fallback system fonts — quebra em devices sem a font

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Logo Brief tem direcção criativa accionável
- [ ] Conceito tem 1 metáfora central descrita em prosa (não lista de adjectivos)
- [ ] Do's e Don'ts com referências visuais concretas (marcas reais, não "moderno" ou "clean")
- [ ] Versões especificadas: primary, dark background, monochrome, favicon crop
- [ ] Mood board direction com 3+ referências nomeadas (ex: "Stripe para minimalismo técnico, Notion para neutralidade")
- ❌ NOT delivery-ready: `"Logo deve ser moderno e transmitir confiança"`
- ✅ Delivery-ready: `"Conceito: escudo fragmentado em grid — remete para protecção fiscal digitalizada. Refs: Plaid (geometria técnica), Wise (cor bold single-hue). Versões obrigatórias: full-color #1A2E4A, white-out para fundo escuro, mono #000 para documentos oficiais"`

### Gate 2 — Color System é completo e passa WCAG
- [ ] Mínimo 8 cores definidas: 2 primary, 2 secondary, 2 neutral, 2 semantic (success/error)
- [ ] Cada cor com hex + RGB + HSL (os três formatos)
- [ ] Contrast ratio calculado para pares texto/fundo (AA = 4.5:1 mínimo, AAA = 7:1 preferível)
- [ ] Usage rule por cor (ex: "Primary só em CTAs e headings H1/H2, nunca em body text")
- ❌ NOT delivery-ready: `Primary: #2D6BE4, Secondary: #F5A623` (sem RGB/HSL, sem contrast check)
- ✅ Delivery-ready: `Primary Blue — #1A2E4A | RGB(26,46,74) | HSL(214,48%,20%) | Contrast vs White: 12.3:1 ✅ AAA | Uso: headers, nav, CTAs primários — nunca como background de texto pequeno`

### Gate 3 — Typography tem escala e fallback stack
- [ ] Font pairing justificado (display + body, max 2 famílias)
- [ ] Escala tipográfica completa: H1→H6 + body + caption + label (px/rem + line-height + weight)
- [ ] Fallback system stack definido para cada fonte (Google Fonts / Adobe / system)
- [ ] Regra de uso: qual fonte para headlines vs corpo vs UI elements
- ❌ NOT delivery-ready: `"Usar Inter para texto e Playfair Display para títulos"`
- ✅ Delivery-ready: `H1: Playfair Display 700, 48px/1.15, fallback: Georgia, serif | Body: Inter 400, 16px/1.6, fallback: -apple-system, BlinkMacSystemFont, sans-serif | Caption: Inter 400, 12px/1.4, color: Neutral-500`

### Gate 4 — Brand Guidelines é documento standalone utilizável
- [ ] Secções obrigatórias presentes: logo usage, clear space rule, color palette, typography, voice & tone, don'ts
- [ ] Clear space rule em unidades relativas ao logo (ex: "espaço mínimo = altura da letra 'A' do logótipo")
- [ ] Mínimo 6 don'ts visuais descritos com exemplos concretos
- [ ] Documento pode ser entregue a designer externo sem briefing adicional
- ❌ NOT delivery-ready: guidelines com secções vazias ou "a definir" — inutilizável por designer externo
- ✅ Delivery-ready: `❌ Don't: Não rodar o logo — nunca usar em ângulos. ❌ Don't: Não aplicar gradiente sobre o logo. ✅ Clear space: mínimo 1× a altura do ícone em todos os lados`

### Gate 5 — Social Media Specs são plataforma-específicas e accionáveis
- [ ] Dimensões correctas por plataforma (Instagram, LinkedIn, Twitter/X no mínimo) com pixels exactos
- [ ] Template de post descrito com grid e placement de elementos (não apenas "postar com a cor primária")
- [ ] Avatar spec com safe zone definida (% do ícone que fica visível após crop circular)
- [ ] Cover/banner dimensions por plataforma com área de segurança marcada
- ❌ NOT delivery-ready: `"Avatar: 400×400px"` (sem safe zone, sem crop guidance)
- ✅ Delivery-ready: `LinkedIn Avatar: 400×400px, elemento central ocupa 60% (240px) — bordas ficam cortadas em círculo. Cover: 1584×396px, safe zone central 1200×300px — evitar texto fora desta área`

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] Nenhum `[MARCA]`, `<client>`, `[COR AQUI]` ou placeholder visível no output final
- [ ] Nome da empresa aparece em todas as secções (guidelines, social specs, favicon naming)
- [ ] Hex codes são reais e verificáveis (não `#XXXXXX`)
- [ ] Referências de fontes incluem URL ou fonte de download real
- ❌ NOT delivery-ready: `"[EMPRESA] deve usar [COR PRIMÁRIA] em todos os materiais"`
- ✅ Delivery-ready: `"Tributario.AI usa #1A2E4A como cor primária em todos os materiais institucionais"`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Brand Identity — Tributario.AI

## 1. Logo Brief

**Conceito central:** Escudo fragmentado em grid de píxeis — fusão entre
segurança fiscal (escudo) e inteligência artificial (grid/dados). O fragmento
sugere análise granular, não rigidez burocrática.

**Mood:** Técnico-confiável. Referências: Plaid (geometria limpa), Stripe
(uso bold de cor única), Harvey (credibilidade legal sem peso institucional).

**Versões obrigatórias:**
- Primary: ícone + wordmark, fundo branco, cor #1A2E4A
- Reversed: ícone + wordmark, fundo #1A2E4A, texto branco
- Monochrome: #000000 para documentos PDF/impressão
- Favicon crop: só ícone do escudo, sem wordmark

**Do's:** Grid geométrico preciso · Single-color dominant · Wordmark em
weight semibold · Espaçamento generoso entre ícone e texto

**Don'ts:** Sem gradientes sobre o logo · Sem sombras · Sem versão
outline-only sem fill · Não combinar com outras marcas sem autorização

---

## 2. Color System

| Token         | Hex     | RGB            | HSL             | Contrast/White | Uso |
|---------------|---------|----------------|-----------------|----------------|-----|
| Primary-900   | #1A2E4A | 26, 46, 74     | 214°, 48%, 20%  | 12.3:1 ✅ AAA  | Headers, CTAs, nav |
| Primary-500   | #2D5BE3 | 45, 91, 227    | 224°, 77%, 53%  | 4.6:1 ✅ AA   | Links, botões |
| Secondary-400 | #00C9A7 | 0, 201, 167    | 171°, 100%, 39% | 2.8:1 ⚠️ large | Badges, success states |
| Accent-500    | #F59E0B | 245, 158, 11   | 38°, 91%, 50%   | 2.4:1 ⚠️ large | Highlights, avisos |
| Neutral-900   | #111827 | 17, 24, 39     | 221°, 39%, 11%  | 16.1:1 ✅ AAA  | Body text |
| Neutral-400   | #9CA3AF | 156, 163, 175  | 218°, 11%, 65%  | 3.1:1 ⚠️ large | Captions, placeholders |
| Neutral-50    | #F9FAFB | 249, 250, 251  | 210°, 17%, 98%  | —              | Backgrounds |
| Semantic-Success | #10B981 | 16,185,129 | 160°, 84%, 39% | 4.6:1 ✅ AA  | Confirmações |
| Semantic-Error   | #EF4444 | 239, 68, 68 | 0°, 83%, 60%   | 4.5:1 ✅ AA  | Erros, alertas |

---

## 3. Typography

**Pairing:** Sora (display/UI) + Inter (body/data)
Justificação: Sora tem geometria técnica sem frieza excessiva; Inter é o
standard de legibilidade para dashboards fiscais/legais.

| Estilo  | Fonte    | Weight | Size       | Line-height | Uso |
|---------|----------|--------|------------|-------------|-----|
| H1      | Sora     | 700    | 48px/3rem  | 1.1         | Hero, page titles |
| H2      | Sora     | 600    | 36px/2.25rem | 1.2       | Section headers |
| H3      | Sora     | 600    | 24px/1.5rem | 1.3        | Card titles |
| H4      | Sora     | 500    | 20px/1.25rem | 1.4       | Sub-sections |
| Body    | Inter    | 400    | 16px/1rem  | 1.6         | Corpo de texto |
| Small   | Inter    | 400    | 14px/0.875rem | 1.5      | UI labels, notas |
| Caption | Inter    | 400    | 12px/0.75rem | 1.4       | Footnotes, metadata |

**Fallback stacks:**
- Sora: `'Sora', 'Nunito', -apple-system, sans-serif`
- Inter: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- Download: fonts.google.com/specimen/Sora · fonts.google.com/specimen/Inter

---

## 4. Brand Guidelines (standalone)

### 4.1 Logo — Clear Space
Espaço mínimo em todos os lados = 1× a altura da letra "T" do wordmark.
Em favicon (≤32px): usar só ícone do escudo, sem wordmark.

### 4.2 Don'ts
❌ Não rodar o logo em nenhum ângulo
❌ Não aplicar gradiente ou efeito sobre o logo
❌ Não usar versão outline sem fill
❌ Não alterar proporções ícone/wordmark
❌ Não usar Primary-500 como cor de background para texto pequeno
❌ Não colocar logo sobre fotografia sem overlay de opacidade ≥60%

### 4.3 Voice & Tone
Tom: Especialista acessível — rigoroso mas nunca intimidante.
Evitar: jargão fiscal sem explicação · tom alarmista · linguagem burocrática
Preferir: frases curtas · voz activa · explicação antes da regra

---

## 5. Social Media Specs

| Plataforma  | Asset      | Dimensões     | Safe Zone       | Notas |
|-------------|------------|---------------|-----------------|-------|
| LinkedIn    | Avatar     | 400×400px     | 240px centrado  | Crop circular — logo a 60% |
| LinkedIn    | Cover      | 1584×396px    | 1200×300px      | Evitar texto fora da safe zone |
| Instagram   | Avatar     | 320×320px     | 192px centrado  | Só ícone escudo |
| Instagram   | Post       | 1080×1080px   | 900×900px       | Grid: logo top-left, CTA bottom-right |
| Twitter/X   | Avatar     | 400×400px     | 240px centrado  | Crop circular |
| Twitter/X   | Header     | 1500×500px    | 1200×400px      | Tagline centrada na safe zone |

---

## 6. Favicon & App Icon Specs

| Tamanho | Uso                          | Ficheiro           |
|---------|------------------------------|--------------------|
| 16×16   | Browser tab (low-res)        | favicon-16.png     |
| 32×32   | Browser tab (retina)         | favicon-32.png     |
| 180×180 | Apple Touch Icon (iOS)       | apple-touch-icon.png |
| 192×192 | Android Chrome               | icon-192.png       |
| 512×512 | PWA splash screen            | icon-512.png       |

Nota: em 16px e 32px, usar só o ícone do escudo sem wordmark.
Em 180px+, pode incluir padding de 10% (18px) para breathing room no iOS.
```

---

## Output anti-patterns

- Paleta com menos de 8 cores — deixa estados semânticos (erro/sucesso) sem definição
- Hex codes sem RGB/HSL — impossibilita uso em CSS variables, Figma tokens, Tailwind config
- Typography sem fallback stack — quebra visual em devices sem Google Fonts carregado
- Logo brief com adjectivos vagos ("moderno", "profissional") sem referências de marcas reais
- Guidelines sem clear space rule mensurável — designer externo não consegue aplicar correctamente
- Social specs com dimensões mas sem safe zones — texto cortado em crops circulares/automáticos
- Contrast ratios não calculados — entrega inacessível, reprovada em audit WCAG
- Versões do logo não especificadas (dark/light/mono) — marca inutilizável em contextos reais
- Fontes referenciadas sem URL de download ou licença — bloqueia implementação
- Output genérico reutilizável em qualquer marca — ausência de decisões de posicionamento visual
