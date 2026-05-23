---
name: lucas-autopilot
description: "LUCAS Autopilot — the ACTIVE heartbeat that EXECUTES. Scans taskboard, auto-dispatches unassigned tasks, executes next wave in parallel, scores completed outputs, enforces budget limits, and self-paces via /loop. This is the skill that makes the system autonomous. Triggers on: 'autopilot', 'auto', 'piloto automatico', 'run all', 'executa tudo', 'lucas go'."
license: MIT
---

# LUCAS Autopilot — Active Heartbeat

The skill that closes the loop. Not a reporter — an **executor**.

## What this does in ONE invocation

```
1. STATE   — Evaluate state machine (python state_machine.py --evaluate --json)
             If GUARDIAN: STOP. If REFLECTIVE_PAUSE: max_parallel=1, no auto-execute.
2. SCAN    — Read all tasks in ~/.claude/orchestrator/tasks/active/
3. BUDGET  — Check spend. If >95%, STOP. If >80%, WARN.
4. UNBLOCK — Cascade: done tasks unblock dependents → todo
5. DISPATCH — Run dispatch engine (python dispatch_engine.py --json)
6. EXECUTE — Launch next wave (max_parallel from state machine) via Agent tool
7. SCORE   — Quality-score completed tasks (rubric 5 dimensions, 0-100)
8. LOG     — Update audit trail + budget + skill metrics
9. PACE    — If more tasks waiting: schedule next pulse in 60s
             If idle: schedule next pulse in 1800s (30min)
             If budget critical or GUARDIAN: STOP loop
```

## When to activate

- Via `/loop /lucas-autopilot` — autonomous self-pacing mode
- Via `/lucas-autopilot` — single pulse execution
- When user says "autopilot", "piloto automatico", "executa tudo", "lucas go"

## Execution Protocol

### Step 1: STATE CHECK (via State Machine)

**First action of every pulse** — evaluate the operational state machine:

```bash
python ~/.claude/orchestrator/state_machine.py --evaluate --json
```

This returns:
```json
{
  "transitioned": false,
  "state": "ACTIVE",
  "autonomy_level": "P-A2",
  "max_parallel": 3,
  "system_health": 0.95
}
```

**Behavior by state:**

| State | Action |
|---|---|
| `ACTIVE` | Continue normally. Use `max_parallel` from state machine response. |
| `REFLECTIVE_PAUSE` | Reduce to max_parallel=1. Skip auto-execute. Dispatch only. Run AutoDiag. |
| `GUARDIAN` | **STOP immediately.** No dispatch, no execution. Log and notify user. |
| `EXPANSION` | Skip execution. Run learning cycle (scores review, weight updates). |

If `state_machine.py` fails: **default to ACTIVE with max_parallel=2** (safe degraded mode).

### Step 2: SCAN

Read every `.yaml` file in `~/.claude/orchestrator/tasks/active/`.
Build a task map:

```
For each task:
  - id, title, status, priority, assignee, skill, depends_on, blocks
  - Group by status: backlog | todo | in_progress | in_review | done | blocked
```

Report:
```
SCAN: 12 tasks total | 3 done | 2 in_progress | 4 todo | 2 backlog | 1 blocked
```

### Step 2: BUDGET CHECK

Read `~/.claude/orchestrator/budgets/YYYY-MM.yaml`:

```python
if percentage >= 95:
    LOG "BUDGET CRITICAL: {percentage}% — STOPPING autopilot"
    # Do NOT execute any tasks
    # Do NOT schedule next pulse
    STOP
elif percentage >= 80:
    LOG "BUDGET WARNING: {percentage}% — limiting to 1 task per pulse"
    max_parallel = 1  # Slow down to conserve
else:
    max_parallel = 3  # Normal operation
```

**This is a HARD STOP.** If budget is critical, autopilot refuses to execute. User must manually approve or increase limit.

### Step 3: UNBLOCK CASCADE

```python
for task in tasks where status == "done":
    for dependent in all_tasks where task.id in dependent.depends_on:
        if ALL of dependent.depends_on are "done":
            dependent.status = "todo"  # Ready for dispatch
            LOG "UNBLOCKED: {dependent.id} — all dependencies met"
            UPDATE dependent YAML file on disk
```

### Step 4: AUTO-DISPATCH (via Dispatch Engine)

**Run the actual dispatch engine** — deterministic routing with full capability matching, workload awareness, sibling fallback, and director escalation:

```bash
python ~/.claude/orchestrator/dispatch_engine.py --json
```

This atomically:
- Reads all unassigned todo tasks
- Matches each to the optimal worker via keyword→skill→worker lookup
- Checks worker availability (max 1 in_progress per worker)
- Falls back to siblings or escalates to director if primary busy
- Writes assignee + dispatch_reason to the task YAML
- Logs to audit/dispatch_{date}.log

The `--json` output gives:
```json
{
  "dispatched": 2,
  "queued": 1,
  "total_analyzed": 3,
  "assignments": [
    {"task_id": "PROJ-001", "assigned_to": "worker-brand", "skill": "dario-brand", "reason": "AVAILABLE"},
    {"task_id": "PROJ-002", "assigned_to": null, "skill": "custom-skill", "reason": "NO_WORKER"}
  ]
}
```

If dispatch returns `queued > 0`, log: `"DISPATCH WARNING: {queued} tasks could not be routed — need manual assignment or new worker"`

**Fallback:** If the Python engine fails (import error, file missing), fall back to inline dispatch:
```python
for task in unassigned_todo_tasks:
    worker = find_worker_by_skill(task.skill)  # simple lookup in company.yaml workers section
    if worker: assign(task, worker)
```

### Step 5: EXECUTE WAVE

