---
name: diva-contract
description: "Generate Portuguese construction contracts (empreitada) with all essential clauses. Covers 4 contract types (preco global, serie precos, percentagem, design-build), guarantees (DL 67/2003), penalties, payment milestones, insurance, SHST, and handover procedures. Triggers on \"contrato\", \"contract\", \"empreitada\", \"clausulas\", \"garantias obra\", \"penalizacoes\", \"contrato empreiteiro\"."
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# DIVA Contract — Portuguese Construction Contracts

Generate complete construction contracts adapted to Portuguese law with all essential clauses, schedules, and annexes.

## When to activate

Invoke `/diva-contract` when:
- User needs a contract template for hiring a contractor
- User asks about guarantees, penalties, payment terms
- User wants to compare contract types
- Before signing any empreitada agreement
- User needs subcontractor agreement template

## Workflow

### 1. Determine contract type
Ask or infer:
- **Preco Global** (default for well-defined projects)
- **Serie de Precos** (for rehabilitation with uncertainties)
- **Percentagem** (for trust-based relationships)
- **Design-Build** (for turnkey delivery)

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "contrato empreitada clausulas garantias portugal", collection: "diva", limit: 5)
```

### 3. Generate contract sections

**SECTION 1 — Partes**
- Dono de obra: NIF, morada, representante legal
- Empreiteiro: NIF, alvara IMPIC (numero, categoria, classe), representante
- Verificacao obrigatoria: alvara valido, seguro RC, seguro AT, situacao fiscal

**SECTION 2 — Objecto**
- Descricao da obra (tipo, morada, area)
- Referencia ao projecto aprovado (versao + data)
- Caderno de encargos como Anexo I
- Mapa de quantidades como Anexo II

**SECTION 3 — Preco e Pagamentos**
- Valor total (sem IVA + com IVA)
- Regime IVA (6% ou 23%, justificacao)
- Revisao de precos: sim/nao, formula (indices INE)
- Plano pagamentos:

| Milestone | % | Valor EUR | Condicao |
|---|---|---|---|
| Sinal | 10% | | Assinatura contrato |
| Inicio obra | 20% | | Consignacao local |
| Estrutura concluida | 25% | | Inspeccao aprovada |
| MEP + acabamentos | 25% | | 70% obra concluida |
| Recepcao provisoria | 15% | | Punch list <10 items |
| Retencao garantia | 5% | | 12 meses apos recepcao |

- Prazo pagamento: 30 dias apos factura + auto medicao
- Juros mora: taxa legal + 2pp

**SECTION 4 — Prazo**
- Data inicio (consignacao)
- Prazo total: ___ dias uteis
- Milestones intermedios obrigatorios
- Prorrogacoes: causas nao imputaveis (chuva excepcional >5 dias consecutivos, atrasos projecto, trabalhos a mais aprovados)

**SECTION 5 — Penalizacoes**
- Atraso: 0.5-1% por semana, max 10-15% do valor total
- Defeitos nao corrigidos no prazo: 2x custo correcao deduzido
- Abandono de obra >5 dias uteis sem justificacao: resolucao por justa causa

**SECTION 6 — Trabalhos a Mais e a Menos**
- Ate 5%: comunicacao previa escrita, execucao autorizada
- 5-25%: acordo escrito previo com orcamento aprovado
- >25%: adenda formal ao contrato
- Trabalhos a menos: deduzidos proporcionalmente
- REGRA: nenhum trabalho a mais sem aprovacao ESCRITA do dono de obra

**SECTION 7 — Garantias (DL 67/2003)**
- Obra geral: 5 anos
- Estrutura e fundacoes: 10 anos
- Equipamentos e instalacoes: 2 anos
- Impermeabilizacao: 10 anos (contratual)
- Retencao 5% ou garantia bancaria equivalente
- Caucao boa execucao: 5% garantia bancaria (libertada com recepcao provisoria)

**SECTION 8 — Seguros Obrigatorios**
- Acidentes de trabalho (empreiteiro): apolice em vigor
- RC profissional: minimo EUR 250.000
- Todo-risco construcao: valor total da obra (negociavel quem contrata)
- Copias das apolices como Anexo III

**SECTION 9 — Seguranca (SHST)**
- PSS obrigatorio (DL 273/2003)
- Coordenador seguranca obra nomeado
- Comunicacao previa ACT (se aplicavel)
- Compilacao tecnica da obra

**SECTION 10 — Fiscalizacao**
- Nomeacao do fiscal pelo dono de obra
- Poderes: aprovar/rejeitar materiais, exigir correccoes, suspender trabalhos
- Acesso: livre a toda a obra e documentacao
- Reunioes: semanais, actas assinadas

**SECTION 11 — Subempreitada**
- Autorizacao previa por escrito
- Empreiteiro mantém responsabilidade total
- Lista de subempreiteiros aprovados como Anexo IV
- Mesmas exigencias de alvara e seguros

**SECTION 12 — Recepcao da Obra**
- Recepcao provisoria: inspeccao, punch list, auto assinado, prazo correccao 30 dias
- Recepcao definitiva: apos periodo garantia (5 anos)
- Documentos obrigatorios na recepcao:
  - Telas finais (as-built)
  - Ficha Tecnica da Habitacao (FTH)
  - Certificado energetico (SCE)
  - Manuais de equipamentos
  - Garantias de equipamentos e subempreiteiros

**SECTION 13 — Resolucao**
- Justa causa pelo dono de obra: incumprimento grave, falencia, abandono >5 dias
- Conveniencia: pagamento trabalho executado + 5-10% indemnizacao
- Justa causa pelo empreiteiro: nao pagamento >60 dias, suspensao >90 dias
- Foro: tribunal comarca do local da obra

**SECTION 14 — Clausulas Especiais**
- Horario de trabalho: [definir, especialmente em condominios]
- Limpeza: empreiteiro responsavel diariamente
- Vizinhanca: responsabilidade por danos a terceiros
- Confidencialidade: dados projecto e cliente
- Propriedade intelectual: projecto pertence ao dono de obra

### 4. Generate annexes
- Anexo I: Caderno de encargos (referencia)
- Anexo II: Mapa de quantidades com precos
- Anexo III: Copias apolices seguro
- Anexo IV: Lista subempreiteiros aprovados
- Anexo V: Cronograma com milestones

## Output
Contrato Markdown completo + checklist pre-assinatura.

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - [Projecto] - Contrato Empreitada.md`

