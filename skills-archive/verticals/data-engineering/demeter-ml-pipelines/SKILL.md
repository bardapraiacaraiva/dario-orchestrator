---
name: demeter-ml-pipelines
description: ML pipelines production-grade. MLflow, Kubeflow, SageMaker, sklearn pipelines. Training, deployment, monitoring, drift detection. Triggers em "ML pipeline", "MLflow", "Kubeflow", "model deployment", "model monitoring", "training pipeline", "feature store".
license: MIT
parent_agent: demeter-director
compliance: [lgpd_by_design, model_explainability, ai_governance]
---

# DEMETER-ML-PIPELINES — ML em Produção

## Quando usar
- Greenfield ML pipeline (training → deploy → monitor)
- Migrar Jupyter notebooks para production
- Setup de feature store
- Model versioning e A/B testing de modelos
- Drift detection + retraining triggers
- MLOps maturity assessment

## Stack moderno
- **MLflow** — experiment tracking + model registry
- **Kubeflow** — pipelines em Kubernetes
- **DVC** — data versioning
- **Feast** — feature store
- **Seldon Core / KServe** — model serving
- **Evidently AI** — drift monitoring
- **Weights & Biases** — experiment tracking alternative
- **SageMaker** (AWS) / **Vertex AI** (GCP) / **Azure ML** — managed end-to-end

## Pipeline production-grade
```
1. Data extraction (versioned com DVC)
2. Feature engineering (com Feast)
3. Training (MLflow tracking)
4. Validation (test set + cross-validation)
5. Model registry (MLflow)
6. Deployment (canary 10% → 100%)
7. Monitoring (Evidently — data drift + model drift)
8. Retraining (triggered automaticamente por drift)
```

## Templates
1. MLflow pipeline (sklearn) com tracking + registry + serving
2. Kubeflow Pipeline DAG
3. SageMaker Pipeline (training + tuning + deployment)
4. Drift detection com Evidently (data + concept drift)
5. Canary deployment strategy

## Compliance
- ✓ **Model explainability:** SHAP/LIME para decisões individuais
- ✓ **Bias detection:** fairness metrics (Equalized Odds, Demographic Parity)
- ✓ **LGPD Art. 20:** direito à revisão humana de decisão automatizada
- ✓ **Model card:** documentação de uso + limitações

## Cross-references
- [[demeter-predictive]] — quando ML resolve problema preditivo
- [[demeter-data-quality]] — features quality
- [[lex-ai-governance]] — compliance Marco Legal IA


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **demeter-ml-pipelines** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in demeter-ml-pipelines:**

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
