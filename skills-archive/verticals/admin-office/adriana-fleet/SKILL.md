---
name: adriana-fleet
description: "ADRIANA Fleet/Asset Management — vehicles, maintenance, insurance, fuel, depreciation"
version: "1.0"
---

# ADRIANA-FLEET: Gestao de Frota e Activos

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** frota, veiculo, carro empresa, manutencao automovel, seguro auto, combustivel, IUC, IPO, km, quilometragem, leasing, renting, via verde, depreciacao, activo fixo
**Trigger words (EN):** fleet, vehicle, company car, car maintenance, insurance, fuel, mileage, leasing, renting, depreciation, fixed asset, asset management

Activar quando o utilizador precisa de:
- Gerir frota de veiculos
- Rastrear manutencao automovel
- Controlar custos de combustivel
- Gerir seguros e documentacao de veiculos
- Calcular depreciacao de activos
- Planear renovacao de frota
- Gerir activos fixos (nao so veiculos)

## Workflow Passo-a-Passo

### 1. Ficha de Veiculo

```markdown
# Ficha Veiculo
**ID Frota:** VEH-NNN
**Matricula:** XX-XX-XX
**Marca/Modelo:** [Marca Modelo]
**Ano:** YYYY
**Combustivel:** Gasolina / Diesel / Hibrido / Electrico
**Cilindrada:** XXXX cc
**Cor:** [Cor]
**VIN:** [Numero chassis]

## Aquisicao
| Campo | Valor |
|-------|-------|
| Tipo | Compra / Leasing / Renting |
| Data aquisicao | YYYY-MM-DD |
| Valor aquisicao | €XX.XXX (s/IVA) |
| Fornecedor/Financeira | [Nome] |
| Contrato ref | [Ref] |
| Prestacao mensal | €XXX (se leasing/renting) |
| Fim contrato | YYYY-MM-DD |

## Documentacao
| Documento | Validade | Estado |
|-----------|----------|--------|
| Seguro | YYYY-MM-DD | Activo |
| IPO (Inspeccao) | YYYY-MM-DD | Activo |
| IUC | YYYY (pago) | Pago |
| Via Verde | Activo | — |
| Dístico estacionamento | YYYY-MM-DD | Activo |

## Atribuicao
| Campo | Valor |
|-------|-------|
| Utilizador principal | [Nome] |
| Departamento | [Dept] |
| Uso | Servico / Atribuido / Pool |
| Km actuais | XX.XXX km |
```

### 2. Plano de Manutencao

**Manutencao preventiva (por km ou tempo — o que ocorrer primeiro):**

| Intervencao | Intervalo km | Intervalo tempo | Custo estimado |
|-------------|-------------|-----------------|----------------|
| Mudanca oleo + filtro | 15.000 km | 12 meses | €80-150 |
| Filtro ar | 30.000 km | 24 meses | €30-50 |
| Pastilhas travao | 30.000 km | 24 meses | €100-200 |
| Pneus (4) | 40.000 km | 36 meses | €300-600 |
| Correia distribuicao | 100.000 km | 5 anos | €400-800 |
| Revisao geral | 15.000 km | 12 meses | €200-400 |
| AC (recarga) | — | 24 meses | €60-100 |
| Bateria | — | 4-5 anos | €80-150 |

**Registo de intervencao:**
```markdown
# Registo Manutencao
**Veiculo:** VEH-NNN ([Matricula])
**Data:** YYYY-MM-DD
**Km:** XX.XXX
**Tipo:** Preventiva / Correctiva / Acidente
**Oficina:** [Nome, local]

## Servicos Realizados
| Servico | Pecas | Custo |
|---------|-------|-------|
| [Descricao] | [Se aplicavel] | €XX.XX |

## Totais
- Mao de obra: €XX.XX
- Pecas: €XX.XX
- **Total (s/IVA):** €XX.XX
- **IVA 23%:** €XX.XX
- **Total (c/IVA):** €XX.XX

## Proxima Intervencao
- Tipo: [Revisao / Pneus / etc.]
- Km: XX.XXX ou Data: YYYY-MM-DD
```

### 3. Controlo de Combustivel

**Registo mensal por veiculo:**
| Data | Km | Litros | €/Litro | Total | Km/L |
|------|-----|--------|---------|-------|------|
| DD/MM | XX.XXX | XX.X | €X.XX | €XX.XX | X.X |

**Metricas:**
- Consumo medio: X.X L/100km
- Custo mensal: €XXX
- Custo por km: €X.XX
- Anomalias: >20% acima da media = investigar

### 4. Gestao de Seguros

**Tipos de seguro e cobertura:**
| Cobertura | Minimo legal | Recomendado empresa |
|-----------|-------------|-------------------|
| Responsabilidade civil | Obrigatorio | Obrigatorio |
| Danos proprios | Opcional | Sim (veiculos <5 anos) |
| Furto/roubo | Opcional | Sim |
| Assistencia viagem | Opcional | Sim |
| Ocupantes | Opcional | Recomendado |
| Vidros | Opcional | Sim |

**Calendario de renovacoes:**
| Veiculo | Seguradora | Apolice | Renovacao | Premio anual |
|---------|-----------|---------|-----------|-------------|
| VEH-001 | [Nome] | [Ref] | YYYY-MM-DD | €XXX |
| VEH-002 | [Nome] | [Ref] | YYYY-MM-DD | €XXX |

