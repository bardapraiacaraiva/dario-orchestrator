---
name: adriana-procurement
description: "ADRIANA Procurement — RFP/RFQ, vendor evaluation matrix, contract checklists, POs, supplier scorecards"
version: "1.0"
---

# ADRIANA-PROCUREMENT: Compras e Fornecedores

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** compras, fornecedor, RFP, RFQ, proposta, avaliacao fornecedores, contrato fornecedor, ordem de compra, purchase order, scorecard, procurement, licitacao, adjudicacao, comparar propostas
**Trigger words (EN):** procurement, vendor, supplier, RFP, RFQ, purchase order, PO, vendor evaluation, contract checklist, supplier scorecard, sourcing, tender

Activar quando o utilizador precisa de:
- Lancar um RFP ou RFQ
- Avaliar e comparar fornecedores
- Criar checklist de contratos com fornecedores
- Emitir ordens de compra
- Monitorizar performance de fornecedores
- Negociar condicoes comerciais

## Workflow Passo-a-Passo

### 1. Identificacao da Necessidade
- Definir o que se pretende comprar (produto/servico)
- Estimar orcamento disponivel
- Definir prazo de entrega necessario
- Verificar se existe contrato-quadro ou fornecedor preferencial
- Determinar nivel de aprovacao necessario

### 2. Solicitar Propostas (RFP/RFQ)

**RFQ (Request for Quotation)** — para produtos/servicos simples, preco e principal criterio
**RFP (Request for Proposal)** — para servicos complexos, avaliacao multi-criterio

Template RFP:
```markdown
# Request for Proposal: [Titulo]

**Ref:** RFP-YYYY-NNN
**Data emissao:** YYYY-MM-DD
**Data limite respostas:** YYYY-MM-DD
**Contacto:** [Nome, email]

## 1. Apresentacao da Empresa
[Breve descricao]

## 2. Ambito do Projecto
[Descricao detalhada do que se pretende]

## 3. Requisitos
### Obrigatorios
- [ ] [Requisito 1]
- [ ] [Requisito 2]
### Desejaveis
- [ ] [Requisito 1]

## 4. Criterios de Avaliacao
| Criterio | Peso |
|----------|------|
| Preco | 30% |
| Qualidade tecnica | 25% |
| Experiencia/Referencias | 20% |
| Prazo de entrega | 15% |
| Suporte pos-venda | 10% |

## 5. Formato da Resposta
[Instrucoes de como responder]

## 6. Condicoes Gerais
- Validade da proposta: 30 dias
- Condicoes de pagamento esperadas
- Penalidades por incumprimento
```

### 3. Avaliacao de Fornecedores

Matriz de avaliacao (pontuar 1-5 cada criterio):

| Criterio | Peso | Fornecedor A | Fornecedor B | Fornecedor C |
|----------|------|-------------|-------------|-------------|
| Preco competitivo | 30% | _ | _ | _ |
| Qualidade tecnica | 25% | _ | _ | _ |
| Experiencia sector | 20% | _ | _ | _ |
| Prazo entrega | 15% | _ | _ | _ |
| Suporte/Garantia | 10% | _ | _ | _ |
| **Score ponderado** | 100% | **_** | **_** | **_** |

Formula: Score = SUM(Pontuacao x Peso)

### 4. Checklist Contrato Fornecedor

- [ ] Identificacao completa das partes (NIF, morada, representante)
- [ ] Ambito e descricao detalhada dos servicos/produtos
- [ ] Preco, condicoes de pagamento e revisao de precos
- [ ] Prazo de entrega e penalidades por atraso
- [ ] Garantias e periodo de garantia
- [ ] SLAs (Service Level Agreements) se aplicavel
- [ ] Clausula de confidencialidade / NDA
- [ ] Proteccao de dados (RGPD) se aplicavel
- [ ] Propriedade intelectual
- [ ] Condicoes de rescisao e pre-aviso
- [ ] Foro competente e lei aplicavel
- [ ] Seguro de responsabilidade civil
- [ ] Clausula anticorrupcao
- [ ] Assinaturas autorizadas

