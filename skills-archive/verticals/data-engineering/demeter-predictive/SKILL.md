---
name: demeter-predictive
description: Predictive analytics — forecasting, churn prediction, propensity scoring, demand forecasting. Triggers em "forecast", "churn prediction", "propensity scoring", "demand forecasting", "Prophet", "ARIMA", "time series", "regression".
license: MIT
parent_agent: demeter-director
compliance: [model_explainability, lgpd_by_design, ai_governance]
---

# DEMETER-PREDICTIVE — Modelos Preditivos

## Quando usar
- Forecast de revenue/demand/churn
- Churn prediction (próximas 30 dias)
- Lead scoring (propensão a comprar)
- Demand forecasting (inventário)
- Anomaly detection (fraud, system failures)

## Stack
- **Prophet (Meta):** time series com sazonalidade
- **ARIMA / SARIMA:** time series clássico
- **XGBoost / LightGBM:** tabular regression/classification
- **TensorFlow / PyTorch:** deep learning quando necessário
- **scikit-learn:** baseline e produção
- **NeuralProphet:** time series com features adicionais

## Templates
1. Revenue forecast (Prophet com holidays/promotions)
2. Churn prediction (XGBoost + SHAP explainability)
3. Lead scoring (logistic regression com calibration)
4. Demand forecast (NeuralProphet com regressors externos)
5. Anomaly detection (Isolation Forest + Z-score híbrido)

## Métricas avaliação
- **Regression:** MAE, MAPE, RMSE, R²
- **Classification:** Precision, Recall, F1, AUC-ROC, calibration
- **Forecasting:** MAPE, sMAPE, MASE
- **Business metrics:** revenue impact, decisões prevenidas

## Princípios
- **Baseline first:** modelo simples (média móvel, regressão linear) antes de XGBoost
- **Cross-validation temporal:** time-series CV (não k-fold normal)
- **Calibration:** probabilities devem corresponder a frequências reais
- **Explainability:** SHAP/LIME para top features

## Cross-references
- [[demeter-ml-pipelines]] — production deployment
- [[demeter-cohort-analysis]] — feature engineering por cohort
- [[demeter-data-quality]] — features quality


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **demeter-predictive** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in demeter-predictive:**

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
