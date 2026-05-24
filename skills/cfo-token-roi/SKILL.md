---
name: cfo-token-roi
description: >
  ROI do orchestrator DARIO — custo total de tokens AI vs revenue gerado.
  Mede quanto cada EUR gasto em AI gera de retorno. Breakdown por modelo,
  skill, projecto. Trend mensal e forecast 90 dias. Recomendacoes de routing.
  Use quando: quanto custa o DARIO, ROI da AI, estamos a gastar demais em tokens,
  vale a pena usar Opus, custo por task, eficiencia do orchestrator.
tools: Read, Bash, Grep
version: 1.0
---

# CFO Token ROI — Return on AI Investment

## Proposito

O DARIO é o único orchestrator que sabe **quanto custa a si próprio** e **quanto retorno gera**.
Este skill mede:
- Custo total de tokens consumidos (por modelo, skill, projecto, mês)
- Revenue atribuível a tasks completadas
- ROI multiplier: por cada EUR gasto em AI, quantos EUR retornam
- Eficiência: custo médio por task, por quality tier, por skill
- Forecast: projecção de custos e ROI para os próximos 90 dias

## Comandos

| Comando | Descricao |
|---------|-----------|
| `/cfo-token-roi` | Dashboard ROI completo (mês actual) |
| `/cfo-token-roi [YYYY-MM]` | ROI de um mês específico |
| `/cfo-token-roi trend` | Trend últimos 3 meses + forecast |
| `/cfo-token-roi breakdown` | Custo detalhado por modelo/skill |
| `/cfo-token-roi optimize` | Recomendações de model routing |
| `/cfo-token-roi compare [m1] [m2]` | Comparar dois meses |

## Workflow

### Phase 1: COST DATA

1. **Budget YAML** — Ler `~/.claude/orchestrator/budgets/YYYY-MM.yaml`
   ```
   tokens_used, token_limit, percentage, by_model (se disponível)
   ```

2. **Token Meter** — Query real costs
   ```bash
   python ~/.claude/orchestrator/token_meter.py --report --month YYYY-MM
   ```
   Output: tokens por modelo, custo USD, custo EUR

3. **Task-Level Costs** — Extrair do DB
   ```bash
   curl -s http://localhost:8422/tasks | python -c "
   import json, sys
   tasks = json.load(sys.stdin)['tasks']
   done = [t for t in tasks if t['status'] == 'done']
   # Group by skill, sum tokens, calc cost
   "
   ```

4. **Model Distribution** — Percentagem por modelo:
   ```
   opus_pct = opus_tokens / total_tokens × 100
   sonnet_pct = sonnet_tokens / total_tokens × 100
   haiku_pct = haiku_tokens / total_tokens × 100
   ```

### Phase 2: REVENUE ATTRIBUTION

1. **Direct Revenue** — Tasks que resultaram em deliverables facturáveis:
   ```
   revenue_tasks = tasks WHERE project IN (facturado_projects)
   attributed_revenue = sum(project_revenue × task_contribution_pct)
   ```

2. **Task Contribution** — Peso de cada task no revenue:
   - Tasks critical/client_facing: 100% weight
   - Tasks default: 50% weight
   - Tasks internal (audit, autodiag): 0% weight

3. **Revenue por Token** — Eficiência base:
   ```
   revenue_per_1k_tokens = attributed_revenue / (total_tokens / 1000)
   ```

### Phase 3: ROI CALCULATION

```python
# === CORE METRICS ===

# Custo total AI (EUR)
total_ai_cost_eur = (
    opus_input_tokens * 15.0/1e6 +
    opus_output_tokens * 75.0/1e6 +
    sonnet_input_tokens * 3.0/1e6 +
    sonnet_output_tokens * 15.0/1e6 +
    haiku_input_tokens * 0.80/1e6 +
    haiku_output_tokens * 4.0/1e6
) * usd_eur_rate

# Revenue atribuível
attributed_revenue_eur = sum(project_revenues_with_weights)

# ROI Multiplier
roi = attributed_revenue_eur / total_ai_cost_eur  # ex: 45x

# Custo medio por task
avg_cost_per_task = total_ai_cost_eur / completed_tasks

# Custo por quality tier
cost_tier_a = avg_cost(tasks WHERE score >= 85)   # High quality
cost_tier_b = avg_cost(tasks WHERE score 60-84)    # Medium
cost_tier_c = avg_cost(tasks WHERE score < 60)     # Needs revision

# === EFFICIENCY METRICS ===

# Model efficiency score (0-100)
# Penaliza uso de Opus em tasks simples
model_efficiency = 100 - (opus_pct_on_simple_tasks × 0.5)

# Rework waste (tokens gastos em revisions / total)
rework_waste_pct = revision_tokens / total_tokens × 100

# Cache hit rate (se disponível)
cache_savings_pct = cached_tokens / total_tokens × 100

# === SAVINGS POTENTIAL ===

# Se migrar X% de Opus para Sonnet
potential_sonnet_savings = opus_simple_tasks_tokens × (opus_rate - sonnet_rate)

# Se migrar Y% de Sonnet para Haiku
potential_haiku_savings = sonnet_simple_tasks_tokens × (sonnet_rate - haiku_rate)
```

