---
name: nexus-backup
description: "Backup & disaster recovery — 3-2-1 rule, RPO/RTO, restore testing, DR runbook, data protection"
version: "1.0"
---

# NEXUS-BACKUP: Backup & Disaster Recovery Skill

## When to Activate

**Trigger words (PT):** backup, recuperacao de desastres, dr, restauro, rpo, rto, 3-2-1, replicacao, retencao, snapshots, plano de recuperacao, continuidade
**Trigger words (EN):** backup, disaster recovery, dr, restore, rpo, rto, 3-2-1 rule, replication, retention, snapshots, recovery plan, continuity, failover, failback

## Step-by-Step Workflow

### Phase 1: Data Classification & RPO/RTO
1. Inventory all data stores: databases, file systems, object storage, SaaS data
2. Classify data by criticality: mission-critical, important, standard, archive
3. Define RPO per data store (maximum acceptable data loss):
   - Mission-critical: <15 min | Important: <1h | Standard: <24h
4. Define RTO per system (maximum acceptable downtime):
   - Mission-critical: <1h | Important: <4h | Standard: <24h
5. Map dependencies between systems for recovery ordering
6. Document data ownership and compliance requirements (RGPD retention)

### Phase 2: Backup Strategy (3-2-1 Rule)
1. **3 copies**: production + 2 backups
2. **2 different media**: disk + cloud, or disk + tape
3. **1 offsite**: different region or cloud provider
4. Backup types per data store:
   - Full: weekly or monthly
   - Incremental: daily
   - Continuous: WAL shipping, CDC, real-time replication
5. Encryption: at rest (AES-256) and in transit (TLS)
6. Immutable backups for ransomware protection (WORM, object lock)

### Phase 3: Implementation
1. Database backups: pg_dump/pg_basebackup, mysqldump, mongodump, native cloud snapshots
2. File system: rsync, restic, Veeam, cloud-native (EBS snapshots, Azure Backup)
3. SaaS data: API exports, third-party backup tools (Spanning, OwnBackup)
4. Container volumes: PVC snapshots, Velero for Kubernetes
5. Configuration: IaC (Terraform state), Git repos, secrets vault
6. Scheduling: cron jobs, cloud scheduler, backup orchestration tools

### Phase 4: DR Planning
1. Define DR scenarios: site failure, region outage, ransomware, data corruption, human error
2. Design DR architecture:
   - **Hot standby**: real-time replication, instant failover
   - **Warm standby**: periodic replication, <4h recovery
   - **Cold standby**: backups only, >24h recovery
3. Document DR runbook: step-by-step recovery procedures
4. Failover procedure: DNS changes, load balancer updates, connection strings
5. Failback procedure: data sync back, switch to primary
6. Communication plan during DR event

### Phase 5: Testing & Validation
1. Automated restore testing: monthly for critical, quarterly for standard
2. Full DR drill: annual minimum, tabletop + functional
3. Test scenarios: single database restore, full environment recovery, partial corruption
4. Validate data integrity after restore (checksums, row counts, application tests)
5. Measure actual RTO vs target RTO
6. Document test results and remediate gaps

### Phase 6: Monitoring & Maintenance
1. Monitor backup job success/failure (alert on failure)
2. Track backup sizes and growth trends
3. Verify backup integrity (periodic checksum validation)
4. Retention policy enforcement and cleanup
5. Cost optimization: lifecycle policies, storage tiers (hot/warm/cold)
6. Annual strategy review aligned with BIA changes

## Commands Table

| Command | Description |
|---------|-------------|
| `nexus backup audit` | Backup coverage and gap analysis |
| `nexus backup strategy` | Backup strategy design template |
| `nexus backup dr` | DR runbook generator |
| `nexus backup test` | Restore test plan and checklist |
| `nexus backup monitor` | Backup monitoring dashboard |
| `nexus backup cost` | Backup cost analysis and optimization |
| `nexus backup retention` | Retention policy template |
| `nexus backup ransomware` | Ransomware resilience checklist |

## Output Template

```markdown
# Backup & DR Assessment — [Organization]
**Date:** YYYY-MM-DD | **Assessed By:** [Name]

## 1. Data Store Inventory
| Data Store | Type | Size | RPO Target | RTO Target | Classification |
|-----------|------|------|-----------|-----------|---------------|

## 2. Backup Status
| Data Store | Backup Type | Schedule | Last Success | 3-2-1 | Encrypted | Immutable |
|-----------|------------|----------|-------------|-------|-----------|-----------|

## 3. DR Readiness
| System | DR Type | Failover Tested | Last Test | Actual RTO | Gap |
|--------|---------|----------------|-----------|-----------|-----|

## 4. Restore Test Results
| Date | Data Store | Scenario | Duration | Success | Issues |
|------|-----------|----------|----------|---------|--------|

## 5. Cost Summary
| Storage Type | Monthly Cost | Optimization Opportunity |
|-------------|-------------|------------------------|

## 6. Recommendations
| # | Issue | Risk | Action | Priority |
|---|-------|------|--------|----------|

## 7. Next Test: YYYY-MM-DD | Next Review: YYYY-MM-DD
```

## Red Flags

- No backups for production databases
- Backups never tested (restore never validated)
- All backups in same region/provider as production
- No encryption on backup data
- RPO/RTO not defined or not aligned with business needs
- Backup failures not monitored or alerting not configured
- No immutable backups (vulnerable to ransomware)
- DR runbook does not exist or is outdated
- DR never tested or last test >12 months ago
- SaaS data not backed up (assuming vendor handles it)
- No retention policy (backups grow indefinitely or deleted too early)
- Single person knows the restore procedure
