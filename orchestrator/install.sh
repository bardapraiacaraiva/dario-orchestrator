#!/usr/bin/env bash
# ============================================================================
# Agent Orchestrator — White-Label Installer
# ============================================================================
# Paperclip-inspired control plane for Claude Code agent ecosystems.
# Installs: orchestrator skills, taskboard, dispatch, company config,
#           directory structure, and CLAUDE.md integration.
#
# Usage:
#   bash install.sh                    # Interactive mode
#   bash install.sh --company "Acme"   # Quick install with company name
#   bash install.sh --preset agency    # Use a preset (agency, saas, studio)
#   bash install.sh --validate         # Check existing installation integrity
#   bash install.sh --uninstall        # Remove orchestrator
#
# Compatible with: Windows (Git Bash/MSYS2), macOS, Linux
# Requires: Claude Code CLI installed
# ============================================================================

set -euo pipefail

# --- Version ---
VERSION="1.0.0"
PRODUCT_NAME="Agent Orchestrator"

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# --- Detect OS and set paths ---
detect_platform() {
    case "$(uname -s)" in
        MINGW*|MSYS*|CYGWIN*) PLATFORM="windows" ;;
        Darwin*)               PLATFORM="macos" ;;
        Linux*)                PLATFORM="linux" ;;
        *)                     PLATFORM="unknown" ;;
    esac

    CLAUDE_HOME="${HOME}/.claude"

    SKILLS_DIR="${CLAUDE_HOME}/skills"
    ORCH_DIR="${CLAUDE_HOME}/orchestrator"
}

# --- Banner ---
print_banner() {
    echo -e "${CYAN}"
    cat << 'BANNER'
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║     AGENT ORCHESTRATOR                                ║
    ║     Paperclip-Inspired Control Plane for Claude Code  ║
    ║                                                       ║
    ║     Heartbeats · Tasks · Dispatch · Audit · Budget    ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
BANNER
    echo -e "${NC}"
    echo -e "    ${BOLD}Version ${VERSION}${NC} | Platform: ${PLATFORM}"
    echo ""
}

# --- Helpers ---
log_info()    { echo -e "  ${BLUE}[INFO]${NC}  $1"; }
log_success() { echo -e "  ${GREEN}[OK]${NC}    $1"; }
log_warn()    { echo -e "  ${YELLOW}[WARN]${NC}  $1"; }
log_error()   { echo -e "  ${RED}[ERROR]${NC} $1"; }
log_step()    { echo -e "\n  ${BOLD}${CYAN}>> $1${NC}"; }

