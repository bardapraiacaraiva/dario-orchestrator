---
name: sphinx-social-engineering-defense
description: Anti-social engineering — advanced phishing, vishing, smishing, BEC, deepfakes. Triggers em "social engineering defense", "advanced phishing", "vishing", "smishing", "BEC", "business email compromise", "deepfake detection".
license: SEE-LICENSE
parent_agent: sphinx-director
compliance: [audit_immutable]
---

# SPHINX-SOCIAL-ENGINEERING-DEFENSE

## Attack vectors
- **Phishing:** email-based
- **Spear phishing:** targeted individual
- **Whaling:** target executives
- **Vishing:** voice (phone)
- **Smishing:** SMS
- **BEC (Business Email Compromise):** CFO fraud, vendor fraud
- **Deepfake voice/video:** AI-generated impersonation
- **Pretexting:** elaborate scenarios

## Defensive layers
- **Technical:** DMARC, DKIM, SPF, sandboxing email
- **AI detection:** behavior anomaly (Abnormal Security, Tessian)
- **Training:** continuous + role-based
- **Process:** out-of-band verification for $$$ transfers
- **Insurance:** cyber + crime policies

## BEC defense
- **Email banner warning:** external sender
- **Wire transfer verification:** phone callback to known number
- **Vendor change verification:** out-of-band
- **CFO/CEO impersonation training**
- **Bait-and-switch detection** (similar domain)

## Templates
1. Anti-phishing program design
2. BEC playbook + financial controls
3. Deepfake awareness training
4. Vendor verification SOP
5. Executive threat protection
6. Incident response (post-compromise wire)

## Cross-references
- [[aegis-security-awareness]] · [[aegis-incident-response]] · [[sphinx-osint-investigations]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **sphinx-social-engineering-defense** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in sphinx-social-engineering-defense:**

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
