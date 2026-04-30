---
name: adriana-reporting
description: "ADRIANA Admin Reporting — monthly dashboard, KPIs (cost/employee, space utilization, vendor performance)"
version: "1.0"
---

# ADRIANA-REPORTING: Dashboard e Reporting Administrativo

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** relatorio, dashboard, KPI, metricas, custo por colaborador, indicadores, performance, painel controlo, reporting, relatorio mensal, estatisticas, analise custos administrativos
**Trigger words (EN):** report, dashboard, KPI, metrics, cost per employee, indicators, performance, reporting, monthly report, statistics, admin cost analysis, space utilization

Activar quando o utilizador precisa de:
- Gerar relatorio administrativo mensal
- Definir ou monitorar KPIs admin
- Criar dashboard de gestao admin
- Analisar custos administrativos
- Benchmarking de eficiencia operacional
- Preparar report para direccao

## Workflow Passo-a-Passo

### 1. KPIs Administrativos

#### Custos Operacionais
| KPI | Formula | Meta | Frequencia |
|-----|---------|------|-----------|
| Custo admin/colaborador | Total custos admin / N colaboradores | <€X/mes | Mensal |
| Custo escritorio/m2 | (Renda + utilidades + manutencao) / m2 | <€X/m2 | Mensal |
| Custo IT/colaborador | Total custos IT / N colaboradores | <€X/mes | Mensal |
| % custos admin vs receita | Total custos admin / Receita total x 100 | <X% | Mensal |
| Custo viagens/colaborador | Total viagens / N colaboradores viajantes | <€X/mes | Mensal |
| Custo material/colaborador | Total material / N colaboradores | <€X/mes | Mensal |

#### Eficiencia Operacional
| KPI | Formula | Meta | Frequencia |
|-----|---------|------|-----------|
| Taxa utilizacao espacos | Horas ocupadas / Horas disponiveis x 100 | >60% | Semanal |
| Tempo resolucao manutencao | Media dias entre pedido e resolucao | <3 dias | Mensal |
| Taxa conformidade politicas | Politicas assinadas / Total obrigatorio x 100 | 100% | Trimestral |
| SOPs documentados | SOPs existentes / Processos identificados x 100 | >80% | Trimestral |
| Taxa onboarding completo | Onboardings 100% / Total onboardings | >95% | Mensal |

#### Fornecedores
| KPI | Formula | Meta | Frequencia |
|-----|---------|------|-----------|
| Score medio fornecedores | Media scores scorecard | >3.5/5 | Trimestral |
| Prazo medio pagamento | Media dias entre factura e pagamento | 30 dias | Mensal |
| N fornecedores activos | Contagem | Monitorar | Trimestral |
| Poupanca em compras | (Orcamento - Real) / Orcamento x 100 | >5% | Trimestral |

#### Pessoas
| KPI | Formula | Meta | Frequencia |
|-----|---------|------|-----------|
| eNPS | Promotores - Detractores | >30 | Trimestral |
| Taxa presenca reunioes | Presentes / Convocados x 100 | >80% | Mensal |
| Accoes pendentes reunioes | Contagem accoes em atraso | <10 | Semanal |
| Taxa abertura newsletter | Aberturas / Envios x 100 | >70% | Mensal |
| Rotatividade (turnover) | Saidas / Media colaboradores x 100 | <15% anual | Trimestral |

### 2. Dashboard Mensal

