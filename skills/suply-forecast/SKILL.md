---
name: suply-forecast
description: "S.U.P.L.Y. Demand Forecasting — statistical methods, seasonality analysis, safety stock calculation, demand sensing, and S&OP process"
version: "1.0"
agent: SUPLY
tags: [demand-forecasting, seasonality, safety-stock, demand-sensing, S&OP, planning]
---

# SUPLY Demand Forecasting Skill

## Triggers

Activate this skill when the user says or implies:
- "demand forecast", "forecasting", "predict demand"
- "seasonality", "seasonal patterns", "demand cycles"
- "safety stock", "buffer stock", "stock buffer"
- "demand sensing", "demand signals", "real-time demand"
- "S&OP", "sales and operations planning", "demand planning"
- "forecast accuracy", "forecast error", "MAPE"

## Workflow

### Step 1 — Data Collection & Preparation
1. **Historical Data Gathering**
   - Minimum 24 months of sales/demand history (36+ preferred)
   - Granularity: SKU-level, weekly or monthly
   - Clean outliers: promotions, stockouts, one-time events
   - Flag data gaps and impute missing values
2. **Demand Drivers Identification**
   - Internal: promotions, pricing changes, new product launches
   - External: seasonality, economic indicators, weather, competitor actions
   - Structural: market trends, regulatory changes, technology shifts
3. **Data Quality Assessment**
   - Completeness score (% of expected data points present)
   - Consistency check (units, currency, time zones)
   - Outlier detection and classification (true demand vs. noise)

### Step 2 — Forecasting Methods Selection
1. **Qualitative Methods** (for new products or limited data)
   - Delphi method (expert consensus)
   - Market research and customer surveys
   - Sales force composite (bottom-up from sales team)
   - Analogous forecasting (similar product history)
