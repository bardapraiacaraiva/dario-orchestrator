# RFC — Multi-Tenant: When and How DARIO Scales Beyond One User

**Status:** Decision RFC (open for objection until a real trigger fires)
**Author:** barda + Claude Opus 4.7
**Created:** 2026-05-24
**Decision needed by:** When trigger conditions in §6 fire (not before)

---

## 1. Problem statement

DARIO was built for a single user (barda). The Automation Solution AI
business model — "entra na empresa, implementa DARIO, gere area, participa
nos resultados" — implies DARIO will eventually run for multiple distinct
clients/companies. Each client has:

- Their own projects (memory should not leak between them)
- Their own budget (their spend, audited separately)
- Their own deliverables (their Obsidian vault, not barda's)
- Their own compliance requirements (LGPD, audit trail per tenant)

Today, DARIO has:

- 1 memory dir (`~/.claude/projects/C--Users-barda/memory/`)
- 1 budget tracker (`orchestrator/budgets/YYYY-MM.yaml`)
- 1 RAG corpus (`localhost:8420`, shared across all queries)
- 1 audit log (`orchestrator/audit/YYYY-MM-DD.yaml`)
- 1 license per machine

**The question:** when does this single-user shape become an actual blocker,
and what should we do about it before it does?

---

## 2. Audit — where single-user assumptions actually live

Grep'd 2026-05-24. Most code uses `Path.home()` which is per-machine
parameterized (good). Hard-codes that need parameterization:

| Location | Hard-code | Severity |
|---|---|---|
| `runners/autodiag.py:58` | `"C--Users-barda"` in `MEMORY_DIR` 🔵 verified | LOW — 1 line, defaults from `Path.home()` works on any machine for same-user installs |
| `scripts/closeout_wave.py:27-47` | `"C:/Users/barda/OneDrive/.../D.A.R.I.O/..."` Obsidian paths 🔵 verified | LOW — that script is a one-off Cuidaí closeout, no longer needs maintaining |
| `config/project_types.yaml` | `owner: barda` field on every entry 🔵 verified | NONE — descriptive metadata, not load-bearing |
| Skills + orchestrator code | Mostly `Path.home()` ✓ 🔵 verified | Per-install state isolation works out of the box on a fresh user account |

**Shared things that SHOULD remain shared (these are the product, not state):**
- `~/.claude/skills/` — 584 skills, the actual product
- `~/.claude/orchestrator/` Python code + tests
- `~/.claude/orchestrator/config/company/*.yaml` — squad/worker definitions
- `~/.claude/orchestrator/PADRAO_A_AB_TEST_RESULTS.md` — documentation
- `~/.claude/orchestrator/CONVENTIONS.md` — conventions

**Per-tenant things that MUST be isolated:**
- Memory dir
- Budget yaml
- Audit logs
- Tasks (active/done/blocked)
- Quality runtime state (polished_production_runs, skill-metrics, etc.)
- API spend log (`api_spend_log.yaml`)
- License key
- RAG corpus (probably — depends on whether clients want their docs cross-indexed)

---

## 3. Three architectural paths

### Path A — Multi-Tenant SaaS (full)

Single hosted DARIO instance. Database backend (Postgres) replaces yaml files.
HTTP API + tenant auth. Each client gets login + isolated data.

**Effort:** 🟢 projection 6+ months of focused work
**Pros:** central observability, single update path, scales horizontally
**Cons:** massive refactor, security surface (auth/authz/leakage), maintenance
overhead, requires SRE skill set barda doesn't have

**Already rejected** 2026-05-22 via [[project_dario_saas]] archive
("Vapor 17d. Não voltar como SaaS multi-tenant"). RFC respects that decision —
re-opening only if §6 trigger A fires.

### Path B — Per-Tenant Install (white-label) ★ ALIGNED WITH PRIOR DECISION

Each client gets their own DARIO install on their own infrastructure
(VPS or workstation). Codebase shared via git (orchestrator + skills repo).
State dirs live in their `~/.claude/` (or equivalent).

**Effort:** 🟢 projection ~10h pre-work + per-install setup time when
client #1 onboards
**Pros:** ~zero arch change (current code mostly already works this way),
data lives on client's hardware (security simple — no cross-tenant leak
possible), aligned with already-archived DARIO SaaS pivot decision
**Cons:** N installs to update when DARIO ships features (mitigated by
`npx ... installer` which already exists), no central observability
across tenants (acceptable — barda manages each client engagement individually
under Automation Solution AI model)

