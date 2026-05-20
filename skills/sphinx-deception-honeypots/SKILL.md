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
