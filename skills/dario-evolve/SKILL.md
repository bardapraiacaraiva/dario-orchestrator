---
name: dario-evolve
description: "DARIO Evolution Engine — the self-evolving core. Runs learning journal capture, mutation engine, pattern crystallization, generative proposals, and fitness selection. Triggers on: 'evolve', 'evolucao', 'auto-improve', 'o que aprendeste', 'fitness', 'generation', 'mutacoes'. Also triggered automatically by heartbeat in EXPANSION state."
license: MIT
---

# DARIO Evolution Engine — Self-Evolving Orchestrator

The mechanism that makes DARIO a living system. No other Claude Code orchestrator has this.

## What Makes This Different

Traditional orchestrators are **defined once, run forever**. DARIO v2.0+ is **alive** — it modifies its own configuration based on what it learns, gets better every session, and evolves without human instruction.

## When to Activate

- **Micro** (automatic): After every task completion — update weights, log observations
- **Session** (automatic): End of session or every 10 tasks — journal + mutations
- **Weekly** (EXPANSION state): Full evolution cycle — fitness, checkpoint, generative
- **Manual**: User says "evolve", "o que aprendeste", "fitness check"

## Workflow

### MICRO EVOLUTION (every task completion)

```
1. Read completed task: skill used, quality score, was it a composite mode?
2. If multi-skill: update synaptic_weights.yaml
   - Score >= 80: pair.weight += 0.05
   - Score < 50: pair.weight -= 0.03
3. Log observation to current session buffer
4. If user corrected dispatch: log dispatch_correction pattern
5. Total cost: ~100 tokens
```

### SESSION EVOLUTION (every 10 tasks or session end)

```
1. CAPTURE — Generate learning journal entry:
   - Read all tasks completed this session
   - Calculate avg_quality, skills_used, pairs_activated
   - Count fallbacks triggered, user corrections
   - Compute evolutionary_delta
   - Save to ~/.claude/orchestrator/evolution/journal/

2. CRYSTALLIZE — Check if any pattern hit threshold (5 repeats):
   - Scan journal entries (current + last 5)
   - For each pattern type, count occurrences
   - If threshold reached → crystallize into rule
   - Apply rule to appropriate YAML file
   - Log mutation

3. MUTATE — Apply pending mutations (max 3/session):
   - Check mutation queue from crystallization
   - Validate each against safety_bounds
   - Apply mutation to target file
   - Log with before/after for rollback capability
   - Increment total_mutations_applied

4. REPORT (silent unless asked):
   - "Learned X patterns, applied Y mutations, delta: +Z%"
   - Only output if user asks or if significant change (delta > 5%)

Total cost: ~500 tokens
```

### WEEKLY EVOLUTION (EXPANSION state)

```
1. CHECKPOINT — Snapshot current state:
   - Copy all mutable YAMLs to checkpoints/
   - Record fitness metric
   - Tag as ckpt_{date}

2. FITNESS REVIEW — Compare vs 4-week baseline:
   - Calculate current fitness: avg_quality * (1 - budget_ratio) * velocity
   - Compare vs checkpoint from 4 weeks ago
   - If dropped >15%: trigger FULL ROLLBACK

3. SURVIVAL CHECK — Evaluate recent mutations:
   - For each mutation applied in last week:
     - Did fitness improve after 10 tasks? → KEEP
     - Did fitness drop >5%? → REVERT
     - Neutral? → KEEP (give more time)

4. PRUNE — Clean dead rules:
   - Rules that haven't fired in 30 days → archive
   - Composite modes never used in 30 days → flag for removal
   - Synaptic weights at minimum (0.1) for 30 days → remove pair

5. GENERATIVE — Propose new components:
   - Scan for recurring patterns not yet crystallized
   - Propose new composite modes, dispatch rules, affinity pairs
   - At P-A4: auto-apply. Below P-A4: propose to user.

6. INCREMENT GENERATION:
   - generation += 1
   - Write CHANGELOG entry
   - Log DARIO_EVOLUTION_GEN_{N}_{fitness}

Total cost: ~2000 tokens
```

