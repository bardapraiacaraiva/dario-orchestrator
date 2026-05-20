---
name: nomos-rgpd-pt-marker
description: RGPD Portugal — Regulamento (UE) 2016/679 + Lei 58/2019 + CNPD orientações. Triggers em "RGPD", "GDPR", "Lei 58/2019", "CNPD", "DPO Portugal", "direitos titulares".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [cnpd_consultation_marker, audit_immutable]
jurisdiction: Portugal + EU
---

# NOMOS-RGPD-PT-MARKER

## Marco
- **Regulamento (UE) 2016/679 (RGPD)** — directamente aplicável
- **Lei 58/2019** — execução RGPD em Portugal (DPO, IDs, sanções)
- **Lei 41/2004** — privacidade comunicações electrónicas
- **CNPD orientações** — pareceres + decisões CNPD
- **Lei 27/2024** — vigilância electrónica
- **EU AI Act 2024/1689** — convergence com RGPD Art. 22 (decisão automatizada)

## Quando usar
- Setup DPO (Data Protection Officer) — obrigatório se >250 employees ou high-risk
- AIPD (Avaliação Impacto Proteção Dados) — high-risk processing
- Comunicação CNPD (incidente ≤ 72h)
- DSR (Direitos titulares) workflow
- Transferências internacionais (EU-US Data Privacy Framework)
- CCTV / vigilância electrónica

## Diferenças PT vs BR
- **Regulator:** CNPD PT vs ANPD BR
- **Lei base:** Lei 58/2019 PT vs Lei 13.709/18 BR
- **DPO:** obrigatório critérios diferentes
- **Sanções:** até 4% revenue PT/EU; até 2% (R$ 50M cap) BR

## Templates
1. AIPD template (DPIA) PT
2. Política privacidade RGPD-aligned
3. DPA (Data Processing Agreement) Art. 28
4. ROPA (Record of Processing Activities) Art. 30
5. Incident response 72h CNPD
6. DSR (acesso/eliminação/portabilidade) workflow
7. Transferência internacional (SCC 2021)
8. CNPD consultation template (prévia)

## Compliance gates
- AIPD obrigatória para high-risk (biometria, geo-tracking, scoring)
- DPO designação > 250 employees
- ROPA mandatory > 250 employees
- Breach notification ≤ 72h CNPD + ≤ "sem demora indevida" titulares

## Cross-references
- [[nomos-cnpd-consultation]] · [[lex-lgpd]] · [[medik-lgpd-healthcare]] · [[risco-rgpd]]
