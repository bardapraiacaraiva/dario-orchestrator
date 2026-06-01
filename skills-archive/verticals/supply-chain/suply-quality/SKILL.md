---
name: suply-quality
description: "S.U.P.L.Y. Quality Control — incoming inspection, sampling plans, defect tracking, supplier quality audits, and corrective actions (8D)"
version: "1.0"
agent: SUPLY
tags: [quality-control, inspection, sampling, defect-tracking, supplier-audit, 8D, CAPA]
---

# SUPLY Quality Control Skill

## Triggers

Activate this skill when the user says or implies:
- "quality control", "QC", "quality assurance", "QA"
- "incoming inspection", "goods inspection", "receiving quality"
- "sampling plan", "AQL", "acceptance sampling"
- "defect tracking", "defect rate", "non-conformance"
- "supplier audit", "quality audit", "supplier quality"
- "8D", "corrective action", "CAPA", "root cause"

## Workflow

### Step 1 — Quality Management System (QMS) Framework
1. **Quality Policy & Objectives**
   - Define quality standards aligned with customer requirements
   - Set measurable quality objectives (defect rate targets, customer complaints)
   - Establish quality roles: QC inspector, QA manager, quality engineer
2. **Documentation Hierarchy**
   - Level 1: Quality manual (policy, scope, organization)
   - Level 2: Procedures (how processes are managed)
   - Level 3: Work instructions (step-by-step task guidance)
   - Level 4: Records and forms (evidence of compliance)
3. **Standards & Certifications**
   - ISO 9001 (Quality Management System)
   - Industry-specific: ISO 13485 (medical), IATF 16949 (automotive), AS9100 (aerospace)
   - Customer-specific quality requirements

### Step 2 — Incoming Inspection
1. **Inspection Levels by Supplier Tier**
   - Tier 1 (Certified/Trusted): Skip lot inspection, sample audit only
   - Tier 2 (Approved): Normal sampling inspection per AQL
   - Tier 3 (New/Probationary): Tightened inspection or 100% check
   - Tier adjustment: Move up/down based on track record (switching rules)
2. **Sampling Plans (ISO 2859 / ANSI Z1.4)**
   - **AQL (Acceptable Quality Level)**: Maximum defect rate considered acceptable
   - Common AQL levels: 0.65% (critical), 1.0% (major), 2.5% (minor)
   - Sample size determined by lot size and inspection level
   - Accept/reject decision based on number of defects found in sample
3. **Inspection Checklist**
   - Visual inspection (appearance, labeling, packaging)
   - Dimensional check (measurements vs. specification)
   - Functional test (does it work as intended)
   - Material verification (certificates, test reports)
   - Documentation check (CoC, CoA, MSDS, certifications)

### Step 3 — Defect Classification & Tracking
1. **Defect Severity Classification**
   - **Critical**: Safety hazard or regulatory non-compliance (0% acceptance)
   - **Major**: Product will not function or significantly impaired (AQL 1.0%)
   - **Minor**: Cosmetic or minor deviation, product still functional (AQL 2.5%)
2. **Defect Tracking System**
   - Unique NCR (Non-Conformance Report) number for each incident
   - Fields: date, supplier, product, defect description, severity, quantity affected
   - Photos and measurement data attached
   - Disposition decision: accept, reject, rework, return, scrap
   - Trend analysis: defects by supplier, product, defect type, period
3. **Defect Metrics**
   - PPM (Parts Per Million defective): target varies by industry
   - Defect Rate (%): defective units / total inspected
   - Cost of Quality (CoQ): prevention + appraisal + internal failure + external failure
   - First Pass Yield (FPY): % of units passing inspection first time

### Step 4 — Supplier Quality Audits
1. **Audit Types**
   - **Pre-qualification audit**: Before approving a new supplier
   - **Periodic audit**: Annual for strategic suppliers, biennial for others
   - **For-cause audit**: Triggered by quality incidents or performance decline
   - **Product audit**: Focused on specific product line quality
2. **Audit Scope (Process Audit)**
   - Management commitment and quality culture
   - Incoming material control
   - Production process controls
   - Measurement and testing equipment (calibration)
   - Traceability and documentation
   - Non-conformance management
   - Packaging, storage, and shipping
   - Continuous improvement activities
3. **Audit Scoring**
   - Score each element: 0 (non-existent) to 4 (best practice)
   - Overall score: A (>85%), B (70-85%), C (50-70%), D (<50%)
   - Corrective actions required for scores below threshold
   - Follow-up audit within 90 days for C/D ratings

