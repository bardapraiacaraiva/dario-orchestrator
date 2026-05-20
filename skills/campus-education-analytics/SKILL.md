---
name: campus-education-analytics
description: Learning analytics — engagement, completion, mastery, dropout prediction. xAPI, Caliper. Triggers em "learning analytics", "xAPI", "Caliper", "education analytics", "dropout prediction", "completion rate".
license: SEE-LICENSE
parent_agent: campus-director
compliance: [lgpd_education_marker, model_explainability]
---

# CAMPUS-EDUCATION-ANALYTICS

## Quando usar
- LMS sem dashboard analytics
- High dropout — identificar at-risk students cedo
- Personalização baseada em performance
- Reporting institucional (CPA, conselhos)
- A/B test de conteúdo educacional

## Stack
- **xAPI (Tin Can):** standard de tracking learning experiences
- **Caliper Analytics:** standard IMS Global
- **SCORM:** legacy, ainda em uso
- **Custom event tracking** (Mixpanel/Amplitude/PostHog)

## Métricas
- **Engagement:** time spent, logins/week, content interactions
- **Completion:** % módulos finalizados
- **Mastery:** assessment scores trend
- **Persistence:** retention week-over-week
- **Dropout risk:** ML-predicted

## Templates
1. xAPI/Caliper event taxonomy
2. Dropout prediction model (XGBoost + features behaviorais)
3. Personalization rules (struggling → easier; advancing → harder)
4. Executive dashboard (institutional level)
5. Student-facing dashboard (self-reflection)

## Compliance
- ✓ LGPD especial menores (consentimento responsável)
- ✓ Anonimização para benchmarks
- ✓ Direito à revisão decisão automatizada

## Cross-references
- [[campus-lms-architecture]] · [[demeter-predictive]] · [[demeter-cohort-analysis]]