## Safety Bounds (INVIOLABLE)

These can NEVER be mutated by the evolution engine:

| Protected | Reason |
|-----------|--------|
| manifesto.yaml | Governance/identity is immutable |
| blocklist in operational_states | Ethics are immutable |
| ethical_pre_gate | Hard safety constraint |
| max_parallel > 3 | Cost explosion prevention |
| quality threshold < 50 | Minimum quality floor |
| Max 3 mutations/session | Anti-runaway protection |
| Weekly checkpoint mandatory | Rollback safety net |

## Mutation Protocol

When the engine decides to mutate a config:

```yaml
# 1. Validate against safety bounds
if mutation.target in PROTECTED_FILES:
  ABORT — "Cannot mutate protected file"

if mutations_this_session >= 3:
  QUEUE for next session

# 2. Log before state
before = read(target_file, target_field)

# 3. Apply mutation
write(target_file, target_field, new_value)

# 4. Log mutation
append_to_log({
  timestamp: now(),
  file: target_file,
  field: target_field,
  old_value: before,
  new_value: new_value,
  reason: pattern_that_triggered,
  confidence: pattern_count / threshold,
  revertable: true
})

# 5. Set review timer (10 tasks)
mutation.review_after = current_task_count + 10
```

## Rollback Protocol

If a mutation causes harm:

```
1. Detect: fitness dropped >5% within 10 tasks of mutation
2. Identify: which mutation(s) were applied in that window
3. Revert: restore old_value from mutation log
4. Log: DARIO_EVOLUTION_REVERT_{mutation_id}_{reason}
5. Learn: mark this mutation type as "failed" — don't retry same pattern
```

## Fitness Metric

```
fitness = avg_quality_last_10 * (1 - budget_usage_pct/100) * task_velocity

Where:
  avg_quality_last_10 = mean quality score of last 10 tasks (0-100, /100 for 0-1)
  budget_usage_pct = current month budget percentage used
  task_velocity = tasks_completed / tasks_planned (capped at 1.0)

Range: 0.0 to 1.0
Target: >= 0.70
Excellent: >= 0.85
```

## What The System Learns Over Time

| Week 1 | Baseline established, first observations |
| Week 2 | First patterns crystallize, first mutations |
| Week 4 | First generation complete, fitness trending |
| Month 2 | Composite modes auto-created, dispatch rules learned |
| Month 3 | System significantly different from original — adapted to user's workflow |
| Month 6 | Fully personalized — routing, weights, modes all shaped by real usage |

## Integration with Other Systems

- **lucas-heartbeat**: Triggers micro_evolution after each task
- **lucas-quality**: Provides scores that feed the fitness metric
- **lucas-autopilot**: In EXPANSION state, triggers weekly_evolution
- **dario-status**: Shows evolution metrics in health dashboard
- **Stop hook**: Triggers session_evolution at session end

## Output (when asked)

```
## DARIO Evolution Status — Generation {N}

| Metric | Value |
|--------|-------|
| Generation | {N} |
| Total Mutations | {applied} ({reverted} reverted) |
| Patterns Crystallized | {count} |
| Composite Modes Created | {count} |
| Dispatch Rules Learned | {count} |
| Affinity Pairs Discovered | {count} |
| Current Fitness | {score} |
| Fitness Trend | {sparkline last 10} |
| Autonomy Level | P-A{level} |
| Next Evolution | {session_end / weekly / etc} |

### Recent Mutations
- {date}: {description} — {kept/reverted}

### Active Learned Rules
- {rule_1}
- {rule_2}
```

## Red Flags

- Never mutate protected files (manifesto, blocklist, ethical gate)
- Never apply more than 3 mutations per session
- Never skip the weekly checkpoint
- Never auto-create at autonomy below P-A3
- Never revert a mutation without logging the reason
- If fitness drops >15% over 4 weeks, FULL ROLLBACK — no exceptions
- Evolution is SILENT by default — only reports when asked or when significant

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Fitness Metric Populated com Dados Reais

