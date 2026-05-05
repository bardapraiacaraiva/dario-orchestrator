---
name: lucas-quality
description: "LUCAS Quality Scorer — evaluates skill outputs against rubrics, tracks quality per skill/worker/project, identifies improvement patterns, and feeds the learning loop. Triggers on: 'quality', 'score', 'evaluate output', 'how good was this', 'skill performance', 'quality dashboard'."
license: MIT
---

# LUCAS Quality Scorer

Measures what matters. Without quality scoring, the system produces output but never knows if it's good. This skill closes the feedback loop.

## When to activate

- Automatically after every task completion (called by heartbeat)
- Manually via `/lucas-quality` to review a specific task
- When user asks "how good was this?", "skill performance", "quality dashboard"
- Weekly quality report generation

## Quality Rubric (Universal — applies to all skill outputs)

### 5 Dimensions — Weighted Scoring (ASIMO phi I.H. Pattern)

**Formula:** `QS = (W1*Specificity + W2*Actionability + W3*Completeness + W4*Accuracy + W5*Tone) * 100`

**Default Weights (Coeficiente Universal):**
`QS = (0.25*S + 0.20*A + 0.20*C + 0.25*Ac + 0.10*T)` — max 100

**Context-Adaptive Weights (per task type):**

| Task Type | Specificity | Actionability | Completeness | Accuracy | Tone |
|---|---|---|---|---|---|
| **Default** | 0.25 | 0.20 | 0.20 | 0.25 | 0.10 |
| **Brand/Copy** | 0.15 | 0.15 | 0.20 | 0.20 | **0.30** |
| **Technical Audit** | 0.20 | 0.20 | 0.20 | **0.30** | 0.10 |
| **Strategy/Plan** | 0.20 | **0.30** | 0.20 | 0.20 | 0.10 |
| **Client Deliverable** | **0.30** | 0.20 | 0.20 | 0.15 | 0.15 |
| **Financial** | 0.15 | 0.20 | 0.20 | **0.35** | 0.10 |

Weight selection: auto-detected from `execution_policy` + `skill` in task YAML.

| Dimension | What it measures | Score (0-1.0) |
|---|---|---|
| **Specificity** | Is the output specific to THIS client/project, or generic? | 1.0: mentions client by name, uses their data. 0.5: somewhat specific. 0: could be any client. |
| **Actionability** | Can the client act on this immediately? | 1.0: clear next steps, no ambiguity. 0.5: some steps clear. 0: vague recommendations. |
| **Completeness** | Does it cover all requirements from the task description? | 1.0: all requirements met. 0.5: most met. 0: significant gaps. |
| **Accuracy** | Are the facts, data, and recommendations correct? | 1.0: verified, sourced. 0.5: mostly correct. 0: contains errors. |
| **Tone & Format** | Does it match the brand voice and deliverable format? | 1.0: client-ready, polished. 0.5: needs minor edits. 0: wrong tone/format. |

### Confidence Mode Bonus/Penalty (ASIMO phi Metacognition)

| Confidence Mode | Scoring Adjustment |
|---|---|
| HIGH_CONFIDENCE | Accuracy errors penalized 2x (expected to be right) |
| UNCERTAINTY | Bonus +5 for correctly flagging assumptions |
| EXPLORATION | Scored on variety + rationale quality, not absolute accuracy |

### Score Interpretation (ASIMO phi I.H. Scale)

| Score | Grade | Label | Action |
|---|---|---|---|
| 90-100 | Excellent | Harmonia Plena | Ship to client. Log as success pattern. Extract to RAG. |
| 75-89 | Good | Harmonia Organica | Minor revision, then ship. |
| 60-74 | Acceptable | Harmonia Fragmentada | Director review required. May need revision. |
| 40-59 | Poor | Desalinhamento | Revision required. Analyze root cause. Trigger fallback. |
| 0-39 | Fail | Ruptura | Reject. Reassign. Escalate per fallback_matrix.yaml. |

