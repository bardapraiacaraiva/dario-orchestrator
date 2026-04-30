---
name: dario-financial-model
description: Financial modelling — P&L forecast, cash flow projection, break-even analysis, scenario planning for agencies and SaaS. Uses CFO Squad frameworks. Triggers on "financial model", "modelo financeiro", "P&L", "cash flow", "break-even", "forecast", "projeção financeira".
license: MIT
---

# DARIO Skill — Financial Model

## Workflow
1. RAG: `search_kb("financial model p&l cash flow break-even", collection: "dario")`
2. Gather: revenue streams, cost structure, growth assumptions, timeline
3. Build P&L (12-month + 3-year), cash flow statement, break-even point
4. Scenario analysis: optimistic / base / pessimistic
5. Output markdown with tables + save to Obsidian

## Output includes
- Monthly P&L (revenue, COGS, gross margin, OpEx, EBITDA, net income)
- Cash flow projection (operating, investing, financing)
- Break-even point (units/months)
- 3 scenarios with assumptions
- Key ratios: gross margin %, net margin %, burn rate, runway

## P&L Template

| Line Item | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Revenue** | | | | | | | | | | | | |
| Web dev projects | 8.000 | 10.000 | 9.000 | 12.000 | 11.000 | 13.000 | 7.000 | 6.000 | 14.000 | 15.000 | 12.000 | 10.000 |
| SEO retainers | 4.500 | 4.500 | 5.000 | 5.000 | 5.500 | 5.500 | 5.500 | 5.500 | 6.000 | 6.000 | 6.500 | 6.500 |
| Ads management | 2.000 | 2.500 | 2.500 | 3.000 | 3.000 | 3.500 | 2.000 | 2.000 | 3.500 | 4.000 | 3.500 | 3.000 |
| SaaS / products | 500 | 600 | 700 | 800 | 900 | 1.000 | 1.100 | 1.200 | 1.300 | 1.500 | 1.700 | 2.000 |
| **Total Revenue** | 15.000 | 17.600 | 17.200 | 20.800 | 20.400 | 23.000 | 15.600 | 14.700 | 24.800 | 26.500 | 23.700 | 21.500 |
| **COGS** | | | | | | | | | | | | |
| Freelancers / subcontract | 3.000 | 3.500 | 3.400 | 4.200 | 4.100 | 4.600 | 3.100 | 2.900 | 5.000 | 5.300 | 4.700 | 4.300 |
| Hosting / infra | 350 | 350 | 350 | 400 | 400 | 400 | 400 | 400 | 450 | 450 | 450 | 450 |
| Software licences (client) | 200 | 200 | 250 | 250 | 250 | 300 | 300 | 300 | 300 | 350 | 350 | 350 |
| **Total COGS** | 3.550 | 4.050 | 4.000 | 4.850 | 4.750 | 5.300 | 3.800 | 3.600 | 5.750 | 6.100 | 5.500 | 5.100 |
| **Gross Margin** | 11.450 | 13.550 | 13.200 | 15.950 | 15.650 | 17.700 | 11.800 | 11.100 | 19.050 | 20.400 | 18.200 | 16.400 |
| **OpEx** | | | | | | | | | | | | |
| Salários + SS (23,75%) | 6.200 | 6.200 | 6.200 | 6.200 | 6.200 | 6.200 | 6.200 | 6.200 | 6.200 | 6.200 | 6.200 | 6.200 |
| Ferramentas internas (SaaS) | 800 | 800 | 800 | 850 | 850 | 850 | 850 | 850 | 900 | 900 | 900 | 900 |
| Escritório / cowork | 500 | 500 | 500 | 500 | 500 | 500 | 500 | 500 | 500 | 500 | 500 | 500 |
| Marketing próprio | 600 | 600 | 800 | 800 | 1.000 | 1.000 | 600 | 600 | 1.200 | 1.200 | 800 | 800 |
| Contabilidade + legal | 250 | 250 | 250 | 250 | 250 | 250 | 250 | 250 | 250 | 250 | 250 | 250 |
| Outros (seguros, deslocações) | 300 | 300 | 300 | 300 | 300 | 300 | 300 | 300 | 300 | 300 | 300 | 300 |
| **Total OpEx** | 8.650 | 8.650 | 8.850 | 8.900 | 9.100 | 9.100 | 8.700 | 8.700 | 9.350 | 9.350 | 8.950 | 8.950 |
| **EBITDA** | 2.800 | 4.900 | 4.350 | 7.050 | 6.550 | 8.600 | 3.100 | 2.400 | 9.700 | 11.050 | 9.250 | 7.450 |
| Estimativa IRC (21%) | 588 | 1.029 | 914 | 1.481 | 1.376 | 1.806 | 651 | 504 | 2.037 | 2.321 | 1.943 | 1.565 |
| Derrama municipal (~1,5%) | 42 | 74 | 65 | 106 | 98 | 129 | 47 | 36 | 146 | 166 | 139 | 112 |
| **Net Income** | 2.170 | 3.798 | 3.371 | 5.464 | 5.077 | 6.665 | 2.403 | 1.860 | 7.518 | 8.564 | 7.169 | 5.774 |

