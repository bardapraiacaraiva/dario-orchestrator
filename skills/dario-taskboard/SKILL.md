---
name: dario-taskboard
description: "Paperclip-inspired task lifecycle management — create, assign, checkout, review, approve tasks with atomic ownership and status tracking. Persistent YAML-based taskboard at ~/.claude/orchestrator/tasks/. Triggers on: 'taskboard', 'tarefas', 'tasks', 'criar tarefa', 'ver tarefas', 'task status', 'backlog', 'sprint', 'kanban'."
license: MIT
---

# DARIO Taskboard — Paperclip-Style Task Lifecycle

Persistent task management with atomic checkout, dependency tracking, execution policies, and audit logging. The backbone of the DARIO Orchestrator.

## When to activate

- User asks to see, create, or manage tasks
- Called by `dario-orchestrator` during decomposition and tracking
- User says "taskboard", "tarefas", "tasks", "backlog", "sprint", "kanban"
- When tracking multi-step work across sessions
- Invoked via `/dario-taskboard`

## Storage

```
~/.claude/orchestrator/tasks/
  ├── active/          # Tasks in progress (backlog through in_review)
  │   ├── PROJ-001.yaml
  │   └── PROJ-002.yaml
  ├── done/            # Completed tasks (archived)
  │   └── PROJ-000.yaml
  └── templates/       # Reusable task templates
      ├── client-audit.yaml
      ├── brand-pipeline.yaml
      └── architecture-project.yaml
```

## Task Schema

```yaml
# PROJ-001.yaml
id: "PROJ-001"
title: "Descriptive imperative action"
description: "What needs to be done, why, and success criteria"
project: "client-slug"                # Links to agent-memory project
status: "todo"                        # See status flow below
priority: "high"                      # critical | high | medium | low
assignee: null                        # Worker ID from company.yaml (agents or workers section)
assigned_by: "dario-ceo"              # Who assigned it
parent: null                          # Parent task ID (for decomposition)
children: []                          # Child task IDs
depends_on: []                        # Must complete before this starts
blocks: []                            # Tasks waiting on this one
execution_policy: "default"           # default | critical | client_facing | financial
estimated_tokens: 5000                # Rough token budget
actual_tokens: null                   # Filled after execution via token capture contract
skill: "dario-brand"                  # Which skill executes this
squad: null                           # Optional squad for parallel work
division: "dario"                     # dario | diva | lucas
tags: []                              # Free-form tags
created_at: "2026-04-26T19:44:00Z"
updated_at: "2026-04-26T19:44:00Z"
checked_out_at: null                  # When assignee claimed it
completed_at: null                    # When marked done
reviewed_by: null                     # Reviewer agent ID
approved_by: null                     # Approver (user or CEO)
completion_comment: null              # Mandatory comment at completion
revision_count: 0                     # How many revision loops
revision_max_loops: 3                 # Max revisions before forced escalation (default from execution_policy)
blocked_reason: null                  # Required when status is "blocked" — why and what unblocks it
watchers: []                          # Agent IDs notified on status changes (CEO auto-added for critical)
notes: []                             # Append-only notes log
```

## Status Flow

```
                    ┌──────────────────────────────┐
                    │                              │
backlog ──→ todo ──→ in_progress ──→ in_review ──→ done
                         │              │
                         │              └──→ in_progress (revision)
                         │
                         └──→ blocked ──→ in_progress (unblocked)
```

**Status definitions:**
- `backlog` — Identified but not prioritized. May lack assignee.
- `todo` — Prioritized, assignee known, ready to start when dependencies clear.
- `in_progress` — Atomic checkout complete. One and only one agent is working on it.
- `in_review` — Work complete, awaiting review per execution policy.
- `done` — Reviewed and approved. Moved to `done/` directory.
- `blocked` — Cannot proceed due to external dependency. Must have `blocked_reason`.

## Operations

### CREATE — New Task

```bash
# Invoke: /dario-taskboard create
```

**Process:**
1. Gather: title, description, project, priority, skill, dependencies
2. Generate ID: `<PROJECT_PREFIX>-<NNN>` (auto-increment per project)
3. Set status to `backlog` (or `todo` if assignee is known)
4. Write YAML to `~/.claude/orchestrator/tasks/active/<ID>.yaml`
5. Log to audit trail