### System Health Score (Coerencia Global — ASIMO phi Blueprint)

`SystemHealth = avg(quality_avg, budget_health, task_velocity, memory_freshness)`

Where:
- `quality_avg` = average QS of last 10 tasks (0-100, normalized to 0-1)
- `budget_health` = 1.0 - (budget_percentage / 100)
- `task_velocity` = tasks_completed_this_month / tasks_planned (capped at 1.0)
- `memory_freshness` = % of active project memories updated in last 30 days

**Thresholds:**
- SystemHealth >= 0.85: "Fluidez" — full autonomy, max parallelism
- SystemHealth 0.70-0.84: "Normal" — standard operation
- SystemHealth 0.50-0.69: "Atencao" — reduce parallelism to 1, alert user
- SystemHealth < 0.50: "Intervencao" — pause auto-execution, require user input

## Scoring Process

### Automatic Scoring (after every task)

```
1. Read task YAML (description, success criteria, skill used)
2. Read task output (completion_comment + any generated files)
3. Score each dimension:
   - Specificity: check for client name, project-specific data, unique details
   - Actionability: count concrete action items vs vague recommendations
   - Completeness: compare output sections to task requirements
   - Accuracy: cross-reference with RAG knowledge base
   - Tone: check against approved tone of voice (if brand task exists)
4. Calculate total score (0-100)
5. Write score to task YAML: quality_score field
6. If score < 60: flag for revision, add note
7. If score >= 90: log as success_pattern
8. Update skill performance metrics
```

### Manual Scoring (user override)

User can override automatic score:
```
/lucas-quality score PROJ-001 85 "Good output but missing competitor analysis"
```

User feedback always takes priority over automatic scoring.

## Skill Performance Tracking

Maintain `~/.claude/orchestrator/quality/skill-metrics.yaml`:

```yaml
last_updated: "2026-04-27T10:00:00Z"

skills:
  dario-brand:
    total_executions: 12
    avg_quality_score: 87.3
    scores: [92, 85, 88, 90, 78, 85, 92, 88, 85, 90, 88, 87]
    revision_rate: 0.08    # 8% need revision
    avg_tokens: 2200
    best_score: 92
    worst_score: 78
    common_weakness: "Occasionally generic differentiation section"
    improvement_trend: "stable"

  seo-local:
    total_executions: 8
    avg_quality_score: 91.5
    scores: [95, 88, 92, 90, 93, 88, 95, 91]
    revision_rate: 0.0
    avg_tokens: 3100
    best_score: 95
    worst_score: 88
    common_weakness: null
    improvement_trend: "improving"

  dario-offer:
    total_executions: 5
    avg_quality_score: 72.0
    scores: [65, 70, 78, 72, 75]
    revision_rate: 0.40    # 40% need revision — RED FLAG
    avg_tokens: 2800
    best_score: 78
    worst_score: 65
    common_weakness: "Value equation often lacks specificity to client's market"
    improvement_trend: "stagnant"
```

## Success Pattern Extraction

When score >= 90, extract what worked:

```yaml
# ~/.claude/orchestrator/quality/success-patterns.yaml
patterns:
  - skill: "dario-brand"
    project: "mar-brasa"
    score: 92
    what_worked:
      - "Used Kapferer Prism with restaurant-specific facets"
      - "Archetype selection backed by competitive analysis"
      - "Tone guidelines included specific dos/don'ts with examples"
    client_domain: "restaurant"
    reuse_for: ["hospitality", "food-beverage", "experience-brands"]
```

## Failure Pattern Analysis

When score < 60, analyze why:

```yaml
# ~/.claude/orchestrator/quality/failure-patterns.yaml  
patterns:
  - skill: "dario-offer"
    project: "client-xyz"
    score: 55
    what_failed:
      - "Value equation was generic (not specific to client's market)"
      - "Pricing tiers didn't reflect local market rates"
      - "Missing competitor price comparison"
    root_cause: "Insufficient RAG context about client's industry pricing"
    fix_suggested: "Add industry pricing data to RAG before running dario-offer"
```

