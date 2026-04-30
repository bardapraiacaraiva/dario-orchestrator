---
name: adriana-policies
description: "ADRIANA Policy Management — create/review/update policies, version control, distribution, acknowledgement"
version: "1.0"
---

# ADRIANA-POLICIES: Gestao de Politicas

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** politica, regulamento, norma, codigo conduta, manual colaborador, regras internas, regulamento interno, procedimento, compliance, conformidade, revisao politica
**Trigger words (EN):** policy, regulation, code of conduct, employee handbook, internal rules, compliance, policy review, policy update, governance, standard

Activar quando o utilizador precisa de:
- Criar nova politica interna
- Rever ou actualizar politica existente
- Distribuir politicas aos colaboradores
- Gerir reconhecimento/assinatura de politicas
- Auditar conformidade com politicas
- Criar manual do colaborador

## Workflow Passo-a-Passo

### 1. Inventario de Politicas

Politicas essenciais para qualquer empresa PT:

| # | Politica | Obrigatoria? | Legislacao |
|---|----------|-------------|------------|
| 1 | Regulamento Interno | Sim (>50 colab.) | Codigo Trabalho Art. 99 |
| 2 | Politica RGPD/Privacidade | Sim | RGPD + Lei 58/2019 |
| 3 | Politica SST | Sim | Lei 102/2009 |
| 4 | Codigo de Conduta/Etica | Recomendada | — |
| 5 | Politica Anti-Assedio | Sim | Lei 73/2017 |
| 6 | Politica de Viagens e Despesas | Recomendada | — |
| 7 | Politica de Utilizacao TI | Recomendada | — |
| 8 | Politica de Trabalho Remoto | Recomendada | Lei 83/2021 |
| 9 | Politica de Compras | Recomendada | — |
| 10 | Politica de Ferias e Ausencias | Recomendada | Codigo Trabalho |
| 11 | Plano de Igualdade | Sim (>50 colab.) | Lei 62/2017 |
| 12 | Politica de Whistleblowing | Sim (>50 colab.) | Lei 93/2021 |

### 2. Template de Politica

```markdown
# [NOME DA POLITICA]

**Ref:** POL-YYYY-NNN
**Versao:** X.X
**Data aprovacao:** YYYY-MM-DD
**Proxima revisao:** YYYY-MM-DD
**Responsavel:** [Nome/Cargo]
**Aprovador:** [Nome/Cargo]
**Classificacao:** [Publica / Interna / Confidencial]

---

## 1. Objectivo
[Porque existe esta politica — 2-3 frases]

## 2. Ambito
[A quem se aplica: todos colaboradores, departamento X, etc.]

## 3. Definicoes
| Termo | Definicao |
|-------|-----------|
| [Termo] | [Definicao clara] |

## 4. Politica
### 4.1 [Topico Principal]
[Regras claras, directas, sem ambiguidade]

### 4.2 [Topico Secundario]
[Regras claras]

### 4.3 [Excepcoes]
[Quando e como se pode pedir excepcao]

## 5. Responsabilidades
| Papel | Responsabilidade |
|-------|-----------------|
| Colaborador | [O que deve fazer] |
| Chefia | [O que deve fazer] |
| RH | [O que deve fazer] |
| Direccao | [O que deve fazer] |

## 6. Incumprimento
[Consequencias do nao cumprimento — proporcional e legal]

## 7. Documentos Relacionados
- [Politica X — POL-YYYY-NNN]
- [SOP Y — SOP-YYYY-NNN]
- [Legislacao aplicavel]

## 8. Historico de Revisoes
| Versao | Data | Alteracao | Autor |
|--------|------|-----------|-------|
| 1.0 | YYYY-MM-DD | Versao inicial | [Nome] |
| 1.1 | YYYY-MM-DD | [Descricao alteracao] | [Nome] |

---
**Assinatura aprovacao:** _______________
**Data:** _______________
```

### 3. Ciclo de Vida da Politica

```
NECESSIDADE → RASCUNHO → REVISAO JURIDICA → APROVACAO DIRECCAO
                                                    ↓
DISTRIBUICAO → FORMACAO → RECONHECIMENTO → MONITORIZACAO → REVISAO
      ↑                                                       ↓
      └────────────── ACTUALIZACAO (nova versao) ─────────────┘
```

