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
