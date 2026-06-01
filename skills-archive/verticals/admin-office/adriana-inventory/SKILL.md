---
name: adriana-inventory
description: "ADRIANA Office Supplies — stock levels, reorder points, supplier comparison, budget"
version: "1.0"
---

# ADRIANA-INVENTORY: Gestao de Material de Escritorio

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** material escritorio, stock, inventario, encomenda, fornecedor material, papel, toner, canetas, reposicao, consumiveis, orcamento material, compras escritorio, requisicao
**Trigger words (EN):** office supplies, stock, inventory, reorder, stationery, toner, paper, consumables, supply budget, requisition, stock levels, replenishment

Activar quando o utilizador precisa de:
- Controlar stock de material de escritorio
- Definir pontos de reposicao
- Comparar fornecedores de material
- Gerir orcamento de consumiveis
- Processar requisicoes de material
- Fazer inventario fisico

## Workflow Passo-a-Passo

### 1. Catalogo de Material

**Categorias padrao:**

| Cat | Categoria | Exemplos |
|-----|-----------|----------|
| PAP | Papel e impressao | Resmas A4, envelopes, etiquetas, toner, tinteiros |
| ESC | Escrita | Canetas, lapis, marcadores, corretores |
| ARQ | Arquivo | Pastas, separadores, capas, caixas arquivo |
| TEC | Tecnologia | Cabos, pilhas, pen drives, adaptadores |
| HIG | Higiene | Sabao, papel WC, toalhas papel, desinfectante |
| COP | Copa | Cafe, cha, acucar, leite, bolachas, copos |
| LIM | Limpeza | Detergente, panos, sacos lixo, luvas |
| MOB | Mobiliario menor | Organizadores, suportes, tapetes rato |

### 2. Ficha de Produto

```markdown
# Ficha de Produto
**SKU:** [CAT]-NNN
**Descricao:** [Nome do produto]
**Categoria:** [Categoria]
**Unidade:** [Un / Cx / Resma / Pack]

## Stock
| Campo | Valor |
|-------|-------|
| Stock actual | XX unidades |
| Stock minimo (reorder point) | XX unidades |
| Stock maximo | XX unidades |
| Quantidade encomenda (EOQ) | XX unidades |
| Localizacao | [Armario X, Prateleira Y] |

## Fornecedores
| Fornecedor | Ref | Preco unit. | Prazo entrega | Min. encomenda |
|------------|-----|-------------|---------------|----------------|
| [Forn. A] | [Ref] | €X.XX | X dias | X un |
| [Forn. B] | [Ref] | €X.XX | X dias | X un |

## Consumo
- Media mensal: XX unidades
- Custo mensal: €XX.XX
- Ultimo inventario: YYYY-MM-DD
```

### 3. Pontos de Reposicao

**Formula de calculo:**
```
Reorder Point = (Consumo diario medio x Lead time dias) + Stock seguranca

Stock seguranca = Consumo diario medio x Dias de buffer (tipicamente 5-7)

EOQ (Qtd Economica Encomenda) = sqrt((2 x Consumo anual x Custo encomenda) / Custo armazenamento por unidade)
```

**Exemplo pratico — Resmas A4:**
- Consumo mensal: 20 resmas → 1 resma/dia util
- Lead time fornecedor: 3 dias
- Stock seguranca: 5 dias = 5 resmas
- **Reorder point: (1 x 3) + 5 = 8 resmas**
- Quando stock chega a 8 resmas → encomendar

**Tabela resumo (top items):**
| Item | Consumo/mes | Reorder Point | Qtd encomenda | Fornecedor |
|------|------------|---------------|---------------|------------|
| Resma A4 80g | 20 | 8 | 50 | [Nome] |
| Toner HP XX | 2 | 1 | 3 | [Nome] |
| Caneta BIC azul | 10 | 5 | 50 | [Nome] |
| Cafe capsulas | 200 | 80 | 200 | [Nome] |
| Papel WC | 30 | 12 | 48 | [Nome] |
| Sabao liquido | 4 | 2 | 6 | [Nome] |
| Sacos lixo | 8 | 4 | 20 | [Nome] |

### 4. Requisicao de Material

```markdown
# Requisicao de Material
**Ref:** REQ-YYYY-NNN
**Data:** YYYY-MM-DD
**Requisitante:** [Nome]
**Departamento:** [Dept]

| # | Descricao | SKU | Qtd | Urgencia | Justificacao |
|---|-----------|-----|-----|----------|-------------|
| 1 | [Item] | [SKU] | XX | Normal/Urgente | [Motivo] |
| 2 | [Item] | [SKU] | XX | Normal/Urgente | [Motivo] |

## Aprovacao
- [ ] Chefia: [Nome] — Data: ___
- [ ] Office manager: [Nome] — Data: ___
```

