---
name: dario-offer-polished
description: "Self-polishing Grand Slam Offer builder — autonomous variant of dario-offer. Internally runs generate → critique → revise → final within one Claude Code session. Use when offer must ship client-ready. Triggers: 'offer polished', 'grand slam offer ready', 'oferta autónoma'."
argument-hint: "[business + target + pricing + competitive context]"
allowed-tools: Read, Write, Glob, Grep
license: MIT
---

# DARIO Skill — Grand Slam Offer (Self-Polishing)

Padrão A wrapper around `dario-offer`. Base skill autonomous ceiling ~85 (sprint4 evidence: 83.6 ± 1.59). Production polished hits ~88. Wrapper closes gap via internal polish loop. **Zero marginal API cost under Claude Max.**

## When to use this vs `dario-offer`

| Situation | Use |
|---|---|
| Internal offer draft, will review before send | `dario-offer` |
| Sales letter / landing page offer block | **`dario-offer-polished`** |
| Client-facing proposal with pricing commitment | **`dario-offer-polished`** |

Original `dario-offer` unchanged.

---

## Workflow (5 steps, MUST execute all in order)

### Step 1 — GENERATE v1

Execute full `dario-offer` workflow (Hormozi value equation):
- RAG consult (Hormozi $100M Offers + $100M Leads + value stack)
- Gather inputs (business, target, current pricing, competitor offers)
- Build: core_offer, value_equation (Dream/Likelihood/Time/Effort), risk_reversal, 3 bonuses with anchor values, urgency

Mark: `### DRAFT v1 (internal — not delivered)`.

### Step 2 — SELF-CRITIQUE (5-dim, 0-100)

Offers are especially gameable — easy to score high with fake bonuses + fake urgency. Be ruthless.

```
1. Specificity (0-20) — Are dream outcome, bonus values, urgency tied to REAL data from briefing?
   (Not generic SaaS template; concrete client/vertical hooks)
2. Actionability (0-20) — Can prospect ACT on offer immediately?
   (Pricing concrete, bonuses claimable, urgency real deadline not faked)
3. Completeness (0-20) — All 6 parts present with substance?
   (core / value_eq / risk_reversal / bonuses[3] / urgency / pricing)
4. Accuracy (0-20) — Math defensible? Bonuses anchored at credible market value?
   (Bonus stated "valor €2.500" must reflect actual market price; faked anchors kill trust)
5. Tone (0-20) — Register matches buyer (HNW vs SMB vs prosumer)?
```

Document with reasoning + Total + Weakest dim(s) + Specific issues to fix in v2.

### Step 3 — DECISION GATE

- **TOTAL ≥ 92:** output v1 final
- **TOTAL ≥ 80 AND no dim < 14:** proceed to revise
- **TOTAL < 80 OR any dim < 14:** STOP, request briefing clarification

### Step 4 — REVISE → v2

Targeted fixes:
- Specificity weak: inject briefing data into bonuses + urgency
- Accuracy weak: re-anchor bonus values to real market, recompute value equation
- Actionability weak: convert vague urgency to dated deadline + concrete capacity number
- Completeness weak: fill missing component
- Tone weak: re-register

Output v2.

### Step 5 — RE-SCORE + OUTPUT FINAL

Re-run critique on v2. Output best with metadata block.

### Step 6 — RECORD TELEMETRY (mandatory, append-only)

After delivering the final output, invoke the telemetry recorder via Bash to log this run into the production rolling metrics. Without this, the system has no evidence Padrão A is paying off for this skill.

```bash
cd ~/.claude/orchestrator && \
.venv/Scripts/python.exe -m scripts.record_polished_run \
    --skill dario-offer-polished \
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

**Baseline:** dario-offer sprint4 held-out 83.6 ± 1.59 (n=9), production_avg 88.0 (n=1).
**Threshold:** ≥+4pts lift on 3 real briefings.
**Test briefings:** Cuidaí Familia+ R$ 49,90 offer / Atrium retainer model / SAQUEI subscription offer.

---

## Red flags

- ❌ Faking bonus anchor values to inflate perceived value — burns trust + violates Hormozi principle
- ❌ Fake urgency ("limited time!" without deadline date) — counts as Tone failure
- ❌ Risk reversal without concrete trigger (vague "satisfaction guarantee" = 12/20 not 18)
- ❌ Skip critique to ship faster — invalidates the loop

---

<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every claim in **dario-offer-polished** output must carry an EXPLICIT label.

- 🔵 **verified** — pricing/data from briefing or competitive research
- 🟡 **assumed** — bonus anchor value or capacity number needing validation
- 🟢 **projection** — dream outcome quantification, conversion estimates

**Why:** offers blend hard pricing data with soft promises (dream outcomes, bonuses). Reader needs to distinguish committed pricing from aspirational anchors.

❌ NOT delivery-ready:
```
R$ 29,90/mês família + 3 bonuses valor R$ 800 total + garantia 30 dias.
```

✅ Delivery-ready:
```
- Pricing R$ 29,90 família 🔵 verified (briefing)
- Bonus 1: relatório burden index ZBI-12 (valor R$ 300) 🟡 assumed (precisa benchmark mercado relatórios clínicos)
- Bonus 2: cross-sell SAQUEI grátis 30d (valor R$ 89) 🔵 verified (SAQUEI pricing actual)
- Bonus 3: 1-1 onboarding 30min (valor R$ 250) 🟢 projection (anchor pelo hourly rate consultor)
- Garantia "se não usar 7 dias → refund total" 🔵 verified (política Stripe configurada)

Status mix: 2 🔵 · 1 🟡 · 1 🟢
```
<!-- gate7:end -->
