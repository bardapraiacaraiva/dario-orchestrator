---
name: adriana-comms
description: "ADRIANA Internal Comms — newsletters, announcements, town halls, employee engagement"
version: "1.0"
---

# ADRIANA-COMMS: Comunicacao Interna

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** comunicacao interna, newsletter, anuncio, town hall, engajamento, colaboradores, email interno, mural, intranet, cultura empresa, boas-vindas, despedida, celebracao, feedback
**Trigger words (EN):** internal comms, newsletter, announcement, town hall, employee engagement, internal email, intranet, company culture, welcome, farewell, recognition, all-hands

Activar quando o utilizador precisa de:
- Criar comunicados internos
- Preparar newsletter da empresa
- Planear town halls ou all-hands
- Iniciativas de engagement
- Anuncios de entradas/saidas
- Comunicacoes de crise internas

## Workflow Passo-a-Passo

### 1. Classificacao da Comunicacao

| Tipo | Urgencia | Canal | Aprovacao |
|------|----------|-------|-----------|
| Informativo | Normal | Email + Slack | Chefia |
| Anuncio oficial | Media | Email + reuniao | Direccao |
| Urgente/Crise | Alta | Email + Slack + SMS | CEO |
| Celebracao | Baixa | Slack + mural | Nenhuma |
| Politica nova | Media | Email + assinatura | RH + Direccao |
| Mudanca organizacional | Alta | Reuniao + email | CEO |

### 2. Templates de Comunicacao

#### Anuncio Novo Colaborador
```markdown
**Assunto:** Bem-vindo/a [Nome] a equipa [Empresa]!

Ola equipa,

Temos o prazer de anunciar que [Nome Completo] se junta a nos como [Cargo] no departamento de [Departamento], a partir de [Data].

[Nome] vem de [background breve — 1-2 frases] e vai trabalhar em [area/projectos].

Factos rapidos:
- Formacao: [X]
- Fun fact: [algo pessoal partilhado pelo proprio]
- Buddy: [Nome do buddy]

Juntem-se a nos para dar as boas-vindas! O primeiro almoco de equipa sera [data].

[Assinatura RH/Chefia]
```

#### Anuncio Saida de Colaborador
```markdown
**Assunto:** [Nome] — novo capitulo

Ola equipa,

Informamos que [Nome] deixa a equipa [Empresa] a [Data], após [X] anos connosco.

Durante o seu percurso, [Nome] contribuiu para [conquistas principais — 1-2 frases].

A passagem de responsabilidades esta em curso com [Nome substituto/equipa].

Desejamos a/ao [Nome] muito sucesso no proximo desafio. O almoco de despedida sera [data/hora].

[Assinatura]
```

#### Comunicado Oficial
```markdown
**Assunto:** [Titulo claro e directo]

**Data:** YYYY-MM-DD
**De:** [Remetente/Cargo]
**Para:** [Audiencia]
**Classificacao:** [Informativo / Accao requerida / Urgente]

## Contexto
[Porque estamos a comunicar isto — 2-3 frases]

## O que muda
[Pontos claros do que e diferente — bullet points]

## O que isto significa para ti
[Impacto pratico nos colaboradores]

## Proximos passos
1. [Accao 1] — Prazo: [Data]
2. [Accao 2] — Prazo: [Data]

## Questoes
Contactar [Nome] via [canal] ate [data].

[Assinatura]
```

### 3. Newsletter Interna (Mensal)

Estrutura recomendada:
```markdown
# [Empresa] Newsletter — [Mes Ano]

## Mensagem da Direccao
[2-3 paragrafos: resultados, visao, agradecimentos]

## Destaques do Mes
- [Projecto X lancado com sucesso]
- [Cliente Y fechado]
- [Marco Z alcancado]

## Novos Rostos
- [Nome] — [Cargo] — [Fun fact]

## Aniversarios e Datas
- [Nome] — X anos na empresa (DD/MM)
- [Nome] — Aniversario (DD/MM)

## Formacao e Desenvolvimento
- [Workshop/curso disponivel]

## Agenda Proxima
| Data | Evento |
|------|--------|
| DD/MM | [Evento] |

## Curiosidade / Team Building
[Quiz, photo challenge, sugestao de livro, etc.]

## Numeros do Mes
- Projectos entregues: X
- NPS clientes: XX
- [Outra metrica relevante]
```