### 5. Depreciacao e Activos Fixos

**Taxas de depreciacao (PT — Decreto Regulamentar 25/2009):**
| Activo | Taxa anual | Vida util |
|--------|-----------|-----------|
| Veiculos ligeiros | 25% | 4 anos |
| Veiculos pesados | 20% | 5 anos |
| Mobiliario escritorio | 12.5% | 8 anos |
| Equipamento informatico | 33.33% | 3 anos |
| Software | 33.33% | 3 anos |
| Equipamento diverso | 14.28%-20% | 5-7 anos |
| Edificios | 2%-5% | 20-50 anos |

**Ficha de activo fixo:**
```markdown
# Activo Fixo
**ID:** AF-YYYY-NNN
**Descricao:** [Descricao]
**Categoria:** [Veiculo / IT / Mobiliario / etc.]
**Data aquisicao:** YYYY-MM-DD
**Valor aquisicao:** €XX.XXX
**Taxa depreciacao:** XX%
**Depreciacao acumulada:** €XX.XXX
**Valor liquido contabilistico:** €XX.XXX
**Localizacao:** [Onde esta]
**Estado:** Activo / Abatido / Vendido
**Responsavel:** [Nome]
```

### 6. Tributacao Autonoma Veiculos (Portugal)

| Custo aquisicao | Taxa TA (lucro) | Taxa TA (prejuizo) |
|-----------------|-----------------|---------------------|
| <€27.500 | 10% | 20% |
| €27.500-€35.000 | 27.5% | 37.5% |
| >€35.000 | 35% | 45% |
| Hibridos plug-in | 50% das taxas acima | 50% + 10pp |
| Electricos | 0% (se <€62.500) | 10% (se <€62.500) |

*Nota: Valores limites sujeitos a actualizacao anual no OE*

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana fleet list` | Listar todos os veiculos/activos |
| `adriana fleet vehicle [id]` | Ficha completa do veiculo |
| `adriana fleet maintenance [id]` | Registar manutencao |
| `adriana fleet fuel [id]` | Registar abastecimento |
| `adriana fleet insurance` | Calendario seguros |
| `adriana fleet ipo` | Calendario IPOs |
| `adriana fleet depreciation` | Mapa de depreciacoes |
| `adriana fleet costs [periodo]` | Custos por veiculo |
| `adriana fleet asset [accao]` | Gerir activo fixo |

## Template de Output

```markdown
## Relatorio Frota — [Periodo]

### Resumo
- Veiculos activos: X
- Km totais percorridos: XX.XXX
- Custo total frota: €XX.XXX
  - Combustivel: €XX.XXX (XX%)
  - Manutencao: €XX.XXX (XX%)
  - Seguros: €XX.XXX (XX%)
  - IUC: €XX.XXX (XX%)
  - Leasing/Renting: €XX.XXX (XX%)
- Custo medio por km: €X.XX

### Alertas
| Veiculo | Alerta | Prazo |
|---------|--------|-------|
| VEH-XXX | IPO expira | DD/MM |
| VEH-XXX | Seguro renova | DD/MM |
| VEH-XXX | Revisao devida | XX.XXX km |

### Activos Fixos
- Total activos: X — Valor bruto: €XXX.XXX
- Depreciacao acumulada: €XXX.XXX
- Valor liquido: €XXX.XXX
```

## Red Flags

- IPO expirado (veiculo nao pode circular legalmente)
- Seguro expirado (ilegal + risco financeiro enorme)
- IUC nao pago (multa + juros)
- Manutencao preventiva em atraso >3 meses
- Consumo combustivel >30% acima da media (uso indevido?)
- Veiculo sem utilizador atribuido (custo sem retorno)
- Activo fixo sem localizacao conhecida
- Depreciacao nao calculada/registada mensalmente
- Veiculo >€35.000 sem analise de tributacao autonoma
- Via Verde com portagens pessoais nao reembolsadas

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-procurement** | Compra/leasing de veiculos e equipamento |
| **adriana-travel** | Veiculos empresa em viagens |
| **adriana-facilities** | Activos fixos de escritorio |
| **adriana-reporting** | Custos frota no dashboard |
| **adriana-policies** | Politica de utilizacao de veiculos |
| **adriana-sop** | SOP de registo km e combustivel |
| **lucas-finance** | Depreciacao, IUC, tributacao autonoma |
| **dario-legal** | Contratos de leasing/renting |

## Contexto Portugal

- IUC: pago anualmente no mes de aniversario da matricula
- IPO: obrigatoria apos 4 anos (ligeiros), depois bianual, apos 8 anos anual
- Seguro: obrigatorio RC minimo — DL 291/2007
- Tributacao autonoma: CIRC Art. 88 — veiculos ligeiros
- IVA: 50% dedutivel em veiculos comerciais, 100% em veiculos mercadorias
- Limite depreciacao fiscal: €25.000 (veiculos ligeiros) / €50.000 (electricos)
- Via Verde: portagens empresariais sao custo fiscal aceite
- Combustivel: IVA 50% dedutivel (gasóleo), 0% (gasolina, excepto GPL/GN)


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **adriana-fleet** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in adriana-fleet:**

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
