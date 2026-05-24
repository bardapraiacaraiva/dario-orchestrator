---
name: dario-financial-model-polished
description: "Self-polishing financial model builder — autonomous variant of dario-financial-model. Internally runs generate → critique → revise → final within one Claude Code session. Use when financial model must ship to investor/board without human polish. Triggers: 'financial model polished', 'P&L autónomo', 'forecast ready-to-ship'."
argument-hint: "[business model + revenue streams + cost structure + horizon]"
allowed-tools: Read, Write, Glob, Grep
license: MIT
---

# DARIO Skill — Financial Model (Self-Polishing)

Padrão A wrapper around `dario-financial-model`. Financial models are HIGHEST risk for hallucination — wrong math kills credibility instantly. Polish loop catches math errors before delivery. **Zero marginal API cost under Claude Max.**

## When to use this vs `dario-financial-model`

| Situation | Use |
|---|---|
| Internal sanity check / scenario exploration | `dario-financial-model` |
| Investor deck financial section | **`dario-financial-model-polished`** |
| Board financial review | **`dario-financial-model-polished`** |
| Pricing decision with revenue impact | **`dario-financial-model-polished`** |

---

## Workflow (5 steps, MUST execute all in order)

### Step 1 — GENERATE v1

Execute full `dario-financial-model` workflow:
- Gather: revenue streams + pricing tiers + customer growth assumption + cost structure (CAC, COGS, opex)
- Build: P&L 12-24 months, cash flow, break-even month, scenario sensitivity (-30%/-+30% revenue)
- Output as tables + key metric summary (BE, runway, ARR at M12, gross margin)

Mark: `### DRAFT v1 (internal — not delivered)`.

### Step 2 — SELF-CRITIQUE (5-dim, 0-100) — MATH EXTRA WEIGHT

Financial models = Accuracy must be 18+. Anything less is a deal-killer.

```
1. Specificity (0-20) — Assumptions tied to briefing (pricing, ramp, costs)?
2. Actionability (0-20) — Can finance team load this into their Excel today?
3. Completeness (0-20) — P&L + cash flow + BE + sensitivity all present?
4. Accuracy (0-20) — RE-VERIFY EVERY MATH (sum of P&L lines, runway = cash/burn, BE month math, ARR formula)?
   *Single math error → score this dim 12 or lower*
5. Tone (0-20) — Conservative vs optimistic registered explicitly?
```

**REQUIRED in Step 2:** explicitly re-do the math for at least 3 key numbers. Show your arithmetic.

### Step 3 — DECISION GATE

- **Accuracy < 16:** STOP unconditionally (cannot ship math errors)
- **TOTAL ≥ 92:** output v1
- **TOTAL ≥ 80 AND Accuracy ≥ 16:** revise
- **TOTAL < 80:** STOP, ask user for missing assumptions

### Step 4 — REVISE → v2

Targeted math fixes:
- Recompute any line where v1 critique flagged error
- Restate assumptions explicitly (don't hide them in narrative)
- Add scenario sensitivity if missing
- Convert any % without absolute number to "X% (= R$ Y)"

Output v2.

### Step 5 — RE-SCORE + OUTPUT FINAL

Re-run critique with full math re-verification. Output best with metadata.

---

## A/B Test Protocol

**Baseline:** dario-financial-model production scoring varies — no consistent baseline. Use Tributário.AI financial model v1.0 (R$ 110K cash, BE M6, R$ 1M ARR M12) as test case for v2 polish lift.
**Threshold:** ≥+4pts lift + zero math errors after polish.
**Test briefings:** Tributário.AI 18-month / Cuidaí seed model / SAQUEI scale model.

---

## Red flags

- ❌ Ship model with un-verified arithmetic — kills investor trust permanently
- ❌ Hide assumptions in prose ("assuming reasonable growth") — Specificity + Accuracy fail
- ❌ Single scenario only — Completeness fail (need 3: conservative/base/aggressive)
- ❌ % without absolute number — Actionability fail (finance team can't plug into Excel)

---

<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7) — FINANCIAL MODELS

Every numeric assumption + projection must carry an EXPLICIT label.

- 🔵 **verified** — actual data from briefing (current MRR, headcount, runway)
- 🟡 **assumed** — industry benchmark or estimate (e.g., "B2C SaaS churn 5%")
- 🟢 **projection** — forward-looking number (forecast revenue, future hire ramp)

**Why:** financial models conflate "what is" with "what we hope will be". Without labels, investors can't pressure-test assumptions.

❌ NOT delivery-ready:
```
M12 ARR R$ 1M, CAC R$ 200, LTV R$ 1.800, gross margin 78%.
```

✅ Delivery-ready:
```
- M12 ARR R$ 1M 🟢 projection (1000 clients × R$ 83 ARPU × 12; assumes 60 new/mo from M6)
- CAC R$ 200 🟡 assumed (B2C SaaS BR benchmark 2024; current CAC unknown, no paid spend yet)
- LTV R$ 1.800 🟢 projection (R$ 83 ARPU × 22 mo avg lifetime at 5% monthly churn)
- Gross margin 78% 🔵 verified (current COGS = Stripe 4% + Resend + Twilio = 22% of revenue)
- Burn rate R$ 12K/mo 🔵 verified (current actual, 18-mo runway with R$ 110K + R$ 110K bootstrap)

Status mix: 2 🔵 · 1 🟡 · 2 🟢
```
<!-- gate7:end -->
