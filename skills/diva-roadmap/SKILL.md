---
name: diva-roadmap
description: "Synthesize a complete project roadmap from diagnose + briefing + budget + timeline into one visual deliverable. The 'big picture' document for client presentation. Generates HTML visual roadmap with phases, milestones, budget allocation, team, and key decisions. Triggers on \"roadmap\", \"plano geral\", \"visao geral projecto\", \"mapa do projecto\", \"apresentacao projecto\", \"big picture\", \"plano completo\"."
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# DIVA Roadmap — Complete Project Synthesis

Generate a single, comprehensive project roadmap that synthesizes ALL project data into one client-ready deliverable. This is the "filme completo" — from briefing to entrega.

## When to activate

Invoke `/diva-roadmap` when:
- Client needs to see "the full picture" before approving
- After diagnose + briefing are complete, to present the plan
- Before signing contract, to align expectations
- User says "mostra-me o plano todo", "big picture", "roadmap"

## Workflow

### 1. Gather all existing project data
Search for completed deliverables:
```
mcp__dario-rag__search_kb(query: "<project name> diagnostico briefing", collection: "diva", limit: 5)
```
Check agent memory for project file.
Check Obsidian vault for existing outputs.

### 2. Synthesize 7 sections

**A. Resumo Executivo** (5 linhas max)
- O que: tipo de projecto + localizacao + area
- Quanto: orcamento total (3 cenarios se disponivel)
- Quando: prazo total estimado
- Como: fases principais
- Porquê: objectivo do cliente

**B. Equipa e Responsabilidades**
| Papel | Quem | Responsabilidade |
| Arquitecto | | Projecto, coordenacao |
| Designer interiores | | Conceito, materiais |
| Empreiteiro | | Execucao |
| Fiscal | | Qualidade, conformidade |
| Engenheiros | | Especialidades |

**C. Timeline Visual** (Gantt simplificado em texto/HTML)
```
M1  M2  M3  M4  M5  M6  M7  M8  M9  M10 M11 M12
|===PROJECTO====|
         |==LICEN==|
                    |===DEMOLICAO+ESTRUTURA====|
                              |===MEP+ACABAMENTOS=======|
                                          |===CARPINT+EQUIP==|
                                                    |==ENTREGA|
```

**D. Budget Overview**
| Fase | % | EUR (recomendado) |
| Projecto + honorarios | 12% | |
| Licenciamento | 2% | |
| Construcao | 70% | |
| Equipamentos | 8% | |
| Contingencia | 8% | |

**E. Design Direction**
- Estilo identificado + designer de referencia
- Paleta de cores (3-5 cores com hex)
- Materiais-chave (pavimento, paredes, bancada)
- 1 render conceptual ou Midjourney prompt

**F. Milestones de Decisao**
| # | Decisao | Prazo | Quem decide |
| 1 | Aprovar conceito/moodboard | Semana X | Cliente |
| 2 | Adjudicar empreiteiro | Semana X | Cliente |
| 3 | Aprovar materiais | Semana X | Cliente + Designer |
| 4 | Aprovar cozinha | Semana X | Cliente |
| 5 | Inspeccao pre-acabamentos | Semana X | Fiscal |
| 6 | Punch list final | Semana X | Todos |

**G. Riscos e Mitigacao**
| Risco | Probabilidade | Impacto | Mitigacao |
Top 5 riscos identificados com plano.

### 3. Generate HTML deliverable

Usar `mcp__aidesigner__generate_design` para criar um HTML visual bonito com:
- Header com nome do projecto + morada
- Timeline visual (SVG bars coloridas)
- Budget donut chart (SVG)
- Team cards
- Material palette visual
- Milestone checklist

OU gerar como Markdown premium para Obsidian/PDF.

### 4. Save
- HTML: `[projecto]-roadmap.html`
- Markdown: Obsidian `05 - Claude - IA/Outputs/YYYY-MM-DD - [Projecto] - Roadmap.md`

## Output template

