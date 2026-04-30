---
name: suply-cost
description: "S.U.P.L.Y. Supply Chain Cost Optimization — total cost of ownership, value engineering, process improvement, waste elimination, and landed cost analysis"
version: "1.0"
agent: SUPLY
tags: [cost-optimization, TCO, value-engineering, waste-elimination, landed-cost, lean, process-improvement]
---

# SUPLY Supply Chain Cost Optimization Skill

## Triggers

Activate this skill when the user says or implies:
- "supply chain cost", "reduce costs", "cost optimization"
- "total cost of ownership", "TCO", "true cost"
- "value engineering", "VA/VE", "cost without cutting quality"
- "process improvement", "efficiency", "lean supply chain"
- "waste elimination", "muda", "lean principles"
- "landed cost", "full cost", "cost breakdown"

## Workflow

### Step 1 — Supply Chain Cost Mapping
1. **Cost Categories**
   - **Procurement**: Raw materials, components, MRO, services (40-70% of total)
   - **Manufacturing/Production**: Direct labor, overhead, equipment, utilities (15-30%)
   - **Logistics**: Transportation, warehousing, distribution (8-15%)
   - **Inventory**: Carrying cost, obsolescence, shrinkage (3-8%)
   - **Quality**: Prevention, appraisal, internal/external failure (2-5%)
   - **Administration**: Planning, IT systems, compliance, management (3-8%)
2. **Cost Visibility Framework**
   - Map costs end-to-end from supplier to customer
   - Identify hidden costs (expediting, rework, returns processing)
   - Allocate overhead to activities (Activity-Based Costing)
   - Benchmark against industry peers and best-in-class
3. **Pareto of Cost Drivers**
   - Identify top 20% of cost elements driving 80% of total supply chain cost
   - Prioritize optimization efforts on biggest cost pools first
   - Decompose each major cost element into controllable sub-drivers

