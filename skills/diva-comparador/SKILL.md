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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Todas as propostas normalizadas para a mesma estrutura

- [ ] Valores sem IVA e com IVA extraídos e conferidos para cada proposta
- [ ] Preço/m² calculado e preenchido (não deixar "EUR" vazio)
- [ ] Capítulos ProNIC alinhados — proposta que não separa capítulos foi decomposta manualmente
- [ ] Unidades homogéneas (m², ml, un) — não misturar "preço global" com itemizado
- ❌ NOT delivery-ready: `Proposta B: valor total €45.000 (IVA incluído?)` — ambíguo, não decomposto
- ✅ Delivery-ready: `Proposta B: €36.585 sem IVA + €8.414 IVA 23% = €45.000 com IVA · €487/m² (75m²)`

---

### Gate 2 — Tabela de itens críticos em falta preenchida com dados reais

- [ ] Pelo menos 4 itens críticos verificados por proposta (impermeabilização, caixilharia, certificação energética, limpeza final)
- [ ] Cada célula diz "Incluído", "**EM FALTA**" ou "Incluído — marca/ref especificada"
- [ ] Items em falta foram quantificados em € estimados (custo de adicionar depois)
- [ ] Nenhuma célula vazia ou com "–" sem justificação
- ❌ NOT delivery-ready: `Impermeabilização: ver proposta B` — não resolve a dúvida
- ✅ Delivery-ready: `Impermeabilização WC (2 casas de banho): Proposta A ✅ — Proposta B **EM FALTA** (~€800-1.200 se adicionado a posteriori) — Proposta C ✅`

---

### Gate 3 — Red flags identificados com evidência específica

- [ ] Cada red flag referencia a proposta exata (A/B/C) e o capítulo ou cláusula
- [ ] Propostas com preço >25% abaixo da média têm flag explícita com % calculada
- [ ] Condições de pagamento analisadas: qualquer cenário com >50% adiantado tem flag
- [ ] Prazo verificado contra referencial DIVA (não aceitar prazo sem confrontar com realidade)
- ❌ NOT delivery-ready: `Proposta B tem preço suspeito` — vago, sem número
- ✅ Delivery-ready: `🚩 Proposta B — Preço anormalmente baixo: €28.400 vs média €38.950 (-27%) · Capítulo Impermeabilização: €0 declarado · Risco: trabalhos a mais após adjudicação`

---

### Gate 4 — Scoring ponderado calculado (não estimado a olho)

- [ ] Todos os 6 critérios pontuados de 0–10 para cada proposta
- [ ] Total ponderado calculado: `(Preço×0,30) + (Scope×0,25) + (Prazo×0,15) + (Garantia×0,10) + (Pagamento×0,10) + (Álvara×0,10)`
- [ ] Nenhum critério deixado em branco — se info não disponível, nota-se "n/d → penalizar com 3/10"
- [ ] Scoring não contradiz a recomendação final (se recomenda A, A tem maior total ponderado)
- ❌ NOT delivery-ready: `Proposta A score: ~7/10 (estimativa)` — não é auditável
- ✅ Delivery-ready: `Proposta A: Preço 6×0,30=1,8 · Scope 9×0,25=2,25 · Prazo 8×0,15=1,2 · Garantia 9×0,10=0,9 · Pagamento 8×0,10=0,8 · Álvara 10×0,10=1,0 → **Total: 7,95/10**`

---

### Gate 5 — Recomendação com justificação e plano de negociação concreto

- [ ] Recomendação nomeia a proposta vencedora E explica porquê (não só preço)
- [ ] Pontos de negociação listados: pelo menos 2 itens a negociar com o empreiteiro escolhido
- [ ] Items a adicionar ao contrato antes de assinar listados com valor estimado
- [ ] Álvara IMPIC do recomendado mencionado com instrução de verificação (impic.pt)
- ❌ NOT delivery-ready: `Recomendamos a Proposta A por ser mais completa.`
- ✅ Delivery-ready: `Recomendamos Proposta A (Construções Ferreira Lda · álvara IMPIC nº 12345 — confirmar em impic.pt). Score 7,95/10. Negociar: (1) reduzir adiantamento de 40% para 25%; (2) incluir impermeabilização terraço no preço base. Adicionar ao contrato: cláusula DL 67/2003 garantia 5 anos estrutura.`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem placeholders entre ângulos

