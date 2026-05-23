---
name: dario-dispatch
description: "Intelligent routing engine — maps tasks to the optimal agent, skill, or squad based on capabilities, availability, and company hierarchy. Supports parallel assignment, escalation chains, and cross-division coordination (DARIO + DIVA + LUCAS). Triggers on: 'dispatch', 'despacha', 'routing', 'quem faz isto', 'atribui', 'assign'."
license: MIT
---

# DARIO Dispatch — Intelligent Task Routing

The "brain" that decides WHO does WHAT. Maps tasks to the optimal executor using capability matching, workload awareness, and company hierarchy from `company.yaml`.

## When to activate

- Called by `dario-orchestrator` during Phase 3 (Dispatch)
- User asks "quem faz isto?", "quem deve trabalhar nisto?"
- User wants to assign or reassign work
- Cross-division coordination needed (DARIO + DIVA + LUCAS)
- Invoked via `/dario-dispatch`

## Routing Algorithm

### Step 0: Check Skill Chains FIRST

Before any individual routing, check if the task matches a **skill chain** in `~/.claude/orchestrator/skill_chains.yaml`:

1. Extract keywords from user request
2. Match against `trigger_keywords` of each chain
3. If match found → **activate chain** (auto-sequential execution, no individual dispatch needed)
4. If no chain match → proceed to Step 1 (individual routing)

**Available chains:** brand_to_market, brand_to_ads, audit_to_fix, seo_full_pipeline, diva_full_project, client_full_onboard

**Priority:** Chain > Composite Mode > Individual Skill

### Step 1: Parse Task Requirements

From the task, extract:
- **Domain keywords** — What area of expertise is needed?
- **Skill reference** — Does the task specify a skill directly?
- **Division** — DARIO (digital), DIVA (architecture), LUCAS (SaaS accounting)?
- **Complexity** — Single skill, multi-skill, or squad-level?
- **Policy** — What execution policy applies?

### Step 2: Capability Matching + Workload Awareness

Load `~/.claude/orchestrator/company.yaml` (both `agents:` and `workers:` sections) and match:

```python
def find_best_executor(task):
    # 1. Direct skill match (fastest path)
    if task.skill:
        worker = find_worker_by_skill(task.skill)  # check workers: section
        if worker and is_available(worker):
            return worker
        elif worker and not is_available(worker):
            # Primary worker busy — find fallback (see Step 2.5)
            fallback = find_fallback(task, worker)
            if fallback:
                return fallback
            # No fallback — queue task for next pulse
            LOG "QUEUED: {task.id} — {worker.id} busy, no fallback available"
            return None
    
    # 2. Capability intersection
    candidates = []
    for worker in all_workers:
        overlap = set(task.required_capabilities) & set(worker.capabilities)
        if overlap:
            load = get_active_task_count(worker)  # workload check
            candidates.append((worker, len(overlap), load))
    
    # 3. Sort by: capability overlap > lowest workload > division match
    candidates.sort(key=lambda x: (
        x[1],                          # More capability overlap = better
        -x[2],                         # FEWER active tasks = better (negative for desc sort)
        x[0].division == task.division, # Same division preferred
    ), reverse=True)
    
    # 4. Return best match (or escalate)
    return candidates[0][0] if candidates else escalate_to_manager(task)
```

### Step 2.5: Workload Awareness

**Before assigning ANY task, check worker availability:**

```python
def is_available(worker):
    """A worker is available if they have no in_progress tasks."""
    active_tasks = read_all_tasks("~/.claude/orchestrator/tasks/active/")
    in_progress = [t for t in active_tasks 
                   if t.assignee == worker.id and t.status == "in_progress"]
    return len(in_progress) == 0

def get_active_task_count(worker):
    """Count tasks assigned to this worker (any non-done status)."""
    active_tasks = read_all_tasks("~/.claude/orchestrator/tasks/active/")
    return len([t for t in active_tasks 
                if t.assignee == worker.id and t.status in ["todo", "in_progress", "in_review"]])

def find_fallback(task, primary_worker):
    """Find next-best worker when primary is busy."""
    # 1. Check same director's other workers with overlapping capabilities
    director = primary_worker.reports_to
    siblings = [w for w in all_workers if w.reports_to == director and w.id != primary_worker.id]
    
    for sibling in siblings:
        overlap = set(task.required_capabilities or []) & set(sibling.capabilities)
        if overlap and is_available(sibling):
            LOG "FALLBACK: {task.id} → {sibling.id} (primary {primary_worker.id} busy)"
            return sibling
    
    # 2. Escalate to director (manager can execute if capable)
    director_agent = get_agent(director)
    if director_agent and has_capability_overlap(director_agent, task):
        LOG "ESCALATE: {task.id} → {director} (all workers busy)"
        return director_agent
    
    # 3. No fallback — return None (task will be queued)
    return None
```

**Workload limits:**
- Worker: max 1 `in_progress` task at a time (atomic checkout)
- Director: max 2 tasks (can oversee + execute)
- VP/CEO: no limit (orchestration overhead, not execution)

### Step 3: Division Routing

| Task Domain | Primary Division | Adapter |
|---|---|---|
| Digital marketing, SEO, web dev, copy | DARIO | `dario-v2-digital-ceo` |
| Architecture, interior design, construction | DIVA | `diva-v1-design-architect` |
| Portuguese accounting SaaS, AI agents | LUCAS | `dario-v2-digital-ceo` (LUCAS context) |
| Cross-division (e.g., website for architect) | DARIO + DIVA | Multi-agent parallel |

