---
name: kirion-market-comparables
description: Comparable sales analysis (CMA), hedonic pricing, GIS-based. Triggers em "CMA", "comparable analysis", "hedonic pricing", "GIS real estate", "Imovirtual", "ZAP Imóveis", "Idealista".
license: SEE-LICENSE
parent_agent: kirion-director
---

# KIRION-MARKET-COMPARABLES

## Sources data
- **PT:** Idealista, Imovirtual, Casa Sapo, Confidencial Imobiliário, INE
- **BR:** ZAP, Vivareal, ImovelWeb, FGV-IBRE, IGV índice
- **Global:** Zillow, Redfin (US), Rightmove (UK)
- **Off-market:** broker network, transaction databases

## Hedonic pricing variables
- **Location:** lat/lng, neighbourhood, school district, transit
- **Property:** size, bedrooms, age, condition
- **Quality:** finishings, view, floor
- **Amenities:** parking, garden, pool, elevator
- **Macro:** crime, demographics, employment

## Adjustments típicas
- **Time:** appreciation since comp transaction (% per month)
- **Location:** premium/discount per neighborhood
- **Size:** $ per m² regression
- **Condition:** renovation cost adjustment
- **Features:** parking + R$ 30K, view + 5%, etc.

## Templates
1. CMA worksheet (8-12 comparables)
2. Hedonic regression model
3. Adjustment matrix (10 dimensions)
4. GIS heat map visualization
5. Confidential Imobiliário data integration
6. Time series adjustment factor

## Cross-references
- [[kirion-real-estate-valuation]] · [[kirion-dcf-property]] · [[demeter-predictive]]
