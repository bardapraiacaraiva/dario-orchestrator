---
name: suply-supplier
description: "S.U.P.L.Y. Supplier Relationship Management — scorecards, development programs, risk assessment, dual sourcing, and performance reviews"
version: "1.0"
agent: SUPLY
tags: [SRM, supplier-scorecard, supplier-development, dual-sourcing, risk-assessment, performance-review]
---

# SUPLY Supplier Relationship Management Skill

## Triggers

Activate this skill when the user says or implies:
- "supplier relationship", "SRM", "vendor management"
- "supplier scorecard", "vendor scorecard", "supplier performance"
- "supplier development", "vendor development", "improve supplier"
- "dual sourcing", "multi-sourcing", "single source risk"
- "supplier risk", "supply risk", "vendor risk assessment"
- "supplier review", "performance review", "vendor evaluation"

## Workflow

### Step 1 — Supplier Segmentation
1. **Segmentation Criteria**
   - Annual spend volume (high/medium/low)
   - Strategic importance (criticality to your operations)
   - Supply risk (alternatives available, geographic concentration)
   - Innovation contribution (co-development, new technology)
2. **Supplier Tiers**
   - **Strategic Partners**: High spend + high criticality → deep collaboration, joint planning
   - **Preferred Suppliers**: Significant spend, reliable → long-term contracts, volume commitments
   - **Approved Suppliers**: Qualified, moderate spend → standard terms, periodic review
   - **Transactional Suppliers**: Low spend, commodities → catalog buying, minimal management
3. **Management Intensity**
   - Strategic: Monthly meetings, quarterly business reviews, annual summits
   - Preferred: Quarterly reviews, annual performance assessment
   - Approved: Semi-annual review, reactive management
   - Transactional: Annual renewal, automated purchasing

### Step 2 — Supplier Scorecard Design
1. **Performance Dimensions**
   - **Quality** (25%): PPM, reject rate, NCR count, audit score
   - **Delivery** (25%): On-time delivery rate, lead time adherence, flexibility
   - **Cost** (20%): Price competitiveness, cost reduction contributions, invoice accuracy
   - **Service** (15%): Responsiveness, communication, problem resolution speed
   - **Innovation** (15%): New product suggestions, process improvements, technology adoption
2. **Scoring Scale**
   - 5: Exceptional (exceeds requirements, best in class)
   - 4: Good (consistently meets all requirements)
   - 3: Acceptable (meets minimum requirements)
   - 2: Below expectations (frequent issues, improvement needed)
   - 1: Unacceptable (systemic failures, at risk of disqualification)
3. **Scorecard Cadence**
   - Strategic suppliers: Monthly updates, quarterly formal review
   - Preferred suppliers: Quarterly updates, annual formal review
   - Approved/Transactional: Annual update

### Step 3 — Supplier Performance Reviews
1. **Quarterly Business Review (Strategic Suppliers)**
   - Scorecard review with trend analysis
   - Open issues and corrective actions status
   - Volume forecast and capacity planning
   - Cost reduction and value engineering projects
   - Innovation pipeline and co-development updates
   - Relationship health assessment
2. **Annual Performance Assessment**
   - Year-in-review scorecards with year-over-year comparison
   - Total business value delivered (savings, innovations, reliability)
   - Tier adjustment recommendation (upgrade/maintain/downgrade/exit)
   - Next year objectives and improvement targets
3. **Consequence Management**
   - Score > 4.0: Reward (more business, longer terms, preferred status)
   - Score 3.0-4.0: Maintain (standard terms, monitor)
   - Score 2.0-3.0: Improve (corrective action plan required, probation)
   - Score < 2.0: Exit (phase out, find alternatives, terminate)

### Step 4 — Supplier Development Programs
1. **Development Triggers**
   - Scorecard consistently below 3.5 but supplier is strategically important
   - Quality or delivery issues that are systemic (not one-off)
   - Supplier willing to invest in improvement
   - No viable alternative supplier in the short term
2. **Development Activities**
   - Joint root cause analysis of performance gaps
   - Process improvement workshops (Lean, Six Sigma)
   - Quality system development (help achieve ISO certification)
   - Technology transfer and training
   - Capacity expansion support (volume guarantees for investment)
3. **Development Plan Structure**
   - Gap assessment (current vs. required capability)
   - Improvement actions with milestones and deadlines
   - Resources committed by both parties
   - Monthly progress reviews
   - Success criteria for program completion (scorecard targets)

### Step 5 — Supplier Risk Assessment
1. **Risk Categories**
   - **Financial Risk**: Supplier insolvency, cash flow problems, acquisition/merger
   - **Operational Risk**: Capacity constraints, quality failures, key person dependency
   - **Geographic Risk**: Natural disasters, political instability, trade restrictions
   - **Concentration Risk**: Single source, single location, single sub-tier supplier
   - **Compliance Risk**: Regulatory changes, sanctions, ESG violations
   - **Cyber Risk**: Data breaches, IT system failures, ransomware