### Step 4: Escalation Chain

If no worker matches:
```
Worker (skill) → Director (manager) → VP (division) → CEO (DARIO)
```

Each level can:
- Accept and execute (if capable)
- Delegate down to a different worker
- Escalate up to the next level
- Request a new worker be "hired" (new skill created)

### Step 5: Parallel Assignment Planning

For complex tasks requiring multiple capabilities:

**Rule: Maximum 3 parallel workers per heartbeat**

```python
def plan_parallel(tasks):
    # Group independent tasks (no mutual dependencies)
    independent_groups = find_independent_sets(tasks)
    
    # Create execution waves
    waves = []
    for group in independent_groups:
        # Max 3 per wave
        for batch in chunks(group, 3):
            waves.append(batch)
    
    return waves
```

**Parallel execution via Agent tool:**
```python
# Wave 1: Independent tasks run simultaneously
Agent({ description: "Task A", subagent_type: "dario-v2-digital-ceo", prompt: "..." })
Agent({ description: "Task B", subagent_type: "diva-v1-design-architect", prompt: "..." })
Agent({ description: "Task C", subagent_type: "dario-v2-digital-ceo", prompt: "..." })

# Wave 2: Tasks that depended on Wave 1
Agent({ description: "Task D (depends on A+B)", ... })
```

## Routing Tables

### DARIO Division — Digital Agency

#### Marketing & Growth (dir-marketing)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| brand, positioning, archetype, identity | worker-brand | dario-brand | Brand Squad |
| offer, pricing, value equation, hormozi | worker-offer | dario-offer | Hormozi Squad |
| copy, sales letter, headline, VSL | worker-sales-letter | dario-sales-letter | Copy Squad |
| ads, traffic, facebook, google, youtube | worker-ads | dario-ads-blueprint | Traffic Masters |
| funnel, value ladder, tripwire, lead magnet | worker-funnel | dario-funnel | Sales Squad |
| pipeline, outbound, prospecting, ICP | worker-pipeline | dario-pipeline | Sales Squad |
| email, sequence, nurture, launch | worker-email-seq | dario-email-seq | Copy Squad |
| naming, brand name, domain | worker-naming | dario-naming | Brand Squad |
| story, narrative, origin, about page | worker-story-circle | dario-story-circle | Storytelling Squad |
| pitch, deck, investor, presentation | worker-pitch | dario-pitch | - |
| proposal, quotation, scope, budget | worker-proposal | dario-proposal | Sales Squad |
| negotiation, objections, closing | worker-negotiation | dario-negotiation | Sales Squad |

#### Technical (dir-technical)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| wordpress, theme, plugin, wp | worker-wp-audit | dario-wp-audit | - |
| woocommerce, checkout, payment, mbway | worker-woo-audit | dario-woo-audit | - |
| core web vitals, lcp, inp, cls, speed | worker-cwv-fix | dario-cwv-fix | - |
| security, pentest, owasp, vulnerability | worker-pentest | dario-pentest-checklist | Cybersecurity Squad |
| make, automation, zapier, webhook | worker-make-blueprint | dario-make-blueprint | - |
| ios, iphone, swift, hig, apple | worker-ios-hig | dario-ios-hig | - |
| sop, procedure, process, checklist | worker-sop | dario-sop | Operations Squad |

#### SEO (dir-seo)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| full seo audit, site health | worker-seo-audit | seo-audit | Data Squad |
| crawl, robots, indexation, javascript render | worker-seo-technical | seo-technical | - |
| content quality, eeat, readability | worker-seo-content | seo-content | - |
| schema, json-ld, structured data, rich results | worker-seo-schema | seo-schema | - |
| local seo, gbp, nap, citations, map pack | worker-seo-local | seo-local | - |
| ai overviews, geo, perplexity, chatgpt search | worker-seo-geo | seo-geo | - |
| seo strategy, content plan, site architecture | worker-seo-plan | seo-plan | - |
| single page analysis, on-page | worker-seo-page | seo-page | - |
| sitemap, xml sitemap | worker-seo-sitemap | seo-sitemap | - |
| image seo, alt text, lazy loading | worker-seo-images | seo-images | - |
| hreflang, international, multilingual | worker-seo-hreflang | seo-hreflang | - |
| programmatic seo, scaled pages | worker-seo-programmatic | seo-programmatic | - |
| competitor pages, vs, alternatives | worker-seo-competitor | seo-competitor-pages | - |
| keyword data, serp, backlinks, live data | worker-seo-dataforseo | seo-dataforseo | - |
| og image, social preview, hero image | worker-seo-image-gen | seo-image-gen | - |
| keyword cluster, topic map, pillar | worker-kw-cluster | dario-kw-cluster | - |

#### Finance (dir-finance)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| p&l, cash flow, forecast, break-even | worker-financial-model | dario-financial-model | CFO Squad |
| pricing, rate, cost/hour, margin | worker-pricing-calculator | dario-pricing-calculator | - |
| mrr, arr, churn, ltv, cac, nrr | worker-saas-metrics | dario-saas-metrics | CFO Squad |

#### Client Success (dir-client-success)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| onboard, new client, kickoff | worker-client-onboard | dario-client-onboard | - |
| diagnose, audit, evaluate, roadmap | worker-diagnose | dario-diagnose | Advisory Board |
| switch project, context, load project | worker-projeto | dario-projeto | - |

