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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Rubric dimensions scored with real data (not estimates)

- [ ] Cada dimensão (Specificity, Actionability, Completeness, Accuracy, Tone) tem score numérico entre 0.0 e 1.0
- [ ] O tipo de task foi identificado e os pesos context-adaptive foram aplicados (não os Default por omissão lazy)
- [ ] A fórmula `QS = (W1*S + W2*A + W3*C + W4*Ac + W5*T) * 100` foi calculada explicitamente, passo a passo
- [ ] O confidence mode (HIGH / UNCERTAINTY / EXPLORATION) foi declarado e ajuste aplicado

❌ NOT delivery-ready: "Score estimado: 78/100 — output razoável, pode melhorar."
✅ Delivery-ready: "Task Type: Client Deliverable → Pesos: S=0.30, A=0.20, C=0.20, Ac=0.15, T=0.15. Scores: S=0.90, A=0.80, C=1.0, Ac=0.85, T=0.90. QS = (0.30×0.90 + 0.20×0.80 + 0.20×1.0 + 0.15×0.85 + 0.15×0.90)×100 = **87.25/100**. Confidence: HIGH_CONFIDENCE — sem penalidade aplicada."

---

### Gate 2 — Grade label + ação consequente declarados

- [ ] Grade label (Harmonia Plena / Harmonia Organica / Harmonia Fragmentada / Desalinhamento / Ruptura) explicitamente atribuído
- [ ] Ação imediata prescrita: ship / minor revision / director review / revision required / reject+escalate
- [ ] Se score < 60: root cause identificada (não apenas "needs improvement")
- [ ] Se score ≥ 90: marcado para log como success_pattern + extração para RAG

❌ NOT delivery-ready: "Score 65 — precisa de revisão."
✅ Delivery-ready: "Score 65/100 → **Harmonia Fragmentada** → Director review obrigatório. Root cause: Accuracy=0.50 (dados financeiros da Cuidai não verificados contra RAG) + Specificity=0.55 (secção de diferenciação genérica, sem referência ao modelo de subscrição €29/mês). Ação: reprocessar com contexto `cuidai-pricing-2025.yaml`."

---

### Gate 3 — Skill performance metrics actualizadas em `skill-metrics.yaml`

- [ ] `total_executions` incrementado para a skill avaliada
- [ ] Array `scores` tem o novo score appended
- [ ] `avg_quality_score` recalculado (não estimado — média aritmética real dos scores no array)
- [ ] `revision_rate` recalculado; se ≥ 0.30, flag RED explícita no output
- [ ] `improvement_trend` revisitado: "improving" / "stable" / "declining" com critério declarado (ex: últimas 5 execuções vs 5 anteriores)

❌ NOT delivery-ready: "`dario-offer` avg: ~72, tendência ok."
✅ Delivery-ready: "`dario-offer` → scores: [65,70,78,72,75,**80**] → avg recalculado: 73.3 (+1.3 vs 72.0). revision_rate: 3/6 = 0.50 → 🔴 RED FLAG. improvement_trend: últimas 3 execuções [75,75,80] vs primeiras 3 [65,70,78] → média 76.7 vs 71.0 → **'improving'**."

---

### Gate 4 — SystemHealth calculado com todas as 4 variáveis

- [ ] `quality_avg` calculado sobre as últimas 10 tasks (ou todas se < 10), normalizado 0–1
- [ ] `budget_health`, `task_velocity`, `memory_freshness` têm valores concretos (não "N/A" ou "a verificar")
- [ ] `SystemHealth = avg(quality_avg, budget_health, task_velocity, memory_freshness)` calculado explicitamente
- [ ] Threshold label atribuído: Fluidez / Normal / Atencao / Intervencao — com consequência operacional activada

❌ NOT delivery-ready: "SystemHealth ≈ 0.78 — Normal. Sistema a funcionar bem."
✅ Delivery-ready: "quality_avg=(87.3/100)=0.873 | budget_health=1-(34/100)=0.660 | task_velocity=11/15=0.733 | memory_freshness=8/10 memories updated=0.800 → SystemHealth=avg(0.873,0.660,0.733,0.800)=**0.767** → **Normal** → standard operation, parallelism mantido."

---

### Gate 5 — Feedback loop fechado (manual override + RAG log)

