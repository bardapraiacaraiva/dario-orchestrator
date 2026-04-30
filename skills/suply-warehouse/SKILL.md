---
name: suply-warehouse
description: "S.U.P.L.Y. Warehouse Management — layout design, pick/pack/ship, receiving, WMS configuration, and KPIs (pick accuracy, cycle time)"
version: "1.0"
agent: SUPLY
tags: [warehouse, WMS, pick-pack-ship, layout, receiving, fulfillment, KPIs]
---

# SUPLY Warehouse Management Skill

## Triggers

Activate this skill when the user says or implies:
- "warehouse", "warehouse management", "WMS"
- "layout", "warehouse layout", "storage design"
- "pick pack ship", "picking", "packing", "order fulfillment"
- "receiving", "inbound", "put-away"
- "warehouse KPIs", "pick accuracy", "cycle time"
- "fulfillment center", "distribution center operations"

## Workflow

### Step 1 — Warehouse Layout Design
1. **Zone Definition**
   - Receiving dock and staging area
   - Quality inspection / quarantine zone
   - Bulk storage (pallet racking, floor stacking)
   - Pick zones (shelving, flow racks, carton pick)
   - Packing stations
   - Shipping dock and staging area
   - Returns processing area
   - Office and break areas
2. **Layout Principles**
   - Flow direction: Receiving → Storage → Pick → Pack → Ship (U-flow, I-flow, or L-flow)
   - Fast movers (A items) closest to packing/shipping
   - Minimize travel distance for pickers (golden zone at waist height)
   - Separate pedestrian and forklift traffic lanes
   - Adequate aisle widths (minimum 3m for forklifts, 1.2m for manual)
   - Fire safety compliance (sprinklers, exits, aisle clearance)
3. **Storage Solutions by Product Type**
   - Selective pallet racking (standard, most flexible)
   - Drive-in/drive-through (high density, FIFO/LIFO)
   - Flow racking (gravity-fed, FIFO for perishables)
   - Mezzanine (double floor space for small items)
   - Carton flow / shelving (for piece-pick operations)
   - Automated Storage and Retrieval (AS/RS) for high throughput

### Step 2 — Receiving & Put-Away
1. **Receiving Process**
   - Advance Shipping Notice (ASN) pre-receipt
   - Dock scheduling (appointment system to avoid congestion)
   - Unloading and quantity verification (count vs. PO)
   - Quality inspection (sampling plan or 100% check based on supplier tier)
   - System receipt (scan barcodes, update WMS inventory)
   - Exception handling (short shipments, damage, wrong items)
2. **Put-Away Strategies**
   - Directed put-away (WMS assigns optimal location based on rules)
   - Fixed locations (dedicated slot per SKU)
   - Random/floating locations (any available slot, system-tracked)
   - Zone-based (items go to their category zone)
   - Cross-docking (bypass storage, direct to outbound for immediate orders)
3. **Receiving KPIs**
   - Dock-to-stock time (target: <24h for standard, <4h for priority)
   - Receiving accuracy (target: >99.5%)
   - Put-away productivity (units/hour per worker)

### Step 3 — Pick/Pack/Ship Operations
1. **Picking Methods**
   - Single order picking (one order at a time — simple, low volume)
   - Batch picking (multiple orders at once, sort after — medium volume)
   - Wave picking (orders released in waves, coordinated with shipping)
   - Zone picking (pickers assigned to zones, orders pass through zones)
   - Pick-to-light / voice picking (technology-assisted for speed and accuracy)
2. **Packing Standards**
   - Right-size packaging (minimize DIM weight, reduce material waste)
   - Protective packaging standards by product fragility class
   - Packing slip / invoice inclusion
   - Branded packaging requirements (unboxing experience)
   - Hazmat packaging compliance (if applicable)
3. **Shipping Process**
   - Carrier label generation and manifest creation
   - Weight/dimension verification
   - Loading sequence optimization (last stop loaded first)
   - Proof of shipment (scan + timestamp)
   - Tracking number communication to customer

### Step 4 — WMS Configuration & Technology
1. **WMS Core Functions**
   - Inventory tracking (real-time location, quantity, status)
   - Order management (allocation, wave planning, prioritization)
   - Task management (directed work, labor tracking)
   - Reporting and analytics (dashboards, KPIs, alerts)
2. **Technology Integration**
   - Barcode / RFID scanning for all movements
   - Integration with ERP (inventory sync, order feed)
   - Integration with carrier systems (rate shopping, label printing)
   - Integration with e-commerce platforms (order import)
   - Mobile devices for workers (RF guns, tablets)
3. **WMS Selection Criteria** (if evaluating)
   - Scalability (handles current volume + 3-5 year growth)
   - Flexibility (supports multiple fulfillment models)
   - Cloud vs. on-premise deployment
   - Vendor support and implementation track record
   - Total cost (license, implementation, maintenance, hardware)

