---
name: lucas-heartbeat
description: "LUCAS Heartbeat Engine — automatic CEO/manager heartbeat that checks the taskboard, dispatches unassigned tasks, executes waiting waves, detects stale tasks, and enforces budget limits. The autonomous nervous system of the orchestrator. Triggers on: 'heartbeat', 'pulse', 'auto-execute', 'check tasks', 'wake up', 'run next wave'."
license: MIT
---

# LUCAS Heartbeat Engine

The missing piece that transforms the orchestrator from a planning tool into an autonomous execution system. Without heartbeat, tasks sit in YAML files forever. With heartbeat, the CEO wakes up, checks the board, and makes things happen.

## When to activate

- Automatically via scheduled trigger (every 30 minutes)
- Manually via `/lucas-heartbeat`
- When user says "check tasks", "run next wave", "what's pending"
- Called by `/dario-orchestrator` to kickstart execution after decomposition

## Heartbeat Cycle (every 30 minutes)

```
PULSE START
│
├── 1. SCAN — Read all tasks in ~/.claude/orchestrator/tasks/active/
│   ├── Count by status: backlog, todo, in_progress, in_review, done, blocked
│   ├── Flag: stale (in_progress >24h without updated_at change)
│   └── Flag: SLA breached (in_progress past sla_deadline — see SLA Enforcement below)
│
├── 2. BUDGET CHECK — Read ~/.claude/orchestrator/budgets/YYYY-MM.yaml
│   ├── If >80% used → log warning, notify user
│   ├── If >95% used → PAUSE all new task execution, alert
│   └── If budget file missing → create with 0 spent
│
├── 3. UNBLOCK CASCADE — For each task with status "done":
│   ├── Find all tasks where depends_on includes this task
│   ├── Check if ALL dependencies are done
│   ├── If yes → transition to "todo" (ready for dispatch)
│   └── Log cascade events to audit
│
├── 4. AUTO-DISPATCH — For each task with status "todo" and no assignee:
│   ├── Read company.yaml → match task capabilities to workers
│   ├── Assign best worker (capability overlap + division match)
│   ├── Set assignee, status stays "todo"
│   └── Log dispatch to audit
│
├── 5. WAVE PLANNING — Group assigned "todo" tasks:
│   ├── Identify independent tasks (no mutual depends_on)
│   ├── Create waves (max 3 per wave)
│   └── Execute Wave 1 immediately via Agent tool (parallel)
│
├── 6. EXECUTE WAVE — For each task in current wave:
│   ├── Set status → "in_progress"
│   ├── Set checked_out_at → now
│   ├── Launch Agent({ subagent_type, prompt with task context })
│   ├── On completion: set completion_comment, check execution_policy
│   ├── If policy requires review → status "in_review"
│   ├── If no review needed → status "done"
│   └── Update actual_tokens, log to audit + budget
│
├── 7. STALE DETECTION — For tasks in_progress >24h:
│   ├── Log stale alert
│   ├── Add note to task: "STALE — no progress in 24h"
│   └── If >48h → escalate to CEO (mark as blocked, add reason)
│
├── 8. REPORT — Generate pulse summary:
│   ├── Tasks executed this pulse: N
│   ├── Tasks waiting: N
│   ├── Tasks stale: N
│   ├── Budget used: X% (N tokens / limit)
│   └── Next wave ready: [task IDs]
│
└── PULSE END — Write pulse timestamp to ~/.claude/orchestrator/last_pulse.yaml
```

## Heartbeat Configuration (from company.yaml)

```yaml
heartbeat_defaults:
  manager:
    interval_minutes: 30    # CEO checks every 30 min
    cooldown_minutes: 5     # Min time between pulses
    coalesce_if_active: true # Don't overlap pulses
  worker:
    interval_minutes: 0     # Workers don't self-wake
    cooldown_minutes: 2
  service:
    interval_minutes: 5     # Services check often
    cooldown_minutes: 1
```

## Budget Enforcement

At each pulse, read and update `~/.claude/orchestrator/budgets/YYYY-MM.yaml`:

