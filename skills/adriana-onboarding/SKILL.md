---
name: adriana-onboarding
description: "ADRIANA Employee Onboarding/Offboarding — day-1 checklist, equipment, accounts, training, exit procedures"
version: "1.0"
---

# ADRIANA-ONBOARDING: Integracao e Saida de Colaboradores

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** onboarding, integracao, novo colaborador, primeiro dia, equipamento, contas, formacao, offboarding, saida, desligamento, checklist entrada, checklist saida, acolhimento
**Trigger words (EN):** onboarding, offboarding, new employee, first day, equipment, accounts, training, exit, termination, new hire, day one, welcome pack

Activar quando o utilizador precisa de:
- Preparar entrada de novo colaborador
- Criar checklist de dia 1
- Configurar equipamento e contas
- Planear formacao inicial
- Processar saida de colaborador
- Gerir entrega de equipamento e revogacao de acessos

## Workflow Passo-a-Passo

### PARTE A: ONBOARDING (Entrada)

#### Fase 1: Pre-Onboarding (1-2 semanas antes)

**Administrativo:**
- [ ] Contrato assinado e arquivado
- [ ] Documentos recebidos (BI/CC, NIF, NISS, IBAN, habilitacoes)
- [ ] Comunicacao a Seguranca Social (ate vespera inicio)
- [ ] Seguro de trabalho actualizado
- [ ] Medicina do trabalho: ficha aptidao marcada
- [ ] Numero de funcionario atribuido

**Equipamento:**
- [ ] Computador/portatil configurado
- [ ] Monitor, teclado, rato (se aplicavel)
- [ ] Telemovel empresa (se aplicavel)
- [ ] Cartao de acesso / chaves
- [ ] Material escritorio (bloco, caneta, etc.)
- [ ] Secretaria/posto trabalho atribuido e limpo

**Contas e Acessos:**
- [ ] Email corporativo criado
- [ ] Slack / Teams / chat interno
- [ ] Drive / SharePoint / repositorios
- [ ] Ferramentas especificas do cargo (Jira, Figma, etc.)
- [ ] VPN / acesso remoto
- [ ] Impressora / scanner
- [ ] Assinatura email configurada

**Comunicacao:**
- [ ] Equipa informada da chegada (nome, funcao, data)
- [ ] Buddy/mentor designado
- [ ] Email de boas-vindas preparado
- [ ] Welcome pack pronto (se existir)

#### Fase 2: Dia 1

```markdown
# Checklist Dia 1 — [Nome do Colaborador]
**Data:** YYYY-MM-DD
**Funcao:** [Cargo]
**Departamento:** [Dept]
**Buddy:** [Nome]

## Manha (09:00-12:30)
- [ ] 09:00 — Recepcao pela chefia directa
- [ ] 09:15 — Tour ao escritorio (WC, cozinha, salas, saidas emergencia)
- [ ] 09:45 — Entrega equipamento + configuracao passwords
- [ ] 10:30 — Apresentacao a equipa directa
- [ ] 11:00 — Leitura: manual colaborador + politicas essenciais
- [ ] 11:30 — Setup ferramentas com buddy

## Tarde (14:00-18:00)
- [ ] 14:00 — Apresentacao empresa (missao, valores, estrutura)
- [ ] 14:30 — Apresentacao departamentos (quem faz o que)
- [ ] 15:00 — Primeira tarefa guiada com buddy
- [ ] 16:30 — Revisao do dia + duvidas com chefia
- [ ] 17:00 — Tempo livre para explorar ferramentas
- [ ] 17:30 — Check-in informal: como correu o dia?
```

#### Fase 3: Primeira Semana

- [ ] Reuniao 1:1 com chefia (expectativas, objectivos)
- [ ] Sessoes com cada departamento relevante (30min cada)
- [ ] Formacao ferramentas internas
- [ ] Acesso completo a documentacao do cargo
- [ ] Primeiro almoco de equipa
- [ ] Feedback dia 5: o que falta? duvidas?

#### Fase 4: Primeiro Mes (30 dias)

- [ ] Objectivos do periodo experimental definidos (SMART)
- [ ] Formacao tecnica especifica concluida
- [ ] Integracao plena em projectos
- [ ] Reuniao 1:1 semanal com chefia
- [ ] Feedback 360: chefia + equipa + auto-avaliacao
- [ ] Revisao e ajuste do plano se necessario

#### Fase 5: Avaliacao (60-90 dias)

