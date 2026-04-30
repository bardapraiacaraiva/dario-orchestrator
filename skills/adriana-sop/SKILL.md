---
name: adriana-sop
description: "ADRIANA Admin SOPs — procedures for all admin processes, templates, checklists, training"
version: "1.0"
---

# ADRIANA-SOP: Procedimentos Operacionais Padrao Administrativos

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** SOP, procedimento, processo, checklist, passo-a-passo, como fazer, instrucao trabalho, fluxo, workflow, procedimento administrativo, treinar, formacao procedimento
**Trigger words (EN):** SOP, procedure, process, checklist, step-by-step, how-to, work instruction, workflow, admin procedure, standard operating procedure, training

Activar quando o utilizador precisa de:
- Criar SOP para processo administrativo
- Documentar procedimento existente
- Criar checklist operacional
- Treinar alguem num procedimento
- Auditar conformidade com SOPs
- Optimizar processo existente

## Workflow Passo-a-Passo

### 1. Identificar o Processo

Antes de criar o SOP, responder a:
- **O que?** Qual o processo (ex: abrir conta fornecedor)
- **Quem?** Quem executa e quem aprova
- **Quando?** Trigger/gatilho que inicia o processo
- **Quanto tempo?** Duracao esperada
- **Com que frequencia?** Diario, semanal, ad hoc
- **Que ferramentas?** Sistemas, templates, formularios
- **Que riscos?** O que pode correr mal

### 2. Template SOP

```markdown
# SOP: [Nome do Procedimento]

**Ref:** SOP-ADM-NNN
**Versao:** X.X
**Data:** YYYY-MM-DD
**Departamento:** Administracao
**Responsavel:** [Nome/Cargo]
**Aprovador:** [Nome/Cargo]
**Proxima revisao:** YYYY-MM-DD

---

## 1. Objectivo
[Para que serve este procedimento — 1-2 frases]

## 2. Ambito
[A quem se aplica e em que situacoes]

## 3. Definicoes e Abreviaturas
| Termo | Significado |
|-------|-------------|
| [Termo] | [Definicao] |

## 4. Responsabilidades
| Papel | Responsabilidade |
|-------|-----------------|
| Executor | [O que faz] |
| Revisor | [O que valida] |
| Aprovador | [O que aprova] |

## 5. Materiais e Ferramentas
- [ ] [Sistema/ferramenta 1]
- [ ] [Template/formulario]
- [ ] [Acesso necessario]

## 6. Procedimento

### Passo 1: [Nome do passo]
**Responsavel:** [Quem]
**Tempo estimado:** X min
**Input:** [O que precisa para comecar]

Instrucoes:
1. [Instrucao detalhada]
2. [Instrucao detalhada]
3. [Instrucao detalhada]

**Output:** [O que resulta deste passo]
**Criterio de qualidade:** [Como saber que esta bem feito]

### Passo 2: [Nome do passo]
...

### Passo N: [Nome do passo]
...

## 7. Fluxograma
```
[INICIO] → [Passo 1] → [Decisao?]
                            ├─ SIM → [Passo 2A] → [FIM]
                            └─ NAO → [Passo 2B] → [Voltar Passo 1]
```

## 8. Excepcoes e Contingencias
| Situacao | Accao | Escalar a |
|----------|-------|-----------|
| [Erro X] | [Corrigir como] | [Quem] |
| [Sistema indisponivel] | [Alternativa manual] | [Quem] |

## 9. Metricas e KPIs
| Metrica | Meta |
|---------|------|
| Tempo de execucao | <X min |
| Taxa de erro | <X% |
| Satisfacao | >X/5 |

## 10. Historico de Revisoes
| Versao | Data | Alteracao | Autor |
|--------|------|-----------|-------|
| 1.0 | YYYY-MM-DD | Criacao | [Nome] |

## 11. Anexos
- [Template referenciado]
- [Formulario referenciado]
```

### 3. Catalogo de SOPs Administrativos

| # | SOP | Ref | Prioridade | Estado |
|---|-----|-----|-----------|--------|
| 1 | Abertura de conta fornecedor | SOP-ADM-001 | Alta | — |
| 2 | Emissao de factura | SOP-ADM-002 | Alta | — |
| 3 | Recepcao de material | SOP-ADM-003 | Media | — |
| 4 | Onboarding novo colaborador | SOP-ADM-004 | Alta | — |
| 5 | Offboarding colaborador | SOP-ADM-005 | Alta | — |
| 6 | Reserva sala reuniao | SOP-ADM-006 | Baixa | — |
| 7 | Registo de visitante | SOP-ADM-007 | Media | — |
| 8 | Pedido de viagem | SOP-ADM-008 | Media | — |
| 9 | Nota de despesas | SOP-ADM-009 | Media | — |
| 10 | Requisicao material | SOP-ADM-010 | Baixa | — |
| 11 | Arquivo de documentos | SOP-ADM-011 | Media | — |
| 12 | Gestao de correio | SOP-ADM-012 | Baixa | — |
| 13 | Pedido de manutencao | SOP-ADM-013 | Media | — |
| 14 | Publicacao de politica | SOP-ADM-014 | Alta | — |
| 15 | Inventario fisico | SOP-ADM-015 | Media | — |
| 16 | Preparacao town hall | SOP-ADM-016 | Baixa | — |
| 17 | Abertura de conta bancaria | SOP-ADM-017 | Alta | — |
| 18 | Pedido certificado AT/SS | SOP-ADM-018 | Media | — |
| 19 | Registo de acidente trabalho | SOP-ADM-019 | Alta | — |
| 20 | Encerramento mensal admin | SOP-ADM-020 | Alta | — |

