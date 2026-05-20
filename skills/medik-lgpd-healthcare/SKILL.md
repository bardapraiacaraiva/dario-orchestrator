---
name: medik-lgpd-healthcare
description: LGPD para saúde — Art. 11 (dados sensíveis), Art. 13 (estudos), AIPD healthcare, DPO. Triggers em "LGPD saúde", "Art 11", "dado sensível saúde", "AIPD saúde", "DPO clínica".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [lgpd_healthcare_marker, zdr_healthcare]
jurisdiction: Brasil
---

# MEDIK-LGPD-HEALTHCARE

## Marco
- **Lei 13.709/2018 (LGPD)** Art. 11 — dados sensíveis (saúde)
- **Lei 13.709/2018** Art. 13 — pesquisa em saúde pública
- **Lei 13.709/2018** Art. 26 — uso compartilhado de dados pelo Poder Público
- **Resolução CFM 1.821/2007** — armazenamento prontuário
- **ANPD Resolução CD/ANPD 2/2022** — agentes pequeno porte

## Quando usar
- Setup DPO/LGPD em clínica (greenfield)
- AIPD para novo sistema (EMR, app paciente)
- Resposta a titular DSR (acesso/portabilidade/eliminação)
- Incidente de dados — comunicação ANPD + titulares
- Contrato compartilhamento dados (Operador-Controlador)

## Bases legais Art. 11 (dados sensíveis)
1. Consentimento específico
2. Tutela da saúde (preferida em emergência)
3. Estudos por órgão de pesquisa
4. Exercício regular de direitos
5. Proteção da vida
6. Cumprimento de obrigação legal

## Templates
1. AIPD healthcare template (15 seções)
2. Política de Privacidade pacientes
3. Contrato Operador-Controlador (clínica + EMR vendor)
4. DSR response workflow
5. Incident response playbook (72h ANPD)

## Compliance built-in
- ✓ Rodapé LGPD automático em outputs externos
- ✓ Anonimização (PCD ANPD) em datasets de pesquisa
- ✓ Logs de acesso prontuário (auditoria)

## Cross-references
- [[medik-emr-integration]] · [[lex-lgpd]] · [[risco-rgpd]]
