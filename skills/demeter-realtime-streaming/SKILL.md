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
