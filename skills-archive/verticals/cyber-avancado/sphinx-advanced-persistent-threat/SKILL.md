---
name: sphinx-advanced-persistent-threat
description: APT detection, TTPs, attribution, nation-state actors. Triggers em "APT", "advanced persistent threat", "nation-state", "Lazarus", "APT28", "APT29", "Cozy Bear", "Fancy Bear", "APT attribution".
license: SEE-LICENSE
parent_agent: sphinx-director
compliance: [audit_immutable, classified_handling]
---

# SPHINX-ADVANCED-PERSISTENT-THREAT

## APT groups conhecidos (top 10)
- **APT28 / Fancy Bear / Sofacy** (Russia GRU)
- **APT29 / Cozy Bear / The Dukes** (Russia SVR)
- **Lazarus Group / APT38** (North Korea)
- **APT40 / TEMP.Periscope** (China MSS)
- **APT41 / Double Dragon** (China — espionage + financial)
- **Equation Group** (NSA — Stuxnet attribution)
- **Charming Kitten / APT35** (Iran)
- **APT10 / menuPass** (China)
- **Sandworm** (Russia — NotPetya)
- **Turla** (Russia FSB)

## Attribution methodology
- **Diamond Model:** adversary / capability / infrastructure / victim
- **Pyramid of Pain (Bianco):** hash → IP → domain → tools → TTPs (top = hardest to change)
- **CTI graph analysis:** infrastructure reuse, code lineage
- **OPSEC failures:** language artifacts, time zones, mistakes
- **HUMINT corroboration:** intel sources

## Detection
- **Behavioral:** lateral movement patterns
- **TTP-based:** ATT&CK techniques tracked
- **Threat hunting:** hypothesis-driven
- **Long-dwell time:** APT median 200+ days (Mandiant)
- **YARA rules:** signature-based for samples

## Templates
1. APT threat model per industry
2. Threat hunting hypotheses library
3. Adversary emulation plans (per APT)
4. Attribution confidence framework
5. Strategic threat briefing template
6. ICS/OT APT special considerations

## Cross-references
- [[sphinx-threat-intel-platforms]] · [[sphinx-red-team-ops]] · [[aegis-soc-operations]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **sphinx-advanced-persistent-threat** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in sphinx-advanced-persistent-threat:**

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