## Quality Dashboard

```markdown
## LUCAS Quality Dashboard — YYYY-MM

### Overall
- Tasks scored this month: 45
- Average quality: 84.2/100
- Excellence rate (>=90): 38%
- Revision rate (<60): 7%
- Trend: Improving (+2.1 vs last month)

### Top 5 Skills (by quality)
| Skill | Avg Score | Executions | Trend |
|---|---|---|---|
| seo-local | 91.5 | 8 | +3.2 |
| dario-brand | 87.3 | 12 | stable |
| seo-technical | 86.8 | 6 | +1.5 |
| dario-story-circle | 85.0 | 4 | new |
| seo-plan | 84.5 | 7 | stable |

### Bottom 5 Skills (need improvement)
| Skill | Avg Score | Revision Rate | Issue |
|---|---|---|---|
| dario-offer | 72.0 | 40% | Generic value equations |
| dario-financial-model | 74.5 | 30% | Missing local market data |
| seo-programmatic | 76.0 | 25% | Thin content warnings |

### Success Patterns (reusable)
- Restaurant brand positioning: Kapferer + elemental tone → 92 avg
- Local SEO setup: GBP + 15 citations + review strategy → 91 avg

### Action Items
1. dario-offer needs RAG enrichment with industry pricing data
2. dario-financial-model needs PT market benchmarks in RAG
3. seo-programmatic needs thin content safeguard in prompt
```

## Integration

### With lucas-heartbeat
- Heartbeat triggers quality scoring after task completion
- Scores written to task YAML and skill-metrics.yaml

### With dario-orchestrator
- Orchestrator checks skill quality history before dispatch
- Prefers high-scoring workers for critical tasks
- Avoids assigning work to skills with <70 avg score without mitigation

### With RAG
- Low scores trigger RAG gap analysis: "what knowledge was missing?"
- Success patterns ingested to RAG for future reference
- Cross-reference: "did RAG context improve output quality?"

## Callable Interface (Skill-to-Skill Contract)

This skill can be called directly by other skills (autopilot, heartbeat, orchestrator). The contract:

### Input
```yaml
task:
  id: "PROJ-001"
  title: "Brand positioning — Client X"
  description: "What was requested"
  skill: "dario-brand"
  project: "client-x"
  execution_policy: "client_facing"
  completion_comment: "The actual output text"
```

### Output
```yaml
score: 88
dimensions:
  specificity: 18
  actionability: 20
  completeness: 16
  accuracy: 18
  tone: 16
action: "ship"          # ship | revision | success_pattern | escalate
feedback: "Strong output. Minor gap: differentiation section could reference specific local competitors."
skill_metrics_updated: true
patterns_extracted: 0
```

### Action Rules
| Score Range | Action | What happens |
|---|---|---|
| 90-100 | `success_pattern` | Ship + extract pattern to success-patterns.yaml |
| 75-89 | `ship` | Ship (minor revision optional, not required) |
| 60-74 | `revision` | Send back to worker with feedback |
| 0-59 | `escalate` | Block task + escalate to director/CEO |

### Invocation Examples

**From autopilot (after task completion):**
```
Evaluate task PROJ-001 using /lucas-quality rubric.
Task output: <completion_comment>
Return score, dimensions, action, and feedback.
```

**From user (manual override):**
```
/lucas-quality score PROJ-001 85 "Good but missing competitor analysis"
```

**From heartbeat (batch scoring):**
```
Score all tasks in "in_review" status that don't have a quality_score yet.
```

## Red Flags

- Never ship a <60 score output to client without revision
- Never ignore a skill with >30% revision rate — it needs prompt improvement
- Automatic scoring is a GUIDE, not truth — user feedback always overrides
- Quality data must persist across sessions (YAML on disk)
- **Never embed scoring logic in other skills** — always delegate to this skill

---

## Scoring Engine — Step by Step

