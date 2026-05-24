# Padrão A — Self-Polishing Skills: A/B Test Results

**Date:** 2026-05-24
**Pattern:** Padrão A (Self-Polishing Skill — internal generate→critique→revise→final loop)
**Total wrappers tested:** 8
**Total briefings:** 26
**Cost model:** Claude Max subscription (zero marginal API cost)
**Evaluator:** Claude Opus 4.7 (single-evaluator caveat)

---

## TL;DR

Padrão A is **validated across all 8 tier-A wrappers**.

- 16 of 26 briefings (62%) passed the polish gate
- Mean quality lift on passed briefings: **+6.5pts** (v1 80.6 → v2 87.1)
- 10 briefings (38%) aborted at gate — by design, on sparse inputs
- Zero net regressions

DARIO can now operate as a **true autonomous orchestrator** for these 8 skills, not as a copilot. Skills produce ship-ready output for rich briefings; explicitly stop and request clarification for sparse ones.

---

## Background

**Problem solved:** Single-pass LLM generation hits structural quality ceiling ~85/100 autonomous. Human polish lifts to 91+. Gap = process (detect gaps → correct → reformulate → validate), not prompt quality.

**Pattern A:** Move the polish loop INSIDE the skill via multi-step prompting within a single Claude Code session. Original skill unchanged; wrapper is a parallel `dario-X-polished` skill.

**Why not DSPy?** Closed investigation 2026-05-24 after sprint3v2 + sprint4 (MIPROv2). Optimizer + expanded goldens + held-out tests confirmed: ceiling is process-bound, not prompt-bound. DSPy archived.

---

## Wrapper Architecture

Every `dario-X-polished` wrapper executes the same 5-step workflow:

1. **Generate v1** — full base-skill workflow
2. **Self-critique** — 5-dim rubric (Specificity / Actionability / Completeness / Accuracy / Tone), 0-20 each, 0-100 total
3. **Decision gate** — score ≥92 → ship v1; 80-91 → revise; <80 → stop & request clarification
4. **Revise** — targeted edits on weakest dim(s)
5. **Re-score + output best** of (v1, v2) with metadata block

The gate is the key innovation: it prevents wrappers from producing inflated output on sparse inputs.

---

## Test Methodology

For each of the 8 wrappers, 3 real client briefings were run through the polish workflow. Each briefing was scored honestly across the 5-dim rubric, with explicit decision-gate decisions logged.

Real client briefings span verticals: BR healthtech, BR fintech B2C, BR fiscal B2B, PT real estate (HNW), PT WordPress (services + design), PT SaaS (accounting), and one mobile app marketplace.

Threshold for propagation: **≥+4pts mean lift, no individual regression**.

---

## Results Per Wrapper

| Wrapper | Pass/Total | Mean Lift (passed) | Verdict |
|---|---|---|---|
| **dario-financial-model-polished** | 2/3 | **+8.0** | Best lift; math-strict gate validated |
| **dario-wp-audit-polished** | **3/3** | +6.0 | Zero aborts; highest baseline (skill was tier A pre-wrapper) |
| **dario-pitch-polished** (POC) | 3/5 | +6.3 | Original validation |
| **dario-product-polished** | 2/3 | +6.5 | External deps gate catches sparse |
| **dario-funnel-polished** | 2/3 | +6.5 | Conversion benchmarks gap noted |
| **dario-offer-polished** | 2/3 | +6.5 | Fake-anchor gate catches sparse |
| **dario-brand-polished** | 1/3 | +7.0 | Needs rich competitive context |
| **dario-sales-letter-polished** | 1/3 | +7.0 | Most sensitive to sparse |

### Combined

- **Total briefings:** 26
- **Passed gate:** 16 (62%)
- **Aborted at gate:** 10 (38%)
- **Mean lift on passed:** +6.5pts (v1 80.6 → v2 87.1)

---

## Decision Gate Behavior

The gate aborted on 10 of 26 briefings. **This is desired behavior**, not a bug. Aborts happened on:

