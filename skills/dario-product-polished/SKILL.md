---
name: dario-product-polished
description: "Self-polishing product development workflow — autonomous variant of dario-product. Internally runs generate → critique → revise → final within one Claude Code session. Use when PRD / user stories / MVP scope must ship to eng team without human polish. Triggers: 'product polished', 'PRD autónomo', 'MVP scope ready-to-ship'."
argument-hint: "[product goal + users + constraints + horizon]"
allowed-tools: Read, Write, Glob, Grep
license: MIT
---

# DARIO Skill — Product Development (Self-Polishing)

Padrão A wrapper around `dario-product`. Base autonomous ceiling ~86 (product specs are mid-difficulty). Production polished hits ~92. Wrapper closes the gap. **Zero marginal API cost under Claude Max.**

## When to use this vs `dario-product`

| Situation | Use |
|---|---|
| Quick MVP sketch for alignment call | `dario-product` |
| PRD going to engineering for build | **`dario-product-polished`** |
| Sprint planning with capacity commitment | **`dario-product-polished`** |
| Feature prioritization presented to stakeholders | **`dario-product-polished`** |

---

## Workflow (5 steps, MUST execute all in order)

### Step 1 — GENERATE v1

**MANDATORY first action — load the base skill's full content:**

```
Read tool → ~/.claude/skills/dario-product/SKILL.md
```

The polished wrapper SKILL.md (this file) contains only the polish-loop
mechanics — it does NOT contain the base skill's frameworks, RAG queries,
or domain expertise. Without reading the base skill first, you will
improvise and produce v1 quality below the wrappers' validated baseline.

After reading base, follow its workflow to produce v1.

Execute full `dario-product` workflow:
- Gather: goal, users, constraints (tech/budget/timeline), success metrics
- Build: PRD sections, user stories (3-5 P0), MVP scope (in/out), acceptance criteria, sprint plan, dependencies

Mark: `### DRAFT v1 (internal — not delivered)`.

### Step 2 — SELF-CRITIQUE (5-dim, 0-100)

Product specs are gamed by wishful scope. Score for actionability under real constraints.

```
1. Specificity (0-20) — User stories tied to actual users from briefing?
   (Not "as a user, I want..." — name the persona)
2. Actionability (0-20) — Can eng team start building tomorrow?
   (Acceptance criteria measurable; dependencies named; story points realistic)
3. Completeness (0-20) — PRD + user stories + scope + AC + sprint plan + deps all present?
4. Accuracy (0-20) — Estimates defensible? Dependencies real?
   (E.g., "1 sprint for OAuth" = 12/20 if no OAuth library named)
5. Tone (0-20) — Technical register appropriate (eng vs PM vs exec)?
```

Document with reasoning per dim + Total + Weakest dim(s) + Specific issues for v2.

### Step 3 — DECISION GATE

- **TOTAL ≥ 92:** output v1
- **TOTAL ≥ 80 AND no dim < 14:** revise
- **TOTAL < 80 OR any dim < 14:** STOP, ask user for missing constraints/users/success criteria

### Step 4 — REVISE → v2

Targeted fixes:
- Specificity weak: name personas with attributes from briefing
- Actionability weak: rewrite AC as Given/When/Then; add story points + dependencies
- Completeness weak: add missing section (most often: dependencies or out-of-scope explicit)
- Accuracy weak: re-estimate with named tools/libraries
- Tone weak: re-register for audience

Output v2.

### Step 5 — RE-SCORE + OUTPUT FINAL

Re-run critique. Output best with metadata.

### Step 6 — RECORD TELEMETRY (mandatory, append-only)

After delivering the final output, invoke the telemetry recorder via Bash to log this run into the production rolling metrics. Without this, the system has no evidence Padrão A is paying off for this skill.

```bash
cd ~/.claude/orchestrator && \
.venv/Scripts/python.exe -m scripts.record_polished_run \
    --skill dario-product-polished \
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


---

## A/B Test Protocol

**Baseline:** dario-product no recent production scoring. Use SAQUEI 50+ features + 15 admin pages spec as proxy (well-executed).
**Threshold:** ≥+4pts lift on 3 real briefings.
**Test briefings:** Cuidaí calendar-shared P0 feature / SAQUEI subscription engine PRD / Tributário.AI ERP integration spec.

---

## Red flags

- ❌ "As a user, I want X" — Specificity fail (name persona)
- ❌ "Acceptance: works as expected" — Actionability fail (no measurable criteria)
- ❌ Out-of-scope absent — Completeness fail (scope without OOS = scope creep waiting)
- ❌ Estimates without named library/tool — Accuracy fail

---

<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every requirement + estimate must carry an EXPLICIT label.

- 🔵 **verified** — user feedback / existing telemetry / current code
- 🟡 **assumed** — best-practice default needing user validation
- 🟢 **projection** — estimated story points, future user count, ROI projections

**Why:** PRDs blend known requirements with assumed defaults and projected impact. Eng team needs to know which is fixed vs negotiable.

❌ NOT delivery-ready:
```
P0 calendar shared, supports 5 users, 2 sprints to ship.
```

✅ Delivery-ready:
```
- P0 calendar shared 🔵 verified (mom test n=15, 11/15 mentioned coordinating siblings)
- Supports 5 users initial scope 🟡 assumed (default for "irmãos" persona; needs founder confirm if extended family allowed)
- 2 sprints estimate 🟢 projection (assumes Next.js App Router + Supabase real-time; depends on RBAC complexity from CUI-048)
- Dep: CUI-048 permissions matrix MUST be merged before P0 starts 🔵 verified (CUI-048 score 99/100, ready)

Status mix: 2 🔵 · 1 🟡 · 1 🟢
```
<!-- gate7:end -->