## Red Flags
- Never omit DL 67/2003 guarantee clauses (5 anos obra geral, 10 anos estrutura, 2 anos equipamentos) — these are mandatory under Portuguese law and any contract that weakens them is voidable in tribunal
- Never skip the payment milestone structure with 5% retention — paying 100% before recepcao provisoria eliminates all leverage to enforce punch list corrections
- Always include penalty clauses for delays (0.5-1% per week, capped at 10-15%) — without written penalties the only recourse is tribunal action, which in Portugal takes 2-4 years
- Never sign a contract without verified proof of insurance (acidentes de trabalho + RC profissional + todo-risco construcao) — if an accident occurs on an uninsured obra, the dono de obra bears joint liability under Portuguese law
- Always verify the empreiteiro's alvara IMPIC is valid and covers the obra's category and class — contracting an unlicensed builder voids insurance, invalidates guarantees, and exposes the client to heavy fines from IMPIC inspections
- Never allow obra to begin without PSS (Plano de Seguranca e Saude) and ACT communication — DL 273/2003 violations carry fines up to 120,000 EUR and can result in criminal liability if an accident occurs

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Partes e alvará IMPIC verificados

- [ ] Dono de obra com NIF completo, morada fiscal e representante legal nomeado
- [ ] Empreiteiro com número de alvará IMPIC, categoria e classe explícitos
- [ ] Confirmação de que o alvará cobre a classe de valor do contrato (ex: Classe 4 = até €1.330.000)
- [ ] Seguros RC e AT referenciados com número de apólice e validade

❌ NOT delivery-ready: `Empreiteiro: [NOME DA EMPRESA], alvará nº [XXXX]`
✅ Delivery-ready: `Construtora Barros & Filhos, Lda — NIF 509 876 234 — Alvará IMPIC nº 12.847, Categoria 1ª Classe 3 (obras até €664.000), RC Apólice Fidelidade nº 2024-RC-008812, válida até 31.12.2025`

---

### Gate 2 — Regime de preços e plano de pagamentos completo

- [ ] Tipo de contrato declarado (Preço Global / Série de Preços / Percentagem / Design-Build)
- [ ] Valor total explícito: base sem IVA + IVA à taxa correcta (6% reabilitação / 23% construção nova) + total com IVA
- [ ] Tabela de milestones preenchida com valores EUR reais (não percentagens vazias)
- [ ] Prazo de pagamento (30 dias) e taxa de juro de mora definidos

