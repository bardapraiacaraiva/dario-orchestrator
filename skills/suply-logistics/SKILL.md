---
name: suply-logistics
description: "S.U.P.L.Y. Logistics & Distribution — route optimization, 3PL management, last mile delivery, shipping costs, and carrier selection"
version: "1.0"
agent: SUPLY
tags: [logistics, distribution, routing, 3PL, last-mile, shipping, carrier-selection]
---

# SUPLY Logistics & Distribution Skill

## Triggers

Activate this skill when the user says or implies:
- "logistics", "distribution", "shipping"
- "route optimization", "delivery routes", "fleet routing"
- "3PL", "third-party logistics", "outsource logistics"
- "last mile", "last-mile delivery", "final delivery"
- "shipping costs", "freight costs", "transport costs"
- "carrier selection", "freight forwarder", "courier"

## Workflow

### Step 1 — Distribution Network Design
1. **Network Analysis**
   - Number and location of distribution centers (DCs)
   - Customer geography and density mapping
   - Demand volume by region and seasonality
   - Current transit times and delivery performance
2. **Network Optimization**
   - Center-of-gravity analysis for DC location
   - Hub-and-spoke vs. direct-ship model comparison
   - Multi-echelon inventory positioning
   - Capacity vs. demand alignment by node
3. **Service Level Definition**
   - Delivery speed tiers (same-day, next-day, 2-3 day, standard)
   - Geographic coverage requirements
   - Cut-off times for order processing
   - Returns and reverse logistics flow

### Step 2 — Carrier Selection & Management
1. **Carrier Evaluation Criteria**
   - Price per unit shipped (per kg, per pallet, per parcel)
   - Transit time and reliability (on-time delivery rate)
   - Geographic coverage and service areas
   - Technology integration (tracking, EDI, API)
   - Claims handling and insurance coverage
   - Capacity and scalability (peak season flexibility)
   - Environmental credentials (carbon footprint, EVs)
2. **Carrier Mix Strategy**
   - Primary carrier(s) for core volume (70-80% of shipments)
   - Secondary carrier(s) for overflow and specialized needs
   - Spot market for peak surges
   - Multi-modal options (road, rail, sea, air) by lane
3. **Rate Negotiation**
   - Annual volume commitments for rate locks
   - Fuel surcharge mechanisms and caps
   - Accessorial charges review (residential, liftgate, inside delivery)
   - Benchmark against market rates regularly

### Step 3 — Route Optimization
1. **Static Routing**
   - Fixed delivery routes by day of week and zone
   - Suitable for predictable, recurring deliveries
   - Optimize for: distance, time, vehicle capacity, delivery windows
2. **Dynamic Routing**
   - Real-time optimization based on daily orders
   - Vehicle Routing Problem (VRP) algorithms
   - Constraints: time windows, vehicle capacity, driver hours, road restrictions
   - Re-optimization for same-day changes (cancellations, add-ons)
3. **Optimization Levers**
   - Consolidation (combine small shipments into full loads)
   - Backhauling (return trips carry freight instead of empty)
   - Milk-run routes (multiple pickups/deliveries on one route)
   - Cross-docking (bypass storage, direct transfer between inbound and outbound)

### Step 4 — 3PL Management
1. **3PL Selection**
   - Scope of services needed (transport, warehousing, fulfillment, returns)
   - Industry specialization and references
   - Technology platform and visibility tools
   - Geographic alignment with your distribution needs
   - Pricing model (cost-plus, gain-sharing, fixed fee, transaction-based)
2. **3PL Contract Structure**
   - SLA definitions (delivery time, accuracy, damage rate)
   - KPI reporting frequency and format
   - Penalty/bonus structure for performance
   - Volume commitments and flexibility bands
   - Data ownership and system integration requirements
   - Transition/exit plan and data portability
3. **3PL Performance Management**
   - Monthly scorecards with KPIs
   - Quarterly business reviews
   - Annual strategic review and rate renegotiation
   - Continuous improvement initiatives (joint projects)

### Step 5 — Last Mile Delivery
1. **Last Mile Models**
   - Own fleet (control, branding, but capital intensive)
   - Gig economy / crowdsourced delivery (flexible, lower fixed cost)
   - 3PL / courier partners (specialized, scalable)
   - Click-and-collect / PUDO (Pick-Up Drop-Off) points
   - Locker networks (parcel lockers, automated pickup)
