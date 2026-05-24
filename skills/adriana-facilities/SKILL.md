---
name: adriana-facilities
description: "ADRIANA Facilities — office layout, maintenance, equipment inventory, H&S, cleaning, access control"
version: "1.0"
---

# ADRIANA-FACILITIES: Gestao de Instalacoes

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** instalacoes, escritorio, manutencao, equipamento, seguranca trabalho, limpeza, controlo acesso, layout, espaco, ar condicionado, avaria, reparacao, higiene seguranca, SHST, extintor, alarme
**Trigger words (EN):** facilities, office, maintenance, equipment, health safety, cleaning, access control, layout, workspace, HVAC, repair, fire safety, building management

Activar quando o utilizador precisa de:
- Gerir layout ou espacos de escritorio
- Planear ou rastrear manutencao
- Inventariar equipamento fixo
- Garantir conformidade H&S (higiene e seguranca)
- Gerir limpeza e higienizacao
- Controlar acessos fisicos

## Workflow Passo-a-Passo

### 1. Inventario de Instalacoes

```markdown
# Ficha de Instalacao
**Morada:** [Morada completa]
**Area total:** XXX m2
**Area util:** XXX m2
**Pisos:** X
**Lotacao maxima:** XX pessoas
**Contrato arrendamento:** [Ref] — Validade: YYYY-MM-DD

## Espacos
| ID | Espaco | Area m2 | Capacidade | Equipamento |
|----|--------|---------|------------|-------------|
| S01 | Sala reuniao A | 15 | 8 | Projector, whiteboard |
| S02 | Sala reuniao B | 10 | 4 | TV, webcam |
| O01 | Open space | 80 | 20 | 20 secretarias |
| K01 | Copa/cozinha | 12 | - | Micro-ondas, frigorifico |
| W01 | WC M | 8 | - | 2 cabines |
| W02 | WC F | 8 | - | 2 cabines |
| A01 | Armazem | 20 | - | Estantes |
```

### 2. Plano de Manutencao

**Manutencao Preventiva (calendario anual):**

| Equipamento | Frequencia | Ultimo | Proximo | Responsavel |
|-------------|-----------|--------|---------|-------------|
| AVAC/Ar condicionado | Trimestral | YYYY-MM | YYYY-MM | [Empresa] |
| Extintores | Anual | YYYY-MM | YYYY-MM | [Empresa] |
| Elevador | Mensal | YYYY-MM | YYYY-MM | [Empresa] |
| Sistema alarme | Semestral | YYYY-MM | YYYY-MM | [Empresa] |
| Desinfestacao | Trimestral | YYYY-MM | YYYY-MM | [Empresa] |
| Canalizacao | Anual | YYYY-MM | YYYY-MM | [Empresa] |
| Electricidade | Anual | YYYY-MM | YYYY-MM | [Empresa] |
| UPS/Gerador | Semestral | YYYY-MM | YYYY-MM | [Empresa] |

**Manutencao Correctiva (registo de ocorrencias):**

```markdown
# Pedido Manutencao
**Ref:** MAN-YYYY-NNN
**Data:** YYYY-MM-DD
**Reportado por:** [Nome]
**Local:** [Espaco ID]
**Urgencia:** Critica / Alta / Media / Baixa

## Descricao
[O que aconteceu / o que precisa de reparacao]

## Accao Tomada
- Data resolucao: YYYY-MM-DD
- Tecnico: [Nome/Empresa]
- Custo: €XX.XX
- Garantia: Sim/Nao
```

### 3. Higiene e Seguranca no Trabalho (SHST)

**Obrigacoes legais (Lei 102/2009):**
- [ ] Servico de SST contratado (interno ou externo)
- [ ] Avaliacao de riscos actualizada (anual)
- [ ] Plano de emergencia interno afixado
- [ ] Exercicio de evacuacao (anual minimo)
- [ ] Primeiros socorros: kit verificado e completo
- [ ] Extintores: verificacao anual, revisao 5 anos
- [ ] Sinalizacao de seguranca (saidas, extintores, quadro electrico)
- [ ] Formacao SST colaboradores (admissao + periodica)
- [ ] Medicina do trabalho: exames em dia
- [ ] Registo de acidentes de trabalho

**Checklist Mensal H&S:**
- [ ] Extintores acessiveis e com pressao
- [ ] Saidas de emergencia desobstruidas
- [ ] Iluminacao de emergencia funcional
- [ ] Kit primeiros socorros completo
- [ ] Quadro electrico sem obstrucoes
- [ ] Cabos electricos sem danos visiveis
- [ ] Temperatura e ventilacao adequadas (18-22C)
- [ ] Ruido dentro dos limites (<80dB)