### 4. Town Hall / All-Hands

**Preparacao (1 semana antes):**
- [ ] Agenda definida e partilhada
- [ ] Recolher perguntas anonimas (Google Form ou similar)
- [ ] Slides preparados (max 15 slides, 30min)
- [ ] Speaker order confirmada
- [ ] Logistica (sala, link virtual, gravacao)

**Estrutura (60min max):**
| Bloco | Duracao | Responsavel |
|-------|---------|-------------|
| Abertura + resultados | 10min | CEO/Director |
| Update por departamento | 15min | Leads |
| Reconhecimento/premios | 5min | RH |
| Estrategia/visao | 10min | CEO |
| Q&A (perguntas anonimas + live) | 15min | Moderador |
| Encerramento + proximos passos | 5min | CEO |

**Pos-Town Hall:**
- [ ] Gravacao disponibilizada em 24h
- [ ] Resumo escrito enviado por email
- [ ] Perguntas nao respondidas — follow-up em 48h
- [ ] Survey de feedback (1 pergunta: NPS)

### 5. Engagement e Cultura

**Iniciativas recorrentes:**
| Iniciativa | Frequencia | Responsavel |
|------------|-----------|-------------|
| Almoco equipa | Mensal | Office manager |
| Team building | Trimestral | RH |
| Aniversarios | Continuo | Office manager |
| Feedback pulse | Trimestral | RH |
| Sugestao do mes | Mensal | Todos |
| Learning lunch | Quinzenal | Rotativo |
| Voluntariado | Semestral | Comissao |

**Metricas de Engagement:**
- eNPS (Employee Net Promoter Score): trimestral, target >30
- Taxa abertura newsletter: target >70%
- Participacao town hall: target >80%
- Sugestoes submetidas/mes: target >5

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana comms announce [tipo]` | Criar comunicado por tipo |
| `adriana comms newsletter [mes]` | Gerar estrutura newsletter mensal |
| `adriana comms townhall` | Preparar town hall completo |
| `adriana comms welcome [nome]` | Anuncio novo colaborador |
| `adriana comms farewell [nome]` | Anuncio saida colaborador |
| `adriana comms engagement` | Dashboard metricas engagement |
| `adriana comms crisis [situacao]` | Template comunicacao crise |

## Template de Output

```markdown
## Comunicacao Interna — [Periodo]

### Metricas
- Comunicados enviados: X
- Taxa abertura media: X%
- Newsletter: X edicoes — taxa abertura X%
- Town halls: X — participacao media X%
- eNPS: XX

### Calendario Proximo Mes
| Data | Comunicacao | Canal | Responsavel |
|------|------------|-------|-------------|
| DD/MM | [Item] | [Canal] | [Nome] |
```

## Red Flags

- Comunicados importantes sem versao escrita (so verbal)
- Newsletter sem periodicidade (>2 meses sem edicao)
- Town hall sem Q&A (comunicacao unidireccional)
- Anuncios de saida feitos apenas "boca a boca"
- Mudancas organizacionais comunicadas por rumor antes do oficial
- eNPS negativo sem plano de accao
- Taxa abertura newsletter <50% (problema de relevancia)
- Comunicados de crise atrasados >2h
- Sem canal para feedback anonimo

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-meetings** | Town halls e all-hands |
| **adriana-onboarding** | Anuncios de entrada e welcome pack |
| **adriana-calendar** | Eventos de equipa no calendario |
| **adriana-policies** | Comunicacao de novas politicas |
| **adriana-docs** | Templates de comunicados |
| **adriana-reporting** | Metricas engagement no dashboard |
| **dario-content** | Producao de conteudo para newsletter |
| **dario-pr** | Alinhamento comms internas-externas |
| **dario-hr** | Iniciativas de engagement e cultura |


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **adriana-comms** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in adriana-comms:**

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
