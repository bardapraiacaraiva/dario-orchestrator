---
name: adriana-calendar
description: "ADRIANA Corporate Calendar — events, PT holidays, deadlines, resource booking, capacity"
version: "1.0"
---

# ADRIANA-CALENDAR: Calendario Corporativo

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** calendario, feriado, evento, prazo, deadline, reserva sala, booking, capacidade, ausencia, ferias, ponte, tolerancia ponto, agenda empresa, dias uteis
**Trigger words (EN):** calendar, holiday, event, deadline, room booking, capacity, absence, vacation, corporate calendar, public holiday, business days, resource booking

Activar quando o utilizador precisa de:
- Consultar feriados e pontes em Portugal
- Planear eventos corporativos
- Gerir reservas de salas/recursos
- Calcular prazos em dias uteis
- Verificar capacidade de equipa
- Planear calendario anual de actividades

## Workflow Passo-a-Passo

### 1. Feriados Obrigatorios Portugal 2026

| Data | Dia | Feriado | Ponte? |
|------|-----|---------|--------|
| 01 Jan (Qui) | Quinta | Ano Novo | Ponte 02 Jan (Sex) |
| 17 Fev (Ter) | Terca | Carnaval* | Ponte possivel |
| 03 Abr (Sex) | Sexta | Sexta-Feira Santa | Weekend longo |
| 05 Abr (Dom) | Domingo | Pascoa | — |
| 25 Abr (Sab) | Sabado | Liberdade | — |
| 01 Mai (Sex) | Sexta | Trabalhador | Weekend longo |
| 04 Jun (Qui) | Quinta | Corpo de Deus | Ponte 05 Jun (Sex) |
| 10 Jun (Qua) | Quarta | Portugal | Ponte possivel |
| 15 Ago (Sab) | Sabado | Assuncao N. Sra. | — |
| 05 Out (Seg) | Segunda | Republica | Weekend longo |
| 01 Nov (Dom) | Domingo | Todos os Santos | — |
| 01 Dez (Ter) | Terca | Restauracao | Ponte possivel |
| 08 Dez (Ter) | Terca | Imaculada | Ponte possivel |
| 25 Dez (Sex) | Sexta | Natal | Weekend longo |

*Carnaval: nao e feriado obrigatorio, mas muitas empresas concedem

**Feriado municipal:** Verificar sempre o feriado do concelho (ex: Lisboa 13 Jun — Santo Antonio)

**Tolerancia de ponto 2026:** Normalmente concedida pela Administracao Publica; empresas privadas podem seguir ou nao.

### 2. Pontes Recomendadas 2026

| Ponte | Dias off | Custo (ferias) | Dias livres |
|-------|---------|----------------|-------------|
| 02 Jan (Sex) | 1 dia | 1 | 4 dias (01-04 Jan) |
| 05 Jun (Sex) | 1 dia | 1 | 4 dias (04-07 Jun) |
| 10 Jun (Qua) | 0 extra | Tolerancia? | 1 dia |

### 3. Calendario Anual da Empresa

```markdown
# Calendario Corporativo [Ano]

## Q1 (Jan-Mar)
| Mes | Evento | Data | Responsavel |
|-----|--------|------|-------------|
| Jan | Kickoff anual | 1a semana | CEO |
| Jan | Definicao OKRs | 2a semana | Todos leads |
| Fev | Entrega IRS modelo 10 | 28 Fev | Contabilidade |
| Mar | Revisao trimestral Q1 | Ultima semana | Direccao |

## Q2 (Abr-Jun)
| Mes | Evento | Data | Responsavel |
|-----|--------|------|-------------|
| Abr | Ferias Pascoa | Conforme | RH |
| Mai | Entrega IES/IRC | 31 Mai | Contabilidade |
| Jun | Team building verão | 2a quinzena | RH |
| Jun | Revisao trimestral Q2 | Ultima semana | Direccao |

## Q3 (Jul-Set)
| Mes | Evento | Data | Responsavel |
|-----|--------|------|-------------|
| Jul-Ago | Periodo ferias principal | Conforme | RH |
| Set | Back-to-office / Rentrée | 1a semana | Todos |
| Set | Revisao trimestral Q3 | Ultima semana | Direccao |

## Q4 (Out-Dez)
| Mes | Evento | Data | Responsavel |
|-----|--------|------|-------------|
| Out | Planeamento proximo ano | Outubro | Direccao |
| Nov | Black Friday / campanhas | Ultima semana | Marketing |
| Dez | Jantar de Natal | 2a/3a semana | Office manager |
| Dez | Encerramento / ferias | 24-31 Dez | Todos |
| Dez | Revisao anual / retrospectiva | Antes encerramento | Direccao |
```