### DIVA Division — Architecture & Design

#### Design (dir-design)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| moodboard, palette, style, inspiration | worker-diva-moodboard | diva-moodboard | Interior Design Squad |
| materials, finishes, ceramic, stone, wood | worker-diva-materials | diva-materials | - |
| floor plan, layout, circulation, spatial | worker-diva-floor-plan | diva-floor-plan | Architecture Masters |
| render, visualization, 3D, midjourney | worker-diva-render | diva-render | - |
| render brief, camera, lighting, styling | worker-diva-render-brief | diva-render-brief | - |
| photo analysis, space assessment, vision | worker-diva-vision | diva-vision | - |
| portfolio, case study, showcase | worker-diva-portfolio | diva-portfolio | - |
| smart home, domotica, knx, zigbee | worker-diva-smart-home | diva-smart-home | - |
| briefing, client needs, requirements | worker-diva-briefing | diva-briefing | - |

#### Construction (dir-construction)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| budget, cost, pronic, iva, m2 price | worker-diva-budget | diva-budget | Budget Squad |
| calculator, 3 scenarios, simulate | worker-diva-calc | diva-calc | - |
| timeline, gantt, duration, phases | worker-diva-timeline | diva-timeline | - |
| inspection, punch list, quality control | worker-diva-inspection | diva-inspection | - |
| contract, empreitada, guarantees, penalties | worker-diva-contract | diva-contract | - |
| compare proposals, contractor, best value | worker-diva-comparador | diva-comparador | - |
| planradar, field report, export tickets | worker-diva-planradar | diva-planradar | - |
| bim, revit, archicad, ifc, schedules | worker-diva-bim | diva-bim | - |
| diagnostic, structural, regulatory check | worker-diva-diagnose | diva-diagnose | - |
| roadmap, big picture, visual plan | worker-diva-roadmap | diva-roadmap | - |

#### Regulatory (dir-regulatory)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| licensing, permits, camara, rjue, rgeu | worker-diva-licensing | diva-licensing | Regulation Squad |
| energy, sce, reh, recs, nzeb, certification | worker-diva-energy | diva-energy | - |

### A360 Division — Business Acceleration

#### Research & Discovery (dir-a360-research)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| nicho, niche, top nichos, validar nicho | worker-a360-nicho-explorer | nicho-explorer | - |
| mapear nicho, ICP, dores, mecanismo, oferta | worker-a360-mapear-nicho | mapear-nicho-lite | - |
| cliente, prospect, pesquisar empresa, SPIN | worker-a360-cliente-radar | cliente-radar | - |

#### Production (dir-a360-production)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| landing page, LP, CRO, AIDA, PAS | worker-a360-lp-builder | lp-builder | - |
| pitch deck, slides, apresentacao comercial | worker-a360-pitch-deck | pitch-deck-builder | - |
| go to market, GTM, outbound, prospectar | worker-a360-gtm | gtm-architect | - |
| script vendas, playbook, objecoes, DEAL | worker-a360-playbook-vendas | playbook-vendas | - |
| meeting prep, briefing reuniao, call | worker-a360-meeting-prep | meeting-prep | - |

#### A360 Pipelines (pre-composed)

O A360 tem o seu proprio coordenador (`a360-framework-lite`) com pipelines pre-compostos. Quando o dispatch detecta intencao A360, pode:
- Delegar directamente ao coordenador A360 (que gere o pipeline internamente)
- Ou decompor em tasks individuais no taskboard (para tracking granular)

| Pipeline | Trigger | Skills Chain |
|---|---|---|
| prospect-meeting | "vou apresentar para cliente X" | cliente-radar → mapear-nicho → pitch-deck → meeting-prep |
| business-foundation | "estruturar empresa para nicho X" | nicho-explorer → mapear-nicho → gtm-architect → lp-builder |
| client-deliverable | "pacote completo para cliente" | cliente-radar → mapear-nicho → lp-builder → pitch-deck |
| niche-discovery | "nao sei que nicho escolher" | nicho-explorer → (user picks) → mapear-nicho |
| quick-pitch-deck | "preciso do deck para amanha" | mapear-nicho → pitch-deck |

### ATLAS Division — Events, Logistics & Services

#### Event Planning (dir-event-planning)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| briefing evento, novo evento, event brief, requisitos | worker-atlas-briefing | atlas-briefing | Event Masters Squad |
| venue, local, espaco, quinta, palacio, sala | worker-atlas-venue | atlas-venue | - |
| timeline, run of show, cronograma, agenda dia | worker-atlas-timeline | atlas-timeline | - |
| budget evento, orcamento evento, custos evento | worker-atlas-budget | atlas-budget | - |
| checklist, day-of, run sheet, procedimentos | worker-atlas-checklist | atlas-checklist | - |
| pos-evento, debrief, survey, ROI evento, feedback | worker-atlas-post-event | atlas-post-event | - |

#### Logistics Operations (dir-logistics)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| vendor, fornecedor, RFP, procurement evento | worker-atlas-vendor | atlas-vendor | Logistics Operations Squad |
| catering, menu, F&B, comida, bebidas, HACCP | worker-atlas-catering | atlas-catering | - |
| transporte, shuttle, parking, fleet, load-in | worker-atlas-transport | atlas-transport | - |
| hotel, alojamento, room block, hospedagem | worker-atlas-accommodation | atlas-accommodation | - |
| staff evento, equipa, voluntarios, briefing equipa | worker-atlas-staff | atlas-staff | - |
| armazem, inventario, equipamento, stock, kit | worker-atlas-warehouse | atlas-warehouse | - |