```yaml
month: "2026-04"
company: "BARDA Digital Agency"
total_tokens_used: 125000
limit: 50000000
percentage_used: 0.25
by_project:
  mar-brasa: 34000
  atrium: 45000
  vivenda: 30000
by_agent:
  worker-brand: 8000
  worker-seo-local: 12000
  worker-seo-plan: 14000
by_skill:
  dario-brand: 8000
  seo-local: 12000
  seo-plan: 14000
alert_80_sent: false
alert_95_sent: false
last_updated: "2026-04-27T09:30:00Z"
```

**Token counting:** After each Agent tool execution, the usage metadata includes `total_tokens`. Capture this and add to budget.

## Stale Task Escalation

| Age | Action |
|---|---|
| 0-24h | Normal — task in progress |
| 24-48h | Flag as STALE, add warning note |
| 48-72h | Escalate to director (reassign or unblock) |
| >72h | Escalate to CEO, mark as blocked |

## Coalescing

If a heartbeat is already running when a new trigger fires:
- **coalesce_if_active: true** → Merge: skip the new pulse, let the active one finish
- This prevents duplicate work and runaway token burn

## Integration Points

### With dario-orchestrator
- Heartbeat is the EXECUTION ENGINE of the orchestrator
- Orchestrator decomposes → creates tasks → heartbeat executes them
- Without heartbeat, orchestrator is a planner only

### With dario-taskboard
- Heartbeat reads task YAML files
- Heartbeat writes status updates, assignees, timestamps
- Heartbeat moves completed tasks to done/

### With dario-dispatch
- Heartbeat calls dispatch logic for unassigned tasks
- Dispatch returns worker assignment
- Heartbeat writes assignment to task YAML

### With lucas-quality-scorer
- After task execution, heartbeat triggers quality evaluation
- Quality score written to task YAML
- Low scores flagged for review

### With lucas-cost-tracker
- After each execution, heartbeat reports token usage
- Budget file updated
- Alerts triggered if needed

## Scheduling the Heartbeat

### Option A: /schedule (Remote Trigger)
```bash
/schedule create --name "dario-ceo-heartbeat" --cron "*/30 * * * *" --prompt "/lucas-heartbeat"
```

### Option B: /loop (Dynamic Self-Pacing)
```bash
/loop /lucas-heartbeat
```
The heartbeat self-paces: if there are pending tasks, wake up in 60s. If idle, wake up in 1800s.

### Option C: Manual
```bash
/lucas-heartbeat
```

## Output Template

```markdown
## LUCAS Pulse — YYYY-MM-DD HH:MM

| Metric | Value |
|---|---|
| Tasks scanned | 15 |
| Executed this pulse | 3 |
| Waiting (todo) | 4 |
| In progress | 2 |
| Stale (>24h) | 1 |
| Blocked | 0 |
| Done (total) | 6 |
| Budget used | 12.5% (125K / 1M) |
| Next wave | [PROJ-007, PROJ-008] |

### Executed
- PROJ-004: Brand story → done (quality: 85/100, tokens: 2100)
- PROJ-005: SEO local → done (quality: 90/100, tokens: 3200)
- PROJ-006: Content plan → in_review (awaiting director review)

### Alerts
- PROJ-003 STALE: in_progress for 26h, no update. Escalating to dir-marketing.

### Next Pulse
Scheduled in 30 minutes (or 60s if pending tasks exist).
```

## SLA Enforcement (Task Timeout Detection)

Every heartbeat pulse checks task SLA compliance. SLAs are set by `dario-dispatch` at assignment time, or derived from the execution policy.

### SLA Timeouts

| Execution Policy | SLA Duration | Timeout Action |
|---|---|---|
| `critical` | 1 hour | Auto-escalate to CEO + block + notify all watchers |
| `client_facing` | 4 hours | Flag as stale + notify director + add to pulse report |
| `financial` | 2 hours | Auto-escalate to CEO + block until user reviews |
| `default` | 8 hours | Flag as stale in pulse report |

### Enforcement Logic (runs in Step 1 of every pulse)