- [ ] Nome do projecto e morada reais substituem `[Projecto]`
- [ ] Nomes dos empreiteiros (ou "Proposta A — Construções X") preenchidos
- [ ] Data de emissão das propostas registada (relevante para validade)
- [ ] Ficheiro salvo em `05 - Claude - IA/Outputs/YYYY-MM-DD - [Projecto real] - Comparacao Propostas.md`
- [ ] Zero ocorrências de `<placeholder>`, `EUR` vazio, `X/10` não substituído, ou `[detalhe]` não preenchido
- ❌ NOT delivery-ready: `Comparação de Propostas — [Projecto] · Proposta A: EUR · Score: X/10`
- ✅ Delivery-ready: `Comparação de Propostas — Apartamento T3 Rua das Flores 42, Lisboa · Proposta A — Construções Ferreira: €41.200 s/IVA · Score: 7,95/10`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## Comparação de Propostas — Apartamento T3, Rua Actor Vale 18, 2.º Dto, Lisboa
**Proprietário:** Cuidai Gestão de Imóveis, Lda — Processo DIVA #CV-2024-031
**Data análise:** 2025-01-15 | **Propostas datadas:** Dez 2024 (validade 90 dias)
**Área útil:** 82 m² | **Obra:** Remodelação completa + cozinha + 2 WC

---

### Resumo Executivo

|  | Proposta A — Ferreira & Filhos | Proposta B — RenoLisboa Lda | Proposta C — AM Construções |
|---|---|---|---|
| **Álvara IMPIC** | ✅ nº 42.817 | ✅ nº 38.104 | ⚠️ não fornecido |
| **Valor sem IVA** | €47.300 | €34.200 | €51.800 |
| **Valor com IVA (23%)** | €58.179 | €42.066 | €63.714 |
| **Preço/m²** | €578/m² | €417/m² | €632/m² |
| **Prazo** | 14 semanas | 8 semanas | 16 semanas |
| **Início previsto** | Fev 2025 | Fev 2025 | Mar 2025 |
| **Garantia geral** | 5 anos (DL 67/2003) | 2 anos | 5 anos (DL 67/2003) |
| **Condições pagamento** | 25%+25%+25%+25% | 50%+30%+20% | 30%+30%+20%+20% |

---

### Breakdown por Capítulo

| Capítulo | Ferreira & Filhos | RenoLisboa | AM Construções | Δ máx |
|---|---|---|---|---|
| Demolição | €2.800 | €2.100 | €3.200 | +52% |
| Alvenaria | €4.500 | €3.800 | €5.100 | +34% |
| Impermeabilização | €3.200 | **€0** | €2.900 | — |
| Electricidade | €7.400 | €6.200 | €8.100 | +31% |
| Canalização | €5.800 | €4.100 | €6.200 | +51% |
| AVAC | €2.600 | €1.800 | €2.800 | +56% |
| Pavimentos | €6.200 | €5.400 | €6.800 | +26% |
| Revestimentos | €4.800 | €3.900 | €5.200 | +33% |
| Carpintaria | €3.100 | **€0** | €3.400 | — |
| Cozinha (móveis+equip.) | €4.200 | €3.600 | €4.800 | +33% |
| Pintura | €1.900 | €1.700 | €2.100 | +24% |
| Sanitários (2 WC) | €3.800 | €3.200 | €4.200 | +31% |
| Limpeza final | €400 | **€0** | €400 | — |
| Certificação energética | **€600** | **€0** | **€0** | — |
| **TOTAL s/IVA** | **€47.300** | **€34.200** | **€51.800** | |

---

### Items Críticos em Falta

| Item | Ferreira & Filhos | RenoLisboa | AM Construções |
|---|---|---|---|
| Impermeabilização WC (2×) | ✅ Incluído | ❌ **EM FALTA** (~€1.400 a posteriori) | ✅ Incluído |
| Carpintaria interior | ✅ Incluído | ❌ **EM FALTA** (~€3.100 a posteriori) | ✅ Incluído |
| Limpeza final de obra | ✅ Incluído | ❌ **EM FALTA** (~€400) | ✅ Incluído |
| Certificação energética | ✅ Incluído | ❌ **EM FALTA** (~€600) | ❌ **EM FALTA** (~€600) |
| Álvara IMPIC verificável | ✅ nº 42.817 | ✅ nº 38.104 | ❌ Não fornecido |

**RenoLisboa custo real estimado:** €34.200 + €5.500 (itens em falta) = **€39.700** — diferença para Ferreira & Filhos reduz para €7.600 (16%)

---

### Red Flags

