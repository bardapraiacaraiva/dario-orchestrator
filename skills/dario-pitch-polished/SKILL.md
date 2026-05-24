---
name: dario-pitch-polished
description: "Self-polishing pitch deck generator — single-skill autonomous version of dario-pitch. Internally runs generate → critique → revise → final loop within one Claude Code session. Use when delivery must be client-ready without human polish. Triggers: 'pitch polished', 'pitch ready-to-ship', 'pitch autonomous', 'pitch sem revisão'."
argument-hint: "[client/venture brief + audience + ask]"
allowed-tools: Read, Write, Glob, Grep
license: MIT
---

# DARIO Skill — Pitch Deck (Self-Polishing)

This is the **autonomous-ready variant** of `dario-pitch`. The base skill achieves ~85-87 quality on raw briefings (held-out evidence sprint4 2026-05-24). To reach the 91+ that humans hit with polish, this wrapper executes an internal **generate → critique → revise → final** loop within a single Claude Code session.

**Architecture pattern:** Padrão A from `DSPY_ROOT_CAUSE.md` follow-up (2026-05-24). Zero marginal API cost under Claude Max — all runs within the active session.

## When to use this vs `dario-pitch`

| Situation | Use |
|---|---|
| Quick first-draft pitch, internal review expected | `dario-pitch` (faster, single-pass) |
| Client-facing pitch that must ship without polish | **`dario-pitch-polished`** |
| `execution_policy: client_facing` or `critical` in orchestrator task | **`dario-pitch-polished`** |
| Atrium HNW pitches, investor decks, board presentations | **`dario-pitch-polished`** |
| A/B testing autonomous quality | **`dario-pitch-polished`** (vs `dario-pitch` baseline) |

The base `dario-pitch` skill remains unchanged and continues to work for all existing flows.

---

## Workflow (5 steps, MUST execute all of them, in order)

### Step 1 — GENERATE v1 (raw draft)

Execute the full `dario-pitch` workflow as if you were that skill:
- Gather inputs (audience, ask, stakes, proof, analogy)
- RAG consult (Klaff STRONG + Duarte Sparkline + Campbell + Park Howell ABT)
- Choose primary framework by context
- Produce the 12-slide outline with `narrative_arc`, `key_slides`, `tam_sam_som`, `financial_ask`

Output v1 internally — do NOT show to user yet. Mark it clearly: `### DRAFT v1 (internal — not delivered)`.

### Step 2 — SELF-CRITIQUE using JUDGE rubric

Score v1 against this 5-dimension rubric (0-20 each, 0-100 total). Be brutally honest — overscoring kills the loop:

```
1. Specificity (0-20) — Does it reference concrete data from the briefing?
   (Client name, real numbers, vertical-specific facts, not generic SaaS template)
2. Actionability (0-20) — Are next steps unambiguous?
   (Concrete ask amount, specific milestones, dated commitments)
3. Completeness (0-20) — Are all 12 slides + tam_sam_som + financial_ask filled with substance?
   (No placeholder phrasing, no "TBD", no empty bullets)
4. Accuracy (0-20) — Are facts/numbers verifiable and internally consistent?
   (TAM > SAM > SOM math holds; equity/valuation math holds; market sizing defensible)
5. Tone (0-20) — Is format appropriate for the audience?
   (HNW = sober + specific; VC = punchy + ambitious; board = data-first)
```

**Document the critique explicitly** in your response:

```
### CRITIQUE v1
- Specificity: X/20 — [1-line reasoning]
- Actionability: X/20 — [1-line reasoning]
- Completeness: X/20 — [1-line reasoning]
- Accuracy: X/20 — [1-line reasoning]
- Tone: X/20 — [1-line reasoning]
- TOTAL: X/100

Weakest dim(s): [name them]
Specific issues to fix in v2:
1. [concrete fix #1]
2. [concrete fix #2]
3. [concrete fix #3]
```

### Step 3 — DECISION GATE

- **If TOTAL ≥ 92:** v1 is ready. Skip to Step 5, output v1 as final.
- **If TOTAL ≥ 80 AND no single dim < 14:** proceed to Step 4 (revise).
- **If TOTAL < 80 OR any dim < 14:** the briefing was too sparse OR the framework choice was wrong. STOP and explicitly ask user for clarification on the weakest dim (do NOT silently produce a bad v2).

### Step 4 — REVISE → v2

Generate v2 addressing ONLY the specific issues identified in Step 2. Rules:

- Do NOT regenerate the whole pitch from scratch (preserves what worked)
- Apply targeted edits to the weak slides/sections
- If Specificity was weak: inject concrete numbers/names from briefing
- If Completeness was weak: fill the empty/thin sections with substance
- If Accuracy was weak: redo the math (TAM/SAM/SOM, valuation)
- If Tone was weak: rewrite the affected slides in the right register
- If Actionability was weak: tighten the ask + milestones

Output v2 with the same 12-slide structure. Mark: `### DRAFT v2 (revised)`.

### Step 5 — RE-SCORE v2 + OUTPUT FINAL

Run Step 2 critique against v2. Then pick:

- **If v2 TOTAL > v1 TOTAL:** output v2 as final
- **If v2 TOTAL ≤ v1 TOTAL:** revision didn't help — output v1 as final with note

**Final delivery format (this is what the user sees):**