❌ NOT delivery-ready: `Pagamento na conclusão da estrutura: 25% = [VALOR]`
✅ Delivery-ready: `Pagamento 3 — Estrutura concluída: 25% = €37.500 + IVA 23% = €46.125 — condição: vistoria aprovada pelo fiscal Pedro Moutinho, até 15.04.2025`

---

### Gate 3 — Prazos, penalizações e trabalhos a mais operacionais

- [ ] Data de consignação concreta (não "a definir") e prazo total em dias úteis
- [ ] Penalização por atraso com percentagem e cap máximo em EUR (não só em %)
- [ ] Threshold de trabalhos a mais definido em % E em valor EUR absoluto
- [ ] Cláusula de prorrogação com causas específicas (chuva >5 dias consecutivos, etc.)

❌ NOT delivery-ready: `Penalização por atraso: 0,5% por semana até ao máximo contratual`
✅ Delivery-ready: `Penalização: 0,5% do valor contrato (€750/semana) por semana de atraso, cap máximo 10% = €15.000. Trabalhos a mais sem aprovação escrita do Eng.º Rui Ferreira: não pagos e passíveis de remoção a custo do empreiteiro`

---

### Gate 4 — Garantias DL 67/2003 intactas e retenção definida

- [ ] Garantia obra geral 5 anos presente e não reduzida
- [ ] Garantia estrutura e fundações 10 anos presente
- [ ] Garantia equipamentos/instalações 2 anos presente
- [ ] Retenção 5% OU garantia bancária equivalente com banco e prazo especificados
- [ ] Caução boa execução (5%) com condições de libertação na recepção provisória

❌ NOT delivery-ready: `Garantias conforme legislação aplicável. Retenção a acordar.`
✅ Delivery-ready: `Garantia geral 5 anos (DL 67/2003 art.4º), estrutura 10 anos, equipamentos 2 anos. Retenção: 5% = €7.500 libertados na recepção definitiva (Out.2030). Alternativa aceite: Garantia Bancária CGD nº [emitida antes de consignação], valor €7.500, prazo até 31.10.2030`

---

### Gate 5 — Secções SHST, fiscalização e subempreitada preenchidas

- [ ] Coordenador de segurança nomeado com nome e habilitação
- [ ] PSS referenciado como Anexo (não apenas mencionado)
- [ ] Fiscal do dono de obra identificado com poderes explícitos
- [ ] Subempreiteiros: lista aprovada em Anexo IV ou declaração de que nenhum é permitido sem aprovação prévia escrita

❌ NOT delivery-ready: `Coordenador de segurança: a nomear. Fiscalização conforme habitual.`
✅ Delivery-ready: `Coordenador Segurança: Arq.ª Sofia Leal (COSE nº 4.521), PSS versão 2 aprovado em 03.01.2025 — Anexo VI. Fiscal: Eng.º Pedro Moutinho (OE 78.923), reuniões às 2ªs feiras 09h, actas em 48h`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets por preencher

- [ ] Nenhum placeholder do tipo `[NOME]`, `[DATA]`, `[VALOR]`, `[XX]` permanece no output final
- [ ] Nome do projecto, morada da obra e partes identificadas com dados reais
- [ ] Anexos listados com títulos concretos (não "Anexo I: [descrever]")
- [ ] Ficheiro nomeado com data real: `2025-06-12 - Vivenda Cascais - Contrato Empreitada.md`

❌ NOT delivery-ready: `Entre [DONO DE OBRA], NIF [NIF], e [EMPREITEIRO], representado por [REPRESENTANTE]…`
✅ Delivery-ready: `Entre Luís Manuel Ferreira Costa, NIF 187 654 321, residente na Rua das Acácias 14, 2750-001 Cascais, e Construtora Barros & Filhos, Lda, NIF 509 876 234, representada por António Barros (gerente)…`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado da sessão/memória/dados do cliente (ex: NIF, alvará IMPIC, número de apólice)
- 🟡 **assumed** — plausível mas precisa confirmação do cliente antes de entregar contrato assinável
- 🟢 **projection** — projeção por design (prazo, milestone, penalização calculada — não verificável até execução)

Output checklist upfront mostra ao cliente exactamente o que é trust-as-is vs. o que precisa de verificar antes de assinar.  **Honest transparency > contrato que parece completo mas tem lacunas.**

---

