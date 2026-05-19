---
name: lex-tributario
description: Direito Tributário Brasileiro. CTN, EC 132/2023 (Reforma Tributária CBS+IBS), defesas fiscais, planejamento tributário, contencioso administrativo (CARF) e judicial (STF/STJ). Triggers em "tributário", "impostos", "IRPJ", "ICMS", "ISS", "PIS/COFINS", "Reforma Tributária", "CBS", "IBS", "CARF", "execução fiscal", "imunidade", "planejamento tributário".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, privilege_marker, audit_oab]
legislation_primary:
  - "CTN (Lei 5.172/66)"
  - "EC 132/2023 (Reforma Tributária)"
  - "LC 87/96 (ICMS — Lei Kandir)"
  - "LC 116/03 (ISS)"
  - "Lei 9.430/96 (IRPJ)"
  - "Lei 10.637/02 + 10.833/03 (PIS/COFINS)"
templates_count: 30
security_tier: 2
---

# LEX-TRIBUTARIO — Direito Tributário

Cobre tributos federais, estaduais e municipais. Reforma Tributária (EC 132/2023) é foco actual.

## Quando usar
- Defesas fiscais administrativas (Delegacias da Receita, CARF)
- Defesas judiciais (Execuções fiscais, Ações de repetição)
- Planejamento tributário (legal — não elisão fiscal abusiva)
- Análise EC 132/2023 (transição CBS + IBS 2026-2033)
- Imunidades constitucionais
- Pareceres sobre incidência de tributos
- Compliance fiscal (SPED, eCAC, NFe)
- Recursos administrativos (DRJ, CARF, CSRF)
- Recursos judiciais tributários (STF/STJ)

## Templates (30)

### Defesa administrativa (8)
1. Impugnação ao Auto de Infração (RFB)
2. Recurso voluntário ao CARF
3. Embargos de declaração CARF
4. Recurso especial CSRF
5. Manifestação inconformidade — compensação não-homologada
6. Pedido de revisão de débito (PER/DComp)
7. Pedido de habilitação de crédito
8. Resposta a intimação fiscal

### Contencioso judicial (10)
9. Mandado de segurança preventivo (impedir lançamento)
10. Mandado de segurança repressivo (suspender exigibilidade)
11. Ação anulatória de lançamento
12. Ação de repetição de indébito
13. Ação declaratória de inexistência relação tributária
14. Embargos à execução fiscal
15. Exceção de pré-executividade
16. Recurso especial ao STJ (tributário)
17. Recurso extraordinário ao STF
18. Ação Direta de Inconstitucionalidade (matéria tributária)

### Pareceres & análises (7)
19. Parecer sobre incidência ICMS
20. Parecer sobre PIS/COFINS regime cumulativo vs não-cumulativo
21. Parecer ISS (local do serviço)
22. Parecer ITBI vs ITCMD
23. Parecer imunidade constitucional
24. Análise impacto Reforma Tributária por setor
25. Planejamento sucessório tributário

### Documentos compliance (5)
26. Checklist obrigações acessórias mensais
27. Política de governança fiscal
28. Programa de compliance fiscal corporativo
29. Manual eSocial + EFD-Reinf
30. Plano de transição EC 132/2023 (2026-2033)

## Reforma Tributária (EC 132/2023) — Transição
- **CBS (Contribuição sobre Bens e Serviços):** Federal — substitui PIS+COFINS
- **IBS (Imposto sobre Bens e Serviços):** Estadual + Municipal — substitui ICMS+ISS
- **Cronograma:** 2026 (teste 0,9% CBS / 0,1% IBS) → 2027 extinção PIS/COFINS → 2029-2032 redução ICMS/ISS → 2033 vigência plena
- **Crédito amplo:** princípio da não-cumulatividade plena
- **Cashback:** restituição automática para baixa renda
- **Imposto Seletivo:** "imposto do pecado" (cigarros, bebidas alcoólicas, etc.)

## Jurisprudência crítica (auto-aplicada)
- **Tema 69 STF:** ICMS na base de cálculo do PIS/COFINS (exclusão)
- **Tema 1.118 STF:** Reforma Tributária — modulações
- **Súmula Vinculante 8:** prescrição/decadência em contribuições previdenciárias
- **Súmula 436 STJ:** entrega da DCTF constitui o crédito (sem auto de infração)

## Compliance crítico
- Outputs sobre **planejamento tributário** → privilege marker AUTO (estratégia confidencial)
- Outputs com **valores tributários** → ZDR obrigatório
- Toda peça com **número de processo administrativo CARF** → audit log obrigatório

## Cross-references
- [[lex-corporate]] — operações M&A com impacto fiscal
- [[lex-administrativo]] — processo administrativo (Lei 9.784/99)
- [[lex-litigation]] — peças processuais civis tributárias