- [ ] `avg_quality_last_10` tem valor numérico concreto (não "N/A" ou placeholder)
- [ ] `budget_usage_pct` referencia mês real (ex: "Junho 2025: 34%")
- [ ] `task_velocity` calculado com numerador/denominador visíveis (ex: "12/15 = 0.80")
- [ ] Score final fitness declarado explicitamente (ex: "fitness = 0.612")

❌ NOT delivery-ready: `fitness = avg_quality * (1 - budget_ratio) * velocity → pendente`
✅ Delivery-ready: `fitness = 0.78 * (1 - 0.34) * 0.80 = 0.412 — abaixo de 0.70, trigger survival check`

---

### Gate 2 — Learning Journal Entry Completo

- [ ] `skills_used` lista os skills por nome real (ex: `dario-write`, `dario-strategy`)
- [ ] `pairs_activated` inclui contagem e pares específicos
- [ ] `evolutionary_delta` expresso em % com sinal (ex: `+3.2%` ou `-1.1%`)
- [ ] `fallbacks_triggered` tem número inteiro (0 é válido, "—" não é)

❌ NOT delivery-ready: "evolutionary_delta: positivo — sistema melhorou esta sessão"
✅ Delivery-ready: "evolutionary_delta: +4.7% | fallbacks: 2 | pairs_activated: dario-write↔dario-strategy (x3)"

---

### Gate 3 — Mutations Documentadas com Before/After

- [ ] Cada mutation tem `target_file` + `target_field` explícitos
- [ ] `old_value` e `new_value` presentes (não deduzidos)
- [ ] `confidence` calculado como `pattern_count / threshold` (ex: `6/5 = 1.2`)
- [ ] `review_after` task count definido (ex: `task #47`)
- [ ] Mutations count ≤ 3 para a sessão, ou overflow justificado para queue

❌ NOT delivery-ready: "Mutação aplicada: ajuste de peso no par escrita+análise"
✅ Delivery-ready: "synaptic_weights.yaml → pair: dario-write+dario-data | 0.65 → 0.70 | confidence: 6/5 | review_after: task #31"

---

### Gate 4 — Safety Bounds Verificados Explicitamente

- [ ] Output confirma que nenhum arquivo protegido foi tocado (lista os 7 invioláveis)
- [ ] `max_parallel` nunca aparece com valor > 3 em nenhuma proposta
- [ ] `quality_threshold` nunca aparece com valor < 50
- [ ] Se mutation foi bloqueada: razão registada (não silenciada)

❌ NOT delivery-ready: "Safety bounds: OK ✓" — sem evidência
✅ Delivery-ready: "Protected check PASS — manifesto.yaml: untouched | ethical_pre_gate: untouched | mutations this session: 2/3"

---

### Gate 5 — Weekly/Generation Report com Métricas Comparativas

- [ ] Geração atual numerada (ex: `Generation 7`)
- [ ] Fitness comparada com checkpoint de 4 semanas atrás (dois valores visíveis)
- [ ] Survival check lista cada mutation com veredicto (KEEP / REVERT / PENDING)
- [ ] Prune log indica regras arquivadas ou "0 rules pruned this cycle"
- [ ] CHANGELOG entry gerada com data e delta

❌ NOT delivery-ready: "Fitness melhorou face à semana passada — geração incrementada"
✅ Delivery-ready: "Gen 7 | fitness: 0.81 vs ckpt_2025-05-12: 0.74 (+9.5%) | KEEP: 3 mutations | REVERT: 0 | Pruned: 1 rule (dario-legal, 32 days silent)"

---

### Gate 6 — Output usa NOME DO CLIENT + dados reais, sem angle-brackets

- [ ] Nenhum `<client_name>`, `<skill_pair>`, `<date>` ou `<value>` no output final
- [ ] Projeto/contexto real identificado (ex: Cuidai, SAQUEI, Tributario.AI)
- [ ] Timestamps em formato concreto ISO ou PT (ex: `2025-06-18` ou `18 Jun 2025`)
- [ ] IDs de mutation em formato real (ex: `DARIO_EVOLUTION_MUT_042_weight_boost`)