❌ **NOT delivery-ready:**
```
Empreiteiro: Construções Silva Lda., NIF 512345678, Alvará IMPIC Classe 4
Prazo total: 180 dias úteis
Penalização por atraso: 0.5% por semana, máx. 10%
Retenção de garantia: 5% libertada aos 12 meses
```
*(Reader assume que tudo está verificado — NIF pode estar errado, alvará pode estar caducado, prazo foi estimado sem projecto aprovado)*

---

✅ **Delivery-ready:**
```
🔵 verified   — NIF empreiteiro: 512345678 (confirmado NIF.pt sessão anterior)
🔵 verified   — Alvará IMPIC nº 12345, Classe 4, válido até 31/12/2025 (doc fornecido cliente)
🟡 assumed    — Apólice RC EUR 250.000 (cliente referiu "tenho seguro" — número não confirmado)
🟡 assumed    — IVA taxa reduzida 6% (obra habitação própria permanente — precisa doc AT)
🟡 assumed    — Prazo 180 dias úteis (estimativa sem consultar mapa de trabalhos aprovado)
🟢 projection — Penalização semana 1 atraso: EUR 1.250 (0.5% × EUR 250.000 — calculado por fórmula)
🟢 projection — Retenção libertada em Março 2027 (12 meses após receção provisória estimada)
```

---

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados — substituir assumptions com actuals (NIF, alvará, apólices, regime IVA)
- [ ] Todas as citações adicionadas por fontes 🔵 (docs fornecidos pelo cliente em sessão)
- [ ] Todas as projeções 🟢 comunicadas ao cliente como estimativas (expectativas claras antes da assinatura)
- [ ] Anexos referenciados no contrato (I–IV) preenchidos ou marcados como `[A FORNECER]`
- [ ] Alvará IMPIC validado em portal IMPIC.pt antes de entrega final

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Contrato de Empreitada — Vivenda Cascais
**Data:** 12 de Junho de 2025
**Tipo:** Preço Global

---

## Cláusula 1 — Partes

**Dono de Obra:**
Luís Manuel Ferreira Costa — NIF 187 654 321
Rua das Acácias 14, 2750-001 Cascais

**Empreiteiro:**
Construtora Barros & Filhos, Lda — NIF 509 876 234
Alvará IMPIC nº 12.847 — Categoria 1ª Classe 3 (até €664.000)
Representado por: António Barros (gerente)
RC Profissional: Apólice Fidelidade nº 2024-RC-008812, válida 31.12.2025
Seguro AT: Apólice Tranquilidade nº AT-2024-77341, válida 31.12.2025

---

## Cláusula 2 — Objecto

Construção de moradia unifamiliar T4 com garagem, sita na
Rua do Outeiro 7, lote 3, 2750-312 Cascais — Proc. CM Cascais nº 2024/0891.
Projecto de Arquitectura: Arq.º Jorge Neves, versão 3, aprovado em 15.01.2025.
Área bruta: 320 m² + 45 m² garagem.
Caderno de Encargos: Anexo I (Rev.2, 20.02.2025)
Mapa de Quantidades: Anexo II (aprovado pelo dono de obra em 01.03.2025)

---

## Cláusula 3 — Preço e Pagamentos

**Valor contrato (Preço Global):**
Base: €150.000,00 (sem IVA)
IVA 23% (construção nova): €34.500,00
**Total: €184.500,00**

Revisão de preços: NÃO aplicável (prazo ≤ 18 meses)

| # | Milestone | % | Valor s/IVA | Condição | Data Prevista |
|---|---|---|---|---|---|
| 1 | Sinal | 10% | €15.000 | Assinatura contrato | 12.06.2025 |
| 2 | Consignação/Início | 20% | €30.000 | Licença emitida + consignação | 01.07.2025 |
| 3 | Estrutura concluída | 25% | €37.500 | Vistoria Eng.º Moutinho aprovada | 15.10.2025 |
| 4 | MEP + acabamentos | 25% | €37.500 | 70% obra concluída verificado | 15.01.2026 |
| 5 | Recepção provisória | 15% | €22.500 | Punch list < 10 itens | 31.03.2026 |
| 6 | Retenção garantia | 5% | €7.500 | 12 meses após recepção | 30.03.2027 |

Prazo pagamento: 30 dias após factura + auto de medição.
Juros de mora: taxa legal BCE + 2 pp (actualmente 6,15% a.a.)

---

## Cláusula 4 — Prazo

Início: 01.07.2025 (data de consignação)
Prazo total: **270 dias úteis** (conclusão prevista: 31.03.2026)

