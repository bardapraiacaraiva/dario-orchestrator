---
name: dario-diagnose
description: DARIO's universal diagnostic workflow — holistic analysis, priority triage (CRÍTICO/IMPORTANTE/OTIMIZAÇÃO), and 4-milestone roadmap. Entry point for any new client request or project audit. Triggers on "diagnose", "audit", "analisa", "avalia", "plano", "onde começar", "roadmap".
license: MIT
---

# DARIO Skill — Diagnose

The universal entry point. Any new substantive request from the user runs through this skill first to produce a structured diagnosis before any specialized work kicks in.

## When to activate

Invoke `/dario-diagnose` (or trigger automatically) when:
- User brings a new client/project and asks where to start
- User requests an audit of a site, product, or funnel
- User shares symptoms without a clear solution ("está a converter mal", "perdi posições", "quero escalar")
- User wants a roadmap for an ambitious transformation
- Start of any `dario-client-onboard` orchestrator flow

Do NOT use when:
- The request is a specific tactical task (use the specific skill or agent)
- The user already provided a clear spec to execute

## Workflow

### 1. Context gathering
Ask (or infer from input) the minimum viable context:
- **Who** is the client (industry, size, target market)
- **What** is the current state (URL, stack, metrics baseline if any)
- **Why now** (what triggered the request)
- **Constraints** (budget, timeline, team, legal)
- **Success criteria** (what would "done well" look like)

If critical context is missing, stop and ask — don't assume.

### 2. RAG consult (mandatory)
```
mcp__dario-rag__search_kb(query: "<sector> <stack> audit priorities", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "<main challenge keywords>", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "<client project name if mentioned>", limit: 5)
```
Search in all collections (omit collection) if client-specific context may exist in obsidian vault.

### 3. Holistic analysis — Phase 1 of DARIO model
Cover ALL dimensions, even if briefly:
- **Technical:** stack, performance, security, infrastructure, code health
- **SEO:** crawlability, indexation, content depth, schema, Core Web Vitals, E-E-A-T
- **Conversion (CRO):** funnel, CTAs, friction, trust signals, social proof
- **Content:** relevance, quality, AI-readiness, audience match
- **Business:** ROI, KPIs, market position, competition
- **Legal/Compliance:** RGPD, cookies, accessibility (EAA), sectorial
- **Brand:** positioning, consistency, narrative

### 4. Identify applicable specializations + squads
Explicitly name them (transparency protocol):
- "Ativando #2 (WordPress) + #3 (Advanced SEO) + PT Legal spec + Brand Squad"
- Cite RAG sources consulted

### 5. Prioritization — Phase 2
Classify every finding into exactly one bucket:
- **🔴 CRÍTICO** — Blocks launch / risks legal / high-impact revenue leak
- **🟡 IMPORTANTE** — Measurable impact, 1-4 weeks to fix
- **🟢 OTIMIZAÇÃO** — Long-term compounding gains

Use quick-wins-first ordering within each tier.

### 6. Roadmap — Phase 3 (4 milestones)
| Milestone | Weeks | Focus |
|---|---|---|
| **M1 — Foundation** | 1-2 | Setup, baseline metrics, TIER 0 blockers |
| **M2 — Core Fixes** | 3-4 | CRÍTICO bucket closed, core integrations |
| **M3 — Optimization** | 5-6 | IMPORTANTE bucket + performance |
| **M4 — Launch + Monitor** | 7-8 | Deploy, alerts, KPI dashboard |

Customize weeks to client scope but keep the 4-stage cadence.

### 7. Confidence declaration
State explicitly:
- 🟢 Alta confiança (80-100%): direct recommendation
- 🟡 Exploração (50-79%): present 2-3 alternatives
- 🔴 Incerteza (<50%): ask questions first

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: diagnostic
dario_specializations: [list]
dario_squads: [list]
confidence: <green|yellow|red>
---

# Diagnóstico DARIO — <Client Name>

## Resumo Executivo
- **Problema identificado:** <1-2 lines>
- **Solução proposta:** <1-2 lines>
- **Impacto esperado:** <metric + timeframe>

## Análise Holística
### Técnico
### SEO
### Conversão
### Conteúdo
### Legal / Compliance
### Brand

## Priorização
### 🔴 CRÍTICO (bloqueia launch / risco legal)
1. ...
### 🟡 IMPORTANTE
1. ...
### 🟢 OTIMIZAÇÃO
1. ...

## Roadmap
### M1 — Foundation (Sem 1-2)
### M2 — Core Fixes (Sem 3-4)
### M3 — Optimization (Sem 5-6)
### M4 — Launch + Monitor (Sem 7-8)

## Métricas de Sucesso
| KPI | Baseline | Target | Deadline |
|---|---|---|---|

## Próximos Passos
- [ ] <immediate action 1>
- [ ] <immediate action 2>

## Questões Pendentes
- <things you need from the user/client>
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Diagnóstico DARIO.md`

## Red flags — don't do this
- Never skip RAG consult (even if you think you know)
- Never produce a roadmap without prioritization tiers
- Never hide confidence level
- Never recommend without checking PT Legal spec for PT clients
- Never forget to check EAA accessibility spec for any EU consumer site