**Prazos de revisao:**
| Tipo Politica | Revisao | Nota |
|---------------|---------|------|
| RGPD/Privacidade | Anual | Ou quando legislacao muda |
| SST | Anual | Ou apos incidente |
| Regulamento Interno | Bianual | Ou mudanca significativa |
| Codigo Conduta | Bianual | — |
| Operacionais | Anual | — |
| Todas | Imediata | Quando legislacao aplicavel muda |

### 4. Distribuicao e Reconhecimento

**Processo:**
1. Publicar politica no repositorio central (Drive/SharePoint)
2. Enviar email a todos os abrangidos com link + resumo das mudancas
3. Sessao de esclarecimento (se mudanca significativa)
4. Recolher assinatura/reconhecimento digital
5. Registar quem assinou e quando
6. Follow-up a quem nao assinou em 7 dias

**Registo de Reconhecimento:**
| Colaborador | Politica | Versao | Data Leitura | Assinado | Notas |
|-------------|----------|--------|-------------|----------|-------|
| [Nome] | [POL-XXX] | 2.0 | YYYY-MM-DD | Sim | — |
| [Nome] | [POL-XXX] | 2.0 | — | Pendente | Lembrete enviado |

### 5. Auditoria de Conformidade

**Checklist trimestral:**
- [ ] Todas as politicas obrigatorias existem
- [ ] Nenhuma politica com revisao em atraso >3 meses
- [ ] 100% colaboradores assinaram politicas vigentes
- [ ] Novos colaboradores recebem politicas no onboarding
- [ ] Politicas acessiveis a todos (repositorio central)
- [ ] Historico de revisoes documentado
- [ ] Formacao realizada quando politica nova/actualizada

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana policy create [nome]` | Criar nova politica com template |
| `adriana policy review [ref]` | Iniciar revisao de politica |
| `adriana policy distribute [ref]` | Distribuir e recolher reconhecimento |
| `adriana policy audit` | Auditoria de conformidade |
| `adriana policy list` | Listar todas as politicas e estado |
| `adriana policy status [ref]` | Ver estado de reconhecimento |
| `adriana policy handbook` | Gerar manual do colaborador |

## Template de Output

```markdown
## Estado Politicas — [Data]

### Resumo
- Politicas activas: X
- Em revisao: X
- Revisao em atraso: X
- Taxa reconhecimento global: X%

### Politicas por Estado
| Ref | Politica | Versao | Revisao | Reconhecimento |
|-----|----------|--------|---------|----------------|
| POL-001 | [Nome] | 2.1 | OK | 95% |
| POL-002 | [Nome] | 1.0 | ATRASADA | 100% |

### Accoes Requeridas
1. [ ] [Politica X] — revisao em atraso 30 dias
2. [ ] [Colaborador Y] — assinatura pendente >7 dias
```

## Red Flags

- Politicas obrigatorias inexistentes (RGPD, SST, Anti-Assedio)
- Politica sem versao ou data de aprovacao
- Revisao em atraso >6 meses
- Colaboradores sem reconhecimento assinado
- Politicas contraditorias entre si
- Politica criada sem revisao juridica
- Linguagem ambigua que permite interpretacoes multiplas
- Consequencias de incumprimento desproporcionais ou ilegais
- Politicas nao acessiveis a todos os colaboradores
- Sem registo de quem aprovou a politica

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-docs** | Politicas seguem gestao documental |
| **adriana-onboarding** | Politicas entregues no onboarding |
| **adriana-comms** | Comunicacao de novas politicas |
| **adriana-sop** | SOPs complementam politicas |
| **adriana-travel** | Politica de viagens e despesas |
| **adriana-procurement** | Politica de compras |
| **adriana-archive** | Retencao de versoes anteriores |
| **dario-legal** | Revisao juridica de politicas |
| **dario-hr** | Regulamento interno e trabalho |
| **risco-rgpd** | Politica de privacidade e RGPD |
| **risco-etica** | Codigo de conduta e etica |

## Contexto Portugal

- Regulamento Interno: obrigatorio >50 colaboradores (CT Art. 99), enviar a ACT em 5 dias
- Anti-Assedio: obrigatorio com codigo de boa conduta (Lei 73/2017)
- Whistleblowing: canal de denuncias obrigatorio >50 colaboradores (Lei 93/2021)
- Igualdade: plano obrigatorio >50 colaboradores (Lei 62/2017)
- RGPD: DPO obrigatorio se tratamento em grande escala
- Trabalho remoto: acordo escrito obrigatorio (Lei 83/2021)
- Todas as politicas devem estar em portugues