- [ ] Avaliacao formal periodo experimental
- [ ] Feedback escrito de chefia e buddy
- [ ] Decisao: confirmacao / extensao / termino
- [ ] Se confirmado: definir plano desenvolvimento anual

### PARTE B: OFFBOARDING (Saida)

#### Fase 1: Comunicacao (Dia 0)

- [ ] Carta/email de rescisao ou demissao recebida
- [ ] Data de saida definida (cumprir pre-aviso legal)
- [ ] RH informado e processo iniciado
- [ ] Comunicacao a equipa (quando e como)

#### Fase 2: Transicao (Ate ultimo dia)

- [ ] Lista de projectos/tarefas em curso
- [ ] Plano de passagem de trabalho a colega
- [ ] Documentacao de processos exclusivos do colaborador
- [ ] Transferencia de contactos de clientes
- [ ] Knowledge transfer sessions agendadas
- [ ] Backup de ficheiros relevantes

#### Fase 3: Ultimo Dia

**Administrativo:**
- [ ] Entrega de equipamento (portatil, telemovel, cartao acesso, chaves)
- [ ] Devolucao material empresa
- [ ] Assinatura auto de devolucao
- [ ] Confirmacao de morada para envio documentos finais

**Acessos (revogar em 24h):**
- [ ] Email corporativo (backup + forward temporario se necessario)
- [ ] Slack / Teams
- [ ] Drive / SharePoint
- [ ] Ferramentas SaaS
- [ ] VPN
- [ ] Cartao acesso fisico
- [ ] Passwords partilhadas alteradas

**Financeiro:**
- [ ] Calculo dias ferias por gozar
- [ ] Notas de despesas pendentes submetidas
- [ ] Ultimo salario + compensacoes calculados
- [ ] Certificado de trabalho emitido

**Entrevista de Saida:**
- [ ] Entrevista marcada (30min, com RH)
- [ ] Motivo de saida documentado
- [ ] Feedback sobre empresa/equipa recolhido
- [ ] Sugestoes de melhoria registadas

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana onboard [nome]` | Gerar checklist onboarding completo |
| `adriana onboard day1 [nome]` | Gerar agenda dia 1 |
| `adriana onboard equipment [nome]` | Lista equipamento necessario |
| `adriana onboard accounts [nome]` | Lista contas a criar |
| `adriana offboard [nome]` | Gerar checklist offboarding |
| `adriana offboard access [nome]` | Lista acessos a revogar |
| `adriana onboard status` | Ver onboardings/offboardings em curso |

## Template de Output

```markdown
## Status Onboarding/Offboarding — [Periodo]

### Em Curso
| Colaborador | Tipo | Data | Progresso | Buddy |
|-------------|------|------|-----------|-------|
| [Nome] | Entrada | YYYY-MM-DD | 70% | [Nome] |
| [Nome] | Saida | YYYY-MM-DD | 40% | N/A |

### Metricas
- Tempo medio onboarding: X dias
- Satisfacao novos colaboradores: X/5
- Items pendentes: X
- Acessos por revogar: X
```

## Red Flags

- Colaborador comeca sem contrato assinado
- Equipamento nao pronto no dia 1
- Contas de email/ferramentas nao criadas no dia 1
- Sem buddy ou mentor designado
- Sem objectivos definidos para periodo experimental
- Offboarding: acessos nao revogados em 24h
- Offboarding: equipamento nao devolvido
- Sem entrevista de saida (perda de feedback)
- Documentacao de processos exclusivos nao transferida

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-docs** | Documentacao do colaborador arquivada |
| **adriana-facilities** | Posto de trabalho preparado |
| **adriana-inventory** | Material escritorio fornecido |
| **adriana-policies** | Manual colaborador e politicas entregues |
| **adriana-comms** | Anuncio de entrada/saida |
| **adriana-calendar** | Reunioes de onboarding no calendario |
| **adriana-sop** | SOPs de onboarding/offboarding |
| **dario-hr** | Gestao RH completa, contrato, ferias |
| **lucas-finance** | Processamento salarial e compensacoes |

## Contexto Portugal

- Periodo experimental: 90 dias (normal), 180 dias (cargos complexidade/responsabilidade), 240 dias (dirigentes/quadros superiores)
- Comunicacao SS: ate vespera do inicio (formulario online SS Directa)
- Pre-aviso demissao trabalhador: 30 dias (<2 anos), 60 dias (>=2 anos)
- Pre-aviso despedimento: varia conforme tipo e antiguidade
- Certificado de trabalho: obrigatório entregar ao colaborador
- RGPD: dados pessoais do ex-colaborador — retencao conforme finalidade
