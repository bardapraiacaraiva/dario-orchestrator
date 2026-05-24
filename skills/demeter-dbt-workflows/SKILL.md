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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **demeter-dbt-workflows** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in demeter-dbt-workflows:**

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