```python
# Gather executable tasks: status=todo, assignee set, all depends_on=done
executable = [t for t in tasks if t.status == "todo" and t.assignee and all_deps_done(t)]

# Sort by priority: critical > high > medium > low
executable.sort(by=priority)

# Take up to max_parallel
wave = executable[:max_parallel]

if not wave:
    LOG "NO TASKS TO EXECUTE — idle"
    return "idle"

# Execute via Agent tool (parallel if multiple)
for task in wave:
    task.status = "in_progress"
    task.checked_out_at = now()
    UPDATE task YAML

    # Determine adapter
    adapter = "dario-v2-digital-ceo"  # default
    if task.division == "diva":
        adapter = "diva-v1-design-architect"

    Agent({
        description: "Autopilot: {task.id} — {task.title}",
        subagent_type: adapter,
        prompt: """
        You are {task.assignee} executing task {task.id} for the DARIO Orchestrator.

        TASK: {task.title}
        DESCRIPTION: {task.description}
        SKILL TO USE: /{task.skill}
        PROJECT: {task.project}
        PRIORITY: {task.priority}
        EXECUTION POLICY: {task.execution_policy}

        Execute this task using the specified skill.
        Be specific to the project — no generic output.
        When done, provide a substantive completion comment.
        """
    })
```

After each Agent returns:
```python
task.status = "in_review" if task.execution_policy in ["critical", "client_facing"] else "done"
task.completion_comment = agent_output_summary
task.actual_tokens = agent_usage.total_tokens
UPDATE task YAML
UPDATE budget YAML (add actual_tokens)
LOG audit entry
```

### Step 7: QUALITY SCORE (via quality_scorer.py)

After executing each task, **evaluate the output** using the 5-dimension rubric, then **record** the score:

**Step 7a — Evaluate (Claude does this inline):**
Read the completion_comment and score each dimension (0.0-1.0):
- **Specificity**: mentions client/project by name, uses specific data?
- **Actionability**: clear next steps, no ambiguity?
- **Completeness**: all task requirements covered?
- **Accuracy**: facts and recommendations correct?
- **Tone**: matches expected format and brand voice?

Calculate: `score = round((0.25*S + 0.20*A + 0.20*C + 0.25*Ac + 0.10*T) * 100)`

**Step 7b — Record (quality_scorer.py persists it):**
```bash
python ~/.claude/orchestrator/quality_scorer.py --task {task_id} --score {score} --skill {skill} --project {project} --dimensions '{"specificity":S,"actionability":A,"completeness":C,"accuracy":Ac,"tone":T}' --json
```

Returns: `{ "action": "ship"|"revision"|"success_pattern"|"escalate", "tier": "A"|"B"|"C"|"D" }`

**Step 7c — Act on result:**
```python
for task in just_completed_tasks:
    score = evaluate_with_rubric(task)  # Claude inline evaluation
    result = call("python quality_scorer.py --task {id} --score {score} ...")  # Record
    
    # lucas-quality returns: { score: int, dimensions: dict, action: str }
    VALID_ACTIONS = ["ship", "revision", "success_pattern", "escalate"]
    if score.action not in VALID_ACTIONS:
        LOG f"WARNING: lucas-quality returned unknown action '{score.action}' for {task.id}. Defaulting to 'ship'."
        score.action = "ship"
    
    task.quality_score = score.score
    UPDATE task YAML
    
    if score.action == "revision":
        # Check revision limits before sending back
        if task.revision_count >= task.revision_max_loops:
            task.status = "blocked"
            task.blocked_reason = f"revision_max_loops exceeded ({task.revision_count} cycles). Score: {score.score}/100."
            task.watchers.append("dario-ceo") if "dario-ceo" not in task.watchers
            LOG "ESCALATED: {task.id} — max revisions reached, score {score.score}"
        else:
            task.status = "in_progress"
            task.revision_count += 1
            task.notes.append(f"Revision #{task.revision_count}: {score.dimensions}")
            LOG "REVISION: {task.id} scored {score.score}/100 — sent back"
    
    elif score.action == "success_pattern":
        LOG "EXCELLENT: {task.id} scored {score.score}/100 — pattern extracted"
    
    UPDATE task YAML
```

**Skill-to-Skill Contract:**
```
invoke_lucas_quality(task) → {
    score: int (0-100),
    dimensions: {
        specificity: int,
        actionability: int,
        completeness: int,
        accuracy: int,
        tone: int
    },
    action: "ship" | "revision" | "success_pattern" | "escalate",
    feedback: str  # Human-readable feedback for revision note
}
```

**Why delegated:** Autopilot executes and paces. Quality evaluates and learns. Mixing them creates circular dependencies and prevents independent iteration on rubrics.

### Step 7: LOG

After all execution:

```yaml
# Append to ~/.claude/orchestrator/audit/YYYY-MM-DD.yaml
- timestamp: "ISO"
  actor: "lucas-autopilot"
  action: "pulse_executed"
  details: "Executed 3 tasks. Wave: [PROJ-007, PROJ-008, PROJ-009]. Budget: 15.2%."
```

Update `~/.claude/orchestrator/budgets/YYYY-MM.yaml` with new token totals.
Update `~/.claude/orchestrator/quality/skill-metrics.yaml` with new scores.

### Step 8: SELF-PACE

This is what makes autopilot truly autonomous via `/loop`:

```python
remaining_todo = count(tasks where status in ["todo", "backlog"])
remaining_in_progress = count(tasks where status == "in_progress")

if budget_critical:
    # STOP — do not schedule next pulse
    LOG "Budget critical. Autopilot stopped."
    # Do NOT call ScheduleWakeup

elif remaining_todo > 0 or remaining_in_progress > 0:
    # Active work — pulse again in 60-90 seconds
    ScheduleWakeup(delaySeconds=90, reason="tasks pending execution")

elif remaining_todo == 0 and remaining_in_progress == 0:
    # Idle — check again in 30 minutes
    ScheduleWakeup(delaySeconds=1800, reason="idle — no pending tasks")
```

