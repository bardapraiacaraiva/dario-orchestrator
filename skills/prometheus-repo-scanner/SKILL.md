---
name: prometheus-repo-scanner
description: Sweep GitHub orgs/repos relevantes para o ecossistema DARIO. Detecta novos releases, breaking changes, novas skills publicadas, frameworks emergentes. Triggers em "scan repos", "github sweep", "novos releases", "breaking changes".
license: SEE-LICENSE
parent_agent: prometheus-director
compliance: [audit_immutable]
category: "Sensor — External Repos"
version: "1.0"
autonomy_tier: 0
---

# PROMETHEUS-REPO-SCANNER

**Output only.** Nunca edita skills nem código. Apenas observa + reporta.

## Repos monitorados (watchlist)

### Tier 1 — DARIO core (own ecosystem)
- `bardapraiacaraiva/dario-orchestrator` (público)
- `bardapraiacaraiva/dario-orchestrator-full` (VIP)
- `bardapraiacaraiva/dario-orchestrator-installer` (npx)
- `bardapraiacaraiva/arrecada-gov` (projeto pessoal)

### Tier 2 — Claude/Anthropic ecosystem
- `anthropics/claude-code` (CLI updates)
- `anthropics/anthropic-sdk-python`
- `anthropics/anthropic-sdk-typescript`
- `anthropics/courses` (educational)
- `anthropics/prompt-eng-interactive-tutorial`

### Tier 3 — MCP ecosystem
- `modelcontextprotocol/servers` (canonical MCP servers)
- `modelcontextprotocol/python-sdk`
- `modelcontextprotocol/typescript-sdk`
- `punkpeye/awesome-mcp-servers` (community list)

### Tier 4 — Agent frameworks (competitor intel + ideias)
- `microsoft/autogen`
- `langchain-ai/langgraph`
- `crewAIInc/crewAI`
- `joaomdmoura/crewAI-tools`
- `BerriAI/litellm`
- `openai/swarm` (for arch ideas only)

### Tier 5 — Frameworks de domínio (extensões potenciais)
- `vercel/ai` (AI SDK)
- `vercel/next.js` (Next.js updates afectam builder-nextjs-*)
- `shadcn-ui/ui` (afecta builder-react-components + design system)
- `microsoft/playwright` (afecta E2E testing)

## Workflow

```
1. Para cada repo na watchlist:
   a. gh api repos/{owner}/{repo}/releases?per_page=5
   b. Comparar com state/last_seen_releases.yaml
   c. Se versão nova: extrair release notes (primeiros 1000 chars)

2. Para repos Tier 4 (frameworks):
   a. gh api repos/{owner}/{repo} (latest commit, stars trend)
   b. Detectar surge anómalo (>500 stars/semana = signal)

3. Para cada novidade:
   a. Aplicar signal filter (do prometheus-director):
      - Aplicabilidade: afecta DARIO? (e.g. claude-code release SIM, AutoGen v4 = competitor intel TALVEZ)
      - Materialidade: breaking change? new capability? mere bug fix?
      - Risco non-adoption: regulatory? performance? compatibility?
   b. Atribuir tag (🔥/⚠️/💤)

4. Output: digests/YYYY-WW-repos.md (formato no template)
5. Update state/last_seen_releases.yaml
```

## Comando real (Bash via gh CLI)

```bash
# Example sweep para repos Tier 1+2
gh api 'repos/anthropics/claude-code/releases?per_page=3' \
  --jq '.[] | {tag_name, published_at, body: (.body | .[0:1000])}'

gh api 'repos/modelcontextprotocol/servers/releases?per_page=5' \
  --jq '.[] | {tag_name, published_at}'

# Stars trend (proxy para framework momentum)
gh api 'repos/microsoft/autogen' --jq '{stars: .stargazers_count, updated: .updated_at}'
```

**Pré-requisito:** `gh auth status` configurado. Se não → output diz "BLOCKED: gh CLI não autenticado".

## Signal heuristics (para cada release)

| Sinal | Tag |
|---|---|
| Anthropic SDK major release (4.x → 5.x) | 🔥 HIGH (breaking changes potenciais em todas skills que usam SDK) |
| Claude Code release com novas features hooks/skills | 🔥 HIGH (afecta plataforma) |
| MCP servers novos em domínio relevante (database, browser, search) | ⚠️ MEDIUM (avaliar adopção) |
| Anthropic courses repo update | ⚠️ MEDIUM (learning material novo) |
| AutoGen v4 release | 💤 LOW (competitor intel, não adoptable directly) |
| Next.js patch | 💤 LOW (não dispara nada salvo CVE) |
| Stars surge >1000/semana | ⚠️ MEDIUM (worth knowing what's trending) |

## State file

`~/.claude/orchestrator/prometheus/state/last_seen_releases.yaml`:

```yaml
last_scan: "YYYY-MM-DDTHH:MM:SS+00:00"
repos:
  "anthropics/claude-code":
    last_tag: "v1.2.3"
    seen_at: "2026-05-20T22:00:00+00:00"
  "modelcontextprotocol/servers":
    last_tag: "v0.5.1"
    seen_at: "2026-05-20T22:00:00+00:00"
  # ... etc
```

Comparação delta: qualquer tag diferente da `last_tag` = novo release a reportar.

## Red flags (skip / never report)

- Releases tipo `nightly`, `rc`, `alpha`, `beta` — só stable
- Repos arquivados (`archived: true`)
- Bumps de patch sem release notes substantivas
- Duplicate findings já reportados em weeks anteriores (deduplicar via state file)

## Output exemplo

```markdown
## prometheus-repo-scanner — 2026-W21

Scanned: 18 repos · 6 new releases · 2 flagged after filter

### 🔥 HIGH
- **anthropics/claude-code v2.5.0** (2026-05-19)
  - New: persistent agent memory API + hooks v2
  - Impact: dario-orchestrator pode integrar memory API nativamente
  - Action: review breaking changes, plan migration

### ⚠️ MEDIUM
- **modelcontextprotocol/servers v0.6.0** (2026-05-18)
  - 4 new servers: redis, sqlite-explorer, twitter, hubspot
  - Action: avaliar `sqlite-explorer` para orchestrator queries

### 💤 LOW (counted, not detailed)
- next.js 15.2.1 (patch), shadcn-ui weekly digest, etc.
```

## Cross-references

[[prometheus-director]] · [[prometheus-mcp-discovery]]