```python
SLA_HOURS = {"critical": 1, "client_facing": 4, "financial": 2, "default": 8}

for task in tasks where status == "in_progress":
    sla_duration = SLA_HOURS.get(task.execution_policy, 8)
    age_hours = (now() - task.checked_out_at).total_hours()
    
    if age_hours > sla_duration * 2:
        # CRITICAL BREACH — double the SLA
        task.status = "blocked"
        task.blocked_reason = f"SLA critical breach: {age_hours:.1f}h vs {sla_duration}h limit. Requires user intervention."
        task.watchers.append("dario-ceo")
        task.assignee = None  # Release atomic checkout
        LOG "SLA CRITICAL: {task.id} — {age_hours:.1f}h, 2x SLA exceeded. Task blocked."
        
    elif age_hours > sla_duration:
        # SLA BREACH — past deadline
        if task.execution_policy in ["critical", "financial"]:
            task.status = "blocked"
            task.blocked_reason = f"SLA breach: {age_hours:.1f}h vs {sla_duration}h limit."
            LOG "SLA ESCALATED: {task.id} — escalated to CEO"
        else:
            # Soft breach — flag but don't block
            task.notes.append(f"SLA WARNING: {age_hours:.1f}h in progress, SLA is {sla_duration}h")
            LOG "SLA WARNING: {task.id} — {age_hours:.1f}h, past {sla_duration}h SLA"
    
    UPDATE task YAML
```

### Pulse Report SLA Section

```markdown
### SLA Status
| Task | Policy | Age | SLA | Status |
|---|---|---|---|---|
| PROJ-001 | critical | 0.5h | 1h | OK |
| PROJ-003 | client_facing | 5.2h | 4h | BREACH — flagged |
| PROJ-005 | financial | 3.1h | 2h | BLOCKED — escalated |
```

## Red Flags

- Never run two heartbeats simultaneously (coalescing prevents this)
- Never execute tasks if budget >95% (hard stop)
- Never skip stale detection — it's the safety net
- Never auto-approve critical tasks — always ask user
- If heartbeat fails mid-execution, tasks stay in_progress (next pulse retries)
- **Never ignore SLA breaches** — they indicate stuck or failed execution
- **Double SLA breach = auto-block** — no exceptions, the task is abandoned

---

## Pulse Execution — Worked Example

A complete pulse cycle with real task IDs from the MNB (Mar'n'Brasa) project:

```
PULSE 2026-04-27 09:30:00
├── SCAN: 8 tasks found (2 done, 3 todo, 1 in_progress, 1 blocked, 1 in_review)
│   ├── done: MNB-001 (brand-story), MNB-002 (seo-local)
│   ├── todo: MNB-004 (story-circle), MNB-005 (content-plan), MNB-006 (social-calendar)
│   ├── in_progress: MNB-003 (grand-slam-offer) — 26h elapsed
│   ├── blocked: MNB-007 (email-sequence) — depends on MNB-004
│   └── in_review: MNB-008 (landing-page-copy) — awaiting dir-marketing
├── BUDGET: 0.32% used (160K/50M) — OK
├── UNBLOCK: MNB-004 unblocked (deps MNB-001+MNB-002 now done)
├── STALE: MNB-003 in_progress for 26h — flagging
├── SLA CHECK: MNB-003 client_facing, 26h > 4h SLA — BREACH
│   └── Added note: "SLA WARNING: 26.0h in progress, SLA is 4h"
├── DISPATCH: MNB-004 → worker-story-circle (capability match: 3/3)
│   └── MNB-005 → worker-seo-plan (capability match: 2/2)
├── WAVE: [MNB-004, MNB-005] — 2 parallel (independent, no mutual depends_on)
│   └── MNB-006 deferred (depends on MNB-005)
├── EXECUTE: Agent(MNB-004), Agent(MNB-005)
│   ├── MNB-004: checked_out_at=09:30:01, adapter=dario-v2-digital-ceo
│   └── MNB-005: checked_out_at=09:30:01, adapter=dario-v2-digital-ceo
├── RESULT: MNB-004 done (2100 tokens), MNB-005 done (3400 tokens)
│   ├── MNB-004: completion_comment="Story circle 8-beat narrative for Mar'n'Brasa grillhouse"
│   └── MNB-005: completion_comment="90-day content plan: 12 pillar posts + 36 clusters"
├── QUALITY: invoke lucas-quality
│   ├── MNB-004: 88/100 → action: "ship"
│   └── MNB-005: 91/100 → action: "success_pattern" (extracted to patterns)
├── BUDGET UPDATE: +5500 tokens → 165.5K total (0.33%)
├── AUDIT: 8 entries appended to 2026-04-27.yaml
│   └── pulse_executed, dispatch x2, execute x2, quality x2, budget_update, unblock
└── NEXT: MNB-006 now unblocked (MNB-005 done) → 1 task remaining → pulse in 90s
```

