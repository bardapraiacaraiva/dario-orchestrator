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