### Step 5 — Corrective & Preventive Action (8D Process)
1. **D1 — Team Formation**: Assemble cross-functional team with knowledge of the issue
2. **D2 — Problem Description**: Define the problem precisely (5W2H: Who, What, When, Where, Why, How, How Many)
3. **D3 — Containment Actions**: Immediate actions to stop the problem from reaching the customer
4. **D4 — Root Cause Analysis**: Identify root cause(s) using:
   - 5 Whys (keep asking why until root is found)
   - Fishbone / Ishikawa diagram (6M: Man, Machine, Method, Material, Measurement, Mother Nature)
   - Fault Tree Analysis (FTA)
   - Pareto analysis (focus on vital few causes)
5. **D5 — Corrective Actions**: Define permanent solutions that eliminate the root cause
6. **D6 — Implementation**: Execute corrective actions with owners and deadlines
7. **D7 — Preventive Actions**: Modify systems/processes to prevent recurrence elsewhere
8. **D8 — Closure & Recognition**: Verify effectiveness, close the 8D, recognize the team

### Step 6 — Quality Reporting & Review
1. **Monthly Quality Report**
   - Incoming inspection results (accept/reject rate by supplier)
   - Defect trends (PPM, defect rate, top defect types)
   - Open NCRs and 8D status
   - Cost of quality breakdown
   - Supplier quality scorecard summary
2. **Management Review**
   - Quarterly quality review with management
   - KPI trends and target achievement
   - Customer complaints and returns analysis
   - Audit findings and corrective action status
   - Continuous improvement project updates

## Commands

```
/suply-quality inspection [product]    — Incoming inspection plan with sampling
/suply-quality defect [ncr_id]         — Defect report and tracking
/suply-quality audit [supplier]        — Supplier quality audit checklist
/suply-quality 8d [problem]            — 8D corrective action report
/suply-quality dashboard [period]      — Quality KPI dashboard
/suply-quality coq                     — Cost of quality analysis
```

## Output Template

```markdown
# Quality Report: [Scope/Period]

## Incoming Inspection Summary
| Supplier | Lots Inspected | Lots Accepted | Reject Rate | PPM | Tier |
|----------|---------------|---------------|-------------|-----|------|
| [Supplier] | [X] | [X] | [X]% | [X] | [1/2/3] |

## Defect Analysis
| Defect Type | Severity | Count | % of Total | Top Supplier | Trend |
|-------------|----------|-------|------------|-------------|-------|
| [Type] | [Crit/Maj/Min] | [X] | [X]% | [Supplier] | [trend] |

## Open NCRs
| NCR # | Date | Supplier | Product | Severity | Status | Days Open |
|-------|------|----------|---------|----------|--------|-----------|
| [NCR] | [Date] | [Supplier] | [Product] | [Sev] | [Status] | [X] |

## 8D Summary (Active)
| 8D # | Problem | Current Step | Root Cause | Due Date | Owner |
|------|---------|-------------|------------|----------|-------|
| [8D] | [Problem] | [D1-D8] | [Cause] | [Date] | [Name] |

## Cost of Quality
| Category | Amount | % of Revenue | Target |
|----------|--------|-------------|--------|
| Prevention | $[X] | [X]% | [X]% |
| Appraisal | $[X] | [X]% | [X]% |
| Internal Failure | $[X] | [X]% | [X]% |
| External Failure | $[X] | [X]% | [X]% |
| **Total CoQ** | **$[X]** | **[X]%** | **<[X]%** |
```

## Red Flags

- No incoming inspection process (goods go directly to stock without verification)
- AQL levels not defined or not aligned with product criticality
- Defect data not tracked systematically (no NCR process)
- 8D corrective actions open for >90 days without progress
- Supplier audits not conducted for strategic suppliers in >2 years
- Cost of quality not measured (hidden costs of poor quality unknown)
- Repeat defects from the same supplier without escalation or consequences
- Critical defect found in the field that should have been caught at inspection
- No calibration program for measurement and testing equipment
- Quality inspectors not trained or certified for the inspection tasks
- Root cause analysis stops at symptoms instead of reaching true root cause
- Customer complaint rate increasing with no quality improvement initiative

## Integration Points

- Receives from: `suply-procurement` (supplier requirements, specs), `suply-warehouse` (receiving process), `suply-supplier` (supplier performance data)
- Feeds into: `suply-supplier` (quality scores for scorecards), `suply-procurement` (supplier tier adjustments), `suply-cost` (cost of quality data)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - SUPLY - Quality [Scope].md`

## Metrics to Track

- **Incoming Reject Rate**: % of lots rejected, by supplier
- **PPM (Parts Per Million)**: Defective parts per million received
- **First Pass Yield**: % passing inspection on first attempt
- **Cost of Quality**: Total CoQ as % of revenue, target <3-5%
- **8D Closure Rate**: % of 8Ds closed within 60 days
- **Supplier Audit Score**: Average audit score across supplier base


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **suply-quality** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in suply-quality:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->
