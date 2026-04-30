---
name: nexus-database
description: "Database administration — schema design, migrations, performance tuning, replication, backup, monitoring"
version: "1.0"
---

# NEXUS-DATABASE: Database Administration Skill

## When to Activate

**Trigger words (PT):** base de dados, schema, migracoes, performance, replicacao, indice, query, postgresql, mysql, mongodb, redis, otimizacao de queries, backup de base de dados
**Trigger words (EN):** database, schema, migrations, performance, replication, index, query, postgresql, mysql, mongodb, redis, query optimization, database backup, dba, connection pool, deadlock

## Step-by-Step Workflow

### Phase 1: Schema Design
1. Requirements gathering: data model, relationships, access patterns
2. Normalization: 3NF for OLTP, denormalize for read-heavy patterns
3. Data types: use appropriate types (avoid storing numbers as strings)
4. Primary keys: UUID vs auto-increment (distribution considerations)
5. Foreign keys: enforce referential integrity, cascade rules
6. Indexing strategy: primary, unique, composite, partial, covering
7. Partitioning strategy for large tables (range, hash, list)
8. Naming conventions: snake_case, singular table names, descriptive columns

### Phase 2: Migration Management
1. Migration tool selection: Prisma Migrate, Flyway, Alembic, Knex, golang-migrate
2. Migration file naming: `YYYYMMDDHHMMSS_description.sql`
3. Rules:
   - Never modify a released migration
   - Always write both up and down migrations
   - Test migrations in staging before production
   - Avoid breaking changes: add columns nullable first, backfill, then constrain
4. Schema versioning: track applied migrations in database
5. Large table migrations: online DDL (pt-online-schema-change, pg_repack)
6. Rollback plan for every migration

### Phase 3: Performance Tuning
1. **Query optimization**:
   - EXPLAIN ANALYZE for slow queries
   - Index usage verification (unused indexes waste write performance)
   - N+1 query detection and resolution
   - Query plan caching and prepared statements
2. **Server configuration**:
   - PostgreSQL: shared_buffers (25% RAM), work_mem, effective_cache_size
   - MySQL: innodb_buffer_pool_size (70-80% RAM), query_cache
   - Connection pooling: PgBouncer, ProxySQL (avoid connection exhaustion)
3. **Monitoring queries**:
   - pg_stat_statements for top queries by time/calls
   - Slow query log analysis
   - Lock contention and deadlock detection

### Phase 4: Replication & High Availability
1. PostgreSQL: streaming replication (sync/async), logical replication
2. MySQL: GTID-based replication, group replication
3. Read replicas: route reads to replicas, writes to primary
4. Failover strategy:
   - Managed: RDS Multi-AZ, Aurora, Cloud SQL HA
   - Self-managed: Patroni (PG), Orchestrator (MySQL)
5. Replication lag monitoring and alerting
6. Split-brain prevention mechanisms

### Phase 5: Backup & Recovery
1. Backup strategy aligned with RPO (see nexus-backup skill)
2. PostgreSQL: pg_basebackup + WAL archiving for PITR
3. MySQL: mysqldump (logical), xtrabackup (physical)
4. Managed services: automated snapshots + PITR
5. Restore testing: monthly validation of backup integrity
6. Encryption of backups at rest

### Phase 6: Monitoring & Alerting
1. Key metrics to monitor:
   - Connection count vs max_connections (alert at 80%)
   - Query latency percentiles (p50, p95, p99)
   - Replication lag (alert >5s for async, >0 for sync)
   - Disk usage and growth rate (alert at 80%)
   - Cache hit ratio (target >99% for PG buffer cache)
   - Deadlocks per minute, lock wait time
2. Tools: pganalyze, Datadog, CloudWatch, PMM (Percona)
3. Automated alerts for all critical thresholds
4. Capacity forecasting: project disk full date, connection saturation

## Commands Table

| Command | Description |
|---------|-------------|
| `nexus db design` | Schema design review and recommendations |
| `nexus db migrate` | Migration best practices checklist |
| `nexus db performance` | Performance audit and tuning guide |
| `nexus db replication` | Replication architecture review |
| `nexus db backup` | Database backup strategy review |
| `nexus db monitor` | Monitoring setup and dashboard |
| `nexus db index` | Index analysis and recommendations |
| `nexus db audit` | Full database health assessment |

## Output Template

```markdown
# Database Assessment — [Database/Service]
**Date:** YYYY-MM-DD | **Engine:** [PostgreSQL X.X/MySQL X.X/etc.] | **Size:** X GB

## 1. Health Overview
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Uptime | | 99.9%+ | |
| Avg query latency (p95) | | <100ms | |
| Connection utilization | | <80% | |
| Cache hit ratio | | >99% | |
| Replication lag | | <1s | |
| Disk usage | | <80% | |

## 2. Top Slow Queries
| Query | Avg Time | Calls/day | Total Time | Fix |
|-------|----------|-----------|-----------|-----|

## 3. Index Analysis
| Table | Missing Index | Unused Index | Recommendation |
|-------|-------------|-------------|---------------|

## 4. Replication Status
| Role | Host | Lag | Status | Last Failover Test |
|------|------|-----|--------|--------------------|

## 5. Backup Status
| Type | Schedule | Last Success | RPO Met | Restore Tested |
|------|----------|-------------|---------|---------------|

## 6. Recommendations
| # | Finding | Impact | Action | Priority |
|---|---------|--------|--------|----------|

## 7. Next Review: YYYY-MM-DD
```

## Red Flags

- No indexes on frequently queried columns
- N+1 queries in application code
- Connection pooling not configured (direct connections)
- Replication lag growing over time
- No backup or backup never tested
- Database disk >90% full with no growth plan
- Queries without LIMIT on large tables
- No slow query logging enabled
- Schema migrations applied directly to production (no staging test)
- Single database instance with no replication (SPOF)
- Credentials hardcoded in application config
- No monitoring or alerting on database metrics
