---
name: medik-clinical-protocols
description: Protocolos clínicos — PCDT (Min. Saúde), guidelines internacionais, evidence-based medicine. Triggers em "protocolo clínico", "PCDT", "guideline", "evidence-based", "MBE", "diretrizes clínicas".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [cfm_205_2021_gate, privilege_clinical]
jurisdiction: Brasil
---

# MEDIK-CLINICAL-PROTOCOLS

## Quando usar
- Implementar PCDT no serviço (SUS-compatível)
- Criar protocolos internos clínica/hospital
- Auditoria de adesão a guidelines
- Adaptação de guideline internacional → contexto BR
- CDSS (Clinical Decision Support System) setup

## Fontes
- **PCDT Min. Saúde** — Protocolos Clínicos e Diretrizes Terapêuticas
- **CONITEC** — Comissão Nac. Incorporação Tecnologias SUS
- **UpToDate / DynaMed / BMJ Best Practice** — referência internacional
- **Sociedades médicas BR:** SBC, SBI, AMB, FBG, etc.
- **CMS Guidelines** (US), NICE (UK) — adaptação cuidadosa

## Templates
1. Protocolo institucional template (objetivo + escopo + população + intervenção + outcomes)
2. CDSS rule engine (drug-allergy, drug-drug, dose adjust)
3. Audit de adesão (% pacientes conforme protocolo)
4. Adaptação guideline internacional (cultural + epidemiológica + econômica)
5. Avaliação de tecnologia (ATS/HTA-style)

## Cross-references
- [[medik-clinical-decision-support]] · [[medik-emr-integration]] · [[medik-anvisa-regulatory]]