## Execution Policies (enforcement during Step 5-6)

| Policy | Auto-execute? | Auto-score? | Auto-approve? |
|---|---|---|---|
| `default` | YES | YES | YES (if score >= 75) |
| `client_facing` | YES | YES | NO — stays in_review for user |
| `critical` | YES | YES | NO — asks user via AskUserQuestion |
| `financial` | YES | YES | NO — asks user via AskUserQuestion |

## Output per Pulse

```markdown
## LUCAS Autopilot Pulse — HH:MM

### Executed
| Task | Skill | Tokens | Quality | Status |
|---|---|---|---|---|
| PROJ-007 | dario-brand | 2,100 | 88/100 | done |
| PROJ-008 | seo-local | 3,200 | 91/100 | done |
| PROJ-009 | dario-offer | 2,800 | 65/100 | REVISION (low score) |

### Unblocked
- PROJ-010 → all dependencies met, moved to todo

### Budget
- This pulse: 8,100 tokens
- Month total: 160,100 / 50,000,000 (0.32%)

### Next Pulse
- 2 tasks remaining → next pulse in 90 seconds

### Alerts
- PROJ-009 scored 65/100 — sent back for revision (value equation generic)
```

## Safety Rails

1. **Budget hard stop at 95%** — no exceptions, no override without user
2. **Max 3 parallel tasks** — prevents cost explosion
3. **Max 3 revision loops** — after 3 retries, escalate to user
4. **Critical/financial tasks always need user approval** — never auto-shipped
5. **Stale detection** — tasks in_progress >24h get flagged, >48h get escalated
6. **Coalescing** — if a pulse is already running, skip the new one
7. **Audit everything** — every action logged with timestamp and actor

## How to Activate

### Full Autonomous Mode
```
/loop /lucas-autopilot
```
This starts the self-pacing loop. Autopilot will:
- Execute tasks when available (pulse every 90s)
- Slow down when idle (pulse every 30min)
- Stop if budget critical

### Single Pulse
```
/lucas-autopilot
```
Runs one pulse cycle and stops.

### Stop Autopilot
Just stop the /loop or say "stop autopilot".

---

## Autopilot Session — Worked Example

A complete autonomous session (3 pulses) for the VCH (Vivenda Creative Home) project:

### Pulse 1 — 2026-04-27 14:00:00
```
SCAN: 6 tasks | 0 done | 0 in_progress | 4 todo | 1 backlog | 1 blocked
BUDGET: 0.28% (140K/50M) — OK, max_parallel=3
UNBLOCK: none (no done tasks yet)
DISPATCH:
  VCH-001 (brand-positioning) → worker-brand (match 3/3)
  VCH-002 (seo-local-audit) → worker-seo-local (match 2/2)
  VCH-003 (content-strategy) → worker-seo-plan (match 2/3)
WAVE: [VCH-001, VCH-002, VCH-003] — 3 parallel (independent)
EXECUTE:
  Agent(VCH-001): "Brand positioning for Vivenda Creative Home — luxury interior design Lisbon"
  Agent(VCH-002): "Local SEO audit for vivendacreativehome.pt — GBP, citations, schema"
  Agent(VCH-003): "Content strategy — pillar pages for renovation + design services"
RESULT:
  VCH-001: done (1800 tokens) — "Kapferer prism + archetype: The Creator"
  VCH-002: done (2900 tokens) — "12 issues found, 3 critical, action plan generated"
  VCH-003: done (2200 tokens) — "4 pillars, 16 clusters, 90-day calendar"
QUALITY (invoke lucas-quality):
  VCH-001: 92/100 → success_pattern (extracted: "brand-positioning-luxury-home")
  VCH-002: 87/100 → ship
  VCH-003: 58/100 → REVISION (low specificity: generic clusters, not Vivenda-specific)
    → VCH-003.revision_count = 1, status → in_progress
BUDGET: +6900 tokens → 146.9K (0.29%)
PACE: 3 tasks remaining (VCH-003 revision + VCH-004 unblocked + VCH-005 blocked)
      → next pulse in 90s
```

### Pulse 2 — 2026-04-27 14:01:30
```
SCAN: 6 tasks | 2 done | 1 in_progress | 1 todo | 1 backlog | 1 blocked
BUDGET: 0.29% — OK, max_parallel=3
UNBLOCK: VCH-004 (depends on VCH-001 ✓ + VCH-002 ✓) → status: todo
DISPATCH: VCH-004 (offer-design) → worker-offer (match 3/3)
WAVE: [VCH-003-retry, VCH-004] — 2 parallel
EXECUTE:
  Agent(VCH-003): "REVISION: Content strategy for Vivenda Creative Home.
    FEEDBACK: clusters must reference Vivenda services (remodelacao, decoracao interiores,
    projecto de cozinhas). Use client's actual service pages as pillar anchors."
  Agent(VCH-004): "Grand Slam Offer for Vivenda — consultation + 3D render + project package"
RESULT:
  VCH-003: done (2600 tokens) — "Revised: 4 pillars mapped to Vivenda services + Lisbon geo"
  VCH-004: done (3100 tokens) — "3-tier offer: Consulta, Projecto, Chave-na-Mao"
QUALITY:
  VCH-003: 84/100 → ship (improved from 58 — specificity now 17/20)
  VCH-004: 89/100 → ship
UNBLOCK (post-execution): VCH-005 (email-sequence, depends on VCH-003 ✓ + VCH-004 ✓) → todo
BUDGET: +5700 tokens → 152.6K (0.31%)
PACE: 1 task remaining (VCH-005) → next pulse in 90s
```

