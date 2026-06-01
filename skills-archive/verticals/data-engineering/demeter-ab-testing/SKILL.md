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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **demeter-ab-testing** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in demeter-ab-testing:**

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
