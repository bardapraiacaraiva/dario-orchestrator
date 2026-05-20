---
name: nomos-acss-healthcare-pt
description: ACSS healthcare PT — Serviço Nacional Saúde, convenções, SNS digital, INFARMED prescription. Triggers em "ACSS", "SNS", "convencionado", "INFARMED", "Ordem dos Médicos PT", "medicamentos PT".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [cnpd_consultation_marker, audit_immutable]
jurisdiction: Portugal
---

# NOMOS-ACSS-HEALTHCARE-PT

## Marco
- **Lei 95/2019** — Lei de Bases da Saúde PT
- **DL 11/2017** — SNS digital
- **DL 113/2011** — ACSS attributions
- **DL 176/2006** — medicamentos uso humano
- **Despacho 2596/2025** — desburocratização
- **Lei 12/2005** — informação genética + saúde
- **Ordem dos Médicos** — Código Deontológico

## Quando usar
- Hospital privado convencionado SNS
- Clínica autorização ERS (Entidade Reguladora Saúde)
- Telemedicina PT (vs CFM 2.314 BR)
- e-Saúde / RSE (Registo Saúde Electrónico)
- Prescrição electrónica
- Farmácia hospitalar + ambulatório
- Ensaios clínicos INFARMED

## Templates
1. Convenção SNS application
2. Autorização ERS (regulator saúde)
3. Telemedicina PT compliance (DGS orientações)
4. e-Receita médica padrão SNS
5. Termo consentimento informado PT
6. Ensaio clínico INFARMED submission
7. Farmacovigilância notification

## Diferenças PT vs BR healthcare
- **Regulator:** ERS PT vs ANS BR
- **Single-payer:** SNS quase universal PT vs SUS+saúde suplementar BR
- **Compliance órgão:** Ordem dos Médicos PT vs CFM BR
- **Med billing:** SIIMA PT vs TUSS BR
- **e-Saúde:** RSE PT vs RNDS BR

## Cross-references
- [[nomos-rgpd-pt-marker]] · [[medik-cfm-resolutions]] · [[medik-emr-integration]]
