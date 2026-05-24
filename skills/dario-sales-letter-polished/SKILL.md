---
name: dario-sales-letter-polished
description: "Self-polishing long-form sales letter — autonomous variant of dario-sales-letter. Internally runs generate → critique → revise → final within one Claude Code session. Use when copy must ship to landing/email without human polish. Triggers: 'sales letter polished', 'copy autónoma', 'long-form ready-to-ship'."
argument-hint: "[product + audience + offer + objections]"
allowed-tools: Read, Write, Glob, Grep
license: MIT
---

# DARIO Skill — Sales Letter (Self-Polishing)

Padrão A wrapper around `dario-sales-letter`. Base autonomous ceiling ~83 (verbose copy is hardest skill). Production polished hits ~89. Wrapper closes the gap. **Zero marginal API cost under Claude Max.**

## When to use this vs `dario-sales-letter`

| Situation | Use |
|---|---|
| Internal copy draft, brand will review | `dario-sales-letter` |
| Landing page hero + body going LIVE | **`dario-sales-letter-polished`** |
| Cold email sequence to enterprise list | **`dario-sales-letter-polished`** |

---

## Workflow (5 steps, MUST execute all in order)

### Step 1 — GENERATE v1

Execute full `dario-sales-letter` workflow:
- RAG consult (Gary Halbert + Eugene Schwartz + Dan Kennedy + StoryBrand + Jon Benson VSL)
- Gather: product, audience awareness level (Schwartz 5), pain points, objections, offer
- Build: hook, problem agitation, solution intro, proof, offer, urgency, CTA, PS x3

Mark: `### DRAFT v1 (internal — not delivered)`.

### Step 2 — SELF-CRITIQUE (5-dim, 0-100)

Sales copy is gameable — long ≠ good. Score for cut-ability + emotional truth.

```
1. Specificity (0-20) — Hook + body reference real client/vertical evidence?
   (Not "Imagine waking up rich" — that's generic; specific scenario)
2. Actionability (0-20) — Single clear CTA + offer terms?
   (Pricing, deadline, button copy, refund terms)
3. Completeness (0-20) — All 8 structural pieces present?
   (hook / agitation / solution / proof / offer / urgency / CTA / PS)
4. Accuracy (0-20) — Proof claims (testimonials, case studies) traceable?
   (Made-up testimonial = 0/20 on accuracy)
5. Tone (0-20) — Matches audience awareness level (unaware vs solution-aware vs product-aware)?
```

Document with reasoning per dim + Total + Weakest dim(s) + Specific issues for v2.

### Step 3 — DECISION GATE

- **TOTAL ≥ 92:** output v1 final
- **TOTAL ≥ 80 AND no dim < 14:** revise
- **TOTAL < 80 OR any dim < 14:** STOP, ask user for missing inputs (testimonials, offer terms, objections)

### Step 4 — REVISE → v2

Targeted fixes:
- Specificity weak: rewrite hook with concrete client/vertical scenario from briefing
- Actionability weak: collapse multiple CTAs to ONE; clarify offer terms
- Accuracy weak: remove unverified testimonials OR mark as 🟡 needs founder confirmation
- Completeness weak: add missing structural piece
- Tone weak: re-register for awareness level

Output v2.

### Step 5 — RE-SCORE + OUTPUT FINAL

Re-run critique. Output best with metadata block.

### Step 6 — RECORD TELEMETRY (mandatory, append-only)

After delivering the final output, invoke the telemetry recorder via Bash to log this run into the production rolling metrics. Without this, the system has no evidence Padrão A is paying off for this skill.

```bash
cd ~/.claude/orchestrator && \
.venv/Scripts/python.exe -m scripts.record_polished_run \
    --skill dario-sales-letter-polished \
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

**Baseline:** dario-sales-letter no production scoring history (skill less-used). Use synthetic baseline ~83 from refactored SKILL.md scoring round.
**Threshold:** ≥+4pts lift on 3 real briefings.
**Test briefings:** Cuidaí landing hero / SAQUEI relatório hero / Tributário.AI cold email sequence.

---

## Red flags

- ❌ Fake testimonials or "average customer" stats — Accuracy + ethics fail
- ❌ Multiple CTAs in same letter — Actionability fail (must pick ONE)
- ❌ Hook that doesn't reference audience pain — Specificity fail
- ❌ "Limited time!" without dated deadline — Accuracy + Tone fail

---

<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every quantified claim must carry an EXPLICIT label.

- 🔵 **verified** — testimonial actual + named, statistic from primary source
- 🟡 **assumed** — generic benchmark (e.g., "average client saves X hours")
- 🟢 **projection** — dream outcome promise ("imagine X")

**Why:** copy mixes hard proof (named testimonials, real stats) with soft promises (dream outcome). Reader needs to know which is which to assess credibility.

❌ NOT delivery-ready:
```
"Our clients save 8 hours/week and increase revenue 32%."
```

✅ Delivery-ready:
```
"Our 14 enterprise clients save an average of 6.2 hours/week 🔵 verified (Q1 2026 customer survey, n=14, methodology in app/metrics)
and report 18-32% revenue lift in their first quarter 🟡 assumed (self-reported in NPS survey, not independently audited)."
```
<!-- gate7:end -->
