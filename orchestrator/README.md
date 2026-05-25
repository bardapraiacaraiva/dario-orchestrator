# DARIO Orchestrator v12.4.0

> **AI Consulting Accelerator** — 568 skill files across 32 squad themes, orchestrated by a Python engine with enforced quality gates.

[![Skills](https://img.shields.io/badge/skills-568_total_·_44_active-blue)](orchestrator/quality/INVENTORY.md)
[![Tests](https://img.shields.io/badge/tests-545_pass-green)](#testing)
[![Tag](https://img.shields.io/badge/release-v12.4.0_open_everything-brightgreen)](#release)
[![License](https://img.shields.io/badge/license-3_tiers-blue)](#license)

## What is DARIO?

DARIO is a **Python orchestrator + library of agent skills** for consulting-style AI work. Solo operator (or small team) uses it to run dispatches, score outputs, track budget/spend, and learn patterns across sessions.

**Honest inventory (per `quality/INVENTORY.md`):**
- **44 skills** (Tier C) actively dispatched via orchestrator (verified by `memory/episodes/*.yaml`)
- **8 polished wrappers** (Padrão A) with measured client-facing lift in A/B tests
- **524 skills** with SKILL.md never dispatched via orchestrator — many ARE used via Claude Code's native `Skill` tool directly (not instrumented), but the rest is library/cold-storage padding. See `INVENTORY.md` for caveats.

**Strategic framing (decided 2026-05-22):**
- Framing C: **consulting accelerator**, not gated SaaS product
- License = consulting/support tier signal, not code-gating (Risk #7 closed 2026-05-25, see RFC_STRATEGIC_DECISIONS.md)
- Trial repo (`origin`) and VIP repo (`full`) ship IDENTICAL code

**Engineering hygiene:**
- 545 tests pass in ~45s · pre-push hook gating · CI on GitHub Actions
- Real Python enforcement layer (`orchestrator/enforcement/`) — budget gate + dispatch validator + cross-process parallelism guard
- Weekly automated backup (`scripts/backup_weekly.sh` + Windows Task Scheduler)
- Honest metrics: `delivery_ready_rate` first-class (not vanity mean scores)

## Live Demo

```
Health:     http://31.97.53.231:8422/health
Dashboard:  http://31.97.53.231:8422/cfo
API:        http://31.97.53.231:8422/core/status
```

(Endpoints may be intermittent — VPS is shared with other client projects, see automation-solution-ai LP at :9090.)

## Skill domains (themes — counts are SKILL.md files on disk, NOT all production-validated)

| Domain | Skills | What it does |
|--------|--------|-------------|
| **CFO & Finance** | 46 | Virtual CFO with PT tax compliance (IVA, IRC, SAF-T, ATCUD) |
| **Marketing & Growth** | 49 | Brand → Offer → Funnel → Ads → Content → Email |
| **Builder (NEW)** | 32 | **Idea to deployed product** — design system, React, API, DB, deploy |
| **SEO** | 16 | Technical + Content + Local + AI Search optimization |
| **Architecture & Design** | 31 | Briefing → Budget → Timeline → Licensing (PT regulations) |
| **Events** | 28 | Venue → Catering → AV → Protocol → Compliance |
| **HR** | 12 | Recruitment → Performance → Engagement → PT labor law |
| **Risk & Compliance** | 14 | RGPD, AML, ISO 27001, ESG, whistleblowing |
| **Administration** | 15 | Docs, meetings, procurement, facilities |
| **Business Acceleration** | 13 | Niche validation → Offer → Launch → Scale |
| **IT Infrastructure** | 12 | Docker, CI/CD, monitoring, security, DR |
| **Supply Chain** | 8 | Procurement, inventory, logistics, warehouse |
| **Customer Success** | 10 | Onboarding, health scoring, churn recovery |
| **Product** | 3 | PRDs, user stories, sprint planning |
| **Technical Ops** | 7 | WordPress, WooCommerce, CWV, security audits |
| **Content & Social** | 2 | Editorial calendars, social media management |
| **PR** | 1 | Press releases, crisis communication |

## Builder Module — Idea to Product

The Builder VP (`B.U.I.L.D.E.R.`) can take any idea and produce a deployed product:

```
PRD → MVP Scope → Tech Stack → Brand Identity → Wireframe
→ Design System → Architecture → Database Schema → API Design
→ Auth System → React Components → Forms → Landing Page
→ Animated UI → SVG Icons → Analytics → Docker → CI/CD
→ Vercel/Coolify/SST Deploy → Launch Checklist
```

**32 builder skills. 100% of the idea-to-product lifecycle.**

## Orchestrator Engine

- **66 Python engines** covering execution, intelligence, quality, state, observability, security, financial
- **259 self-tests** (100% pass rate)
- **168 Agent Cards** (A2A protocol)
- **Knowledge Graph** (98 entities, 133 relations)
- **VMAO Wave Scheduler** (critical-path DAG optimization)
- **Q-Value Memory** (RL-based strategy selection)
- **OWASP 10/10** security coverage

## Unique Differentiators

1. **Self-aware financials** — knows its own token cost per client/project
2. **Portuguese compliance native** — IVA, IRC, SNC, ATCUD, SAF-T, NIF validation
3. **Self-evolving** — Q-value memory + benchmark evolution + synaptic weights
4. **Three-tier security** — Anthropic Financial Services pattern for data handling
5. **Idea to product** — 32 builder skills from PRD to deployed app

## Trial Access (7 days)

This public repository contains the orchestrator core. Full access with all 269 skills, VIP support, and custom deployment:

**Contact:** barda@automationsolutionai.com

## Architecture

```
dario-ceo (CEO)
├── dario-cfo (VP Finance) — 43 workers
├── builder-vp (VP Product Build) — 32 workers
├── diva-vp (VP Architecture) — 20 workers
├── lucas-vp (VP Operations) — 16 workers
├── a360-vp (VP Acceleration) — 8 workers
├── atlas-vp (VP Events) — 27 workers
├── dir-marketing — 12 workers
├── dir-seo — 16 workers
├── dir-technical — 7 workers
└── ... (17 domains total)
```

## License

**Proprietary — All Rights Reserved.** See [LICENSE](LICENSE) for full terms.

Summary:
  - **7-day Evaluation License** is automatically granted on first `--init-trial`.
  - **Commercial License** is granted upon purchase of a valid key (see `license_manager.py` TIERS dict for the 59 tiers + 5 Onda 12 bundles).
  - **Prohibited under both licenses:** redistribution, derivative works, white-label rebranding, reverse engineering of license enforcement, sublicensing, building competing products that reuse the architecture, skill catalog, or pricing model.

Possession of this code does NOT grant any rights beyond the explicit terms in `LICENSE`. Reading the source for evaluation is allowed; copying it into another project is not.

For commercial licensing, partnerships, or authorization to redistribute: **barda@automationsolutionai.com**

---

Built with Claude Code. Powered by Anthropic Claude Opus 4.6.