### 4. Niveis de Documentacao

| Nivel | Tipo | Detalhe | Quando usar |
|-------|------|---------|------------|
| 1 | **Politica** | O que fazer (principios) | Regras gerais |
| 2 | **SOP** | Como fazer (passo-a-passo) | Processos completos |
| 3 | **Instrucao trabalho** | Detalhe tecnico (screenshots) | Tarefa especifica |
| 4 | **Checklist** | Lista verificacao (sim/nao) | Validacao rapida |
| 5 | **Template** | Modelo pre-preenchido | Documentos recorrentes |

### 5. Checklist Rapida (formato curto)

```markdown
# Checklist: [Nome]
**Ref:** CHK-ADM-NNN
**Versao:** X.X

- [ ] Passo 1: [Accao]
- [ ] Passo 2: [Accao]
- [ ] Passo 3: [Accao]
- [ ] Passo 4: [Accao]
- [ ] Verificacao final: [Criterio]

**Executado por:** _______________ **Data:** _______________
```

### 6. Formacao e Certificacao

**Processo de formacao em SOP:**
1. Ler o SOP completo
2. Observar execucao por pessoa experiente (shadowing)
3. Executar sob supervisao (1-3 vezes)
4. Executar de forma autonoma
5. Validacao: quiz ou checklist de competencia
6. Registo de formacao assinado

**Registo de formacao:**
| Colaborador | SOP | Data formacao | Formador | Certificado |
|-------------|-----|--------------|----------|-------------|
| [Nome] | SOP-ADM-001 | YYYY-MM-DD | [Nome] | Sim |

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana sop create [nome]` | Criar SOP com template completo |
| `adriana sop checklist [nome]` | Criar checklist rapida |
| `adriana sop catalog` | Listar todos os SOPs |
| `adriana sop audit` | Auditar conformidade com SOPs |
| `adriana sop train [sop] [pessoa]` | Registar formacao |
| `adriana sop review [ref]` | Iniciar revisao de SOP |
| `adriana sop optimize [ref]` | Sugerir optimizacoes |

## Template de Output

```markdown
## Estado SOPs — [Data]

### Resumo
- SOPs activos: X
- SOPs por criar (identificados): X
- SOPs para revisao: X
- Formacoes realizadas este mes: X

### Conformidade
| Departamento | SOPs aplicaveis | % cobertos | % formacao |
|-------------|----------------|------------|-----------|
| Admin | X | XX% | XX% |
| [Dept] | X | XX% | XX% |

### Accoes Requeridas
1. [ ] Criar SOP para [processo]
2. [ ] Rever SOP-ADM-XXX (vencido)
3. [ ] Formar [Nome] em SOP-ADM-XXX
```

## Red Flags

- Processo critico sem SOP documentado
- SOP desactualizado (>12 meses sem revisao)
- Colaborador executa processo sem formacao registada
- SOP contradiz politica em vigor
- SOP demasiado complexo (>30 passos sem sub-divisao)
- Nenhum responsavel designado para o SOP
- SOP sem fluxo de excepcoes/contingencias
- Multiplas versoes do SOP em circulacao
- Processo executado diferente do SOP (gap pratica vs teoria)
- Sem metricas para medir eficacia do processo

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-docs** | SOPs seguem gestao documental |
| **adriana-policies** | SOPs implementam politicas |
| **adriana-onboarding** | SOPs essenciais no onboarding |
| **adriana-meetings** | SOP de tipos de reuniao |
| **adriana-procurement** | SOP de compras e aprovacoes |
| **adriana-travel** | SOP de viagens e despesas |
| **adriana-reception** | SOP de recepcao visitantes |
| **adriana-inventory** | SOP de inventario e encomendas |
| **adriana-facilities** | SOP de manutencao |
| **adriana-archive** | SOP de arquivo e destruicao |
| **dario-sop** | Framework generico de SOPs (Carpenter, Gawande) |

## Boas Praticas

- **Regra dos 5 minutos:** Se o SOP demora >5min a ler, precisa de ser simplificado
- **Test with a stranger:** Se alguem de fora consegue executar so com o SOP, esta bom
- **Visual first:** Fluxogramas e screenshots antes de texto longo
- **Versao viva:** SOP que nao e actualizado e pior que nao ter SOP
- **Um processo, um SOP:** Nao juntar processos diferentes no mesmo documento
- **Feedback loop:** Quem executa deve poder sugerir melhorias
