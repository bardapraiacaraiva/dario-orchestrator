---
name: nexus-capacity
description: "Capacity planning — demand forecasting, scaling strategies, load testing, performance baselines, resource planning"
version: "1.0"
---

# NEXUS-CAPACITY: Capacity Planning Skill

## When to Activate

**Trigger words (PT):** capacidade, planeamento de capacidade, escalabilidade, load testing, teste de carga, baseline, previsao de crescimento, auto-scaling, dimensionamento, performance
**Trigger words (EN):** capacity, capacity planning, scalability, load testing, stress testing, baseline, growth forecasting, auto-scaling, sizing, performance, throughput, bottleneck

## Step-by-Step Workflow

### Phase 1: Current State Baseline
1. Inventory all infrastructure resources (compute, storage, network, database)
2. Establish baseline metrics for normal operation:
   - CPU utilization (avg, p95, max)
   - Memory utilization (avg, p95, max)
   - Disk I/O (IOPS, throughput, latency)
   - Network throughput and connection counts
   - Application: requests/sec, response time (p50, p95, p99)
   - Database: queries/sec, connection count, replication lag
3. Identify current peak periods (time of day, day of week, seasonal)
4. Document current resource headroom per component
5. Map resource dependencies and bottleneck chains

### Phase 2: Demand Forecasting
1. Historical trend analysis: 3-6 months minimum data
2. Growth drivers: user growth, feature launches, marketing campaigns, seasonality
3. Forecasting methods:
   - Linear extrapolation (steady growth)
   - Exponential (viral/high-growth phase)
   - Seasonal decomposition (cyclical patterns)
4. Create 3 scenarios: conservative (base), expected, aggressive
5. Project resource needs per scenario (compute, storage, bandwidth)
6. Identify "cliff" moments: when current capacity is exhausted

### Phase 3: Scaling Strategy
1. **Vertical scaling** (scale up): larger instances
   - Quick, no architecture change
   - Limited by max instance size, requires downtime
2. **Horizontal scaling** (scale out): more instances
   - Requires stateless architecture or distributed state
   - Auto-scaling groups, K8s HPA/VPA
3. **Database scaling**:
   - Read replicas for read-heavy workloads
   - Sharding for write-heavy workloads
   - Caching layer (Redis/Memcached) to reduce DB load
4. **CDN/Edge**: offload static content, edge computing
5. **Async processing**: queue-based architecture for burst handling
6. Auto-scaling policies: target tracking, step scaling, scheduled

### Phase 4: Load Testing
1. Define test scenarios:
   - **Load test**: expected traffic (validate current capacity)
   - **Stress test**: 2-3x expected traffic (find breaking points)
   - **Spike test**: sudden traffic surge (validate auto-scaling)
   - **Soak test**: sustained load over hours (find memory leaks, connection leaks)
2. Tool selection: k6, Locust, Gatling, Artillery, JMeter
3. Test environment: production-like (same instance types, data volume)
4. Realistic traffic patterns: user journeys, not just endpoint hammering
5. Measure: throughput, latency, error rate, resource utilization
6. Identify bottlenecks and saturation points

### Phase 5: Performance Optimization
1. Application: profiling, caching, query optimization, connection pooling
2. Database: index tuning, query rewrite, partitioning, materialized views
3. Infrastructure: instance right-sizing, storage IOPS provisioning
4. Network: CDN configuration, compression, connection reuse (keep-alive)
5. Architecture: async processing, microservice decomposition, event-driven
6. Cost-performance tradeoffs: cheapest path to meeting SLOs

### Phase 6: Capacity Governance
1. Monthly capacity review with trending dashboard
2. Capacity thresholds and alerts (80% utilization = plan, 90% = act)
3. Lead time accounting: procurement, provisioning, migration
4. Budget alignment: capacity plan feeds into cloud cost forecast
5. Capacity requirements in new feature/project intake process
6. Annual capacity planning cycle aligned with business planning

## Commands Table

| Command | Description |
|---------|-------------|
| `nexus capacity baseline` | Current state resource baseline |
| `nexus capacity forecast` | Demand forecasting model |
| `nexus capacity loadtest` | Load testing plan and execution guide |
| `nexus capacity scaling` | Scaling strategy recommendation |
| `nexus capacity optimize` | Performance optimization checklist |
| `nexus capacity review` | Monthly capacity review dashboard |
| `nexus capacity plan` | Annual capacity plan template |
| `nexus capacity alert` | Capacity threshold alerting setup |

## Output Template

```markdown
# Capacity Planning Report — [Service/Organization]
**Date:** YYYY-MM-DD | **Period:** [Q/Year] | **Lead:** [Name]

## 1. Current Baseline
| Resource | Current Usage | Peak Usage | Capacity | Headroom |
|----------|-------------|-----------|----------|----------|
| CPU | | | | % |
| Memory | | | | % |
| Storage | | | | GB |
| Network | | | | Mbps |
| DB connections | | | | count |
| Requests/sec | | | | rps |

## 2. Growth Forecast
| Metric | Current | +3 months | +6 months | +12 months |
|--------|---------|-----------|-----------|-----------|

## 3. Capacity Cliff Dates
| Resource | Exhaustion Date (Conservative) | Expected | Aggressive |
|----------|-------------------------------|----------|-----------|

## 4. Scaling Recommendations
| Resource | Action | When | Cost Impact | Effort |
|----------|--------|------|-----------|--------|

## 5. Load Test Results (Latest)
| Scenario | Peak RPS | P95 Latency | Error Rate | Bottleneck |
|----------|---------|-------------|-----------|-----------|

## 6. Action Items
| # | Action | Owner | Deadline | Status |
|---|--------|-------|----------|--------|

## 7. Next Load Test: YYYY-MM-DD | Next Review: YYYY-MM-DD
```

## Red Flags

- No baseline metrics established
- No load testing ever conducted
- Auto-scaling not configured for variable workloads
- Resources consistently >85% utilized with no scaling plan
- Growth forecast not aligned with business/product roadmap
- No capacity alerts (discovering saturation reactively)
- Database at max connections with no pooling
- Storage growth rate exceeds provisioned capacity timeline
- No consideration of lead time for capacity changes
- Single bottleneck point that limits entire system
- Load tests run on non-production environments with different sizing
- No cost-capacity tradeoff analysis