2. **Time Series Methods** (for stable demand patterns)
   - Moving Average (simple, weighted, exponential)
   - Exponential Smoothing (SES, Holt's linear, Holt-Winters seasonal)
   - ARIMA / SARIMA (auto-regressive integrated moving average)
   - Prophet (Facebook/Meta) for seasonal with holidays
3. **Causal Methods** (for driver-based forecasting)
   - Linear regression with demand drivers
   - Multiple regression with marketing mix variables
   - Econometric models with external indicators
4. **Machine Learning Methods** (for complex patterns)
   - Gradient boosting (XGBoost, LightGBM)
   - LSTM neural networks for sequence prediction
   - Ensemble methods (combine multiple models)

### Step 3 — Seasonality & Trend Analysis
1. **Decomposition**: Separate trend, seasonal, cyclical, and random components
2. **Seasonal Indices**: Calculate monthly/weekly indices relative to base
3. **Trend Projection**: Linear, exponential, or logistic growth curves
4. **Cycle Detection**: Business cycles, product lifecycle position
5. **Holiday & Event Calendar**: Map known demand spikes to calendar events

### Step 4 — Safety Stock Calculation
1. **Inputs Required**
   - Average demand per period
   - Demand variability (standard deviation)
   - Lead time (average and variability)
   - Desired service level (typically 95-99%)
   - Z-score for target service level
2. **Formulas**
   - Basic: SS = Z x sigma_demand x sqrt(lead_time)
   - With lead time variability: SS = Z x sqrt(LT x sigma_d^2 + d^2 x sigma_LT^2)
   - Service level approach: SS based on fill rate or cycle service level
3. **Segmented Safety Stock**
   - A items (high value): higher service level (99%)
   - B items (medium value): standard service level (95%)
   - C items (low value): lower service level (90%)

### Step 5 — Demand Sensing (Short-Term Adjustment)
1. **Real-Time Signals**: POS data, web traffic, social media trends
2. **Leading Indicators**: Order pipeline, quote requests, web search volume
3. **Weather Integration**: Weather-sensitive product adjustments
4. **Event-Driven Adjustments**: Promotions, competitor actions, supply disruptions
5. **Consensus Adjustment**: Sales team intelligence overlay on statistical forecast

### Step 6 — S&OP Process Integration
1. **Monthly S&OP Cycle**
   - Week 1: Data gathering and statistical forecast generation
   - Week 2: Demand review (sales + marketing input)
   - Week 3: Supply review (operations + procurement alignment)
   - Week 4: Executive S&OP meeting (final plan approval)
2. **Forecast Outputs**
   - Unconstrained demand forecast (what the market wants)
   - Constrained forecast (what we can supply)
   - Financial forecast (revenue and margin projection)
   - Consensus forecast (agreed plan across functions)

## Commands

```
/suply-forecast [product/category]     — Generate demand forecast with method selection
/suply-forecast seasonality [data]     — Seasonality analysis and index calculation
/suply-forecast safety-stock [params]  — Safety stock calculation with service levels
/suply-forecast accuracy [period]      — Forecast accuracy review and improvement plan
/suply-forecast sop                    — S&OP process design or review
/suply-forecast sensing                — Demand sensing signal configuration
```

## Output Template

```markdown
# Demand Forecast: [Product/Category]

## Forecast Summary
- **Period**: [Start — End]
- **Method**: [Selected method with rationale]
- **Granularity**: [SKU/Category x Weekly/Monthly]
- **Horizon**: [Short-term (1-3mo) / Medium (3-12mo) / Long (12-36mo)]

## Forecast Results
| Period | Base Forecast | Seasonal Adj. | Promo Adj. | Final Forecast | Confidence |
|--------|--------------|---------------|------------|----------------|------------|
| [Period] | [Units] | [+/- %] | [+/- %] | [Units] | [Low-High] |

## Seasonality Profile
| Month | Index | Interpretation |
|-------|-------|----------------|
| Jan | [X.XX] | [Above/Below average] |

## Safety Stock Recommendation
| SKU/Category | Avg Demand | Std Dev | Lead Time | Service Level | Safety Stock |
|-------------|------------|---------|-----------|---------------|-------------|
| [SKU] | [Units] | [Units] | [Days] | [%] | [Units] |

## Forecast Accuracy (Historical)
| Metric | Last Quarter | YTD | Target |
|--------|-------------|-----|--------|
| MAPE | [X]% | [X]% | <[X]% |
| Bias | [+/-X]% | [+/-X]% | <[X]% |
| WMAPE | [X]% | [X]% | <[X]% |

## Risks & Assumptions
| Risk | Probability | Impact on Forecast | Mitigation |
|------|-------------|-------------------|------------|
| [Risk] | [H/M/L] | [+/- X%] | [Action] |
```

## Red Flags

- Forecast built on less than 12 months of historical data without qualitative supplementation
- Single forecasting method used without cross-validation against alternatives
- Seasonality not accounted for in products with obvious seasonal patterns
- Safety stock calculated with a single service level across all SKUs (no segmentation)
- Forecast accuracy (MAPE) consistently above 30% without improvement actions
- No demand sensing layer for short-term forecast adjustments
- S&OP process skips executive review or does not produce consensus plan
- Forecast not updated after major market events (pandemic, competitor exit, regulation change)
- Stockout data not cleaned from historical demand (understates true demand)
- Promotional uplift not separated from baseline demand
- Forecast bias consistently positive or negative (systematic over/under-forecasting)
- No forecast accuracy KPI tracked or reported regularly

## Integration Points

- Feeds into: `suply-inventory` (reorder points, stock levels), `suply-procurement` (purchase planning), `suply-logistics` (capacity planning)
- Receives from: `suply-cost` (cost data for financial forecast), `suply-supplier` (lead time data)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - SUPLY - Forecast [Product].md`

## Metrics to Track

- **MAPE (Mean Absolute Percentage Error)**: Target <20% for A items, <30% for B/C
- **Bias**: Target within +/-5% (balanced forecast)
- **Forecast Value Added (FVA)**: Each adjustment step should improve accuracy
- **Weighted MAPE**: Revenue-weighted accuracy across portfolio
- **Safety Stock Turns**: Safety stock value relative to sales (minimize without stockouts)
- **Service Level Achievement**: Actual vs. target service level
