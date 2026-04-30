---
name: suply-procurement
description: "S.U.P.L.Y. Strategic Sourcing — supplier evaluation, TCO analysis, make vs buy decisions, RFP management, and contract negotiation"
version: "1.0"
agent: SUPLY
tags: [procurement, sourcing, TCO, RFP, supplier-evaluation, make-vs-buy, negotiation]
---

# SUPLY Strategic Sourcing & Procurement Skill

## Triggers

Activate this skill when the user says or implies:
- "procurement", "sourcing", "strategic sourcing"
- "supplier evaluation", "vendor selection", "supplier scorecard"
- "TCO", "total cost of ownership", "landed cost"
- "make vs buy", "outsource decision", "insource"
- "RFP", "RFQ", "request for proposal", "request for quotation"
- "contract negotiation", "supplier contract", "purchase agreement"

## Workflow

### Step 1 — Category Analysis & Spend Assessment
1. **Spend Analysis**
   - Total spend by category, supplier, business unit
   - Pareto analysis: top 20% suppliers = 80% spend
   - Maverick spend detection (off-contract purchases)
   - Spend trend over 12-24 months
2. **Category Segmentation (Kraljic Matrix)**
   - **Strategic** (high profit impact, high supply risk): partnerships, long-term contracts
   - **Leverage** (high profit impact, low supply risk): competitive bidding, volume consolidation
   - **Bottleneck** (low profit impact, high supply risk): secure supply, develop alternatives
   - **Non-Critical** (low profit impact, low supply risk): simplify, automate, reduce effort
3. **Market Intelligence**
   - Supplier landscape (number of viable suppliers, market concentration)
   - Price trends and commodity indices
   - Technology and innovation trends in the category
   - Regulatory requirements affecting sourcing

### Step 2 — Supplier Evaluation & Selection
1. **Evaluation Criteria (weighted scorecard)**
   - Quality (25%): defect rates, certifications, QMS maturity
   - Cost (25%): unit price, TCO, payment terms, cost breakdown
   - Delivery (20%): lead time, on-time delivery rate, flexibility
   - Service (15%): responsiveness, technical support, communication
   - Risk (15%): financial stability, geographic risk, concentration risk, ESG compliance
2. **Evaluation Process**
   - Desktop research and pre-qualification
   - RFI (Request for Information) for longlist screening
   - RFP/RFQ for shortlisted suppliers
   - Supplier site visits / audits (for strategic categories)
   - Reference checks with existing customers
   - Pilot order or trial period before full commitment
3. **Scoring & Selection**
   - Quantitative scoring on each criterion (1-5 scale)
   - Weighted total score
   - Shortlist top 2-3 for negotiation
   - Document selection rationale for audit trail

### Step 3 — Total Cost of Ownership (TCO) Analysis
1. **Acquisition Costs**: Unit price, MOQ premiums, tooling, setup fees
2. **Logistics Costs**: Freight, customs, duties, insurance, warehousing
3. **Quality Costs**: Inspection, testing, rework, returns, warranty claims
4. **Operating Costs**: Integration, training, IT systems, change management
5. **Risk Costs**: Buffer inventory, dual sourcing premium, insurance
6. **End-of-Life Costs**: Disposal, decommissioning, contract exit fees
7. **Opportunity Costs**: Innovation foregone, flexibility lost, tied-up capital

### Step 4 — Make vs Buy Decision Framework
1. **Strategic Factors**
   - Core competency alignment (keep core, outsource non-core)
   - IP protection requirements
   - Control over quality and delivery
   - Strategic flexibility and optionality
2. **Financial Factors**
   - Full cost comparison (internal fully-loaded cost vs. external TCO)
   - Capital investment required for in-house
   - Volume sensitivity (break-even volume for each option)
   - Cash flow impact
3. **Operational Factors**
   - Capacity availability (internal vs. external)
   - Technical capability and expertise
   - Scalability requirements
   - Lead time comparison
4. **Risk Factors**
   - Supply continuity risk
   - Quality control risk
   - Dependency and lock-in risk
   - Regulatory and compliance risk

### Step 5 — RFP/RFQ Management
1. **RFP Structure**
   - Company overview and project background
   - Scope of work / specifications (detailed and unambiguous)
   - Evaluation criteria and weighting (transparent)
   - Commercial requirements (pricing format, payment terms)
   - Timeline (submission deadline, evaluation period, decision date)
   - Terms and conditions (contract template, NDA)
   - Required certifications and compliance