- [ ] Se user override foi fornecido (`/lucas-quality score PROJ-XXX`), esse score substituiu o automático e razão foi registada
- [ ] Se score ≥ 90: entrada adicionada ao success_pattern log com skill + task_type + winning dimensions
- [ ] Se score < 60: `common_weakness` field actualizado com pattern específico (não genérico)
- [ ] Output referencia o ficheiro concreto onde o score foi persistido (`skill-metrics.yaml` path explícito)

❌ NOT delivery-ready: "Pattern de fraqueza: output podia ser mais específico."
✅ Delivery-ready: "common_weakness actualizado → `dario-brand`: 'Secção de diferenciação tende a omitir pricing anchor vs concorrência directa (Cuidai vs Kinder Care) quando task não inclui competitor_data explícito.' Ficheiro: `~/.claude/orchestrator/quality/skill-metrics.yaml` linha 14. Success pattern logged: `seo-local` × `Technical Audit` × Accuracy=0.95 → RAG entry `seo-local-success-2026-04-27`."

---

### Gate 6 — Output usa CLIENT NAME + dados reais, sem angle-brackets placeholder

- [ ] Nenhum `<client_name>`, `<score>`, `<skill>`, `<date>` presente no output final
- [ ] Datas são reais (formato ISO `2026-04-27`, não `YYYY-MM-DD`)
- [ ] Skill names são os reais do sistema (`dario-brand`, `seo-local`, `lucas-quality`), não genéricos
- [ ] Cliente ou projecto referenciado pelo nome real (Cuidai, SAQUEI, Atrium, LUSOconta, etc.)

❌ NOT delivery-ready: "Score para `<skill_name>` do projecto `<project_id>`: `<score>`/100 em `<date>`."
✅ Delivery-ready: "Score para `dario-brand` — PROJ-CUIDAI-007 (Cuidai Homepage Copy, 2026-04-27): **88.5/100** → Harmonia Organica → minor revision, then ship."

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / memória / dados reais do projeto
- 🟡 **assumed** — plausível mas precisa de confirmação do cliente antes de entregar
- 🟢 **projection** — forecast by design (não verificável — esperado pelo contexto)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs. o que precisa de verify. **Honest transparency > inflated delivery.**

---

❌ NOT delivery-ready:
> "QS médio do último mês: 84. Skill `brand-copy` com melhor performance. SystemHealth: 0.78."
> *(sem labels — reader assume que tudo é verified; pode estar a misturar actuals com placeholders)*

✅ Delivery-ready:
> - 🔵 **verified** — QS médio das últimas 10 tasks: **81.4** (calculado de `quality_score` fields em YAML)
> - 🔵 **verified** — Skill com menor score: `lucas-financial` → QS 58 (flagged para revision)
> - 🟡 **assumed** — `task_velocity` estimada em **0.87** (tasks_planned não confirmadas para este mês)
> - 🟡 **assumed** — `memory_freshness` calculada em **72%** (última sync de memória não datada na sessão actual)
> - 🟢 **projection** — SystemHealth projectado em **0.79 → "Normal"** (baseado nos valores acima; sujeito a confirmação dos 🟡 items)
> - 🟢 **projection** — Se score médio subir para ≥ 85 nas próximas 5 tasks → SystemHealth entra em **"Fluidez"** (full autonomy)

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — `tasks_planned` do mês validadas; data da última memory sync confirmada
- [ ] All 🔵 citations added — YAML `quality_score` fields referenciados por task ID
- [ ] All 🟢 projections labeled as such ao cliente — SystemHealth forecast apresentado como estimativa, não como estado actual

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## LUCAS Quality Report — PROJ-CUIDAI-007
**Gerado:** 2026-04-27T14:32:00Z | **Skill:** dario-brand | **Task:** Homepage copy refresh

---

### Score Breakdown

**Task Type detectado:** Client Deliverable
**Pesos aplicados:** Specificity=0.30 · Actionability=0.20 · Completeness=0.20 · Accuracy=0.15 · Tone=0.15
**Confidence Mode:** HIGH_CONFIDENCE (RAG knowledge base confirmado para Cuidai)

| Dimensão       | Score | Justificação                                                              |
|----------------|-------|---------------------------------------------------------------------------|
| Specificity    | 0.90  | Menciona "subscrição €29/mês", "cobertura Lisboa e Porto", nome Cuidai 7× |
| Actionability  | 0.85  | 4 CTA claros; 1 recomendação vaga ("melhorar SEO") sem keyword específica  |
| Completeness   | 1.00  | Todos os 5 blocos do brief cobertos (hero, features, pricing, FAQ, CTA)   |
| Accuracy       | 0.80  | Pricing verificado; claim "4.9★ App Store" não verificável via RAG        |
| Tone           | 0.95  | Alinhado com brand voice Cuidai: empático, directo, sem jargão médico     |