### Path C — Hybrid (Shared skills, per-tenant state-dir override)

Shared codebase + skills via git. Each tenant runs same DARIO binary but
points `DARIO_STATE_ROOT` env var at their own state dir
(`/srv/dario-state/cuidai/` vs `/srv/dario-state/saquei/`).

**Effort:** 🟢 projection ~20h (parameterize all state paths, add env
var resolution, test isolation)
**Pros:** can run multiple tenants on same VPS, single codebase to update
**Cons:** still requires careful path discipline (one rogue `Path.home()`
breaks isolation), license model unclear (per-tenant or per-VPS?), middle
ground that may serve neither extreme well

---

## 4. Recommendation

**Path B (per-tenant install)** because:

1. It's what the DARIO SaaS archive decision (2026-05-22) already chose
   ("white-label install caso-a-caso, não SaaS multi-tenant"). Re-deciding
   adds nothing.
2. Audit (§2) shows current code is already 90% there. Only 1 hardcoded
   path needs parameterization.
3. Aligns with Automation Solution AI's actual business model — barda
   enters each company and OPERATES with them. Centralized SaaS doesn't
   match that engagement style.
4. Security is simple by construction: client's data on client's hardware.
   No multi-tenant auth/authz bugs possible.
5. Reversible: if a future client demands central hosting, Path C can be
   built on top of Path B's parameterization work.

---

## 5. Pre-work to do NOW (cheap, low-risk)

These are improvements that pay off regardless of Path A/B/C and are cheap
enough not to need a trigger:

| # | Task | Effort | Why now |
|---|---|---|---|
| PW-1 | Fix `runners/autodiag.py:58` — replace `"C--Users-barda"` with logic that resolves user dir from `Path.home()` parts | 🟢 projection ~30min | Removes the 1 user-specific hard-code in runtime code. Pure hygiene. |
| PW-2 | Add `DARIO_OBSIDIAN_VAULT` env var read in skill that saves to Obsidian; default to current barda path | 🟢 projection ~1h | Future installs can point at their own vault without editing skill files. |
| PW-3 | Delete `scripts/closeout_wave.py` — it's a Cuidaí-specific one-off | 🟢 projection ~5min | Removes 1 source of hardcoded barda paths + dead code. |
| PW-4 | Document in CONVENTIONS.md: "every new path reference must use `Path.home()` or env var, never hardcode `barda` or `C--Users-barda`" | 🟢 projection ~10min | Test guard already catches the routing tests. Add a path-discipline test that greps for forbidden patterns. |

**Total pre-work:** ~2h, no architecture change, no trigger required.

---

## 6. Trigger conditions for Path B activation

DO NOT start Path B onboarding work until ONE of these fires:

- 🔴 **Trigger 1:** First Automation Solution AI client contract signed for
  a DARIO install (not "interested" — signed)
- 🔴 **Trigger 2:** Atrium / Cuidaí / SAQUEI founder requests a private
  DARIO install for their own use (not third-party)
- 🟡 **Trigger 3:** Audit findings: pre-push hook + tests catch a
  cross-tenant leak in barda's own multi-project use (memory of client A
  visible to skills serving client B) — would force isolation as bug fix