2. **Risk Assessment Process**
   - Annual risk review for all active suppliers
   - Quarterly deep-dive for strategic suppliers
   - Event-triggered reassessment (natural disaster, financial news, geopolitical event)
   - Risk scoring: Likelihood (1-5) x Impact (1-5) = Risk Score (1-25)
3. **Risk Mitigation Strategies**
   - Dual/multi-sourcing for critical items
   - Safety stock buffers for high-risk supply lines
   - Geographic diversification of supply base
   - Financial monitoring (credit reports, financial statements)
   - Business continuity plans with key suppliers
   - Contractual protections (force majeure, exit clauses)

### Step 6 — Dual Sourcing Strategy
1. **When to Dual Source**
   - Critical items with high supply risk
   - High-volume items where one supplier cannot meet total demand
   - Categories where competition drives better pricing
   - Items requiring geographic redundancy (different regions/countries)
2. **Allocation Models**
   - 70/30 split (primary gets majority, secondary stays qualified)
   - Dynamic allocation (adjust based on performance scorecards)
   - Product split (different variants to different suppliers)
   - Geographic split (regional suppliers for regional demand)
3. **Dual Sourcing Costs & Trade-offs**
   - Higher procurement management effort (2 relationships vs. 1)
   - Potentially higher unit cost (lower volume per supplier)
   - Qualification and audit costs for second supplier
   - Benefit: Supply security, competitive tension, risk reduction

## Commands

```
/suply-supplier scorecard [supplier]   — Generate or update supplier scorecard
/suply-supplier review [supplier]      — Performance review preparation
/suply-supplier develop [supplier]     — Development program design
/suply-supplier risk [supplier]        — Risk assessment with mitigation plan
/suply-supplier dual-source [item]     — Dual sourcing strategy evaluation
/suply-supplier portfolio              — Full supplier portfolio overview
```

## Output Template

```markdown
# Supplier Relationship Report: [Supplier Name]

## Supplier Profile
- **Tier**: [Strategic / Preferred / Approved / Transactional]
- **Annual Spend**: $[X]
- **Categories Supplied**: [List]
- **Contract Status**: [Active until Date / Month-to-month]
- **Relationship Since**: [Year]

## Performance Scorecard
| Dimension | Weight | Score (1-5) | Weighted | Trend | Notes |
|-----------|--------|-------------|----------|-------|-------|
| Quality | 25% | [X] | [X] | [trend] | [Notes] |
| Delivery | 25% | [X] | [X] | [trend] | [Notes] |
| Cost | 20% | [X] | [X] | [trend] | [Notes] |
| Service | 15% | [X] | [X] | [trend] | [Notes] |
| Innovation | 15% | [X] | [X] | [trend] | [Notes] |
| **Total** | **100%** | | **[X.X]** | [trend] | |

## Risk Assessment
| Risk Category | Likelihood | Impact | Score | Mitigation |
|--------------|------------|--------|-------|-----------|
| Financial | [1-5] | [1-5] | [X] | [Action] |
| Operational | [1-5] | [1-5] | [X] | [Action] |
| Geographic | [1-5] | [1-5] | [X] | [Action] |
| Concentration | [1-5] | [1-5] | [X] | [Action] |

## Action Plan
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| [Action] | [Name] | [Date] | [Status] |

## Recommendation
- **Tier Adjustment**: [Maintain / Upgrade / Downgrade / Exit]
- **Rationale**: [Summary]
```

## Red Flags

- Strategic supplier with no scorecard or formal performance review in >12 months
- Single-source supplier for critical items with no risk mitigation plan
- Supplier scorecard consistently below 2.5 with no development plan or exit plan
- Supplier financial distress signals (late payments to their suppliers, credit rating downgrade)
- No supplier risk assessment performed for top 20 suppliers
- Dual sourcing in place but secondary supplier never tested with real volume
- Supplier performance data not shared with the supplier (no transparency)
- Supplier development program running >12 months with no measurable improvement
- Geographic concentration: >60% of spend in a single country/region for critical categories
- No consequence for poor supplier performance (same treatment regardless of score)
- Supplier exits handled abruptly without transition plan (supply disruption risk)
- Supplier innovation not tracked or incentivized in scorecards

## Integration Points

- Receives from: `suply-quality` (quality data for scorecards), `suply-procurement` (spend data, contract terms), `suply-logistics` (delivery performance)
- Feeds into: `suply-procurement` (supplier selection input), `suply-forecast` (lead time data), `suply-cost` (supplier cost performance)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - SUPLY - Supplier [Name].md`

## Metrics to Track

- **Average Supplier Score**: Across portfolio, by tier, trend over time
- **On-Time Delivery Rate**: Per supplier, target >95%
- **Quality PPM**: Per supplier, target varies by category
- **Single Source %**: % of critical items with only one supplier, target <20%
- **Supplier Turnover**: % of suppliers exited or replaced per year
- **Development ROI**: Performance improvement vs. investment in development programs