```markdown
---
project: <nome>
date: <YYYY-MM-DD>
type: roadmap
diva_specializations: [all relevant]
budget_total: <EUR>
timeline_months: <N>
---

# Roadmap — <Projecto>

## Resumo Executivo
<5 linhas>

## Equipa
<tabela>

## Timeline
<gantt visual>

## Budget
<breakdown com 3 cenarios>

## Design Direction
<estilo + paleta + materiais + render concept>

## Milestones de Decisao
<tabela com datas e responsaveis>

## Riscos
<top 5 com mitigacao>

## Proximos Passos Imediatos
1. <accao>
2. <accao>
3. <accao>
```

## Red flags
- Nunca apresentar roadmap sem orcamento (mesmo estimado)
- Nunca omitir riscos — honestidade constroi confianca
- Nunca dar datas absolutas sem margem (sempre "Semana X +-1")
- Incluir SEMPRE disclaimer de precos estimados

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Resumo Executivo está completo e quantificado
- [ ] Tipo de projecto + localização identificados (ex: "remodelação integral apartamento T3, Estrela, Lisboa")
- [ ] Orçamento total presente com pelo menos 1 cenário numérico em EUR
- [ ] Prazo total em meses explícito (não "alguns meses")
- [ ] Objectivo do cliente formulado em 1 frase concreta

❌ NOT delivery-ready: `Projecto de renovação com orçamento a definir, prazo estimado.`
✅ Delivery-ready: `Remodelação integral T3 Príncipe Real (142m²) | Orçamento recomendado: 185.000€ | Prazo: 11 meses | Objectivo: revenda premium antes de Setembro 2026.`

---

### Gate 2 — Timeline tem fases sem sobreposição impossível e margem declarada
- [ ] Todas as fases nomeadas (Projecto, Licenciamento, Obra, MEP, Acabamentos, Entrega)
- [ ] Cada fase tem duração em semanas/meses com `±1` ou margem explícita
- [ ] Sobreposições de fases são realistas (ex: MEP não começa antes de estrutura estar 60% feita)
- [ ] Data de início é relativa ("Semana 1 = assinatura contrato") ou absoluta com disclaimer

❌ NOT delivery-ready: `Fase 1: projecto. Fase 2: obra. Fase 3: entrega. Duração total: ~1 ano.`
✅ Delivery-ready: `M1–M3: Projecto + CAD | M3–M5: Licenciamento CM Lisboa (±4 sem.) | M5–M7: Demolição + Estrutura | M7–M10: MEP + Isolamentos | M10–M11: Acabamentos + Carpintaria | M11: Punch list + Entrega — Total: 11 meses ±1`

---

### Gate 3 — Budget breakdown tem 5 linhas com % + EUR calculados
- [ ] Todas as 5 categorias presentes: Projecto/Honorários, Licenciamento, Construção, Equipamentos, Contingência
- [ ] Percentagens somam 100%
- [ ] Valores EUR calculados a partir do total (não inventados por linha)
- [ ] Se 3 cenários: Económico / Recomendado / Premium com totais distintos
- [ ] Disclaimer "preços estimados — sujeitos a revisão em fase de consulta a empreiteiros" presente

❌ NOT delivery-ready: `Construção: ~100k€. Projecto: alguns milhares. Contingência incluída.`
✅ Delivery-ready: `Total recomendado 185.000€ | Projecto+Honor. 12% = 22.200€ | Licenc. 2% = 3.700€ | Construção 70% = 129.500€ | Equipamentos 8% = 14.800€ | Contingência 8% = 14.800€ — *Estimativa sujeita a consulta a 3 empreiteiros.*`

---

### Gate 4 — Milestones de Decisão têm semana + responsável nomeado
- [ ] Mínimo 5 milestones listados
- [ ] Cada milestone tem prazo relativo ("Semana 8", não "em breve")
- [ ] Coluna "Quem decide" preenchida (não vazia, não "TBD")
- [ ] Milestone 1 é sempre aprovação de conceito/moodboard — o mais urgente
- [ ] Último milestone é Punch List Final com todos os intervenientes