### 5. Ordem de Compra (PO)

```markdown
# Ordem de Compra
**Ref:** PO-YYYY-NNN
**Data:** YYYY-MM-DD
**Fornecedor:** [Nome, NIF]
**Aprovador:** [Nome]

| # | Descricao | Qtd | Preco Unit. | Total |
|---|-----------|-----|-------------|-------|
| 1 | [Item] | X | €XX.XX | €XX.XX |
| 2 | [Item] | X | €XX.XX | €XX.XX |
| | | | **Subtotal** | €XX.XX |
| | | | **IVA 23%** | €XX.XX |
| | | | **Total** | €XX.XX |

**Condicoes:** Pagamento a 30 dias
**Entrega:** YYYY-MM-DD
**Morada entrega:** [Morada]
```

### 6. Supplier Scorecard (Trimestral)

| KPI | Meta | Real | Score |
|-----|------|------|-------|
| Entrega no prazo | >=95% | _% | _/5 |
| Qualidade (defeitos) | <2% | _% | _/5 |
| Tempo de resposta | <24h | _h | _/5 |
| Cumprimento SLA | >=98% | _% | _/5 |
| Competitividade preco | Mercado +-5% | _% | _/5 |
| **Score global** | | | **_/25** |

Classificacao: A (21-25) / B (16-20) / C (11-15) / D (<11)

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana procurement rfp [titulo]` | Gerar template RFP |
| `adriana procurement rfq [titulo]` | Gerar template RFQ |
| `adriana procurement evaluate` | Gerar matriz avaliacao fornecedores |
| `adriana procurement po [fornecedor]` | Criar ordem de compra |
| `adriana procurement scorecard [fornecedor]` | Gerar scorecard trimestral |
| `adriana procurement contract-check` | Checklist de revisao contratual |
| `adriana procurement compare [propostas]` | Comparar propostas lado-a-lado |

## Template de Output

```markdown
## Relatorio Procurement — [Periodo]

### Metricas
- POs emitidas: X (€XX.XXX)
- Fornecedores activos: X
- Prazo medio pagamento: X dias
- Poupanca vs orcamento: X%
- RFPs abertos: X

### Top Fornecedores (Score)
1. [Fornecedor A] — Score A (23/25)
2. [Fornecedor B] — Score B (18/25)

### Alertas
- [Fornecedor X]: Score D — considerar substituicao
- [PO-YYYY-NNN]: Entrega em atraso X dias
```

## Red Flags

- Compra >€5.000 sem consulta a multiplos fornecedores
- Fornecedor unico sem justificacao documentada
- Contrato sem clausula de rescisao
- PO emitida sem aprovacao do nivel hierarquico adequado
- Fornecedor com Score D em 2 trimestres consecutivos
- Pagamentos antecipados sem garantia bancaria
- Contratos auto-renovaveis sem revisao anual
- Falta de NDA com fornecedores que acedem a dados sensiveis

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-docs** | Contratos e POs seguem gestao documental |
| **adriana-policies** | Politica de compras e aprovacoes |
| **adriana-inventory** | Stock triggers requerem procurement |
| **adriana-fleet** | Compra/leasing de veiculos |
| **adriana-reporting** | Metricas de procurement no dashboard |
| **dario-legal** | Revisao juridica de contratos |
| **dario-negotiation** | Tácticas de negociacao com fornecedores |
| **lucas-finance** | Impacto financeiro e IVA das compras |

## Contexto Portugal

- IVA: 23% (normal), 13% (intermedia), 6% (reduzida)
- Retencao na fonte servicos: 25% (nao residentes), varia para residentes
- Pagamentos a fornecedores: prazo legal max 60 dias (DL 62/2013)
- Facturacao electronica: obrigatoria para entidades publicas
- NIF do fornecedor obrigatorio em todos os documentos


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **adriana-procurement** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in adriana-procurement:**

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
