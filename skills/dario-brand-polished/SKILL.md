---
name: dario-brand-polished
description: "Self-polishing brand positioning workshop — single-skill autonomous variant of dario-brand. Internally runs generate → critique → revise → final within one Claude Code session. Use when brand work must ship without human polish. Triggers: 'brand polished', 'posicionamento ready-to-ship', 'brand autonomous'."
argument-hint: "[client/business + target + competitive context]"
allowed-tools: Read, Write, Glob, Grep
license: MIT
---

# DARIO Skill — Brand Positioning (Self-Polishing)

Padrão A wrapper around `dario-brand`. Base skill achieves ~85 quality autonomous; production-polished hits ~92. This wrapper closes the gap via internal generate→critique→revise loop within one Claude Code session. **Zero marginal API cost under Claude Max.**

## When to use this vs `dario-brand`

| Situation | Use |
|---|---|
| Quick positioning exercise, internal review expected | `dario-brand` |
| Brand statement going to client deck / public site | **`dario-brand-polished`** |
| `execution_policy: client_facing` in orchestrator | **`dario-brand-polished`** |

Original `dario-brand` unchanged — zero functionality loss.

---

## Workflow (5 steps, MUST execute all in order)

### Step 1 — GENERATE v1

**MANDATORY first action — load the base skill's full content:**

```
Read tool → ~/.claude/skills/dario-brand/SKILL.md
```

The polished wrapper SKILL.md (this file) contains only the polish-loop
mechanics — it does NOT contain the base skill's frameworks, RAG queries,
or domain expertise. Without reading the base skill first, you will
improvise and produce v1 quality below the wrappers' validated baseline.

After reading base, follow its workflow to produce v1.

Execute full `dario-brand` workflow:
- RAG consult (Kapferer Prism + Neumeier Zag + StoryBrand SB7 + Aaker)
- Gather inputs (target, competitors, differential, tone)
- Pick primary framework
- Produce: positioning statement, archetype, messaging hierarchy, brand voice, differentiation matrix

Mark internally: `### DRAFT v1 (internal — not delivered)`.

### Step 2 — SELF-CRITIQUE (5-dim, 0-100)

Be brutally honest. Brand work is especially prone to vague/aspirational scoring inflation.

```
1. Specificity (0-20) — Does the statement reference the actual client/vertical?
   (Not "we help businesses grow" — that's generic; needs concrete target + pain)
2. Actionability (0-20) — Can a copywriter/designer USE the statement?
   (Concrete enough to drive headline, logo brief, tone-of-voice doc)
3. Completeness (0-20) — All 5 frameworks layered (Kapferer/Neumeier/SB7/Aaker)?
   (Or explicit reason for choosing subset)
4. Accuracy (0-20) — Does archetype match actual brand evidence?
   (E.g., "Hero" archetype for a quirky D2C startup = mismatch)
5. Tone (0-20) — Does positioning voice match intended audience?
   (HNW vs SMB vs Gen Z = different registers)
```

Document the critique explicitly with reasoning per dim + Total + Weakest dim(s) + Specific issues to fix in v2.

### Step 3 — DECISION GATE

- **TOTAL ≥ 92:** skip Step 4, output v1 final
- **TOTAL ≥ 80 AND no dim < 14:** proceed to revise
- **TOTAL < 80 OR any dim < 14:** STOP, ask user for clarification on weakest dim

### Step 4 — REVISE → v2

Targeted edits only:
- Specificity weak: inject client/vertical concrete details
- Actionability weak: tighten statement, add taglines candidates
- Completeness weak: layer in missing framework outputs
- Accuracy weak: re-pick archetype with justification
- Tone weak: rewrite in correct register

Output v2. Mark: `### DRAFT v2 (revised)`.

### Step 5 — RE-SCORE + OUTPUT FINAL

Re-run Step 2 critique on v2. Output best of (v1, v2) with metadata block at end:

### Step 6 — RECORD TELEMETRY (mandatory, append-only)

After delivering the final output, invoke the telemetry recorder via Bash to log this run into the production rolling metrics. Without this, the system has no evidence Padrão A is paying off for this skill.

```bash
cd ~/.claude/orchestrator && \
.venv/Scripts/python.exe -m scripts.record_polished_run \
    --skill dario-brand-polished \
    --v1-score $V1_SCORE \
    --v2-score $V2_SCORE \
    --final $FINAL \
    --client $CLIENT_SLUG \
    --briefing-summary "$ONE_LINE_DESCRIPTION" \
    --gate-decision $GATE_DECISION \
    --status-mix "$VERIFIED/$ASSUMED/$PROJECTION"
```

Where:
- `$GATE_DECISION` ∈ {`revised`, `ship_v1`, `aborted`}
- `--v2-score` omitted when `gate_decision=ship_v1` or `aborted`
- `--final` ∈ {`v1`, `v2`, `aborted`}

Appends one entry to `~/.claude/orchestrator/quality/polished_production_runs.yaml`. Aggregator (`scripts/aggregate_polished_metrics.py`) computes per-skill 30-day metrics on demand or via cron.

**DO NOT skip this step.** This is what closes the loop on the "track production_avg_delivery_ready 90 days" goal.


```
## Polish Metadata
- v1 score: X/100 (S/A/C/A/T breakdown)
- v2 score: X/100 (S/A/C/A/T breakdown)
- Final delivered: vN (reason)
- Status mix: N 🔵 · N 🟡 · N 🟢
```

---

## A/B Test Protocol

**Baseline:** dario-brand production_avg_delivery_ready = 85.7 (n=7 outputs, source `quality/skill-metrics.yaml`).
**Threshold:** ≥+4pts lift across 3 real-briefing tests → propagation validated.
**Test briefings:** use 3 client briefings (Cuidaí, Atrium Premium RE, SAQUEI brand statements).

---

## Integration with orchestrator

```yaml
- id: CLIENT-BRAND-001
  skill: dario-brand-polished   # for client_facing tasks
  execution_policy: client_facing
```

---

## Red flags

- ❌ Score archetype higher than warranted to skip revision — invalidates the loop
- ❌ Output v2 when v2 scored lower than v1 — always pick best
- ❌ Use on sparse briefings — output won't exceed v1 quality, wastes tokens

---

<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every claim in **dario-brand-polished** output must carry an EXPLICIT label.

- 🔵 **verified** — confirmed from briefing/competitive research/RAG
- 🟡 **assumed** — plausible default needing client confirmation
- 🟢 **projection** — opinion/recommendation (archetype choice, taglines)

**Why:** brand work mixes verified facts (client industry, competitors named) with judgment calls (archetype, voice). Reader needs to know which is which to push back constructively.

**How to apply:**
1. After Step 5 final, label every name, claim, comparison.
2. Justify archetype choice with evidence (🔵) or call it 🟡 if subjective.
3. End with Status Mix count: `Status mix: N 🔵 · N 🟡 · N 🟢`.

❌ NOT delivery-ready:
```
Posicionamento: "Somos o Notion para [vertical]." Archetype: Sage. Diferencial: simplicidade.
```

✅ Delivery-ready:
```
- Posicionamento "O Notion para famílias com idosos" 🔵 verified (insight central briefing CUI-014)
- Archetype: Caregiver (não Sage) 🟡 assumed (matches "cuida + ai" wordmark + audience emocional; precisa A/B test)
- Diferencial: "filho usa, idoso só recebe WhatsApp" 🔵 verified (Wave 0 patterns)

Status mix: 2 🔵 · 1 🟡 · 0 🟢
```
<!-- gate7:end -->