Milestones obrigatórios:
- Fundações concluídas: 01.09.2025
- Estrutura concluída: 15.10.2025
- Fechamentos exteriores: 15.12.2025
- MEP roughed-in: 31.01.2026

Prorrogações aceites (não imputáveis ao empreiteiro):
- Chuva excepcional > 5 dias úteis consecutivos (com registo IPMA)
- Atrasos na aprovação de especialidades pela CM Cascais
- Trabalhos a mais aprovados que alterem o caminho crítico

---

## Cláusula 5 — Penalizações

Atraso: **€750/semana** (0,5% × €150.000), cap máximo **€15.000** (10%)
Defeitos não corrigidos em 30 dias após notificação escrita:
dedução de 2× o custo de correcção avaliado pelo fiscal.
Abandono > 5 dias úteis sem justificação: resolução por justa causa
sem indemnização ao empreiteiro.

---

## Cláusula 7 — Garantias (DL 67/2003)

| Elemento | Prazo Legal | Prazo Contratual |
|---|---|---|
| Obra geral | 5 anos | 5 anos (até 31.03.2031) |
| Estrutura e fundações | 10 anos | 10 anos (até 31.03.2036) |
| Equipamentos/instalações | 2 anos | 2 anos (até 31.03.2028) |
| Impermeabilização coberturas | — | 10 anos contratual |

Retenção: 5% = €7.500 retidos até recepção definitiva (31.03.2027).
Alternativa aceite: Garantia Bancária CGD emitida até 25.06.2025,
valor €7.500, prazo até 30.04.2027.

---

## Cláusula 9 — Segurança (SHST / DL 273/2003)

Coordenador Segurança em Obra: Arq.ª Sofia Leal — COSE nº 4.521
PSS versão 2, aprovado 03.01.2025 — **Anexo VI**
Comunicação prévia ACT submetida em 15.06.2025 (ref. ACT/2025/CAS/04419)
Compilação técnica: responsabilidade do empreiteiro, entregue na recepção definitiva.

---

## Cláusula 10 — Fiscalização

Fiscal nomeado pelo dono de obra: Eng.º Pedro Moutinho — OE nº 78.923
Poderes: aprovação/rejeição de materiais, exigência de correcções,
suspensão de trabalhos com fundamento escrito.
Reuniões: 2ªs feiras, 09h00, obra. Actas em 48h, assinadas por ambas as partes.
Acesso: livre e sem aviso prévio a toda a obra e documentação.

---

## Recepção e Documentos Obrigatórios

Na recepção provisória (prevista 31.03.2026), o empreiteiro entrega:
- Telas finais (as-built) em DWG + PDF
- Ficha Técnica da Habitação (FTH)
- Certificado SCE (classe mínima B)
- Manuais de todos os equipamentos instalados
- Garantias de subempreiteiros (Soares Electricidade, Lda — aprovado Anexo IV)

---

**Foro:** Tribunal Judicial da Comarca de Cascais
**Local e data:** Cascais, 12 de Junho de 2025

_________________________ _________________________
Luís Manuel Ferreira Costa    António Barros (Construtora Barros & Filhos, Lda)
```

---

## Output anti-patterns

- Emitir contrato sem número de alvará IMPIC verificado — alvará inválido ou de classe insuficiente invalida a cobertura de seguro e expõe o dono de obra a litígio
- Deixar tabela de milestones com valores EUR em branco (`[VALOR]`) — contrato não é executável sem valores absolutos
- Mencionar "garantias conforme lei" sem citar DL 67/2003 e prazos concretos — cláusula vaga é inútil em tribunal
- Omitir o cap máximo das penalizações em EUR — percentagem sozinha não protege nenhuma das partes
- Gerar contrato Preço Global para obra de reabilitação com grandes incertezas — tipo de contrato errado para o contexto
- Não identificar o coordenador de segurança por nome — PSS sem responsável nomeado viola DL 273/2003
- Incluir cláusula de arbitragem como foro único sem acordo expresso do dono de obra — cláusula potencialmente nula
- Omitir lista de documentos obrigatórios na recepção (FTH, SCE, telas finais) — recepção incompleta bloqueia escritura de venda futura
- Redigir cláusula de trabalhos a mais apenas em percentagem sem aprovação escrita obrigatória — empreiteiro pode alegar verbal approval
- Não especificar qual parte contrata o seguro todo-risco construção — omissão frequente que resulta em obra descoberta
