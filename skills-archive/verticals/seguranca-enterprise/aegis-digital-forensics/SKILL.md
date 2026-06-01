---
name: aegis-digital-forensics
description: Digital forensics — disk imaging, memory analysis, network forensics, mobile forensics. Triggers em "digital forensics", "FTK", "Autopsy", "Volatility", "memory forensics", "Wireshark forensics".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [audit_immutable, chain_of_custody]
---

# AEGIS-DIGITAL-FORENSICS

## Quando usar
- Post-breach investigation
- Insider threat investigation
- Legal hold + e-discovery
- Mobile forensics
- Cloud forensics

## Stack
- **Disk imaging:** FTK Imager, dd, dc3dd
- **Disk analysis:** Autopsy (open-source), FTK, EnCase, X-Ways
- **Memory:** Volatility 3, Rekall, MemProcFS
- **Network:** Wireshark, NetworkMiner, Zeek
- **Mobile:** Cellebrite, Magnet AXIOM
- **Cloud:** AWS GuardDuty + CloudTrail, Magnet AXIOM Cyber

## Princípios
- **Chain of custody mandatory**
- **Write-blockers** ao copiar disk
- **Hash everything** (MD5 + SHA-256 mínimo)
- **Documentation extensive** (cada step)
- **Trained personnel** (court-defensible)

## Templates
1. Chain of custody form
2. Forensic image acquisition SOP
3. Memory analysis playbook (Volatility + common artifacts)
4. Network forensics workflow (Zeek + logs)
5. Final report template (executive + technical + appendix)
6. Cloud forensics (AWS/Azure/GCP)

## Compliance
- ✓ Evidence court-admissible
- ✓ LGPD specific care (PII em evidence)
- ✓ ISO 27037 — Identification, collection, acquisition

## Cross-references
- [[aegis-incident-response]] · [[aegis-soc-operations]] · [[lex-criminal]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-digital-forensics** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-digital-forensics:**

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