**QS = (0.30×0.90 + 0.20×0.85 + 0.20×1.00 + 0.15×0.80 + 0.15×0.95) × 100**
**QS = (0.270 + 0.170 + 0.200 + 0.120 + 0.143) × 100 = 90.3/100**

**HIGH_CONFIDENCE penalty check:** Accuracy < 1.0 → penalidade 2× em delta.
Accuracy raw delta = 0.20 × (1.0 - 0.80) = 0.04 → penalidade 2× = -0.04
**QS ajustado: 90.3 - 4.0 = 86.3/100**

---

### Grade: Harmonia Organica (75–89)

**Acção:** Minor revision, then ship.
**Revision point:** Verificar claim "4.9★ App Store" — confirmar com equipa Cuidai ou remover.
**Estimated revision time:** 10 min.

---

### skill-metrics.yaml update — dario-brand

```yaml
dario-brand:
  last_updated: "2026-04-27T14:32:00Z"
  total_executions: 13          # era 12
  scores: [92,85,88,90,78,85,92,88,85,90,88,87,86]  # 86.3 rounded
  avg_quality_score: 86.8       # recalculado: soma=1128/13
  revision_rate: 0.08           # 1 revision em 13 — mantém
  best_score: 92
  worst_score: 78
  common_weakness: "Unverified social proof claims (App Store ratings, review counts)"
  improvement_trend: "stable"   # últimas 5: [87,88,86,86,87] vs anteriores 5: [88,85,90,78,85]
```

---

### SystemHealth — 2026-04-27

| Variável          | Cálculo                                    | Valor  |
|-------------------|--------------------------------------------|--------|
| quality_avg       | avg últimas 10 tasks: 876/10               | 0.876  |
| budget_health     | 1 - (34% budget usado)                     | 0.660  |
| task_velocity     | 11 tasks completas / 15 planeadas          | 0.733  |
| memory_freshness  | 8/10 project memories updated < 30 dias    | 0.800  |
| **SystemHealth**  | avg(0.876, 0.660, 0.733, 0.800)            | **0.767** |

**Status: Normal** — standard operation. Parallelism mantido em 2.
⚠️ budget_health=0.660 é o indicador mais fraco — monitorizar na próxima semana.

---

### Feedback Loop

- ✅ Score < 90 (86.3) → NÃO adicionado a success_patterns
- 📝 common_weakness actualizado com novo padrão detectado
- 📁 Persistido em: `~/.claude/orchestrator/quality/skill-metrics.yaml`
- 🔁 Próxima avaliação automática: após próxima execução de `dario-brand`
```

---

## Output anti-patterns

- **Score sem breakdown dimensional** — "Output score: 78/100" sem mostrar S/A/C/Ac/T individualmente é inauditável e não accionável
- **Pesos Default aplicados a tudo** — usar 0.25/0.20/0.20/0.25/0.10 numa task financeira da LUSOconta ignora os pesos Accuracy=0.35 que são a única coisa que importa ali
- **SystemHealth com variáveis em N/A** — calcular SystemHealth com 2 de 4 variáveis reais contamina o threshold; se `memory_freshness` é desconhecido, declarar explicitamente e usar 0.5 como conservative default
- **revision_rate sem RED FLAG** — skill com revision_rate ≥ 0.30 que não dispara alerta visual leva o director a não intervir (padrão `dario-offer` no exemplo original ignorado durante semanas)
- **common_weakness genérico** — "output podia ser mais específico" não alimenta nenhum loop de melhoria; o pattern tem de ser reproducível e actionable para o próximo prompt engineer
- **Confidence Mode omitido** — HIGH_CONFIDENCE sem aplicar penalidade 2× em erros de Accuracy é o erro mais silencioso: infla scores de skills "confiantes mas erradas"
- **avg_quality_score estimado** — recalcular manualmente só quando "parece diferente" cria drift acumulado; a média tem de ser recalculada do array completo a cada update
- **User override sem registo de razão** — aceitar `/lucas-quality score PROJ-001 85` sem gravar o comentário do utilizador desperdiça o único sinal de qualidade ground-truth que o sistema tem
