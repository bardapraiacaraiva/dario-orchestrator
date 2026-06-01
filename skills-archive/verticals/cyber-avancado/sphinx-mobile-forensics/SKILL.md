---
name: sphinx-mobile-forensics
description: Mobile forensics — iOS/Android extraction, Cellebrite, Magnet AXIOM, Oxygen Forensic. Triggers em "mobile forensics", "iOS forensics", "Android forensics", "Cellebrite UFED", "Magnet AXIOM", "Oxygen Forensic", "GrayKey".
license: SEE-LICENSE
parent_agent: sphinx-director
compliance: [audit_immutable, classified_handling, responsible_disclosure]
---

# SPHINX-MOBILE-FORENSICS

## Extraction levels
- **Manual:** photo of screen
- **Logical:** file system via vendor protocol (iTunes-like)
- **File system:** root/jailbreak access
- **Physical:** bit-by-bit copy (chip-off, JTAG)
- **Cloud:** iCloud/Google Drive backups

## Stack
- **Cellebrite UFED** — líder LE/government
- **Magnet AXIOM** — competitive
- **Oxygen Forensic Detective** — cost-effective
- **GrayKey (Grayshift):** iOS specific unlock
- **MOBILedit Forensic** — affordable

## iOS challenges
- Secure Enclave + Touch ID/Face ID
- iOS 17/18 lockdown mode
- iCloud encrypted backups
- Recovery vs forensic data

## Android challenges
- Manufacturer variations (Samsung, Xiaomi)
- TrustZone (ARM)
- KeyMaster (hardware-backed crypto)
- File-based encryption (FBE)
- Verified boot

## Templates
1. Forensic acquisition SOP
2. Chain of custody mobile
3. iOS extraction workflow
4. Android extraction workflow
5. Report court-admissible
6. Anti-forensics detection

## Cross-references
- [[aegis-digital-forensics]] · [[sphinx-malware-analysis]] · [[lex-criminal]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **sphinx-mobile-forensics** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in sphinx-mobile-forensics:**

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