---

## Error Handling Playbook

| # | Error | Detection | Recovery | Escalation |
|---|---|---|---|---|
| 1 | **Agent timeout** | Agent tool returns no response after 120s | Retry once with same prompt. If second timeout, set task status → `blocked`, reason: "agent_timeout_2x" | Add `dario-ceo` to watchers. Log to audit. Alert user on next pulse report. |
| 2 | **YAML corrupt** | `yaml.safe_load()` raises `ScannerError` or `ParserError` | Skip corrupted file. Log filename + error. Continue pulse with remaining tasks. Attempt auto-repair: read raw text, strip invalid chars, retry parse. | If auto-repair fails, copy corrupt file to `~/.claude/orchestrator/tasks/corrupt/` and remove from active/. Alert user. |
| 3 | **Budget file missing** | `FileNotFoundError` when reading `budgets/YYYY-MM.yaml` | Create fresh budget file with `total_tokens_used: 0`, `limit: 50000000`, current month. Continue pulse. | Log warning. No escalation needed — self-healing. |
| 4 | **Worker not found** | `find_worker_by_skill()` returns `None` for task skill | Leave task as `todo` with `assignee: null`. Add note: "No worker with capability: {skill}". Skip dispatch for this task. | After 3 consecutive pulses with unmatched task, escalate to CEO. Suggest adding worker to company.yaml. |
| 5 | **Circular dependency** | Cycle detected during unblock cascade (A→B→C→A) | Mark ALL tasks in cycle as `blocked`, reason: "circular_dependency_detected: [task_ids]". Break cycle by clearing `depends_on` on the lowest-priority task. | Immediate CEO alert. Log full dependency graph to audit. Require user to manually resolve. |
| 6 | **Task already claimed** | Task has `checked_out_at` set and `status: in_progress` when pulse tries to execute | Skip task. Another pulse or manual execution owns it. Check coalescing flag. | If task has been claimed for >SLA hours, treat as stale per normal escalation rules. |
| 7 | **RAG unavailable** | `search_kb` returns connection error or timeout to localhost:8420 | Execute tasks without RAG context injection. Add note to task: "executed_without_rag_context". Log warning. | If RAG has been down for 3+ consecutive pulses, attempt restart: `cd /c/dario-rag/engine && .venv/Scripts/python.exe main.py &`. Alert user. |
| 8 | **Quality service unreachable** | `invoke_lucas_quality()` returns error or empty response | Set task to `done` without quality score. Add `quality_score: null`, note: "quality_scoring_unavailable". | Tasks without scores flagged in next pulse report. Batch-score them when service recovers. |

---

## Task YAML Read/Write Contract

### Reading all task files from active/

```python
import os
import yaml
from pathlib import Path
from datetime import datetime, timezone

TASKS_DIR = Path.home() / ".claude" / "orchestrator" / "tasks" / "active"

def read_all_tasks() -> list[dict]:
    """Read and parse all task YAML files from the active directory."""
    tasks = []
    
    if not TASKS_DIR.exists():
        LOG("WARNING: tasks/active/ directory does not exist. Creating.")
        TASKS_DIR.mkdir(parents=True, exist_ok=True)
        return tasks
    
    for filepath in TASKS_DIR.glob("*.yaml"):
        task = read_task_safe(filepath)
        if task is not None:
            task["_filepath"] = str(filepath)  # Track source file
            tasks.append(task)
    
    return tasks
```

### Parsing YAML safely (try/except with fallback)