❌ NOT delivery-ready: `Decisão sobre materiais — a definir. Adjudicação empreiteiro — cliente decide quando quiser.`
✅ Delivery-ready: `Sem. 4: Aprovar moodboard → Ana Ferreira (cliente) | Sem. 9: Adjudicar empreiteiro → Ana Ferreira + Arq. Rui Costa | Sem. 12: Aprovar materiais cozinha → Ana Ferreira + Designer | Sem. 32: Punch list final → Todos`

---

### Gate 5 — Top 5 Riscos têm probabilidade + impacto + mitigação concreta
- [ ] Exactamente 5 riscos (não 2, não 10)
- [ ] Probabilidade: Alta / Média / Baixa (não omitida)
- [ ] Impacto: quantificado se possível ("atraso 4–6 semanas", "+8.000–15.000€")
- [ ] Mitigação é uma acção, não um desejo ("Contratar fiscal independente na Semana 1", não "ter cuidado")
- [ ] Risco de licenciamento camarário sempre presente para projectos Lisboa/Porto

❌ NOT delivery-ready: `Risco: obra pode atrasar. Mitigação: acompanhar de perto.`
✅ Delivery-ready: `Risco: Licenciamento CM Lisboa excede prazo | P: Alta | I: +6–10 sem., +3.500€ honorários | Mitigação: Submeter com arquitecto licenciado experiente na CM Lisboa; buffer 4 sem. já incluído no timeline.`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] Zero ocorrências de `<nome>`, `<projecto>`, `<EUR>`, `<YYYY-MM-DD>` ou similares no output final
- [ ] Nome do projecto/cliente aparece no header, no frontmatter YAML e nos milestones
- [ ] Endereço ou localização real (ou anonimizado com decisão explícita) está presente
- [ ] Ficheiro salvo com nome real: ex. `vivenda-estrela-roadmap.html`, não `projecto-roadmap.html`

❌ NOT delivery-ready: `# Roadmap — <Projecto> | Budget: <EUR> | Timeline: <N> meses`
✅ Delivery-ready: `# Roadmap — Vivenda Estrela | Budget recomendado: 185.000€ | Timeline: 11 meses | Cliente: Ana Ferreira | Data: 2025-06-12`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no roadmap deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de diagnóstico, briefing, ou memória de sessão anterior
- 🟡 **assumed** — plausível dado o tipo de projecto, mas precisa confirmação do cliente pré-entrega
- 🟢 **projection** — estimativa de design (não verificável até execução)

Output checklist upfront mostra ao cliente exactamente o que é trust-as-is vs. o que precisa validar. **Honest transparency > roadmap inflado com falsa precisão.**

❌ NOT delivery-ready:
```
Timeline: 10 meses | Orçamento: €180.000 | Empreiteiro: Silva & Filhos
Fase 1 — Projecto: M1–M3 | Contingência: 8%
```
*(reader assume tudo verificado — nenhum label, empreiteiro pode não estar adjudicado, orçamento pode ser chute)*

✅ Delivery-ready:
```
Timeline: 10 meses 🟢 (projection — sem caderno encargos fechado)
Orçamento total: €180.000 🔵 (verified — briefing sessão 2024-11-03)
Empreiteiro: Silva & Filhos 🟡 (assumed — indicado pelo cliente, adjudicação pendente)
Contingência: 8% 🟢 (projection — standard DIVA para remodelação integral)
Paleta: Warm White #F5F0EB + Sage #8A9E8C + Brass #B08D57 🟡 (assumed — baseado em moodboard aprovado verbalmente, confirmação escrita pendente)
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir empreiteiro/designer assumidos por nomes adjudicados; paleta validada por escrito
- [ ] All 🔵 items com referência à fonte (sessão, documento, email) anotada no Obsidian
- [ ] All 🟢 projections comunicadas explicitamente ao cliente como estimativas ("prazo +-1 semana", "orçamento +-10%")

## Fully-worked A-tier example (delivery-ready reference)

```markdown
---
project: Vivenda Estrela
date: 2025-06-12
type: roadmap
diva_specializations: [residencial, remodelacao-integral, licenciamento-lisboa]
budget_total: 185000
timeline_months: 11
---

# Roadmap — Vivenda Estrela
### Rua de São Bento 214, 3ºDto, Lisboa — Remodelação Integral T3 142m²

