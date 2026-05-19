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
