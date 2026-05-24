---
name: nexus-cloud
description: "Cloud cost optimization — right-sizing, reserved/spot instances, FinOps, waste elimination, cost governance"
version: "1.0"
---

# NEXUS-CLOUD: Cloud Cost Optimization Skill

## When to Activate

**Trigger words (PT):** custo cloud, otimizacao de custos, finops, right-sizing, instancias reservadas, spot, desperdicio, fatura cloud, orçamento cloud, governanca de custos
**Trigger words (EN):** cloud cost, cost optimization, finops, right-sizing, reserved instances, spot instances, savings plans, waste, cloud bill, cloud budget, cost governance, cost allocation

## Step-by-Step Workflow

### Phase 1: Cost Visibility
1. Enable cost allocation tags: project, environment, team, cost-center
2. Set up billing alerts and budgets per account/project
3. Implement showback/chargeback model
4. Deploy cost monitoring: AWS Cost Explorer, Azure Cost Management, GCP Billing
5. FinOps tool selection: Infracost, Spot.io, CloudHealth, Kubecost
6. Monthly cost review cadence with engineering teams

### Phase 2: Waste Elimination (Quick Wins)
1. **Idle resources**: unused EC2/VMs, unattached EBS/disks, old snapshots
2. **Orphaned resources**: load balancers with no targets, unused elastic IPs
3. **Oversized resources**: instances with <20% avg CPU utilization
4. **Dev/staging left running**: environments running 24/7 instead of business hours
5. **Old generation**: previous-gen instance types (upgrade = cheaper)
6. Estimated savings: typically 20-35% of total cloud spend

### Phase 3: Right-Sizing
1. Analyze utilization data (minimum 14 days, ideally 30 days)
2. CPU, memory, network, disk IOPS utilization per instance
3. Recommendation engine: AWS Compute Optimizer, Azure Advisor, GCP Recommender
4. Downsize over-provisioned instances (watch for peak patterns)
5. Upsize under-provisioned instances (prevent performance issues)
6. Automate with horizontal/vertical autoscaling where applicable

### Phase 4: Commitment-Based Discounts
1. **Reserved Instances / Savings Plans**:
   - Analyze stable baseline workloads (running 24/7 consistently)
   - 1-year vs 3-year commitment tradeoffs
   - All upfront > partial upfront > no upfront (discount depth)
   - Coverage target: 60-80% of stable compute baseline
2. **Spot/Preemptible Instances**:
   - Suitable for: batch processing, CI/CD, stateless workers, dev/test
   - Not suitable for: databases, stateful services, user-facing production
   - Implement graceful interruption handling
   - Savings: 60-90% vs on-demand
3. Review and adjust quarterly

### Phase 5: Architecture Optimization
1. Serverless migration for event-driven, low-traffic workloads
2. Container density optimization (bin-packing)
3. Storage tiering: hot -> warm -> cold -> archive (S3/Blob lifecycle policies)
4. CDN for static assets (reduce origin load and egress)
5. Data transfer optimization: minimize cross-region, use VPC endpoints
6. Database: Aurora Serverless, managed services vs self-hosted

### Phase 6: FinOps Culture
1. Unit economics: cost per transaction, cost per user, cost per request
2. Engineering awareness: include cost in PR reviews and architecture decisions
3. FinOps team or champion per engineering team
4. Monthly FinOps review with spending trends and anomaly detection
5. Gamification: cost reduction leaderboard per team
6. Forecast accuracy tracking: predicted vs actual spend

## Commands Table

| Command | Description |
|---------|-------------|
| `nexus cloud audit` | Full cloud cost audit and savings report |
| `nexus cloud waste` | Waste identification and cleanup list |
| `nexus cloud rightsize` | Right-sizing recommendations |
| `nexus cloud reserved` | Reserved/Savings Plan coverage analysis |
| `nexus cloud spot` | Spot instance opportunity assessment |
| `nexus cloud budget` | Budget and alert setup guide |
| `nexus cloud tags` | Tagging strategy and compliance check |
| `nexus cloud forecast` | Cost forecasting template |

## Output Template

```markdown
# Cloud Cost Optimization Report — [Organization]
**Date:** YYYY-MM-DD | **Provider:** [AWS/Azure/GCP] | **Monthly Spend:** EUR X

## 1. Cost Breakdown
| Category | Monthly Cost | % of Total | MoM Change |
|----------|-------------|-----------|-----------|
| Compute | | | |
| Storage | | | |
| Database | | | |
| Network | | | |
| Other | | | |

## 2. Waste Identified
| Resource | Type | Monthly Cost | Action | Savings |
|----------|------|-------------|--------|---------|

## 3. Right-Sizing Opportunities
| Resource | Current | Recommended | Monthly Savings |
|----------|---------|------------|----------------|

## 4. Commitment Coverage
| Type | Current Coverage | Optimal | Savings if Optimized |
|------|-----------------|---------|---------------------|

## 5. Savings Summary
| Category | Annual Savings | Effort |
|----------|---------------|--------|
| Waste elimination | | Low |
| Right-sizing | | Medium |
| Commitments | | Low |
| Architecture | | High |
| **Total** | **EUR X** | |

## 6. Unit Economics
| Metric | Current | Target | Trend |
|--------|---------|--------|-------|

## 7. Next Review: YYYY-MM-DD
```

## Red Flags

- No cost allocation tags (impossible to attribute costs)
- No billing alerts or budgets set
- Cloud spend growing faster than revenue/users
- >30% of compute resources underutilized (<20% CPU avg)
- No reserved instances or savings plans for stable workloads
- Dev/staging environments running 24/7 without need
- Old snapshots and backups never cleaned up
- Data transfer costs unexpectedly high (cross-region, egress)
- No cost review cadence with engineering teams
- Single account/project for all environments (no cost separation)
- Oversized managed services (e.g., RDS db.r6g.xlarge for 10 queries/min)
- No FinOps practice or cost ownership culture


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nexus-cloud** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nexus-cloud:**

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
