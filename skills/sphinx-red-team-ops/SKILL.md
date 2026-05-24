---
name: sphinx-red-team-ops
description: Red team continuous engagement, adversary emulation, objective-based. Triggers em "red team", "adversary emulation", "purple team", "objective-based engagement", "TIBER-EU", "CREST CRT".
license: SEE-LICENSE
parent_agent: sphinx-director
compliance: [responsible_disclosure, audit_immutable, classified_handling]
---

# SPHINX-RED-TEAM-OPS

## Red team vs pentest
- **Pentest:** find vulnerabilities (breadth)
- **Red team:** test detection + response (depth, stealth)
- **Purple team:** red + blue together, real-time learning

## Frameworks
- **TIBER-EU (DORA):** Threat Intelligence-Based Ethical Red-teaming
- **CBEST (UK)** — Bank of England framework
- **iCAST (HK)** — Hong Kong Monetary Authority
- **CORIE (AU)** — Australia
- **MITRE ATT&CK** — TTPs reference
- **MITRE ATT&CK Evaluations** — vendor comparison

## Engagement structure
```
1. Threat Intelligence (per TIBER) — define realistic adversary
2. Scoping + RoE (Rules of Engagement) signed
3. White cell (organization aware) defined
4. Test execution (6-12 weeks typical)
5. Replay + Purple team workshops
6. Detection improvements implemented
7. Report (sanitized + technical)
```

## Templates
1. TIBER-EU scoping document
2. RoE template (legal-cleared)
3. White cell SOP
4. Replay workshop facilitation
5. Detection engineering output
6. Executive briefing post-engagement

## Cross-references
- [[sphinx-threat-intel-platforms]] · [[aegis-breach-simulation]] · [[sphinx-advanced-persistent-threat]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **sphinx-red-team-ops** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in sphinx-red-team-ops:**

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
