---
name: lex-familia
description: Direito de Família e Sucessões Brasileiro. CC livro IV, Lei do Divórcio, alimentos, guarda, união estável, partilha, inventários. Triggers em "divórcio", "guarda", "alimentos", "partilha", "inventário", "união estável", "pensão alimentícia", "casamento", "regime de bens", "tutela", "curatela".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, privilege_marker, audit_oab]
legislation_primary:
  - "CC livro IV (Família, arts. 1.511-1.783)"
  - "CC livro V (Sucessões, arts. 1.784-2.027)"
  - "Lei 5.478/68 (Alimentos)"
  - "Lei 11.340/06 (Maria da Penha)"
  - "Lei 13.058/14 (Guarda Compartilhada)"
templates_count: 20
security_tier: 2
---

# LEX-FAMILIA — Família e Sucessões

Skill com alta sensibilidade — outputs frequentemente privilege marked.

## Quando usar
- Divórcio (consensual ou litigioso)
- Partilha de bens (com ou sem filhos)
- Pensão alimentícia (fixação, revisão, exoneração)
- Guarda (unilateral, compartilhada, alternada)
- Reconhecimento/dissolução união estável
- Investigação de paternidade
- Adoção
- Tutela/curatela
- Violência doméstica (Maria da Penha)
- Inventário (judicial ou extrajudicial)
- Testamento (público, particular, cerrado)
- Planejamento sucessório (com [[lex-tributario]] para impactos fiscais)

## Templates (20)

### Divórcio & união (6)
1. PI — divórcio consensual com partilha
2. PI — divórcio litigioso
3. PI — dissolução de união estável
4. Escritura pública de divórcio (extrajudicial)
5. Pacto antenupcial
6. Contrato de namoro (delimitação união estável)

### Alimentos (4)
7. PI — alimentos provisórios + definitivos
8. PI — revisão de alimentos
9. PI — exoneração de alimentos
10. Execução de alimentos (com prisão civil)

### Guarda & filiação (4)
11. PI — guarda unilateral
12. PI — guarda compartilhada (preferencial Lei 13.058/14)
13. PI — investigação de paternidade
14. PI — adoção (consensual ou litigiosa)

### Sucessões (4)
15. PI — inventário judicial
16. Escritura pública de inventário extrajudicial
17. Testamento público
18. Sobrepartilha

### Outros (2)
19. Medida protetiva Maria da Penha
20. Pedido de interdição (curatela)

## Princípios aplicados
- **Melhor interesse da criança** (CDC + ECA)
- **Igualdade entre cônjuges** (art. 226 §5º CF)
- **Convivência familiar** (ECA)
- **Função social da família**
- **Reconhecimento da união estável** (art. 1.723 CC)

## Regimes de bens
- **Comunhão parcial** (default desde 1977)
- **Comunhão universal**
- **Separação total**
- **Separação obrigatória** (art. 1.641 CC — > 70 anos)
- **Participação final nos aquestos** (raro)

## Maria da Penha (Lei 11.340/06)
- Medidas protetivas (urgência)
- Suspensão de posse/guarda armas
- Distanciamento (mínimo varia)
- Acompanhamento policial (mudança de residência)

## Compliance específico
- **Casos de família** = privilege marker AUTO (sensibilidade alta)
- **Dados de menores** = ZDR obrigatório
- **Outputs envolvendo violência doméstica** = privilege + audit reforçado
- Termos como "vítima", "agressor" usados conforme proteção da privacidade

## Cross-references
- [[lex-civil]] — sucessões + CC livro IV/V
- [[lex-criminal]] — violência doméstica (interface com Lei Maria da Penha)
- [[lex-tributario]] — ITCMD em planejamento sucessório
- [[lex-imobiliario]] — partilha de imóveis
