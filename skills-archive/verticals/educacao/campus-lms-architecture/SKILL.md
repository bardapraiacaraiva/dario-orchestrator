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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **campus-lms-architecture** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in campus-lms-architecture:**

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