### Phase 4: FORECAST (90 dias)

```python
# Baseado em burn rate actual
daily_burn_rate = total_ai_cost_eur / days_elapsed
monthly_forecast = daily_burn_rate * 30

# Revenue trend
monthly_revenue_trend = revenue_last_3_months / 3
revenue_forecast_90d = monthly_revenue_trend * 3

# ROI forecast
roi_forecast = revenue_forecast_90d / (monthly_forecast * 3)

# Budget runway
tokens_remaining = token_limit - tokens_used
days_at_current_rate = tokens_remaining / (tokens_used / days_elapsed)
```

### Phase 5: OUTPUT

```markdown
## Token ROI Dashboard — [Mes/Ano]

### ROI Summary
| Metrica | Valor |
|---------|-------|
| Custo total AI | EUR X.XX |
| Revenue atribuivel | EUR X,XXX |
| **ROI Multiplier** | **Xx** |
| Custo medio/task | EUR X.XX |
| Tasks completadas | N |

### Cost Breakdown por Modelo
| Modelo | Tokens | Custo EUR | % Total | Efficiency |
|--------|--------|-----------|---------|------------|
| Opus 4 | X,XXX | EUR X.XX | X% | [semaforo] |
| Sonnet 4 | X,XXX | EUR X.XX | X% | [semaforo] |
| Haiku 3.5 | X,XXX | EUR X.XX | X% | [semaforo] |

### Top 5 Skills por Custo
| Skill | Tasks | Tokens | Custo | Avg Score | Cost/Score Ratio |
|-------|-------|--------|-------|-----------|-----------------|
| [skill] | N | X,XXX | EUR X.XX | XX | X.XX |

### Efficiency Analysis
| Metrica | Valor | Status |
|---------|-------|--------|
| Model efficiency score | X/100 | [semaforo] |
| Rework waste | X% | [semaforo] |
| Cache hit rate | X% | [semaforo] |
| Budget usage | X% | [semaforo] |

### Savings Potential
| Accao | Saving Estimado | Impacto Quality |
|-------|-----------------|-----------------|
| Migrate simple tasks Opus→Sonnet | EUR X.XX/mes | Minimo (-2pts avg) |
| Migrate simple tasks Sonnet→Haiku | EUR X.XX/mes | Baixo (-5pts avg) |
| Reduce rework (improve rubrics) | EUR X.XX/mes | Positivo (+Xpts) |
| Improve cache hit rate | EUR X.XX/mes | Zero |

### 90-Day Forecast
| Metrica | Actual | Forecast |
|---------|--------|----------|
| Monthly AI cost | EUR X.XX | EUR X.XX |
| Monthly revenue | EUR X,XXX | EUR X,XXX |
| ROI | Xx | Xx |
| Budget exhaustion | [data] | [data] |

### Recomendacoes
1. [routing] ...
2. [budget] ...
3. [quality] ...
```

## Classification

| ROI Multiplier | Status | Interpretacao |
|----------------|--------|---------------|
| >= 50x | EXCELENTE | AI paga-se 50x — modelo de referencia |
| 20-49x | BOM | Retorno sólido — optimizar nas margens |
| 10-19x | ACEITAVEL | Retorno positivo mas com espaço para melhorar |
| 5-9x | ATENCAO | ROI baixo — rever model routing + pricing |
| < 5x | CRITICO | AI quase nao se paga — accao urgente |

## Red Flags

| # | Red Flag | Accao |
|---|----------|-------|
| 1 | ROI < 5x | Rever se pricing cobre custo AI + margem |
| 2 | Opus > 60% dos tokens | Migrar tasks simples para Sonnet/Haiku |
| 3 | Rework waste > 15% | Investir em rubrics e guardrails |
| 4 | Budget > 80% antes de dia 20 | Throttle para Haiku, limitar parallelism |
| 5 | Cost/score ratio > 0.5 | Skill produz pouca qualidade por EUR gasto |
| 6 | Revenue atribuição = 0 | Tasks sem projecto facturável — trabalho pro bono? |
| 7 | Forecast excede budget | Ajustar routing ou aumentar budget limit |


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **cfo-token-roi** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in cfo-token-roi:**

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
