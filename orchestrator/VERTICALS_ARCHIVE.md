# Vertical squads — archive log & revival guide

Industry squads built speculatively (v11.4/v11.5/v12) with **zero usage**
(no score, no dispatched task, no chain) targeting verticals the agency does
not serve. Moved out of `~/.claude/skills/` on 2026-06-01 so they stop polluting
semantic routing (the WordPress→medik misroute class) and inflating the skill
surface. **Archive, not product** — per "use, não vender" + the KILLED
multi-tenant SaaS decision. No second orchestrator, no vertical-SaaS.

> NOTE: the physical files live in `~/.claude/skills-archive/verticals/<segment>/`
> on this machine, but that path is **gitignored**, so the repo records only
> their removal from `skills/`. They remain fully recoverable from git history.

## Phase 1 (2026-06-01) — 8 squads, 133 skills

| Segment | Squad | Skills | Domain |
|---|---|---|---|
| saude | medik | 15 | healthcare BR (ANVISA, CFM, TUSS, telemedicine) |
| imobiliario | kirion | 15 | real estate (REIT, DCF, mortgage, Golden Visa PT) |
| energia | helios | 15 | energy (ANEEL, PPA, microgrid, carbon credits) |
| esg | gaia | 15 | ESG/CSRD (GRI, SASB, SBTi) |
| educacao | campus | 15 | education (LMS, BNCC, MEC) |
| eventos | atlas (events) | 28 | event management (venue, catering, seating…) |
| vendas-enterprise | mercurius | 15 | enterprise sales |
| marketing-massa | euterpe | 15 | mass marketing (programmatic, MMM) |

KEPT ACTIVE: `atlas-fin-*` (15 fintech skills — PIX/open-banking-BR/KYC) —
relevant to BR SaaS clients (SAQUEI/Tributário/ARRECADA), not events.

## Revive a segment (demand-pulled — when a real client appears)

```bash
# 1a. If skills-archive/ still has the files (this machine):
git -C ~/.claude mv skills-archive/verticals/saude/medik-* skills/
# 1b. Or restore from git history (any clone):
#     git -C ~/.claude checkout <commit-before-e22b020>^ -- skills/medik-<name>
# 2. Re-add to the semantic index (Ollama must be running):
cd ~/.claude/orchestrator && .venv/Scripts/python.exe -m dispatch.semantic_dispatch --bootstrap
# 3. company.yaml worker entries for archived squads were left as harmless
#    no-ops, so dispatch routing works again immediately.
```

## Routing impact (verified Phase 1)
- "auditoria WordPress segurança" → seo-audit (was medik-health-insurance-operations)
- semantic index 570 → 437 embeddings
- company.yaml: dead worker entries left as no-ops (never selected post-prune); cleanup deferred

## Future phases (not yet archived)
Zero-use, later phases: aegis, sphinx, orion, oraculo, zenith, demeter, adriana,
risco, pessoa, nexus, suply, obsidian.
Discuss-first (may map to client SaaS): conta (→LUSOconta), lex/nomos
(→Tributário/SAQUEI), atlas-fin (→BR fintech), client (agency lifecycle).