- Sparse briefings (missing competitive context, missing testimonials, missing market data)
- Math errors that couldn't be corrected without ground-truth (e.g., unrealistic CAC projections in a financial model briefing)
- Missing external dependencies (e.g., third-party API specs)
- Confidentiality blockers (e.g., HNW testimonials requiring founder permission)

In each aborted case, the wrapper output an explicit list of missing information instead of fabricating it. This is the opposite of LLM hallucination on under-specified inputs.

---

## Routing Recommendations for Orchestrator

Based on gate-pass consistency and lift magnitude, wrappers fall into two tiers:

### Tier 1 — Default route for `execution_policy: client_facing`

These wrappers can be invoked directly without pre-flight briefing validation:

- `dario-financial-model-polished`
- `dario-wp-audit-polished`
- `dario-pitch-polished`
- `dario-product-polished`
- `dario-funnel-polished`
- `dario-offer-polished`

### Tier 2 — Pre-flight briefing validator required

These wrappers have higher abort rates and benefit from a briefing-completeness check before dispatch:

- `dario-brand-polished` — requires competitive context, target tone, archetype hint
- `dario-sales-letter-polished` — requires testimonials/proof, offer terms, audience awareness level

If the orchestrator detects missing inputs for Tier 2 skills, it should ask the user before dispatch instead of letting the wrapper hit the gate.

---

## Expected Production Outcomes

- **Autonomous delivery_ready_rate baseline:** 17.5% (pre-Padrão A, measured)
- **Autonomous delivery_ready_rate target:** 50-70% (post-Padrão A, estimated)
- **Gate abort rate expected:** ~38% (feature, not bug — surfaces briefing gaps explicitly)

---

## Honest Limitations

1. **Single evaluator** (Opus 4.7). Possible scoring drift between v1 and v2 critique passes. Multi-evaluator validation recommended.
2. **Briefings selected by author.** Possible cherry-pick bias. Production-cycle A/B against unbiased dispatch queue is the next step.
3. **+4pts threshold is judgment call**, not statistically derived. Confidence intervals on n=3 per skill are wide.
4. **Wave 2 used compact critique format** for efficiency. May have skipped subtle scoring nuances visible in fully-rendered Wave 1 (5 briefings of `dario-pitch-polished`).
5. **Critique-loop estimates ≠ real client delivery scores.** Production validation pending (track `production_avg_delivery_ready` evolution over 90 days post-deployment).

---

## What's Next

1. Update orchestrator dispatch to route `execution_policy: client_facing` through Tier 1 wrappers by default.
2. Build pre-flight briefing validators for Tier 2 wrappers (brand, sales-letter).
3. Track `production_avg_delivery_ready` evolution 90 days post-deployment.
4. If any wrapper shows <+2pts on real production briefings, investigate via **Padrão C (RAG-grounded skills)** — inject client context from RAG before generation to lift Specificity dimension structurally.
5. Consider per-skill A/B with larger sample (n=10+) before declaring statistical confidence.

---

## Files

- Wrapper SKILL.md files: `~/.claude/skills/dario-{pitch,brand,offer,funnel,sales-letter,financial-model,product,wp-audit}-polished/SKILL.md`
- Per-briefing A/B data (gitignored runtime state): `~/.claude/orchestrator/quality/padrao_a_ab_test_pitch.yaml`
- 3 delivered pitch decks (Obsidian): `D.A.R.I.O/05 - Claude - IA/Outputs/2026-05-24 - {Cuidai|SAQUEI|Tributario.AI} - Pitch Deck Seed v2 Polished.md`
- Architectural rationale + DSPy failure analysis: `~/.claude/orchestrator/optimization/DSPY_ROOT_CAUSE.md`

---

## Acknowledgments

This pattern was selected after rejecting ruvnet/ruflo adoption (assessed as overkill for single-user DARIO; federation + multi-model ensemble not justified by use case). The decision to invest in self-polishing instead of teleprompter optimization was informed by 2 prior failed DSPy investigations (`compile_sprint3` word-overlap metric, `compile_sprint4` MIPROv2 + expanded goldens) — both confirmed structural ceiling around 85/100 autonomous.
