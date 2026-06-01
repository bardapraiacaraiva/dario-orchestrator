---
name: aegis-security-awareness
description: Security awareness — phishing simulation, training, culture, KnowBe4, Hoxhunt. Triggers em "security awareness", "phishing simulation", "KnowBe4", "Hoxhunt", "security training", "human firewall".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, audit_trail]
---

# AEGIS-SECURITY-AWARENESS

## Filosofia
**Human is not the weakest link — humans are the firewall when trained right.**

## Quando usar
- Phishing program from scratch
- Annual awareness training compliance
- Post-incident reinforcement
- Culture transformation (security-first mindset)
- Specific high-risk role training (devs, finance, exec)

## Stack
- **KnowBe4** — líder enterprise
- **Hoxhunt** — gamified
- **Cofense** — phishing-focused
- **Infosec IQ**
- **Wizer** (free tier)
- **PhishMe** (legacy)

## Programa structure
- **Baseline phishing test** (pre-training)
- **Foundation training** (all hands, annual)
- **Role-based training** (devs SecCode, finance BEC, exec whaling)
- **Continuous phishing** (monthly, escalating difficulty)
- **Just-in-time** (after click → micro-lesson)
- **Champions program** (security ambassadors per dept)

## Templates
1. Phishing program design (12-month cadence)
2. Training content map (by role + risk)
3. Phishing simulation difficulty tiers (1-5)
4. Reporting dashboard (click rate + report rate trend)
5. Champions program SOP

## Métricas
- **Click rate trend** (target: declining)
- **Report rate** (target: >25%)
- **Time to report** (faster = better)
- **Repeat clickers** (escalation needed)

## Cross-references
- [[aegis-incident-response]] · [[pessoa-engagement]] · [[risco-etica]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-security-awareness** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-security-awareness:**

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
