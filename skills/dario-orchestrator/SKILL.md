---
name: dario-orchestrator
description: "Paperclip-inspired control plane for the DARIO + DIVA ecosystem. Orchestrates agents, skills, squads, and services using heartbeats, atomic task checkout, execution policies, and budget controls. Triggers on: 'orchestrate', 'planeia', 'decompoe', 'coordena', 'delega', 'orquestra', 'paperclip mode', 'control plane', 'quem faz o que', 'organiza o trabalho'."
license: MIT
---

# DARIO Orchestrator — Paperclip-Inspired Control Plane

The central nervous system of the DARIO + DIVA ecosystem. This skill transforms ad-hoc skill invocation into structured, auditable, budget-aware orchestration using patterns from Paperclip AI.

## Core Principles

1. **Orchestration, not execution** — The orchestrator coordinates; workers execute
2. **Discrete heartbeats** — Work happens in bounded execution windows, not continuous loops
3. **Atomic task checkout** — One agent owns a task at a time; no duplicate work
4. **Execution policies** — Quality gates (comment, review, approval) enforced at runtime
5. **Transparency** — Every action logged to audit trail; every delegation explained
6. **Budget awareness** — Token spend tracked per project and agent

## When to activate

- User brings a complex, multi-step project (not a single tactical task)
- User says "orchestrate", "planeia", "decompoe", "coordena", "delega", "orquestra"
- User wants to understand or control how work flows across agents
- User asks "quem faz o que" or "organiza o trabalho"
- Start of any ambitious initiative spanning multiple skills/squads
- When the user explicitly invokes `/dario-orchestrator`

Do NOT activate when:
- Single tactical task (just invoke the specific skill directly)
- Quick question or status check
- User already knows exactly which skill to run

## Architecture Overview

```
User Request
    |
    v
[DARIO CEO — Orchestrator]
    |
    ├── 1. UNDERSTAND — Parse intent, gather context
    ├── 2. DECOMPOSE — Break into atomic tasks
    ├── 3. DISPATCH — Route each task to right agent/skill
    ├── 4. EXECUTE — Workers run in heartbeat windows
    ├── 5. REVIEW — Execution policies enforced
    ├── 6. SYNTHESIZE — Combine outputs into deliverable
    └── 7. AUDIT — Log everything, update budget
```

## Workflow

### Phase 0: VALIDATE (Pre-flight Checks)

Before any decomposition or execution, run these validation checks:

**1. Circular Dependency Detection:**
```
For each task in the project:
  visited = set()
  stack = [task]
  while stack:
    current = stack.pop()
    if current in visited:
      ABORT — circular dependency detected: {chain}
    visited.add(current)
    stack.extend(current.depends_on)
```
If circular dependency found → report to user with the full cycle chain. DO NOT proceed.

**2. Worker Availability Check:**
```
For each task to dispatch:
  worker = lookup(task.skill) in company.yaml workers section
  active_tasks = count tasks in active/ where assignee == worker AND status == "in_progress"
  if active_tasks > 0:
    FLAG — worker busy. Queue task or find fallback.
```

**3. Budget Pre-check:**
Read `~/.claude/orchestrator/budgets/YYYY-MM.yaml`:
- If `percentage >= 95`: **ABORT** — budget exceeded. Inform user.
- If `percentage >= 80`: **WARN** — limit to 1 parallel worker (not 3).
- If budget file doesn't exist: **CREATE** it with defaults.

**4. File Initialization:**
Ensure all required paths exist before execution:
```
~/.claude/orchestrator/tasks/active/     — create if missing
~/.claude/orchestrator/tasks/done/       — create if missing
~/.claude/orchestrator/tasks/templates/  — create if missing
~/.claude/orchestrator/audit/            — create if missing
~/.claude/orchestrator/budgets/          — create if missing
~/.claude/orchestrator/quality/          — create if missing
```

**5. Stale Task Recovery:**
Scan `tasks/active/` for tasks stuck in `in_progress` for >24h:
- If found: set status → `blocked`, set `blocked_reason: "stale — no update for >24h"`
- Add to report for user visibility

### Phase 1: UNDERSTAND

1. **Parse the user request** — What is the end goal? What's the scope?
2. **RAG consult** (mandatory):
   ```
   mcp__dario-rag__search_kb(query: "<extracted keywords>", collection: "dario", limit: 5)
   ```
3. **Check agent memory** — Is there existing context for this client/project?
4. **Load company config** — Read `~/.claude/orchestrator/company.yaml` to understand available agents
5. **Identify constraints** — Budget, timeline, dependencies, blockers

Output: **Mission Brief** — A structured understanding of what needs to happen.

### Phase 2: DECOMPOSE (Task Breakdown)

Break the mission into **atomic tasks** following Paperclip's issue model:

```yaml
task:
  id: "PROJ-001"
  title: "Descriptive action title"
  description: "What needs to be done and why"
  status: "todo"              # backlog | todo | in_progress | in_review | done | blocked
  priority: "high"            # critical | high | medium | low
  assignee: null              # Set during dispatch
  parent: null                # Parent task ID (for hierarchy)
  project: "client-slug"
  execution_policy: "default" # default | critical | client_facing | financial
  estimated_tokens: 5000      # Rough token budget for this task
  depends_on: []              # Task IDs that must complete first
  created: "2026-04-26T19:44:00Z"
```

