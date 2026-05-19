---
name: demeter-data-quality
description: Data quality testing automatizado. Great Expectations, dbt tests, Soda, Monte Carlo, Anomalo. Detecta data drift, freshness, completeness, uniqueness. Triggers em "data quality", "Great Expectations", "dbt tests", "Soda", "data drift", "anomaly detection".
license: MIT
parent_agent: demeter-director
compliance: [lgpd_by_design, pii_detection]
---

# DEMETER-DATA-QUALITY — Garbage In, Garbage Out (Stop It Here)

## Quando usar
- Bootstrap de programa de data quality
- Auditoria de pipelines existentes (que tests faltam?)
- Investigação de incidents (data foi corrompida quando?)
- Setup de alerting automatic
- Definir SLA de qualidade

## 7 dimensões de data quality
1. **Completeness:** não-nulos onde esperado
2. **Uniqueness:** duplicates detectados
3. **Validity:** formato correto (CPF, email, dates)
4. **Consistency:** referential integrity preservada
5. **Accuracy:** valores fazem sentido (idade não negativa)
6. **Freshness:** data não-stale (idade dos registos)
7. **Drift:** distribuição muda ao longo do tempo

## Templates
1. Great Expectations suite completa para pipeline ETL
2. dbt schema.yml com tests (unique, not_null, accepted_values, relationships)
3. Soda Cloud monitors para production tables
4. Anomaly detection com ML (Prophet, Isolation Forest)
5. Data quality dashboard (Soda + Grafana)

## SLA de qualidade
| Métrica | SLA típico |
|---|---|
| Freshness | 99% < 4h delay |
| Completeness | 99.5% non-null em colunas críticas |
| Uniqueness | 0 duplicados em PKs |
| Validity | 99.9% formato válido (emails, CPFs) |
| Drift | < 5% population shift sem alert |

## Compliance
- ✓ PII detection automatic (regex CPF/CNPJ/email)
- ✓ Anomalias flagged não bloqueiam pipeline mas requerem review

## Cross-references
- [[demeter-etl]] — gates pre/post load
- [[demeter-dataops]] — testing como CI gate