```python
def read_task_safe(filepath: Path) -> dict | None:
    """Parse a task YAML file with error recovery."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()
        
        task = yaml.safe_load(raw)
        
        if not isinstance(task, dict):
            LOG(f"WARNING: {filepath.name} did not parse as dict. Skipping.")
            return None
        
        # Validate required fields
        required = ["id", "title", "status"]
        for field in required:
            if field not in task:
                LOG(f"WARNING: {filepath.name} missing required field '{field}'. Skipping.")
                return None
        
        return task
    
    except yaml.YAMLError as e:
        LOG(f"ERROR: YAML parse failed for {filepath.name}: {e}")
        # Attempt fallback: try loading with allow_duplicate_keys
        try:
            task = yaml.safe_load(raw.replace("\t", "  "))  # Fix tab issues
            if isinstance(task, dict):
                LOG(f"RECOVERED: {filepath.name} parsed after tab replacement.")
                return task
        except Exception:
            pass
        # Move to corrupt/
        corrupt_dir = filepath.parent.parent / "corrupt"
        corrupt_dir.mkdir(exist_ok=True)
        filepath.rename(corrupt_dir / filepath.name)
        LOG(f"MOVED: {filepath.name} → corrupt/ (unrecoverable parse error)")
        return None
    
    except Exception as e:
        LOG(f"ERROR: Unexpected error reading {filepath.name}: {e}")
        return None
```

### Writing task mutations atomically (write to .tmp then rename)

```python
def write_task_atomic(task: dict, filepath: Path = None) -> bool:
    """Write task YAML atomically: write .tmp then rename to prevent corruption."""
    if filepath is None:
        filepath = Path(task["_filepath"])
    
    # Remove internal tracking fields before writing
    write_data = {k: v for k, v in task.items() if not k.startswith("_")}
    write_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    tmp_path = filepath.with_suffix(".yaml.tmp")
    
    try:
        # Write to temporary file
        with open(tmp_path, "w", encoding="utf-8") as f:
            yaml.dump(write_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        # Atomic rename (on Windows, remove target first if exists)
        if filepath.exists():
            filepath.unlink()
        tmp_path.rename(filepath)
        
        LOG(f"WRITTEN: {filepath.name} (status: {write_data.get('status')})")
        return True
    
    except Exception as e:
        LOG(f"ERROR: Failed to write {filepath.name}: {e}")
        # Clean up tmp file if it exists
        if tmp_path.exists():
            tmp_path.unlink()
        return False
```

### Updating budget after execution

```python
BUDGET_DIR = Path.home() / ".claude" / "orchestrator" / "budgets"

def update_budget(tokens_used: int, project: str, agent: str, skill: str) -> dict:
    """Update the monthly budget file after task execution."""
    now = datetime.now(timezone.utc)
    budget_file = BUDGET_DIR / f"{now.strftime('%Y-%m')}.yaml"
    
    # Read or create budget
    if budget_file.exists():
        with open(budget_file, "r", encoding="utf-8") as f:
            budget = yaml.safe_load(f) or {}
    else:
        BUDGET_DIR.mkdir(parents=True, exist_ok=True)
        budget = {
            "month": now.strftime("%Y-%m"),
            "company": "BARDA Digital Agency",
            "total_tokens_used": 0,
            "limit": 50000000,
            "percentage_used": 0.0,
            "by_project": {},
            "by_agent": {},
            "by_skill": {},
            "alert_80_sent": False,
            "alert_95_sent": False,
        }
    
    # Update totals
    budget["total_tokens_used"] = budget.get("total_tokens_used", 0) + tokens_used
    budget["percentage_used"] = round(budget["total_tokens_used"] / budget["limit"] * 100, 4)
    budget["last_updated"] = now.isoformat()
    
    # Update breakdowns
    budget.setdefault("by_project", {})[project] = budget["by_project"].get(project, 0) + tokens_used
    budget.setdefault("by_agent", {})[agent] = budget["by_agent"].get(agent, 0) + tokens_used
    budget.setdefault("by_skill", {})[skill] = budget["by_skill"].get(skill, 0) + tokens_used
    
    # Write atomically
    tmp_path = budget_file.with_suffix(".yaml.tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        yaml.dump(budget, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    if budget_file.exists():
        budget_file.unlink()
    tmp_path.rename(budget_file)
    
    LOG(f"BUDGET: +{tokens_used} tokens → {budget['total_tokens_used']} total ({budget['percentage_used']}%)")
    return budget
```

