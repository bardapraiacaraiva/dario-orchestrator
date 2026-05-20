# PROMETHEUS — External Knowledge & Evolution Squad

**Wave 1: Passive monitoring only. ZERO autonomous action.**

## Diferenciação

| Sistema | Função |
|---|---|
| `dream/` subsystem | Internal memory consolidation (4-fase diária) |
| `ORACULO` squad | Deep research em papers/conferences (specialized depth) |
| **PROMETHEUS** | External breadth sweep (repos, MCPs, papers, regulatory) |

## Sensores Wave 1

| Sensor | Source | Frequência sugerida | Output |
|---|---|---|---|
| `prometheus-repo-scanner` | GitHub Tier 1-5 watchlist | Domingo 22h00 | `digests/YYYY-WW-repos.md` |
| `prometheus-mcp-discovery` | MCP marketplaces + npm | Domingo 22h15 | `digests/YYYY-WW-mcp.md` |
| `prometheus-paper-tracker` | arXiv + Anthropic blog | Domingo 22h30 | `digests/YYYY-WW-papers.md` |
| `prometheus-regulatory-watch` | PT/BR/EU sources | Sexta 18h00 | `digests/YYYY-WW-regulatory.md` |

## Invocação

### Manual (qualquer altura)
```
/prometheus-director  → vê estado, decide próxima acção
ou triggers:
  "scan mundo"
  "weekly digest"
  "novidades semana"
```

### Via chain (sequencial 4 sensores + master digest)
```
prometheus_weekly_scan  → ~18K tokens, 4 sensores em sequência
```

### Programado (Task Scheduler — instalar manualmente)
Pendente configuração. Suggested:
```powershell
schtasks /create /tn "PROMETHEUS Weekly" /tr "claude --skill prometheus_weekly_scan" /sc weekly /d SUN /st 22:00
```

## Governance — Wave 1 rules

✅ **PERMITIDO:**
- Escrever em `digests/*.md` (output)
- Escrever em `state/*.yaml` (tracking)
- Ler GitHub API, arXiv, blogs, gov sources

❌ **PROIBIDO:**
- Editar qualquer SKILL.md
- Modificar `company.yaml`, `skill_chains.yaml`
- Eliminar memorias
- Push para repos
- Modificar licensing

## Signal filter (90% noise reduction)

Para um finding aparecer no digest, passa 3 perguntas:
1. **Aplicabilidade:** afecta directamente um dos 32 squads / 536 skills?
2. **Materialidade:** delta vs estado actual >10% OU resolve gap OU regulatory mandatory?
3. **Risco non-adoção:** perder edge / compliance em 6 meses?

Tags: 🔥 HIGH (decisão <7d) · ⚠️ MEDIUM (revisitar 30d) · 💤 LOW (noted)

## Estado actual

- ✅ 5 skills criadas (director + 4 sensores)
- ✅ Chain `prometheus_weekly_scan` em skill_chains.yaml
- ✅ Entries em company.yaml (agents_meta_evolution, workers_prometheus, squads_prometheus, dispatch_prometheus, prometheus_governance)
- ⏳ State files vazios (populate on first run)
- ⏳ Task Scheduler cron: instalação manual pendente
- ⏳ Primeiro weekly digest: pendente primeira execução

## Próximos passos (sugeridos)

1. **Primeira execução manual** — invocar `prometheus_weekly_scan` para gerar baseline digest
2. **Configurar Task Scheduler** — automatizar weekly cron
3. **30 dias de dados** antes de avançar para Wave 2 (decay detectors)
4. **Wave 2** quando: 4 weekly digests produzidos + signal:noise ratio aceitável validado

## Wave roadmap

| Wave | Tier | Skills | Status |
|---|---|---|---|
| **1** | T0 — Passive | 4 sensores + director | ✅ Built |
| 2 | T1 — Flag-only | 3 decay detectors (deprecation, stale facts, version drift) | Pending |
| 3 | T2 — Sandboxed | 3 experimenters (A/B, shadow dispatch, meta-skill-builder) | Pending |
| 3 | T3 — Supervised | 2 curator + self-updater (com green/yellow/red list enforcement) | Pending |

## Related

- `~/.claude/skills/prometheus-*/SKILL.md` — sensors
- `~/.claude/orchestrator/skill_chains.yaml` — chain definition
- `~/.claude/orchestrator/company.yaml` — agent/worker/squad config
- `~/.claude/orchestrator/memory/` — internal consolidation (dream subsystem)
- `~/.claude/skills/oraculo-*/SKILL.md` — deep research squad (complementary)