**Niveis de aprovacao:**
| Valor | Aprovador |
|-------|-----------|
| <€50 | Office manager |
| €50-€200 | Chefia departamento |
| >€200 | Direccao |

### 5. Comparacao de Fornecedores

| Criterio | Peso | Staples | Lyreco | Local |
|----------|------|---------|--------|-------|
| Precos | 35% | _/5 | _/5 | _/5 |
| Prazo entrega | 20% | _/5 | _/5 | _/5 |
| Minimo encomenda | 15% | _/5 | _/5 | _/5 |
| Portes gratis a partir de | 10% | €XX | €XX | €XX |
| Gama produtos | 10% | _/5 | _/5 | _/5 |
| Sustentabilidade | 10% | _/5 | _/5 | _/5 |
| **Score ponderado** | 100% | **_** | **_** | **_** |

### 6. Orcamento Anual de Material

```markdown
# Orcamento Material Escritorio — [Ano]

| Categoria | Orcamento Anual | Mensal | % Total |
|-----------|----------------|--------|---------|
| Papel e impressao | €X.XXX | €XXX | XX% |
| Escrita e arquivo | €XXX | €XX | XX% |
| Tecnologia | €XXX | €XX | XX% |
| Higiene | €XXX | €XX | XX% |
| Copa | €X.XXX | €XXX | XX% |
| Limpeza | €XXX | €XX | XX% |
| Outros | €XXX | €XX | XX% |
| **TOTAL** | **€X.XXX** | **€XXX** | **100%** |

Referencia: €XX-€XX per capita/mes (benchmark PME PT)
```

### 7. Inventario Fisico

**Frequencia:** Trimestral (ou mensal para items de alto valor)

**Processo:**
1. Imprimir lista de stock actual (sistema)
2. Contagem fisica por 2 pessoas
3. Registar diferencas
4. Investigar desvios >10%
5. Ajustar sistema
6. Assinatura do responsavel

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana inventory list` | Listar stock actual |
| `adriana inventory low` | Items abaixo do reorder point |
| `adriana inventory order [sku]` | Criar encomenda |
| `adriana inventory request [dept]` | Requisicao de material |
| `adriana inventory count` | Iniciar inventario fisico |
| `adriana inventory compare [item]` | Comparar fornecedores para item |
| `adriana inventory budget [ano]` | Orcamento anual |
| `adriana inventory report [periodo]` | Relatorio consumo |

## Template de Output

```markdown
## Inventario — [Data]

### Alertas de Stock
| SKU | Item | Stock | Reorder | Accao |
|-----|------|-------|---------|-------|
| PAP-001 | Resma A4 | 5 | 8 | ENCOMENDAR |
| TEC-003 | Toner HP | 0 | 1 | URGENTE |

### Consumo Mensal
- Total gasto: €XXX (orcamento: €XXX — desvio: X%)
- Top 5 items por custo: [lista]
- Custo per capita: €XX

### Encomendas Pendentes
| Ref | Fornecedor | Valor | Data prevista |
|-----|-----------|-------|---------------|
| [Ref] | [Nome] | €XX | DD/MM |
```

## Red Flags

- Stock a zero de item essencial (papel, toner)
- Consumo de item >50% acima da media sem justificacao
- Orcamento excedido >10% sem aprovacao
- Inventario fisico nao realizado >6 meses
- Fornecedor unico sem alternativa identificada
- Items armazenados em condicoes inadequadas
- Requisicoes nao aprovadas antes de compra
- Material pessoal comprado como material empresa
- Desvios de inventario >5% nao investigados
- Produtos expirados em stock (toner, alimentos copa)

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-procurement** | Encomendas e contratos com fornecedores |
| **adriana-facilities** | Material de limpeza e manutencao |
| **adriana-onboarding** | Kit material para novos colaboradores |
| **adriana-reporting** | Custos material no dashboard mensal |
| **adriana-policies** | Politica de requisicoes |
| **adriana-sop** | SOP de inventario e encomendas |
| **lucas-finance** | Contabilizacao e IVA do material |
| **adriana-fleet** | Consumiveis de veiculos |

## Contexto Portugal

- IVA material escritorio: 23% (taxa normal)
- IVA cafe/alimentos copa: 23% (quando empresa, nao refeicao)
- Custo fiscalmente aceite: material necessario a actividade
- Fornecedores PT grandes: Staples, Lyreco, Office Depot, OfficeMax
- Sustentabilidade: privilegiar papel reciclado/FSC, toners reciclados
- Benchmark PME: €20-€40 per capita/mes em consumiveis


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **adriana-inventory** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in adriana-inventory:**

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