---

## Integration Contracts

### dario-dispatch

**Purpose:** Maps unassigned tasks to the optimal worker based on capabilities.

**Invocation:**
```python
# Input: task dict with at minimum {id, skill, division, priority}
dispatch_input = {
    "task_id": "MNB-004",
    "skill_required": "dario-story-circle",
    "division": "dario",
    "priority": "high",
    "project": "mar-brasa",
    "execution_policy": "client_facing"
}

# Call pattern (within heartbeat):
worker = dispatch_task(dispatch_input)

# Output on success:
{
    "worker_id": "worker-story-circle",
    "worker_name": "Story Circle Specialist",
    "capability_match": 3,  # out of required capabilities
    "capability_total": 3,
    "division_match": True,
    "confidence": 1.0
}

# Output on failure:
{
    "worker_id": None,
    "reason": "no_worker_with_capability",
    "skill_required": "dario-story-circle",
    "suggestion": "Add worker with skill 'dario-story-circle' to company.yaml"
}
```

**Error Handling:**
- If dispatch returns `worker_id: None`, task stays as `todo` unassigned
- If company.yaml is unreadable, skip dispatch step entirely, log error
- Never assign a worker from a different division unless `cross_division: true` in task

### lucas-quality

**Purpose:** Evaluates completed task outputs against a 5-dimension rubric.

**Invocation:**
```python
# Input: completed task with output
quality_input = {
    "task_id": "MNB-004",
    "task_title": "Brand story circle for Mar'n'Brasa",
    "skill_used": "dario-story-circle",
    "project": "mar-brasa",
    "execution_policy": "client_facing",
    "completion_comment": "Story circle 8-beat narrative for Mar'n'Brasa grillhouse...",
    "output_text": "<full agent output>",
    "revision_count": 0,
    "revision_max_loops": 3
}

# Call pattern:
score_result = invoke_lucas_quality(quality_input)

# Output:
{
    "score": 88,
    "dimensions": {
        "specificity": 18,      # /20 — mentions Mar'n'Brasa, Lisbon, grillhouse
        "actionability": 17,    # /20 — clear next steps for copy team
        "completeness": 19,     # /20 — all 8 beats of story circle covered
        "accuracy": 16,         # /20 — brand values aligned
        "tone": 18              # /20 — warm, inviting, premium casual
    },
    "action": "ship",           # ship | revision | success_pattern | escalate
    "feedback": "Strong narrative arc. Minor: beat 5 could reference specific menu items."
}
```

**Error Handling:**
- If quality returns empty/error → task marked `done` without score, flagged for batch scoring
- If `action` is not in `["ship", "revision", "success_pattern", "escalate"]` → default to "ship", log warning
- If `score` is not int 0-100 → discard, log error, treat as "ship"

### budget_tracker.py

**Purpose:** CLI tool to query and update budget state.

**Invocation (after each pulse):**
```bash
# Report token usage for a completed task
python ~/.claude/orchestrator/scripts/budget_tracker.py add \
    --tokens 2100 \
    --project mar-brasa \
    --agent worker-story-circle \
    --skill dario-story-circle \
    --task-id MNB-004

# Check budget status (returns JSON to stdout)
python ~/.claude/orchestrator/scripts/budget_tracker.py status
# Output: {"percentage": 0.33, "total": 165500, "limit": 50000000, "alert_level": "ok"}

# Get remaining budget for a project
python ~/.claude/orchestrator/scripts/budget_tracker.py remaining --project mar-brasa
# Output: {"project": "mar-brasa", "used": 34000, "remaining": 49966000}
```

**Error Handling:**
- If script not found → fallback to inline YAML read/write (see update_budget function above)
- If budget file locked → retry once after 1s, then skip budget update and log warning
- Never fail the entire pulse due to budget tracking error — log and continue

---

## Pulse Report Template (Pro)