#### Creative Production (dir-production)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| som, luz, AV, projecao, palco tech, streaming | worker-atlas-av | atlas-av | Creative Production Squad |
| cenografia, palco design, set, truss, rigging | worker-atlas-staging | atlas-staging | - |
| decoracao, tema, flores, ambiance, centros mesa | worker-atlas-decor | atlas-decor | - |
| entretenimento, banda, DJ, fado, artista, MC | worker-atlas-entertainment | atlas-entertainment | - |
| fotografia, video, drone, photo booth, ANAC | worker-atlas-photo-video | atlas-photo-video | - |

#### Guest Experience (dir-guest-experience)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| convidados, RSVP, guest list, registo, badges | worker-atlas-guest | atlas-guest | Guest Experience Squad |
| seating, mapa lugares, mesas, planta sala | worker-atlas-seating | atlas-seating | - |
| protocolo, VIP, etiqueta, precedencia, dress code | worker-atlas-protocol | atlas-protocol | - |
| tech evento, app, WiFi, check-in, QR code | worker-atlas-tech | atlas-tech | - |
| hibrido, virtual, streaming, zoom, plataforma online | worker-atlas-hybrid | atlas-hybrid | - |

#### Event Business (dir-event-business)

| Capability Keywords | Worker | Skill | Squad Boost |
|---|---|---|---|
| marketing evento, promocao, ticketing, earlybird | worker-atlas-marketing | atlas-marketing | Event Business Squad |
| sponsor, patrocinio, sponsorship deck, parceiros | worker-atlas-sponsor | atlas-sponsor | - |
| CRM evento, follow-up, retencao, attendee | worker-atlas-crm | atlas-crm | - |
| risco evento, contingencia, seguranca, emergencia | worker-atlas-risk | atlas-risk | Risk & Compliance Squad |
| licencas, IGAC, camara, SCIE, HACCP, alvara | worker-atlas-compliance | atlas-compliance | Risk & Compliance Squad |
| sustentabilidade, green event, ISO 20121, carbono | worker-atlas-sustainability | atlas-sustainability | - |

#### ATLAS Pipelines (pre-composed)

| Pipeline | Trigger | Skills Chain |
|---|---|---|
| full-event | "planear evento completo" | briefing → venue + budget → timeline + staff → catering + decor + av → checklist → marketing → post-event |
| corporate-conference | "conferencia corporate" | briefing → venue → av + tech + hybrid → guest + seating → sponsor → marketing → checklist → post-event |
| wedding-gala | "casamento" ou "gala" | briefing → venue → decor + entertainment + catering → guest + seating + protocol → photo-video → checklist → post-event |
| festival-outdoor | "festival" ou "evento outdoor" | briefing → venue → compliance + risk → av + staging → entertainment → transport + staff → marketing → checklist |
| quick-event-audit | "auditar evento existente" | checklist → risk → compliance → budget → post-event |

### LUCAS Division — SaaS Accounting

| Capability Keywords | Routing |
|---|---|
| contabilidade, accounting, portuguese tax | Project context: LUCAS/LUSOconta |
| ai agents, multi-agent, saas platform | Project context: LUCAS + orchestrator |
| iva, irs, irc, at portal, efatura | Project context: LUCAS accounting domain |

**LUCAS routing note:** LUCAS doesn't have its own skill set yet — it operates through DARIO's technical + financial workers with LUCAS project context loaded. Cross-reference agent-memory `project_lucas_lusoconta.md`.

## Squad Boost Protocol

When a task is complex enough to benefit from squad activation:

1. **Detect complexity signals:**
   - Task description mentions multiple dimensions
   - Priority is `critical`
   - Multiple capabilities needed simultaneously
   - User explicitly requests "deep analysis"

2. **Select squad(s)** from the routing table (max 2 squads per task)

3. **Compose squad prompt:**
   ```
   Agent({
     subagent_type: "dario-v2-digital-ceo",
     prompt: "Activate <Squad Name>. Analyze <target> focusing on <squad-specific dimensions>. 
              Task context: <task description>. 
              Deliver: <specific outputs expected>."
   })
   ```

4. **Merge squad output** into task completion comment

## Cross-Division Coordination

When a task spans DARIO + DIVA (e.g., "website for architecture studio"):

```
1. CEO decomposes into division-specific subtasks:
   ├── DARIO subtask: Website design, SEO, copy
   └── DIVA subtask: Portfolio content, project descriptions, material specs

2. Each subtask dispatched to its division's director

3. Directors coordinate via parent task:
   ├── Shared artifact: client brief (both divisions read)
   ├── Handoff point: DIVA delivers content → DARIO integrates
   └── Sync point: Both done → CEO synthesizes

4. Final deliverable merges both divisions' outputs
```

## Dispatch Report

After routing all tasks, generate:

```markdown
## Dispatch Report — <Project>

### Routing Decisions
| Task | Assigned To | Skill | Squad | Division | Wave |
|---|---|---|---|---|---|
| PROJ-001 | worker-brand | dario-brand | Brand Squad | DARIO | 1 |
| PROJ-002 | worker-seo-audit | seo-audit | - | DARIO | 1 |
| PROJ-003 | worker-diva-budget | diva-budget | - | DIVA | 1 |
| PROJ-004 | worker-sales-letter | dario-sales-letter | Copy Squad | DARIO | 2 |

### Execution Plan
- **Wave 1:** PROJ-001 + PROJ-002 + PROJ-003 (parallel, independent)
- **Wave 2:** PROJ-004 (depends on PROJ-001)

### Escalations
- None (all tasks matched to workers)

### Budget Estimate
- Total estimated tokens: ~25,000
- By division: DARIO 18,000 | DIVA 7,000
```

