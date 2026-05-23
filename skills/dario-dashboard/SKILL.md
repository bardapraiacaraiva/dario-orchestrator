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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Comando de arranque está correcto e testável
- [ ] Comando `python3 -m http.server` inclui porta correcta (8766) e directório correcto (`~/.claude/orchestrator/`)
- [ ] Sufixo `&>/dev/null &` presente para background silencioso
- [ ] URL de acesso especificado como `http://localhost:8766/dashboard.html` (não IP, não porta errada)
- [ ] Variantes OS presentes (Windows/macOS/Linux) com comando correcto para cada

- ❌ NOT delivery-ready: "Abre o terminal e executa o servidor HTTP na pasta do orchestrator"
- ✅ Delivery-ready: `python3 -m http.server 8766 --directory ~/.claude/orchestrator/ &>/dev/null &` → browser em `http://localhost:8766/dashboard.html`

---

### Gate 2 — Widgets mostram dados reais do projecto activo
- [ ] Widget Active Tasks referencia tasks reais (não "Task #1", "Task #2")
- [ ] Widget Budget mostra breakdown por projecto com nomes reais e valores (ex: "Cuidai — €340 / €500")
- [ ] Widget Quality Overview tem score numérico real (ex: "87.4 avg") com tier breakdown (A: 12, B: 8, C: 2)
- [ ] Widget System Health lista serviços com status datado (não só "verde")

- ❌ NOT delivery-ready: "O budget widget mostra quanto foi gasto no projecto"
- ✅ Delivery-ready: Budget ring chart → `LUSOconta: €127/$300 (42%) · SAQUEI: €89/$200 (44%) · Pulse: 14:32 22/06`

---

### Gate 3 — Sidebar com contagens verificáveis e skills correctas
- [ ] Contagem total de skills declarada e verificável (ex: "93 skills" — conta bate certo)
- [ ] Categorias com número correcto de skills entre parênteses
- [ ] Skills listadas correspondem às realmente instaladas em `~/.claude/orchestrator/`
- [ ] Nenhuma skill fantasma (listada mas ficheiro não existe)

- ❌ NOT delivery-ready: "A sidebar mostra várias categorias com as skills disponíveis"
- ✅ Delivery-ready: `SEO (16): seo-audit, seo-technical, seo-local, seo-schema... · DIVA (20): briefing, budget, timeline...` — total 93 confirma `ls ~/.claude/orchestrator/*.md | wc -l`

---

### Gate 4 — Red Flags e limitações comunicadas com workaround claro
- [ ] Limitação "dados estáticos" explicada com causa técnica (browser não lê YAML)
- [ ] Alternativa live especificada com comando exacto (`/dario-status` no Claude Code)
- [ ] Instrução de manutenção presente: quando actualizar o dashboard (ao adicionar/remover skills)
- [ ] Nenhuma promessa de real-time sem workaround documentado

- ❌ NOT delivery-ready: "Nota: o dashboard pode não ter os dados mais recentes"
- ✅ Delivery-ready: "Dashboard mostra snapshot estático — para dados live usa `/dario-status` no Claude Code. Actualizar `dashboard.html` sempre que adicionares skills novas."

---

### Gate 5 — Quick Actions mapeadas para skills/comandos reais
- [ ] Cada Quick Action (8) tem skill de destino identificável
- [ ] Acção "New Client" liga a skill específica (ex: `a360-nicho-explorer` ou `diva-briefing`)
- [ ] Acção "Diagnose" tem destino claro (ex: `/dario-status` ou `dario-analytics`)
- [ ] Clipboard copy confirmado com feedback visual (toast notification documentada)

- ❌ NOT delivery-ready: "Os botões de Quick Actions executam as acções principais do sistema"
- ✅ Delivery-ready: `Orchestrate → /dario-orchestrate · Taskboard → /dario-taskboard · New Client → /a360-nicho-explorer · Diagnose → /dario-status`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder
- [ ] Zero ocorrências de `<client>`, `<projecto>`, `<budget>`, `<score>`, `<data>`
- [ ] Se exemplo de budget → valores reais em € com nome de projecto real
- [ ] Se exemplo de task → task com título real, assignee real, prazo real
- [ ] Ficheiro referenciado (`dashboard.html`) com tamanho real (29KB) confirmado