**Batch create from template:**
```bash
# Invoke: /dario-taskboard template <template-name> <project-slug>
```
Reads from `~/.claude/orchestrator/tasks/templates/<name>.yaml` and creates all tasks with proper IDs and dependencies.

### ASSIGN — Atomic Checkout

```bash
# Invoke: /dario-taskboard assign <task-id> <worker-id>
```

**Process:**
1. Read task YAML
2. Verify task is `todo` or `backlog`
3. Verify worker capabilities match task requirements (check company.yaml)
4. Verify no dependency blockers (all `depends_on` tasks are `done`)
5. Set `assignee`, `assigned_by`, `checked_out_at`, status → `todo`
6. Write YAML atomically
7. Log to audit trail

**Atomic guarantee:** If task is already `in_progress` with a different assignee, REJECT with 409 (conflict). Only the current assignee or the CEO can reassign.

### START — Begin Work

```bash
# Invoke: /dario-taskboard start <task-id>
```

**Process:**
1. Verify task is `todo` and has assignee
2. Verify all `depends_on` are `done`
3. Set status → `in_progress`, `checked_out_at` → now
4. Write YAML
5. Log to audit trail

### UPDATE — Progress Notes

```bash
# Invoke: /dario-taskboard note <task-id> <text>
```

**Process:**
1. Append timestamped note to `notes[]` array
2. Update `updated_at`
3. Write YAML

### COMPLETE — Submit for Review

```bash
# Invoke: /dario-taskboard complete <task-id> <comment>
```

**Process:**
1. Verify task is `in_progress`
2. Verify `comment` is substantive (not empty, not trivial)
3. Set `completion_comment`, status → `in_review`
4. Check execution policy:
   - If `default` and no review required → status → `done`
   - If review/approval required → stay `in_review`
5. Write YAML
6. Log to audit trail

### REVIEW — Quality Gate

```bash
# Invoke: /dario-taskboard review <task-id> <approve|revise|escalate> [comment]
```

**Process:**
- `approve`: Set `reviewed_by`, status → `done` (or → pending approval if policy requires)
- `revise`: Increment `revision_count`, add revision note, status → `in_progress`
- `escalate`: Add escalation note, reassign to manager/CEO
- Check `revision_max_loops` — if exceeded, force escalate to user

### APPROVE — Final Gate

```bash
# Invoke: /dario-taskboard approve <task-id>
```

**Process:**
1. Set `approved_by` (user or CEO)
2. Status → `done`
3. Set `completed_at` → now
4. Move YAML from `active/` to `done/`
5. Unblock dependent tasks (check `blocks[]`)
6. Log to audit trail

### BLOCK / UNBLOCK

```bash
# Invoke: /dario-taskboard block <task-id> <reason>
# Invoke: /dario-taskboard unblock <task-id>
```

**Process (BLOCK):**
1. Set status → `blocked`
2. Set `blocked_reason` to the provided reason (MANDATORY — block without reason is rejected)
3. Notify all `watchers[]` agents
4. Log to audit trail

**Process (UNBLOCK):**
1. Verify blocker is resolved
2. Clear `blocked_reason`
3. Status → `todo` (not `in_progress` — requires re-checkout)
4. Log to audit trail

### LIST — View Taskboard

```bash
# Invoke: /dario-taskboard list [project] [status] [assignee]
```

**Output format:**
```markdown
## Taskboard — <Project> (or All Projects)

### CRITICAL
| ID | Task | Assignee | Status | Age | Blocked? |
|---|---|---|---|---|---|
| PROJ-001 | Brand positioning | worker-brand | in_progress | 2h | - |

### HIGH
| ID | Task | Assignee | Status | Age | Blocked? |
|---|---|---|---|---|---|

### MEDIUM / LOW
...

**Summary:** X total | Y active | Z blocked | W done
**Stale tasks (>24h no update):** PROJ-003, PROJ-007
```

### STALE — Detect Stale Tasks

```bash
# Invoke: /dario-taskboard stale [hours]
```

Finds tasks `in_progress` with no `updated_at` change in N hours (default: 24).

## Dependency Resolution

