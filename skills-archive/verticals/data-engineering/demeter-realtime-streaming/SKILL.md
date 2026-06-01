---
name: demeter-realtime-streaming
description: Real-time data streaming — Kafka, Kinesis, Flink, Spark Streaming, ksqlDB, Pulsar. Event-driven architectures, CDC, real-time analytics. Triggers em "Kafka", "streaming", "real-time", "CDC", "Kinesis", "Flink", "event-driven", "exactly-once".
license: MIT
parent_agent: demeter-director
compliance: [lgpd_by_design, retention_policies]
---

# DEMETER-REALTIME-STREAMING — Event-Driven Data

## Quando usar
- Greenfield streaming architecture
- Batch → streaming migration
- CDC (Change Data Capture) de OLTP databases
- Real-time fraud detection / alerting
- Event sourcing patterns
- Materialized views em tempo real

## Stack
- **Apache Kafka** — message broker (incumbent)
- **AWS Kinesis** — managed alternative
- **Apache Pulsar** — Kafka alternative com multi-tenancy
- **Apache Flink** — stateful stream processing
- **Spark Structured Streaming** — micro-batches
- **ksqlDB** — SQL on streams
- **Debezium** — CDC (Postgres, MySQL, MongoDB)
- **Redpanda** — Kafka-compatible, simpler ops

## Patterns
- **Event Sourcing:** state = sum(events)
- **CQRS:** Command/Query Responsibility Segregation
- **Saga pattern:** distributed transactions
- **Exactly-once semantics:** Kafka transactions + idempotent consumers
- **Stream-table duality:** ksqlDB

## Templates
1. Kafka cluster setup (3 brokers HA + Schema Registry + Connect)
2. Debezium CDC pipeline (Postgres → Kafka → BigQuery)
3. Flink job (windowed aggregation + sink)
4. Spark Structured Streaming (micro-batch para warehouse)
5. ksqlDB pull/push queries

## Compliance
- ✓ Topic-level retention policies (GDPR right to be forgotten)
- ✓ Encryption at-rest + in-transit
- ✓ ACLs por consumer group
- ✓ PII masking em stream processing

## Cross-references
- [[demeter-etl]] — batch alternative
- [[demeter-event-tracking]] — front-end events
- [[demeter-warehouse]] — sink para analytics


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **demeter-realtime-streaming** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in demeter-realtime-streaming:**

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