### Step 2 — Landed Cost Analysis
1. **Landed Cost Components**
   - Ex-works price (unit cost at supplier's facility)
   - Packaging and crating
   - Inland freight (supplier to port/hub)
   - International freight (ocean, air, rail)
   - Insurance
   - Customs duties and tariffs (HS code classification)
   - Import fees, brokerage, documentation
   - Port handling and terminal charges
   - Inland freight (port to warehouse)
   - Receiving, inspection, put-away costs
2. **Landed Cost Comparison Template**
   - Compare same product from different supplier locations
   - Factor in lead time differences (inventory carrying cost)
   - Include quality risk costs (higher inspection, reject rates)
   - Calculate total landed cost per unit, not just purchase price
3. **Incoterms Impact**
   - EXW, FOB, CIF, DDP — each shifts cost and risk differently
   - Choose Incoterms that give best total cost, not just lowest price
   - Ensure insurance coverage matches Incoterm responsibility

### Step 3 — Value Engineering (VA/VE)
1. **Function Analysis**
   - Define the function of each component/feature (verb + noun: "supports load")
   - Classify functions: basic (essential) vs. secondary (nice-to-have)
   - Calculate function cost ratio: cost to deliver each function
   - Target: reduce cost of secondary functions, maintain basic function quality
2. **Value Engineering Techniques**
   - Material substitution (same function, lower cost material)
   - Design simplification (fewer parts, easier assembly)
   - Standardization (reduce part variety, increase volume leverage)
   - Specification optimization (are tolerances tighter than needed?)
   - Packaging optimization (reduce material, improve protection-to-cost ratio)
3. **VA/VE Workshop Process**
   - Cross-functional team: engineering, procurement, quality, supplier
   - Map current design cost breakdown
   - Brainstorm alternatives for each function
   - Evaluate: cost reduction vs. risk vs. implementation effort
   - Prototype and validate before full implementation
   - Track savings realization over 12 months

### Step 4 — Process Improvement (Lean Supply Chain)
1. **Value Stream Mapping (VSM)**
   - Map current state: all steps from order to delivery
   - Identify value-adding vs. non-value-adding activities
   - Calculate process efficiency: value-add time / total lead time
   - Design future state: eliminate or reduce NVA steps
   - Implementation roadmap with quick wins and strategic improvements
2. **Seven Wastes (Muda) in Supply Chain**
   - **Overproduction**: Making more than needed, producing too early
   - **Waiting**: Idle time between process steps, approval delays
   - **Transportation**: Unnecessary movement of goods between locations
   - **Overprocessing**: Doing more than the customer requires
   - **Inventory**: Excess stock tying up capital and space
   - **Motion**: Unnecessary movement of people (poor layout)
   - **Defects**: Rework, returns, scrap from quality failures
3. **Quick Win Opportunities**
   - Eliminate expediting (plan better, reduce need for express shipping)
   - Consolidate suppliers (fewer vendors, higher volume, better prices)
   - Automate manual processes (PO creation, invoice matching, reporting)
   - Reduce touchpoints (each handling = cost + error risk)
   - Optimize lot sizes (balance ordering cost vs. carrying cost)

### Step 5 — Strategic Cost Reduction Initiatives
1. **Demand Management**
   - Specification rationalization (do we need this variant?)
   - Consumption reduction (use less of the same material)
   - Demand aggregation (pool volume across business units)
2. **Supply Market Leverage**
   - Competitive bidding and market testing
   - Long-term agreements with volume commitments
   - Consortia / group purchasing organizations
   - Global sourcing (lower-cost country sourcing with TCO validation)
3. **Structural Cost Reduction**
   - Network optimization (number and location of warehouses, plants)
   - Make vs. buy reassessment (in-source or outsource based on total cost)
   - Technology investment (automation, digitization ROI analysis)
   - Vertical integration (acquire or develop supplier capability)
4. **Collaborative Cost Reduction**
   - Open-book costing with strategic suppliers
   - Joint cost reduction targets (shared savings model)
   - Supplier suggestion programs (incentivize ideas)
   - Design-to-cost with engineering and procurement collaboration

### Step 6 — Cost Tracking & Governance
1. **Savings Methodology**
   - Define what counts as "savings" (cost avoidance vs. hard savings)
   - Baseline: prior year spend, adjusted for volume/mix changes
   - Actual vs. budget tracking by initiative
   - Finance validation of claimed savings
2. **Cost Dashboard**
   - Total supply chain cost as % of revenue (trend)
   - Savings pipeline: identified, in progress, realized
   - Cost per unit by product line
   - Cost breakdown by category (procurement, logistics, inventory, quality)
3. **Governance**
   - Monthly cost review with functional leads
   - Quarterly executive review of savings targets vs. actual
   - Annual target setting aligned with business plan
   - Initiative portfolio management (prioritize, resource, track)

## Commands

```
/suply-cost map [scope]                — Supply chain cost mapping and Pareto
/suply-cost landed [product]           — Landed cost analysis and comparison
/suply-cost ve [product/component]     — Value engineering workshop guide
/suply-cost lean [process]             — Lean process improvement with VSM
/suply-cost savings [period]           — Savings pipeline and tracking dashboard
/suply-cost benchmark [industry]       — Cost benchmarking against industry peers
```

## Output Template

```markdown
# Supply Chain Cost Analysis: [Scope]

## Cost Overview
- **Total Supply Chain Cost**: $[X] ([X]% of revenue)
- **Period**: [Period]
- **Benchmark**: Industry average [X]% of revenue

## Cost Breakdown
| Category | Amount | % of Total | vs. Last Year | vs. Benchmark |
|----------|--------|------------|---------------|---------------|
| Procurement | $[X] | [X]% | [+/-X]% | [Above/Below] |
| Manufacturing | $[X] | [X]% | [+/-X]% | [Above/Below] |
| Logistics | $[X] | [X]% | [+/-X]% | [Above/Below] |
| Inventory | $[X] | [X]% | [+/-X]% | [Above/Below] |
| Quality | $[X] | [X]% | [+/-X]% | [Above/Below] |
| Admin | $[X] | [X]% | [+/-X]% | [Above/Below] |

## Top Cost Reduction Opportunities
| Initiative | Category | Est. Savings | Effort | Timeline | Priority |
|-----------|----------|-------------|--------|----------|----------|
| [Initiative] | [Cat] | $[X]/yr | [H/M/L] | [Months] | [1-N] |

## Landed Cost Comparison (if applicable)
| Component | Supplier A (Local) | Supplier B (Import) | Delta |
|-----------|-------------------|--------------------:|-------|
| Unit Price | $[X] | $[X] | $[X] |
| Freight | $[X] | $[X] | $[X] |
| Duties | $[X] | $[X] | $[X] |
| Inventory Carry | $[X] | $[X] | $[X] |
| Quality Cost | $[X] | $[X] | $[X] |
| **Landed Cost** | **$[X]** | **$[X]** | **$[X]** |

## Savings Tracker
| Initiative | Target | Identified | In Progress | Realized | Gap |
|-----------|--------|-----------|-------------|----------|-----|
| [Init] | $[X] | $[X] | $[X] | $[X] | $[X] |
| **Total** | **$[X]** | **$[X]** | **$[X]** | **$[X]** | **$[X]** |

## Value Engineering Candidates
| Component | Current Cost | Function | VE Opportunity | Est. Savings |
|-----------|-------------|----------|----------------|-------------|
| [Component] | $[X] | [Function] | [Idea] | $[X] |
```

## Red Flags

- Supply chain cost as % of revenue increasing year-over-year without business justification
- No landed cost analysis performed when sourcing from different geographies
- Supplier selection based on unit price alone, ignoring total cost of ownership
- Value engineering never conducted on top-spend products/components
- Cost savings claimed but not validated by finance (inflated numbers)
- No cost benchmarking against industry peers (blind to competitiveness)
- Process waste identified but no improvement actions assigned or tracked
- Expediting costs exceeding 3% of freight budget (symptom of planning failures)
- Inventory carrying cost not calculated or not included in decision-making
- Cost reduction targets set without bottom-up initiative identification
- Savings pipeline empty with 6+ months remaining in fiscal year
- Cost cutting that degrades quality or service levels (false savings)

## Integration Points

- Receives from: `suply-procurement` (purchase costs), `suply-logistics` (freight costs), `suply-inventory` (carrying costs), `suply-quality` (cost of quality), `suply-warehouse` (operational costs)
- Feeds into: `suply-forecast` (financial forecast), `suply-procurement` (TCO for sourcing decisions), `suply-supplier` (cost performance in scorecards)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - SUPLY - Cost Analysis [Scope].md`

## Metrics to Track

- **Total Supply Chain Cost as % of Revenue**: Trend, target reduction
- **Realized Savings**: Actual savings vs. annual target
- **Cost per Unit**: By product line, trend over time
- **Inventory Carrying Cost Rate**: As % of inventory value (target 20-25%)
- **Freight Cost per Unit Shipped**: By mode and lane
- **Cost of Quality**: As % of revenue (target <3%)