## Taskboard Integration (Bidirectional)

Dispatch reads FROM and writes TO the taskboard. This is the link between routing decisions and persistent task state.

### READ: Unassigned Tasks

```python
def get_dispatchable_tasks():
    """Read taskboard for tasks needing assignment."""
    tasks = read_all_yamls("~/.claude/orchestrator/tasks/active/")
    return [t for t in tasks 
            if t.status in ["todo", "backlog"] 
            and t.assignee is None
            and all_deps_done(t)]
```

### WRITE: Assignment Results

After routing a task to a worker:
```python
def write_assignment(task, worker):
    """Write dispatch result back to taskboard."""
    task.assignee = worker.id
    task.assigned_by = "dario-dispatch"
    task.status = "todo"  # Ready for execution
    task.updated_at = now()
    write_yaml(f"~/.claude/orchestrator/tasks/active/{task.id}.yaml", task)
    
    # Audit log
    append_audit({
        "timestamp": now(),
        "actor": "dario-dispatch",
        "action": "task_assigned",
        "entity_id": task.id,
        "details": f"Dispatched to {worker.id} (skill: {worker.skill})"
    })
```

### CREATE: Cross-Division Subtasks

When dispatch detects a cross-division task, it CREATES subtasks in the taskboard:

```python
def create_subtasks(parent_task, subtask_specs):
    """Create subtasks for cross-division work."""
    for i, spec in enumerate(subtask_specs):
        subtask = {
            "id": f"{parent_task.id}-{chr(65+i)}",  # PROJ-001-A, PROJ-001-B
            "title": spec.title,
            "description": spec.description,
            "project": parent_task.project,
            "status": "todo",
            "priority": parent_task.priority,
            "parent": parent_task.id,
            "depends_on": spec.depends_on or [],
            "blocks": [],
            "execution_policy": spec.policy or parent_task.execution_policy,
            "skill": spec.skill,
            "division": spec.division,
            "revision_max_loops": 3,
            "blocked_reason": None,
            "watchers": parent_task.watchers or [],
        }
        write_yaml(f"~/.claude/orchestrator/tasks/active/{subtask['id']}.yaml", subtask)
    
    # Update parent
    parent_task.children = [f"{parent_task.id}-{chr(65+i)}" for i in range(len(subtask_specs))]
    write_yaml(f"~/.claude/orchestrator/tasks/active/{parent_task.id}.yaml", parent_task)
```

### Batch Dispatch

Process all unassigned tasks in one pass:

```python
def batch_dispatch():
    """Dispatch all unassigned tasks. Called by autopilot/heartbeat."""
    tasks = get_dispatchable_tasks()
    results = {"assigned": [], "queued": [], "escalated": []}
    
    for task in sorted(tasks, key=lambda t: t.priority_rank):
        worker = find_best_executor(task)
        if worker:
            write_assignment(task, worker)
            results["assigned"].append((task.id, worker.id))
        elif is_cross_division(task):
            create_subtasks(task, decompose_cross_division(task))
            results["escalated"].append((task.id, "decomposed"))
        else:
            results["queued"].append(task.id)
    
    return results
```

## SLA Timeouts per Execution Policy

Dispatch records expected SLA at assignment time:

| Execution Policy | SLA Timeout | Action on Timeout |
|---|---|---|
| `critical` | 1 hour | Auto-escalate to CEO + notify watchers |
| `client_facing` | 4 hours | Flag as stale + notify director |
| `financial` | 2 hours | Auto-escalate to CEO + block until reviewed |
| `default` | 8 hours | Flag as stale in next heartbeat |

When assigning a task, record the SLA deadline:
```python
task.sla_deadline = now() + sla_duration[task.execution_policy]
```
Heartbeat checks `sla_deadline` against current time during stale detection.

## Auto-Playbook Recommendation

When dispatch receives the **first task** in a new project, it detects the domain and recommends a pre-built skill chain (playbook) for automatic decomposition.

### Domain Detection Algorithm

Scan task + project keywords against known patterns:

```python
DOMAIN_PATTERNS = {
    "restaurant":    ["restaurant", "restaurante", "menu", "reserva", "chef"],
    "agency":        ["agency", "agencia", "servicos digitais", "web agency"],
    "ecommerce":     ["ecommerce", "loja online", "woocommerce", "produtos", "checkout"],
    "saas":          ["saas", "subscription", "mrr", "churn", "software"],
    "architecture":  ["architecture", "arquitectura", "remodelacao", "obra", "planta"],  # → DIVA
    "events":       ["evento", "event", "conferencia", "gala", "casamento", "festival", "catering", "venue", "logistics"],  # → ATLAS
}

def detect_domain(project_keywords):
    scores = {}
    for domain, patterns in DOMAIN_PATTERNS.items():
        hits = sum(1 for kw in project_keywords if kw.lower() in patterns)
        if hits > 0:
            scores[domain] = hits
    if scores:
        return max(scores, key=scores.get)
    return "custom"  # fallback → manual decomposition
```

### Playbook Loading

