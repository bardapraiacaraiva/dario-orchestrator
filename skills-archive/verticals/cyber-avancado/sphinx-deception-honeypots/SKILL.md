---
name: sphinx-deception-honeypots
description: Deception tech — Cymmetria, TrapX, honeypots, honeynets, canary tokens. Triggers em "deception tech", "honeypot", "honeynet", "Cymmetria", "TrapX", "canary tokens", "Thinkst Canary", "deception-based defense".
license: SEE-LICENSE
parent_agent: sphinx-director
---

# SPHINX-DECEPTION-HONEYPOTS

## Conceito
**Inverter advantage attacker.** Deception cria ambiente onde QUALQUER interação = high-confidence detection.

## Tipos
- **Low-interaction honeypots:** simulate services (Cowrie, Dionaea)
- **High-interaction honeypots:** real systems isolated (HoneyDrive)
- **Honeyfiles:** decoy documents (alert on access)
- **Honey credentials:** fake admin accounts
- **Canary tokens:** files/URLs/emails that beacon
- **Deception platforms (enterprise):** Cymmetria, TrapX, Illusive

## Stack
- **Thinkst Canary** — best UX, easy deploy
- **Illusive Networks** — enterprise líder
- **Acalvio ShadowPlex**
- **TrapX (now Commvault):** enterprise
- **Open-source:** T-Pot, OpenCanary, honeyd

## Use cases
- Lateral movement detection
- Insider threat
- Ransomware early warning
- Credential theft detection
- APT campaign detection

## Templates
1. Deception strategy design
2. Canary placement (network + endpoint + email)
3. Alert triage workflow
4. Deception vs production maintenance
5. Honey credential injection
6. Honeyfile content engineering

## Cross-references
- [[sphinx-advanced-persistent-threat]] · [[aegis-soc-operations]] · [[aegis-threat-modeling]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **sphinx-deception-honeypots** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in sphinx-deception-honeypots:**

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
