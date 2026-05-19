---
name: demeter-dbt-workflows
description: dbt expert — modeling, testing, docs, packages, dbt Semantic Layer, dbt Mesh. Best practices. Triggers em "dbt", "dbt Core", "dbt Cloud", "dbt models", "dbt tests", "dbt macros", "dbt Semantic Layer", "dbt Mesh", "modelagem dimensional dbt".
license: MIT
parent_agent: demeter-director
compliance: [lgpd_by_design, model_documentation]
---

# DEMETER-DBT-WORKFLOWS — dbt Production Excellence

## Quando usar
- Greenfield dbt project (estruturar do zero)
- Migration: SQL ad-hoc → dbt
- Refactoring de projeto dbt legado
- dbt Cloud vs Core decision
- dbt Mesh (multi-team setup)
- Performance tuning (incremental, materialization strategy)

## Estrutura recomendada (Modern Data Stack)
```
models/
├── staging/         # Renames + casts (vista 1:1 com source)
├── intermediate/    # Lógica complexa, joins
├── marts/           # Final tables (fact, dim, OBT)
│   ├── core/        # Cross-team
│   ├── marketing/
│   ├── finance/
│   └── product/
└── snapshots/       # SCD Type 2

tests/               # Singular tests (.sql files)
macros/              # Reusable Jinja
seeds/               # CSV reference data
```

## Best practices
- **Naming:** `stg_<source>__<table>`, `int_<purpose>`, `fct_<grain>`, `dim_<entity>`, `obt_<purpose>`
- **Tests obrigatórios:** unique + not_null em PKs, accepted_values em enums
- **Documentation:** description em todos models + columns críticos
- **Incremental models:** para tabelas > 10M rows
- **Materialization strategy:** view (default), table (heavy), incremental (large), ephemeral (CTE)
- **Macros over copy-paste:** ROI alto

## Templates
1. dbt_project.yml production-grade
2. Source declaration + freshness
3. Staging model (renames + casts + soft deletes)
4. Mart fact table (incremental)
5. Mart dim table (SCD Type 2 com snapshot)
6. Custom test (singular SQL)
7. Macro reutilizável (anonymize_pii)
8. Semantic model (dbt Semantic Layer)

## Packages essenciais
- **dbt-utils:** Helper macros
- **dbt-expectations:** Great Expectations style tests
- **dbt-audit-helper:** PR comparison
- **dbt-labs/codegen:** Auto-generate boilerplate
- **calogica/dbt-date:** Date helpers
- **dbt-project-evaluator:** Best practices linter

## Cross-references
- [[demeter-warehouse]] — onde dbt corre
- [[demeter-dataops]] — dbt em CI/CD
- [[demeter-metrics-layer]] — dbt Semantic
- [[demeter-data-quality]] — dbt tests