```python
def recommend_playbook(project_keywords):
    domain = detect_domain(project_keywords)
    playbooks = load_yaml("~/.claude/orchestrator/quality/skill-metrics.yaml")["domain_playbooks"]
    if domain in playbooks:
        playbook = playbooks[domain]
        LOG f"PLAYBOOK DETECTED: {domain} — {len(playbook['optimal_skill_chain'])} skills"
        return playbook
    return None
```

### Auto-Decompose from Playbook

When a playbook is found, auto-create tasks on the taskboard:

```python
def auto_decompose(project, playbook):
    tasks = []
    for step in playbook["optimal_skill_chain"]:
        deps = [t.id for t in tasks if t.order < step["order"] and not step["parallel"]]
        task = create_task(
            project=project,
            skill=step["skill"],
            order=step["order"],
            parallel=step["parallel"],
            depends_on=deps
        )
        tasks.append(task)
    LOG f"AUTO-DECOMPOSED: {project} → {len(tasks)} tasks from {playbook['domain']} playbook"
    return tasks
```

### Playbook Override

User can always override the auto-detection:

| User says | Behavior |
|---|---|
| "use restaurant playbook" | Force specific playbook regardless of keywords |
| "custom decomposition" | Skip playbook, use manual task-by-task decomposition |
| "adapt restaurant playbook + add seo-technical" | Load playbook + append custom skills to the chain |

Override is applied **before** `auto_decompose` runs — dispatch checks for explicit user intent first, keyword detection second.

### Learning Loop

After project completes, compare actual execution vs playbook prediction:

```python
def playbook_feedback(project, playbook):
    actual_chain = get_completed_skill_chain(project)  # what actually ran
    predicted_chain = playbook["optimal_skill_chain"]   # what playbook suggested
    project_score = get_project_avg_score(project)      # quality score

    diff = compare_chains(actual_chain, predicted_chain)
    if diff["reordered"] or diff["added_skills"] or diff["skipped_skills"]:
        suggestion = {
            "domain": playbook["domain"],
            "project": project,
            "score": project_score,
            "changes": diff,
            "recommendation": "update_playbook" if project_score > playbook["avg_score"] else "keep"
        }
        append_to("~/.claude/orchestrator/quality/playbook-feedback.yaml", suggestion)
        LOG f"PLAYBOOK FEEDBACK: {playbook['domain']} — score {project_score} vs avg {playbook['avg_score']}"
```

Feedback is consumed by `lucas-analytics` to propose playbook updates when enough data accumulates (min 3 projects per domain).

## Implementation: dispatch_engine.py

The routing algorithm above is implemented as a deterministic Python engine at `~/.claude/orchestrator/dispatch_engine.py`. This is the **single source of truth** for dispatch decisions.

### CLI Usage

```bash
# Dispatch all unassigned tasks (default)
python ~/.claude/orchestrator/dispatch_engine.py

# Dispatch a specific task
python ~/.claude/orchestrator/dispatch_engine.py --task MNB-002

# Preview routing without assigning
python ~/.claude/orchestrator/dispatch_engine.py --dry-run

# Show all worker availability
python ~/.claude/orchestrator/dispatch_engine.py --status

# Explain WHY a routing decision was made
python ~/.claude/orchestrator/dispatch_engine.py --explain MNB-002

# Machine-readable output for autopilot/heartbeat integration
python ~/.claude/orchestrator/dispatch_engine.py --json
```

### Integration Points

| Caller | How it invokes dispatch | When |
|---|---|---|
| `lucas-autopilot` | `python dispatch_engine.py --json` | Step 4 of every pulse |
| `lucas-heartbeat` | `python dispatch_engine.py --json` | Step 4 of every heartbeat cycle |
| `dario-orchestrator` | `python dispatch_engine.py --task {id}` | After decomposing a task into subtasks |
| User (manual) | `python dispatch_engine.py --dry-run` | When verifying routing before committing |

### What it does atomically

1. Reads `company.yaml` → builds worker indexes
2. Reads all `tasks/active/*.yaml` → calculates workload per worker
3. For each unassigned todo task:
   - Infers skill from title/description keywords
   - Maps skill → primary worker
   - Checks availability (max 1 in_progress per worker)
   - Falls back to sibling workers with capability overlap
   - Escalates to director if all siblings busy
   - Queues if no one available
4. Writes `assignee`, `assigned_at`, `dispatch_reason` to task YAML
5. Logs decision chain to `audit/dispatch_{date}.log`

### Exit Codes

- `0` = success (dispatched or nothing to dispatch)
- `1` = error (missing files, parse failure)
- `2` = all workers busy (tasks queued for next pulse)

## Red Flags

- Never assign a task outside the worker's declared capabilities
- Never run more than 3 parallel workers (cost control)
- Never dispatch without checking dependencies first
- Never ignore division boundaries — use cross-division protocol
- If no worker matches, escalate to director, don't force-fit
- If LUCAS tasks come in, always load LUCAS project context first
- Squad boost is optional — don't activate squads for simple tasks (cost waste)
- **Never assign to a busy worker** — check workload first (Step 2.5)
- **Always write back to taskboard** — dispatch without persistence is lost work

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Skill chain detection é executado ANTES de qualquer routing individual
- [ ] Keywords extraídas do pedido são comparadas contra `trigger_keywords` em `skill_chains.yaml` antes do Step 1
- [ ] Se chain match encontrado, output indica explicitamente qual chain foi ativada (ex: `brand_to_market`, `seo_full_pipeline`)
- [ ] Se sem match, output confirma "no chain match → routing individual" antes de prosseguir
- [ ] Priority order documentada: Chain > Composite Mode > Individual Skill