# --- Check prerequisites ---
check_prereqs() {
    log_step "Checking prerequisites"

    # Check Claude Code
    if command -v claude >/dev/null 2>&1; then
        log_success "Claude Code CLI found"
    else
        log_error "Claude Code CLI not found. Install from https://claude.ai/code"
        exit 1
    fi

    # Check .claude directory
    if [[ -d "$CLAUDE_HOME" ]]; then
        log_success "Claude home directory found: $CLAUDE_HOME"
    else
        log_info "Creating Claude home directory: $CLAUDE_HOME"
        mkdir -p "$CLAUDE_HOME"
    fi

    # Check skills directory
    if [[ -d "$SKILLS_DIR" ]]; then
        local skill_count
        skill_count=$(ls -d "$SKILLS_DIR"/*/ 2>/dev/null | wc -l)
        log_success "Skills directory found ($skill_count existing skills)"
    else
        log_info "Creating skills directory"
        mkdir -p "$SKILLS_DIR"
    fi
}

# --- Parse arguments ---
COMPANY_NAME=""
COMPANY_GOAL=""
OWNER_NAME=""
PRESET=""
DIVISIONS=""
UNINSTALL=false
VALIDATE=false
NONINTERACTIVE=false

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --company)     COMPANY_NAME="$2"; shift 2 ;;
            --goal)        COMPANY_GOAL="$2"; shift 2 ;;
            --owner)       OWNER_NAME="$2"; shift 2 ;;
            --preset)      PRESET="$2"; shift 2 ;;
            --divisions)   DIVISIONS="$2"; shift 2 ;;
            --uninstall)   UNINSTALL=true; shift ;;
            --validate)    VALIDATE=true; shift ;;
            --yes|-y)      NONINTERACTIVE=true; shift ;;
            --help|-h)     show_help; exit 0 ;;
            --version|-v)  echo "$VERSION"; exit 0 ;;
            *)             log_error "Unknown option: $1"; show_help; exit 1 ;;
        esac
    done
}

show_help() {
    cat << 'HELP'
Usage: bash install.sh [OPTIONS]

Options:
  --company NAME     Company/agency name (default: interactive prompt)
  --goal TEXT        Company mission/goal statement
  --owner NAME       Owner username
  --preset TYPE      Use a preset: agency, saas, studio, freelancer
  --divisions LIST   Comma-separated divisions: marketing,technical,seo,finance,design
  --yes, -y          Non-interactive mode (accept defaults)
  --uninstall        Remove orchestrator (keeps skills)
  --validate         Check existing installation integrity
  --help, -h         Show this help
  --version, -v      Show version

Presets:
  agency      Digital agency (marketing + technical + SEO + finance)
  saas        SaaS company (engineering + product + growth + finance)
  studio      Design studio (design + construction + regulatory)
  freelancer  Solo freelancer (all-in-one, minimal hierarchy)

Examples:
  bash install.sh                                    # Interactive
  bash install.sh --company "Acme Digital" --preset agency
  bash install.sh --company "ArchStudio" --preset studio --owner "john"
HELP
}

# --- Uninstall ---
do_uninstall() {
    log_step "Uninstalling Agent Orchestrator"

    if [[ -d "$ORCH_DIR" ]]; then
        rm -rf "$ORCH_DIR"
        log_success "Removed orchestrator directory"
    fi

    for skill in "orchestrator" "taskboard" "dispatch"; do
        local skill_dir="${SKILLS_DIR}/${skill}"
        if [[ -d "$skill_dir" ]]; then
            rm -rf "$skill_dir"
            log_success "Removed skill: $skill"
        fi
    done

    log_success "Uninstall complete (existing skills preserved)"
    exit 0
}

# --- Validate existing installation ---
do_validate() {
    log_step "Validating Agent Orchestrator installation"

    local errors=0

    # Check required directories
    local required_dirs=(
        "$ORCH_DIR"
        "$ORCH_DIR/tasks/active"
        "$ORCH_DIR/tasks/done"
        "$ORCH_DIR/tasks/templates"
        "$ORCH_DIR/audit"
        "$ORCH_DIR/budgets"
        "$SKILLS_DIR/orchestrator"
        "$SKILLS_DIR/taskboard"
        "$SKILLS_DIR/dispatch"
    )
    for dir in "${required_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            log_success "Directory exists: $dir"
        else
            log_error "Missing directory: $dir"
            ((errors++))
        fi
    done

    # Check company.yaml exists, is not empty, and contains expected key
    local config="$ORCH_DIR/company.yaml"
    if [[ -f "$config" ]]; then
        if [[ -s "$config" ]]; then
            if grep -q '^company:' "$config"; then
                log_success "company.yaml valid (contains company: key)"
            else
                log_error "company.yaml missing 'company:' key"
                ((errors++))
            fi
        else
            log_error "company.yaml is empty"
            ((errors++))
        fi
    else
        log_error "company.yaml not found"
        ((errors++))
    fi

    # Check skill files
    local skills=("orchestrator" "taskboard" "dispatch")
    for skill in "${skills[@]}"; do
        local skill_file="${SKILLS_DIR}/${skill}/SKILL.md"
        if [[ -f "$skill_file" && -s "$skill_file" ]]; then
            log_success "Skill installed: $skill"
        else
            log_error "Skill missing or empty: $skill ($skill_file)"
            ((errors++))
        fi
    done

    # Count total skills in skills directory
    local skill_count=0
    if [[ -d "$SKILLS_DIR" ]]; then
        skill_count=$(find "$SKILLS_DIR" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l)
    fi
    log_info "Total skills installed: $skill_count"

    # Summary
    echo ""
    if [[ $errors -eq 0 ]]; then
        log_success "Validation passed — installation is intact"
        exit 0
    else
        log_error "Validation found $errors issue(s)"
        exit 1
    fi
}

# --- Interactive setup ---
interactive_setup() {
    if [[ "$NONINTERACTIVE" == true ]]; then
        COMPANY_NAME="${COMPANY_NAME:-My Agency}"
        COMPANY_GOAL="${COMPANY_GOAL:-Deliver excellent digital solutions}"
        OWNER_NAME="${OWNER_NAME:-$(whoami)}"
        PRESET="${PRESET:-agency}"
        return
    fi

    echo ""
    log_step "Company Configuration"
    echo ""

    if [[ -z "$COMPANY_NAME" ]]; then
        read -p "    Company name: " COMPANY_NAME
        COMPANY_NAME="${COMPANY_NAME:-My Agency}"
    fi

    if [[ -z "$OWNER_NAME" ]]; then
        read -p "    Owner username [$(whoami)]: " OWNER_NAME
        OWNER_NAME="${OWNER_NAME:-$(whoami)}"
    fi

    if [[ -z "$COMPANY_GOAL" ]]; then
        read -p "    Company goal/mission (1 line): " COMPANY_GOAL
        COMPANY_GOAL="${COMPANY_GOAL:-Deliver excellent digital solutions for our clients}"
    fi

    if [[ -z "$PRESET" ]]; then
        echo ""
        echo "    Available presets:"
        echo "      ${BOLD}1) agency${NC}      — Digital agency (marketing + technical + SEO + finance)"
        echo "      ${BOLD}2) saas${NC}        — SaaS company (engineering + product + growth + finance)"
        echo "      ${BOLD}3) studio${NC}      — Design studio (design + construction + regulatory)"
        echo "      ${BOLD}4) freelancer${NC}  — Solo freelancer (minimal hierarchy)"
        echo "      ${BOLD}5) custom${NC}      — Pick your own divisions"
        echo ""
        read -p "    Choose preset [1]: " preset_choice
        case "${preset_choice:-1}" in
            1) PRESET="agency" ;;
            2) PRESET="saas" ;;
            3) PRESET="studio" ;;
            4) PRESET="freelancer" ;;
            5) PRESET="custom" ;;
            *) PRESET="agency" ;;
        esac
    fi

    if [[ "$PRESET" == "custom" && -z "$DIVISIONS" ]]; then
        echo ""
        echo "    Available divisions (comma-separated):"
        echo "      marketing, technical, seo, finance, design, construction,"
        echo "      regulatory, saas-engineering, accounting, client-success"
        echo ""
        read -p "    Divisions: " DIVISIONS
        DIVISIONS="${DIVISIONS:-marketing,technical,seo}"
    fi
}

# --- Get preset divisions ---
get_preset_divisions() {
    case "$PRESET" in
        agency)      echo "marketing,technical,seo,finance,client-success" ;;
        saas)        echo "saas-engineering,marketing,finance,client-success" ;;
        studio)      echo "design,construction,regulatory,client-success" ;;
        freelancer)  echo "marketing,technical,seo" ;;
        custom)      echo "$DIVISIONS" ;;
        *)           echo "marketing,technical,seo,finance" ;;
    esac
}

# --- Create directory structure ---
create_directories() {
    log_step "Creating directory structure"

    local dirs=(
        "$ORCH_DIR/tasks/active"
        "$ORCH_DIR/tasks/done"
        "$ORCH_DIR/tasks/templates"
        "$ORCH_DIR/audit"
        "$ORCH_DIR/budgets"
        "$SKILLS_DIR/orchestrator"
        "$SKILLS_DIR/taskboard"
        "$SKILLS_DIR/dispatch"
    )

    for dir in "${dirs[@]}"; do
        if ! mkdir -p "$dir"; then
            log_error "Failed to create directory: $dir"
            exit 1
        fi
    done

    log_success "Directory structure created"
}

# --- Generate company.yaml ---
generate_company_config() {
    log_step "Generating company configuration"

    local divisions
    divisions=$(get_preset_divisions)
    local today
    today=$(date +%Y-%m-%d)

    cat > "$ORCH_DIR/company.yaml" << YAML
# ============================================================================
# ${COMPANY_NAME} — Organizational Structure
# ============================================================================
# Generated by Agent Orchestrator v${VERSION} on ${today}
# Preset: ${PRESET}
# ============================================================================

company:
  name: "${COMPANY_NAME}"
  goal: "${COMPANY_GOAL}"
  owner: "${OWNER_NAME}"
  preset: "${PRESET}"
  budget:
    monthly_limit_tokens: 50000000
    alert_threshold: 0.80
    auto_pause_threshold: 0.95
  created: "${today}"

# ============================================================================
# AGENTS — Organizational Hierarchy
# ============================================================================

agents:

  ceo:
    id: "ceo"
    name: "${COMPANY_NAME} CEO"
    title: "Chief Executive Officer"
    type: "orchestrator"
    adapter: "dario-v2-digital-ceo"
    reports_to: null
    capabilities:
      - strategic_planning
      - task_decomposition
      - agent_hiring
      - budget_allocation
      - cross_division_coordination
      - client_communication
      - quality_assurance
    heartbeat:
      enable_timer: true
      interval_minutes: 30
      enable_assignment_wakeup: true
      enable_on_demand: true
      cooldown_minutes: 5
    context_mode: "full"

YAML

    # Generate divisions based on selection
    IFS=',' read -ra div_array <<< "$divisions"
    for div in "${div_array[@]}"; do
        div=$(echo "$div" | xargs)  # trim whitespace
        generate_division "$div" >> "$ORCH_DIR/company.yaml"
    done

    # Add execution policies and heartbeat defaults
    cat >> "$ORCH_DIR/company.yaml" << 'YAML'

# ============================================================================
# EXECUTION POLICIES
# ============================================================================

execution_policies:
  default:
    comment_required: true
    review_required: false
    approval_required: false
  critical:
    comment_required: true
    review_required: true
    approval_required: true
    revision_max_loops: 3
  client_facing:
    comment_required: true
    review_required: true
    approval_required: false
    revision_max_loops: 2
  financial:
    comment_required: true
    review_required: true
    approval_required: true
    revision_max_loops: 2

# ============================================================================
# HEARTBEAT DEFAULTS
# ============================================================================

heartbeat_defaults:
  manager:
    interval_minutes: 30
    cooldown_minutes: 5
    coalesce_if_active: true
  worker:
    interval_minutes: 0
    cooldown_minutes: 2
    coalesce_if_active: true
  service:
    interval_minutes: 5
    cooldown_minutes: 1
    coalesce_if_active: true

# ============================================================================
# ROUTINES
# ============================================================================

routines:
  daily_standup:
    trigger: "schedule"
    schedule: "0 9 * * 1-5"
    timezone: "Europe/Lisbon"
    action: "Review all in_progress tasks, flag stale, report blockers"
    concurrency: "skip_if_active"
  weekly_review:
    trigger: "schedule"
    schedule: "0 18 * * 5"
    timezone: "Europe/Lisbon"
    action: "Summarize week: tasks completed, budget spent, next priorities"
    concurrency: "skip_if_active"
YAML

    log_success "Company config generated: $ORCH_DIR/company.yaml"

    # Validate generated YAML
    if [[ ! -s "$ORCH_DIR/company.yaml" ]]; then
        log_error "company.yaml is empty — generation failed"
        exit 1
    fi
    if ! grep -q '^company:' "$ORCH_DIR/company.yaml"; then
        log_error "company.yaml is missing the 'company:' key — generation failed"
        exit 1
    fi
    log_success "company.yaml validated (not empty, contains company: key)"
}

# --- Generate individual division config ---
generate_division() {
    local div="$1"

    case "$div" in
        marketing)
            cat << 'DIV'

  # --- Director: Marketing & Growth ---
  dir_marketing:
    id: "dir-marketing"
    name: "Marketing Director"
    title: "Director of Marketing & Growth"
    type: "manager"
    reports_to: "ceo"
    capabilities:
      - brand_strategy
      - offer_creation
      - copywriting
      - paid_traffic
      - funnel_design
      - sales_pipeline
      - email_marketing
    skills:
      - "brand"
      - "offer"
      - "sales-letter"
      - "ads-blueprint"
      - "funnel"
      - "pipeline"
      - "email-seq"
      - "naming"
      - "story-circle"
      - "pitch"
      - "proposal"
      - "negotiation"
DIV
            ;;
        technical)
            cat << 'DIV'

  # --- Director: Technical ---
  dir_technical:
    id: "dir-technical"
    name: "Technical Director"
    title: "Director of Technical Operations"
    type: "manager"
    reports_to: "ceo"
    capabilities:
      - wordpress_engineering
      - woocommerce_optimization
      - performance_optimization
      - security_auditing
      - automation_design
      - process_documentation
    skills:
      - "wp-audit"
      - "woo-audit"
      - "cwv-fix"
      - "pentest-checklist"
      - "make-blueprint"
      - "sop"
DIV
            ;;
        seo)
            cat << 'DIV'

  # --- Director: SEO ---
  dir_seo:
    id: "dir-seo"
    name: "SEO Director"
    title: "Director of Search & Visibility"
    type: "manager"
    reports_to: "ceo"
    capabilities:
      - technical_seo
      - content_seo
      - local_seo
      - geo_optimization
      - schema_markup
      - seo_strategy
      - keyword_research
    skills:
      - "seo-audit"
      - "seo-technical"
      - "seo-content"
      - "seo-schema"
      - "seo-local"
      - "seo-geo"
      - "seo-plan"
      - "seo-page"
      - "seo-sitemap"
      - "kw-cluster"
DIV
            ;;
        finance)
            cat << 'DIV'

  # --- Director: Finance ---
  dir_finance:
    id: "dir-finance"
    name: "Finance Director"
    title: "Director of Finance & Operations"
    type: "manager"
    reports_to: "ceo"
    capabilities:
      - financial_modeling
      - pricing_strategy
      - saas_analytics
      - budget_forecasting
    skills:
      - "financial-model"
      - "pricing-calculator"
      - "saas-metrics"
DIV
            ;;
        design)
            cat << 'DIV'

  # --- Director: Design ---
  dir_design:
    id: "dir-design"
    name: "Design Director"
    title: "Director of Design"
    type: "manager"
    reports_to: "ceo"
    capabilities:
      - interior_design
      - moodboard_creation
      - material_specification
      - spatial_planning
      - 3d_visualization
    skills:
      - "moodboard"
      - "materials"
      - "floor-plan"
      - "render"
      - "render-brief"
      - "vision"
      - "portfolio"
      - "smart-home"
DIV
            ;;
        construction)
            cat << 'DIV'

  # --- Director: Construction ---
  dir_construction:
    id: "dir-construction"
    name: "Construction Director"
    title: "Director of Construction Management"
    type: "manager"
    reports_to: "ceo"
    capabilities:
      - budget_estimation
      - timeline_planning
      - inspection_management
      - contract_generation
      - bim_coordination
    skills:
      - "budget"
      - "calc"
      - "timeline"
      - "inspection"
      - "contract"
      - "comparador"
      - "planradar"
      - "bim"
DIV
            ;;
        regulatory)
            cat << 'DIV'

  # --- Director: Regulatory ---
  dir_regulatory:
    id: "dir-regulatory"
    name: "Regulatory Director"
    title: "Director of Regulatory & Compliance"
    type: "manager"
    reports_to: "ceo"
    capabilities:
      - building_regulations
      - energy_certification
      - municipal_permits
    skills:
      - "licensing"
      - "energy"
DIV
            ;;
        saas-engineering)
            cat << 'DIV'

  # --- Director: SaaS Engineering ---
  dir_saas_engineering:
    id: "dir-saas-engineering"
    name: "SaaS Engineering Director"
    title: "Director of SaaS Engineering"
    type: "manager"
    reports_to: "ceo"
    capabilities:
      - fullstack_development
      - api_design
      - ai_agent_building
      - database_architecture
    skills: []
DIV
            ;;
        accounting)
            cat << 'DIV'

  # --- Director: Accounting ---
  dir_accounting:
    id: "dir-accounting"
    name: "Accounting Director"
    title: "Director of Accounting & Compliance"
    type: "manager"
    reports_to: "ceo"
    capabilities:
      - tax_law
      - financial_reporting
      - compliance
    skills: []
DIV
            ;;
        client-success)
            cat << 'DIV'

  # --- Director: Client Success ---
  dir_client_success:
    id: "dir-client-success"
    name: "Client Success Director"
    title: "Director of Client Success"
    type: "manager"
    reports_to: "ceo"
    capabilities:
      - client_onboarding
      - diagnostic_analysis
      - project_management
    skills:
      - "client-onboard"
      - "diagnose"
      - "projeto"
DIV
            ;;
    esac
}

# --- Install orchestrator skill ---
install_orchestrator_skill() {
    log_step "Installing orchestrator skill"

    cat > "$SKILLS_DIR/orchestrator/SKILL.md" << 'SKILL'
---
name: orchestrator
description: "Paperclip-inspired control plane — orchestrates agents, skills, and squads using heartbeats, atomic task checkout, execution policies, and budget controls. Triggers on: 'orchestrate', 'plan', 'decompose', 'coordinate', 'delegate', 'who does what', 'organize work'."
license: MIT
---

# Agent Orchestrator — Control Plane

The central nervous system of your agent ecosystem. Transforms ad-hoc skill invocation into structured, auditable, budget-aware orchestration.

## Architecture

```
User Request
    |
    v
[CEO — Orchestrator]
    |
    +-- 1. UNDERSTAND — Parse intent, gather context
    +-- 2. DECOMPOSE — Break into atomic tasks
    +-- 3. DISPATCH — Route each task to right agent/skill
    +-- 4. EXECUTE — Workers run in heartbeat windows
    +-- 5. REVIEW — Execution policies enforced
    +-- 6. SYNTHESIZE — Combine outputs into deliverable
    +-- 7. AUDIT — Log everything, update budget
```

## Workflow

### Phase 1: UNDERSTAND
1. Parse the user request — What is the end goal?
2. Check agent memory for existing context
3. Load company config from `~/.claude/orchestrator/company.yaml`
4. Identify constraints — Budget, timeline, dependencies

### Phase 2: DECOMPOSE
Break into atomic tasks, each mapping to ONE skill:

```yaml
task:
  id: "PROJ-001"
  title: "Action title"
  status: "todo"        # backlog | todo | in_progress | in_review | done | blocked
  priority: "high"      # critical | high | medium | low
  assignee: null
  skill: "skill-name"
  execution_policy: "default"  # default | critical | client_facing | financial
  depends_on: []
```

Save tasks to `~/.claude/orchestrator/tasks/active/`

### Phase 3: DISPATCH
Match tasks to agents using company.yaml capabilities:
- Direct skill match (fastest)
- Capability intersection
- Division routing
- Escalation chain: Worker -> Director -> CEO

Max 3 parallel workers per heartbeat.

### Phase 4: EXECUTE
Each execution is a discrete heartbeat:
1. Check identity
2. Review assigned tasks
3. Pick highest priority, no blockers
4. Atomic checkout (claim it)
5. Execute via skill
6. Post completion comment
7. Update task status

### Phase 5: REVIEW
Enforce execution policy:
- **Layer 1 (always):** Completion comment required
- **Layer 2 (optional):** Director review
- **Layer 3 (optional):** User/CEO approval

### Phase 6: SYNTHESIZE
Combine all task outputs into unified deliverable.

### Phase 7: AUDIT
Log every mutation to `~/.claude/orchestrator/audit/YYYY-MM-DD.yaml`

## Commands
| Command | Action |
|---|---|
| `status` | Show all active tasks |
| `next` | Execute next available task |
| `assign <task> <worker>` | Assign a task |
| `review <task>` | Trigger review |
| `approve <task>` | Approve task |
| `budget` | Show budget usage |
| `audit` | Show audit log |
| `template <name> <project>` | Create from template |

SKILL

    log_success "Orchestrator skill installed"
}

# --- Install taskboard skill ---
install_taskboard_skill() {
    log_step "Installing taskboard skill"

    cat > "$SKILLS_DIR/taskboard/SKILL.md" << 'SKILL'
---
name: taskboard
description: "Task lifecycle management — create, assign, checkout, review, approve with atomic ownership. Persistent YAML tasks at ~/.claude/orchestrator/tasks/. Triggers on: 'taskboard', 'tasks', 'create task', 'view tasks', 'task status', 'backlog', 'sprint', 'kanban'."
license: MIT
---

# Taskboard — Task Lifecycle Management

## Status Flow
```
backlog -> todo -> in_progress -> in_review -> done
                       |              |
                       +-> blocked     +-> in_progress (revision)
```

## Task Schema
```yaml
id: "PROJ-001"
title: "Action title"
description: "What and why"
project: "project-slug"
status: "todo"
priority: "high"          # critical | high | medium | low
assignee: null
skill: "skill-name"
execution_policy: "default"
depends_on: []
blocks: []
created_at: "ISO timestamp"
completed_at: null
completion_comment: null
revision_count: 0
notes: []
```

## Operations
- **create** — New task with auto-ID
- **assign** — Atomic checkout (one owner at a time)
- **start** — Begin work (verify dependencies)
- **complete** — Submit with mandatory comment
- **review** — approve | revise | escalate
- **approve** — Final gate, move to done/
- **block/unblock** — Manage blockers
- **list** — View by project/status/assignee
- **stale** — Find tasks with no updates >24h

## Atomic Guarantee
If task is already in_progress with a different assignee, REJECT.
Only current assignee or CEO can reassign.

## Dependency Resolution
When a task completes, cascade-unblock all dependents.

SKILL

    log_success "Taskboard skill installed"
}

# --- Install dispatch skill ---
install_dispatch_skill() {
    log_step "Installing dispatch skill"

    cat > "$SKILLS_DIR/dispatch/SKILL.md" << 'SKILL'
---
name: dispatch
description: "Intelligent routing — maps tasks to optimal agent/skill/squad based on capabilities and company hierarchy. Triggers on: 'dispatch', 'routing', 'who does this', 'assign'."
license: MIT
---

# Dispatch — Intelligent Task Routing

## Algorithm
1. **Parse requirements** — Domain, skill, division, complexity
2. **Capability match** — Compare task needs to agent capabilities in company.yaml
3. **Division routing** — Route to correct organizational division
4. **Escalation chain** — Worker -> Director -> CEO
5. **Parallel planning** — Max 3 workers per wave

## Routing Process
```python
1. Direct skill match (if task.skill specified)
2. Capability intersection (best overlap wins)
3. Division preference (same division preferred)
4. Escalate if no match
```

## Parallel Execution
- Group independent tasks (no mutual dependencies)
- Max 3 per wave
- Execute via Agent tool simultaneously

## Cross-Division Coordination
When task spans divisions:
1. CEO decomposes into division subtasks
2. Each dispatched to its director
3. Shared artifacts for coordination
4. CEO synthesizes final output

SKILL

    log_success "Dispatch skill installed"
}

# --- Create task templates ---
create_templates() {
    log_step "Creating task templates"

    # Client audit template
    cat > "$ORCH_DIR/tasks/templates/client-audit.yaml" << 'TEMPLATE'
# Template: Full Client Audit
name: "client-audit"
description: "Complete client diagnostic and audit pipeline"
tasks:
  - title: "Diagnostic analysis"
    skill: "diagnose"
    policy: "default"
    priority: "critical"
    order: 1
  - title: "Technical audit"
    skill: "wp-audit"
    policy: "client_facing"
    depends_on: ["diagnostic"]
    order: 2
  - title: "SEO audit"
    skill: "seo-audit"
    policy: "client_facing"
    depends_on: ["diagnostic"]
    order: 2
  - title: "Synthesize findings"
    skill: "orchestrator"
    policy: "critical"
    depends_on: ["technical-audit", "seo-audit"]
    order: 3
TEMPLATE

    # Brand pipeline template
    cat > "$ORCH_DIR/tasks/templates/brand-pipeline.yaml" << 'TEMPLATE'
# Template: Brand + Offer + Copy Pipeline
name: "brand-pipeline"
description: "Full brand positioning through to sales copy and traffic"
tasks:
  - title: "Brand positioning"
    skill: "brand"
    policy: "client_facing"
    priority: "high"
    order: 1
  - title: "Grand Slam Offer"
    skill: "offer"
    policy: "client_facing"
    depends_on: ["brand-positioning"]
    order: 2
  - title: "Sales letter"
    skill: "sales-letter"
    policy: "client_facing"
    depends_on: ["grand-slam-offer"]
    order: 3
  - title: "Ads blueprint"
    skill: "ads-blueprint"
    policy: "default"
    depends_on: ["sales-letter"]
    order: 4
TEMPLATE

    log_success "Task templates created"
}

# --- Create initial audit log ---
create_audit_log() {
    local today
    today=$(date +%Y-%m-%d)

    cat > "$ORCH_DIR/audit/${today}.yaml" << AUDIT
# Audit Log — ${today}
# Agent Orchestrator v${VERSION}

- timestamp: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  actor: "installer"
  action: "system_installed"
  entity_type: "system"
  entity_id: "orchestrator"
  details: "Agent Orchestrator v${VERSION} installed for ${COMPANY_NAME} (preset: ${PRESET})"
AUDIT

    log_success "Audit log initialized"
}

# --- Create budget file ---
create_budget() {
    local month
    month=$(date +%Y-%m)

    cat > "$ORCH_DIR/budgets/${month}.yaml" << BUDGET
# Budget Tracking — ${month}
month: "${month}"
company: "${COMPANY_NAME}"
total_tokens_used: 0
by_project: {}
by_agent: {}
alert_sent: false
BUDGET

    log_success "Budget tracking initialized"
}

# --- Summary ---
print_summary() {
    echo ""
    echo -e "  ${GREEN}${BOLD}Installation Complete!${NC}"
    echo ""
    echo -e "  ${BOLD}Company:${NC}  ${COMPANY_NAME}"
    echo -e "  ${BOLD}Preset:${NC}   ${PRESET}"
    echo -e "  ${BOLD}Owner:${NC}    ${OWNER_NAME}"
    echo ""
    echo -e "  ${BOLD}Files created:${NC}"
    echo -e "    ${CYAN}$ORCH_DIR/company.yaml${NC}           — Org hierarchy"
    echo -e "    ${CYAN}$ORCH_DIR/tasks/${NC}                 — Task storage"
    echo -e "    ${CYAN}$ORCH_DIR/audit/${NC}                 — Audit trail"
    echo -e "    ${CYAN}$ORCH_DIR/budgets/${NC}               — Budget tracking"
    echo -e "    ${CYAN}$SKILLS_DIR/orchestrator/SKILL.md${NC} — Control plane skill"
    echo -e "    ${CYAN}$SKILLS_DIR/taskboard/SKILL.md${NC}   — Task lifecycle skill"
    echo -e "    ${CYAN}$SKILLS_DIR/dispatch/SKILL.md${NC}    — Routing skill"
    echo ""
    echo -e "  ${BOLD}Quick start:${NC}"
    echo -e "    In Claude Code, try:"
    echo -e "      ${YELLOW}/orchestrator${NC}        — Open the control plane"
    echo -e "      ${YELLOW}/taskboard list${NC}      — View all tasks"
    echo -e "      ${YELLOW}/dispatch${NC}            — Route a task"
    echo ""
    echo -e "  ${BOLD}Customize:${NC}"
    echo -e "    Edit ${CYAN}$ORCH_DIR/company.yaml${NC} to add/remove divisions, workers, and skills."
    echo -e "    Add your own skills to ${CYAN}$SKILLS_DIR/${NC} and reference them in company.yaml."
    echo ""
    echo -e "  ${BOLD}Documentation:${NC}"
    echo -e "    Each skill has full docs in its SKILL.md file."
    echo -e "    Read the company.yaml comments for hierarchy explanation."
    echo ""
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    detect_platform
    parse_args "$@"
    print_banner

    if [[ "$UNINSTALL" == true ]]; then
        do_uninstall
    fi

    if [[ "$VALIDATE" == true ]]; then
        do_validate
    fi

    check_prereqs
    interactive_setup
    create_directories
    generate_company_config
    install_orchestrator_skill
    install_taskboard_skill
    install_dispatch_skill
    create_templates
    create_audit_log
    create_budget
    print_summary
}

main "$@"