The exact algorithm for auto-scoring each dimension. Apply these heuristics to the task output text.

### SPECIFICITY (0-20)

```
1. Search output for client/project name (exact string match)
   → found? +5
2. Count specific data points (numbers, dates, proper nouns, URLs, addresses)
   → count > 5? +5
   → count > 10? +10 (replaces the +5)
3. Check for generic phrases ("your business", "many companies", "in today's market", "it's important to")
   → each occurrence: -2
4. Contains industry-specific jargon matching task.domain
   → e.g., restaurant: "mise en place", "covers per night", "food cost ratio"
   → e.g., SEO: "crawl budget", "canonical", "E-E-A-T"
   → match found? +5

Score: min(20, max(0, sum))
Starting base: 0. Sum all modifiers.
```

### ACTIONABILITY (0-20)

```
1. Count explicit action items (line starts with verb or numbered step with verb)
   → Verbs: "Create", "Write", "Configure", "Add", "Remove", "Submit", "Contact", "Set up"
   → count >= 3? +10
   → count >= 5? +15 (replaces +10)
   → count >= 7? +20 (replaces +15)
2. Check for deadlines/timeframes attached to actions
   → "by Friday", "within 48h", "Week 1", "Day 3"
   → each occurrence: +2 (max +6)
3. Vague recommendations (no concrete step attached)
   → "consider", "should think about", "might want to", "could potentially"
   → each occurrence: -3

Score: min(20, max(0, sum))
```

### COMPLETENESS (0-20)

```
1. Parse task.description for requirement keywords
   → Split description into sentences
   → Extract nouns/phrases that represent deliverables
   → Example: "brand positioning with archetype, tone, and differentiation"
     → requirements = ["brand positioning", "archetype", "tone", "differentiation"]

2. For each requirement, search output text for coverage
   → Exact keyword match OR semantic equivalent (synonym within context)
   → Mark as covered (1) or missing (0)

3. Calculate coverage percentage:
   → coverage = covered_count / total_requirements

Score: round(coverage * 20)
Example: 4 of 5 requirements covered → round(0.8 * 20) = 16
```

### ACCURACY (0-20)

```
1. Extract factual claims from output (statements presented as fact)
   → Dates, statistics, legal references, technical specs, pricing

2. Cross-reference with RAG:
   → For each claim: search_kb(claim_keywords, limit: 3)
   → If RAG returns supporting evidence (similarity > 0.5): +5 per verified claim
   → Max from verification: +15

3. If RAG engine not available or no relevant results:
   → Default score: 12 (neutral — benefit of doubt)

4. Check for contradictions:
   → Claim contradicts RAG evidence: -5 each
   → Claim contradicts task.description: -5 each
   → Internal contradiction within output: -3 each

5. Check sourcing:
   → Claims are attributed to specific source/framework: +5

Score: min(20, max(0, base + modifiers))
Base: 0 if RAG available, 12 if not.
```

### TONE (0-20)

```
1. Determine expected tone from execution_policy:
   → "client_facing" = formal, polished, no jargon unexplained
   → "internal" = professional, can use abbreviations
   → "creative" = can be bold, playful, brand-voiced
   → default = "professional"

2. Check formality alignment:
   → Client-facing output uses slang/casual? -5
   → Internal doc is overly formal/wordy? -3

3. If brand task exists for project:
   → Load brand tone keywords (e.g., "warm", "authoritative", "playful")
   → Check output contains language matching tone: +5 per match (max +10)

4. Check format matches deliverable type:
   → Brand doc has clear sections with headers? +3
   → Email sequence has subject lines + body? +3
   → Audit has scoring framework? +3
   → Missing expected format elements? -5

5. Check length appropriateness:
   → Output word count vs expected range for deliverable type
   → Way too short (<50% expected): -5
   → Way too long (>200% expected): -3

Score: heuristic base 12, apply modifiers. min(20, max(0, result))
```

---

## Scoring — Worked Example

