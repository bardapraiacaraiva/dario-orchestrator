---
name: prometheus-director
description: PROMETHEUS squad orchestrator — external knowledge & evolution sensors. Use when user wants to scan the outside world for relevant updates (new skill releases, MCP servers, papers, regulatory changes, deprecations). Triggers em "scan mundo", "prometheus", "novidades semana", "weekly digest", "novidades repos", "novidades MCP", "novidades regulatorias", "atualizar dario".
license: SEE-LICENSE
parent_agent: prometheus-director
compliance: [audit_immutable, responsible_disclosure]
category: "Meta — External Evolution"
version: "1.0"
autonomy_tier: 0
---

# PROMETHEUS-DIRECTOR

Squad meta de **vigilância externa**. Inspirado em Prometheus (mitologia: trouxe o fogo dos deuses para os humanos).

Diferenciação dos outros squads:
- `dream` subsystem = consolida o que aconteceu DENTRO (internal)
- `ORACULO` squad = research académico/papers em depth (specialized)
- **PROMETHEUS** = sweeps o mundo EXTERNO em breadth + flags o que merece atenção

**Wave 1 = passive monitoring only.** Nenhuma das skills altera ficheiros. Apenas observa + reporta.

## 4 sensores

| Sensor | Frequência | Output |
|---|---|---|
| `prometheus-repo-scanner` | semanal Dom 22h | `prometheus/digests/YYYY-WW-repos.md` |
| `prometheus-mcp-discovery` | semanal Dom 22h15 | `prometheus/digests/YYYY-WW-mcp.md` |
| `prometheus-paper-tracker` | semanal Dom 22h30 | `prometheus/digests/YYYY-WW-papers.md` |
| `prometheus-regulatory-watch` | semanal Sex 18h | `prometheus/digests/YYYY-WW-regulatory.md` |

## Workflow do director

**Modo A — Marker-driven (cron-collected data já disponível):**

Antes de tudo, verificar `~/.claude/orchestrator/prometheus/state/_pending_digest.json`.
Se existe:
1. Ler o marker JSON
2. Ler os 4 raw files: `_repo_findings_raw.json`, `_mcp_findings_raw.json`, `_paper_findings_raw.json`, `_regulatory_findings_raw.json`
3. Para cada raw, aplicar signal filter (3 perguntas) e produzir narrative digest em `digests/YYYY-WW-{sensor}.md`
4. Compilar master `digests/YYYY-WW-master.md` com TOP 5 actionable
5. **Apagar** `_pending_digest.json` (marker consumed)
6. **Apagar** os 4 raw files
7. Update state files (`last_run.yaml`, `last_seen_releases.yaml`, etc.) com dados consolidados

**Modo B — Manual invocation (sem cron, user pediu):**

1. Verificar `last_run.yaml` — `>= 7 dias desde último weekly`?
2. Se sim: invocar os 4 sensores manualmente (via Skill tool calling cada um)
3. Compilar master digest
4. Mesma signal filter + output

**Em ambos os modos:**

- Apenas escrita em `digests/*.md` e `state/*.yaml`
- NO auto-action sobre skills, configs, ou anything else
- User decide se implementa findings

## Signal filter (90% noise reduction)

Para qualquer finding entrar no digest, tem que passar 3 perguntas:

1. **Aplicabilidade:** afecta diretamente um dos 32 squads ou 536 skills actuais? Se não → discard.
2. **Materialidade:** delta vs estado actual é >10% improvement OU resolve gap conhecido OU é regulatory mandatory? Se não → noted but not flagged.
3. **Risco de não-adoção:** se ignorarmos isto 6 meses, perdemos competitive edge OU compliance? Se sim → high signal.

**Tagging:**
- 🔥 **HIGH** — flag obrigatório, exige decisão user em <7 dias
- ⚠️ **MEDIUM** — worth knowing, revisitar em 30 dias
- 💤 **LOW** — noted, sem acção imediata

## Output template (weekly master digest)

```markdown
# PROMETHEUS Weekly Digest — YYYY-WW

**Period:** YYYY-MM-DD to YYYY-MM-DD
**Sensors ran:** repos/mcp/papers/regulatory
**Total findings:** N raw → M filtered (signal:noise ratio)

## TOP 5 Actionable (🔥 HIGH signal)

1. **[Finding title]** [SENSOR] [TAG]
   - What: 1 sentence
   - Why it matters to DARIO: 1 sentence
   - Suggested action: 1 sentence
   - Cost to implement (rough): X hours / Y tokens

## MEDIUM signal (worth knowing)

[Bullet list with 1-line each]

## LOW signal (noted, no action)

[Bullet list compressed]

## Sensor health

- repo-scanner: X repos scanned, Y new releases
- mcp-discovery: X marketplaces scanned, Y new servers
- paper-tracker: X papers, Y relevant
- regulatory-watch: X sources, Y updates
```

## Autonomy tier 0 — RULES

PROMETHEUS Wave 1 has **ZERO autonomous action authority**:
- ❌ Não editar skills
- ❌ Não modificar company.yaml, skill_chains.yaml, ou qualquer config core
- ❌ Não criar pull requests
- ❌ Não ingerir conteúdo no RAG sem aprovação
- ✅ Apenas escrever em `~/.claude/orchestrator/prometheus/digests/*.md`
- ✅ Apenas escrever em `~/.claude/orchestrator/prometheus/state/*.yaml`

Tiers 1-3 (decay detectors, experimenters, self-updater) virão em Waves 2-3 com governance estrita.

## Cross-references

[[prometheus-repo-scanner]] · [[prometheus-mcp-discovery]] · [[prometheus-paper-tracker]] · [[prometheus-regulatory-watch]] · [[dream]] · [[oraculo-conference-tracking]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **prometheus-director** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in prometheus-director:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->
