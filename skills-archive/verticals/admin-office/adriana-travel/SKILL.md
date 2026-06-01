---
name: adriana-travel
description: "ADRIANA Travel & Expenses — policy, booking, expense reports, per diem, approval workflows"
version: "1.0"
---

# ADRIANA-TRAVEL: Viagens e Despesas

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** viagem, despesa, ajudas de custo, per diem, bilhete aviao, hotel, reserva, nota de despesas, reembolso, deslocacao, quilometros, km, alojamento, transporte
**Trigger words (EN):** travel, expense, per diem, booking, flight, hotel, expense report, reimbursement, mileage, travel policy, corporate travel, business trip

Activar quando o utilizador precisa de:
- Planear uma viagem de negocios
- Criar ou consultar politica de viagens
- Submeter nota de despesas
- Calcular ajudas de custo / per diem
- Aprovacao de despesas de viagem
- Comparar opcoes de transporte/alojamento

## Workflow Passo-a-Passo

### 1. Pre-Viagem: Pedido e Aprovacao

```markdown
# Pedido de Viagem
**Ref:** VIA-YYYY-NNN
**Data pedido:** YYYY-MM-DD
**Colaborador:** [Nome]
**Departamento:** [Dept]

## Detalhes
- **Destino:** [Cidade/Pais]
- **Data ida:** YYYY-MM-DD
- **Data volta:** YYYY-MM-DD
- **Motivo:** [Reuniao cliente / Conferencia / Formacao / etc.]
- **Participantes:** [Quem mais vai]

## Orcamento Estimado
| Item | Estimativa |
|------|-----------|
| Transporte (voo/comboio/carro) | €XXX |
| Alojamento (X noites x €XX) | €XXX |
| Ajudas de custo (X dias x €XX) | €XXX |
| Outros (taxi, parking, visa) | €XXX |
| **Total estimado** | **€XXX** |

## Aprovacao
- [ ] Chefia directa: [Nome] — Data: ___
- [ ] Financeiro (se >€1.000): [Nome] — Data: ___
```

### 2. Politica de Viagens (Referencia)

**Transporte:**
| Meio | Regra |
|------|-------|
| Aviao | Classe economica (business se >4h e aprovado) |
| Comboio | 1a classe se >2h |
| Carro proprio | €0.36/km (Portaria 1553-D/2008) |
| Carro empresa | Sem reembolso km, combustivel empresa |
| Taxi/TVDE | Permitido aeroporto-hotel e horario nocturno |
| Rent-a-car | Pre-aprovacao obrigatoria |

**Alojamento:**
| Localizacao | Limite/noite |
|-------------|-------------|
| Lisboa/Porto | €120 |
| Outras cidades PT | €90 |
| Europa | €150 |
| Fora Europa | €200 |
| Excepcoes | Aprovacao director |

**Ajudas de Custo (PT — valores fiscais isentos 2026):**
| Tipo | Nacional | Estrangeiro |
|------|----------|-------------|
| Almoco | €6.41 | €13.98 |
| Jantar | €6.41 | €13.98 |
| Alojamento | €62.75 | €148.91 |
| Dia completo | €75.57 | €176.87 |

*Nota: Verificar sempre valores actualizados na Portaria em vigor*

### 3. Durante a Viagem

Regras de despesas:
- Guardar TODOS os recibos/facturas (com NIF empresa)
- Fotografar recibos no momento (backup digital)
- Refeicoes: limite razoavel, sem bebidas alcoolicas em despesas
- Despesas pessoais nao sao reembolsaveis
- Wi-fi e chamadas profissionais: reembolsaveis

### 4. Pos-Viagem: Nota de Despesas

Submeter em 5 dias uteis apos regresso.