> **Nota:** Valores em EUR. Agosto é tipicamente o mês mais fraco (férias). SS patronal de 23,75% já incluída nos salários.

## Cash Flow Template

```
DEMONSTRAÇÃO DE FLUXOS DE CAIXA (mensal)
=========================================

ACTIVIDADES OPERACIONAIS
  (+) Recebimentos de clientes
  (-) Pagamentos a fornecedores e freelancers
  (-) Pagamentos de salários e SS
  (-) Pagamentos de OpEx (ferramentas, escritório, etc.)
  (-) Pagamentos de IRC / IVA / derrama
  (=) Cash flow operacional
  
ACTIVIDADES DE INVESTIMENTO
  (-) Aquisição de equipamento (portáteis, monitores)
  (-) Desenvolvimento de software próprio (SaaS)
  (-) Depósitos / cauções
  (=) Cash flow de investimento

ACTIVIDADES DE FINANCIAMENTO
  (+) Injeções de capital / empréstimos
  (-) Reembolsos de empréstimos
  (-) Distribuição de dividendos
  (=) Cash flow de financiamento

VARIAÇÃO LÍQUIDA DE CAIXA = Operacional + Investimento + Financiamento
SALDO INICIAL DE CAIXA
SALDO FINAL DE CAIXA
```

### Regras de timing para agências PT
- **Recebimentos:** 30-60 dias após faturação (PMR médio agências PT: 45 dias)
- **Pagamentos a freelancers:** 15-30 dias
- **IVA:** trimestral (até dia 15 do 2º mês seguinte ao trimestre)
- **IRC:** pagamentos por conta em Jul, Set, Dez + acerto em Mai do ano seguinte
- **SS:** até dia 20 do mês seguinte
- **Retenção na fonte:** até dia 20 do mês seguinte (se aplicável)

## Break-Even Formula

```
Break-Even Mensal = Custos Fixos / (1 - Rácio Custos Variáveis)
```

Onde:
- **Custos Fixos** = salários + SS + escritório + ferramentas + contabilidade + seguros
- **Custos Variáveis** = freelancers + hosting + licenças cliente (tipicamente 20-25% da receita)
- **Rácio Custos Variáveis** = Total Custos Variáveis / Receita Total

### Exemplo Trabalhado

| Componente | Valor |
|---|---|
| Custos fixos mensais | 8.650 EUR |
| Rácio custos variáveis | 23,7% (3.550 / 15.000) |
| **Break-even** | 8.650 / (1 - 0,237) = **11.336 EUR/mês** |
| Dias úteis/mês | 22 |
| Break-even diário | 515 EUR/dia |
| Break-even por pessoa (3 FTE) | 3.779 EUR/mês per capita |

> Se a agência fatura 15.000 EUR/mês, tem uma margem de segurança de 32% acima do break-even.
> 
> **Margem de segurança** = (Receita - Break-even) / Receita = (15.000 - 11.336) / 15.000 = 24,4%

## Scenario Analysis

| Indicador | Pessimista (-20%) | Base | Otimista (+30%) |
|---|---|---|---|
| **Receita anual** | 192.720 EUR | 240.800 EUR | 313.040 EUR |
| **Receita mensal média** | 16.060 EUR | 20.067 EUR | 26.087 EUR |
| **COGS (%)** | 25% (pressão preços) | 23,7% | 22% (escala) |
| **COGS anual** | 48.180 EUR | 57.070 EUR | 68.869 EUR |
| **Gross Margin** | 144.540 EUR | 183.730 EUR | 244.171 EUR |
| **OpEx anual** | 104.400 EUR (cortes) | 107.400 EUR | 115.000 EUR (contratação) |
| **EBITDA** | 40.140 EUR | 76.330 EUR | 129.171 EUR |
| **EBITDA %** | 20,8% | 31,7% | 41,3% |
| **IRC + derrama** | 9.032 EUR | 17.174 EUR | 29.063 EUR |
| **Net Income** | 31.108 EUR | 59.156 EUR | 100.108 EUR |
| **Net Margin %** | 16,1% | 24,6% | 32,0% |
| **Runway (3 meses custos)** | Apertado — reduzir custos | Confortável | Investir em crescimento |