| 🚩 Flag | Proposta | Detalhe |
|---|---|---|
| Preço anormalmente baixo | RenoLisboa | €34.200 vs média €44.433 (**-23%**) · Impermeabilização e carpintaria a €0 · Risco elevado de trabalhos a mais |
| Prazo irrealista | RenoLisboa | 8 semanas para remodelação completa 82m² — referencial DIVA: 13-16 semanas |
| Condições desequilibradas | RenoLisboa | 50% adiantamento: empreiteiro recebe €21.033 antes de iniciar obra |
| Álvara não fornecido | AM Construções | Verificação obrigatória em impic.pt antes de qualquer adjudicação |
| Sem marca de materiais | RenoLisboa | "Pavimentos incluídos" sem ref — risco de material de baixa gama |
| Certificação energética omitida | RenoLisboa + AM Const. | Obrigatória para arrendamento (SCE) — custo não previsto de ~€600 |

---

### Scoring Ponderado

| Critério (peso) | Ferreira & Filhos | RenoLisboa | AM Construções |
|---|---|---|---|
| Preço real (30%) | 7 × 0,30 = **2,10** | 5 × 0,30 = **1,50** | 5 × 0,30 = **1,50** |
| Completude scope (25%) | 9 × 0,25 = **2,25** | 3 × 0,25 = **0,75** | 8 × 0,25 = **2,00** |
| Prazo realista (15%) | 8 × 0,15 = **1,20** | 2 × 0,15 = **0,30** | 9 × 0,15 = **1,35** |
| Garantias (10%) | 9 × 0,10 = **0,90** | 5 × 0,10 = **0,50** | 9 × 0,10 = **0,90** |
| Condições pagamento (10%) | 9 × 0,10 = **0,90** | 3 × 0,10 = **0,30** | 7 × 0,10 = **0,70** |
| Álvara + seguros (10%) | 10 × 0,10 = **1,00** | 9 × 0,10 = **0,90** | 3 × 0,10 = **0,30** |
| **TOTAL PONDERADO** | **8,35/10** | **4,25/10** | **6,75/10** |

---

### Recomendação

**✅ Melhor valor: Proposta A — Ferreira & Filhos (8,35/10)**

**Justificação:** Scope completo (único a incluir impermeabilização, carpintaria e certificação energética), condições de pagamento equilibradas (25%×4), prazo realista (14 semanas), garantia 5 anos DL 67/2003, álvara IMPIC verificado nº 42.817. Preço real €47.300 vs RenoLisboa €39.700 real — diferença de €7.600 (16%) justificada pelo scope completo e risco eliminado.

**Negociação sugerida com Ferreira & Filhos:**
1. Reduzir 1.ª prestação de 25% para 20% (€9.460 → €7.568) — argumento: obra só começa em Fev
2. Solicitar marca e referência de pavimentos e revestimentos antes de assinar
3. Incluir penalização de €150/semana por atraso superior a 2 semanas no contrato

**Antes de assinar — adicionar ao contrato:**
- Cláusula DL 67/2003 explícita (garantia 5 anos estrutura, 1 ano restantes)
- Mapa de quantidades detalhado por artigo como anexo vinculativo
- Cronograma semanal com marcos de pagamento associados a entregas físicas

**Verificar antes de adjudicar:** impic.pt → pesquisa por "Ferreira & Filhos" → confirmar nº 42.817 activo e sem processos disciplinares.
```

---

## Output anti-patterns

- Recomendar a proposta mais barata sem analisar scope completo — o "barato" de €34.200 tornava-se €39.700 após itens em falta
- Deixar células da matriz com "EUR" ou "X/10" por preencher — output inutilizável para decisão
- Identificar red flag sem quantificar o risco em € — "preço suspeito" não ajuda; "-23% vs média, risco de €5.500 em trabalhos a mais" ajuda
- Scoring "estimado a olho" sem cálculo ponderado auditável — contradições entre score e recomendação destroem credibilidade
- Omitir custo real dos itens em falta — comparação de preço total sem normalização de scope é enganadora
- Não mencionar verificação IMPIC antes de recomendar — responsabilidade legal do conselho
- Prazo aceite sem confrontar com referencial realista — empreiteiro que promete 8 semanas para 82m² de remodelação total vai falhar
- Recomendação sem plano de negociação — cliente sabe "quem" mas não "como negociar"
- Condições de pagamento não analisadas — 50% de adiantamento é red flag maior que diferença de preço de 10%
- Output sem nome do cliente e data das propostas — análise sem âncora temporal perde validade