```markdown
## LUCAS Pulse Report — 2026-04-27 09:30

### Summary
| Metric | Value |
|---|---|
| Pulse ID | pulse-2026-04-27-0930 |
| Duration | 14.2s |
| Tasks scanned | 8 |
| Executed this pulse | 2 |
| Quality scored | 2 |
| Unblocked | 1 |
| Stale flagged | 1 |
| SLA breaches | 1 |
| Budget used | 0.33% (165.5K / 50M) |

### Execution Wave
| Task | Skill | Worker | Tokens | Quality | Action |
|---|---|---|---|---|---|
| MNB-004 | dario-story-circle | worker-story-circle | 2,100 | 88/100 | ship |
| MNB-005 | seo-plan | worker-seo-plan | 3,400 | 91/100 | success_pattern |

### Unblock Cascade
| Task | Was Blocked By | Now Status |
|---|---|---|
| MNB-004 | MNB-001, MNB-002 (both done) | todo → dispatched → executed → done |
| MNB-006 | MNB-005 (now done) | blocked → todo (ready for next wave) |

### Stale & SLA Alerts
| Task | Policy | Age | SLA Limit | Status | Action Taken |
|---|---|---|---|---|---|
| MNB-003 | client_facing | 26.0h | 4h | BREACH | Note added, flagged in report |

### Dispatch Log
| Task | Assigned To | Match Score | Method |
|---|---|---|---|
| MNB-004 | worker-story-circle | 3/3 capabilities | auto-dispatch |
| MNB-005 | worker-seo-plan | 2/2 capabilities | auto-dispatch |

### Budget Delta
| Item | Tokens | Running Total |
|---|---|---|
| MNB-004 execution | +2,100 | 162,100 |
| MNB-005 execution | +3,400 | 165,500 |
| **Pulse total** | **+5,500** | **165,500 (0.33%)** |

### Quality Patterns Extracted
- **MNB-005** (91/100): Pattern "seo-plan-with-clusters" added to success-patterns.yaml
  - Key factor: specificity dimension 19/20 — named exact cluster topics for Mar'n'Brasa

### Next Pulse
- **When:** 90 seconds (tasks pending: MNB-006)
- **Wave candidates:** [MNB-006] — social calendar (depends on MNB-005 ✓)
- **Blocked tasks:** MNB-007 (depends on MNB-004 ✓, will unblock next pulse)
- **In review:** MNB-008 (awaiting dir-marketing manual review)

### Audit Trail (this pulse)
```yaml
- {ts: "2026-04-27T09:30:00Z", actor: lucas-heartbeat, action: pulse_start}
- {ts: "2026-04-27T09:30:01Z", actor: lucas-heartbeat, action: unblock, task: MNB-004, reason: "deps MNB-001+MNB-002 done"}
- {ts: "2026-04-27T09:30:01Z", actor: lucas-heartbeat, action: sla_breach, task: MNB-003, age: "26.0h", sla: "4h"}
- {ts: "2026-04-27T09:30:02Z", actor: dario-dispatch, action: assign, task: MNB-004, worker: worker-story-circle}
- {ts: "2026-04-27T09:30:02Z", actor: dario-dispatch, action: assign, task: MNB-005, worker: worker-seo-plan}
- {ts: "2026-04-27T09:30:03Z", actor: lucas-heartbeat, action: execute_start, wave: [MNB-004, MNB-005]}
- {ts: "2026-04-27T09:30:10Z", actor: lucas-heartbeat, action: execute_done, task: MNB-004, tokens: 2100}
- {ts: "2026-04-27T09:30:12Z", actor: lucas-heartbeat, action: execute_done, task: MNB-005, tokens: 3400}
- {ts: "2026-04-27T09:30:13Z", actor: lucas-quality, action: score, task: MNB-004, score: 88, action_taken: ship}
- {ts: "2026-04-27T09:30:13Z", actor: lucas-quality, action: score, task: MNB-005, score: 91, action_taken: success_pattern}
- {ts: "2026-04-27T09:30:14Z", actor: lucas-heartbeat, action: budget_update, delta: 5500, total: 165500}
- {ts: "2026-04-27T09:30:14Z", actor: lucas-heartbeat, action: pulse_end, next_in: "90s"}
```
```
