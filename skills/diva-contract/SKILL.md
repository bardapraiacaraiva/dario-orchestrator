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
