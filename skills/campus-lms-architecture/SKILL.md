---
name: campus-lms-architecture
description: LMS architecture — Moodle, Canvas, Open edX, Google Classroom, Brightspace. Triggers em "LMS", "Moodle", "Canvas", "Open edX", "Google Classroom", "Brightspace", "Blackboard".
license: SEE-LICENSE
parent_agent: campus-director
compliance: [lgpd_education_marker, audit_trail]
---

# CAMPUS-LMS-ARCHITECTURE

## Quando usar
- LMS selection (greenfield ou migration)
- LMS performance tuning (Moodle slow)
- LTI integration (LMS ↔ tools)
- Multi-tenant LMS for EAD provider
- SSO + identity federation

## Stack landscape
- **Moodle** (open-source #1, PHP)
- **Canvas (Instructure)** (PaaS, US líder)
- **Open edX** (open-source, edX-derived)
- **Google Classroom** (free, K-12-focused)
- **Brightspace (D2L)** (enterprise EAD)
- **Blackboard** (legacy enterprise)
- **TalentLMS / LearnWorlds** (cursos corporativos/coaches)

## Integração
- **LTI 1.3 (IMS Global):** tools embedded em LMS
- **SCORM:** course package portable
- **xAPI:** event-level tracking
- **CC (Common Cartridge):** import/export

## Templates
1. LMS selection scorecard (features × cost × scale)
2. Moodle production deploy (Docker + reverse proxy + Redis cache)
3. LTI 1.3 tool integration
4. SSO via SAML2/OIDC
5. Migration plan (Moodle → Canvas com SCORM export)

## Cross-references
- [[campus-ead-regulation]] · [[campus-education-analytics]] · [[nexus-cloud]]
