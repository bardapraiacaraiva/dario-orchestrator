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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **demeter-data-catalog** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in demeter-data-catalog:**

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