❌ NOT delivery-ready: "Log: DARIO_EVOLUTION_GEN_{N}_{fitness}"
✅ Delivery-ready: "Log: DARIO_EVOLUTION_GEN_7_0.81 — Atrium | 2025-06-18"

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# DARIO Evolution Report — Atrium | Sessão #23 | 2025-06-18

## SESSION EVOLUTION — Summary

**Tasks completed:** 14
**Skills used:** dario-write (x6), dario-strategy (x4), dario-data (x3), dario-legal (x1)
**Pairs activated:** dario-write↔dario-strategy (x4), dario-data↔dario-write (x3)
**Avg quality last 10:** 83.4/100
**Fallbacks triggered:** 1 (dario-legal → dario-write fallback, task #19)
**User corrections to dispatch:** 0
**Evolutionary delta:** +5.1%

---

## PATTERNS CRYSTALLIZED

Pattern: dario-write↔dario-strategy co-activation
Occurrences this session: 4 | Cumulative: 6 | Threshold: 5
Status: **CRYSTALLIZED → synaptic_weights.yaml update queued**

---

## MUTATIONS APPLIED (2/3 this session)

### Mutation MUT_041
- File: `synaptic_weights.yaml`
- Field: `pairs.dario-write+dario-strategy.weight`
- Old value: `0.65`
- New value: `0.70`
- Reason: pattern_write_strategy_coactivation (6/5 = confidence 1.20)
- Review after: task #33
- Revertable: true

### Mutation MUT_042
- File: `dispatch_rules.yaml`
- Field: `rules.legal_fallback.priority`
- Old value: `0.40`
- New value: `0.35`
- Reason: dispatch_correction_legal_x3 (3/5 = confidence 0.60 — partial)
- Review after: task #33
- Revertable: true

**Queued (overflow):** 0

---

## SAFETY BOUNDS CHECK — PASS

| Protected File         | Status     |
|------------------------|------------|
| manifesto.yaml         | ✅ Untouched |
| blocklist              | ✅ Untouched |
| ethical_pre_gate       | ✅ Untouched |
| max_parallel           | ✅ Current: 2 (limit: 3) |
| quality_threshold      | ✅ Current: 65 (floor: 50) |
| mutations this session | ✅ 2/3      |
| weekly checkpoint      | ✅ Scheduled: 2025-06-23 |

---

## FITNESS METRIC

```
avg_quality_last_10 = 83.4 / 100 = 0.834
budget_usage_pct    = 41% (Junho 2025, Atrium workspace)
task_velocity       = 14 / 15 = 0.933

fitness = 0.834 × (1 - 0.41) × 0.933
fitness = 0.834 × 0.59 × 0.933
fitness = 0.459

⚠️ Below 0.70 target — driver: budget_usage_pct elevated
Recommendation: monitor budget burn rate, not quality-driven
```

---

## GENERATION STATUS

**Current generation:** Gen 6 (weekly cycle pending — next: 2025-06-23)
**Last checkpoint:** ckpt_2025-05-26 | fitness: 0.71
**Trend:** -0.251 vs checkpoint (budget spike, not quality regression)
**Action:** NO rollback triggered (quality arm 0.834 healthy)

**Log entry:** `DARIO_EVOLUTION_GEN_6_0.459 — Atrium | 2025-06-18 | budget-flag`
```

---

## Output anti-patterns

- Fitness score declarado como "positivo" ou "bom" sem valor numérico calculado
- Mutations listadas com `<field>` ou `<old_value>` ainda por preencher
- Safety bounds check como tick único sem verificação por arquivo protegido
- Learning journal com `evolutionary_delta: TBD` entregue ao cliente
- Generation number omitido ("geração incrementada" sem número concreto)
- Survival check com veredicto "a avaliar" — deve ser KEEP, REVERT, ou PENDING com razão
- Rollback report sem `mutation_id` específico — impossível de auditar
- Fitness abaixo de 0.70 entregue sem diagnóstico do driver (qualidade vs. budget vs. velocity)
- Timestamps como "hoje" ou "recente" em vez de data ISO
- Prune log silenciado — "0 rules pruned" é output válido, omissão não é