When a task completes:
1. Find all tasks where `depends_on` includes the completed task ID
2. For each dependent task:
   a. Check if ALL dependencies are now `done`
   b. If yes AND task has assignee → auto-transition to `todo`
   c. If yes AND task has no assignee → flag for dispatch

This creates a **cascading unblock** effect — completing one task can trigger a chain of tasks becoming available.

## Parent Task Rollup

When a child task changes status:
1. Read the parent task (if `parent` is set)
2. Read ALL children of that parent
3. Apply rollup rules:
   - If ANY child is `blocked` → parent is `blocked` (set `blocked_reason: "child <ID> blocked"`)
   - If ALL children are `done` → parent auto-transitions to `in_review` (if review required) or `done`
   - If ANY child is `in_progress` → parent is `in_progress`
   - Otherwise parent stays at its current status
4. Update parent's `updated_at`

**Note:** Parent tasks are grouping nodes — they don't execute directly. Only leaf tasks (no children) run skills.

## Revision Loop Control

When a reviewer requests revision:
1. Check `revision_count` against `revision_max_loops`
2. If `revision_count >= revision_max_loops`:
   - **DO NOT send back to worker** — the loop is broken
   - Set status → `blocked`
   - Set `blocked_reason: "revision_max_loops exceeded (<N> cycles). Requires user intervention."`
   - Add `watchers: ["dario-ceo"]` if not already present
   - Log escalation to audit trail
3. If within limits:
   - Increment `revision_count`
   - Add revision note to `notes[]` with reviewer feedback
   - Status → `in_progress`

## Cross-Session Persistence