If 🔴 trigger fires:
1. Run PW-1 to PW-4 if not already done (~2h)
2. Run `npx github:bardapraiacaraiva/dario-orchestrator-installer` on
   the client's machine
3. Configure their env vars (Obsidian vault, license key)
4. Walk them through `/dario-onboarding` for the 5-min tour
5. **No code changes to DARIO itself** — install is parameterized via
   env vars + Path.home()

Estimated time to onboard first client (when trigger fires): **half a day**
(not 6 months).

---

## 7. Re-evaluation triggers for Path A (full SaaS)

Path A is killed for now. Re-open ONLY if:

- 🔴 5+ clients want DARIO simultaneously and barda can't visit each — but
  business model says barda DOES go in person, so this contradicts the
  thesis
- 🔴 A client demands centralized observability across multiple internal
  departments (would justify Path C, not full A)
- 🔴 The Automation Solution AI business model itself changes from
  "consultoria + DARIO" to "DARIO as SaaS"

These are improbable enough that Path A is effectively shelved indefinitely.

---

## 8. What NOT to do (anti-patterns to call out)

- ❌ Start refactoring the orchestrator for multi-tenancy "just in case"
  before a trigger fires — wastes ~6 months that could go to current
  client work
- ❌ Add user/tenant fields to every yaml schema "for future-proofing" —
  pollutes schemas with unused fields
- ❌ Build an admin panel for managing tenants — Path B by design has no
  central admin; each client manages their own install
- ❌ Add Postgres backend — Path B works with yaml; Postgres only matters
  if Path A is chosen
- ❌ Defer PW-1 to PW-4 — they're cheap and provide value regardless

---

## 9. Status mix

- Hardcoded path audit: 🔵 verified (grep of orchestrator/ runtime code)
- Path B alignment with prior archive decision: 🔵 verified (project_dario_saas memory)
- Effort estimates for Paths A/B/C: 🟢 projection (no benchmark from comparable refactors)
- Trigger conditions: 🟡 assumed (no real client signed yet to validate)
- Half-day onboarding estimate: 🟢 projection (assumes installer works smoothly on fresh machine; not tested with non-barda user)

**Status mix: 2 🔵 · 1 🟡 · 2 🟢**

---

## 10. Decision

**Adopted: Path B with PW-1 to PW-4 as pre-work.** Path A and Path C
shelved unless §6 / §7 triggers fire.

This RFC is **closed for decision** but **open for re-evaluation** when
any trigger fires. Re-open by editing this file with a `## 11. Re-evaluation YYYY-MM-DD` section.

---

## 11. Pre-work execution log

- [x] **PW-1** (2026-05-24): `runners/autodiag.py:58` MEMORY_DIR now
      auto-resolves via `_resolve_memory_dir()` — walks
      `~/.claude/projects/*/memory/` and picks the first existing dir.
      Override available via `DARIO_MEMORY_DIR` env var. Legacy barda
      fallback preserved for backward compat. Smoke test: autodiag
      memory_staleness check still runs correctly.
- [ ] **PW-2**: `DARIO_OBSIDIAN_VAULT` env var — deferred (skill files
      need careful surgery to not break existing behavior, leave for
      when first non-barda install happens).
- [x] **PW-3** (2026-05-24): `scripts/closeout_wave.py` deleted —
      Cuidaí-specific one-off, no longer needed.
- [x] **PW-4** (2026-05-24): CONVENTIONS.md updated with Path discipline
      rule + `tests/test_no_hardcoded_user_paths.py` enforces via grep
      pattern check across orchestrator/ Python+YAML. Pre-push hook
      gates. 2 tests pass.

---

## Related

- `project_dario_saas` memory (2026-05-22 archive decision)
- `feedback_product_pivot_decisions` (KILL/DORMANT/PURSUE filter — Path A is KILLED)
- `project_automation_solution_ai` (business model context)
- `~/.claude/orchestrator/CONVENTIONS.md` (path discipline lives here after PW-4)