---

## Resumo Executivo
Remodelação integral de apartamento T3 (142m²) em edifício pombalino, Estrela, Lisboa.
Orçamento recomendado: **185.000€** (cenário premium: 220.000€ / económico: 155.000€).
Prazo total: **11 meses ±1** — início previsto Julho 2025, entrega Junho 2026.
Fases: Projecto → Licenciamento → Obra → Acabamentos → Entrega.
Objectivo: valorização para revenda premium no mercado de expatriados — target €1.2M.

---

## Equipa

| Papel                  | Quem                        | Responsabilidade                          |
|------------------------|-----------------------------|-------------------------------------------|
| Arquitecto             | Rui Costa (RC Arquitectos)  | Projecto, coordenação geral, licenciamento|
| Designer de Interiores | Sofia Menezes Studio        | Conceito, materiais, FF&E                 |
| Empreiteiro            | A adjudicar — Semana 9      | Execução integral da obra                 |
| Fiscal de Obra         | Eng.ª Carla Nunes           | Qualidade, conformidade, relatórios       |
| Eng. Estruturas        | Paulo Ribeiro (Estrutotek)  | Reforço laje + abertura vãos              |
| Eng. MEP               | Fábio Santos (MEPLisboa)    | AVAC, electricidade, hidráulica           |

---

## Timeline (Gantt simplificado)

```
          Jul  Ago  Set  Out  Nov  Dez  Jan  Fev  Mar  Abr  Mai  Jun
          M1   M2   M3   M4   M5   M6   M7   M8   M9   M10  M11  M12
Projecto  |====|====|====|
Licenc.             |====|====|====|
Demolição                     |====|====|
Estrutura                          |====|====|
MEP                                     |====|====|====|
Acabamentos                                        |====|====|
Carpintaria                                              |====|====|
Entrega                                                        |====|
```
*Todas as durações com margem ±1 semana. Licenciamento CM Lisboa: buffer 4 semanas incluído.*

---

## Budget — 3 Cenários

| Categoria              | %   | Económico (155k€) | Recomendado (185k€) | Premium (220k€) |
|------------------------|-----|-------------------|---------------------|-----------------|
| Projecto + Honorários  | 12% | 18.600€           | 22.200€             | 26.400€         |
| Licenciamento          | 2%  | 3.100€            | 3.700€              | 4.400€          |
| Construção             | 70% | 108.500€          | 129.500€            | 154.000€        |
| Equipamentos + FF&E    | 8%  | 12.400€           | 14.800€             | 17.600€         |
| Contingência           | 8%  | 12.400€           | 14.800€             | 17.600€         |
| **TOTAL**              |100% | **155.000€**      | **185.000€**        | **220.000€**    |

> ⚠️ *Estimativas baseadas em diagnóstico de Maio 2025. Sujeitas a revisão após consulta a 3 empreiteiros (Semana 8).*

---

## Design Direction

**Estilo:** Contemporary Portuguese — fusão de modernismo minimalista com referências ao azulejo e tecto pombalino recuperado. Referência: Studiomk27 (São Paulo) adaptado ao contexto lisboeta.

**Paleta:**
- `#F5F0E8` — Branco caiação (paredes principais)
- `#2C3E35` — Verde musgo escuro (cozinha + carpintarias)
- `#C4A882` — Terracota suave (detalhes cerâmica)
- `#1A1A1A` — Ferro forjado (perfis, puxadores)
- `#D4C5A9` — Linho natural (têxteis)

**Materiais-chave:**
- Pavimento: Soalho pinho recuperado + acabamento mate natural
- Paredes: Estuque liso pintado + painel azulejo artesanal (I&D Azulejos, Caldas)
- Bancada cozinha: Dekton Pietra Kode 12mm antracite
- Casa de banho: Mármore Estremoz polido + torneiras Brodware série Yokato

**Midjourney prompt concept:**
`Contemporary Portuguese apartment interior, Estrela Lisbon, recovered pine floors, dark green kitchen cabinetry, white lime walls, artisan azulejo accents, natural linen, black steel profiles, golden hour light --ar 16:9 --style raw`