2. **Last Mile Optimization**
   - Delivery density clustering (group orders by proximity)
   - Time-slot management (customer-chosen windows)
   - Proof of delivery (photo, signature, geolocation)
   - Failed delivery management (re-attempt, redirect, hold)
   - Communication: real-time tracking and ETA updates
3. **Last Mile Cost Control**
   - Average cost per delivery by zone and order size
   - Minimum order thresholds for free delivery
   - Delivery fee structures (flat, tiered, dynamic)
   - Returns rate impact on last mile economics

### Step 6 — Shipping Cost Analysis & Reduction
1. **Cost Decomposition**
   - Base freight rate (per unit, per weight, per distance)
   - Fuel surcharges (% of base rate)
   - Accessorials (residential, appointment, special handling)
   - Insurance and declared value charges
   - Customs, duties, and tariffs (international)
2. **Cost Reduction Strategies**
   - Consolidation (fewer, fuller shipments)
   - Mode shifting (air to sea, express to ground where possible)
   - Packaging optimization (DIM weight reduction)
   - Zone skipping (bypass carrier sort facilities)
   - Pre-negotiated rates with volume commitments
   - Audit invoices (billing errors are common, 1-5% of freight spend)

## Commands

```
/suply-logistics network               — Distribution network analysis and optimization
/suply-logistics carrier [lane]        — Carrier selection and comparison
/suply-logistics route [zone]          — Route optimization analysis
/suply-logistics 3pl [scope]           — 3PL evaluation framework
/suply-logistics last-mile             — Last mile strategy and cost analysis
/suply-logistics cost [period]         — Shipping cost breakdown and reduction plan
```

## Output Template

```markdown
# Logistics Analysis: [Scope/Region]

## Distribution Network
- **DCs**: [X] locations: [List]
- **Coverage**: [X]% of customers within [X]-day delivery
- **Model**: [Hub-and-spoke / Direct / Hybrid]

## Carrier Scorecard
| Carrier | Rate/unit | On-Time % | Coverage | Tech | Overall |
|---------|----------|-----------|----------|------|---------|
| [Carrier A] | $[X] | [X]% | [X regions] | [Y/N] | [X/5] |
| [Carrier B] | $[X] | [X]% | [X regions] | [Y/N] | [X/5] |

## Shipping Cost Breakdown
| Cost Element | Monthly | % of Total | Trend | Reduction Opportunity |
|-------------|---------|------------|-------|----------------------|
| Base Freight | $[X] | [X]% | [trend] | [Opportunity] |
| Fuel Surcharge | $[X] | [X]% | [trend] | [Opportunity] |
| Accessorials | $[X] | [X]% | [trend] | [Opportunity] |
| **Total** | **$[X]** | **100%** | | Est. savings: $[X] |

## Last Mile Performance
| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Cost per delivery | $[X] | $[X] | $[X] |
| On-time delivery | [X]% | [X]% | [X]% |
| First attempt success | [X]% | [X]% | [X]% |
| Customer satisfaction | [X/5] | [X/5] | [X] |

## Recommendations
1. [Recommendation with estimated impact]
2. [Recommendation with estimated impact]
```

## Red Flags

- Single carrier dependency for >80% of shipments with no backup plan
- Shipping costs increasing faster than revenue growth
- On-time delivery rate below 90% without corrective action plan
- No freight invoice auditing (billing errors going undetected)
- 3PL contract without SLA penalties for underperformance
- Last mile cost per delivery exceeding product margin for low-value orders
- No real-time shipment tracking provided to customers
- Distribution network not reviewed in >3 years despite business changes
- Route optimization done manually instead of using algorithmic tools
- Failed first delivery attempt rate above 15% with no root cause analysis
- Carrier rates not benchmarked against market for >12 months
- No contingency plan for carrier disruptions (strikes, capacity crunch, weather)

## Integration Points

- Receives from: `suply-forecast` (volume for capacity planning), `suply-inventory` (shipment requirements), `suply-warehouse` (outbound scheduling)
- Feeds into: `suply-cost` (transportation cost data), `suply-supplier` (inbound logistics coordination), `suply-quality` (in-transit damage tracking)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - SUPLY - Logistics [Region].md`

## Metrics to Track

- **On-Time In-Full (OTIF)**: Target >95%
- **Cost per Unit Shipped**: By mode, carrier, and lane
- **Freight Cost as % of Revenue**: Benchmark against industry
- **Average Transit Time**: By lane, trend over time
- **First Attempt Delivery Rate**: Target >85%
- **Carrier Utilization**: % of contracted capacity used
