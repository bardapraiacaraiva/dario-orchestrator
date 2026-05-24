---
name: mercurius-prospecting
description: Outbound prospecting — cold email, LinkedIn, calls, sequences, ICP, intent data. Triggers em "prospecting", "cold outbound", "cold email", "LinkedIn outreach", "ICP", "intent data", "sequences", "Apollo", "Outreach".
license: MIT
parent_agent: mercurius-director
compliance: [no_dark_patterns, lgpd_lead_data]
---

# MERCURIUS-PROSPECTING

## Quando usar
- SDR program greenfield
- ICP (Ideal Customer Profile) refinement
- Cold email sequence design
- LinkedIn outreach playbook
- Intent data integration (6sense, Bombora)

## Channels mix recomendado
- **Cold email:** 50% volume (low cost, scalable)
- **LinkedIn (DM + InMail):** 25% (warmer, B2B)
- **Cold call:** 15% (high touch, mid-market+)
- **Video (Loom, Vidyard):** 10% (differentiation)

## ICP framework
- Firmographic (industry, size, geo, tech stack)
- Demographic (role, seniority, tenure)
- Behavioral (intent signals, engagement)
- Pain triggers (funding event, leadership change, regulatory)

## Cold email anatomy (5-7 sentence rule)
1. Personalization line (research-based)
2. Problem hypothesis
3. Social proof (similar customer outcome)
4. CTA soft (yes/no question, not meeting)
5. Sign-off

## Stack
- **Apollo, ZoomInfo, Cognism** — data + automation
- **Outreach, Salesloft** — sequences (Tier 1)
- **Lemlist, Mailshake** — SMB-friendly
- **Bombora, 6sense** — intent data
- **Clay** — workflow automation prospecting

## Templates
1. ICP definition canvas (3 personas + segments)
2. Cold email sequence 5-touch (E1 problem, E2 social, E3 break-up)
3. LinkedIn 4-step sequence (connect + value + ask + bump)
4. Cold call opener scripts (10 variations)
5. Multi-channel orchestration playbook
6. Deliverability checklist (SPF/DKIM/DMARC)

## Compliance
- LGPD: ROPA para lead database
- GDPR: opt-out facilitado, basis legítimo interesse
- CAN-SPAM (US) + CASL (Canada) requirements

## Cross-references
- [[mercurius-sales-methodology]] · [[mercurius-discovery-call]] · [[orion-jobs-to-be-done]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-prospecting** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-prospecting:**

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
