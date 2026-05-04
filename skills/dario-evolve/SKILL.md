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