### Pulse 3 — 2026-04-27 14:03:00
```
SCAN: 6 tasks | 4 done | 0 in_progress | 1 todo | 1 backlog | 0 blocked
BUDGET: 0.31% — OK
DISPATCH: VCH-005 (email-welcome-sequence) → worker-email (match 2/2)
WAVE: [VCH-005] — 1 task
EXECUTE:
  Agent(VCH-005): "5-email welcome sequence for Vivenda Creative Home.
    Context: The Creator archetype, luxury positioning, 3-tier offer with consultation lead."
RESULT: VCH-005: done (3800 tokens) — "5-email SOAP opera sequence with Vivenda story"
QUALITY: VCH-005: 90/100 → success_pattern (extracted: "email-sequence-luxury-home")
BUDGET: +3800 tokens → 156.4K (0.31%)

PROJECT COMPLETE: All active VCH tasks done (5/5 executed, 1 remains in backlog)
SYNTHESIZE: "Vivenda Creative Home — 5 deliverables complete. Total: 16,400 tokens.
  Quality avg: 86.8/100. 1 revision cycle (content strategy). 2 success patterns extracted."
PACE: 0 tasks remaining → next pulse in 1800s (idle mode)
```

---

## Agent Invocation Template (Pro)

### DARIO Task (subagent_type: dario-v2-digital-ceo)

```python
Agent({
    "description": f"Autopilot: {task.id} — {task.title}",
    "subagent_type": "dario-v2-digital-ceo",
    "prompt": f"""You are {task.assignee} executing task {task.id} for the DARIO Orchestrator.

== TASK ==
ID: {task.id}
Title: {task.title}
Description: {task.description}
Skill: /{task.skill}
Project: {task.project}
Priority: {task.priority}
Execution Policy: {task.execution_policy}

== CONTEXT ==
Client: {project_context.client_name}
Industry: {project_context.industry}
Brand positioning: {project_context.brand_summary or 'N/A'}
Previous deliverables: {[t.id + ': ' + t.title for t in completed_project_tasks]}

== INSTRUCTIONS ==
1. Use the /{task.skill} skill to produce the deliverable.
2. Be SPECIFIC to {project_context.client_name} — no generic output.
3. Reference the client by name, their industry, their location.
4. Output must be actionable: clear next steps, specific recommendations.
5. When done, provide a 1-2 sentence completion_comment summarizing what was produced.

== REVISION CONTEXT (if applicable) ==
{f"This is revision #{task.revision_count}. Previous feedback: {task.revision_feedback}" if task.revision_count > 0 else "First execution — no prior revisions."}
""",
    "timeout_seconds": 120
})
```

### DIVA Task (subagent_type: diva-v1-design-architect)

```python
Agent({
    "description": f"Autopilot: {task.id} — {task.title}",
    "subagent_type": "diva-v1-design-architect",
    "prompt": f"""You are {task.assignee} executing task {task.id} for the DIVA division.

== TASK ==
ID: {task.id}
Title: {task.title}
Description: {task.description}
Skill: /{task.skill}
Project: {task.project}
Priority: {task.priority}
Execution Policy: {task.execution_policy}

== PROJECT CONTEXT ==
Client: {project_context.client_name}
Project type: {project_context.project_type}  # remodelacao, construcao_nova, interiores
Location: {project_context.location}
Area: {project_context.area_m2} m2
Budget range: {project_context.budget_range}
Style references: {project_context.style_refs}
Regulatory: {project_context.regulatory_context}  # RGEU, RJUE, PDM constraints

== INSTRUCTIONS ==
1. Use the /{task.skill} skill to produce the deliverable.
2. All measurements in metric. All references to Portuguese regulations.
3. Include material specifications with Portuguese supplier references where applicable.
4. Cost estimates in EUR with IVA indication (6% rehab / 23% standard).
5. When done, provide a 1-2 sentence completion_comment.

== REVISION CONTEXT ==
{f"Revision #{task.revision_count}. Feedback: {task.revision_feedback}" if task.revision_count > 0 else "First execution."}
""",
    "timeout_seconds": 120
})
```

### Error Handling Wrapper (applies to both)

```python
def execute_task_safe(task: dict, project_context: dict) -> dict:
    """Execute a task via Agent with full error handling."""
    try:
        # Set pre-execution state
        task["status"] = "in_progress"
        task["checked_out_at"] = datetime.now(timezone.utc).isoformat()
        write_task_atomic(task)
        
        # Determine adapter
        adapter = "dario-v2-digital-ceo"
        if task.get("division") == "diva":
            adapter = "diva-v1-design-architect"
        
        # Build prompt (see templates above)
        prompt = build_agent_prompt(task, project_context, adapter)
        
        # Execute
        result = Agent(
            description=f"Autopilot: {task['id']} — {task['title']}",
            subagent_type=adapter,
            prompt=prompt,
            timeout_seconds=120
        )
        
        if result is None or result.output is None:
            raise AgentTimeoutError(f"Agent returned None for {task['id']}")
        
        # Post-execution
        task["completion_comment"] = summarize_output(result.output, max_chars=200)
        task["actual_tokens"] = result.usage.total_tokens
        task["completed_at"] = datetime.now(timezone.utc).isoformat()
        
        if task.get("execution_policy") in ["critical", "client_facing"]:
            task["status"] = "in_review"
        else:
            task["status"] = "done"
        
        write_task_atomic(task)
        return {"success": True, "task": task, "tokens": result.usage.total_tokens}
    
    except AgentTimeoutError:
        LOG(f"TIMEOUT: {task['id']} — agent did not respond within 120s")
        # Retry once
        retry_result = retry_agent_once(task, project_context)
        if retry_result:
            return retry_result
        # If retry also fails, block the task
        task["status"] = "blocked"
        task["blocked_reason"] = "agent_timeout_2x"
        task["watchers"] = list(set(task.get("watchers", []) + ["dario-ceo"]))
        write_task_atomic(task)
        return {"success": False, "task": task, "error": "agent_timeout_2x"}
    
    except Exception as e:
        LOG(f"ERROR: {task['id']} — unexpected: {e}")
        task["status"] = "blocked"
        task["blocked_reason"] = f"execution_error: {str(e)[:100]}"
        write_task_atomic(task)
        return {"success": False, "task": task, "error": str(e)}
```