```markdown
# Pitch Deck — [Venture / Client]

## Narrative Arc
[from final version]

## 12-Slide Outline
1. ...
2. ...
[etc]

## TAM / SAM / SOM
[from final version]

## Financial Ask
[from final version]

---

## Polish Metadata (transparency for the user)
- v1 score: X/100 (5-dim breakdown: S/A/C/A/T)
- v2 score: X/100 (5-dim breakdown: S/A/C/A/T)
- Final delivered: vN (reason: ...)
- Time invested: ~2-3× single-pass dario-pitch
- A/B baseline available via: `dario-pitch` skill on same briefing
```

---

## Why this works (and why it's not magic)

**What humans do in polish loops:**
1. Detect gaps ("slide 7 has no number")
2. Correct facts ("TAM math doesn't add up")
3. Reformulate ("slide 3 is fluffy, tighten")
4. Validate coherence ("ask doesn't match runway shown in slide 10")

**What this skill does:**
- Step 2 (critique) = detection + fact-check
- Step 4 (revise) = correction + reformulation
- Step 5 (re-score + best-of) = coherence validation

A single LLM pass can't do this because it commits the whole output in one shot. Two passes with explicit critique-then-revise structure mimics what humans do — empirically.

**What this skill does NOT do (limits):**
- Cannot add facts that aren't in the briefing or accessible via RAG (no hallucinated traction)
- Cannot exceed ~93-95 ceiling — there's still no human-in-loop validation
- Cannot replace deep client conversation (sparse briefing → mediocre output regardless)

---

## A/B Test Protocol (run this before propagating to other skills)

**Goal:** Determine if `dario-pitch-polished` lifts autonomous quality by ≥ +4pts vs `dario-pitch` baseline.

**Method:**

1. Use the 3 held-out briefings from sprint4 (`HELDOUT_PITCH` in `optimization/compile_sprint4.py`):
   - ZenStudio (chain yoga premium BR Series A)
   - ObraDigital (SaaS gestão construção BR pre-Series B)
   - TechBridge LatAm (marketplace freelancers tech seed)

2. For each briefing, generate output via:
   - `dario-pitch` (baseline — currently held-out mean 87.4 ± 1.74 from sprint4)
   - `dario-pitch-polished` (treatment)

3. Score both outputs using the same JUDGE rubric (Step 2 above).

4. Compute lift = mean(treatment) - mean(baseline).

**Decision:**

| Lift | Verdict | Next action |
|---|---|---|
| ≥ +4pts | Padrão A validated | Propagate wrapper to other 7 tier-A skills |
| +1 to +3.9pts | Marginal — needs more samples | Run on 5 additional production briefings before deciding |
| ≤ 0 | Padrão A fails on pitch | Investigate why (likely sparse briefings); try Padrão C (RAG-grounded) before giving up |

**Important:** A/B test results MUST be documented in `~/.claude/orchestrator/quality/padrao_a_ab_test_pitch.yaml` with full critique data per briefing, not just summary numbers.

---

## Integration with orchestrator

When dispatching, the orchestrator should:

```yaml
# In task definition:
- id: ATRIUM-PITCH-001
  title: "Pitch deck para HNW investor meeting"
  skill: dario-pitch-polished   # ← use polished variant
  execution_policy: client_facing
  ...
```

The orchestrator's existing dispatch logic already routes `client_facing` tasks through review gates. With this wrapper, the review gate becomes mostly a sanity check rather than a polish step.

---

## Red flags (do NOT do these)

- ❌ Skip the critique step ("looks good enough") — the loop only works if critique is honest
- ❌ Generate v2 without specific issues from v1 — you'll just regenerate similar quality
- ❌ Output v2 if it scored lower than v1 — best-of selection is mandatory
- ❌ Pretend score is higher than it is — overscoring breaks the gate logic
- ❌ Use this for sparse/vague briefings — output won't exceed v1 quality, just costs 2-3× tokens

---

<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **dario-pitch-polished** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** pitches mix verified traction (real ARR, real client count) with projections (Year 3 revenue, market share). The reader either over-trusts the projections (commits capital on a guess) or under-trusts the verified numbers (ignores real traction). Explicit labels restore signal.

**How to apply in dario-pitch-polished:**

1. After Step 5 (final output), scan every numeric claim in slides + TAM/SAM/SOM + financial ask.
2. Attach a label inline. If you can't pick a label confidently, the claim isn't ready to ship.
3. Critique step (Step 2) MUST verify Status Mix — if a pitch has 12 🟢 projections and 0 🔵 verifications, Specificity score drops to ≤12/20.

❌ **NOT delivery-ready:**

```
Tração: R$ 28M ARR, 47K alunos, NPS 76, recolocação 68%.
TAM R$ 32B EdTech BR, SAM R$ 8B profissional adulto.
M12: R$ 180M ARR.
```

✅ **Delivery-ready:**

```
Tração:
- R$ 28M ARR 🔵 verified (briefing client data, fechado 2026-03)
- 47K alunos em 12M 🔵 verified (briefing)
- NPS 76 🟡 assumed (precisa confirmação metodologia + n)
- Recolocação 68% 🟡 assumed (precisa definir "recolocação" + amostra)

TAM/SAM/SOM:
- TAM R$ 32B 🟡 assumed (cita ABED 2025; precisa link à fonte)
- SAM R$ 8B 🟢 projection (25% do TAM via filtro etário + renda)
- SOM R$ 480M 🟢 projection (250K alunos × R$ 1.9K AOV ano 2)

M12 projection R$ 180M ARR 🟢 projection (extrapolação linear taxa atual)

Status mix: 3 🔵 · 3 🟡 · 3 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed by client (or downgraded to 🟢)
- [ ] All 🔵 citations actually exist in briefing/RAG (no fabrication)
- [ ] All 🟢 projections labeled as such to investor (never as commitments)
<!-- gate7:end -->