```markdown
# Dashboard Administrativo — [Mes/Ano]
**Gerado em:** YYYY-MM-DD
**Periodo:** YYYY-MM-01 a YYYY-MM-DD

---

## RESUMO EXECUTIVO
[3-5 frases: principais resultados, desvios, accoes requeridas]

---

## CUSTOS OPERACIONAIS

### Orcamento vs Real
| Categoria | Orcamento | Real | Desvio | Desvio % |
|-----------|----------|------|--------|---------|
| Renda + condominio | €X.XXX | €X.XXX | €XXX | X% |
| Utilidades (agua, luz, gas, net) | €XXX | €XXX | €XX | X% |
| Material escritorio | €XXX | €XXX | €XX | X% |
| Limpeza | €XXX | €XXX | €XX | X% |
| Manutencao | €XXX | €XXX | €XX | X% |
| Viagens e deslocacoes | €X.XXX | €X.XXX | €XXX | X% |
| Frota | €X.XXX | €X.XXX | €XXX | X% |
| Seguros | €XXX | €XXX | €XX | X% |
| Telefone/comunicacoes | €XXX | €XXX | €XX | X% |
| Formacao | €XXX | €XXX | €XX | X% |
| Outros | €XXX | €XXX | €XX | X% |
| **TOTAL** | **€XX.XXX** | **€XX.XXX** | **€XXX** | **X%** |

### Custo per Capita
- **Custo admin total / colaborador:** €XXX /mes
- **Custo escritorio / m2:** €XX /m2/mes
- **Tendencia 3 meses:** ↑ / → / ↓

---

## INSTALACOES E ESPACOS

### Utilizacao
| Espaco | Capacidade | Utilizacao | Tendencia |
|--------|-----------|-----------|-----------|
| Postos trabalho | XX | XX% | → |
| Sala reuniao A | 8 | XX% | ↑ |
| Sala reuniao B | 4 | XX% | ↓ |

### Manutencao
- Pedidos abertos: X
- Pedidos resolvidos este mes: X
- Tempo medio resolucao: X dias
- Custo manutencao: €XXX

---

## FORNECEDORES

### Performance
| Fornecedor | Score | Tendencia | Facturacao | Prazo pgto |
|------------|-------|-----------|-----------|-----------|
| [Nome] | X.X/5 | → | €X.XXX | XX dias |
| [Nome] | X.X/5 | ↑ | €X.XXX | XX dias |

### Compras
- POs emitidas: X (€XX.XXX)
- Poupanca vs orcamento: X%

---

## PESSOAS E CULTURA

| Indicador | Valor | Meta | Status |
|-----------|-------|------|--------|
| Colaboradores activos | XX | — | — |
| Entradas este mes | X | — | — |
| Saidas este mes | X | — | — |
| eNPS | XX | >30 | OK/NOK |
| Taxa presenca town hall | XX% | >80% | OK/NOK |
| Newsletter abertura | XX% | >70% | OK/NOK |

---

## CONFORMIDADE

| Item | Estado | Nota |
|------|--------|------|
| Politicas actualizadas | X/X | — |
| SST: inspeccao em dia | Sim/Nao | [Data] |
| Extintores | OK/NOK | [Data verificacao] |
| Medicina trabalho | XX% em dia | [Proximos exames] |
| SOPs documentados | XX% | X por documentar |
| RGPD: ROPA actualizado | Sim/Nao | [Data] |

---

## FROTA E ACTIVOS

| Indicador | Valor |
|-----------|-------|
| Veiculos activos | X |
| Custo frota total | €X.XXX |
| Custo medio/veiculo | €XXX |
| IPOs a vencer (30 dias) | X |
| Seguros a renovar (30 dias) | X |

---

## ALERTAS E ACCOES

### Alertas Criticos
| # | Alerta | Impacto | Accao | Responsavel | Prazo |
|---|--------|---------|-------|-------------|-------|
| 1 | [Alerta] | [Alto/Medio] | [Accao] | [Nome] | DD/MM |

### Accoes do Mes Anterior
| # | Accao | Estado | Nota |
|---|-------|--------|------|
| 1 | [Accao] | Concluida/Pendente/Atrasada | [Nota] |

---

## PROXIMOS 30 DIAS

| Data | Evento/Deadline | Responsavel |
|------|----------------|-------------|
| DD/MM | [Item] | [Nome] |

---
*Relatorio gerado por ADRIANA — Proxima edicao: YYYY-MM-DD*
```

