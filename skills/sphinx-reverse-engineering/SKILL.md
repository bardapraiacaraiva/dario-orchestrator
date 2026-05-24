---
name: sphinx-reverse-engineering
description: Binary RE — Ghidra, IDA Pro, Binary Ninja, anti-debugging, anti-VM. Triggers em "reverse engineering", "binary analysis", "Ghidra", "IDA Pro", "Binary Ninja", "Radare2", "decompile", "anti-debugging".
license: SEE-LICENSE
parent_agent: sphinx-director
compliance: [audit_immutable, responsible_disclosure]
---

# SPHINX-REVERSE-ENGINEERING

## Stack
- **IDA Pro (Hex-Rays)** — gold standard $$$
- **Ghidra (NSA, free)** — IDA Pro competitor
- **Binary Ninja** — modern mid-tier
- **Radare2 + Cutter** — open-source
- **x64dbg** — Windows debugger
- **GDB + pwndbg/gef** — Linux
- **Frida** — dynamic instrumentation
- **angr** — binary analysis framework

## Use cases
- Vulnerability research
- Malware analysis
- License bypass research (forensic/legal)
- Protocol analysis (proprietary)
- Firmware analysis (IoT, automotive)
- Game cheating analysis (anti-cheat research)

## Anti-RE techniques (need to bypass)
- **Anti-debugging:** IsDebuggerPresent, PEB checks
- **Anti-VM:** detect VMware, VirtualBox
- **Code obfuscation:** packers, virtualization
- **Anti-tampering:** code integrity checks
- **Time bombs:** detect analysis duration

## Templates
1. RE workflow per file type
2. Ghidra script library
3. IDA Python scripts
4. Anti-anti-debugging plugins
5. Firmware extraction (binwalk, etc.)
6. Decompilation cleanup methodology

## Cross-references
- [[sphinx-malware-analysis]] · [[aegis-pentest-methodology]] · [[sphinx-zero-day-management]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **sphinx-reverse-engineering** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in sphinx-reverse-engineering:**

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
