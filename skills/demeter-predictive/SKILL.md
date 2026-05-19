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
