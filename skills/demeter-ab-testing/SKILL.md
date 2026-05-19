---
name: demeter-ab-testing
description: A/B testing com rigor estatístico. Frequentist + Bayesian, multi-armed bandits, GrowthBook, Optimizely, sample size, power analysis. Triggers em "A/B test", "experiment", "split test", "multi-armed bandit", "Bayesian", "sample size", "statistical significance", "p-value", "GrowthBook".
license: MIT
parent_agent: demeter-director
compliance: [lgpd_by_design, ethics_in_experiments]
---

# DEMETER-AB-TESTING — Experiments com Rigor

## Filosofia
**Sem rigor estatístico, A/B testing é teatro.** Cada test precisa: hipótese clara, sample size pré-calculado, métrica primária definida, análise documentada.

## Quando usar
- Desenhar teste A/B (greenfield)
- Auditar testes existentes (sample size adequado? p-hacking?)
- Multi-armed bandit setup (CTR optimization)
- Setup GrowthBook / Optimizely / Google Optimize alternative
- Análise de testes terminados

## Stack
- **GrowthBook** (open-source, modern)
- **Optimizely** (enterprise)
- **VWO**
- **AB Tasty**
- **Statsig** (real-time analytics)
- **PostHog** (open-source product analytics)

## Princípios estatísticos
- **Power analysis ANTES do test:** sample size adequado p/ effect size mínimo
- **Métrica primária ÚNICA:** múltiplas métricas = multiple comparisons problem
- **Tempo mínimo:** 1-2 semanas (capturar weekly seasonality)
- **Don't peek:** análise final ao fim do período (early stopping inflaciona Type I)
- **CUPED:** variance reduction para tests mais sensíveis
- **Bayesian vs Frequentist:** Bayesian melhor para decision-making sob incerteza

## Templates
1. Test plan template (hipótese, métricas, sample size, duration)
2. Sample size calculator (Cohen's d, alpha, beta, baseline)
3. Análise frequentist (t-test, chi-square, Mann-Whitney)
4. Análise Bayesian (Beta-Binomial, posterior + credible interval)
5. Multi-armed bandit (Thompson Sampling, Epsilon-Greedy)
6. Post-mortem (was it stat-sig? was it practically significant? what to ship?)

## Métricas comuns
- **OEC (Overall Evaluation Criterion):** métrica primária do test
- **Guardrails:** métricas que NÃO podem piorar (revenue, error rate)
- **Secondary:** exploratórias (não decidem ship)

## Pitfalls a evitar
- ❌ Early stopping sem correção sequencial (Pocock / O'Brien-Fleming)
- ❌ Multiple comparisons sem Bonferroni / FDR
- ❌ Novelty effect confundido com lift real
- ❌ Sample ratio mismatch (SRM) não detectado
- ❌ Selection bias (test só para "engaged users")

## Cross-references
- [[demeter-event-tracking]] — exposure/conversion tracking
- [[demeter-cohort-analysis]] — segmentation
- [[demeter-data-storytelling]] — reportar resultados