❌ NOT delivery-ready: "Atribuí a task ao worker disponível."
✅ Delivery-ready: "Sem match em skill_chains.yaml (keywords: 'copy landing page' — sem trigger keyword de chain). Routing individual iniciado → Step 1."

---

### Gate 2 — Capability matching usa dados reais de `company.yaml`
- [ ] Worker encontrado é referenciado pelo `id` exacto de `company.yaml` (ex: `ux-01`, `seo-02`), não por nome genérico
- [ ] `required_capabilities` da task intersectam com `capabilities[]` do worker atribuído, listadas explicitamente
- [ ] Workload check executado: número de tasks `in_progress` do worker indicado no output
- [ ] Sort criteria documentado quando há múltiplos candidatos (overlap count → workload → division match)

❌ NOT delivery-ready: "O melhor worker para SEO foi selecionado com base nas suas capacidades."
✅ Delivery-ready: "Candidatos: `seo-02` (overlap: 3/3, load: 0 tasks), `content-01` (overlap: 2/3, load: 1 task). Atribuído: `seo-02` (max overlap + disponível)."

---

### Gate 3 — Workload awareness aplicado com limites correctos por role
- [ ] Worker com status `in_progress` NÃO é atribuído sem fallback logic explícita
- [ ] Fallback hierarchy documentada quando primary busy: sibling → director → queue
- [ ] Limites respeitados e declarados: Worker max 1 `in_progress`, Director max 2, VP/CEO sem limite de execução
- [ ] Tarefas em queue têm log format correcto: `QUEUED: {task.id} — {worker.id} busy, no fallback available`

❌ NOT delivery-ready: "Worker estava ocupado por isso foi para outro."
✅ Delivery-ready: "`copy-01` tem 1 task `in_progress` (task-047). Fallback: `copy-02` (mesmo director `dir-content`, overlap 2/3, load: 0). LOG: FALLBACK: task-051 → copy-02 (primary copy-01 busy)."

---

### Gate 4 — Division routing correcto e adapter identificado
- [ ] Domain da task mapeado à division correcta (DARIO/DIVA/LUCAS) segundo tabela Step 3
- [ ] Adapter explícito indicado no output (ex: `dario-v2-digital-ceo`, `diva-v1-design-architect`)
- [ ] Tasks cross-division identificadas e modo multi-agent parallel declarado
- [ ] Para LUCAS tasks, contexto LUCAS explicitamente passado ao adapter `dario-v2-digital-ceo`

❌ NOT delivery-ready: "Task de SEO atribuída ao departamento digital."
✅ Delivery-ready: "Domain: SEO/web → Division: DARIO → Adapter: `dario-v2-digital-ceo`. Worker: `seo-02`. Task cross-division? Não."

---

### Gate 5 — Escalation chain seguida e documentada quando necessário
- [ ] Quando nenhum worker match, escalation chain documentada passo-a-passo: Worker → Director → VP → CEO
- [ ] Cada nível com decisão explícita (accept/delegate/escalate) registada
- [ ] Output final indica qual nível aceitou a task e porquê (capacidade + disponibilidade)
- [ ] Tasks sem executor possível terminam em queue com log, não em silêncio

❌ NOT delivery-ready: "Nenhum worker disponível, escalado para cima."
✅ Delivery-ready: "Escalation: `seo-02` busy → `dir-growth` (director, capability overlap: sim, load: 1/2 — aceita). LOG: ESCALATE: task-053 → dir-growth (all workers busy)."

---

### Gate 6 — Output usa CLIENT NAME + dados REAIS, sem angle-brackets placeholder
- [ ] Nenhum `<worker_id>`, `<task_name>`, `<division>`, `<client>` no output entregue
- [ ] Task ID real (ex: `task-051`) e worker ID real (ex: `seo-02`) presentes
- [ ] Client context identificável (ex: Cuidai, Atrium, LUSOconta) associado à task se relevante
- [ ] Routing decision é rastreável: dados de input → lógica aplicada → output concreto

❌ NOT delivery-ready: "Task `<task_id>` atribuída a `<worker>` da divisão `<division>`."
✅ Delivery-ready: "Task `task-058` (Cuidai — landing page copy) → `copy-01` (DARIO, overlap: copywriting, conversion-copy; load: 0; adapter: `dario-v2-digital-ceo`)."

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output de routing deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmed from `company.yaml`, `skill_chains.yaml`, or active task files
- 🟡 **assumed** — plausible based on dispatch logic but needs cliente/operator confirm pre-delivery
- 🟢 **projection** — estimated routing outcome by design (não verificável até execução real)

Output checklist upfront mostra ao operator exatamente o que é trust-as-is vs. precisa de validação antes de despachar.  
**Honest transparency > inflated dispatch confidence.**

---

❌ NOT delivery-ready:
```
Task atribuída a LUCAS-worker-02 (carga: 1 tarefa ativa). Fallback: DARIO-worker-05. Chain: seo_full_pipeline activada.
```
*Sem labels — operator assume tudo verified; pode despachar para worker errado ou chain inexistente.*