---

## Failure Recovery Matrix

| # | Failure | Detection | Auto-Recovery | Manual Escalation |
|---|---|---|---|---|
| 1 | **Agent returns empty** | `result.output is None` or `len(result.output.strip()) == 0` | Retry once with enhanced prompt (add "You MUST produce substantive output"). If still empty, block task. | CEO alert. Task flagged with `blocked_reason: "empty_output_2x"`. User must review skill/prompt. |
| 2 | **Agent timeout** | No response within 120 seconds | Retry once (same prompt, fresh agent). Log both attempts. | After 2 timeouts, block task. Add to pulse report "Agent Timeout" section. |
| 3 | **Quality score <40** | `score_result.score < 40` | Immediate revision with explicit feedback injected into prompt. Do NOT count as normal revision — mark as `emergency_revision`. | If emergency revision also scores <40, block task. CEO must review whether skill is appropriate for this task type. |
| 4 | **revision_max exceeded** | `task.revision_count >= task.revision_max_loops` (default 3) | No auto-recovery. Task blocked immediately. | CEO alert. Options: (a) increase revision_max, (b) reassign to different worker, (c) accept current quality, (d) manual execution. |
| 5 | **Budget >95% mid-wave** | Budget check after each task completion within a wave | Complete current executing tasks (do not abort mid-execution). Do NOT start next task in wave. Set remaining wave tasks back to `todo`. | Hard stop all autopilot activity. User notified: "Budget critical. Autopilot paused. {N} tasks remain unexecuted." |
| 6 | **Task YAML write fails** | `write_task_atomic()` returns `False` or raises exception | Retry write once. If disk full or permission error, hold task state in memory and attempt write on next pulse. | If write fails 3 consecutive times, dump task state to `stderr` and stop autopilot. Alert: "Filesystem error — cannot persist state." |
| 7 | **Dependency cycle detected** | During unblock cascade, task A depends on B which depends on A (or longer chains) | Identify all tasks in cycle. Block ALL with reason `circular_dependency`. Clear `depends_on` on the lowest-priority task in the cycle to break it. | CEO alert with full cycle visualization. Require user to manually correct dependency graph. |

---

## Self-Pacing Decision Tree

```
┌─────────────────────────────────────────────────────────┐
│                  SELF-PACING LOGIC                       │
│              (runs at end of every pulse)                │
└─────────────────────────────────────────────────────────┘

budget >= 95%?
  YES → STOP. Do NOT schedule next pulse.
         Log "Budget critical ({percentage}%). Autopilot halted."
         Set autopilot_state = "stopped_budget"
         EXIT

  NO → tasks_remaining > 0 AND budget < 80%?
    YES → ScheduleWakeup(90s, "active tasks pending, budget healthy")
           Log "Next pulse in 90s. {tasks_remaining} tasks waiting."

    NO → tasks_remaining > 0 AND budget 80-95%?
      YES → ScheduleWakeup(270s, "budget warning, conserving pace")
             Log "Next pulse in 270s. Budget {percentage}%, slowing pace."
             Set max_parallel = 1  # For next pulse

      NO → tasks_remaining == 0 AND tasks_in_progress > 0?
        YES → ScheduleWakeup(120s, "waiting for in-progress tasks to complete")
               Log "No new tasks. {tasks_in_progress} still executing externally."

        NO → tasks_remaining == 0 AND tasks_in_progress == 0?
          YES → ScheduleWakeup(1800s, "idle, no pending tasks")
                 Log "All tasks complete or backlog only. Idle mode (30min)."
                 Set autopilot_state = "idle"

          NO → # Should never reach here
               Log "WARNING: unexpected pacing state. Defaulting to 1800s."
               ScheduleWakeup(1800s, "fallback_idle")
```

**State Transitions:**
```
active (90s) ←→ conserving (270s) ←→ idle (1800s) → stopped (no schedule)
     ↑                                                        ↓
     └──── user says "lucas go" / new tasks added ────────────┘
```

---

## Quality Delegation — Full Flow

A complete quality scoring flow with actual data from task MNB-001:

### 1. Task MNB-001 completed with output

```yaml
# Task state after Agent execution
id: MNB-001
title: "Brand story for Mar'n'Brasa grillhouse"
status: done  # Just completed by agent
project: mar-brasa
skill: dario-brand
assignee: worker-brand
execution_policy: client_facing
actual_tokens: 1800
completion_comment: "Brand positioning using Kapferer Prism. Archetype: The Outlaw/Explorer."
completed_at: "2026-04-27T14:00:12Z"
revision_count: 0
revision_max_loops: 3
```

### 2. Invoke lucas-quality with task data

