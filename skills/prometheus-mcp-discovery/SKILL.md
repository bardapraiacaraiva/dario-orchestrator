---
name: prometheus-mcp-discovery
description: Sweep MCP marketplaces e registries para novos servers que possam estender capacidades DARIO. Triggers em "scan mcp", "novos mcp", "mcp marketplace", "mcp servers novos".
license: SEE-LICENSE
parent_agent: prometheus-director
compliance: [audit_immutable]
category: "Sensor — MCP Ecosystem"
version: "1.0"
autonomy_tier: 0
---

# PROMETHEUS-MCP-DISCOVERY

**Output only.** Não instala servers. Reporta candidatos.

## Sources monitorados

### Canonical (Anthropic-blessed)
- `github.com/modelcontextprotocol/servers` — official servers list
- `modelcontextprotocol.io` — MCP spec + ecosystem page

### Community curated
- `github.com/punkpeye/awesome-mcp-servers` (~600+ servers tracked)
- `github.com/wong2/awesome-mcp-servers`
- `github.com/appcypher/awesome-mcp-servers`

### Marketplaces
- `mcpmarket.com` (community marketplace)
- `pulsemcp.com` (curated)
- `mcp.so` (registry)
- `glama.ai/mcp` (Glama platform)

### Package registries (programmatic discovery)
- npm: `mcp-server-*`, `@modelcontextprotocol/*`
- pypi: `mcp-server-*`

## Workflow

```
1. Fetch awesome-mcp-servers README.md (canonical list)
2. Diff vs state/known_mcp_servers.yaml
3. Para cada NEW server:
   a. Categorize (database, browser, search, productivity, finance, etc.)
   b. Quality check:
      - GitHub stars >50?
      - Last commit <90 days?
      - Has README + install instructions?
      - License compatible (MIT/Apache)?
   c. Relevância DARIO check:
      - Cobre gap actual? (e.g. ainda não temos MCP de Notion, Linear, Slack)
      - Duplicate de algo já existente?
      - Risco LGPD/security?

4. Output: digests/YYYY-WW-mcp.md

5. Update state/known_mcp_servers.yaml
```

## Comando real

```bash
# Fetch canonical MCP servers list
curl -s https://raw.githubusercontent.com/modelcontextprotocol/servers/main/README.md \
  | grep -E "^\- \[" | head -50

# Awesome-mcp-servers
curl -s https://raw.githubusercontent.com/punkpeye/awesome-mcp-servers/main/README.md \
  | wc -l  # rough line count to detect updates

# Recent npm registry
curl -s "https://registry.npmjs.org/-/v1/search?text=mcp-server&size=20" \
  | jq '.objects[].package | {name, version, date}'
```

## Categorization rubric

| Categoria | Sinal de relevância para DARIO | Tag default |
|---|---|---|
| **Database/Storage** (postgres, mongo, redis) | ⚠️ relevante se cobre gap |
| **Browser/Web** (playwright, fetch, jina) | ⚠️ alguns já temos via playwright MCP |
| **Search** (brave, google, perplexity) | ⚠️ avaliar vs WebSearch nativo |
| **Productivity** (notion, linear, slack, trello) | 🔥 high — coverage gap actual |
| **Finance** (stripe, asaas, mercadopago) | ⚠️ relevante para atlas-fin/kirion |
| **Healthcare** (FHIR, HL7) | ⚠️ relevante para medik |
| **Legal/Regulatory** (lex, RGPD scanners) | 🔥 high — coverage gap actual |
| **Dev tools** (filesystem, git, github) | 💤 maioria já temos |
| **AI/ML** (huggingface, openai, replicate) | ⚠️ avaliar caso a caso |
| **Niche/Hobby** (D&D, recipes, etc.) | 💤 ignore |

## Signal filter — DARIO specifics

Para um MCP entrar como 🔥 HIGH precisa de:

1. **Resolver gap conhecido:**
   - Notion / Linear / Slack integration (productivity squads precisam)
   - Real-time analytics (demeter precisa)
   - Banking PT/BR APIs (atlas-fin gaps)

2. **Better than existing alternative:**
   - Se já temos solução via Bash/curl, MCP só vale se simplifica >50%

3. **Maintained:**
   - Last commit <90 days
   - Issue response time razoável
   - Não-abandonado

## State file

`~/.claude/orchestrator/prometheus/state/known_mcp_servers.yaml`:

```yaml
last_scan: "YYYY-MM-DDTHH:MM:SS+00:00"
sources_scanned:
  - awesome-mcp-servers (punkpeye)
  - modelcontextprotocol/servers
  - npm registry
servers:
  "@modelcontextprotocol/server-filesystem":
    seen_at: "2026-05-20"
    category: dev-tools
    relevance: low
  # ... etc
new_this_week: []  # populated each run
```

## Output exemplo

```markdown
## prometheus-mcp-discovery — 2026-W21

Scanned: 4 sources · 12 new servers · 2 flagged after filter

### 🔥 HIGH
- **mcp-server-notion** (@notionhq, 800★, MIT)
  - Coverage gap: integration Notion → obsidian-corp squad
  - Capability: read/write páginas, blocos, databases via MCP
  - Risk: API key handling LGPD (read-only mode possible)
  - Suggested action: avaliar adopção piloto

### ⚠️ MEDIUM
- mcp-server-linear (community, 240★)
- mcp-server-perplexity (Perplexity team)

### 💤 LOW
- 7 niche servers (D&D, recipes, etc.) — counted not detailed
```

## Cross-references

[[prometheus-director]] · [[prometheus-repo-scanner]] · [[builder-smart-context]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **prometheus-mcp-discovery** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in prometheus-mcp-discovery:**

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