**Decomposition rules:**
- Each task maps to ONE skill or squad invocation
- Tasks must have clear success criteria
- Dependencies must be explicit (don't assume ordering)
- Parent tasks group related work; only leaf tasks are executable
- CRITICO items get `execution_policy: "critical"` automatically
- Client deliverables get `execution_policy: "client_facing"`
- **Every task MUST include schema v2 fields:** `revision_max_loops` (from execution_policy), `blocked_reason: null`, `watchers: []`
- **Every task MUST set `sla_deadline`** based on execution_policy.sla_hours from company.yaml (critical: 1h, client_facing: 4h, financial: 2h, default: 8h). If task is created without going through dispatch, orchestrator sets this directly.

**Save each task** to `~/.claude/orchestrator/tasks/active/PROJ-NNN.yaml`

### Phase 3: DISPATCH (Intelligent Routing)

For each task, determine the best executor:

1. **Read company.yaml** — Match task capabilities to agent capabilities
2. **Apply routing rules:**

| Task Domain | Primary Agent | Fallback | Parallel Squad |
|---|---|---|---|
| Brand/positioning | worker-brand | dir-marketing | Brand Squad |
| Offer/pricing | worker-offer | dir-marketing | Hormozi Squad |
| Copy/sales letter | worker-sales-letter | dir-marketing | Copy Squad |
| Paid traffic | worker-ads | dir-marketing | Traffic Masters |
| Funnel design | worker-funnel | dir-marketing | Sales Squad |
| WordPress audit | worker-wp-audit | dir-technical | Cybersecurity Squad |
| WooCommerce | worker-woo-audit | dir-technical | - |
| Performance | worker-cwv-fix | dir-technical | - |
| Security | worker-pentest | dir-technical | Cybersecurity Squad |
| Full SEO audit | worker-seo-audit | dir-seo | Data Squad |
| Technical SEO | worker-seo-technical | dir-seo | - |
| Content SEO | worker-seo-content | dir-seo | - |
| Local SEO | worker-seo-local | dir-seo | - |
| AI/GEO | worker-seo-geo | dir-seo | - |
| Schema | worker-seo-schema | dir-seo | - |
| Keywords | worker-kw-cluster | dir-seo | - |
| Financial model | worker-financial-model | dir-finance | CFO Squad |
| Pricing | worker-pricing-calculator | dir-finance | - |
| SaaS metrics | worker-saas-metrics | dir-finance | - |
| Client onboard | worker-client-onboard | dir-client-success | - |
| Diagnostic | worker-diagnose | dir-client-success | Advisory Board |
| Interior design | worker-diva-moodboard | dir-design | Interior Design Squad |
| Materials | worker-diva-materials | dir-design | - |
| Floor plan | worker-diva-floor-plan | dir-design | Architecture Masters |
| Renders | worker-diva-render | dir-design | - |
| Budget (constr.) | worker-diva-budget | dir-construction | Budget Squad |
| Timeline | worker-diva-timeline | dir-construction | - |
| Inspection | worker-diva-inspection | dir-construction | - |
| Contract | worker-diva-contract | dir-construction | - |
| Licensing | worker-diva-licensing | dir-regulatory | Regulation Squad |
| Energy cert | worker-diva-energy | dir-regulatory | - |

3. **Assign task** (atomic checkout):
   - Set `assignee` to the chosen worker ID
   - Set `status` to `todo`
   - Set `checked_out_at` timestamp
   - Only ONE agent can own a task at a time

4. **Plan parallelism:**
   - Independent tasks run simultaneously via Agent tool
   - Maximum 3 parallel workers per heartbeat (cost + context)
   - Tasks with `depends_on` wait for predecessors to reach `done`

### Phase 4: EXECUTE (Heartbeat Windows)

Each execution is a **discrete heartbeat** — a bounded work session:

```
Heartbeat Execution Flow:
1. Check identity (which agent am I?)
2. Review assigned tasks (what's on my plate?)
3. Pick next task (highest priority, no blockers)
4. Atomic checkout (claim it)
5. Execute via skill invocation
6. Post completion comment (mandatory)
7. Update task status
8. Return control to orchestrator
```

**Execution via Agent tool:**
```python
# Single worker execution
Agent({
  description: "Execute task PROJ-001: <title>",
  subagent_type: "dario-v2-digital-ceo",  # or "diva-v1-design-architect" for DIVA tasks
  prompt: """
  You are worker <worker-id> executing task PROJ-001.
  
  TASK: <title>
  DESCRIPTION: <description>
  SKILL TO USE: /dario-<skill-name>
  CONTEXT: <relevant context from RAG + memory>
  SUCCESS CRITERIA: <what "done" looks like>
  EXECUTION POLICY: <policy name>
  
  Execute this task using the specified skill.
  When done, provide:
  1. A substantive completion comment
  2. The deliverable/output
  3. Any blockers or follow-up tasks discovered
  """
})
```

**Parallel execution (up to 3):**
```python
# Launch independent tasks simultaneously
Agent({ description: "PROJ-001: Brand audit", ... })  # In parallel
Agent({ description: "PROJ-002: SEO audit", ... })    # In parallel
Agent({ description: "PROJ-003: CRO audit", ... })    # In parallel
```

**Coalescing rules:**
- If a worker is already processing a similar task, coalesce (merge) instead of duplicating
- If a heartbeat is running, queue new work for the next window
- Cooldown: minimum 2 minutes between heartbeats for the same worker

### Phase 4.5: ERROR RECOVERY

When a task execution fails (Agent tool timeout, error, or empty output):

**Retry Protocol (exponential backoff):**
```
max_retries = 3
for attempt in 1..max_retries:
  wait = min(30 * (2 ^ attempt), 270)  # 60s, 120s, 240s — stay in cache window
  execute(task)
  if success:
    break
  if attempt == max_retries:
    ESCALATE to dead-letter
```

**Dead-Letter Queue:**
Tasks that fail after all retries:
1. Set status → `blocked`
2. Set `blocked_reason: "execution_failed — {error_summary}. Retried {N} times."`
3. Add note with full error context
4. Move to dead-letter list in report
5. Continue with other tasks (don't block the wave)

**Mid-Execution Crash Recovery:**
If the session ends unexpectedly (compaction, timeout):
1. On next heartbeat, scan `tasks/active/` for tasks with:
   - `status: "in_progress"` AND `checked_out_at` older than SLA timeout
2. Apply SLA timeouts per execution policy:
   - `critical` → 1h
   - `client_facing` → 4h  
   - `default` → 8h
   - `financial` → 2h
3. If past SLA: reset status → `todo`, clear `checked_out_at`, increment `notes[]` with recovery entry
4. Task is now available for re-dispatch

**Idempotency Guard:**
Before executing a task, check:
- Is this task already `done`? → Skip (don't double-execute)
- Is this task `in_progress` by another agent? → Skip (atomic checkout)
- Did this task run in the last 5 minutes? → Skip (prevent rapid re-execution after crash)

### Phase 5: REVIEW (Execution Policies)

After each task completes, enforce the applicable execution policy:

**Layer 1 — Comment (always enforced):**
- Worker MUST post a substantive completion comment
- Comment includes: what was done, key findings, confidence level
- If missing, task stays `in_progress` and agent is re-prompted

**Layer 2 — Review (when policy requires it):**
- Director-level agent reviews the output
- Can: approve (→ done), request revision (→ back to worker), escalate (→ CEO)
- Maximum revision loops defined per policy (default: 3)

**Layer 3 — Approval (for critical/financial tasks):**
- CEO or user explicitly approves
- For `critical` policy: user is always asked to approve
- For `financial` policy: user approves budget-impacting decisions
- Use AskUserQuestion tool to get approval

**Status transitions during review:**
```
in_progress → in_review (worker marks as done)
in_review → done (reviewer approves)
in_review → in_progress (reviewer requests revision)
in_review → blocked (reviewer finds external dependency)
```

### Phase 6: SYNTHESIZE (Combine Outputs)

Once all tasks in a project reach `done`:

1. **Gather all task outputs** from the heartbeat results
2. **Combine into a unified deliverable** using the project template
3. **Cross-reference findings** — look for contradictions or synergies across outputs
4. **Apply DARIO prioritization** — CRITICO / IMPORTANTE / OTIMIZACAO
5. **Generate executive summary** with actionable next steps

### Phase 7: AUDIT (Logging & Budget)

**Activity Audit Trail:**
Every mutation is logged to `~/.claude/orchestrator/audit/YYYY-MM-DD.yaml`:

```yaml
- timestamp: "2026-04-26T19:45:00Z"
  actor: "dario-ceo"
  action: "task_created"
  entity_type: "task"
  entity_id: "PROJ-001"
  details: "Created task: Brand positioning audit for Client X"

- timestamp: "2026-04-26T19:46:00Z"
  actor: "dario-ceo"
  action: "task_assigned"
  entity_type: "task"
  entity_id: "PROJ-001"
  details: "Assigned to worker-brand (atomic checkout)"
```

**Budget Tracking — Token Capture Contract:**

Tokens flow from execution to budget in 3 steps:

**Step 1: Capture** — After each Agent tool execution completes:
- Extract token count from the Agent result metadata (if available)
- If metadata unavailable, ESTIMATE based on output length:
  - Short output (<500 chars): ~2,000 tokens
  - Medium output (500-3000 chars): ~5,000 tokens
  - Long output (>3000 chars): ~10,000 tokens
  - With subagent spawning: multiply by 1.5x
- Record `actual_tokens` in the task YAML

**Step 2: Aggregate** — Update `~/.claude/orchestrator/budgets/YYYY-MM.yaml`:
```yaml
month: "2026-04"
total_tokens_used: 125000
limit: 50000000
percentage: 0.25                      # auto-calculated: total / limit * 100
by_project:
  atrium: 45000
  vivenda: 30000
  lucas: 50000
by_skill:                             # track per skill for optimization insights
  dario-brand: 15000
  seo-audit: 35000
  dario-wp-audit: 25000
by_model:                             # track model usage for cost optimization
  opus: 80000
  sonnet: 35000
  haiku: 10000
last_updated: "2026-04-27T08:00:00Z"
alert_80_sent: false
alert_95_sent: false
```

**Step 3: Enforce** — Check thresholds AFTER every budget update:
- If `percentage >= 80` AND `alert_80_sent == false`:
  - Set `alert_80_sent: true`
  - Report to user: "Budget a 80% — limitando a 1 worker paralelo"
  - Reduce max parallel workers from 3 to 1
- If `percentage >= 95` AND `alert_95_sent == false`:
  - Set `alert_95_sent: true`
  - **STOP all execution**. Report: "Budget critico (X%). Execucao pausada."
  - Set all `in_progress` tasks back to `todo`
  - Do NOT proceed until user explicitly raises the limit

**Budget File Initialization:**
If `budgets/YYYY-MM.yaml` doesn't exist at month start, create it:
```yaml
month: "<current month>"
total_tokens_used: 0
limit: 50000000      # from company.yaml company.budget.monthly_limit_tokens
percentage: 0.0
by_project: {}
by_skill: {}
by_model: {}
last_updated: "<now>"
alert_80_sent: false
alert_95_sent: false
```

## Task Templates

### Template: Full Client Audit
```yaml
parent: "AUDIT-000"
children:
  - title: "Diagnostic analysis"
    skill: "dario-diagnose"
    policy: "default"
    priority: "critical"
  - title: "WordPress audit"
    skill: "dario-wp-audit"
    policy: "client_facing"
    depends_on: ["diagnostic"]
  - title: "SEO audit"
    skill: "seo-audit"
    policy: "client_facing"
    depends_on: ["diagnostic"]
  - title: "CRO review"
    squad: "CRO Squad"
    policy: "client_facing"
    depends_on: ["diagnostic"]
  - title: "Synthesize findings"
    skill: "orchestrator"
    policy: "critical"
    depends_on: ["wp-audit", "seo-audit", "cro-review"]
  - title: "Save to Obsidian + RAG"
    skill: "dario-obsidian-save"
    depends_on: ["synthesize"]
```

### Template: Brand + Offer + Copy Pipeline
```yaml
parent: "BRAND-000"
children:
  - title: "Brand positioning workshop"
    skill: "dario-brand"
    policy: "client_facing"
    priority: "high"
  - title: "Grand Slam Offer creation"
    skill: "dario-offer"
    policy: "client_facing"
    depends_on: ["brand-positioning"]
  - title: "Sales letter"
    skill: "dario-sales-letter"
    policy: "client_facing"
    depends_on: ["offer-creation"]
  - title: "Ads blueprint"
    skill: "dario-ads-blueprint"
    policy: "default"
    depends_on: ["sales-letter"]
  - title: "Email sequences"
    skill: "dario-email-seq"
    policy: "default"
    depends_on: ["offer-creation"]
```

### Template: Architecture Project (DIVA)
```yaml
parent: "ARCH-000"
children:
  - title: "Client briefing"
    skill: "diva-briefing"
    policy: "default"
    priority: "critical"
  - title: "Space diagnostic"
    skill: "diva-diagnose"
    policy: "default"
    depends_on: ["briefing"]
  - title: "Floor plan analysis"
    skill: "diva-floor-plan"
    policy: "client_facing"
    depends_on: ["diagnostic"]
  - title: "Moodboard creation"
    skill: "diva-moodboard"
    policy: "client_facing"
    depends_on: ["briefing"]
  - title: "Material specification"
    skill: "diva-materials"
    policy: "client_facing"
    depends_on: ["moodboard"]
  - title: "Budget estimation"
    skill: "diva-budget"
    policy: "financial"
    depends_on: ["floor-plan", "materials"]
  - title: "Timeline / Gantt"
    skill: "diva-timeline"
    policy: "client_facing"
    depends_on: ["budget"]
  - title: "Licensing check"
    skill: "diva-licensing"
    policy: "critical"
    depends_on: ["diagnostic"]
  - title: "Project roadmap"
    skill: "diva-roadmap"
    policy: "critical"
    depends_on: ["budget", "timeline", "licensing"]
```

## Orchestrator Commands

When the orchestrator is active, these commands are available:

| Command | Action |
|---|---|
| `status` | Show all active tasks with status, assignee, priority |
| `next` | Pick and execute the next available task |
| `assign <task> to <worker>` | Manually assign a task |
| `block <task> reason <text>` | Mark task as blocked |
| `unblock <task>` | Remove blocker |
| `review <task>` | Trigger review for completed task |
| `approve <task>` | Approve a task pending approval |
| `budget` | Show current budget usage |
| `audit [date]` | Show audit log for date |
| `parallel <task1> <task2> [task3]` | Execute tasks in parallel |
| `template <name> <project>` | Create tasks from a template |
| `escalate <task>` | Escalate task to next level in hierarchy |
| `reassign <task> to <worker>` | Change task assignee |
| `pause` | Pause all active heartbeats |
| `resume` | Resume paused heartbeats |

## Output Template (Orchestration Report)

```markdown
# Orchestration Report — <Project Name>

## Mission
<What was requested and why>

## Task Decomposition
| # | Task | Assignee | Status | Policy | Priority |
|---|---|---|---|---|---|
| 001 | ... | worker-brand | done | client_facing | high |
| 002 | ... | worker-seo-audit | in_progress | client_facing | high |

## Execution Timeline
1. [19:45] Task 001 created, assigned to worker-brand
2. [19:46] Task 001 execution started (heartbeat)
3. [19:52] Task 001 completed, review passed
4. [19:52] Task 002 started (dependency resolved)

## Deliverables
- <list of outputs produced>

## Budget Impact
- Tokens used this session: X
- Project total: Y / Z (budget)

## Next Actions
- <what needs to happen next>

## Blockers
- <any unresolved blockers>
```

## Integration with Existing Systems

### RAG Engine
- ALL tasks consult RAG before execution (mandatory DARIO protocol)
- Task outputs are ingested into RAG via `dario-rag-ingest`
- RAG collection: `orchestrator` for task metadata; project-specific for deliverables

### Agent Memory
- Orchestration state persists in `~/.claude/orchestrator/`
- Project context in `~/.claude/agent-memory/dario-v2-digital-ceo/`
- Cross-session continuity via session hooks (already in place)

### Obsidian
- Final deliverables saved via `dario-obsidian-save` or `diva-obsidian-save`
- Orchestration reports saved to `05 - Claude - IA/Outputs/`
- Audit logs optionally mirrored to `05 - Claude - IA/Decisoes/`

### Hooks
- `SessionStart` — Load active orchestration state
- `PreCompact` — Save orchestration progress
- `PostCompact` — Restore orchestration context
- `Stop` — Archive completed tasks, update budget totals

## Notification Protocol

Events trigger notifications through channels defined in `~/.claude/orchestrator/notifications.yaml`. The orchestrator uses a `notify(event, data)` pattern:

```python
def notify(event_name, data):
    config = load_yaml("~/.claude/orchestrator/notifications.yaml")
    event = config["events"][event_name]
    message = event["template"].format(**data)
    
    for channel in event["channels"]:
        if channel == "pulse_report":
            append_to_pulse(message, event["severity"])
        elif channel == "audit_log":
            append_audit({"timestamp": now(), "actor": "orchestrator", "action": event_name, "details": message})
        elif channel == "obsidian_alert" and event["severity"] == "critical":
            save_obsidian_alert(event_name, message)
        elif channel == "task_note" and "task" in data:
            data["task"].notes.append(f"[{now()}] {message}")
```

**Key events:** `task_completed`, `task_revision`, `task_escalated`, `sla_warning`, `sla_breach`, `budget_warning`, `budget_critical`, `quality_low`, `playbook_detected`, `project_completed`, `health_check_failed`, `stale_task`

**Severity levels:** `info` (pulse only), `warning` (pulse + audit), `critical` (pulse + audit + Obsidian alert note)

## Phase 7.5: SKILL CHAINING (Auto-Sequential Execution)

When a task matches a chain (defined in `~/.claude/orchestrator/skill_chains.yaml`), execute skills **sequentially with automatic output passing** — no CEO intervention between steps.

**How it works:**
```
User: "cria marca completa para restaurante"
Orchestrator detects: chain "brand_to_market"

Step 1: dario-brand → produces: posicionamento, archetype
   ↓ (output passes automatically)
Step 2: dario-naming → receives posicionamento → produces: nome
   ↓
Step 3: dario-offer → receives posicionamento + nome → produces: offer
   ↓
Step 4: dario-sales-letter → receives all above → produces: copy
   ↓
Step 5: dario-email-seq → receives offer + copy → produces: emails

Result: complete package without CEO re-dispatching between steps.
```

**Execution protocol:**
1. Dispatch detects chain trigger keywords
2. First skill receives user context
3. Each subsequent skill receives: user context + previous skill output
4. Quality gate between steps: if score < 70, retry 1x before stopping
5. On complete: merge all outputs + calculate avg score + log chain
6. On failure: deliver partial output (everything completed before failure)

**Available chains:** brand_to_market, brand_to_ads, audit_to_fix, seo_full_pipeline, diva_full_project, client_full_onboard

**Difference from Composite Modes:**
- Composite Modes = parallel (all at once, merge)
- Skill Chains = sequential (each feeds the next, automatic handoff)

**Log codes:**
- `DARIO_CHAIN_START_{name}` — chain activated
- `DARIO_CHAIN_STEP_{n}_{skill}_DONE` — step completed
- `DARIO_CHAIN_COMPLETE_{name}_{score}` — chain finished
- `DARIO_CHAIN_FAIL_{name}_AT_STEP_{n}` — chain failed at step

---

## Phase 8: AUTODIAG (Silent Periodic Audit) — ASIMO Pattern

Inspired by ASIMO's AutoDiag_20 module. The orchestrator runs a silent self-diagnostic at defined intervals WITHOUT producing output unless issues are detected.

**Trigger:** Every 10 task completions OR at the start of each heartbeat pulse.

**Diagnostic Checks:**

```yaml
autodiag_protocol:
  frequency: every_10_tasks_or_pulse_start
  mode: silent  # Only outputs if issues found
  checks:
    - name: coherence_check
      action: "Verify all in_progress tasks still have valid assignees in company.yaml"
      on_fail: "Set task status → blocked, reason: 'assignee not found in hierarchy'"

    - name: orphan_detection
      action: "Find tasks with parent IDs that don't exist"
      on_fail: "Clear parent reference, add note: 'orphaned — parent removed'"

    - name: dependency_integrity
      action: "Verify all depends_on references point to existing tasks"
      on_fail: "Remove broken dep, add note: 'dependency removed — target missing'"

    - name: budget_drift
      action: "Compare actual_tokens sum vs budget YAML total"
      on_fail: "Recalculate and update budget YAML"

    - name: stale_review
      action: "Find tasks in_review for >2x SLA time"
      on_fail: "Auto-approve if score >= auto_approve_threshold, else escalate"

    - name: quality_regression
      action: "Check last 5 task scores — if avg dropped >15 points from baseline"
      on_fail: "Flag quality regression, notify user"
```

**Log codes (structured, append-only):**
```
DARIO_AUTODIAG_OK_{timestamp}        — all checks passed
DARIO_AUTODIAG_WARN_{check}_{id}     — issue found and auto-fixed
DARIO_AUTODIAG_FAIL_{check}_{id}     — issue found, needs manual intervention
```

**Principles (from ASIMO):**
- `append-only` — never delete audit entries, only add
- `most-specific-wins` — if two rules conflict, the more specific one applies
- `silent-mode` — AutoDiag never outputs unless it finds a problem

---

## Phase 9: REACTIVATION PROTOCOL (Context Recovery) — ASIMO Pattern

Inspired by ASIMO's PromptActivation_Master_21. Ensures full system state is restored at session start.

**Trigger:** Start of every new session OR after context compaction.

**Sequence (5 steps, sequential):**

```
Step 1: MEMORY LOAD
  - Read ~/.claude/projects/*/memory/MEMORY.md
  - Identify active project from user's first message or taskboard state
  - Load project-specific memory file

Step 2: RAG HEALTH
  - mcp__dario-rag__kb_health()
  - If DOWN: attempt restart, flag to user
  - If UP: note source count and last ingest

Step 3: TASKBOARD SYNC
  - Scan ~/.claude/orchestrator/tasks/active/*.yaml
  - Count: total, in_progress, blocked, todo
  - Identify next executable task (highest priority, deps resolved)
  - Run stale check (>24h in_progress → block)

Step 4: BUDGET CHECK
  - Read ~/.claude/orchestrator/budgets/YYYY-MM.yaml
  - Report percentage, enforce limits (80%/95%)

Step 5: INTEGRITY SEAL
  - If all 4 steps pass: log DARIO_REACTIVATION_OK_{timestamp}
  - If any step fails: log DARIO_REACTIVATION_DEGRADED_{step}
  - Report status to user in compact format
```

**Output format (only on degraded state):**
```
[DARIO Reactivation] DEGRADED
- RAG: DOWN (attempting restart...)
- Taskboard: 3 stale tasks auto-blocked
- Budget: 67% (OK)
```

**On healthy state:** No output (silent, like ASIMO's principle).

---

## Conflict Resolution — Most-Specific-Wins (ASIMO Pattern)

When multiple skills or agents could handle a task, or when instructions conflict:

**Resolution hierarchy (most specific wins):**
```
1. User explicit instruction (highest priority)
2. Task-level config (skill, assignee specified in YAML)
3. Project-level playbook (if domain detected)
4. Division-level routing (company.yaml dispatch table)
5. Global defaults (lowest priority)
```

**Example:** User says "use seo-technical for this". Project playbook says "use seo-audit". Resolution: User instruction wins (level 1 > level 3).

**Merge policy:** `append-only`
- New instructions don't delete previous ones
- They layer on top with higher specificity
- Previous context remains accessible for reference
- Only user can explicitly revoke a previous instruction

---

## Fallback Protocol (Per-Skill Resilience) — ASIMO Pattern

Every skill invocation must have a defined fallback path:

```yaml
fallback_matrix:
  # If primary skill fails → try fallback → if fallback fails → escalate
  dario-brand:
    fallback: dir-marketing  # Director handles manually
    escalate: dario-ceo
  seo-audit:
    fallback: seo-technical  # Narrower scope but still useful
    escalate: dir-seo
  diva-budget:
    fallback: diva-calc      # Simpler calculator version
    escalate: dir-construction
  dario-wp-audit:
    fallback: seo-technical  # At least do technical checks
    escalate: dir-technical
  DEFAULT:
    fallback: null           # No automatic fallback
    escalate: dario-ceo      # CEO decides
```

**Fallback trigger conditions:**
- Skill execution returns empty output
- Skill execution exceeds SLA timeout
- Skill produces output with quality score < 40
- Agent tool returns error

**Fallback does NOT trigger for:**
- User-cancelled execution
- Budget exceeded (that's a hard stop, not a fallback)
- Circular dependency detected (that's an abort)

---

## Metacognition Protocol (Confidence Signaling) — ASIMO Pattern

Inspired by ASIMO's 3-mode metacognition (INCERTEZA / ALTA_CONFIANCA / EXPLORACAO). Every task output must declare its confidence mode:

```yaml
confidence_modes:
  HIGH_CONFIDENCE:
    signal: "Baseado em dados verificados, RAG confirmado, experiencia anterior"
    output_style: "Assertivo, recomendacoes directas, sem hedging"
    when: "RAG score >0.7 AND similar task completed before AND data available"

  UNCERTAINTY:
    signal: "Dados insuficientes, primeira vez neste contexto, assumptions marcadas"
    output_style: "Explicitar assumptions, marcar como [ASSUMPTION], pedir validacao"
    when: "RAG score <0.5 OR no prior context OR missing data"

  EXPLORATION:
    signal: "Modo criativo/experimental, multiplas opcoes, sem resposta unica correcta"
    output_style: "Apresentar 2-3 alternativas com pros/cons, pedir preferencia"
    when: "Creative task (brand, naming, content) OR user asks 'o que achas?'"
```

**Integration with Quality Scoring:**
- HIGH_CONFIDENCE outputs penalized harder for errors (expected to be right)
- UNCERTAINTY outputs get bonus for flagging assumptions correctly
- EXPLORATION outputs scored on variety and rationale quality

---

## Operational States (DARIO v1.0 Pattern)

The orchestrator is ALWAYS in one of 4 states defined in `~/.claude/orchestrator/operational_states.yaml`:

| State | Max Parallel | Actions Allowed | Trigger |
|---|---|---|---|
| **ACTIVE** | 3 | All | SystemHealth >= 0.85, Budget < 80% |
| **REFLECTIVE_PAUSE** | 1 | Dispatch, Score, Audit | Quality avg < 60, 3+ AutoDiag warnings |
| **GUARDIAN** | 0 | Audit, Report only | Budget >= 95%, Ethical gate fail, Health < 0.50 |
| **EXPANSION** | 1 | Audit, Score, Learn | No pending work, weekly cycle |

**State transitions are logged:** `DARIO_STATE_{from}→{to}_{reason}`

## Ethical Pre-Gate (DARIO v1.0 "Filtro Triplice")

Before EVERY dispatch decision, apply 3 questions:
1. **Clarity:** Is the task clearly defined with unambiguous success criteria?
2. **Freedom:** Does this respect user autonomy and informed consent?
3. **Coherence:** Is this aligned with project objectives and manifesto values?

If ANY answer is `false`: do NOT dispatch. Instead:
- Propose reformulated task that passes all 3 checks
- Log `DARIO_ETHICAL_GATE_FAIL_{question}_{task_id}`
- If repeated failures: enter GUARDIAN state

## Synaptic Weights (Inter-Agent Affinity)

Skills that co-activate frequently with high scores build "synaptic weight" — stored in `~/.claude/orchestrator/synaptic_weights.yaml`.

**Dispatch enhancement:** When a complex task needs 2+ skills:
1. Check affinity graph for highest-weight pairs
2. Prefer proven combinations over untested ones
3. After task completion, update weights:
   - Score >= 80: weight += 0.05
   - Score < 50: weight -= 0.03

## Evolutionary Delta (Meta-Learning)

Track improvement rate: `delta = avg_quality_last_10 - avg_quality_previous_10`
- delta > 0: System improving (ACTIVE state valid)
- delta < -5: Regression detected → trigger REFLECTIVE_PAUSE
- Stored in `~/.claude/orchestrator/quality/evolution.yaml`

## Red Flags

- Never execute a task without checking company.yaml for the right agent
- Never skip the audit log
- Never run more than 3 parallel workers (cost explosion risk)
- Never auto-approve critical or financial tasks (always ask user)
- Never ignore a task's `depends_on` — respect the dependency graph
- Never assign a task to an agent outside its declared capabilities
- If a revision loop exceeds max_loops, escalate to user immediately
- Never delete audit entries (append-only principle)
- Never suppress AutoDiag findings — if it finds a problem, it reports
- Never skip the Reactivation Protocol at session start
- Never override a higher-specificity instruction with a lower one
- Never dispatch when Ethical Pre-Gate fails (clarity/freedom/coherence)
- Never execute in GUARDIAN state without user acknowledgement
- Never bypass the blocklist (operational_states.yaml)

## Why This Skill Exists

The DARIO ecosystem grew to 70+ skills and 18 squads. Without structured orchestration:
- Work was ad-hoc (whoever got called first did the work)
- No task tracking across sessions
- No execution quality gates
- No budget visibility
- No audit trail for client accountability
- Cross-division work (DARIO + DIVA) had no coordination protocol

The Paperclip-inspired orchestrator fixes all of this while preserving everything that already works.

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Mission Brief está estruturado e não é vago

- [ ] O Brief identifica o **end goal concreto** (não "melhorar processos")
- [ ] Constraints explícitas: budget %, timeline, dependências nomeadas
- [ ] RAG consult foi executado com keywords extraídas do pedido real
- [ ] Scope delimitado: o que está IN vs OUT do orchestration run

❌ NOT delivery-ready: "Objetivo: organizar o trabalho do cliente. Sem constraints identificadas."
✅ Delivery-ready: "Mission: migrar infraestrutura LUSOconta para novo stack. Budget: 34% usado (Março 2026). Timeline: 14 dias. Blocker: dependência de PROJ-007 (compliance sign-off pendente Ana Ferreira)."

---

### Gate 2 — Decomposição produz tarefas verdadeiramente atómicas

- [ ] Cada task mapeia a **exatamente 1 skill ou squad** (sem tarefas "multi-skill")
- [ ] Todos os campos schema v2 presentes: `revision_max_loops`, `blocked_reason: null`, `watchers: []`, `sla_deadline`
- [ ] `sla_deadline` calculado a partir de `execution_policy.sla_hours` (critical=1h, client_facing=4h, financial=2h, default=8h)
- [ ] `depends_on` explícito — nenhuma tarefa com ordering implícito
- [ ] `estimated_tokens` preenchido com valor numérico real (não `null`)

❌ NOT delivery-ready: `{ id: "PROJ-003", title: "Fazer relatório e enviar ao cliente", depends_on: [] }`
✅ Delivery-ready: `{ id: "CUIDAI-003", title: "Gerar relatório mensal cuidadores Abril 2026", assignee: "diva-reporting", execution_policy: "client_facing", sla_deadline: "2026-04-27T10:00Z", estimated_tokens: 4200, depends_on: ["CUIDAI-001", "CUIDAI-002"], revision_max_loops: 2, blocked_reason: null, watchers: ["ricardo@cuidai.pt"] }`

---

### Gate 3 — Phase 0 Validation foi executada e documentada

- [ ] Circular dependency check concluído — resultado explícito ("nenhuma dependência circular detectada" ou ciclo reportado)
- [ ] Worker availability verificado para cada assignee em `company.yaml`
- [ ] Budget pre-check executado: ficheiro `~/.claude/orchestrator/budgets/YYYY-MM.yaml` lido ou criado
- [ ] Stale task scan feito em `tasks/active/` — resultado reportado (mesmo que "0 tarefas stale")

❌ NOT delivery-ready: Orchestration plan entregue sem mencionar validações de Phase 0.
✅ Delivery-ready: "Phase 0 ✅ — Sem dependências circulares. Workers disponíveis: diva-reporting (0 tasks ativas), dario-fiscal (1 task ativa → SAQUEI-011 queued). Budget Abril 2026: 61% usado. Stale scan: 0 tarefas bloqueadas."

---

### Gate 4 — Execution Policies aplicadas corretamente

- [ ] Itens CRITICOS têm `execution_policy: "critical"` **e** `sla_deadline` dentro de 1h
- [ ] Deliverables de cliente têm `execution_policy: "client_facing"` (não `"default"`)
- [ ] Tarefas financeiras têm `execution_policy: "financial"` com review gate explícito
- [ ] Budget ≥80%: paralelismo limitado a 1 worker documentado no dispatch plan

❌ NOT delivery-ready: Proposta de fee para Atrium com `execution_policy: "default"` e sem review gate.
✅ Delivery-ready: `{ id: "ATRIUM-009", title: "Proposta fee Q3 2026", execution_policy: "financial", sla_deadline: "2026-04-26T21:44Z", revision_max_loops: 1, watchers: ["joao.silva@atrium.pt", "cfo@atrium.pt"] }` — aguarda approval gate antes de dispatch.

---

### Gate 5 — Audit trail e dispatch são rastreáveis

- [ ] Cada delegação explica **porquê** aquele agent/skill foi escolhido (não apenas "foi assignado")
- [ ] Paths de ficheiro concretos listados para tasks/active/, audit/, budgets/
- [ ] Token spend estimado por task **e** total do run
- [ ] Synthesis plan indica como os outputs parciais convergem no deliverable final

❌ NOT delivery-ready: "Tarefa delegada a diva-content. Ver audit log."
✅ Delivery-ready: "ARRECADA-005 → diva-content: escolhido por ser o único worker com skill `gov-copywriting` e 0 tasks ativas. Ficheiro: `~/.claude/orchestrator/tasks/active/ARRECADA-005.yaml`. Estimated tokens: 3 800. Audit: `~/.claude/orchestrator/audit/2026-04-26.jsonl` linha 47."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets

- [ ] Zero ocorrências de `<client>`, `<project>`, `<assignee>`, `<date>`, `<skill>` no output final
- [ ] IDs de task seguem convenção `CLIENTSLUG-NNN` com slug real
- [ ] Datas em ISO-8601 com valores reais (não `YYYY-MM-DD`)
- [ ] Nomes de workers/agents vindos do `company.yaml` real, não inventados

❌ NOT delivery-ready: `{ id: "<PROJECT>-001", assignee: "<agent>", sla_deadline: "<date>" }`
✅ Delivery-ready: `{ id: "PUPLI-012", assignee: "dario-growth", sla_deadline: "2026-04-27T14:00Z", project: "pupli-launch-maio" }`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output do **DARIO Orchestrator** deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via `company.yaml`, audit trail, ou session memory (ex: worker ativo, budget real, task ID existente)
- 🟡 **assumed** — plausível mas precisa de confirmação do cliente antes de delivery (ex: disponibilidade de agente, dependências inferidas)
- 🟢 **projection** — estimativa por design, não verificável no momento (ex: tempo de execução, token spend previsto)

Output checklist upfront mostra ao reader exatamente o que é trust-as-is vs. o que precisa de verify. **Honest transparency > inflated delivery.**

---

❌ **NOT delivery-ready:**
```
Worker DIVA-copywriter assignado ao TASK-003. Budget: 40% usado. ETA: 2h.
```
*Problema: reader assume que worker está disponível, budget é real e ETA é garantido — nenhum deles verificado.*

---

✅ **Delivery-ready:**
```
- Worker DIVA-copywriter → TASK-003 🟡 assumed (nenhuma task active/ confirmada; verificar company.yaml)
- Budget YYYY-MM: 40% consumido 🔵 verified (lido de ~/.claude/orchestrator/budgets/YYYY-MM.yaml)
- ETA execução: ~2h 🟢 projection (estimado por heartbeat window padrão; depende de carga real)
- Dependência TASK-002 → TASK-003: sem ciclo detetado 🔵 verified (circular dependency check passou em Phase 0)
- Skill RAG consultada (query: "onboarding flow") 🟡 assumed (resultado relevante, mas match não confirmado pelo cliente)
```

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — workers verificados em `active/`, dependências validadas pelo cliente, RAG matches aprovados
- [ ] All 🔵 citations added — paths de ficheiros (`company.yaml`, `budgets/`, `audit/`) referenciados explicitamente no output
- [ ] All 🟢 projections labeled como tal ao cliente — ETA, token spend e throughput marcados como estimativas, não garantias

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Orchestration Plan — Tributario.AI | Sprint Lançamento Beta (Abril 2026)

## Phase 0: Validation Report
- Circular dependencies: ✅ Nenhuma detectada (grafo acíclico verificado)
- Worker availability: dario-fiscal ✅ livre | diva-content ✅ livre | dario-growth ⚠️ 1 task ativa (TRIB-008 in_review) → TRIB-011 queued
- Budget Abril 2026: 58% usado (€ 1 160 / € 2 000) — ✅ sem restrições de paralelismo
- Stale scan: 1 tarefa stale → TRIB-006 (in_progress há 31h) → status atualizado para `blocked`, blocked_reason: "stale — no update for >24h"

## Mission Brief
**Goal:** Lançar beta fechado Tributario.AI para 50 contabilistas portugueses até 30 Abril 2026.
**In scope:** Landing page, sequência email onboarding, guia fiscal Q2 2026, campanha LinkedIn.
**Out of scope:** Integração AT (fase 2). Suporte pós-lançamento.
**Constraints:** Budget 58% usado. Miguel Costa (CEO) aprova todos os client_facing antes de publicar.

## Task Breakdown

```yaml
- id: TRIB-010
  title: "Redigir guia fiscal IRS 2026 para contabilistas beta"
  assignee: dario-fiscal
  execution_policy: client_facing
  estimated_tokens: 6500
  sla_deadline: "2026-04-27T10:00Z"
  depends_on: []
  revision_max_loops: 2
  blocked_reason: null
  watchers: ["miguel.costa@tributario.ai"]

- id: TRIB-011
  title: "Escrever sequência 3 emails onboarding beta users"
  assignee: diva-content
  execution_policy: client_facing
  estimated_tokens: 4200
  sla_deadline: "2026-04-27T14:00Z"
  depends_on: ["TRIB-010"]
  revision_max_loops: 2
  blocked_reason: null
  watchers: ["miguel.costa@tributario.ai"]

- id: TRIB-012
  title: "Criar copy landing page beta + CTA principal"
  assignee: diva-content
  execution_policy: client_facing
  estimated_tokens: 3800
  sla_deadline: "2026-04-27T14:00Z"
  depends_on: []
  revision_max_loops: 1
  blocked_reason: null
  watchers: ["miguel.costa@tributario.ai", "design@tributario.ai"]

- id: TRIB-013
  title: "Gerar 5 posts LinkedIn campanha lançamento beta"
  assignee: dario-growth
  execution_policy: default
  estimated_tokens: 3000
  sla_deadline: "2026-04-27T22:00Z"
  depends_on: ["TRIB-012"]
  revision_max_loops: 2
  blocked_reason: null
  watchers: ["miguel.costa@tributario.ai"]
```

## Dispatch Log
- TRIB-010 → dario-fiscal: único worker com `skill: fiscal-pt` e 0 tasks ativas. Iniciado 2026-04-26T19:44Z.
- TRIB-012 → diva-content: worker livre, skill `copywriting-saas` confirmado. Iniciado em paralelo com TRIB-010.
- TRIB-011 → diva-content: queued, aguarda TRIB-010 (depende do guia fiscal).
- TRIB-013 → dario-growth: queued, aguarda TRIB-012.

## Synthesis Plan
TRIB-010 + TRIB-012 → review Miguel Costa → TRIB-011 gerado com referências ao guia → TRIB-013 alinhado com copy da landing → entrega bundle completo até 2026-04-28T09:00Z.

**Total estimated tokens:** 17 500 | **Budget pós-run estimado:** 87 500 tokens ≈ 75% do mês.

Audit: `~/.claude/orchestrator/audit/2026-04-26.jsonl`
```

---

## Output anti-patterns

- **Placeholders não substituídos** — entregar plano com `<client>`, `<project-id>` ou `<assignee>` visíveis
- **Tarefas não-atómicas** — uma task com dois verbos ("escrever e publicar", "criar e rever") que deviam ser duas tasks separadas
- **Phase 0 omitida** — saltar validações de circular dependency, stale tasks ou budget e ir direto à decomposição
- **SLA deadlines inventados** — datas que não derivam de `execution_policy.sla_hours` + timestamp de criação real
- **Dispatch sem justificação** — "TASK-X atribuída a dario-fiscal" sem explicar porquê aquele worker
- **Schema v2 incompleto** — tasks sem `revision_max_loops`, `blocked_reason` ou `watchers`, inviabilizando review gates
- **Budget ignorado** — orquestrar 3 workers em paralelo quando budget ≥80% (devia limitar a 1)
- **Synthesis plan ausente** — listar tarefas mas não explicar como os outputs convergem no deliverable final
