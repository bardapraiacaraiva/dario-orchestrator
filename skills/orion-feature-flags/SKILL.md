---
name: orion-feature-flags
description: Feature flags / progressive delivery — LaunchDarkly, GrowthBook, Unleash, Statsig. Canary, rollback, A/B integration. Triggers em "feature flag", "LaunchDarkly", "GrowthBook", "progressive delivery", "canary release".
license: MIT
parent_agent: orion-director
compliance: [data_privacy_by_design, feature_flag_audit]
---

# ORION-FEATURE-FLAGS

## Quando usar
- Setup feature flag system (greenfield)
- Migration de hardcoded toggles → managed system
- Trunk-based development sem long-running branches
- Safe deploys (deploy != release)
- A/B testing integration

## Stack
- **LaunchDarkly** (enterprise líder)
- **GrowthBook** (open-source, integra A/B)
- **Unleash** (open-source enterprise)
- **Statsig** (real-time + experimentation)
- **Flagsmith** (self-hostable)
- **ConfigCat** (developer-friendly, cheaper)

## Tipos de flag
- **Release flag:** dark launch + canary rollout (short-lived)
- **Experiment flag:** A/B testing (medium-lived)
- **Ops flag:** kill switch, circuit breaker (permanent)
- **Permission flag:** beta access, paid tier gating (permanent)

## Princípios
- **Lifecycle clear:** cada flag tem dono + remove date
- **Clean up religiously:** flags antigos = tech debt
- **Targeting rules versionadas:** audit trail
- **Default safe:** off por defeito quando em dúvida

## Templates
1. Feature flag governance doc (naming, lifecycle, ownership)
2. LaunchDarkly project setup (envs, segments, roles)
3. Canary rollout playbook (1% → 10% → 50% → 100%)
4. Flag cleanup audit script
5. Incident response: kill switch playbook

## Cross-references
- [[orion-product-launch]] · [[demeter-ab-testing]] · [[builder-ci-cd]]
