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
