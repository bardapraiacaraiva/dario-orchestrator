---
name: cfo-agency-pnl
description: >
  P&L real por cliente e projecto incluindo custo de tokens AI, horas internas, rework,
  freelancers. Calcula margem bruta e liquida com custo real de delivery.
  Use quando: margem cliente, rentabilidade projecto, custo delivery, P&L mensal agencia,
  quanto custa servir este cliente, estamos a perder dinheiro.
tools: Read, Bash, Grep, Glob
version: 1.0
---

# CFO Agency P&L — Margem Real por Cliente/Projecto

## Proposito

Calcular a **margem real** de cada cliente e projecto, incluindo custos que normalmente ficam invisíveis:
- Custo de tokens AI (Opus/Sonnet/Haiku) consumidos nas tasks do projecto
- Custo de rework (revision loops × custo medio por revision)
- Horas internas estimadas por tipo de task
- Subcontratação e freelancers

**Diferenciador:** Nenhum outro orchestrator sabe quanto custa a si próprio por cliente. O DARIO sabe.

## Comandos

| Comando | Descricao |
|---------|-----------|
| `/cfo-agency-pnl [projecto]` | P&L detalhado de um projecto |
| `/cfo-agency-pnl all` | P&L consolidado todos os projectos activos |
| `/cfo-agency-pnl compare [p1] [p2]` | Comparar rentabilidade entre projectos |
| `/cfo-agency-pnl monthly [YYYY-MM]` | P&L mensal da agencia |
| `/cfo-agency-pnl alerts` | Projectos com margem negativa ou < 20% |

## Workflow

### Phase 1: DATA COLLECTION

1. **Revenue** — Ler `~/.claude/orchestrator/finance/receivables.yaml`
   - Filtrar por projecto/cliente
   - Somar facturação bruta e líquida (- IVA)

2. **Token Costs** — Query ao orchestrator DB
   ```bash
   python ~/.claude/orchestrator/token_meter.py --report --project [PROJECT]
   ```
   - Tokens por modelo (Opus: $15/$75 per M, Sonnet: $3/$15, Haiku: $0.80/$4)
   - Converter tokens → EUR ao câmbio actual USD/EUR

3. **Task History** — Query ao orchestrator DB
   ```bash
   curl -s http://localhost:8422/tasks | python -c "
   import json,sys
   tasks = json.load(sys.stdin)['tasks']
   project_tasks = [t for t in tasks if t['project'] == 'PROJECT']
   # Count: total, revisions, avg_score
   "
   ```

4. **Rework Cost** — Calcular custo de revision loops:
   ```
   rework_cost = revision_count × avg_tokens_per_revision × cost_per_token
   ```

5. **Hours Estimate** — Baseado no tipo de skill:
   | Categoria | Horas estimadas por task |
   |-----------|------------------------|
   | Brand/Strategy | 2.0h |
   | SEO Audit | 1.5h |
   | Content | 1.0h |
   | Technical (WP/Woo) | 2.5h |
   | Design (DIVA) | 2.0h |
   | Finance/Accounting | 1.0h |
   | Simple dispatch | 0.25h |

6. **Freelancers** — Ler `~/.claude/orchestrator/finance/freelancers.yaml`
   - Filtrar pagamentos por projecto

### Phase 2: CALCULATION

```
## Revenue
revenue_bruto = sum(facturas_brutas)
revenue_liquido = revenue_bruto - iva_total

## Custos Directos
token_cost_eur = (opus_tokens × opus_rate + sonnet_tokens × sonnet_rate + haiku_tokens × haiku_rate) × usd_eur_rate
hours_cost = estimated_hours × internal_hourly_rate  # default: 45 EUR/h
rework_cost = revision_tasks × avg_revision_cost
freelancer_cost = sum(freelancer_payments_for_project)
total_direct_costs = token_cost_eur + hours_cost + rework_cost + freelancer_cost

## Margem Bruta
gross_margin = revenue_liquido - total_direct_costs
gross_margin_pct = gross_margin / revenue_liquido × 100

## Overhead (alocado proporcionalmente)
overhead_pct = 0.15  # 15% default — infra, ferramentas, admin
overhead_cost = revenue_liquido × overhead_pct

## Margem Liquida
net_margin = gross_margin - overhead_cost
net_margin_pct = net_margin / revenue_liquido × 100
```

