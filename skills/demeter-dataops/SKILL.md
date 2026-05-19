---
name: demeter-dataops
description: DataOps — CI/CD para data, data testing, versioning, deployment automation. dbt CI, GitHub Actions for data, lakeFS, DVC. Triggers em "DataOps", "CI/CD data", "dbt CI", "data versioning", "lakeFS", "DVC", "data deployment".
license: MIT
parent_agent: demeter-director
compliance: [lgpd_by_design, pipeline_governance]
---

# DEMETER-DATAOPS — CI/CD para Data

## Filosofia
**Treat data as code.** PRs com tests, deployments versionados, rollback possible, monitoring built-in.

## Quando usar
- Bootstrap de DataOps (greenfield)
- Migração de processos manuais para CI/CD
- Setup de dbt Cloud / dbt Core CI
- Versioning de dados (DVC, lakeFS)
- Blue-green deployment para pipelines
- Disaster recovery para data

## Stack
- **GitHub Actions / GitLab CI:** orchestrate CI
- **dbt Cloud / dbt Core:** transformations versionadas
- **lakeFS:** git-like for data lakes
- **DVC:** data + model versioning
- **Datafold:** PR comparison para data
- **SQLFluff:** SQL linting
- **Pre-commit hooks:** quality gates locais

## Workflow
```
1. Developer abre PR (SQL/Python changes)
2. CI runs:
   - SQL lint (SQLFluff)
   - dbt parse + compile
   - dbt run em dev/staging warehouse
   - dbt test (data quality)
   - Datafold compare (production vs PR)
3. Review humano (1+ approver)
4. Merge → automatic deploy to production
5. Monitor (Soda / Monte Carlo) post-deploy
```

## Templates
1. GitHub Actions workflow para dbt (run + test + docs)
2. SQLFluff config (.sqlfluff)
3. Pre-commit hook config
4. lakeFS branching strategy
5. Datafold setup para PR comparison
6. Blue-green deployment para Airflow DAGs

## Princípios
- **PR mandatory:** ninguém faz push direto para main
- **Tests obrigatórios:** falha = block merge
- **Documentation generated:** dbt docs sempre actualizada
- **Versioning:** semver para data products (v1.2.3)
- **Rollback plan:** sempre claro

## Cross-references
- [[demeter-etl]] — pipelines deployed via DataOps
- [[demeter-data-quality]] — testing como gate
- [[demeter-dbt-workflows]] — transformations em CI
- [[builder-ci-cd]] — pattern transferível para code geral
