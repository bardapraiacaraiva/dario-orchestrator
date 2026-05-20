---
name: euterpe-cro-advanced
description: CRO advanced — multi-variate, personalization, sequential testing, MAB. Triggers em "CRO", "conversion rate optimization", "multi-variate testing", "MVT", "personalization", "Bayesian AB", "MAB", "multi armed bandit".
license: MIT
parent_agent: euterpe-director
compliance: [no_dark_patterns, audit_trail]
---

# EUTERPE-CRO-ADVANCED

## Test types
- **A/B test:** 1 variable, 2 variants
- **A/B/n test:** 1 variable, N variants
- **MVT (Multi-Variate Test):** N variables × M variants = N×M combinations
- **Sequential testing:** Bayesian, no peeking penalty
- **Multi-Armed Bandit (MAB):** Thompson sampling, auto-allocate
- **Contextual bandit:** + features (personalize)

## Frameworks
- **Bayesian over Frequentist:** smaller samples, no p-hacking
- **CUPED:** variance reduction (Microsoft) — 2x faster tests
- **Sequential probability ratio test (SPRT):** flexible stopping
- **Hierarchical Bayesian:** test multiple metrics jointly

## Stack
- **Optimizely** — enterprise líder
- **VWO** — alternative
- **Adobe Target** — enterprise
- **GrowthBook** — open-source modern
- **Convert.com, AB Tasty** — mid-market
- **Statsig** — real-time + product analytics
- **PostHog** — open-source product + AB

## Anti-patterns
- ❌ Sample size sub-calculation
- ❌ Peek-and-stop (frequentist)
- ❌ Multiple comparisons sem correção
- ❌ Trust 1 winner sem replication
- ❌ HiPPO override sem data

## Templates
1. CRO program governance
2. Test hypothesis library
3. Sample size calculator (Bayesian + Frequentist)
4. MVT design (factorial vs fractional)
5. Personalization rules engine
6. Test postmortem template

## Cross-references
- [[demeter-ab-testing]] · [[orion-product-analytics]] · [[euterpe-customer-data-platform]]
