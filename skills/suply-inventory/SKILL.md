---
name: suply-inventory
description: "S.U.P.L.Y. Inventory Optimization — ABC/XYZ analysis, reorder points, EOQ, dead stock management, inventory turns, and JIT principles"
version: "1.0"
agent: SUPLY
tags: [inventory, ABC-analysis, reorder-point, EOQ, dead-stock, JIT, inventory-turns]
---

# SUPLY Inventory Optimization Skill

## Triggers

Activate this skill when the user says or implies:
- "inventory", "stock levels", "inventory management"
- "ABC analysis", "XYZ analysis", "inventory classification"
- "reorder point", "ROP", "when to order"
- "EOQ", "economic order quantity", "how much to order"
- "dead stock", "obsolete inventory", "slow movers"
- "inventory turns", "turnover ratio", "JIT", "just in time"

## Workflow

### Step 1 — Inventory Classification (ABC/XYZ Matrix)
1. **ABC Analysis (by value)**
   - A items: Top 20% of SKUs = ~80% of annual consumption value
   - B items: Next 30% of SKUs = ~15% of value
   - C items: Bottom 50% of SKUs = ~5% of value
   - Classify each SKU and assign management policy
2. **XYZ Analysis (by demand variability)**
   - X items: Low variability (CoV < 0.5) — predictable, easy to forecast
   - Y items: Medium variability (CoV 0.5-1.0) — some fluctuation
   - Z items: High variability (CoV > 1.0) — erratic, hard to forecast
3. **Combined ABC-XYZ Matrix**
   - AX: High value, predictable → JIT, lean inventory, tight control
   - AY: High value, variable → moderate buffer, frequent review
   - AZ: High value, erratic → strategic buffer, demand sensing
   - BX/BY: Standard inventory policies, periodic review
   - CX/CY/CZ: Simplified management, larger buffers, less frequent review
   - Special attention to AZ and BZ (high risk of stockout or excess)

### Step 2 — Reorder Point (ROP) Calculation
1. **Basic Formula**: ROP = (Average Daily Demand x Lead Time) + Safety Stock
2. **With Variability**:
   - ROP = (d x LT) + Z x sqrt(LT x sigma_d^2 + d^2 x sigma_LT^2)
   - d = average daily demand
   - LT = average lead time in days
   - sigma_d = standard deviation of daily demand
   - sigma_LT = standard deviation of lead time
   - Z = service level factor (1.65 for 95%, 2.33 for 99%)
3. **Review Policies**
   - Continuous review (s, Q): Order Q units when stock hits s
   - Periodic review (R, S): Review every R periods, order up to S
   - (s, S) policy: Review periodically, order to S when stock < s

### Step 3 — Economic Order Quantity (EOQ)
1. **Classic EOQ Formula**: Q* = sqrt(2DS / H)
   - D = annual demand (units)
   - S = ordering cost per order ($)
   - H = holding cost per unit per year ($)
2. **EOQ Variants**
   - Production EOQ (EPQ): For gradual replenishment during production
   - Quantity discount EOQ: Adjusted for volume-based pricing tiers
   - Backorder EOQ: When planned backorders are acceptable
3. **Sensitivity Analysis**
   - EOQ is robust: 20% error in inputs causes only ~2% cost increase
   - Round to practical lot sizes (pallet, carton, MOQ)
   - Adjust for storage constraints and shelf life

### Step 4 — Dead Stock & Excess Inventory Management
1. **Identification Criteria**
   - No sales in last 6 months = slow-moving
   - No sales in last 12 months = dead stock
   - Stock > 12 months of future demand = excess
   - Expiration date approaching (perishables, dated products)
2. **Disposition Options**
   - Markdown and clearance sale (recover partial value)
   - Bundle with active products
   - Return to supplier (if agreement allows)
   - Donate (tax benefit in some jurisdictions)
   - Scrap/dispose (last resort, write off cost)
3. **Prevention Strategies**
   - Minimum order quantities aligned with demand forecast
   - New product introduction (NPI) risk controls
   - Phase-out planning for end-of-life products
   - Regular dead stock reviews (monthly for A items, quarterly for B/C)

### Step 5 — Inventory Turns & Working Capital
1. **Inventory Turns**: COGS / Average Inventory Value
   - Industry benchmarks vary widely (retail 8-12x, manufacturing 4-8x, distribution 6-10x)
   - Higher turns = better capital efficiency (but risk of stockouts if too aggressive)
2. **Days of Inventory (DOI)**: 365 / Inventory Turns
   - Target by ABC class: A items 15-30 days, B items 30-60 days, C items 60-120 days