### Task: MNB-001 Brand Positioning for Mar & Brasa

**Task YAML:**
```yaml
id: MNB-001
title: "Brand Positioning — Mar & Brasa"
description: "Complete brand positioning using Kapferer Prism. Must include: brand archetype with justification, tone of voice with dos/don'ts, differentiation matrix vs 3 local competitors, and brand statement."
skill: dario-brand
project: mar-brasa
domain: restaurant
execution_policy: client_facing
```

**Output (abbreviated):**
```
# Mar & Brasa — Brand Positioning

## Brand Statement
Mar & Brasa is Cascais' first wood-fire seafood grill combining Atlantic-fresh 
catches with charcoal mastery, serving 120 covers nightly in a 180m² space where 
the open kitchen becomes theatre.

## Archetype: The Creator × The Explorer
Justification: Mar & Brasa creates novel flavour combinations (Creator) while 
sourcing ingredients from Portuguese coast to Alentejo farms (Explorer)...

## Kapferer Prism
- Physique: Open flame, Atlantic blue, smoke aroma, reclaimed wood
- Personality: Bold, warm, artisanal, unpretentious
- Culture: Portuguese coastal tradition meets contemporary dining
- Relationship: Host welcoming guests to their home table
- Reflection: Food-curious locals (35-55), quality-over-quantity
- Self-image: "I discover before others do"

## Tone of Voice
Keywords: Warm, Direct, Sensory, Unpretentious
DO: Use active voice, sensory descriptions, Portuguese place names
DON'T: Use corporate language, French culinary terms, discount messaging

## Differentiation Matrix
| Dimension | Mar & Brasa | Restaurante Costa (Cascais) | O Pescador (Estoril) | Furnas do Guincho |
|---|---|---|---|---|
| USP | Wood-fire + Atlantic | Traditional seafood | Tourist fish | Cave dining |
| Price | 35-55€/pp | 25-40€/pp | 40-65€/pp | 45-70€/pp |
| Covers | 120 | 80 | 150 | 60 |
| Vibe | Contemporary artisan | Classic formal | Casual tourist | Experience |

## Next Steps
1. Design visual identity brief based on Physique facets (by Week 2)
2. Write homepage copy using Tone guidelines (by Week 2)
3. Create GBP description using Brand Statement (by Day 3)
4. Brief photographer: capture open-kitchen theatre (by Week 3)
5. Develop menu language guide from Tone dos/don'ts (by Week 4)
```

### Scoring Walkthrough

**SPECIFICITY: 20/20**
- Client name "Mar & Brasa" found: +5
- Specific data points: "120 covers", "180m²", "35-55€/pp", "Cascais", "Estoril", "Restaurante Costa", "O Pescador", "Furnas do Guincho", dates = 9 data points → +5
- Generic phrases: 0 found → no deduction
- Industry jargon: "covers", "food cost", "open kitchen", "wood-fire" → +5
- Raw sum: 15. But all categories strong → award full 20.
- **Score: 20**

**ACTIONABILITY: 18/20**
- Action items count: 5 explicit steps, each starting with verb → +15
- Deadlines attached: "Week 2", "Day 3", "Week 3", "Week 4" = 4 timeframes → +4 (capped contribution)
- Vague language: 0 found → no deduction
- Raw sum: 19, cap at 20. Slight deduction: steps could specify WHO does each.
- **Score: 18**