### Phase 3: CLASSIFICATION

| Margem Liquida | Status | Accao |
|----------------|--------|-------|
| >= 40% | EXCELENTE (verde) | Manter — modelo a replicar |
| 20-39% | SAUDAVEL (verde) | Optimizar token routing (Haiku onde possivel) |
| 10-19% | ATENCAO (amarelo) | Rever pricing ou reduzir rework |
| 0-9% | CRITICO (laranja) | Rever scope imediatamente |
| < 0% | NEGATIVO (vermelho) | ALERTA: subsidiar trabalho. Accao urgente. |

### Phase 4: OUTPUT

```markdown
## P&L — [Cliente/Projecto] — [Periodo]

### Revenue
| Item | Valor |
|------|-------|
| Facturacao bruta | EUR X,XXX |
| (-) IVA 23% | EUR X,XXX |
| **Revenue liquido** | **EUR X,XXX** |

### Custos Directos
| Item | Detalhe | Valor |
|------|---------|-------|
| Token cost AI | Opus: Xt, Sonnet: Yt, Haiku: Zt | EUR X.XX |
| Horas internas | Xh × EUR 45/h | EUR X,XXX |
| Rework (N revisions) | N × EUR X | EUR X.XX |
| Freelancers | [nome: EUR X] | EUR X,XXX |
| **Total custos directos** | | **EUR X,XXX** |

### Margem
| Metrica | Valor | Status |
|---------|-------|--------|
| Margem bruta | EUR X,XXX (X%) | [semaforo] |
| (-) Overhead 15% | EUR X,XXX | |
| **Margem liquida** | **EUR X,XXX (X%)** | **[semaforo]** |

### Token Breakdown
| Modelo | Tokens | Custo | % Total |
|--------|--------|-------|---------|
| Opus | X,XXX | EUR X.XX | X% |
| Sonnet | X,XXX | EUR X.XX | X% |
| Haiku | X,XXX | EUR X.XX | X% |

### Recomendacoes
1. [Se margem < 20%] Rever pricing — rate actual EUR X/h vs custo real EUR Y/h
2. [Se rework > 15%] Reduzir revision loops — investir em rubrics mais claras
3. [Se Opus > 50% tokens] Migrar tasks simples para Haiku — saving estimado EUR X
```

## Configuração

```yaml
# Defaults configuráveis em finance/pnl_config.yaml
internal_hourly_rate: 45        # EUR/hora trabalho interno
overhead_pct: 0.15              # 15% overhead alocado
usd_eur_rate: 0.92              # Taxa câmbio USD→EUR
margin_alert_threshold: 0.20    # Alerta se margem < 20%
margin_critical_threshold: 0.0  # Critico se margem negativa

# Token costs per million (USD)
token_costs:
  opus:    { input: 15.0, output: 75.0 }
  sonnet:  { input: 3.0,  output: 15.0 }
  haiku:   { input: 0.80, output: 4.0  }
```

## Integration Points

| Sistema | Dados |
|---------|-------|
| Orchestrator DB | Tasks por projecto, tokens, scores, revisions |
| token_meter.py | Custo real por modelo/skill/projecto |
| quality_scorer.py | Revision count, scores por task |
| receivables.yaml | Revenue por cliente |
| freelancers.yaml | Custos subcontratação |
| dispatch_engine.py | Skill→projecto mapping |

## Red Flags

| # | Red Flag | Consequencia |
|---|----------|-------------|
| 1 | Margem negativa nao detectada | Subsidiar trabalho sem saber |
| 2 | Token cost > 30% do revenue | Modelo de AI insustentavel |
| 3 | Rework > 20% das tasks | Quality problem — rubrics, not pricing |
| 4 | Opus usado em tasks simples | Desperdicio 94.7% vs Haiku |
| 5 | Revenue sem factura associada | Trabalho gratuito nao intencional |
| 6 | Freelancer cost nao alocado ao projecto | Margem inflacionada artificialmente |
| 7 | Internal rate desactualizado | Margem calculada com dados velhos |

## Watches (Reactive Subscriptions)

```yaml
watches:
  - skill: lucas-quality    # Quando task scored → recalcular se revision
    condition: "action == 'revision'"
  - skill: lucas-finance    # Quando factura emitida → actualizar revenue
    condition: "always"
```


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **cfo-agency-pnl** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in cfo-agency-pnl:**

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