```python
# Autopilot calls lucas-quality with full context
quality_input = {
    "task_id": "MNB-001",
    "task_title": "Brand story for Mar'n'Brasa grillhouse",
    "skill_used": "dario-brand",
    "project": "mar-brasa",
    "execution_policy": "client_facing",
    "completion_comment": "Brand positioning using Kapferer Prism. Archetype: The Outlaw/Explorer.",
    "output_text": """
        ## Mar'n'Brasa — Brand Positioning
        
        ### Brand Archetype: The Outlaw / Explorer Blend
        Mar'n'Brasa breaks the mold of traditional Portuguese restaurants...
        
        ### Kapferer Prism
        - Physique: Open-flame grilling, industrial-chic decor, Lisbon riverside
        - Personality: Bold, irreverent, adventurous
        - Culture: Portuguese craftsmanship meets global BBQ culture
        - Relationship: "Your crew's spot" — community, shared plates
        - Reflection: Young professionals, foodies, 25-40, Lisbon expats
        - Self-image: "I discover the real Lisbon" — insider knowledge
        
        ### Messaging Hierarchy
        1. Tagline: "Fogo na alma, sabor na brasa"
        2. Elevator: "Lisbon's boldest grillhouse — where Portuguese fire meets global flavor"
        3. Story: [8-beat narrative follows]
        ...
    """,
    "revision_count": 0
}

score_result = invoke_lucas_quality(quality_input)
```

### 3. Receive score response

```python
score_result = {
    "score": 92,
    "dimensions": {
        "specificity": 19,      # Mentions Mar'n'Brasa, Lisbon, riverside, Portuguese
        "actionability": 18,    # Clear messaging hierarchy, usable tagline
        "completeness": 20,     # Full Kapferer prism + archetype + messaging + story
        "accuracy": 17,         # Archetype choice well-justified, minor: Explorer less evident
        "tone": 18              # Bold, irreverent — matches brand personality
    },
    "action": "success_pattern",
    "feedback": "Excellent brand positioning. Kapferer prism fully populated with Mar'n'Brasa specifics. Tagline is memorable and bilingual. Minor improvement: strengthen Explorer archetype evidence in narrative."
}
```

### 4. Update task YAML with score

```python
# Autopilot writes score to task file
task["quality_score"] = score_result["score"]
task["quality_dimensions"] = score_result["dimensions"]
task["quality_action"] = score_result["action"]
task["quality_feedback"] = score_result["feedback"]
write_task_atomic(task)

# Resulting task YAML on disk:
"""
id: MNB-001
title: "Brand story for Mar'n'Brasa grillhouse"
status: done
project: mar-brasa
skill: dario-brand
assignee: worker-brand
actual_tokens: 1800
completion_comment: "Brand positioning using Kapferer Prism. Archetype: The Outlaw/Explorer."
completed_at: "2026-04-27T14:00:12Z"
quality_score: 92
quality_dimensions:
  specificity: 19
  actionability: 18
  completeness: 20
  accuracy: 17
  tone: 18
quality_action: success_pattern
quality_feedback: "Excellent brand positioning. Kapferer prism fully populated..."
"""
```

### 5. Extract pattern to success-patterns.yaml

```python
# Because action == "success_pattern" (score >= 90), extract the winning pattern
PATTERNS_FILE = Path.home() / ".claude" / "orchestrator" / "quality" / "success-patterns.yaml"

new_pattern = {
    "pattern_id": "brand-positioning-restaurant-2026-04",
    "skill": "dario-brand",
    "project": "mar-brasa",
    "task_id": "MNB-001",
    "score": 92,
    "extracted_at": "2026-04-27T14:00:15Z",
    "key_factors": [
        "Full Kapferer prism with all 6 facets populated using client specifics",
        "Bilingual tagline (PT+EN) that captures brand essence",
        "Archetype justified with behavioral evidence, not just labels",
        "Messaging hierarchy: tagline → elevator → full story (progressive depth)"
    ],
    "reusable_template": "For restaurant/hospitality brands: lead with sensory physique, use food culture as bridge between local+global, define relationship as community gathering"
}

# Append to patterns file
patterns = yaml.safe_load(open(PATTERNS_FILE)) or []
patterns.append(new_pattern)
write_yaml_atomic(PATTERNS_FILE, patterns)
LOG(f"SUCCESS PATTERN: {new_pattern['pattern_id']} extracted from {task['id']}")
```

### 6. Update skill-metrics.yaml

```python
METRICS_FILE = Path.home() / ".claude" / "orchestrator" / "quality" / "skill-metrics.yaml"

metrics = yaml.safe_load(open(METRICS_FILE)) or {}

skill_key = "dario-brand"
if skill_key not in metrics:
    metrics[skill_key] = {
        "total_executions": 0,
        "total_score": 0,
        "avg_score": 0,
        "scores_history": [],
        "revision_rate": 0.0,
        "success_pattern_count": 0,
        "last_execution": None
    }

m = metrics[skill_key]
m["total_executions"] += 1
m["total_score"] += score_result["score"]
m["avg_score"] = round(m["total_score"] / m["total_executions"], 1)
m["scores_history"].append({
    "task_id": "MNB-001",
    "score": 92,
    "date": "2026-04-27"
})
m["success_pattern_count"] += 1  # Because action was success_pattern
m["last_execution"] = "2026-04-27T14:00:15Z"

# Keep only last 20 scores in history to prevent file bloat
m["scores_history"] = m["scores_history"][-20:]

write_yaml_atomic(METRICS_FILE, metrics)
LOG(f"METRICS: {skill_key} — avg {m['avg_score']}, {m['total_executions']} executions")

# Final state of skill-metrics.yaml for dario-brand:
"""
dario-brand:
  total_executions: 7
  total_score: 612
  avg_score: 87.4
  scores_history:
    - {task_id: ATR-003, score: 85, date: "2026-04-15"}
    - {task_id: ATR-007, score: 82, date: "2026-04-18"}
    - {task_id: VCH-001, score: 92, date: "2026-04-22"}
    - {task_id: MNB-001, score: 92, date: "2026-04-27"}
  revision_rate: 0.14
  success_pattern_count: 3
  last_execution: "2026-04-27T14:00:15Z"
"""
```

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — State Machine avaliada e resultado refletido na execução
- [ ] `state_machine.py --evaluate --json` foi chamado como **primeira ação** do pulse
- [ ] `max_parallel` foi lido do JSON retornado (não hardcoded)
- [ ] Se state = `GUARDIAN`, autopilot parou imediatamente e notificou o utilizador
- [ ] Se state machine falhou, degraded mode `ACTIVE / max_parallel=2` foi aplicado e logado