### Step 5 — Warehouse KPIs & Performance Management
1. **Productivity KPIs**
   - Lines picked per hour (by method: single, batch, wave)
   - Units packed per hour
   - Orders shipped per day
   - Receiving units per hour
   - Warehouse throughput (total units processed / time)
2. **Accuracy KPIs**
   - Pick accuracy rate (target: >99.7%)
   - Shipping accuracy rate (right item, right quantity, right address)
   - Inventory accuracy (cycle count vs. system, target >99%)
   - Receiving accuracy (actual vs. ASN match)
3. **Efficiency KPIs**
   - Space utilization (% of available storage capacity used)
   - Order cycle time (order received to shipped)
   - Dock-to-stock time
   - Lines per labor hour (overall productivity)
4. **Cost KPIs**
   - Cost per order fulfilled
   - Cost per unit handled
   - Labor cost as % of total warehouse cost
   - Overtime as % of total labor hours

### Step 6 — Continuous Improvement
1. **Lean Warehouse Principles**
   - 5S: Sort, Set in order, Shine, Standardize, Sustain
   - Eliminate waste (unnecessary motion, waiting, overprocessing)
   - Standard work procedures for each task
   - Visual management (floor markings, signage, dashboards)
2. **Kaizen Projects**
   - Monthly improvement projects targeting specific KPIs
   - Worker-driven suggestions and problem solving
   - A3 problem-solving for systemic issues
   - Gemba walks (management on the floor)

## Commands

```
/suply-warehouse layout [specs]        — Warehouse layout design recommendation
/suply-warehouse receiving             — Receiving process design and SOP
/suply-warehouse picking [method]      — Pick method selection and optimization
/suply-warehouse wms [requirements]    — WMS evaluation and configuration guide
/suply-warehouse kpis [period]         — Warehouse KPI dashboard
/suply-warehouse improve               — Continuous improvement opportunity scan
```

## Output Template

```markdown
# Warehouse Operations: [Facility Name]

## Facility Profile
- **Location**: [Address]
- **Size**: [X] sqm / [X] sqft
- **Capacity**: [X] pallet positions / [X] SKUs
- **Throughput**: [X] orders/day, [X] lines/day
- **Staff**: [X] FTEs, [X] shifts

## Layout Assessment
| Zone | Area (sqm) | % of Total | Utilization | Status |
|------|------------|------------|-------------|--------|
| Receiving | [X] | [X]% | [X]% | [OK/Bottleneck] |
| Storage | [X] | [X]% | [X]% | [OK/Bottleneck] |
| Pick Zones | [X] | [X]% | [X]% | [OK/Bottleneck] |
| Packing | [X] | [X]% | [X]% | [OK/Bottleneck] |
| Shipping | [X] | [X]% | [X]% | [OK/Bottleneck] |

## Performance Dashboard
| KPI | Current | Target | Status | Trend |
|-----|---------|--------|--------|-------|
| Pick accuracy | [X]% | >99.7% | [status] | [trend] |
| Lines/hour | [X] | [X] | [status] | [trend] |
| Order cycle time | [X]h | <[X]h | [status] | [trend] |
| Space utilization | [X]% | [X]% | [status] | [trend] |
| Cost per order | $[X] | <$[X] | [status] | [trend] |

## Improvement Opportunities
| Opportunity | Impact | Effort | Priority | Est. Savings |
|-------------|--------|--------|----------|-------------|
| [Opportunity] | [H/M/L] | [H/M/L] | [1-N] | $[X]/yr |
```

## Red Flags

- Pick accuracy below 99% (industry standard is 99.5%+)
- Inventory accuracy below 95% (system vs. physical count)
- No cycle counting program in place (relying on annual count only)
- Space utilization above 90% consistently (no room for growth or peak capacity)
- Space utilization below 50% (overcapacity, wasted cost)
- Order cycle time exceeding SLA without root cause analysis
- No WMS or operating on manual spreadsheets/paper-based processes
- Safety incidents trending upward (forklift accidents, ergonomic injuries)
- No receiving inspection process (damaged/wrong goods entering inventory)
- High overtime (>15% of total hours) as standard practice, not exception
- Picking method not matched to order profile (e.g., single-order picking for high-volume operation)
- No standard operating procedures (SOPs) documented for warehouse tasks

## Integration Points

- Receives from: `suply-inventory` (stock policies, reorder triggers), `suply-logistics` (shipping schedules), `suply-quality` (inspection requirements)
- Feeds into: `suply-logistics` (outbound shipments), `suply-cost` (warehouse cost data), `suply-inventory` (actual stock counts)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - SUPLY - Warehouse [Facility].md`

## Metrics to Track

- **Pick Accuracy**: Target >99.7%
- **Order Cycle Time**: Order to ship, by priority tier
- **Space Utilization**: Target 75-85% (room for peaks)
- **Cost per Order**: Trend and benchmark against industry
- **Lines per Labor Hour**: Productivity by pick method
- **Inventory Accuracy**: Target >99% (cycle count based)