### Pressupostos por cenário
- **Pessimista:** perda de 1-2 clientes retainer, mercado em contração, projetos menores, agosto/dezembro fracos
- **Base:** crescimento orgânico moderado, retenção de clientes estável, mix de serviços equilibrado
- **Otimista:** entrada de 2-3 clientes grandes, upsell de serviços existentes, SaaS revenue a crescer 2x

## PT-Specific Notes

### IVA (Imposto sobre o Valor Acrescentado)
- **Taxa normal:** 23% (serviços digitais, consultoria, publicidade)
- **Regime:** Mensal se volume > 650.000 EUR/ano, trimestral abaixo
- **Declaração periódica:** até dia 10 do 2º mês seguinte (mensal) ou dia 15 (trimestral)
- **Reverse charge:** Serviços a clientes B2B noutros estados-membros UE — IVA 0% com menção obrigatória
- **Reembolsos:** Se IVA dedutível > IVA liquidado, pedido de reembolso via declaração periódica

### IRC (Imposto sobre o Rendimento de Pessoas Colectivas)
- **Taxa normal:** 21%
- **PME (até 50.000 EUR matéria colectável):** 17% nos primeiros 50.000 EUR
- **Derrama municipal:** 0% a 1,5% (varia por município — Lisboa 1,5%, Porto 1,5%)
- **Derrama estadual:** 3% sobre lucro 1,5M-7,5M; 5% sobre 7,5M-35M; 9% acima 35M
- **Pagamentos por conta:** 3 prestações (Julho, Setembro, Dezembro) = 75-95% do IRC anterior
- **Declaração Modelo 22:** até 31 de Maio do ano seguinte

### Tributação Autónoma
- **Despesas não documentadas:** 50% (70% se prejuízo fiscal)
- **Encargos com viaturas:** 10% (custo <27.500), 27,5% (27.500-35.000), 35% (>35.000)
- **Despesas de representação:** 10%
- **Ajudas de custo não faturadas:** 5%
- **Bónus e participações de lucros (>25.000 EUR):** 35%
- **ATENÇÃO:** Tributação autónoma aplica-se MESMO com prejuízo fiscal — agrava 10 pontos percentuais

### Segurança Social
- **Contribuição entidade patronal:** 23,75%
- **Contribuição trabalhador:** 11%
- **Gerentes (MOE):** podem optar por regime de trabalhadores independentes (21,4% sobre 70% do rendimento)
- **Trabalhadores independentes (recibos verdes):** 21,4% sobre 70% do rendimento relevante
- **Pagamento:** até dia 20 do mês seguinte
- **Isenção 1º ano:** novos trabalhadores independentes (12 meses)

### Retenção na Fonte
- **Categoria B (recibos verdes a empresa):** 25% (rendimentos profissionais)
- **Dispensa de retenção:** se prestador não atingiu 14.500 EUR no ano anterior
- **Rendimentos pagos a não residentes:** 25% (salvo convenção dupla tributação)

## Save Location

```
Obsidian: C:\Users\barda\OneDrive\Documents\D.A.R.I.O\05 - Claude - IA\Outputs\YYYY-MM-DD - Financial Model - [Cliente/Projeto].md
```

Guardar automaticamente quando o modelo financeiro for gerado. Incluir frontmatter:
```yaml
---
type: financial-model
client: "[nome]"
project: "[projeto]"
date: YYYY-MM-DD
status: draft | reviewed | approved
revenue_monthly_avg: "[valor]"
break_even: "[valor]"
scenario: base | optimistic | pessimistic
---
```

## Red Flags

Alertar SEMPRE que qualquer destas situações for detectada:

| Red Flag | Limiar | Acção |
|---|---|---|
| Net margin negativa 2+ meses | < 0% por 2 meses consecutivos | PARAR — reestruturar custos imediatamente |
| Gross margin abaixo de 50% | < 50% | Renegociar freelancers ou aumentar preços |
| Cash runway < 3 meses | Saldo caixa / burn mensal < 3 | Congelar investimentos, acelerar cobranças |
| PMR > 60 dias | Prazo médio recebimento > 60 dias | Implementar cobrança proactiva, rever condições pagamento |
| Concentração de cliente > 40% | Um cliente > 40% da receita | RISCO GRAVE — diversificar carteira urgente |
| OpEx > 60% da receita | Total OpEx / Receita > 60% | Rever equipa, ferramentas, cortar não essenciais |
| EBITDA margin < 15% | EBITDA / Receita < 15% | Agência não é sustentável — rever modelo de negócio |
| IVA em atraso | Qualquer declaração não entregue | URGENTE — multas + juros automáticos da AT |
| Tributação autónoma crescente | TA > 5% do lucro | Rever política de despesas, documentação |
| Freelancer > 50% do COGS | Sem equipa interna suficiente | Risco operacional — considerar contratação |