3. **Working Capital Impact**
   - Inventory investment = Average Inventory x Unit Cost
   - Carrying cost = Inventory Investment x Carrying Cost Rate (typically 20-30% annually)
   - Cash-to-cash cycle: DIO + DSO - DPO

### Step 6 — JIT & Lean Inventory Principles
1. **Core Principles**
   - Pull-based replenishment (demand-driven, not forecast-pushed)
   - Small batch sizes, frequent deliveries
   - Kanban signaling for replenishment triggers
   - Supplier proximity and reliability requirements
   - Continuous flow and waste elimination
2. **Prerequisites for JIT**
   - Reliable suppliers with short, consistent lead times
   - High forecast accuracy or demand visibility
   - Flexible production/receiving capacity
   - Strong quality control (defects disrupt flow)
3. **Risks of JIT**
   - Vulnerable to supply disruptions (single source, long distance)
   - Requires investment in supplier relationships
   - Not suitable for all categories (better for AX items)

## Commands

```
/suply-inventory abc [data]            — ABC/XYZ classification with policies
/suply-inventory rop [sku]             — Reorder point calculation
/suply-inventory eoq [sku]             — Economic order quantity with sensitivity
/suply-inventory dead-stock            — Dead stock report with disposition plan
/suply-inventory turns [period]        — Inventory turns analysis by category
/suply-inventory optimize              — Full inventory optimization review
```

## Output Template

```markdown
# Inventory Optimization: [Warehouse/Category]

## ABC-XYZ Classification Summary
| Class | SKU Count | % of SKUs | Value Share | Policy |
|-------|-----------|-----------|-------------|--------|
| AX | [X] | [X]% | [X]% | JIT, continuous review |
| AY | [X] | [X]% | [X]% | Moderate buffer, weekly review |
| AZ | [X] | [X]% | [X]% | Strategic buffer, demand sensing |
| BX-BZ | [X] | [X]% | [X]% | Periodic review, standard EOQ |
| CX-CZ | [X] | [X]% | [X]% | Simplified, larger lots |

## Reorder Points (Top SKUs)
| SKU | Avg Demand/day | Lead Time | Safety Stock | ROP | Service Level |
|-----|---------------|-----------|-------------|-----|---------------|
| [SKU] | [X] | [X days] | [X units] | [X units] | [X]% |

## EOQ Analysis
| SKU | Annual Demand | Order Cost | Holding Cost | EOQ | Orders/Year |
|-----|-------------|------------|-------------|-----|-------------|
| [SKU] | [X] | $[X] | $[X] | [X units] | [X] |

## Dead Stock Report
| SKU | Last Sale | Qty on Hand | Value | Disposition |
|-----|-----------|-------------|-------|------------|
| [SKU] | [Date] | [X] | $[X] | [Action] |

## Inventory Health KPIs
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Inventory Turns | [X] | [X] | [On/Off track] |
| Days of Inventory | [X] | [X] | [On/Off track] |
| Dead Stock % | [X]% | <[X]% | [On/Off track] |
| Fill Rate | [X]% | >[X]% | [On/Off track] |
| Carrying Cost | $[X] | <$[X] | [On/Off track] |
```

## Red Flags

- No ABC classification performed — all SKUs managed with the same policy
- Reorder points not adjusted for seasonal demand changes
- EOQ calculated but never updated after cost or demand changes
- Dead stock exceeding 10% of total inventory value with no disposition plan
- Inventory turns declining for 3+ consecutive quarters
- Safety stock set arbitrarily ("we always keep 2 months") instead of calculated
- Stockout rate above 5% for A items
- Excess inventory growing while sales are flat or declining
- No cycle count program (relying only on annual physical count)
- JIT attempted without reliable suppliers or quality controls
- Inventory data accuracy below 95% (system vs. physical count discrepancy)
- Carrying cost not calculated or not included in sourcing decisions

## Integration Points

- Receives from: `suply-forecast` (demand plan), `suply-procurement` (lead times, MOQs), `suply-warehouse` (storage capacity)
- Feeds into: `suply-logistics` (shipment planning), `suply-cost` (carrying cost optimization), `suply-procurement` (purchase orders)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - SUPLY - Inventory [Category].md`

## Metrics to Track

- **Inventory Turns**: By ABC class, trend over time
- **Fill Rate / Service Level**: % of demand fulfilled from stock
- **Dead Stock %**: Value of dead stock / total inventory value
- **Inventory Accuracy**: System count vs. physical count match rate
- **Carrying Cost**: Total cost of holding inventory (% of inventory value)
- **Days of Inventory (DOI)**: By category and overall
