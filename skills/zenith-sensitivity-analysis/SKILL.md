---
name: zenith-sensitivity-analysis
description: Sensitivity analysis — tornado, spider, what-if, two-way sensitivity. Triggers em "sensitivity analysis", "tornado", "what-if analysis", "two-way sensitivity", "data table Excel".
license: SEE-LICENSE
parent_agent: zenith-director
---

# ZENITH-SENSITIVITY-ANALYSIS

## Quando usar
- Financial model robustness check
- M&A valuation (what drives NPV?)
- Capital project decision
- Pricing change impact
- Budget assumptions stress test

## Métodos
- **One-way (Tornado):** vary 1 variable, hold others. Rank by impact
- **Two-way (data table):** 2 variables, matrix output
- **Spider chart:** multiple variables at % change
- **Scenario analysis:** discrete combinations (best/base/worst)
- **Monte Carlo:** probabilistic (see zenith-monte-carlo)

## Templates
1. Tornado chart template (Excel data table + waterfall)
2. Two-way sensitivity (NPV × discount rate × growth)
3. Spider chart (multiple drivers ±20%)
4. Scenario summary table (best/base/worst)
5. Decision criteria sob incerteza (NPV mean + std)

## Princípios
- **Identify what matters:** focus em high-impact variables
- **Realistic ranges:** ±10/20/30% baseado em historical
- **Document assumptions:** cada variable + source
- **Pair com Monte Carlo:** sensitivity = qualitative; MC = probabilistic

## Cross-references
- [[zenith-monte-carlo]] · [[zenith-ma-evaluation]] · [[zenith-capital-allocation]]
