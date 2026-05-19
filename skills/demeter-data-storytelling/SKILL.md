---
name: demeter-data-storytelling
description: Data storytelling — executive narratives, slide decks data-driven, Tableau Story Points. Comunicar insights para não-técnicos. Triggers em "data storytelling", "executive presentation", "data slides", "narrative", "story points", "data visualization narrative".
license: MIT
parent_agent: demeter-director
compliance: [data_integrity, no_misleading_charts]
---

# DEMETER-DATA-STORYTELLING — Insights → Acção

## Filosofia
**Análise técnica sem narrativa = report ignorado.** Storytelling traduz p-values em decisões.

## Quando usar
- Apresentação executiva pós-A/B test
- QBR (Quarterly Business Review)
- Board pack / investor update
- Pitch deck com dados
- Post-mortem de experiment
- Annual report

## Frameworks
- **Pyramid Principle (McKinsey):** conclusão first, depois suporte
- **SCQA:** Situation → Complication → Question → Answer
- **STAR:** Situation → Task → Action → Result
- **Hero's Journey:** desafio → insight → resolução
- **Cole Nussbaumer Knaflic:** "Storytelling with Data" framework

## Templates
1. Executive 1-slide summary (recomendação + 3 razões)
2. A/B test result slides (10 slides: hipótese → setup → resultados → recomendação)
3. QBR deck (15 slides: highlights + lowlights + ações)
4. Board pack (5 metrics + commentary + outlook)
5. Pitch deck data section (TAM/SAM/SOM + traction)

## Princípios de visual design
- **Highlight é mais importante que beleza:** uma cor para focal point, resto grayscale
- **Title como takeaway:** "Revenue cresceu 30%" não "Revenue Q4 2025"
- **Annotate context:** anotação na curva explicando spike
- **Remove chart junk:** Tufte data-ink ratio
- **Order matters:** ordenar bars por value, não alphabetical

## Anti-patterns (chart crimes)
- ❌ Pie chart com 8 fatias
- ❌ Y-axis truncado para inflar visual
- ❌ 3D anything
- ❌ Dual-axis sem cor consistente
- ❌ Legenda fora do contexto (use direct labels)

## Cross-references
- [[demeter-bi-dashboard]] — visualizações
- [[demeter-ab-testing]] — reportar resultados
- [[dario-pitch]] — pitch frameworks
- [[a360-pitch]] — investor decks