❌ NOT delivery-ready: "Executei 3 tasks em paralelo" — sem evidência do state check, estado pode ser REFLECTIVE_PAUSE  
✅ Delivery-ready: `STATE: ACTIVE | autonomy_level=P-A2 | max_parallel=3 | system_health=0.95 — proceeding with full wave`

---

### Gate 2 — SCAN completo com contagem real de tasks
- [ ] Leu todos os `.yaml` em `~/.claude/orchestrator/tasks/active/`
- [ ] Reportou totais por status: backlog / todo / in_progress / in_review / done / blocked
- [ ] Identificou tarefas com `depends_on` ainda não resolvidas
- [ ] Output inclui linha de scan com números concretos

❌ NOT delivery-ready: "Há algumas tasks pendentes no sistema"  
✅ Delivery-ready: `SCAN: 9 tasks total | 4 done | 1 in_progress | 3 todo | 0 backlog | 1 blocked (CUIDAI-007: awaits CUIDAI-004)`

---

### Gate 3 — Budget verificado com percentagem real e limite respeitado
- [ ] Leu `~/.claude/orchestrator/budgets/YYYY-MM.yaml` (mês corrente)
- [ ] Percentagem calculada e comparada aos thresholds 80% / 95%
- [ ] Se ≥95%: HARD STOP executado, zero tasks lançadas
- [ ] Se ≥80%: `max_parallel` reduzido para 1 e warning logado com percentagem

❌ NOT delivery-ready: "Budget OK" — sem percentagem, sem mês, sem fonte  
✅ Delivery-ready: `BUDGET: 2025-07 | 67.3% used ($134.60/$200.00) — normal operation, max_parallel=3`

---

### Gate 4 — Dispatch Engine chamado e resultado reportado
- [ ] `dispatch_engine.py --json` invocado (ou fallback inline documentado se falhou)
- [ ] JSON de output inclui `dispatched`, `queued`, `total_analyzed`
- [ ] Tarefas com `reason: NO_WORKER` foram logadas com aviso de assignment manual
- [ ] Assignee + dispatch_reason escritos nos YAMLs das tasks dispatched

❌ NOT delivery-ready: "Atribuí as tasks aos workers disponíveis" — sem prova do engine, sem task IDs  
✅ Delivery-ready: `DISPATCH: 2 dispatched | 1 queued (NO_WORKER: custom-skill) | CUIDAI-005→worker-brand (AVAILABLE), CUIDAI-006→worker-copy (SIBLING_FALLBACK)`

---

### Gate 5 — Wave executada via Agent tool com prioridade e estado corretos
- [ ] Wave limitada a `max_parallel` tasks (não mais)
- [ ] Ordenação por prioridade aplicada: critical > high > medium > low
- [ ] Cada task teve `status=in_progress` + `checked_out_at` escritos antes de lançar Agent
- [ ] Adapter correto usado (`diva-v1-design-architect` para division=diva, `dario-v2-digital-ceo` default)

❌ NOT delivery-ready: Lançou 4 tasks quando max_parallel=3, ou não registou `checked_out_at`  
✅ Delivery-ready: `WAVE: CUIDAI-002 [critical/dario], CUIDAI-005 [high/dario], CUIDAI-008 [high/diva] — checked_out 2025-07-14T09:42:11Z`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] Nenhum placeholder `<CLIENT>`, `<TASK_ID>`, `<WORKER>`, `<DATE>` no output
- [ ] Project prefix real no ID das tasks (ex: `CUIDAI-`, `SAQU-`, `ATRI-`, não `PROJ-`)
- [ ] Budget com mês/ano real e valores monetários reais
- [ ] Log lines com timestamps ISO reais, não `{timestamp}`

❌ NOT delivery-ready: `BUDGET: {percentage}% — {status}` ou `Task PROJ-001 assigned to {worker}`  
✅ Delivery-ready: `BUDGET: 2025-07 | 67.3% | SAQU-003→worker-legal (AVAILABLE) | wave launched 2025-07-14T09:42Z`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output do **lucas-autopilot** deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via state machine, task YAML, ou budget file lidos neste pulse
- 🟡 **assumed** — plausível mas precisa confirm antes de agir (ex: worker availability, skill mapping)
- 🟢 **projection** — forecast by design (estimativas de tempo, scores esperados, pulse scheduling)

Output checklist upfront mostra ao operador exactamente o que é trust-as-is vs o que precisa de validação antes de executar wave seguinte. **Honest transparency > inflated dispatch.**

---

❌ NOT delivery-ready:
```
SCAN: 12 tasks | BUDGET: 67% | Dispatched: PROJ-001 → worker-brand | Next pulse: 60s
```
*(reader assume que tudo está verified — mas worker-brand pode estar busy, budget file pode estar stale, task YAML pode ter depends_on por resolver)*

