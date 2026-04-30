---
name: nexus-monitoring
description: "Monitoring & observability — Prometheus/Grafana, uptime monitoring, alerting, SLA dashboards, APM"
version: "1.0"
---

# NEXUS-MONITORING: Monitoring & Observability Skill

## When to Activate

**Trigger words (PT):** monitorizacao, alertas, uptime, grafana, prometheus, metricas, disponibilidade, sla, apm, logs, dashboards, observabilidade, latencia
**Trigger words (EN):** monitoring, alerts, uptime, grafana, prometheus, metrics, availability, sla, apm, logs, dashboards, observability, latency, tracing, health check

## Step-by-Step Workflow

### Phase 1: Monitoring Strategy
1. Define monitoring objectives: availability, performance, reliability, cost
2. Identify critical services and SLA requirements
3. Map the three pillars: Metrics, Logs, Traces
4. Select tooling stack:
   - Metrics: Prometheus, Datadog, CloudWatch, Azure Monitor
   - Logs: Loki, ELK, CloudWatch Logs, Datadog Logs
   - Traces: Jaeger, Zipkin, Datadog APM, OpenTelemetry
   - Dashboards: Grafana, Datadog, Kibana
5. Define retention policies per signal type
6. Budget for monitoring infrastructure

### Phase 2: Metrics Collection
1. Infrastructure metrics: CPU, memory, disk, network, IOPS
2. Application metrics (RED method):
   - Rate: requests per second
   - Errors: error rate / error ratio
   - Duration: latency percentiles (p50, p95, p99)
3. Business metrics: signups, transactions, revenue, active users
4. Custom metrics via Prometheus client libraries or StatsD
5. Service-level indicators (SLIs) aligned to SLOs

### Phase 3: Alerting
1. Define alert severity levels: P1 (critical), P2 (high), P3 (medium), P4 (low)
2. Alert routing: PagerDuty/OpsGenie for P1-P2, Slack for P3-P4
3. Alert rules based on SLOs (burn rate alerts preferred over threshold)
4. Reduce noise: aggregate, deduplicate, use inhibition rules
5. On-call rotation schedule and escalation policy
6. Alert documentation: runbook link in every alert

### Phase 4: Dashboards
1. Executive dashboard: SLA/SLO compliance, uptime, incidents
2. Service dashboard (per service): RED metrics, dependencies, errors
3. Infrastructure dashboard: resource utilization, capacity headroom
4. Business dashboard: KPIs, conversion, revenue metrics
5. Design principles: top-down (overview to detail), consistent layout
6. Grafana variables for environment/service filtering

### Phase 5: SLA/SLO Management
1. Define SLOs per service (e.g., 99.9% availability, p99 < 500ms)
2. Calculate error budgets (100% - SLO target)
3. Track error budget consumption rate
4. Burn rate alerts: fast burn (1h window) + slow burn (6h window)
5. Monthly SLO review with engineering teams
6. SLA reporting to customers (if contractual)

### Phase 6: Continuous Improvement
1. Post-incident review of monitoring gaps
2. Alert quality review: false positive rate, MTTA, MTTR
3. Dashboard usage analytics (are they being used?)
4. Quarterly monitoring stack review
5. Chaos engineering to validate alerting (Game Days)
6. OpenTelemetry adoption for vendor-neutral instrumentation

## Commands Table

| Command | Description |
|---------|-------------|
| `nexus monitor setup` | Monitoring stack architecture |
| `nexus monitor alerts` | Alert rules and routing design |
| `nexus monitor dashboard` | Dashboard template generator |
| `nexus monitor slo` | SLO/SLI definition template |
| `nexus monitor oncall` | On-call rotation and escalation setup |
| `nexus monitor audit` | Monitoring coverage gap analysis |
| `nexus monitor noise` | Alert noise reduction analysis |
| `nexus monitor incident` | Incident timeline reconstruction |

## Output Template

```markdown
# Monitoring Assessment — [Organization/Service]
**Date:** YYYY-MM-DD | **Stack:** [Prometheus/Grafana/etc.] | **Services:** X

## 1. Monitoring Coverage
| Service | Metrics | Logs | Traces | Alerts | Dashboard | SLO |
|---------|---------|------|--------|--------|-----------|-----|

## 2. SLO Status
| Service | SLO Target | Current | Error Budget | Budget Remaining |
|---------|-----------|---------|-------------|-----------------|

## 3. Alert Quality (Last 30d)
| Metric | Value |
|--------|-------|
| Total alerts fired | |
| True positives | |
| False positives (noise) | |
| MTTA (mean time to acknowledge) | |
| MTTR (mean time to resolve) | |

## 4. Top Incidents (Period)
| Date | Service | Duration | Impact | Root Cause | Monitor Gap? |
|------|---------|----------|--------|------------|-------------|

## 5. Recommendations
| # | Gap | Impact | Action | Priority |
|---|-----|--------|--------|----------|

## 6. Next Review: YYYY-MM-DD
```

## Red Flags

- No monitoring for production services
- Alerts without runbook links
- No on-call rotation or escalation policy
- Alert fatigue: >50% false positive rate
- SLOs not defined for customer-facing services
- No log aggregation (relying on SSH to individual servers)
- No distributed tracing for microservice architecture
- Dashboards exist but nobody reviews them
- Monitoring infrastructure itself not monitored
- No error budget tracking
- P1 alerts routed only to Slack (not paging)
- Metrics retention too short for trend analysis (<30 days)
