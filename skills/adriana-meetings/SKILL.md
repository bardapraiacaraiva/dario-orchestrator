---
name: adriana-meetings
description: "ADRIANA Meetings — agenda prep, minutes/actas, action items, follow-ups, recurring cadence"
version: "1.0"
---

# ADRIANA-MEETINGS: Gestao de Reunioes

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** reuniao, acta, agenda, minuta, ordem de trabalhos, follow-up, seguimento, cadencia, convocatoria, accoes pendentes, pontos de accao
**Trigger words (EN):** meeting, minutes, agenda, action items, follow-up, recurring meeting, cadence, standup, retrospective, one-on-one

Activar quando o utilizador precisa de:
- Preparar agenda para uma reuniao
- Criar acta/minuta de reuniao
- Rastrear accoes e follow-ups
- Definir cadencia de reunioes recorrentes
- Gerar convocatoria formal
- Rever eficacia das reunioes

## Workflow Passo-a-Passo

### 1. Pre-Reuniao: Preparacao da Agenda

Recolher informacao:
- **Objectivo:** Qual a decisao ou resultado esperado?
- **Tipo:** Decisao / Informativa / Brainstorm / Status / Retrospectiva
- **Participantes:** Quem deve estar? Quem e opcional?
- **Duracao:** Quanto tempo necessario? (default: 30min)
- **Material previo:** Documentos a enviar com antecedencia

Template de Agenda:
```markdown
# Agenda: [Titulo da Reuniao]
**Data:** YYYY-MM-DD HH:MM
**Local/Link:** [Presencial/Teams/Zoom]
**Organizador:** [Nome]
**Participantes:** [Lista]
**Duracao:** XX min

## Objectivo
[Frase clara do que se pretende decidir/alcançar]

## Pontos da Agenda
| # | Topico | Responsavel | Tempo | Tipo |
|---|--------|-------------|-------|------|
| 1 | [Topico] | [Nome] | Xmin | Info/Decisao |
| 2 | [Topico] | [Nome] | Xmin | Info/Decisao |
| 3 | Pontos abertos / AOB | Todos | 5min | Aberto |

## Material Previo
- [ ] [Documento/link a consultar antes]

## Notas
[Contexto relevante]
```

### 2. Durante a Reuniao: Captura

Estrutura de notas em tempo real:
- Decisoes tomadas (com quem decidiu)
- Accoes atribuidas (quem, o que, quando)
- Topicos adiados (para proxima reuniao)
- Riscos ou bloqueios identificados

### 3. Pos-Reuniao: Acta

Template de Acta:
```markdown
# Acta: [Titulo da Reuniao]
**Data:** YYYY-MM-DD HH:MM-HH:MM
**Local:** [Local/Link]
**Presentes:** [Lista]
**Ausentes:** [Lista]
**Redactor:** [Nome]

## Resumo Executivo
[2-3 frases com principais decisoes]

## Discussao por Topico

### 1. [Topico]
- Apresentado por: [Nome]
- Discussao: [Pontos-chave]
- **Decisao:** [O que ficou decidido]

### 2. [Topico]
- ...

## Accoes
| # | Accao | Responsavel | Prazo | Estado |
|---|-------|-------------|-------|--------|
| 1 | [Accao] | [Nome] | YYYY-MM-DD | Pendente |
| 2 | [Accao] | [Nome] | YYYY-MM-DD | Pendente |

## Proxima Reuniao
- **Data:** YYYY-MM-DD HH:MM
- **Topicos a retomar:** [Lista]

---
*Acta aprovada por: [Nome] em YYYY-MM-DD*
```

### 4. Follow-Up

- Enviar acta em 24h uteis
- Lembrete de accoes pendentes 48h antes do prazo
- Revisao de accoes no inicio da proxima reuniao
- Escalar accoes em atraso >7 dias

### 5. Cadencia Recomendada

| Tipo | Frequencia | Duracao | Participantes |
|------|-----------|---------|---------------|
| Daily standup | Diario | 15min | Equipa |
| Reuniao equipa | Semanal | 45min | Equipa + Lead |
| 1:1 Manager | Quinzenal | 30min | 2 pessoas |
| Reuniao cliente | Semanal/Quinzenal | 30-60min | PM + Cliente |
| Retrospectiva | Mensal | 60min | Equipa |
| Reuniao estrategica | Trimestral | 90min | Lideranca |
| Town Hall | Trimestral | 60min | Todos |
| Board review | Semestral | 120min | Administracao |

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana meeting agenda [titulo]` | Gerar template de agenda |
| `adriana meeting minutes [titulo]` | Gerar template de acta |
| `adriana meeting actions` | Listar accoes pendentes de reunioes |
| `adriana meeting followup [reuniao]` | Gerar email de follow-up |
| `adriana meeting cadence [equipa]` | Recomendar cadencia de reunioes |
| `adriana meeting review [periodo]` | Analisar eficacia das reunioes |
| `adriana meeting convocatoria` | Gerar convocatoria formal |

## Template de Output

```markdown
## Resumo de Reunioes — [Periodo]

### Metricas
- Reunioes realizadas: X
- Horas totais: Xh
- Taxa de presenca media: X%
- Accoes geradas: X
- Accoes concluidas: X (Y%)
- Accoes em atraso: X

### Top Decisoes
1. [Decisao] — [Data]
2. [Decisao] — [Data]

### Accoes Criticas Pendentes
| Accao | Responsavel | Prazo | Atraso |
|-------|-------------|-------|--------|
| [Accao] | [Nome] | [Data] | X dias |
```

## Red Flags

- Reunioes sem agenda definida previamente
- Reunioes sem acta registada em 48h
- Accoes sem responsavel ou prazo atribuido
- Reunioes recorrentes sem participacao justificada (>3 ausencias)
- Reunioes que excedem sistematicamente o tempo previsto (>20%)
- Mesmas accoes pendentes em 3+ reunioes consecutivas
- Reunioes com >8 participantes sem facilitador designado
- Reunioes informativas que podiam ser email
- Falta de decisoes claras no final da reuniao

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-docs** | Actas seguem nomenclatura e arquivo documental |
| **adriana-calendar** | Reunioes integradas no calendario corporativo |
| **adriana-comms** | Town halls e reunioes gerais via comms internas |
| **adriana-sop** | SOPs para conduzir cada tipo de reuniao |
| **adriana-reporting** | Metricas de reunioes no dashboard mensal |
| **adriana-reception** | Reunioes presenciais com visitantes |
| **dario-orchestrator** | Accoes de reunioes podem gerar tasks no taskboard |
| **dario-projeto** | Contexto de projecto carregado para reuniao de cliente |

## Boas Praticas

- **Regra dos 2 pizzas:** Se a reuniao nao alimenta com 2 pizzas, tem gente a mais
- **No agenda, no attenda:** Sem agenda, nao aceitar convite
- **Accoes SMART:** Especificas, Mensuraveis, Atribuidas, Realistas, com Tempo
- **Standing meetings:** Standups de pe para manter brevidade
- **Parking lot:** Topicos fora de ambito vao para lista separada
- **Rotacao de facilitador:** Em reunioes recorrentes, rodar quem facilita


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **adriana-meetings** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in adriana-meetings:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->
