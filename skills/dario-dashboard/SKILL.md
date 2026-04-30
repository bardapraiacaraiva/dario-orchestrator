---
name: dario-dashboard
description: "Abre o dashboard visual do DARIO Orchestrator no browser. Mostra taskboard, budget, quality, health, e quick actions. Triggers: 'dashboard', 'painel', 'abrir dashboard', 'mostrar dashboard'."
license: MIT
---

# DARIO Dashboard — Visual Operations Center

## Quando usar

- Inicio de sessao: ver estado geral do sistema
- Review rapido: tasks, budget, quality, health
- Acesso rapido a qualquer skill via sidebar
- Quando o user pede "dashboard", "painel", "mostrar dashboard"

## Como abrir

Executar no terminal:
```bash
python3 -m http.server 8766 --directory ~/.claude/orchestrator/ &>/dev/null &
```

Depois abrir no browser:
```
http://localhost:8766/dashboard.html
```

Ou abrir directamente o ficheiro:
```bash
start ~/.claude/orchestrator/dashboard.html    # Windows
open ~/.claude/orchestrator/dashboard.html     # macOS
xdg-open ~/.claude/orchestrator/dashboard.html # Linux
```

## O que mostra

### Header
- Budget badge (% usado)
- Ultimo pulse timestamp
- Health indicator (verde/amarelo/vermelho)
- Search bar para filtrar skills

### Sidebar (93 skills organizadas)
- Orchestrator (3) — orchestrator, taskboard, dispatch
- Automation (2) — heartbeat, autopilot
- Intelligence (3) — quality, analytics, status
- Marketing (12) — brand, offer, ads, funnel, etc.
- Technical (7) — wp-audit, cwv-fix, pentest, etc.
- SEO (16) — audit, technical, local, schema, etc.
- Finance (3) — financial-model, pricing, saas-metrics
- Content (7) — content, social, hr, legal, etc.
- A360 (15) — nicho-explorer, pipeline completo
- DIVA (20) — briefing, budget, timeline, etc.
- LUCAS (5) — heartbeat, autopilot, quality, etc.

### 4 Widgets
1. **Active Tasks** — tabela com tasks do taskboard
2. **Budget** — ring chart + breakdown por projecto/modelo
3. **Quality Overview** — score medio + tier distribution
4. **System Health** — status de todos os servicos

### Quick Actions (8 botoes)
Orchestrate, Taskboard, Autopilot, Health Check, Budget, New Client, A360, Diagnose

## Funcionalidades

- Click em qualquer skill → copia comando para clipboard
- Search filtra skills em tempo real
- Toast notifications ao copiar
- Sidebar colapsavel

## Ficheiro
`~/.claude/orchestrator/dashboard.html` (29KB, single file, zero dependencies)

## Red Flags

- Dashboard mostra dados estaticos — nao le YAML em tempo real (limitacao do browser)
- Para dados live, usar `/dario-status` no Claude Code
- Manter o dashboard actualizado quando mudar skills ou adicionar novas
