# RFC — Strategic Decisions Required (audit risks #1, #4, #7, #10)

**Status:** Decision RFC (open — needs user input, not auto-executable)
**Created:** 2026-05-24
**Why combined:** These 4 risks share root: **what is DARIO as a product?**
A coherent answer cascades to all four. Deciding them one-by-one leads
to inconsistency.

---

## The unified question

Is DARIO:

- **(A) An open-source prompt library + helpers** that barda uses personally
  and shares freely (or via consulting hours)?
- **(B) A proprietary product** sold as license-protected install, with
  ongoing maintenance + support model?
- **(C) A consulting accelerator** — barda enters client companies via
  Automation Solution AI, installs DARIO white-label, lives there, shares
  in results?

The current state is **all three at once**, which is why all four risks
exist:
- License complexity (B implies real anti-piracy; A/C don't need it)
- VIP stubs (B implies hiding crown jewels; A/C don't)
- "Orchestrator = markdown" (A/C are fine with this; B promises more)
- LLM version drift (B implies SLA on Claude version; A/C don't)

---

## Risk #4 — License complexity (€?? engineering investment)

### Current state
- 3-layer fingerprint (orch dir + home obfuscated + Windows registry)
- FastAPI license server with HMAC tokens + anti-snapshot rollback
- Cython binary obfuscation + code signing
- Cert pinning RFC 7469
- 5 Enterprise bundle tiers (R$ 297/997/2997/...)
- 17+ license tests
- CI pipeline for Linux gcc + Windows MSVC Cython builds

### Cost incurred (from memory log)
- License Onda 8 → 9 → 10 → 12 = at least 4 sprints
- Memory mentions "339 fast tests verde", "447 tests verde" — large fraction
  is licensing infrastructure
- Each Anthropic SDK version upgrade requires Cython rebuild + cert validation

### Decision matrix

| Option | Effort to maintain | Defends against | Aligned with |
|---|---|---|---|
| **Keep all** | 20+ h/quarter | Determined attacker | (B) proprietary product |
| **Simplify to token + server check** | 2 h/quarter | Casual unauthorized use | All three (A/B/C) |
| **Drop entirely** | 0 h/quarter | Nothing | (A) open source OR (C) consulting |

### Recommendation
**Simplify**. Even if final answer is B (proprietary), Cython obfuscation
doesn't defend against the real attacker (anyone with `pyc-decompile` + 30min
breaks it). Effort is better spent on product quality + support SLA.

Concrete first step: archive `license-build.yml` CI workflow (saves CI compute);
keep license server + token validation (cheap signal); delete Cython pipeline
+ cert pinning code in 30-day window after no incidents.

**User decision needed:** which option (Keep / Simplify / Drop)?

---

## Risk #7 — VIP stubs as product strategy ✅ RESOLVED 2026-05-25

**Decision:** Open everything. Restored 6,057 LOC across 13 modules + 21
files in upgrades/ package from commit 5bba778. Both origin (trial) and
full (VIP) now ship identical, working implementations. The "VIP-only"
ImportError theater is gone. `vip_only` test marker deprecated. pre-push
hook no longer tolerates collection errors.

Aligned with framing C (consulting accelerator): value is in the
installation/curation/workflow, not in withholding Python files. Buyers
of "DARIO Install" (R$ 997) get the working system, not a partial one.

Test surface: 449 → 545 (+96 tests now run). 0 collection errors.

### Historical analysis (kept for context)

### Current state
```python
# dispatch_engine.py, dispatch_cot.py, semantic_dispatch.py — REMOVED
raise ImportError(
    f"{_MODULE_NAME!r} is a VIP-only module. "
    "Buy a Professional or Enterprise license..."
)
```

### What this implies
- Two repos: public (trial, with stubs) + private (full, with real implementation)
- Documentation must describe behavior that the public repo can't run
- Tests for VIP modules can't exist in public repo (correctly marked `vip_only`)
- Onboarding: trial users get a partial product that "works" but missing intelligence layer

### Honest assessment
The "intelligence" hidden behind stubs (semantic_dispatch, dispatch_cot) is —
based on observable behavior — **probably also markdown-prompt-driven**. So
the stub is hiding... more prompts. Not actual proprietary algorithms.

### Decision matrix

| Option | Implication | Reality |
|---|---|---|
| **Keep stubs** | "Proprietary" framing — pay to unlock | Hides that "intelligence" is more prompts |
| **Open everything** | Show the real architecture — markdown + Python helpers | Strips the moat illusion; honest |
| **Move intelligence server-side** | Truly hidden — public uses HTTP API | Requires real backend; bigger investment |

### Recommendation
**Open everything**. The current "VIP stub" model is least-of-both-worlds:
- Trial users get a broken experience
- Paid users get... the same prompts, just imported

If the moat is real, prove it via server-side execution. If it's prompts,
own that — the value is in the *curation* and *workflow design*, which open
source doesn't strip.

**User decision needed:** Keep stubs / Open everything / Move server-side?

---

## Risk #1 — Orchestrator = markdown

### Current state
- `dario-orchestrator/SKILL.md` is ~1000 lines of instructions Claude reads
- `company.yaml` is data that Claude is **expected** to honor (e.g. max 3
  parallel workers, atomic checkout)
- Real Python `dispatch_engine.py` is a VIP stub (see Risk #7)
- The audit tests I added verify config consistency, not execution behavior

### Why this is risky
- Behavior depends on which Claude model interprets the markdown
- Invariants ("max 3 parallel") have no Python enforcement
- "Add new client" workflow depends on me remembering the steps from SKILL.md

### Decision matrix

| Option | Investment | Result |
|---|---|---|
| **Accept it** | None | Document honestly: "DARIO is a prompt library, Claude is the runtime" |
| **Thin enforcement layer** | ~16 h | Python wrapper validates company.yaml + enforces hard limits before each dispatch decision (parallelism, budget gate, validator) |
| **Full Python orchestrator** | ~6 weeks | Real dispatcher with state machine, deterministic execution, true behavior tests |

### Recommendation
**Thin enforcement layer**. Honest middle ground. Doesn't pretend full
orchestrator exists, but adds real safety rails:
- A `dispatch_validator.py` that checks every task dispatch against company.yaml
  rules and rejects violations
- A `parallelism_guard.py` that enforces max 3 concurrent (process-level lock)
- Behavior tests that exercise these rails

Full Python orchestrator (Temporal/Dagster style) is overkill until you have
multiple developers needing determinism guarantees.

**User decision needed:** Accept / Thin layer / Full rewrite?

---

## Risk #10 — LLM version drift

### Current state
- All Padrão A wrappers depend on Claude's interpretation of markdown
- No version pinning in skill files (no "tested with Opus 4.7" stamps)
- Memory mentions "DARIO Opus 4.7 (1M context)" but skills don't assert this
- If Anthropic deprecates Opus 4.7, behavior drifts silently

### Decision matrix

| Option | Investment | Defends against |
|---|---|---|
| **Ignore** | 0 | Nothing — drift will be silent |
| **Version stamp + warn** | 2 h | Drift visibility (alert when model differs) |
| **Pin via API exclusively** | ~1 week | Deterministic version (paid model lock) |
| **Cross-model regression tests** | ~2 weeks | Catch drift before user sees it |

### Recommendation
**Version stamp + warn** as first step. Cheap, catches drift.

Concrete:
- Each polished wrapper SKILL.md gets `tested_with_model: claude-opus-4-7` frontmatter
- A pre-dispatch check that reads current model + compares to declared
- Mismatch = WARNING in dashboard + audit log (not block — too aggressive
  for now)

Cross-model regression tests are Phase 2, when polished wrapper population
is stable.

**User decision needed:** Ignore / Version stamp / API pin / Regression tests?

---

## Recommended unified strategy

Pick ONE of the three product framings (A/B/C) above. The four risk
decisions follow:

### If (A) Open source

- Risk #4: **Drop license** (delete Cython pipeline + license server)
- Risk #7: **Open all stubs** (remove `dispatch_engine.py` stub, ship empty/honest module)
- Risk #1: **Accept markdown-as-orchestrator** (document honestly)
- Risk #10: **Version stamp + warn** (cheap discipline)
- License: MIT/Apache; consulting hours = your monetization

### If (B) Proprietary product

- Risk #4: **Simplify license** to token + server (drop Cython); invest saved
  cycles in product quality
- Risk #7: **Move intelligence server-side** (real moat = your service, not
  obfuscated bytecode)
- Risk #1: **Thin enforcement layer** (deterministic safety rails matter for SLA)
- Risk #10: **Cross-model regression tests** (paying customers expect predictable behavior)
- License: SaaS subscription; SLA + support contract

### If (C) Consulting accelerator (current Automation Solution AI direction)

- Risk #4: **Drop license** (you give it to each client; no piracy concern)
- Risk #7: **Open everything** to the client (they need to understand what they bought)
- Risk #1: **Thin enforcement layer** (clients want reliability)
- Risk #10: **Version stamp + warn** (each client install is independent)
- License: Per-engagement contract; participate-in-results model

---

## Honest meta-observation

Current state is closest to (C) but with (B) instrumentation. The (B)
instrumentation (license complexity, VIP stubs) is **friction against (C)
execution**. Each Automation Solution AI client install requires:
- License generation
- Cython binary distribution
- VIP repo access setup
- ...all for a client who **needs you in-house anyway**.

Drop the (B) layer + commit to (C) cleanly. If a future client wants
SaaS hosting, build that *for them* server-side; don't pre-build it.

---

## Process for closing this RFC

This RFC stays open until you (barda) reply with:

1. Product framing chosen (A / B / C / "other")
2. Risk #4 decision
3. Risk #7 decision
4. Risk #1 decision
5. Risk #10 decision

I will then execute the chosen path one risk at a time, validate, commit.

No auto-execution before your decision. These cuts are too consequential
to be made on my own initiative.
