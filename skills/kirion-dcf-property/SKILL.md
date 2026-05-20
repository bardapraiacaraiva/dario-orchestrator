---
name: kirion-dcf-property
description: DCF property — NPV, IRR, cap rate, exit yield, leveraged returns. Triggers em "DCF property", "NPV imóvel", "IRR real estate", "cap rate", "exit yield", "leveraged IRR", "underwriting".
license: SEE-LICENSE
parent_agent: kirion-director
---

# KIRION-DCF-PROPERTY

## DCF components RE
```
NOI = Gross Rent - Vacancy - Operating Expenses
DCF Year N:
  CF = NOI_N + Capex_N
  Terminal Value = NOI_(N+1) / Exit Cap Rate
  PV = Σ CF / (1+r)^t + TV / (1+r)^N
```

## Métricas chave
- **Going-in cap rate:** NOI Year 1 / Price
- **Exit cap rate:** assumption tipicamente 25-50 bps above going-in
- **Stabilized cap rate:** post-leasing/renovation
- **Cash-on-Cash:** Cash flow / Equity invested (leveraged metric)
- **Unleveraged IRR:** all-cash deal
- **Leveraged IRR:** with debt financing
- **Equity multiple:** total cash returned / cash invested

## Discount rates típicas
- **Office stabilized:** WACC 6-8%
- **Retail prime:** 7-9%
- **Industrial:** 6.5-8.5%
- **Development:** 12-18% (risk premium)
- **Hotel:** 10-14%

## Templates
1. 10-year DCF model template (5 sheets)
2. Sensitivity table (cap rate × growth rate)
3. Leveraged vs unleveraged comparison
4. Capex schedule (capital improvements)
5. Hold period analysis (3y, 5y, 7y, 10y)
6. Waterfall structure (LP/GP)

## Cross-references
- [[kirion-real-estate-valuation]] · [[kirion-reit-analysis]] · [[zenith-ma-evaluation]]
