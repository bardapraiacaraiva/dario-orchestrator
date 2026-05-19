---
name: lex-trabalhista
description: Direito do Trabalho Brasileiro. CLT, Reforma 13.467/17, Justiça do Trabalho, Súmulas TST. Reclamações, defesas, recursos, cálculos trabalhistas. Triggers em "trabalhista", "CLT", "reclamação trabalhista", "demissão", "FGTS", "horas extras", "rescisão", "justa causa", "TST", "Justiça do Trabalho", "vínculo empregatício", "estabilidade".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, audit_oab]
legislation_primary:
  - "CLT (Decreto-Lei 5.452/43)"
  - "Lei 13.467/17 (Reforma Trabalhista)"
  - "Lei 8.213/91 (Acidente de Trabalho / Estabilidade)"
  - "Lei 11.340/06 (Maria da Penha — assédio)"
  - "Súmulas TST (mais de 470)"
  - "OJ SDI-1 e SDI-2 TST"
  - "Acórdãos vinculantes TST"
templates_count: 40
priority: critical_volume
---

# LEX-TRABALHISTA — Direito do Trabalho

Skill mais usada em escritórios brasileiros (volume alto). Cobre reclamações, defesas, cálculos, recursos.

## Quando usar
- Redação de reclamações trabalhistas (empregado)
- Defesas/contestações (empresa)
- Cálculos trabalhistas (rescisão, horas extras, adicionais)
- Análise de rescisão (justa causa, sem justa causa, indireta)
- Estabilidade (gestante, dirigente sindical, acidente — art. 118 Lei 8.213/91)
- Assédio moral/sexual
- Equiparação salarial (art. 461 CLT)
- Acordo coletivo / convenção coletiva
- Compliance trabalhista (eSocial, FGTS, INSS)
- Recursos (ordinário, revisão, embargos)
- Súmulas TST aplicáveis

## Templates (40)

### Reclamações (empregado) (10)
1. Reclamação inicial — verbas rescisórias
2. Reclamação — danos morais (assédio)
3. Reclamação — equiparação salarial
4. Reclamação — horas extras + adicional noturno
5. Reclamação — desvio de função
6. Reclamação — acidente de trabalho + estabilidade
7. Reclamação — rescisão indireta (art. 483 CLT)
8. Reclamação — terceirização ilícita
9. Reclamação — grupo econômico (responsabilidade solidária)
10. Reclamação — fraude na contratação

### Defesas (empresa) (10)
11. Contestação genérica
12. Defesa — alegando justa causa (art. 482 CLT)
13. Defesa — negativa de vínculo (PJ / autônomo)
14. Defesa — prescrição (bienal + quinquenal)
15. Defesa — pejotização legítima (Lei 11.196/05)
16. Defesa em ação de equiparação salarial
17. Defesa em ação de horas extras
18. Defesa — terceirização lícita (Lei 13.429/17)
19. Defesa em ação de assédio
20. Resposta a embargos de declaração

### Cálculos (8)
21. Cálculo rescisão (sem justa causa)
22. Cálculo rescisão indireta
23. Cálculo horas extras (50%/100%)
24. Cálculo adicional noturno (20%) + insalubridade/periculosidade
25. Cálculo equiparação salarial
26. Cálculo FGTS atrasado + multa 40%
27. Cálculo verbas trabalhistas estabilidade acidentária
28. Cálculo honorários sucumbenciais (art. 791-A CLT pós-reforma)

### Recursos (6)
29. Recurso ordinário (TRT)
30. Recurso de revista (TST)
31. Embargos de declaração
32. Agravo de instrumento
33. Recurso extraordinário (com modulação)
34. Embargos infringentes

### Documentos administrativos (6)
35. Carta de aviso prévio (empregado)
36. Carta de demissão por justa causa (empresa)
37. Acordo de rescisão (art. 484-A CLT)
38. Termo de rescisão (TRCT)
39. Política interna anti-assédio
40. Programa de compliance trabalhista

## Súmulas TST relevantes (auto-aplicadas)
- **Súmula 90 TST:** horas in itinere
- **Súmula 244 TST:** estabilidade gestante
- **Súmula 277 TST:** convenções coletivas (incorporação)
- **Súmula 331 TST:** terceirização e responsabilidade subsidiária
- **Súmula 363 TST:** contratação irregular pela Administração
- **Súmula 437 TST:** intervalo intrajornada

## Reforma Trabalhista (Lei 13.467/17) — checks automáticos
- Negociado sobre legislado (CC art. 611-A)
- Banco de horas individual (art. 59)
- Trabalho intermitente (art. 452-A)
- Demissão por acordo (art. 484-A — 50% multa)
- Honorários sucumbenciais (art. 791-A)
- Justa causa por estádio público (art. 482 m)

## Limitações
- **Jurisprudência específica de TRTs** requer mcp-jusbrasil (planned)
- **Cálculos complexos com correção monetária** requerem inputs precisos (TR, IPCA-E, SELIC)
- **Tabelas de honorários OAB** variam por região — confirmar antes de release

## Cross-references
- [[lex-litigation]] — para peças genéricas processuais civis
- [[lex-civil]] — para questões civis em paralelo (danos morais)
- [[lex-lgpd]] — para dados de empregados (LGPD trabalhista)
