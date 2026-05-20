---
name: euterpe-mmm-modeling
description: Marketing Mix Modeling — Bayesian MMM, Robyn (Meta), LightweightMMM (Google). Triggers em "MMM", "Marketing Mix Modeling", "Robyn", "LightweightMMM", "Bayesian MMM", "media attribution", "carryover effects".
license: MIT
parent_agent: euterpe-director
compliance: [lgpd_marketing, audit_trail]
---

# EUTERPE-MMM-MODELING

## Quando usar
- Cookie deprecation forced (no more MTA)
- Multi-channel budget allocation
- Brand vs performance trade-off
- TV/OOH/Print + Digital combined
- Annual planning + ROI by channel

## Frameworks/tools
- **Robyn (Meta open-source):** R-based, Bayesian
- **LightweightMMM (Google):** Python, JAX
- **PyMC-Marketing:** modern Bayesian Python
- **Nielsen, Analytic Partners, Marketing Science:** enterprise consultancies
- **Recast, Lifesight:** modern SaaS MMM

## Conceitos chave
- **Adstock (carryover):** media decay function
- **Saturation:** diminishing returns (Hill/Michaelis-Menten)
- **Hierarchical Bayesian:** prior + posterior
- **Geo-experiments:** validate MMM with holdout
- **Calibration:** geo lift tests inform priors

## Outputs típicos
- Channel ROI/ROAS by spend level
- Optimal budget allocation
- Saturation curves per channel
- Carryover effects (TV: 4-8 weeks; digital: 1-2 weeks)
- Baseline vs incremental sales

## Templates
1. MMM data requirements (2y weekly minimum)
2. Robyn project setup (R + reticulate)
3. Calibration with geo-lift experiments
4. Budget optimization scenarios
5. MMM stakeholder presentation
6. Refresh cadence (quarterly + ad-hoc)

## Cross-references
- [[euterpe-attribution-multi-touch]] · [[demeter-ml-pipelines]] · [[zenith-monte-carlo]]