### 3. Relatorio Trimestral (extensao)

Adicionar ao dashboard mensal:
- Comparativo trimestral (Q vs Q anterior vs Q ano anterior)
- Scorecards de fornecedores
- Auditoria de conformidade completa
- Revisao de SOPs (quais rever/criar)
- Plano de accao para proximo trimestre
- Analise de tendencias (graficos sugeridos)

### 4. Relatorio Anual (extensao)

Adicionar:
- Resumo executivo do ano
- Comparativo anual completo
- ROI de iniciativas implementadas
- Benchmark com sector/mercado
- Orcamento proximo ano (proposta)
- Plano estrategico admin proximo ano

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana report monthly [mes]` | Dashboard mensal completo |
| `adriana report quarterly [Q]` | Relatorio trimestral |
| `adriana report annual [ano]` | Relatorio anual |
| `adriana report kpi [area]` | KPIs por area especifica |
| `adriana report costs [periodo]` | Analise custos detalhada |
| `adriana report vendors [periodo]` | Performance fornecedores |
| `adriana report compliance` | Estado conformidade |
| `adriana report custom [params]` | Relatorio personalizado |

## Template de Output

```markdown
## Sumario Executivo — [Periodo]

### Saude Operacional: [VERDE/AMARELO/VERMELHO]

**Custos:** €XX.XXX (X% vs orcamento) [OK/ATENCAO/CRITICO]
**Conformidade:** XX% [OK/ATENCAO/CRITICO]
**Satisfacao:** eNPS XX [OK/ATENCAO/CRITICO]
**Fornecedores:** Score medio X.X/5 [OK/ATENCAO/CRITICO]

### Top 3 Conquistas
1. [Conquista]
2. [Conquista]
3. [Conquista]

### Top 3 Preocupacoes
1. [Preocupacao] — Accao: [Accao]
2. [Preocupacao] — Accao: [Accao]
3. [Preocupacao] — Accao: [Accao]
```

## Red Flags

- Dashboard nao produzido ha >2 meses
- KPIs sem meta definida (medir sem objectivo)
- Metricas manipuladas ou incompletas
- Desvio orcamental >15% sem justificacao
- Tendencia negativa em 3+ meses consecutivos
- Accoes criticas sem responsavel ou prazo
- Relatorio nao partilhado com stakeholders
- Dados de diferentes fontes contraditorios
- Foco so em custos, negligenciando qualidade/satisfacao

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-facilities** | Dados de utilizacao e manutencao |
| **adriana-procurement** | Dados de fornecedores e compras |
| **adriana-travel** | Dados de viagens e despesas |
| **adriana-fleet** | Dados de frota e activos |
| **adriana-inventory** | Dados de consumo material |
| **adriana-comms** | Metricas de engagement |
| **adriana-meetings** | Metricas de reunioes |
| **adriana-onboarding** | Dados de onboarding/offboarding |
| **adriana-policies** | Dados de conformidade |
| **adriana-archive** | Dados de arquivo e retencao |
| **adriana-calendar** | Capacidade e ausencias |
| **lucas-finance** | Dados financeiros e contabilisticos |
| **dario-data** | Frameworks de analytics |
| **dario-obsidian-save** | Dashboard salvo no vault Obsidian |

## Boas Praticas de Reporting

- **Regra 5-15-30:** Resumo executivo em 5 linhas, dashboard em 15 min de leitura, detalhe completo em 30 paginas max
- **Semaforo:** Verde (OK), Amarelo (atencao), Vermelho (critico) — visual e imediato
- **Tendencias > Numeros:** Uma seta (↑↓→) comunica mais que um numero isolado
- **Accoes > Diagnostico:** Cada problema identificado deve ter accao associada
- **Periodicidade:** Mensal para operacional, trimestral para tactico, anual para estrategico
- **Audiencia:** Adaptar nivel de detalhe ao receptor (CEO vs Operations)