---

## Milestones de Decisão

| # | Decisão                              | Prazo     | Quem Decide                            |
|---|--------------------------------------|-----------|----------------------------------------|
| 1 | Aprovar conceito + moodboard         | Semana 3  | Ana Ferreira                           |
| 2 | Aprovar projecto de arquitectura     | Semana 6  | Ana Ferreira + Rui Costa               |
| 3 | Adjudicar empreiteiro (de 3 propostas)| Semana 9 | Ana Ferreira + Eng.ª Carla Nunes       |
| 4 | Aprovar selecção de materiais        | Semana 12 | Ana Ferreira + Sofia Menezes           |
| 5 | Aprovar cozinha + electrodomésticos  | Semana 14 | Ana Ferreira                           |
| 6 | Inspecção pré-acabamentos            | Semana 36 | Eng.ª Carla Nunes + Empreiteiro        |
| 7 | Punch list final + chaves            | Semana 44 | Ana Ferreira + Todos os intervenientes |

---

## Top 5 Riscos e Mitigação

| # | Risco                                    | Prob.  | Impacto                    | Mitigação                                                                 |
|---|------------------------------------------|--------|----------------------------|---------------------------------------------------------------------------|
| 1 | Licenciamento CM Lisboa excede prazo     | Alta   | +6–10 sem., +3.500€        | Arquitecto com experiência comprovada CM Lisboa; buffer 4 sem. no plano   |
| 2 | Surpresas estruturais (edifício 1890)    | Média  | +15.000–30.000€, +4 sem.   | Sondagens antes de obra; contingência 8% alocada; eng. estruturas on-call |
| 3 | Escassez de materiais (soalho pinho)     | Média  | +3 sem., substituição      | Encomendar soalho recuperado na Semana 2, antes de adjudicar obra         |
| 4 | Rotatividade de subempreiteiros          | Média  | +2–4 sem. por especialidade| Cláusula contratual de penalidade; fiscal acompanha semanalmente          |
| 5 | Alteração de programa pelo cliente      | Baixa  | +20.000€, +6 sem. mínimo   | Freeze de programa na Semana 6 (assinatura); change order protocol escrito|

---

## Próximos Passos Imediatos

1. **Esta semana:** Ana Ferreira confirma orçamento-alvo (recomendado vs. económico) — prazo: 16 Jun 2025
2. **Semana 2:** RC Arquitectos submete proposta de honorários detalhada para aprovação
3. **Semana 3:** Reunião de conceito com Sofia Menezes Studio — apresentação moodboard + paleta final
4. **Semana 4:** Eng.ª Carla Nunes realiza inspecção técnica ao imóvel (estrutura + MEP existente)
5. **Semana 6:** Aprovação projecto → início processo licenciamento CM Lisboa

---
*Roadmap gerado por DARIO/DIVA em 2025-06-12. Dados baseados em diagnóstico e briefing de Maio 2025.*
*Próxima revisão: após adjudicação de empreiteiro (Semana 9).*
```

---

## Output anti-patterns

- Budget sem valores EUR calculados — percentagens sozinhas não são entregáveis de cliente
- Timeline com fases em sequência pura sem sobreposições realistas (ex: MEP que começa só depois de obra 100% concluída)
- Milestones sem responsável nomeado — "cliente decide" sem nome não gera accountability
- Design Direction genérica sem hex codes, sem materiais com marca/origem específica
- Riscos formulados como preocupações vagas ("pode atrasar", "pode custar mais") em vez de eventos com impacto quantificado
- Equipa com colunas vazias ou "A definir" sem prazo para definição — sinaliza falta de síntese
- Roadmap entregue sem disclaimer de estimativa de preços (cria responsabilidade legal)
- Resumo Executivo com mais de 5 linhas ou sem o "porquê" do cliente (objectivo final/exit strategy)
- Angle-brackets `<nome>` ou `<EUR>` sobrevivendo no output final — documento nunca chega ao cliente assim
- Punch list final sem lista de todos os intervenientes — milestone de entrega de obra exige presença de todos
