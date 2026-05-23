---
name: lucas-analytics
description: "LUCAS Analytics & Intelligence — cross-project pattern detection, skill performance dashboard, revenue attribution, knowledge graph queries, and competitive intelligence. The brain that makes the system smarter over time. Triggers on: 'analytics', 'dashboard', 'patterns', 'performance', 'ROI', 'intelligence', 'what worked', 'which skill', 'revenue', 'cross-project'."
license: MIT
---

# LUCAS Analytics & Intelligence

The intelligence layer that turns data into decisions. Without analytics, the system executes but never learns. With analytics, every project makes the next one better.

## When to activate

- Weekly automated report (via scheduled trigger)
- User asks "what patterns do we see?", "which skill works best?", "ROI?"
- After milestone completion on any project
- When planning new project (recommend approach based on history)
- Via `/lucas-analytics`

## 5 Analytics Modules

### Module 1: Cross-Project Pattern Detection

Scans all completed projects and extracts reusable patterns.

**Data sources:**
- `~/.claude/orchestrator/tasks/done/` — completed tasks with quality scores
- `~/.claude/orchestrator/quality/success-patterns.yaml` — what worked
- `~/.claude/orchestrator/quality/failure-patterns.yaml` — what failed
- Agent memory project files — client domain, stack, outcomes

**Pattern extraction:**
```
For each client domain (restaurant, architecture, saas, ecommerce...):
  1. Which skills were used?
  2. What quality scores did they achieve?
  3. What was the optimal execution order?
  4. What RAG context improved quality?
  5. What common mistakes occurred?
  → Generate: "Playbook for [domain] projects"
```

**Output: Domain Playbook**
```yaml
domain: "restaurant"
projects_analyzed: 3
avg_quality: 87.5
optimal_skill_chain:
  - dario-brand (always first, 92 avg)
  - dario-naming (parallel with seo-local)
  - seo-local (critical for restaurants, 91 avg)
  - seo-plan (after brand, 84 avg)
  - dario-story-circle (after brand+naming, 85 avg)
avoid:
  - "dario-offer before brand positioning — produces generic output"
rag_context_needed:
  - "Local competitor data for the specific city"
  - "Industry pricing benchmarks"
estimated_tokens: 35000
estimated_time: "15-20 minutes"
```

### Module 2: Skill Performance Dashboard

Real-time view of every skill's effectiveness.

**Metrics per skill:**
- Success rate (% tasks >= 75 quality score)
- Revision rate (% tasks needing revision)
- Average quality score
- Average tokens used (cost efficiency)
- Trend (improving / stable / declining)
- Best use case (domain where it scores highest)
- Worst use case (domain where it scores lowest)

**Dashboard output:**
```markdown
## Skill Performance — April 2026

### Tier A (Avg >= 85, Revision < 10%)
| Skill | Score | Rev% | Best Domain | Tokens |
|---|---|---|---|---|
| seo-local | 91.5 | 0% | restaurant | 3100 |
| dario-brand | 87.3 | 8% | any | 2200 |
| seo-technical | 86.8 | 5% | any | 2800 |

### Tier B (Avg 70-84, Revision 10-25%)
| Skill | Score | Rev% | Issue | Fix |
|---|---|---|---|---|
| seo-plan | 84.5 | 12% | Sometimes thin on keywords | Enrich RAG with DataForSEO data |
| dario-story-circle | 82.0 | 15% | Occasionally generic | Needs more client context |

### Tier C (Avg < 70, Revision > 25%) — NEEDS ATTENTION
| Skill | Score | Rev% | Root Cause | Action |
|---|---|---|---|---|
| dario-offer | 72.0 | 40% | Generic value equations | RAG needs pricing data |
| dario-financial-model | 74.5 | 30% | Missing PT benchmarks | Ingest PT market data |
```

### Module 3: Revenue Attribution

Track which skills and projects generate measurable value.

**Data model:**
```yaml
# ~/.claude/orchestrator/analytics/revenue.yaml
clients:
  mar-brasa:
    monthly_retainer: 1500
    start_date: "2026-04"
    skills_used: [dario-brand, dario-naming, seo-local, seo-plan, dario-story-circle]
    total_tokens_invested: 34000
    token_cost_estimate: 3.40  # EUR
    revenue_to_date: 1500
    roi_multiplier: 441x
    satisfaction: "high"

  atrium:
    monthly_retainer: 2500
    start_date: "2025-11"
    skills_used: [seo-audit, seo-technical, seo-schema, seo-content, seo-local]
    total_tokens_invested: 250000
    token_cost_estimate: 25.00
    revenue_to_date: 15000
    roi_multiplier: 600x
    satisfaction: "high"
```

**Revenue per skill:**
```markdown
### Revenue Attribution by Skill
| Skill | Projects Using | Avg Revenue/Project | Token Cost | ROI |
|---|---|---|---|---|
| seo-audit | 5 | 2000 EUR | 3.50 EUR | 571x |
| dario-brand | 4 | 1500 EUR | 2.20 EUR | 681x |
| dario-wp-audit | 3 | 1800 EUR | 4.00 EUR | 450x |
```

### Module 4: Knowledge Graph Queries

Query relationships between entities across the entire system.

