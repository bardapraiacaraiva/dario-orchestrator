---
name: adriana-archive
description: "ADRIANA Records Management — retention schedules, RGPD data inventory, legal holds, destruction"
version: "1.0"
---

# ADRIANA-ARCHIVE: Gestao de Arquivo e Retencao

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** arquivo, retencao, destruicao documentos, RGPD, dados pessoais, inventario dados, legal hold, conservacao, eliminacao, prazo retencao, data retention, registos, proteccao dados
**Trigger words (EN):** archive, retention, records management, document destruction, GDPR, data inventory, legal hold, data retention, records disposal, compliance, data mapping

Activar quando o utilizador precisa de:
- Definir politicas de retencao documental
- Criar inventario de dados pessoais (RGPD)
- Implementar legal holds
- Planear destruicao segura de documentos
- Auditar conformidade de arquivo
- Mapear fluxos de dados pessoais

## Workflow Passo-a-Passo

### 1. Tabela de Retencao por Tipo de Documento (Portugal)

| Categoria | Tipo Documento | Retencao Minima | Base Legal | Apos Retencao |
|-----------|---------------|-----------------|------------|---------------|
| **Fiscal** | Facturas emitidas/recebidas | 12 anos | CIVA Art. 52 | Destruir |
| **Fiscal** | Livros contabilidade | 10 anos | CIRC Art. 123 | Destruir |
| **Fiscal** | Declaracoes fiscais | 10 anos | LGT Art. 36 | Destruir |
| **Fiscal** | Recibos de vencimento | 10 anos | CIRC Art. 123 | Destruir |
| **Laboral** | Contrato trabalho | 5 anos apos termino | CT Art. 337 | Destruir |
| **Laboral** | Registo de ponto | 5 anos | CT Art. 202 | Destruir |
| **Laboral** | Ficha colaborador | 5 anos apos saida | CT | Destruir |
| **Laboral** | Acidentes trabalho | 5 anos | Lei 102/2009 | Destruir |
| **Comercial** | Contratos com clientes | 10 anos apos termino | CC Art. 309 | Avaliar |
| **Comercial** | Propostas | 3 anos | Operacional | Destruir |
| **Comercial** | Correspondencia comercial | 5 anos | Ccom Art. 40 | Destruir |
| **Societario** | Actas assembleia | Permanente | CSC | Conservar |
| **Societario** | Estatutos/pacto social | Permanente | CSC | Conservar |
| **Legal** | Processos judiciais | 10 anos apos decisao | CPC | Avaliar |
| **SST** | Avaliacoes risco | 5 anos | Lei 102/2009 | Destruir |
| **RGPD** | Consentimentos | Duracao + 5 anos | RGPD Art. 7 | Destruir |
| **RGPD** | Contratos subcontratantes | Duracao + 5 anos | RGPD Art. 28 | Destruir |

### 2. Inventario de Dados Pessoais (ROPA — RGPD Art. 30)

```markdown
# Registo de Actividades de Tratamento (ROPA)
**Responsavel tratamento:** [Empresa, NIF, morada]
**DPO:** [Nome, contacto] (se aplicavel)
**Data ultima actualizacao:** YYYY-MM-DD

## Actividade de Tratamento #N
| Campo | Valor |
|-------|-------|
| Nome actividade | [Ex: Gestao RH] |
| Finalidade | [Ex: Processamento salarial] |
| Base legal | [Execucao contrato / Obrigacao legal / Consentimento / Interesse legitimo] |
| Categorias titulares | [Colaboradores / Clientes / Fornecedores] |
| Categorias dados | [Nome, NIF, morada, IBAN, contacto] |
| Dados sensiveis? | [Sim/Nao — se sim, quais] |
| Origem dados | [Titular / Terceiro / Publico] |
| Destinatarios | [Contabilidade, SS, AT, Seguradora] |
| Transferencia fora UE? | [Sim/Nao — se sim, garantias] |
| Prazo retencao | [X anos / critérios] |
| Medidas seguranca | [Encriptacao, controlo acesso, backup] |
| Sistema/aplicacao | [Software/plataforma onde dados estao] |
```

### 3. Classificacao de Documentos

| Nivel | Classificacao | Descricao | Exemplos |
|-------|-------------|-----------|----------|
| 1 | **Permanente** | Nunca destruir | Actas, estatutos, propriedade intelectual |
| 2 | **Retencao longa** | >10 anos | Fiscal, contabilidade |
| 3 | **Retencao media** | 5-10 anos | Contratos, laboral |
| 4 | **Retencao curta** | 1-5 anos | Propostas, correspondencia |
| 5 | **Temporario** | <1 ano | Rascunhos, versoes intermedias |

### 4. Processo de Destruicao

**Pre-destruicao:**
- [ ] Verificar se documento atingiu prazo de retencao
- [ ] Verificar se existe legal hold activo
- [ ] Verificar se existe auditoria ou inspeccao pendente
- [ ] Obter autorizacao do responsavel

