---
name: lex-lgpd
description: LGPD (Lei 13.709/18) e proteção de dados pessoais. RIPD, DPO, contratos com LGPD, política de privacidade, DPA, DSR, sanções ANPD. Comparativo GDPR. Triggers em "LGPD", "proteção de dados", "DPO", "ANPD", "DSR", "RIPD", "privacy by design", "consent", "DPA", "vazamento de dados", "incidente de segurança".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, audit_oab]
legislation_primary:
  - "Lei 13.709/18 (LGPD)"
  - "Resoluções ANPD (CD/ANPD)"
  - "Decreto 11.246/22 (regulamentação)"
  - "GDPR EU 2016/679 (comparativo)"
  - "Marco Civil da Internet (Lei 12.965/14)"
templates_count: 15
priority: critical_demand
---

# LEX-LGPD — Proteção de Dados

Skill de alta procura (LGPD + ANPD activos desde 2020+sancoes desde 2023).

## Quando usar
- Implementação programa LGPD (do zero)
- RIPD (Relatório de Impacto à Proteção de Dados)
- Política de privacidade externa + interna
- DPA (Data Processing Agreement) controlador-operador
- Resposta a DSR (Data Subject Request) — direitos titular (art. 18 LGPD)
- Resposta a incidentes (vazamento, ransomware) — notificação ANPD
- Defesa em processos administrativos ANPD
- Compliance setorial LGPD (saúde, financeiro, marketing)
- Análise transferência internacional de dados
- Programa de Privacy by Design / Default

## Templates (15)

### Documentos foundation (5)
1. Política de privacidade externa (site/app)
2. Política de privacidade interna (funcionários)
3. Termo de consentimento (LGPD-compliant)
4. Aviso de cookies (banner + central de preferências)
5. Aviso de privacidade colaboradores (RH)

### Operacional LGPD (5)
6. RIPD completo (Relatório de Impacto)
7. DPA controlador → operador
8. DPA controlador → controlador (compartilhamento)
9. Política de retenção e descarte
10. Procedimento de incidente de segurança + notificação ANPD

### DSR responses (3)
11. Resposta DSR — acesso (art. 18, II)
12. Resposta DSR — exclusão (art. 18, VI)
13. Resposta DSR — portabilidade (art. 18, V)

### Defesa ANPD (2)
14. Defesa administrativa ANPD
15. Recurso administrativo ANPD

## Direitos do titular (art. 18 LGPD — prazo 15 dias)
1. Confirmação de tratamento
2. Acesso
3. Correção
4. Anonimização/bloqueio/eliminação de dados desnecessários
5. Portabilidade
6. Eliminação
7. Informação sobre compartilhamento
8. Informação sobre não consentir
9. Revogação do consentimento

## Sanções ANPD (escala progressiva)
1. Advertência
2. Multa simples (até 2% do faturamento, limite R$ 50 milhões/infração)
3. Multa diária
4. Publicização da infração
5. Bloqueio dos dados
6. Eliminação dos dados
7. Suspensão parcial do banco de dados (6 meses, prorrogável)
8. Suspensão do tratamento
9. Proibição parcial ou total

## Bases legais (art. 7º LGPD)
1. Consentimento (I)
2. Cumprimento de obrigação legal (II)
3. Execução de políticas públicas (III)
4. Estudos por órgãos de pesquisa (IV)
5. **Execução de contrato (V)** — base comum em escritórios
6. Tutela da saúde (VIII)
7. **Legítimo interesse (IX)** — segunda base mais comum
8. Proteção do crédito (X)

## Compliance específico
- Outputs com **dados pessoais identificáveis** → ZDR active obrigatório
- **Vazamento de dados:** notificação ANPD em "prazo razoável" (interpretação atual: 48-72h)
- **Crianças/adolescentes:** consentimento específico dos pais (art. 14)
- **Dados sensíveis** (origem racial, religião, saúde, biometria, etc.): base legal específica (art. 11)

## Cross-references
- [[lex-corporate]] — DPA em M&A
- [[lex-commercial]] — cláusulas LGPD em contratos B2B
- [[lex-trabalhista]] — dados de empregados (LGPD em RH)
- [[lex-consumidor]] — interface LGPD + CDC
- [[lex-criminal]] — incidentes que configuram crime cibernético
