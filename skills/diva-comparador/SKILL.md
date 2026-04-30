---
name: diva-comparador
description: "Compare 2-3 contractor proposals side-by-side. Identifies price discrepancies, missing items, scope differences, payment terms, guarantees, and red flags. Recommends best value option with justification. Triggers on \"comparar propostas\", \"comparar orcamentos\", \"qual empreiteiro\", \"comparador\", \"analise propostas\", \"melhor proposta\", \"proposta mais barata\"."
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# DIVA Comparador — Contractor Proposal Analysis

Compare 2-3 contractor proposals systematically. Identify what's included, what's missing, price discrepancies, and red flags. Recommend best value (not just cheapest).

## When to activate

Invoke `/diva-comparador` when:
- User has 2-3 proposals from contractors and needs to decide
- User suspects one proposal is missing scope items
- User wants to negotiate informed by market comparison
- User asks "qual e a melhor proposta?"

## Workflow

### 1. Input the proposals
For each proposal, extract:
- Empreiteiro (nome, alvara, contacto)
- Valor total (sem IVA, com IVA)
- Prazo proposto
- Condicoes pagamento
- Garantias oferecidas
- Items incluidos (artigo a artigo se disponivel)
- Items EXCLUIDOS (cruciais — o que NAO esta incluido?)
- Condicoes especiais

### 2. Normalize for comparison
Convert all proposals to the same structure:
- Mesmo formato de capitulos (ProNIC)
- Mesmas unidades (m2, ml, un)
- Preco por m2 global
- IVA separado e verificado

### 3. Generate comparison matrix

```markdown
## Comparacao de Propostas — [Projecto]

### Resumo Executivo
| | Proposta A | Proposta B | Proposta C |
|---|---|---|---|
| **Empreiteiro** | | | |
| **Valor sem IVA** | EUR | EUR | EUR |
| **Valor com IVA** | EUR | EUR | EUR |
| **Preco/m2** | EUR | EUR | EUR |
| **Prazo (semanas)** | | | |
| **Inicio previsto** | | | |
| **Garantia geral** | | | |
| **Condicoes pagamento** | | | |
| **Alvara IMPIC** | | | |

### Breakdown por Capitulo
| Capitulo | Proposta A | Proposta B | Proposta C | Diferenca max |
|---|---|---|---|---|
| Demolicao | EUR | EUR | EUR | X% |
| Alvenaria | EUR | EUR | EUR | X% |
| Impermeabilizacao | EUR | EUR | EUR | X% |
| Electricidade | EUR | EUR | EUR | X% |
| Canalizacao | EUR | EUR | EUR | X% |
| AVAC | EUR | EUR | EUR | X% |
| Pavimentos | EUR | EUR | EUR | X% |
| Revestimentos | EUR | EUR | EUR | X% |
| Carpintaria | EUR | EUR | EUR | X% |
| Cozinha | EUR | EUR | EUR | X% |
| Pintura | EUR | EUR | EUR | X% |
| Sanitarios | EUR | EUR | EUR | X% |
| **TOTAL** | **EUR** | **EUR** | **EUR** | |

### Items CRITICOS em Falta
| Item | Proposta A | Proposta B | Proposta C |
|---|---|---|---|
| Impermeabilizacao WC | Incluido | **EM FALTA** | Incluido |
| Caixilharia | Incluido | Incluido | **EM FALTA** |
| Certificacao energetica | **EM FALTA** | **EM FALTA** | Incluido |
| Limpeza final | Incluido | **EM FALTA** | Incluido |

### Red Flags
| Flag | Proposta | Detalhe |
|---|---|---|
| Preco anormalmente baixo | B | -30% vs media — risco de trabalhos a mais |
| Sem alvara verificavel | C | Verificar em impic.pt |
| Prazo irrealista | A | 6 semanas para obra de 12 — impossivel |
| Sem detalhe por artigo | B | Preco global sem breakdown — nao permite controlo |

### Scoring
| Criterio (peso) | Proposta A | Proposta B | Proposta C |
|---|---|---|---|
| Preco (30%) | X/10 | X/10 | X/10 |
| Completude scope (25%) | X/10 | X/10 | X/10 |
| Prazo realista (15%) | X/10 | X/10 | X/10 |
| Garantias (10%) | X/10 | X/10 | X/10 |
| Condicoes pagamento (10%) | X/10 | X/10 | X/10 |
| Alvara + seguros (10%) | X/10 | X/10 | X/10 |
| **TOTAL PONDERADO** | **X/10** | **X/10** | **X/10** |

### Recomendacao
**Melhor valor:** Proposta [X]
**Justificacao:** [porque — nao e so o preco]
**Negociacao sugerida:** [pontos a negociar com o escolhido]
**Items a adicionar:** [scope em falta que deve ser incluido antes de assinar]
```

### 4. Red flag detection rules

| Sinal | Significado | Accao |
|---|---|---|
| Preco >25% abaixo da media | Possivel sub-orcamentacao, vai pedir trabalhos a mais | Pedir detalhe por artigo, confirmar inclusoes |
| Sem breakdown por capitulo | Impossivel controlar custos durante obra | Pedir mapa quantidades detalhado |
| Prazo <50% do realista | Nao vai cumprir, ou vai cortar qualidade | Confrontar com cronograma DIVA |
| Sem referencia alvara | Pode nao ter licenca | Verificar IMPIC antes de adjudicar |
| Condicoes 50%+25%+25% | Empreiteiro fica com maioria antes de acabar | Negociar plano mais equilibrado |
| Sem clausula garantias | Risco de abandonar apos pagamento | Exigir DL 67/2003 no contrato |
| "Materiais incluidos" sem especificar | Vai usar o mais barato | Exigir marca e referencia de cada material |

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - [Projecto] - Comparacao Propostas.md`

## Red flags
- NUNCA recomendar so pelo preco — o mais barato raramente e o melhor
- SEMPRE verificar alvara IMPIC do recomendado
- SEMPRE listar items em falta antes de decidir
- Diferenca >20% entre propostas em qualquer capitulo merece investigacao
