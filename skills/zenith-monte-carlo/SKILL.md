---
name: zenith-monte-carlo
description: Monte Carlo simulation — probabilistic risk, NPV distribution, project risk. @RISK, Crystal Ball, Python. Triggers em "Monte Carlo", "simulation", "probabilistic", "Latin Hypercube", "@RISK", "Crystal Ball".
license: SEE-LICENSE
parent_agent: zenith-director
---

# ZENITH-MONTE-CARLO

## Quando usar
- NPV distribution (não point estimate)
- Project risk analysis
- Insurance pricing (actuarial)
- Construction cost contingency
- Capital allocation sob incerteza

## Stack
- **@RISK (Palisade)** — líder Excel add-in
- **Crystal Ball (Oracle)** — alternative
- **Python:** NumPy + SciPy + Pyro (probabilistic programming)
- **R:** mc2d, fitdistrplus
- **Custom Excel** (com RAND() functions)

## Workflow
```
1. Define input distributions (triangular, normal, lognormal, beta)
2. Define output formula (e.g., NPV = f(inputs))
3. Run N simulations (10,000+ typical)
4. Analyze output distribution (mean, std, P10/P50/P90)
5. Sensitivity (which input drives output variance?)
6. Decision under uncertainty
```

## Templates
1. NPV Monte Carlo model (5y projection)
2. Construction cost contingency (10/50/90)
3. Project schedule risk (3-point estimate + MC)
4. Portfolio Monte Carlo (correlated risks)
5. Decision tree + MC hybrid

## Cross-references
- [[zenith-sensitivity-analysis]] · [[zenith-decision-intelligence]] · [[zenith-risk-assessment]]
