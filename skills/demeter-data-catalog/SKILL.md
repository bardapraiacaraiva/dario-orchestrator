---
name: demeter-data-catalog
description: Data catalog & governance — Amundsen, DataHub, OpenMetadata, Atlan, Collibra. Discovery, lineage, ownership, classification, business glossary. Triggers em "data catalog", "data governance", "Amundsen", "DataHub", "OpenMetadata", "lineage", "data discovery", "business glossary".
license: MIT
parent_agent: demeter-director
compliance: [lgpd_governance, data_classification, ownership_clear]
---

# DEMETER-DATA-CATALOG — Data Discovery e Governance

## Quando usar
- Catalog implementation (greenfield)
- Lineage tracking end-to-end
- Business glossary definition
- Data classification (public/internal/confidential/PII)
- Data ownership (DPO + Data Stewards)
- Auditoria de catalog existente

## Stack
- **Amundsen** (Lyft, open-source)
- **DataHub** (LinkedIn, open-source enterprise)
- **OpenMetadata** (open-source, moderna)
- **Atlan** (proprietary, modern UX)
- **Collibra** (enterprise heavyweight)
- **Alation** (enterprise)
- **dbt + dbt-docs** (lightweight)

## O que catalogar
- **Tables/views:** schema + business definition + owner
- **Pipelines:** quem produz e quem consome
- **Metrics:** definição canónica (single source of truth)
- **Dashboards:** quem usa, frequência, importância
- **Reports:** auditoria de uso
- **Models ML:** registry + version + performance

## Lineage
- **Column-level lineage:** quando coluna X foi computed?
- **Cross-system lineage:** Postgres → Airflow → BigQuery → Looker
- **Impact analysis:** "se mudar tabela X, que dashboards quebram?"

## Templates
1. DataHub deployment (Helm chart + Kafka + ElasticSearch)
2. Amundsen setup minimal
3. dbt sources.yml + descriptions completos (lightweight catalog)
4. Data classification rubric (PII, PHI, Financial)
5. RACI matrix (DPO + Data Owners + Data Stewards)

## Governança
- **Data Steward:** dono de domínio (Marketing, Finance, etc.)
- **DPO:** compliance LGPD
- **Data Engineer:** technical owner
- **Consumer:** analista, PM, executive

## Compliance
- ✓ Auto-detection PII (regex + ML classifier)
- ✓ Right-to-be-forgotten propagation (deletion lineage)
- ✓ Access control auditing

## Cross-references
- [[demeter-data-quality]] — quality status no catalog
- [[demeter-warehouse]] — schema catalog source
- [[risco-rgpd]] — compliance audit