```markdown
# Nota de Despesas
**Ref:** DESP-YYYY-NNN
**Colaborador:** [Nome] | **NIF:** [NIF]
**Viagem:** VIA-YYYY-NNN
**Periodo:** YYYY-MM-DD a YYYY-MM-DD
**Destino:** [Local]

## Despesas Detalhadas
| Data | Descricao | Categoria | Valor | Recibo |
|------|-----------|-----------|-------|--------|
| YYYY-MM-DD | [Desc] | Transporte | €XX.XX | Sim/Nao |
| YYYY-MM-DD | [Desc] | Alojamento | €XX.XX | Sim/Nao |
| YYYY-MM-DD | [Desc] | Refeicao | €XX.XX | Sim/Nao |
| YYYY-MM-DD | [Desc] | Outros | €XX.XX | Sim/Nao |

## Resumo
| Categoria | Total |
|-----------|-------|
| Transporte | €XX.XX |
| Alojamento | €XX.XX |
| Refeicoes | €XX.XX |
| Ajudas custo | €XX.XX |
| Outros | €XX.XX |
| **TOTAL** | **€XXX.XX** |

## Aprovacao
- [ ] Chefia directa: [Nome] — Data: ___
- [ ] Financeiro: [Nome] — Data: ___
- [ ] Reembolso processado: Data: ___
```

### 5. Workflow de Aprovacao

```
PEDIDO → APROVACAO CHEFIA → APROVACAO FINANCEIRO (se >€1.000)
                                    ↓
VIAGEM → NOTA DESPESAS → VALIDACAO → REEMBOLSO (max 15 dias uteis)
```

Niveis de aprovacao:
| Valor | Aprovador |
|-------|-----------|
| <€500 | Chefia directa |
| €500-€2.000 | Director departamento |
| €2.000-€5.000 | Director geral |
| >€5.000 | Administracao |

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana travel request` | Gerar pedido de viagem |
| `adriana travel expense [viagem]` | Gerar nota de despesas |
| `adriana travel perdiem [destino] [dias]` | Calcular ajudas de custo |
| `adriana travel policy` | Mostrar politica de viagens |
| `adriana travel compare [opcoes]` | Comparar opcoes transporte/hotel |
| `adriana travel pending` | Listar reembolsos pendentes |
| `adriana travel report [periodo]` | Relatorio despesas viagem |

## Template de Output

```markdown
## Relatorio Viagens — [Periodo]

### Metricas
- Viagens realizadas: X
- Custo total: €XX.XXX
- Custo medio/viagem: €XXX
- Despesas em conformidade: X%
- Reembolsos pendentes: €XX.XXX

### Top Destinos
1. [Destino] — X viagens — €XX.XXX
2. [Destino] — X viagens — €XX.XXX

### Alertas
- [X] notas de despesas pendentes >5 dias
- [X] despesas acima do limite sem aprovacao
```

## Red Flags

- Despesas sem recibo/factura
- Notas de despesas submetidas >15 dias apos viagem
- Despesas acima dos limites da politica sem aprovacao
- Reservas fora dos canais aprovados
- Viagens sem pedido previo aprovado
- Km declarados inconsistentes com distancia real
- Refeicoes em dias sem deslocacao comprovada
- Duplicacao de despesas (ajuda custo + refeicao no mesmo dia)

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-policies** | Politica de viagens e despesas |
| **adriana-docs** | Arquivo de notas de despesas e recibos |
| **adriana-reporting** | Custos de viagem no dashboard mensal |
| **adriana-fleet** | Viagens com veiculo da empresa |
| **adriana-calendar** | Bloqueio de calendario durante viagem |
| **adriana-procurement** | Contratos com agencias de viagem |
| **lucas-finance** | Contabilizacao e IVA das despesas |
| **dario-legal** | Seguros de viagem e cobertura |

## Contexto Portugal

- Ajudas de custo isentas IRS/SS: dentro dos limites legais (Portaria 1553-D/2008)
- Acima dos limites: tributadas como rendimento de trabalho
- Km em veiculo proprio: €0.36/km (isento ate limites legais)
- IVA recuperavel: alojamento 6%, transporte passageiros 6%, combustivel 50%
- Seguro viagem: obrigatorio para deslocacoes internacionais
- Cartao Europeu Seguro Doenca: levar em viagens UE


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **adriana-travel** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in adriana-travel:**

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