✅ Delivery-ready:
```
SCAN: 12 tasks total 🔵 verified (lidos de ~/.claude/orchestrator/tasks/active/ às 14:32)
  └─ 3 done | 2 in_progress | 4 todo | 2 backlog | 1 blocked

BUDGET: 67% spend este mês 🔵 verified (2025-07.yaml lido neste pulse)
  └─ max_parallel = 3 — budget safe

DISPATCH:
  PROJ-001 → worker-brand (dario-brand) 🟡 assumed — worker reportado AVAILABLE mas sem lock atómico confirmado
  PROJ-002 → sem assignee 🔵 verified — dispatch_engine retornou NO_WORKER para custom-skill

UNBLOCK: PROJ-005 desbloqueado 🔵 verified — todos depends_on em "done" confirmados via YAML
SCORE esperado (próximo pulse): 82/100 🟢 projection — baseado em média histórica dario-brand (5 runs)
NEXT PULSE: 60s 🟢 projection — agendado se tasks ainda em queue; cancela se GUARDIAN activar
```

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — worker availability locked antes de lançar Agent tool (substituir assumptions com estado real do worker no momento de execução)
- [ ] All 🔵 sources citadas — path do YAML + timestamp de leitura incluídos no audit log
- [ ] All 🟢 projections comunicadas ao cliente como forecast, não garantia (pulse timing e scores sujeitos a state machine transitions)

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## LUCAS Autopilot — Pulse #7 | 2025-07-14T09:42:03Z

### STATE CHECK
python state_machine.py --evaluate --json
→ { "state": "ACTIVE", "autonomy_level": "P-A2", "max_parallel": 3, "system_health": 0.91 }
Proceeding with full autonomous wave.

### SCAN
Directory: ~/.claude/orchestrator/tasks/active/ (Cuidai)
SCAN: 11 tasks total | 5 done | 1 in_progress | 4 todo | 0 backlog | 1 blocked

  done:       CUIDAI-001, CUIDAI-002, CUIDAI-003, CUIDAI-004, CUIDAI-006
  in_progress: CUIDAI-005 (worker-brand, checked_out 09:15Z)
  todo:       CUIDAI-007, CUIDAI-008, CUIDAI-009, CUIDAI-010
  blocked:    CUIDAI-011 (awaits CUIDAI-009, CUIDAI-010)

### BUDGET
File: ~/.claude/orchestrator/budgets/2025-07.yaml
Spent: $142.80 / $200.00 — 71.4%
Status: NORMAL — max_parallel=3 (no throttle applied)

### UNBLOCK CASCADE
CUIDAI-007 depends_on: [CUIDAI-003, CUIDAI-004] → both done → UNBLOCKED → status: todo
(already todo — no change needed)
CUIDAI-011 depends_on: [CUIDAI-009, CUIDAI-010] → pending → remains blocked

### DISPATCH
python dispatch_engine.py --json
→ {
    "dispatched": 3,
    "queued": 1,
    "total_analyzed": 4,
    "assignments": [
      {"task_id": "CUIDAI-007", "assigned_to": "worker-ops",   "skill": "lucas-project", "reason": "AVAILABLE"},
      {"task_id": "CUIDAI-008", "assigned_to": "worker-brand", "skill": "dario-brand",   "reason": "SIBLING_FALLBACK"},
      {"task_id": "CUIDAI-009", "assigned_to": "worker-copy",  "skill": "dario-copy",    "reason": "AVAILABLE"},
      {"task_id": "CUIDAI-010", "assigned_to": null,           "skill": "dario-legal",   "reason": "NO_WORKER"}
    ]
  }
⚠ DISPATCH WARNING: 1 task queued — CUIDAI-010 requires dario-legal, no worker available. Manual assignment needed.

### WAVE EXECUTION
Executable tasks (todo + assignee + deps done): CUIDAI-007, CUIDAI-008, CUIDAI-009
Sorted by priority: CUIDAI-008 [high], CUIDAI-007 [medium], CUIDAI-009 [medium]
Wave size: 3 (= max_parallel)

→ CUIDAI-008: status=in_progress | checked_out=2025-07-14T09:42:11Z | adapter=dario-v2-digital-ceo
   Agent: "Autopilot: CUIDAI-008 — Criar guia de identidade visual Cuidai v2"

→ CUIDAI-007: status=in_progress | checked_out=2025-07-14T09:42:12Z | adapter=dario-v2-digital-ceo
   Agent: "Autopilot: CUIDAI-007 — Mapear fluxo de onboarding cuidadores"

→ CUIDAI-009: status=in_progress | checked_out=2025-07-14T09:42:12Z | adapter=dario-v2-digital-ceo
   Agent: "Autopilot: CUIDAI-009 — Redigir FAQ para famílias plataforma Cuidai"

### AUDIT LOG
Appended to: ~/.claude/orchestrator/audit/dispatch_2025-07-14.log
  09:42:11Z | pulse=7 | state=ACTIVE | budget=71.4% | wave=3 | dispatched=3 | queued=1

### PACE
Tasks remaining after wave: 1 blocked (CUIDAI-011) + 1 queued (CUIDAI-010/NO_WORKER)
→ Scheduling next pulse in 60s (tasks in flight)
   /loop /lucas-autopilot — pulse #8 at 09:43:03Z
```

---

## Output anti-patterns

- Executar wave sem mostrar resultado do `state_machine.py` — viola Gate 1, pode violar GUARDIAN silenciosamente
- Escrever `max_parallel=3` hardcoded em vez de ler do JSON do state machine — ignora REFLECTIVE_PAUSE
- Reportar "budget OK" sem percentagem, mês e ficheiro fonte — não é auditável
- Usar IDs genéricos `PROJ-001`, `PROJ-002` em vez dos prefixos reais do cliente (CUIDAI-, SAQU-, ATRI-)
- Fazer dispatch sem invocar `dispatch_engine.py` e sem documentar que usou fallback inline
- Lançar mais tasks do que `max_parallel` porque "eram todas prioritárias"
- Não escrever `checked_out_at` no YAML antes de lançar o Agent — task fica sem timestamp de início
- Marcar task como `in_progress` só após o Agent terminar — perde rastreabilidade mid-execution
- Não logar tasks com `NO_WORKER` — ficam silenciosamente esquecidas no backlog
- Deixar `<CLIENT>`, `<DATE>`, `<PERCENTAGE>` no output final — nunca é delivery-ready com placeholders