✅ Delivery-ready:
```
- 🔵 Worker primário: LUCAS-worker-02 — lido de company.yaml, status "in_progress" confirmado em tasks/active/
- 🟡 Fallback: DARIO-worker-05 — capabilities com overlap assumido; confirmar se cobre domínio contabilístico antes de activar
- 🟢 Estimativa de conclusão: ~2 pulses — projecção por design, depende de workload em runtime
- 🔵 Chain match: seo_full_pipeline — trigger keyword "SEO audit" confirmado em skill_chains.yaml
- 🟡 Division match: DARIO preferred — assumido por keyword "digital"; validar se task tem componente DIVA antes de despachar
```

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (worker capabilities e division scope validados com operator antes do dispatch)
- [ ] All 🔵 sources cited (company.yaml path, task file IDs, skill_chains.yaml version)
- [ ] All 🟢 projections labeled como tal ao cliente — expectativas de timing são estimates, não SLAs

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## DARIO Dispatch — Routing Report

**Request recebido:** "Preciso de um audit de SEO completo para o Tributario.AI e depois optimizar as páginas"
**Timestamp:** 2025-01-15T09:42Z
**Invoked by:** dario-orchestrator (Phase 3 — Dispatch)

---

### Step 0 — Skill Chain Check

Keywords extraídas: `audit`, `SEO`, `optimizar`, `páginas`
Match check vs skill_chains.yaml:
- `brand_to_market` → trigger: brand, identity, launch → ❌
- `audit_to_fix` → trigger: audit, fix, optimizar, SEO → ✅ MATCH

**→ CHAIN ACTIVATED: `audit_to_fix`**
Sequência auto-executada:
  1. `dario-seo-audit` → 2. `dario-seo-optimizer` → 3. `dario-content-writer`
Routing individual: não necessário. Chain gestiona sequência.

---

### Step 0b — Override request (task manual sem chain)

Request paralelo do mesmo cliente: "Cria copy para anúncio Google Ads para o Tributario.AI"
Keywords: `copy`, `anúncio`, `Google Ads`
Chain check: `brand_to_ads` → trigger: brand, ads, copy, campanha → ❌ (sem 'brand' keyword)
→ Sem chain match. Routing individual iniciado.

---

### Step 1 — Parse Task Requirements

- **Domain keywords:** copywriting, paid ads, Google Ads, PPC
- **Skill reference:** `dario-ads-copy` (inferido)
- **Division:** DARIO (digital marketing)
- **Complexity:** Single skill
- **Policy:** standard execution

---

### Step 2 — Capability Matching

Workers carregados de company.yaml (secção `workers:`):

| Worker ID   | Capabilities                          | Load (active tasks) |
|-------------|---------------------------------------|---------------------|
| copy-01     | copywriting, conversion-copy, ads-copy| 0 in_progress       |
| copy-02     | copywriting, content, blog            | 1 in_progress       |
| ads-01      | google-ads, meta-ads, ppc             | 0 in_progress       |

Task required_capabilities: `copywriting`, `ads-copy`

Candidates:
- `copy-01`: overlap 2/2 (copywriting ✅, ads-copy ✅), load: 0 → **score: A**
- `ads-01`: overlap 1/2 (ads-copy ✅, copywriting ❌), load: 0 → score: B
- `copy-02`: overlap 1/2 (copywriting ✅, ads-copy ❌), load: 1 → score: C

Sort: overlap > load > division match
→ **Best match: `copy-01`**

---

### Step 2.5 — Workload Check: copy-01

Active tasks para copy-01:
- task-044: status `done` ✅
- task-049: status `in_review` (não bloqueia — não é `in_progress`)

`is_available(copy-01)` → **TRUE** (0 tasks `in_progress`)

---

### Step 3 — Division Routing

Domain: copywriting / paid ads → **DARIO**
Adapter: `dario-v2-digital-ceo`
Cross-division? Não (Tributario.AI é cliente DARIO puro — SaaS contabilidade PT, web presence)

---

### Final Dispatch Decision

```
DISPATCH: task-061
  Client:   Tributario.AI
  Task:     Google Ads copy — campanha awareness Q1 2025
  Assignee: copy-01
  Division: DARIO
  Adapter:  dario-v2-digital-ceo
  Skill:    dario-ads-copy
  Reason:   Max capability overlap (2/2), load 0, division match
  Status:   → in_progress
```

LOG: ASSIGNED: task-061 → copy-01 (capabilities: copywriting, ads-copy; load before: 0)
```

---

## Output anti-patterns

- Routing decision sem indicar o `worker.id` exacto de `company.yaml` — nomes genéricos como "o worker de SEO" não são rastreáveis
- Skip do Step 0 (skill chain check) e ir directo para routing individual — viola priority order obrigatória
- Workload check omitido ou assumido disponível sem verificar tasks `in_progress` no directório `active/`
- Escalation documentada como "escalei para o manager" sem indicar qual nível aceitou, com que capacidade, e com que load
- Cross-division tasks atribuídas a uma só divisão sem declarar modo multi-agent parallel e adapters de ambas
- Output com `<placeholders>` de angle-bracket entregue ao cliente — especialmente `<task_id>`, `<worker>`, `<client_name>`
- LOG entries ausentes para FALLBACK e QUEUED — sem log não há rastreabilidade de decisões de routing
- Capability intersection declarada sem listar quais capabilities específicas fazem overlap (ex: apenas "match encontrado")
- Division LUCAS tratada sem passar contexto LUCAS ao adapter `dario-v2-digital-ceo` — resulta em output fora de contexto
- Chain activada mas sub-skills da sequência não listadas explicitamente — cliente não sabe o que vai ser executado