2. **Process Timeline**
   - Day 1-3: Issue RFP to qualified suppliers
   - Day 3-5: Supplier Q&A period
   - Day 5-7: Publish answers to all participants
   - Day 7-21: Supplier response preparation
   - Day 21: Submission deadline
   - Day 21-28: Evaluation and scoring
   - Day 28-35: Shortlist presentations / demos
   - Day 35-42: Negotiation with finalists
   - Day 42-49: Award decision and notification

### Step 6 — Contract Negotiation
1. **Preparation**
   - Define BATNA (Best Alternative to Negotiated Agreement)
   - Set target price, walk-away price, and opening position
   - Identify tradeable variables (price, volume, terms, service, exclusivity)
   - Research supplier's position and constraints
2. **Key Contract Clauses**
   - Pricing (fixed, indexed, cost-plus, tiered by volume)
   - Volume commitments and flexibility bands (+/- 20%)
   - Quality standards and acceptance criteria
   - Delivery schedule and penalties for late delivery
   - Payment terms (net-30/60/90, early payment discount)
   - Warranty and liability provisions
   - Termination clause (for cause and for convenience)
   - IP ownership and confidentiality
   - Force majeure and business continuity
   - Continuous improvement and cost reduction targets

## Commands

```
/suply-procurement category [name]     — Category analysis with Kraljic positioning
/suply-procurement evaluate [supplier] — Supplier evaluation scorecard
/suply-procurement tco [scenario]      — Total cost of ownership comparison
/suply-procurement make-buy [item]     — Make vs buy decision framework
/suply-procurement rfp [scope]         — Generate RFP document template
/suply-procurement negotiate [supplier]— Negotiation preparation brief
```

## Output Template

```markdown
# Procurement Analysis: [Category/Item]

## Category Profile
- **Annual Spend**: $[X]
- **Kraljic Position**: [Strategic/Leverage/Bottleneck/Non-Critical]
- **Current Suppliers**: [X] ([names])
- **Contract Status**: [Active until Date / Expiring / No contract]

## Supplier Evaluation Scorecard
| Criterion | Weight | Supplier A | Supplier B | Supplier C |
|-----------|--------|------------|------------|------------|
| Quality | 25% | [X/5] | [X/5] | [X/5] |
| Cost | 25% | [X/5] | [X/5] | [X/5] |
| Delivery | 20% | [X/5] | [X/5] | [X/5] |
| Service | 15% | [X/5] | [X/5] | [X/5] |
| Risk | 15% | [X/5] | [X/5] | [X/5] |
| **Total** | **100%** | **[X.X]** | **[X.X]** | **[X.X]** |

## TCO Comparison
| Cost Element | Option A | Option B | Delta |
|-------------|----------|----------|-------|
| Unit Price | $[X] | $[X] | $[X] |
| Logistics | $[X] | $[X] | $[X] |
| Quality | $[X] | $[X] | $[X] |
| **Total TCO** | **$[X]** | **$[X]** | **$[X]** |

## Recommendation
- **Preferred Supplier**: [Name]
- **Rationale**: [Summary]
- **Contract Terms**: [Key terms]
- **Next Steps**: [Actions with dates]
```

## Red Flags

- Sole source dependency without documented justification or risk mitigation
- Supplier selected on price alone without TCO analysis
- RFP specifications so narrow they pre-select a specific supplier
- No competitive bidding for spend categories >$50K annually
- Contract expired and operating on informal terms (handshake deals)
- Make vs buy decision driven by emotion ("we've always done it ourselves") instead of data
- Supplier evaluation criteria not shared with bidders (non-transparent process)
- Payment terms worse than industry standard without compensating benefit
- No quality clauses or SLA penalties in supplier contracts
- Volume commitments made without demand forecast validation
- Maverick spend (off-contract purchasing) exceeding 20% of category spend
- Contract signed without legal review for agreements >$25K

## Integration Points

- Receives from: `suply-forecast` (demand plan for volume commitments), `suply-quality` (supplier quality data), `suply-supplier` (performance history)
- Feeds into: `suply-inventory` (lead times and MOQs), `suply-cost` (purchase cost data), `suply-logistics` (inbound logistics planning)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - SUPLY - Procurement [Category].md`

## Metrics to Track

- **Cost Savings**: Actual vs. budgeted spend, negotiated savings
- **Supplier On-Time Delivery**: Target >95%
- **Supplier Quality (PPM)**: Defective parts per million, target <500
- **Maverick Spend %**: Off-contract spending, target <10%
- **RFP Cycle Time**: Days from issue to award
- **Contract Coverage**: % of spend under formal contracts, target >80%