### 4. Limpeza

| Area | Frequencia | Horario | Observacoes |
|------|-----------|---------|-------------|
| WCs | Diario | 08:00 + 14:00 | Produtos e reposicao |
| Open space | Diario | 07:00 | Aspirar + limpar |
| Salas reuniao | Diario | 07:00 | Limpar mesa + quadro |
| Copa | Diario | 07:00 + 18:00 | Loica, superficies |
| Vidros | Quinzenal | Sabado | Interior + exterior |
| Carpetes | Mensal | Sabado | Limpeza profunda |
| Desinfeccao geral | Trimestral | Fim-de-semana | Todos os espacos |

### 5. Controlo de Acessos

| Tipo Acesso | Metodo | Horario | Quem |
|-------------|--------|---------|------|
| Porta principal | Cartao + PIN | 07:00-22:00 | Todos colaboradores |
| Fora de horas | Cartao + autorizacao | 22:00-07:00 | Autorizados |
| Sala servidores | Cartao + biometrico | 24h | IT apenas |
| Armazem | Chave fisica | Horario laboral | Responsavel facilities |
| Visitantes | Registo recepcao | Horario laboral | Acompanhados |

### 6. Inventario Equipamento Fixo

| ID | Equipamento | Marca/Modelo | Localizacao | Data compra | Garantia ate | Estado |
|----|-------------|-------------|-------------|-------------|-------------|--------|
| EQ001 | Projector | Epson EB-X51 | Sala A | 2025-03 | 2027-03 | Activo |
| EQ002 | Impressora | HP LaserJet | Open space | 2024-06 | 2026-06 | Activo |
| EQ003 | Ar condicionado | Daikin FTXM | Sala B | 2023-01 | 2028-01 | Activo |

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana facilities inventory` | Listar espacos e equipamento |
| `adriana facilities maintenance [pedido]` | Registar pedido manutencao |
| `adriana facilities schedule` | Calendario manutencao preventiva |
| `adriana facilities hse-check` | Checklist mensal H&S |
| `adriana facilities cleaning` | Plano de limpeza |
| `adriana facilities access [accao]` | Gerir acessos (add/remove/list) |
| `adriana facilities report` | Relatorio mensal instalacoes |

## Template de Output

```markdown
## Relatorio Instalacoes — [Mes/Ano]

### Estado Geral
- Ocupacao media: X% (XX/XX postos)
- Pedidos manutencao: X (resolvidos: X, pendentes: X)
- Tempo medio resolucao: X dias
- Custo manutencao: €XX.XXX

### Manutencao Preventiva
- Proximas intervencoes: [Lista]
- Em atraso: [Lista]

### H&S
- Ultima inspeccao: YYYY-MM-DD — Resultado: OK/NOK
- Proximo simulacro: YYYY-MM-DD
- Incidentes no periodo: X

### Alertas
- [Equipamento X]: garantia expira em 30 dias
- [Manutencao Y]: atrasada X dias
```

## Red Flags

- Extintores fora de validade ou sem pressao
- Saidas de emergencia bloqueadas
- Manutencao preventiva em atraso >30 dias
- Temperatura fora do intervalo 18-22C persistentemente
- Avaria em sistema de seguranca sem resolucao em 24h
- Quadro electrico obstruido ou danificado
- Falta de exercicio de evacuacao anual
- Acessos de ex-colaboradores nao revogados
- Sem servico SST contratado (ilegal)
- Medicina do trabalho: exames em atraso

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-onboarding** | Preparar posto trabalho para novo colaborador |
| **adriana-inventory** | Material e consumiveis de limpeza/manutencao |
| **adriana-procurement** | Contratos com fornecedores de manutencao |
| **adriana-reception** | Gestao de salas e acessos visitantes |
| **adriana-calendar** | Agendamento manutencao preventiva |
| **adriana-reporting** | KPIs de facilities no dashboard mensal |
| **adriana-archive** | Registo legal de inspeccoes e acidentes |
| **adriana-policies** | Politica de utilizacao de espacos |

## Contexto Portugal

- SST: Lei 102/2009 (Regime Juridico Seguranca e Saude no Trabalho)
- Medicina trabalho: exame admissao + periodico (anual ou bianual conforme risco)
- Incendio: Regime Juridico SCIE (DL 220/2008) — categorias de risco 1-4
- Acessibilidade: DL 163/2006 (acessibilidade para pessoas com mobilidade reduzida)
- Temperatura: minimo 18C em trabalho sedentario (recomendado 20-22C)
- Ruido: limite 80dB(A) sem proteccao, 85dB(A) com proteccao (DL 182/2006)


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **adriana-facilities** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in adriana-facilities:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->
