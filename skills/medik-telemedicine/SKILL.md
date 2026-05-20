---
name: medik-telemedicine
description: Telemedicina BR — CFM 2.314/2022, ANVISA RDC SaMD, prescrição digital, teleconsulta. Triggers em "telemedicina", "teleconsulta", "telessaúde", "CFM 2314", "prescrição digital", "Memed", "Doctoralia".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [cfm_205_2021_gate, lgpd_healthcare_marker, zdr_healthcare]
jurisdiction: Brasil
---

# MEDIK-TELEMEDICINE

## Marco
- **Resolução CFM 2.314/2022** — Define telemedicina (define modalidades + requisitos)
- **Lei 13.989/2020** — Autoriza telemedicina (durante pandemia, prorrogada)
- **Lei 14.510/2022** — Telemedicina permanente
- **RDC ANVISA 751/2022** — Software como dispositivo médico

## Modalidades CFM 2.314
1. **Teleconsulta** — médico ↔ paciente
2. **Teleinterconsulta** — médico ↔ médico
3. **Telediagnóstico** — análise de exames remoto
4. **Telecirurgia** — robótica
5. **Telemonitoramento** — wearables, monitoramento crônico
6. **Tele-orientação** — triagem

## Requisitos
- Identificação inequívoca de paciente e médico
- Consentimento livre e esclarecido
- Prontuário eletrônico
- Padrões mínimos de qualidade técnica
- Sigilo e segurança da informação
- Receita digital (ICP-Brasil ou validação CRM)

## Templates
1. Termo de consentimento teleconsulta
2. Compliance checklist plataforma telemedicina
3. Workflow prescrição digital ICP-Brasil
4. Auditoria de plataforma (Doctoralia/Memed integration)
5. Disaster recovery (consulta interrompida)

## Cross-references
- [[medik-cfm-resolutions]] · [[medik-lgpd-healthcare]] · [[medik-emr-integration]]