- ❌ NOT delivery-ready: "Budget: `<client_name>` — `<valor_gasto>`/`<budget_total>`"
- ✅ Delivery-ready: "Budget: `Cuidai — €340/€500 (68%) · última actualização: pulse 14:47 22/06/2025`"

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## DARIO Dashboard — Cuidai Health Platform

**Abrir dashboard:**
```bash
python3 -m http.server 8766 --directory ~/.claude/orchestrator/ &>/dev/null &
```
Browser: `http://localhost:8766/dashboard.html`

---

### Estado actual (pulse 14:47 · 22/06/2025)

**Header:**
- Budget badge: 68% usado (€340 / €500)
- Último pulse: 22/06/2025 14:47
- Health: 🟢 Todos os serviços operacionais
- Search: filtra em tempo real (ex: "seo" → 16 skills)

---

### Active Tasks (Widget 1)
| Task | Projecto | Status | Prazo |
|------|----------|--------|-------|
| SEO audit homepage | Cuidai | 🔄 In Progress | 24/06 |
| CWV fix mobile | Cuidai | ⏳ Pending | 25/06 |
| Pricing page copy | Cuidai | ✅ Done | 21/06 |

---

### Budget Breakdown (Widget 2)
- Cuidai total: **€340 / €500**
  - Claude Opus 4: €210 (62%)
  - Claude Sonnet 4: €98 (29%)
  - GPT-4o: €32 (9%)
- Ring chart: 68% preenchido · restam €160

---

### Quality Overview (Widget 3)
- Score médio: **87.4 / 100**
- Tier A (90+): 12 outputs
- Tier B (75-89): 8 outputs
- Tier C (<75): 2 outputs → revisão pendente

---

### System Health (Widget 4)
- ✅ Orchestrator: operacional
- ✅ Taskboard: 3 tasks activas
- ✅ Heartbeat: último pulse há 13 min
- ⚠️ Autopilot: pausado (manual override 14:30)

---

### Quick Actions
`Orchestrate` → `/dario-orchestrate` · `Taskboard` → `/dario-taskboard`
`Autopilot` → `/dario-autopilot` · `Health Check` → `/dario-status`
`Budget` → `/dario-budget` · `New Client` → `/a360-nicho-explorer`
`A360` → `/a360-pipeline` · `Diagnose` → `/dario-analytics`

---

### Sidebar — 93 skills (Cuidai stack activo)
- **SEO (16):** seo-audit ✅ · seo-technical ✅ · seo-local ✅ · seo-schema ✅
- **DIVA (20):** diva-briefing ✅ · diva-budget ✅ · diva-timeline ✅
- **Technical (7):** wp-audit ✅ · cwv-fix 🔄 · pentest ⏳
- Click em qualquer skill → copia `/skill-name` para clipboard + toast "Copiado!"

---

⚠️ **Limitação:** Dashboard mostra snapshot estático do último pulse (14:47).
Para dados live: usar `/dario-status` directamente no Claude Code.
Actualizar `dashboard.html` ao adicionar novas skills (`~/.claude/orchestrator/`).

**Ficheiro:** `~/.claude/orchestrator/dashboard.html` · 29KB · zero dependências
```

---

## Output anti-patterns

- Descrever widgets em abstracto sem mostrar dados de exemplo reais (valores, nomes, datas)
- Listar Quick Actions sem mapear cada botão ao comando ou skill de destino exacto
- Omitir a limitação "dados estáticos" ou mencioná-la sem alternativa live accionável
- Contagem de skills declarada (93) sem verificabilidade — número não bate com ficheiros reais
- Comandos OS-specific incompletos (só macOS, esquece Windows/Linux)
- Red Flags enterradas no fim sem destaque visual — user ignora e fica confuso com dados desactualizados
- Sidebar descrita como "várias categorias" sem especificar quais skills estão em cada uma
- Exemplo de budget com `<valor>` ou `<projecto>` em vez de números reais
- Toast notification mencionada mas sem confirmar comportamento (quanto tempo dura, o quê exactamente copia)
- Ficheiro `dashboard.html` referenciado sem tamanho ou indicação de self-contained (zero dependencies)