### 4. Gestao de Salas e Recursos

**Regras de booking:**
- Reservar com minimo 2h antecedencia
- Cancelar se nao necessaria (liberar para outros)
- Max 2h por booking (excepto formacoes/workshops)
- Sala limpa apos utilizacao
- Equipamento desligado ao sair

**Matriz de salas:**
| Sala | Capacidade | Equipamento | Booking por |
|------|-----------|-------------|-------------|
| Sala A | 8 | Projector, whiteboard | Calendario partilhado |
| Sala B | 4 | TV, webcam | Calendario partilhado |
| Sala C | 2 | Nenhum (focus room) | Livre |
| Auditorio | 30 | Som, projector, micro | Pedido a admin |

### 5. Capacidade de Equipa

**Calculo de capacidade mensal:**
```
Dias uteis no mes: X
- Feriados: X
- Pontes empresa: X
- Media ferias planeadas: X
= Dias disponiveis: X

Capacidade = Dias disponiveis x N colaboradores x 8h
```

**Mapa de ausencias (template mensal):**
| Colaborador | S1 | S2 | S3 | S4 | S5 | Total dias off |
|-------------|----|----|----|----|----|----|
| [Nome] | | F | | | | 5 |
| [Nome] | | | D | | | 1 |
| [Nome] | | | | | F | 5 |

Legenda: F=Ferias, D=Doença, FO=Formação, P=Parentalidade, O=Outro

### 6. Deadlines Fiscais/Legais Recorrentes

| Prazo | Obrigacao | Responsavel |
|-------|-----------|-------------|
| Dia 10 cada mes | Entrega SS/IRS retencoes | Contabilidade |
| Dia 15 cada mes | IVA mensal (se aplicavel) | Contabilidade |
| 28 Fev | IRS Modelo 10 | Contabilidade |
| 31 Mar | Relatorio Unico | RH |
| 31 Mai | IES + IRC | Contabilidade |
| 30 Jun | IRS (se empresa) | Contabilidade |
| 15 Jul | Pagamento especial por conta | Contabilidade |
| 30 Nov | Mapa ferias ano seguinte | RH |

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana calendar holidays [ano]` | Feriados e pontes do ano |
| `adriana calendar events [periodo]` | Eventos corporativos |
| `adriana calendar capacity [mes]` | Capacidade equipa no mes |
| `adriana calendar deadlines [mes]` | Prazos fiscais/legais |
| `adriana calendar book [sala] [data]` | Reservar sala |
| `adriana calendar absences [mes]` | Mapa de ausencias |
| `adriana calendar workdays [inicio] [fim]` | Calcular dias uteis |

## Template de Output

```markdown
## Calendario — [Mes/Ano]

### Resumo
- Dias uteis: X
- Feriados: X ([lista])
- Pontes empresa: X
- Capacidade equipa: X dias-pessoa

### Eventos
| Data | Evento | Tipo | Responsavel |
|------|--------|------|-------------|
| DD/MM | [Evento] | [Tipo] | [Nome] |

### Ausencias Planeadas
- X colaboradores em ferias
- Capacidade efectiva: X%

### Deadlines
| Data | Obrigacao | Estado |
|------|-----------|--------|
| DD/MM | [Obrigacao] | Pendente/OK |
```

## Red Flags

- Equipa com <50% capacidade sem plano de cobertura
- Deadlines fiscais/legais nao monitorizadas
- Salas consistentemente sobrepostas (falta de booking)
- Ferias nao planeadas ate 30 Nov do ano anterior (legal)
- >70% equipa ausente simultaneamente
- Eventos corporate sem comunicacao previa >1 semana
- Feriados municipais nao contemplados no calendario
- Deadlines criticas na semana de feriados/pontes

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-meetings** | Reunioes integradas no calendario |
| **adriana-facilities** | Reserva de salas e recursos |
| **adriana-comms** | Comunicacao de eventos e ausencias |
| **adriana-travel** | Viagens no calendario, bloqueio datas |
| **adriana-reporting** | Metricas de capacidade no dashboard |
| **adriana-reception** | Visitas agendadas no calendario |
| **lucas-finance** | Deadlines fiscais e contabilisticas |
| **dario-hr** | Gestao de ferias e ausencias |

## Contexto Portugal

- Ferias anuais: minimo 22 dias uteis (Codigo Trabalho Art. 238)
- Marcacao ferias: acordo empregador-trabalhador, mapa ate 15 Abr
- Feriados: 13 obrigatorios + feriado municipal + Carnaval (facultativo)
- Tolerancia de ponto: decisao da empresa (Adm. Publica normalmente concede)
- Trabalho em feriado: compensacao conforme CT Art. 269


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **adriana-calendar** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in adriana-calendar:**

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