Tasks are stored as individual YAML files. This means:
- Tasks survive session compaction (they're on disk, not in memory)
- Multiple sessions can read the same taskboard
- Git-friendly if the orchestrator directory is tracked
- Human-readable and editable

## Integration Points

### With dario-orchestrator
- Orchestrator calls taskboard for all task CRUD
- Taskboard enforces atomic checkout rules
- Taskboard triggers dependency resolution

### With dario-dispatch
- Dispatch reads taskboard for unassigned tasks
- Dispatch writes assignments back to taskboard

### With Audit Trail
- Every taskboard mutation writes to `~/.claude/orchestrator/audit/YYYY-MM-DD.yaml`
- Format: `{timestamp, actor, action, entity_id, details}`

### With Agent Memory
- Task `project` field links to agent-memory project files
- Completed task summaries can be appended to project context

### With Obsidian
- Task reports saved to `05 - Claude - IA/Outputs/` on demand
- Sprint summaries saved weekly

## Red Flags

- Never allow two agents to own the same task simultaneously
- Never mark a task `done` without a completion comment
- Never skip dependency checks — if depends_on isn't all done, task stays blocked
- Never delete tasks — archive to `done/` for audit trail
- Never exceed revision_max_loops without escalating to user
- Stale tasks (>48h) should trigger an alert in the orchestration report

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Task IDs e Schema completo
- [ ] Cada tarefa tem ID no formato `<PREFIX>-<NNN>` com prefixo coerente com o projeto (ex: `CUI-001`, `ATR-007`)
- [ ] Campos obrigatórios preenchidos: `id`, `title`, `status`, `priority`, `skill`, `created_at`, `assigned_by`
- [ ] `depends_on` e `blocks` são listas (mesmo que vazias `[]`), nunca `null` implícito
- [ ] `execution_policy` é um dos 4 valores válidos: `default | critical | client_facing | financial`
- ❌ NOT delivery-ready: `assignee: <worker-id>` ou `project: <client-slug>`
- ✅ Delivery-ready: `assignee: "lucas-dev"`, `project: "cuidai"`, `skill: "dario-brand"`

### Gate 2 — Status Flow coerente
- [ ] Status corresponde ao estado real da tarefa (não `todo` se ninguém está atribuído)
- [ ] Toda tarefa `blocked` tem `blocked_reason` preenchido com texto explicativo
- [ ] Tarefas `in_progress` têm `checked_out_at` com timestamp ISO 8601 real
- [ ] Tarefas `done` têm `completed_at` + `completion_comment` + `approved_by` preenchidos
- ❌ NOT delivery-ready: status `blocked` sem `blocked_reason`, ou `done` sem `completed_at`
- ✅ Delivery-ready: `blocked_reason: "Aguarda aprovação de orçamento pelo cliente Cuidai — desbloqueio esperado 2026-05-02"`

### Gate 3 — Dependências e Atomic Checkout
- [ ] Não existe tarefa `in_progress` com `depends_on` contendo tarefas ainda `todo` ou `backlog`
- [ ] Nenhuma tarefa tem dois `assignee` diferentes em simultâneo (regra 409 respeitada)
- [ ] `revision_count` ≤ `revision_max_loops`; se atingido, tarefa está escalada para CEO
- [ ] Tarefas com `execution_policy: critical` têm CEO (`dario-ceo`) em `watchers[]`
- ❌ NOT delivery-ready: `in_progress` com `depends_on: ["ATR-003"]` e ATR-003 ainda `todo`
- ✅ Delivery-ready: ATR-003 está `done` antes de ATR-004 passar a `in_progress`

### Gate 4 — Audit Trail e Notas
- [ ] Toda transição de status tem entrada no `notes[]` com timestamp e actor
- [ ] `updated_at` foi actualizado em cada operação (nunca igual a `created_at` após mudanças)
- [ ] `revision_count` incrementado correctamente em cada loop `in_review → in_progress`
- [ ] `completion_comment` é substantivo (mínimo 1 frase descritiva), não `"done"` ou `"ok"`
- ❌ NOT delivery-ready: `notes: []` numa tarefa que já passou por 3 status diferentes
- ✅ Delivery-ready: `notes: [{ts: "2026-04-28T10:22:00Z", actor: "lucas-dev", text: "API Stripe integrada, testes unitários a 87% coverage"}]`

### Gate 5 — Prioridades e Estimativas realistas
- [ ] Distribuição de prioridades coerente: não existe sprint com 100% tarefas `critical`
- [ ] `estimated_tokens` é número inteiro positivo e plausível para o scope da tarefa (≥500)
- [ ] Tarefas `critical` têm `squad` ou `assignee` definido — nunca ficam `null` em ambos
- [ ] `division` é um dos valores válidos: `dario | diva | lucas`
- ❌ NOT delivery-ready: `estimated_tokens: null` ou `priority: critical` com `assignee: null` e `squad: null`
- ✅ Delivery-ready: `estimated_tokens: 8000`, `priority: "high"`, `assignee: "dario-cfo"`, `division: "dario"`

### Gate 6 — Output usa CLIENT NAME + REAL data, sem angle-brackets placeholder
- [ ] Nenhum campo contém `<placeholder>`, `<client>`, `<worker-id>`, `<date>` ou similar
- [ ] Project slug corresponde a cliente real ou projecto identificável
- [ ] Timestamps são datas ISO 8601 plausíveis (não `0000-00-00` ou futuro impossível)
- [ ] Worker IDs existem no universo DARIO (`dario-ceo`, `lucas-dev`, `dario-cfo`, etc.)
- ❌ NOT delivery-ready: `project: "<client-slug>"`, `approved_by: "<approver>"`
- ✅ Delivery-ready: `project: "saquei"`, `approved_by: "dario-ceo"`, `created_at: "2026-04-26T14:30:00Z"`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output do Taskboard deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via YAML persistido em `~/.claude/orchestrator/tasks/` ou audit log da sessão
- 🟡 **assumed** — plausível dado o contexto do projecto, mas precisa de confirmar com utilizador antes de entrega
- 🟢 **projection** — estimativa de design (token budget, deadline, revision cycles — não verificável até execução)

Output checklist upfront mostra ao utilizador exactamente o que é trust-as-is vs. precisa de sync. **Honest transparency > inflated delivery.**

---

❌ NOT delivery-ready:
```
PROJ-007 | "Redesign homepage" | assignee: diva-brand | 3 revisões | deadline: sexta
```
*(reader assume que tudo está confirmado — assignee pode não existir em company.yaml, deadline nunca foi registado)*

✅ Delivery-ready:
```
🔵 ID: PROJ-007 (gerado e persistido em active/)
🔵 Título: "Redesign homepage" (criado nesta sessão, YAML escrito)
🟡 Assignee: diva-brand (existe em company.yaml? — confirmar antes de checkout)
🟡 Priority: high (assumed por contexto do sprint — utilizador não especificou)
🟢 estimated_tokens: 8 000 (projecção de design; actual_tokens preenchido pós-execução)
🟢 revision_max_loops: 3 (default da execution_policy — pode variar se policy mudar)
```

---

**Ship checklist post-cliente-sync:**
- [ ] Todos os 🟡 items confirmados — assignee existe em `company.yaml`, priority validada pelo utilizador
- [ ] Todos os 🔵 items citam source (ID do YAML persistido, timestamp do audit log)
- [ ] Todos os 🟢 projections comunicados ao cliente como estimativas — expectativas claras sobre token budget e revision loops antes de `in_progress`

## Fully-worked A-tier example (delivery-ready reference)

```yaml
# ~/.claude/orchestrator/tasks/active/SAQ-003.yaml
id: "SAQ-003"
title: "Implementar webhook de confirmação de crédito Stripe → SAQUEI backend"
description: |
  Configurar endpoint /webhooks/stripe no backend SAQUEI para receber
  eventos payment_intent.succeeded e credit.created. Validar assinatura
  HMAC, actualizar estado do empréstimo em Supabase e disparar notificação
  push ao utilizador. Critério de sucesso: 100% dos eventos de teste
  processados sem erro 5xx em staging.
project: "saquei"
status: "in_review"
priority: "critical"
assignee: "lucas-dev"
assigned_by: "dario-ceo"
parent: "SAQ-001"
children: []
depends_on: ["SAQ-001", "SAQ-002"]
blocks: ["SAQ-004", "SAQ-005"]
execution_policy: "financial"
estimated_tokens: 12000
actual_tokens: 11340
skill: "dario-code"
squad: null
division: "lucas"
tags: ["stripe", "webhook", "backend", "financeiro"]
created_at: "2026-04-22T09:00:00Z"
updated_at: "2026-04-28T16:45:00Z"
checked_out_at: "2026-04-23T08:15:00Z"
completed_at: "2026-04-28T16:40:00Z"
reviewed_by: "dario-cto"
approved_by: null
completion_comment: |
  Webhook implementado em /webhooks/stripe. Validação HMAC activa com
  secret rotacionado. Supabase actualiza campo loan_status para 'funded'
  em <200ms. Testes em staging: 47/47 eventos processados, zero 5xx.
  Aguarda aprovação final dario-ceo antes de deploy para produção.
revision_count: 1
revision_max_loops: 3
blocked_reason: null
watchers: ["dario-ceo", "dario-cfo"]
notes:
  - ts: "2026-04-23T08:15:00Z"
    actor: "lucas-dev"
    text: "Checkout atómico confirmado. A iniciar implementação do endpoint."
  - ts: "2026-04-25T11:30:00Z"
    actor: "dario-cto"
    text: "Revisão intercalar: lógica HMAC correcta, falta idempotency key para retries."
  - ts: "2026-04-25T14:00:00Z"
    actor: "lucas-dev"
    text: "Revisão 1 endereçada: adicionado idempotency_key via stripe-signature header hash."
  - ts: "2026-04-28T16:45:00Z"
    actor: "lucas-dev"
    text: "Submetido para review final. 47/47 testes staging OK. Token spend: 11340."
```

---

## Output anti-patterns

- Criar tarefa com `status: in_progress` mas `checked_out_at: null` — viola o contrato de atomic checkout
- Usar `blocked_reason: null` numa tarefa com `status: blocked` — bloqueia o dashboard sem contexto accionável
- Tarefas `done` sem `completion_comment` — perde o audit trail e impossibilita retrospectivas
- `depends_on` com IDs que não existem no sistema (ex: `SAQ-099` sem ficheiro correspondente)
- `revision_count` maior que `revision_max_loops` sem escalação registada para `dario-ceo`
- `priority: critical` com `watchers: []` — CEO nunca é notificado de tarefas de risco financeiro/operacional
- `estimated_tokens: 500` numa tarefa descrita como "arquitectura completa do sistema de pagamentos"
- Copiar template sem actualizar `id`, resultando em IDs duplicados no mesmo projecto
- `notes[]` com entradas sem `actor` — impossível determinar quem fez o quê em auditoria