**Metodos de destruicao:**
| Tipo | Metodo | Nivel seguranca |
|------|--------|-----------------|
| Papel (normal) | Trituracao nivel P-3 | Medio |
| Papel (confidencial) | Trituracao nivel P-5 | Alto |
| Digital (normal) | Delete + backup rotation | Medio |
| Digital (confidencial) | Wipe certificado + certificado destruicao | Alto |
| Discos/media | Destruicao fisica | Maximo |

**Registo de destruicao:**
```markdown
# Certificado de Destruicao
**Ref:** DEST-YYYY-NNN
**Data:** YYYY-MM-DD
**Metodo:** [Trituracao / Wipe / Destruicao fisica]
**Executado por:** [Nome/Empresa]
**Testemunha:** [Nome]

## Documentos Destruidos
| # | Descricao | Quantidade | Periodo | Classificacao |
|---|-----------|-----------|---------|---------------|
| 1 | [Tipo documento] | XX caixas/ficheiros | YYYY-YYYY | [Nivel] |

**Confirmacao:** Certifico que os documentos acima foram destruidos de forma
irrecuperavel, em conformidade com a politica de retencao da empresa.

Assinatura: _______________ Data: _______________
```

### 5. Legal Hold

Quando activar: litigio actual ou potencial, auditoria, inspeccao fiscal

```markdown
# Aviso de Legal Hold
**Ref:** LH-YYYY-NNN
**Data emissao:** YYYY-MM-DD
**Emitido por:** [Dept. Juridico / Compliance]

## Instrucoes
A partir desta data, TODOS os documentos (fisicos e digitais) relacionados
com [assunto] devem ser preservados integralmente.

**Ambito:**
- Periodo: [De YYYY-MM-DD a YYYY-MM-DD]
- Departamentos: [Lista]
- Tipos documento: [Lista]
- Palavras-chave: [Lista]

**Proibicoes:**
- NAO destruir, alterar ou mover documentos abrangidos
- NAO eliminar emails ou mensagens relacionados
- NAO modificar backups que contenham documentos abrangidos

**Duracao:** Ate levantamento formal por escrito.
**Contacto:** [Nome, email] para duvidas.
```

### 6. Arquivo Fisico vs Digital

| Aspecto | Fisico | Digital |
|---------|--------|---------|
| Localizacao | Arquivo morto + off-site | Cloud + backup local |
| Organizacao | Caixas numeradas + inventario | Pastas + metadados |
| Acesso | Pedido a responsavel (24-48h) | Pesquisa + permissoes |
| Seguranca | Fechadura + acesso restrito | Encriptacao + MFA |
| Destruicao | Trituracao certificada | Wipe + certificado |
| Custo | Espaco + manutencao | Storage + licencas |

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana archive retention [tipo]` | Consultar prazo retencao |
| `adriana archive inventory` | Inventario dados pessoais (ROPA) |
| `adriana archive schedule` | Calendario de destruicao |
| `adriana archive hold [assunto]` | Activar legal hold |
| `adriana archive destroy [ref]` | Registar destruicao |
| `adriana archive audit` | Auditoria conformidade arquivo |
| `adriana archive search [query]` | Pesquisar no arquivo |

## Template de Output

```markdown
## Estado Arquivo — [Data]

### Metricas
- Documentos em arquivo: X (fisico: X, digital: X)
- Legal holds activos: X
- Documentos elegíveis destruicao: X
- Conformidade RGPD: X% (ROPA completo?)

### Retencao
- Em prazo: X documentos
- Expirados (destruir): X documentos
- Permanentes: X documentos

### Accoes Requeridas
1. [ ] Destruir [X] documentos expirados
2. [ ] Actualizar ROPA — ultimo update [data]
3. [ ] Legal hold LH-XXX — revisao em [data]
```

## Red Flags

- Documentos retidos alem do prazo sem justificacao (violacao RGPD)
- ROPA inexistente ou desactualizado (obrigacao RGPD Art. 30)
- Destruicao sem certificado/registo
- Documentos destruidos durante legal hold
- Dados pessoais sem base legal identificada
- Backup de dados pessoais nao incluido no prazo de retencao
- Arquivo fisico sem controlo de acesso
- Falta de inventario de arquivo fisico
- Dados sensiveis (saude, etnia, politica) sem DPIA

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-docs** | Ciclo de vida documental termina no arquivo |
| **adriana-policies** | Politica de retencao e privacidade |
| **adriana-onboarding** | Dados de ex-colaboradores |
| **adriana-facilities** | Espaco fisico de arquivo |
| **adriana-sop** | SOP de destruicao segura |
| **risco-rgpd** | Conformidade RGPD completa |
| **dario-legal** | Legal holds e litigios |
| **lucas-finance** | Retencao documentos fiscais |

## Contexto Portugal

- RGPD: Regulamento (UE) 2016/679 + Lei 58/2019
- CNPD: Comissao Nacional Proteccao Dados — autoridade supervisora PT
- Retencao fiscal: 10-12 anos conforme tipo (mais longo da UE)
- Documentos electronicos: validade legal se assinatura digital qualificada
- Direito ao esquecimento: RGPD Art. 17 — eliminar quando prazo legal permite
- Notificacao violacao dados: 72h a CNPD (RGPD Art. 33)
- DPIA obrigatoria: tratamento grande escala dados sensiveis (RGPD Art. 35)
