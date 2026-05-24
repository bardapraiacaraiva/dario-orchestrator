---
name: dario-funnel-polished
description: "Self-polishing funnel designer — autonomous variant of dario-funnel. Internally runs generate → critique → revise → final within one Claude Code session. Use when funnel design must ship client-ready. Triggers: 'funnel polished', 'funil autónomo', 'value ladder ready-to-ship'."
argument-hint: "[business + traffic source + current metrics + goal]"
allowed-tools: Read, Write, Glob, Grep
license: MIT
tested_with_model: claude-opus-4-7
---

# DARIO Skill — Funnel Designer (Self-Polishing)

Padrão A wrapper around `dario-funnel`. Base skill autonomous ceiling ~85 (sprint4 held-out 85.7 ± 2.5). Polished hits ~89. Wrapper closes the gap. **Zero marginal API cost under Claude Max.**

## When to use this vs `dario-funnel`

| Situation | Use |
|---|---|
| Quick funnel sketch for internal alignment | `dario-funnel` |
| Funnel that drives paid acquisition spend | **`dario-funnel-polished`** |
| Client-facing growth deck or playbook | **`dario-funnel-polished`** |

---

## Workflow (5 steps, MUST execute all in order)

### Step 1 — GENERATE v1

**MANDATORY first action — load the base skill's full content:**

```
Read tool → ~/.claude/skills/dario-funnel/SKILL.md
```

The polished wrapper SKILL.md (this file) contains only the polish-loop
mechanics — it does NOT contain the base skill's frameworks, RAG queries,
or domain expertise. Without reading the base skill first, you will
improvise and produce v1 quality below the wrappers' validated baseline.

After reading base, follow its workflow to produce v1.

Execute full `dario-funnel` workflow (Brunson Value Ladder + Hormozi lead gen):
- RAG consult (DotCom Secrets, Expert Secrets, $100M Leads)
- Gather inputs (business, target, traffic, current conv rates, ARPU)
- Build: stages (4-6), conversion_thresholds (% per stage), copy_hooks per stage, automations (triggers + actions)

Mark: `### DRAFT v1 (internal — not delivered)`.

### Step 2 — SELF-CRITIQUE (5-dim, 0-100)

Funnels are gamed by overly optimistic conv rates. Be honest with benchmarks.

```
1. Specificity (0-20) — Stages tied to actual traffic source + target from briefing?
   (Not generic SaaS funnel; vertical-specific friction points)
2. Actionability (0-20) — Can growth/ops team build this funnel today?
   (Concrete tools mentioned, copy hooks executable, automations real)
3. Completeness (0-20) — All 4 funnel components present?
   (Stages / conversion thresholds / copy hooks per stage / automations)
4. Accuracy (0-20) — Conversion thresholds defensible by industry benchmark?
   (E.g., "CTR 8%" for cold ads = unrealistic; flag if claimed)
5. Tone (0-20) — Copy hooks match brand voice and audience register?
```

Document with reasoning per dim + Total + Weakest + Specific issues for v2.

### Step 3 — DECISION GATE

- **TOTAL ≥ 92:** output v1 final
- **TOTAL ≥ 80 AND no dim < 14:** revise
- **TOTAL < 80 OR any dim < 14:** STOP, ask user for traffic data + current funnel state

### Step 4 — REVISE → v2

Targeted fixes:
- Conversion thresholds unrealistic: re-anchor to benchmark (Cold paid CTR 1-2%; warm 4-6%; email open 25-35%)
- Copy hooks weak: rewrite to brand voice with specific hook formulas
- Automations missing: add 3 explicit triggers + actions per stage
- Stages too many/few: collapse or expand based on ARPU+sales cycle

Output v2.

### Step 5 — RE-SCORE + OUTPUT FINAL

Re-run critique on v2. Output best with metadata.

### Step 6 — RECORD TELEMETRY (mandatory, append-only)

After delivering the final output, invoke the telemetry recorder via Bash to log this run into the production rolling metrics. Without this, the system has no evidence Padrão A is paying off for this skill.

```bash
cd ~/.claude/orchestrator && \
.venv/Scripts/python.exe -m scripts.record_polished_run \
    --skill dario-funnel-polished \
    --v1-score $V1_SCORE \
    --v2-score $V2_SCORE \
    --final $FINAL \
    --client $CLIENT_SLUG \
    --briefing-summary "$ONE_LINE_DESCRIPTION" \
    --gate-decision $GATE_DECISION \
    --model-used "claude-opus-4-7" \
    --status-mix "$VERIFIED/$ASSUMED/$PROJECTION"
```

Where:
- `$GATE_DECISION` ∈ {`revised`, `ship_v1`, `aborted`}
- `--v2-score` omitted when `gate_decision=ship_v1` or `aborted`
- `--final` ∈ {`v1`, `v2`, `aborted`}

Appends one entry to `~/.claude/orchestrator/quality/polished_production_runs.yaml`. Aggregator (`scripts/aggregate_polished_metrics.py`) computes per-skill 30-day metrics on demand or via cron.

**DO NOT skip this step.** This is what closes the loop on the "track production_avg_delivery_ready 90 days" goal.


---

## A/B Test Protocol

**Baseline:** dario-funnel sprint4 held-out 85.7 ± 2.5 (n=9), pre-v2 baseline 86.3.
**Threshold:** ≥+4pts lift on 3 real briefings.
**Test briefings:** Cuidaí design partner acquisition / SAQUEI paid → subscription / Tributário.AI outbound enterprise.

---

## Red flags

- ❌ Inventing conversion rates ("CTR 4.8%") without benchmark backing — Accuracy fail
- ❌ Generic stages ("Awareness → Interest → Decision") — Specificity fail
- ❌ Skip automations — Completeness fail (4/4 components required)
- ❌ Override industry-defensible benchmarks to make funnel look better — kills trust

---

<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every claim must carry an EXPLICIT label.

- 🔵 **verified** — traffic source, current MRR/conv rates from briefing
- 🟡 **assumed** — benchmark conversion (e.g., "B2C CTR 1.8%") needing source citation
- 🟢 **projection** — target conversion rates, LTV, scale numbers

**Why:** funnels mix verified current state with projected future state. Reader/operator needs to know which numbers are committed vs aspirational to allocate budget.

❌ NOT delivery-ready:
```
Stage 1 ad CTR 2.4% → opt-in 31% → tripwire 12%. CAC R$ 25.
```

✅ Delivery-ready:
```
- Stage 1 Meta Ads CTR 2.4% 🟡 assumed (benchmark B2C BR fintech 2024; precisa A/B real)
- Opt-in 31% 🟡 assumed (boa landing benchmark 25-35%, depende creative)
- Tripwire R$ 29 conversion 12% 🟢 projection (depende pricing perception A/B test)
- CAC R$ 25 🟢 projection (derivado de CTR×CPM×conv; realistic se hooks segurarem)
- Current conv rate baseline (briefing): R$ 29 single 0% (PWA novo, sem dados) 🔵 verified

Status mix: 1 🔵 · 2 🟡 · 2 🟢
```
<!-- gate7:end -->