**Entity types:**
- Client (name, domain, location, stack, status)
- Project (client, skills used, quality scores, timeline)
- Skill (name, avg quality, revision rate, cost)
- Worker (skill, director, capabilities)
- Competitor (client's competitor, tracked metrics)
- Pattern (domain, optimal approach, common mistakes)

**Example queries:**
```
Q: "All restaurant clients"
A: Mar & Brasa (Cascais), [future clients...]

Q: "Best approach for architecture studio website"
A: Playbook: dario-brand → diva-portfolio → seo-local → seo-plan (based on 2 prior projects, avg quality 88)

Q: "Which skills have declining quality?"
A: dario-offer (was 78 avg, now 72 — declining), dario-financial-model (was 80, now 74)

Q: "Clients with stale projects (no task activity >30 days)"
A: Lisbon Dog Care (last activity: 2026-03-15)
```

### Module 5: Competitive Intelligence

Track and alert on competitor movements.

**Monitoring:**
- Weekly SERP check for client target keywords
- GBP ranking changes for local clients
- Competitor new content detection
- Market trend shifts in client domains

**Alert triggers:**
- Competitor moved to position #1 for client's primary keyword
- New competitor entered client's market
- Client's ranking dropped >5 positions
- Industry trend shift (e.g., AI Overviews now showing for client's queries)

## Weekly Intelligence Report

Generated automatically every Friday:

```markdown
## LUCAS Intelligence Report — Week of YYYY-MM-DD

### Portfolio Health
- Active projects: 5
- Tasks completed this week: 12
- Avg quality score: 85.2
- Budget used: 18% (month to date)

### Top Insight
"Restaurant projects consistently score 8 points higher on brand 
positioning when RAG has local competitor data pre-loaded. 
Recommend: always run competitor research before dario-brand 
for hospitality clients."

### Skill Health
- Improving: seo-local (+3.2 pts), dario-story-circle (+5.0 pts)
- Declining: dario-offer (-3.0 pts) — needs RAG enrichment
- New skill needed: No skill covers "social media content calendar" — 
  gap detected in 3 client projects

### Cross-Project Patterns
- Pattern confirmed: brand → naming → seo-local pipeline works for 
  any local business (3 projects, avg quality 89)
- Pattern emerging: DIVA + DARIO cross-division for design studios 
  produces higher satisfaction than DARIO alone

### Revenue
- Monthly revenue from orchestrated projects: 8,500 EUR
- Token cost: 25.00 EUR
- ROI: 340x

### Action Items
1. Enrich RAG with pricing benchmarks for dario-offer
2. Create social media calendar skill (gap detected)
3. Schedule competitor check for Atrium (30 days since last)
```

## Red Flags

- Never report revenue estimates as exact (always "estimate")
- Quality trends need minimum 5 data points before declaring "declining"
- Cross-project patterns need minimum 3 projects to be "confirmed"
- Competitive intelligence must use only public data
- Analytics are decision support, not decisions — user always decides

---

## Data Sources & Queries

Exactly WHERE data lives and HOW to query it. Every analytics module starts here.

### Source 1: Completed Tasks — `~/.claude/orchestrator/tasks/done/*.yaml`

```
Location: ~/.claude/orchestrator/tasks/done/
File format: One YAML per completed task (e.g., MNB-001.yaml)
Fields used: id, title, skill, project, quality_score, tokens_used, completed_at, completion_comment

Query — Count tasks by project:
  1. Read all *.yaml files in done/
  2. Group by project field
  3. Count per group
  → Output: { "mar-brasa": 6, "atrium": 12, "lisbon-dog-care": 3 }

Query — Sum tokens by skill:
  1. Read all *.yaml files in done/
  2. Group by skill field
  3. Sum tokens_used per group
  → Output: { "dario-brand": 4400, "seo-local": 6200, "seo-audit": 14000 }

Query — Average quality by project:
  1. Read all *.yaml files in done/
  2. Group by project field
  3. Average quality_score per group
  → Output: { "mar-brasa": 87.5, "atrium": 85.2 }

Query — Tasks completed this week:
  1. Read all *.yaml files in done/
  2. Filter: completed_at >= (today - 7 days)
  3. Sort by completed_at descending
  → Output: list of task summaries
```

### Source 2: Skill Metrics — `~/.claude/orchestrator/quality/skill-metrics.yaml`

```
Location: ~/.claude/orchestrator/quality/skill-metrics.yaml
Updated by: lucas-quality after every task scoring
Fields used: skills.{name}.total_executions, avg_quality_score, scores[], revision_rate, avg_tokens, improvement_trend

Query — Top performers:
  1. Load skill-metrics.yaml
  2. Sort skills by avg_quality_score descending
  3. Filter: total_executions >= 3 (minimum sample)
  → Output: ranked list of skills with scores

Query — Skills needing attention:
  1. Load skill-metrics.yaml
  2. Filter: revision_rate > 0.25 OR avg_quality_score < 75
  3. Sort by revision_rate descending
  → Output: skills with problems + root cause from common_weakness field

Query — Trend detection:
  1. Load skill-metrics.yaml
  2. For each skill with scores[] length >= 5:
     - Compare avg of last 3 scores vs avg of first 3 scores
     - Difference > +5: "improving"
     - Difference < -5: "declining"
     - Otherwise: "stable"
  → Output: trend per skill
```

### Source 3: Monthly Budgets — `~/.claude/orchestrator/budgets/YYYY-MM.yaml`

```
Location: ~/.claude/orchestrator/budgets/YYYY-MM.yaml (e.g., 2026-04.yaml)
Updated by: lucas-heartbeat after every execution
Fields used: total_budget, spent, percentage, daily_breakdown[]

Query — Current month status:
  1. Load budgets/2026-04.yaml
  2. Read: spent, total_budget, percentage
  → Output: "April 2026: 45.00 EUR / 100.00 EUR (45%)"

Query — Month-over-month comparison:
  1. Load current month + previous 2 months
  2. Compare: spent at same day-of-month
  3. Calculate: burn rate trend (accelerating / steady / decelerating)
  → Output: "April burn rate 1.5 EUR/day vs March 1.2 EUR/day — accelerating"

Query — Budget forecast:
  1. Load current month
  2. Calculate: daily_burn = spent / days_elapsed
  3. Forecast: daily_burn × days_remaining_in_month
  4. Compare to total_budget
  → Output: "Projected spend: 67.50 EUR (67% of budget). Safe."
```

### Source 4: Audit Logs — `~/.claude/orchestrator/audit/YYYY-MM-DD.yaml`

```
Location: ~/.claude/orchestrator/audit/YYYY-MM-DD.yaml
Updated by: orchestrator on every action
Fields used: entries[].timestamp, action, task_id, actor, details

Query — Actions by type in date range:
  1. Read all audit files in date range
  2. Flatten entries[]
  3. Group by action field
  4. Count per group
  → Output: { "task_created": 8, "task_dispatched": 8, "task_completed": 6, "task_scored": 6, "budget_check": 12 }

Query — Actor activity:
  1. Read all audit files in date range
  2. Group by actor field
  3. Count per actor
  → Output: { "autopilot": 15, "user": 5, "heartbeat": 22 }

Query — Timeline for specific task:
  1. Read all audit files
  2. Filter entries where task_id matches
  3. Sort by timestamp
  → Output: full lifecycle of one task from creation to scoring
```

---

## Pattern Detection — Worked Example

### Input: 6 Completed Mar & Brasa Tasks

```yaml
# From tasks/done/
MNB-001: { skill: dario-brand, quality_score: 92, tokens: 2200 }
MNB-002: { skill: dario-naming, quality_score: 88, tokens: 1800 }
MNB-003: { skill: seo-local, quality_score: 91, tokens: 3100 }
MNB-004: { skill: seo-plan, quality_score: 84, tokens: 2500 }
MNB-005: { skill: dario-story-circle, quality_score: 85, tokens: 2100 }
MNB-006: { skill: dario-offer, quality_score: 72, tokens: 2800 }
```

### Process

**Step 1: Group by skill and calculate stats**

```
dario-brand:        1 execution, avg 92, tokens 2200
dario-naming:       1 execution, avg 88, tokens 1800
seo-local:          1 execution, avg 91, tokens 3100
seo-plan:           1 execution, avg 84, tokens 2500
dario-story-circle: 1 execution, avg 85, tokens 2100
dario-offer:        1 execution, avg 72, tokens 2800 ← WORST
```

**Step 2: Identify highest scorer and extract what_worked**

```
Winner: dario-brand (92)
Load success-patterns.yaml → find entry for MNB-001
what_worked:
  - "Kapferer Prism with restaurant-specific facets"
  - "Real local competitors with actual price ranges"
  - "Dual archetype with justification"
```

**Step 3: Identify lowest scorer and extract what_failed**

```
Loser: dario-offer (72)
Load failure-patterns.yaml → find entry for MNB-006
what_failed:
  - "Value equation generic — not restaurant-specific"
  - "Missing local pricing benchmarks"
root_cause: "RAG lacked restaurant industry pricing for Cascais market"
```

**Step 4: Determine optimal execution order**

```
Analyze dependencies:
- dario-brand MUST be first (other skills reference brand output)
- dario-naming can run PARALLEL with seo-local (no dependency)
- seo-plan AFTER brand (needs positioning to inform keyword strategy)
- dario-story-circle AFTER brand + naming (needs both as input)
- dario-offer LAST (needs all context, still underperformed → needs RAG fix first)

Optimal chain:
  Wave 1: dario-brand
  Wave 2: dario-naming + seo-local (parallel)
  Wave 3: seo-plan + dario-story-circle (parallel, after wave 1)
  Wave 4: dario-offer (only after RAG enrichment)
```

**Step 5: Generate domain playbook**

```yaml
# Output: Restaurant Domain Playbook
domain: "restaurant"
source_projects: ["mar-brasa"]
projects_analyzed: 1
avg_quality: 85.3
total_tokens: 14500
estimated_time: "12-18 minutes for full chain"

optimal_skill_chain:
  wave_1:
    - skill: dario-brand
      avg_score: 92
      role: "Foundation — must be first"
  wave_2:
    - skill: dario-naming
      avg_score: 88
      role: "Parallel with seo-local"
    - skill: seo-local
      avg_score: 91
      role: "Critical for restaurant visibility"
  wave_3:
    - skill: seo-plan
      avg_score: 84
      role: "Keyword strategy informed by brand"
    - skill: dario-story-circle
      avg_score: 85
      role: "Brand narrative for about page"
  wave_4_conditional:
    - skill: dario-offer
      avg_score: 72
      role: "Only after RAG has pricing data"
      prerequisite: "Ingest restaurant pricing benchmarks into RAG"

pre_flight_checklist:
  - "Load local competitor data into RAG before starting"
  - "Confirm client has provided: menu prices, cover count, location, target demographic"
  - "Check if brand task already exists (skip wave 1 if so)"

avoid:
  - "Running dario-offer before RAG has industry pricing data"
  - "Running seo-plan before brand positioning is complete"

success_patterns:
  - "Kapferer Prism + restaurant-specific facets → 92 avg"
  - "Real competitor matrix with actual prices → high specificity scores"

status: "emerging"  # needs 3+ projects to be "confirmed"
```

---

## Skill Performance Dashboard — Worked Example

### How to generate the dashboard

```
1. Load ~/.claude/orchestrator/quality/skill-metrics.yaml
2. For each skill in skills:
   a. Read: total_executions, avg_quality_score, revision_rate, avg_tokens, improvement_trend
   b. Classify into tier:
      - Tier A: avg_quality_score >= 85 AND revision_rate < 0.10
      - Tier B: avg_quality_score >= 75 AND revision_rate < 0.25
      - Tier C: everything else (needs attention)
   c. Identify best domain from success-patterns.yaml (filter by skill)
3. Sort each tier by avg_quality_score descending
4. Generate recommendations for Tier C skills
5. Output formatted dashboard
```

### Full Dashboard with Real Data

```markdown
## Skill Dashboard — April 2026

Generated: 2026-04-27 | Data: skill-metrics.yaml | Tasks scored: 25

### Tier A — Ship with confidence (avg >= 85, revision < 10%)

| Skill | Executions | Avg Score | Rev% | Trend | Best Domain | Avg Tokens |
|---|---|---|---|---|---|---|
| seo-local | 8 | 91.5 | 0% | improving (+3.2) | restaurant | 3100 |
| dario-brand | 12 | 87.3 | 8% | stable | any | 2200 |
| seo-technical | 6 | 86.8 | 5% | improving (+1.5) | any | 2800 |
| dario-story-circle | 4 | 85.0 | 0% | new | restaurant | 2100 |

**Tier A health:** 4 skills, 30 total executions, 0 failures. Strong foundation.

### Tier B — Good, minor improvements possible (avg 75-84, revision 10-25%)

| Skill | Executions | Avg Score | Rev% | Trend | Weakness | Fix |
|---|---|---|---|---|---|---|
| seo-plan | 7 | 84.5 | 12% | stable | Sometimes thin on long-tail keywords | Pair with seo-dataforseo for live volume data |
| dario-story-circle | 4 | 82.0 | 15% | new | Occasionally generic when client context thin | Load more project context before running |
| seo-content | 5 | 80.2 | 15% | stable | E-E-A-T signals sometimes weak | Add author bio template to prompt |

**Tier B health:** 3 skills, 16 executions. All fixable with RAG/context improvements.

### Tier C — Needs attention (avg < 75 or revision > 25%)

| Skill | Executions | Avg Score | Rev% | Trend | Root Cause | Action Required |
|---|---|---|---|---|---|---|
| dario-offer | 5 | 72.0 | 40% | stagnant | Value equation lacks market specificity | Ingest industry pricing data into RAG per client domain |
| dario-financial-model | 3 | 74.5 | 30% | declining (-2.0) | Missing PT market benchmarks | Ingest INE/Pordata statistics, PT tax rates, industry margins |
| seo-programmatic | 2 | 76.0 | 25% | new | Thin content on generated pages | Add minimum word count gate + quality check per page |

**Tier C health:** 3 skills, 10 executions, 32% avg revision rate. Priority fixes needed.

### Cost Efficiency

| Skill | Avg Tokens | Avg Score | Score/1K Tokens | Verdict |
|---|---|---|---|---|
| dario-brand | 2200 | 87.3 | 39.7 | Excellent value |
| dario-naming | 1800 | 88.0 | 48.9 | Best ROI |
| seo-local | 3100 | 91.5 | 29.5 | Good — high score justifies tokens |
| dario-offer | 2800 | 72.0 | 25.7 | Poor — high cost, low quality |
| seo-audit | 5500 | 85.0 | 15.5 | Acceptable — complex task justifies tokens |

### Recommendations

1. **URGENT:** dario-offer (72 avg, 40% revision) — Ingest pricing benchmarks before next use. Consider: run competitor pricing research as prerequisite task.
2. **IMPORTANT:** dario-financial-model (74.5 avg, declining) — Ingest PT market data from INE. Add PT tax rate reference table to RAG.
3. **MONITOR:** seo-programmatic (76 avg, small sample) — Needs more executions before firm verdict. Add thin content safeguard to prompt.
4. **OPTIMIZE:** seo-plan could move to Tier A with DataForSEO integration for live keyword data.
```

---

## Revenue Attribution — How to Track

Step-by-step process to connect revenue back to skills and measure real business impact.

### Step 1: Record Revenue Event

When an invoice is created or payment received, create/update the revenue entry:

```yaml
# ~/.claude/orchestrator/analytics/revenue.yaml
# Add or update when user says "client X paid" or "invoice created for X"

clients:
  mar-brasa:
    invoices:
      - id: "INV-2026-001"
        date: "2026-04-15"
        amount: 1500.00
        currency: "EUR"
        description: "Website + Brand + SEO setup"
        status: "paid"
    total_revenue: 1500.00
    start_date: "2026-04-01"
```

### Step 2: Look Up Project Tasks

```
1. List all files in tasks/done/ where project == "mar-brasa"
2. Collect: skill, tokens_used, quality_score for each task
3. Sum total tokens across all tasks for this project
```

### Step 3: Calculate Token Cost

```
Token pricing (Claude Sonnet 4 as of 2026-04):
  Input:  $3.00 / 1M tokens → 0.003 EUR / 1K tokens
  Output: $15.00 / 1M tokens → 0.015 EUR / 1K tokens
  Blended estimate: 0.01 EUR / 1K tokens (conservative)

Example:
  mar-brasa total tokens: 14,500
  Estimated cost: 14.5 × 0.01 = 0.145 EUR
```

### Step 4: Calculate Value Metrics

```
Revenue per token = total_revenue / total_tokens
  mar-brasa: 1500 / 14500 = 0.103 EUR per token

ROI multiplier = total_revenue / token_cost
  mar-brasa: 1500 / 0.145 = 10,345x

Value per skill = revenue_attributed / tokens_per_skill
  Attribute revenue proportionally to token usage or equally per task.
  
  Equal attribution (6 tasks):
    Each task attributed: 1500 / 6 = 250 EUR
    dario-brand: 250 EUR / 2200 tokens = 0.114 EUR/token
    seo-local: 250 EUR / 3100 tokens = 0.081 EUR/token
```

### Step 5: Store Results

```yaml
# Append to ~/.claude/orchestrator/analytics/revenue.yaml

attribution:
  mar-brasa:
    total_revenue: 1500.00
    total_tokens: 14500
    token_cost_estimate: 0.145
    roi_multiplier: 10345
    per_skill:
      dario-brand: { revenue: 250, tokens: 2200, value_per_token: 0.114 }
      dario-naming: { revenue: 250, tokens: 1800, value_per_token: 0.139 }
      seo-local: { revenue: 250, tokens: 3100, value_per_token: 0.081 }
      seo-plan: { revenue: 250, tokens: 2500, value_per_token: 0.100 }
      dario-story-circle: { revenue: 250, tokens: 2100, value_per_token: 0.119 }
      dario-offer: { revenue: 250, tokens: 2800, value_per_token: 0.089 }
```

### When to Run Revenue Attribution

- After every invoice is marked "paid"
- Monthly rollup: aggregate all clients for monthly revenue report
- On demand: when user asks "ROI?", "value per skill?", "which skills make money?"

---

## Cross-Project Intelligence Report

Full template for comparing performance across all active projects. Generate on demand or monthly.

### How to Generate

```
1. Load all project memory files from ~/.claude/projects/*/memory/
   → Extract: project name, domain, status, start_date
2. Load all done tasks grouped by project
   → Count tasks, sum tokens, average quality per project
3. Load revenue.yaml
   → Get revenue per project
4. Load skill-metrics.yaml
   → Cross-reference which skills each project used
5. Load success-patterns.yaml + failure-patterns.yaml
   → Extract patterns per project domain
6. Compile into report
```

### Report Template

```markdown
## Cross-Project Intelligence Report — April 2026

Generated: 2026-04-27 | Active projects: 5 | Completed tasks: 45

### Project Performance Comparison

| Project | Domain | Tasks Done | Avg Quality | Tokens Used | Revenue | ROI | Status |
|---|---|---|---|---|---|---|---|
| Atrium Golden Visa | real-estate/immigration | 18 | 85.2 | 125,000 | 15,000 EUR | 600x | active |
| Mar & Brasa | restaurant | 6 | 85.3 | 14,500 | 1,500 EUR | 10,345x | active |
| LUCAS/LUSOconta | saas | 12 | 88.0 | 45,000 | 2,400 EUR | 533x | live |
| Lisbon Dog Care | pet-services | 4 | 82.5 | 12,000 | 800 EUR | 667x | maintenance |
| Vivenda Creative | interior-design | 5 | 84.0 | 18,000 | 1,200 EUR | 667x | active |

### Cross-Project Skill Effectiveness

| Skill | Projects Using | Avg Score Across Projects | Best Project | Worst Project |
|---|---|---|---|---|
| dario-brand | 4 | 87.3 | mar-brasa (92) | lisbon-dog-care (82) |
| seo-local | 3 | 89.0 | mar-brasa (91) | vivenda (85) |
| seo-audit | 3 | 85.0 | atrium (88) | lisbon-dog-care (80) |
| dario-offer | 2 | 72.0 | — | mar-brasa (72) |

### Domain Insights

**Restaurant (1 project: Mar & Brasa)**
- Optimal chain: brand → naming + seo-local → seo-plan → story-circle
- Key success factor: local competitor data in RAG
- Watch: dario-offer needs pricing benchmarks

**Real Estate / Immigration (1 project: Atrium)**
- Optimal chain: seo-audit → seo-technical → seo-schema → seo-content → seo-local
- Key success factor: schema markup for property/service pages
- Watch: content needs multilingual support (EN/PT)

**SaaS (1 project: LUSOconta)**
- Optimal chain: dario-brand → dario-product → seo-plan → dario-funnel
- Key success factor: product-led content strategy
- Watch: saas-metrics tracking needed

**Pet Services (1 project: Lisbon Dog Care)**
- Limited data (4 tasks). Pattern not yet established.
- Preliminary: local SEO + GBP optimization = highest impact

**Interior Design (1 project: Vivenda)**
- Cross-division opportunity: DIVA skills + DARIO skills together
- Preliminary: diva-moodboard + dario-brand combined → strong visual identity

### Cross-Domain Patterns

1. **Confirmed (3+ projects):** Brand positioning first → everything else improves by 5-8 points average
2. **Confirmed:** Local businesses (restaurant, pet, design studio) → seo-local is highest ROI skill
3. **Emerging:** DIVA + DARIO cross-division → higher client satisfaction for design/architecture clients
4. **Emerging:** RAG pre-loading with domain data → 10-15 point quality improvement on first task

### Actionable Recommendations

1. **Standardize:** Always run dario-brand as wave 1 for new clients. No exceptions.
2. **Fix:** dario-offer is the weakest skill across all projects. Invest in RAG pricing data per domain.
3. **Expand:** Create domain-specific RAG collections (restaurant pricing, PT real estate market, SaaS benchmarks)
4. **Track:** Start revenue attribution for all clients (currently only 3/5 have revenue data)
5. **Explore:** DIVA + DARIO cross-division pipeline for Vivenda — document if it works, make it a template
```

---

## Weekly Digest Generator

Automated weekly summary for the agency owner. Generate every Friday (or on demand via `/lucas-analytics weekly`).

### How to Generate

```
1. Determine date range: Monday 00:00 to Friday 23:59 of current week
2. Load tasks/done/*.yaml → filter by completed_at in date range → "tasks_this_week"
3. Load tasks/backlog/*.yaml + tasks/in_progress/*.yaml → count "pending" and "blocked"
4. Load budgets/YYYY-MM.yaml → read current spend + percentage
5. Load skill-metrics.yaml → calculate avg quality for tasks_this_week
6. Load audit/ files for date range → find stale tasks (no activity > 7 days)
7. Compile into digest
```

### Digest Template

```markdown
## LUCAS Weekly Digest — Week of YYYY-MM-DD

### Summary
- Tasks completed: 8
- Tasks in progress: 3
- Tasks blocked/stale: 1
- Budget used this month: 34.50 EUR / 100.00 EUR (34.5%)
- Average quality this week: 86.2/100
- Revenue invoiced this week: 2,500 EUR

### Completed This Week

| Task | Project | Skill | Score | Tokens |
|---|---|---|---|---|
| MNB-001 Brand Positioning | Mar & Brasa | dario-brand | 92 | 2200 |
| MNB-002 Brand Naming | Mar & Brasa | dario-naming | 88 | 1800 |
| MNB-003 GBP Setup | Mar & Brasa | seo-local | 91 | 3100 |
| ATR-015 Schema Markup | Atrium | seo-schema | 85 | 2400 |
| ATR-016 Content Refresh | Atrium | seo-content | 83 | 2800 |
| LDC-005 Review Strategy | Lisbon Dog Care | seo-local | 84 | 2200 |
| VCH-003 Moodboard | Vivenda | diva-moodboard | 86 | 1900 |
| LUS-008 Feature Page | LUSOconta | seo-content | 82 | 2600 |

### Quality Highlights
- Best output: MNB-001 Brand Positioning (92) — success pattern extracted
- Worst output: LUS-008 Feature Page (82) — E-E-A-T signals could be stronger
- Week-over-week trend: +1.4 points (improving)

### Budget Status
- April budget: 100.00 EUR
- Spent to date: 34.50 EUR (34.5%)
- Projected end-of-month: 52.00 EUR (52%) — ON TRACK
- Daily burn rate: 1.28 EUR/day

### Blocked / Stale Items
| Task | Project | Status | Days Stale | Issue |
|---|---|---|---|---|
| LDC-006 | Lisbon Dog Care | in_progress | 12 days | Waiting for client to provide GBP credentials |

**Action required:** Contact Lisbon Dog Care client for GBP access. If no response by Wednesday, escalate.

### Top Recommendation for Next Week
**Priority 1:** Complete Mar & Brasa remaining tasks (seo-plan, story-circle, offer). Brand foundation is solid (92) — capitalize on momentum.
**Priority 2:** Unblock LDC-006 (Lisbon Dog Care). 12 days stale is approaching the 14-day escalation threshold.
**Priority 3:** Start Vivenda Creative brand positioning. Cross-division DIVA + DARIO pipeline opportunity.

### Skill Health Alert
- dario-offer revision rate is 40% — do NOT run for new clients until RAG is enriched with pricing data
- seo-local is on a 3-week improvement streak (+3.2 pts) — keep current approach

---
*Generated by LUCAS Analytics. Data from: tasks/done/, skill-metrics.yaml, budgets/2026-04.yaml, audit/*
```

### Delivery Options

```
1. Display in terminal: default when user runs /lucas-analytics weekly
2. Save to Obsidian: save to D.A.R.I.O vault at 05 - Claude - IA/Outputs/YYYY-MM-DD - Weekly Digest.md
3. Both: display + save (recommended for record-keeping)
```

### Automation via /loop

```
To run weekly digest every Friday at end of day:
  /schedule "lucas-analytics-weekly" --cron "0 18 * * 5" --command "/lucas-analytics weekly"

Or manual: /lucas-analytics weekly
```

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1: Dados reais de projetos (não placeholders)
- [ ] Todos os clientes referenciados têm `start_date` real e `monthly_retainer` confirmado
- [ ] `skills_used` lista apenas skills que existem no sistema LUCAS (sem nomes inventados)
- [ ] `total_tokens_invested` calculado a partir de tarefas reais em `tasks/done/`, não estimado
- [ ] `satisfaction` tem evidência (mensagem, NPS, renovação) — não assumido
- ❌ NOT delivery-ready: `client: cliente_x`, `monthly_retainer: ???`, `roi_multiplier: TBD`
- ✅ Delivery-ready: `client: atrium`, `monthly_retainer: 2500`, `start_date: "2025-11"`, `roi_multiplier: 600x`

### Gate 2: Skill Performance Dashboard com scores verificáveis
- [ ] Cada skill no dashboard tem ≥3 projetos analisados (não score de 1 único output)
- [ ] Revision rate calculado a partir de tasks que voltaram ao worker (não estimado)
- [ ] Tier C skills têm `root_cause` específico + `action` com owner e prazo
- [ ] Tendência (improving/stable/declining) tem pelo menos 2 pontos temporais comparados
- ❌ NOT delivery-ready: `| dario-offer | ~72 | high% | generic | fix somehow |`
- ✅ Delivery-ready: `| dario-offer | 72.0 | 40% | Generic value equations — sem pricing data PT | Ingest DataForSEO PT benchmarks até 2026-05-15 |`

### Gate 3: Domain Playbook com lógica causal (não só ordem)
- [ ] `optimal_skill_chain` explica *porquê* cada skill está naquela posição (dependências, não só sequência)
- [ ] `avoid` tem pelo menos 1 exemplo real de projeto que falhou por violar a regra
- [ ] `rag_context_needed` especifica fonte concreta (ex: "Google Maps reviews do restaurante + 3 competidores Cascais")
- [ ] `estimated_time` validado contra projetos reais — não teórico
- ❌ NOT delivery-ready: `avoid: "bad order"`, `rag_context_needed: "context"`, `projects_analyzed: 1`
- ✅ Delivery-ready: `avoid: "dario-offer antes de dario-brand — Mar & Brasa Q1 produziu value equation genérica, score 68"`, `projects_analyzed: 3`

### Gate 4: Revenue Attribution com ROI auditável
- [ ] `token_cost_estimate` usa taxa real do modelo (ex: Claude 3.5 Sonnet: $3/MTok input, $15/MTok output)
- [ ] `revenue_to_date` reflecte apenas pagamentos recebidos, não contratos assinados
- [ ] ROI multiplier formula documentada: `(revenue_to_date / token_cost_estimate)` — não inventada
- [ ] Skills sem revenue attribution têm flag explícito `revenue_impact: indirect` ou `not_yet_measured`
- ❌ NOT delivery-ready: `roi_multiplier: muito alto`, `revenue_to_date: estimado ~5000`
- ✅ Delivery-ready: `revenue_to_date: 15000`, `token_cost_estimate: 25.00`, `roi_multiplier: 600x  # 15000/25`

### Gate 5: Knowledge Graph — queries retornam dados, não templates
- [ ] Cada query de exemplo tem resposta real com nomes/datas/números do sistema actual
- [ ] "Stale projects" query usa data actual como referência (não `>30 days` abstracto)
- [ ] "Best approach for [domain]" cita projetos reais como evidência, não só skill chain
- [ ] Queries de "declining quality" têm dois timestamps concretos comparados
- ❌ NOT delivery-ready: `Q: "All restaurant clients" A: [client_1], [client_2]`
- ✅ Delivery-ready: `Q: "All restaurant clients" A: Mar & Brasa (Cascais, desde 2026-04), próximo cliente pendente onboarding`

### Gate 6: Output usa CLIENT NAME + dados REAIS, sem angle-brackets
- [ ] Zero ocorrências de `<client_name>`, `[CLIENT]`, `{{placeholder}}`, `TBD`, `???`
- [ ] Todos os `domain: "restaurant"` têm pelo menos 1 projeto real como âncora
- [ ] Competitive Intelligence alerts referem keywords reais do cliente (ex: "restaurante cascais vista mar"), não `[keyword]`
- [ ] Módulo 5 tem pelo menos 1 alerta real ou "sem alertas activos desde YYYY-MM-DD" — não template vazio
- ❌ NOT delivery-ready: `competitor: [competitor_name]`, `keyword: [client_target_keyword]`
- ✅ Delivery-ready: `keyword: "restaurante cascais vista mar"`, `alert: "A Taberna do Mar subiu para #1 em 2026-04-12 — era posição #3"`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# LUCAS Analytics Report — Semana 2026-04-14

## Module 2: Skill Performance Dashboard — Abril 2026

### Tier A (Avg ≥ 85, Revision < 10%)
| Skill            | Score | Rev% | Best Domain | Tokens |
|------------------|-------|------|-------------|--------|
| seo-local        | 91.5  | 0%   | restaurant  | 3 100  |
| dario-brand      | 87.3  | 8%   | any         | 2 200  |
| seo-technical    | 86.8  | 5%   | any         | 2 800  |

### Tier B (Avg 70–84, Revision 10–25%)
| Skill              | Score | Rev% | Issue                         | Fix                                      |
|--------------------|-------|------|-------------------------------|------------------------------------------|
| seo-plan           | 84.5  | 12%  | Keywords thin sem DataForSEO  | Enriquecer RAG com export DataForSEO PT  |
| dario-story-circle | 82.0  | 15%  | Genérico sem contexto cliente | Exigir brand doc antes de activar        |

### Tier C — NEEDS ATTENTION
| Skill                  | Score | Rev% | Root Cause                    | Action                              | Prazo      |
|------------------------|-------|------|-------------------------------|-------------------------------------|------------|
| dario-offer            | 72.0  | 40%  | Sem pricing data PT           | Ingest benchmarks DataForSEO PT     | 2026-05-01 |
| dario-financial-model  | 74.5  | 30%  | Sem benchmarks mercado PT     | Ingest INE + Banco Portugal datasets| 2026-05-15 |

---

## Module 1: Domain Playbook — Restaurant (3 projetos analisados)

```yaml
domain: "restaurant"
projects_analyzed: 3  # Mar & Brasa, [onboarding Q2-A], [onboarding Q2-B]
avg_quality: 87.5
anchor_project: "mar-brasa (2026-04, Cascais)"

optimal_skill_chain:
  - dario-brand     # Sempre primeiro — define tom p/ todos os outros. Mar & Brasa: 92
  - dario-naming    # Paralelo com seo-local — naming precisa do brand doc
  - seo-local       # Crítico para restaurantes, depende de GBP e morada real. 91 avg
  - seo-plan        # Depois do brand — keywords alinhadas com posicionamento. 84 avg
  - dario-story-circle  # Depois de brand+naming — hero/conflict já definido. 85 avg

avoid:
  - "dario-offer antes de dario-brand — Mar & Brasa Q1-2026 produziu value equation
     genérica ('comida boa, preço justo'). Score: 68. Corrigido após brand doc."

rag_context_needed:
  - "Google Maps reviews do restaurante (min 50 reviews)"
  - "3 competidores directos com distância <2 km + respectivos menus"
  - "Preços médios da área (fonte: The Fork / Zomato scrape)"
  - "GBP listing completo do cliente"

estimated_tokens: 35 000
estimated_time: "15–20 min (validado em Mar & Brasa: 17 min)"
```

---

## Module 3: Revenue Attribution — Abril 2026

### Por Cliente
| Cliente          | Retainer/mês | Início     | Tokens     | Custo Token | Revenue Acum. | ROI    |
|------------------|-------------|------------|------------|-------------|---------------|--------|
| Atrium           | 2 500 EUR   | 2025-11    | 250 000    | 25,00 EUR   | 15 000 EUR    | 600x   |
| Mar & Brasa      | 1 500 EUR   | 2026-04    | 34 000     | 3,40 EUR    | 1 500 EUR     | 441x   |

*ROI = revenue_acumulado / custo_tokens. Custo: Claude 3.5 Sonnet $3/MTok input.*

### Por Skill
| Skill        | Projectos | Revenue Médio/Proj | Custo Token | ROI   |
|--------------|-----------|-------------------|-------------|-------|
| seo-audit    | 5         | 2 000 EUR         | 3,50 EUR    | 571x  |
| dario-brand  | 4         | 1 500 EUR         | 2,20 EUR    | 681x  |
| dario-wp-audit | 3       | 1 800 EUR         | 4,00 EUR    | 450x  |

---

## Module 5: Competitive Intelligence — Alertas Activos

**Cliente: Mar & Brasa (Cascais)**
- ⚠️ `2026-04-12` — "A Taberna do Mar" subiu para posição #1 em "restaurante cascais vista mar"
  (Mar & Brasa desceu de #2 para #3). Acção recomendada: publicar 2 posts GBP esta semana.
- ✅ Sem novos competidores detectados no raio 2 km desde 2026-03-01.

**Cliente: Atrium (Lisboa)**
- ✅ Sem movimentos relevantes. Última verificação: 2026-04-13.
- Próxima verificação programada: 2026-04-21.
```

---

## Output anti-patterns

- Dashboard gerado sem dados reais: scores inventados, revision rates a zero porque "ainda não há histórico" — se não há dados suficientes, diz explicitamente `insufficient_data: true` em vez de fingir métricas
- ROI calculado com revenue futuro/contratual em vez de pagamentos recebidos — infla artificialmente o ROI e perde credibilidade quando confrontado
- Domain Playbook com `projects_analyzed: 1` — um único projecto não é padrão, é anedota; exige mínimo 2
- Knowledge Graph queries com respostas template em vez de dados do sistema: `A: [client_name]` em vez de `A: Mar & Brasa (Cascais)`
- Competitive Intelligence vazia com texto genérico "sem alertas" sem data de verificação — cliente não sabe se foi verificado hoje ou há 3 meses
- Token cost calculado sem especificar modelo e taxa usada — impossível auditar ou replicar o ROI
- Tier C skills sem prazo e owner para a acção correctiva — lista de problemas sem accountability não resolve nada
- Módulo 5 truncado (o SKILL.md original corta em "Industry tren") — entregar output com conteúdo incompleto do template sem flag explícita ao cliente