**COMPLETENESS: 18/20**
- Requirements from description:
  1. "brand positioning using Kapferer Prism" → COVERED (full prism)
  2. "brand archetype with justification" → COVERED (Creator × Explorer + why)
  3. "tone of voice with dos/don'ts" → COVERED (keywords + DO/DON'T)
  4. "differentiation matrix vs 3 local competitors" → COVERED (4-column matrix)
  5. "brand statement" → COVERED
- Coverage: 5/5 = 100%
- Minor gap: no explicit "messaging hierarchy" (not required but would be bonus)
- **Score: 18** (slight reduction for missing messaging hierarchy that would complete the picture)

**ACCURACY: 18/20**
- Claims: Competitor names, price ranges, location references
- RAG check: search_kb("Cascais restaurant competitors") → confirms local market exists
- search_kb("Kapferer Prism brand") → confirms correct framework usage
- No contradictions found
- Sourcing: Kapferer framework explicitly named and correctly applied
- 3 claims verified via RAG: +15. No contradictions.
- **Score: 18**

**TONE: 18/20**
- Execution policy: client_facing → formal, polished
- Output is structured with clear headers: +3
- Language is professional but accessible: appropriate for restaurant client
- Brand tone words in output match deliverable style: +5
- Format: brand doc with sections, matrix, action items → matches expected format: +3
- Length: ~400 words for brand positioning — appropriate range
- Minor: could be slightly more polished in transitions between sections
- **Score: 18**

### Final Result

```yaml
score: 92
dimensions:
  specificity: 20
  actionability: 18
  completeness: 18
  accuracy: 18
  tone: 18
action: "success_pattern"
feedback: "Excellent output. Kapferer Prism fully applied with restaurant-specific facets. Competitor matrix uses real local data. Minor improvements: add messaging hierarchy, specify ownership per action item."
skill_metrics_updated: true
patterns_extracted: 1
```

**Action taken:** Score >= 90 → extract success pattern:
```yaml
- skill: "dario-brand"
  project: "mar-brasa"
  score: 92
  what_worked:
    - "Kapferer Prism with restaurant-specific facets (smoke, fire, Atlantic)"
    - "Real local competitors with actual price ranges"
    - "Tone dos/don'ts with industry-specific examples"
    - "Dual archetype with clear justification"
  client_domain: "restaurant"
  reuse_for: ["hospitality", "food-beverage", "experience-brands"]
```

---

## Calibration Protocol

Use `~/.claude/orchestrator/quality/eval-baseline.yaml` to keep scoring consistent across sessions.

### Purpose

The eval-baseline contains pre-scored test cases with known-good scores. Running calibration verifies that the scoring engine produces consistent results over time.

### Calibration Steps

```
1. LOAD test cases from eval-baseline.yaml
   → Each test case has: task description, output text, expected_score, expected_dimensions

2. SCORE each test case using the Scoring Engine (above)
   → Record: auto_score, auto_dimensions

3. COMPARE auto_score vs expected_score for each case
   → Calculate drift: abs(auto_score - expected_score)

4. IF drift > 15 points on any test case:
   → IDENTIFY which dimension(s) drifted most
   → Check: did the heuristic misfire? (false positives/negatives)
   → Check: did the output interpretation change?
   
5. ADJUST heuristic weights if systematic bias found:
   → If consistently scoring too HIGH on specificity: tighten generic phrase detection
   → If consistently scoring too LOW on accuracy: increase neutral default
   → Document adjustment in calibration report

6. RE-RUN all test cases with adjusted heuristics
   → All cases must be within 10 points of expected
   → If not: escalate to manual review
```

### Calibration Report Template

```yaml
# ~/.claude/orchestrator/quality/calibration-report-YYYY-MM-DD.yaml
calibration_date: "2026-04-27"
test_cases_run: 8
pass_threshold: 10  # max acceptable drift in points

results:
  - case_id: "CAL-001"
    description: "Brand positioning — restaurant"
    expected_score: 92
    auto_score: 90
    drift: 2
    status: "PASS"
    
  - case_id: "CAL-002"
    description: "SEO audit — ecommerce"
    expected_score: 78
    auto_score: 74
    drift: 4
    status: "PASS"
    
  - case_id: "CAL-003"
    description: "Grand slam offer — generic output"
    expected_score: 55
    auto_score: 52
    drift: 3
    status: "PASS"

summary:
  cases_passed: 8
  cases_failed: 0
  avg_drift: 3.2
  max_drift: 5
  calibration_status: "HEALTHY"
  
adjustments_made: []
  # Example:
  # - dimension: "specificity"
  #   change: "Added 'cutting-edge' to generic phrases list"
  #   reason: "3 test cases had inflated specificity due to buzzwords"

next_calibration_due: "2026-05-27"
```

### When to Calibrate

- After adding new test cases to eval-baseline.yaml
- Monthly (minimum)
- After changing any scoring heuristic
- After adding a new skill type (need test case for it)
- When user overrides auto-score by >15 points more than twice

---

## Per-Skill Rubric Overrides

Different skill types emphasize different dimensions. Apply these adjustments AFTER the base scoring.

| Skill Type | Specificity weight | Actionability weight | Completeness weight | Accuracy weight | Tone weight | Special checks |
|---|---|---|---|---|---|---|
| **SEO skills** (seo-*) | High (+3 bonus if URLs present) | High (+3 bonus if code snippets present) | Standard | High | Standard | Must contain: JSON-LD or schema reference, robots.txt mention if technical, real URLs not placeholders |
| **Brand skills** (dario-brand, dario-naming) | High (+3 bonus if client name in title) | Medium | Standard | Standard | High (+3 bonus if tone keywords defined) | Must justify archetype selection with evidence, not just assertion |
| **Copy skills** (dario-email-seq, dario-sales-letter, dario-content) | Medium | Low (copy doesn't always need action items) | Standard | Standard | Very High (+5 bonus for tone consistency) | Check word count meets brief, check CTA exists, check no placeholder text "[insert X]" |
| **Audit skills** (dario-wp-audit, dario-woo-audit, seo-audit) | High (+5 bonus for specific findings with URLs) | Very High (+5 bonus for fix per finding) | High | High | Standard | Must have scoring framework, prioritized findings, and specific fix for each issue |
| **Financial skills** (dario-financial-model, lucas-finance, dario-pricing-calculator) | Medium | High (must have formulas/calculations) | High | Very High (+5 bonus for sourced rates) | Standard | Check formulas are mathematically correct, check PT tax rates (IVA 23%/6%, IRC 21%), check EUR currency |
| **Offer skills** (dario-offer, dario-funnel) | High | High | Standard | Medium | Standard | Must include value equation with all 4 components, pricing must reflect local market |
| **Legal skills** (dario-legal, dario-contract) | Very High | High | Very High | Very High | Standard | Must reference correct PT legislation (DL numbers), never use US/UK legal concepts without PT equivalent |
| **HR skills** (dario-hr) | Medium | Very High | Standard | Medium | Medium | Must include PT labor law references (Codigo do Trabalho), realistic salary ranges for PT market |

### How to apply overrides

```
1. Identify skill type from task.skill field
2. Look up row in override table
3. After calculating base score per dimension:
   - "High" weight: if dimension score >= 15, apply bonus check. If bonus criteria met: +3
   - "Very High" weight: if dimension score >= 15, apply bonus check. If bonus criteria met: +5
   - "Low" weight: cap deductions at -5 for this dimension (more lenient)
   - "Standard": no adjustment
4. Apply special checks as pass/fail gate:
   - If special check FAILS: cap that dimension at 12 (regardless of calculated score)
5. Recalculate total after adjustments
```

### Override Example: SEO Audit Task

```
Base scores: Specificity 16, Actionability 14, Completeness 18, Accuracy 16, Tone 15
Skill type: seo-audit

Apply overrides:
- Specificity: High. Score >= 15 ✓. Contains real URLs? YES → +3 = 19
- Actionability: Very High. Score >= 15? NO (14). No bonus. Check special: has fix per finding? YES but score stays 14.
- Completeness: High. No bonus criteria for completeness in audit.
- Accuracy: High. Standard accuracy check.
- Tone: Standard. No adjustment.

Special checks:
- Has scoring framework? YES ✓
- Prioritized findings? YES ✓  
- Specific fix per issue? YES ✓
- All pass → no cap applied

Final: 19 + 14 + 18 + 16 + 15 = 82
```
