---
name: diva-energy
description: Energy certification preparation (SCE Portugal) — covers REH residential and RECS commercial requirements, building envelope analysis, HVAC efficiency, renewable energy, solar thermal obligations, and improvement recommendations. Triggers on "certificacao energetica", "energy certification", "SCE", "classe energetica", "eficiencia energetica", "REH", "RECS", "NZEB".
license: MIT
---

# DIVA Skill — Energy Certification (SCE Portugal)

Prepares comprehensive energy certification analysis for Portuguese buildings under the SCE (Sistema de Certificacao Energetica dos Edificios). Covers both REH (residential) and RECS (commercial/services) regulatory frameworks, building envelope assessment, HVAC systems evaluation, renewable energy integration, and cost-ranked improvement recommendations.

## When to activate

- Client needs energy certification for a new build, renovation, or sale/rental
- Pre-construction energy class simulation (targeting B- minimum for new/major rehab)
- Building envelope optimization during design phase
- HVAC system specification with energy performance targets
- NZEB (Nearly Zero Energy Building) compliance check
- Renovation project where energy class upgrade is a goal or legal requirement

Do NOT use for:
- General sustainability consulting without SCE context
- Industrial process energy audits (not covered by REH/RECS)
- Buildings exempt from SCE (military, religious, temporary <2 years)

## Regulatory framework (reference)

| Regulation | Scope | Key requirement |
|---|---|---|
| DL 118/2013 | SCE system framework | Mandatory certification for sale/rent |
| Portaria 349-B/2013 | REH — residential | U-values, Nic, Nvc, Nac, Ntc |
| Portaria 349-D/2013 | RECS — commercial | IEE (energy use intensity), minimum renewables |
| DL 101-D/2020 | NZEB transposition | All new buildings NZEB from Jan 2021 |
| Despacho 15793-F/2013 | Climate zones | I1/I2/I3 (winter), V1/V2/V3 (summer) |

Minimum classes:
- **New construction:** B- (since 2013)
- **Major rehabilitation:** B- (>25% envelope or >25% HVAC replacement)
- **Existing buildings:** No minimum for sale/rent (but class affects value)
- **Public buildings >250m2:** Must display DEC (Declaracao de Conformidade Energetica)

## Workflow

### 1. Identify building type and scope

Determine:
- **Building type:** residential (REH) or commercial/services (RECS)
- **Situation:** new build, major rehabilitation, existing (sale/rent), voluntary upgrade
- **Climate zone:** based on municipality (NUTS III) — affects heating/cooling degree-days
- **Gross floor area and conditioned area (Ap)**
- **Number of floors, orientation, building shape factor (Ff)**

### 2. Building envelope analysis

Evaluate each component against reference U-values for the climate zone:

| Element | I1 max (W/m2.K) | I2 max (W/m2.K) | I3 max (W/m2.K) |
|---|---|---|---|
| External walls | 0.50 | 0.40 | 0.35 |
| Roof (horizontal) | 0.40 | 0.35 | 0.30 |
| Floor | 0.40 | 0.35 | 0.30 |
| Windows (Uw+gT) | 2.80 | 2.40 | 2.20 |

Check:
- Wall composition (ETICS, double wall, single leaf + insulation)
- Roof insulation (XPS, EPS, PIR thickness)
- Floor insulation (above crawl space, slab-on-grade, over garage)
- Windows (frame material, glazing type, gas fill, solar factor gT)
- Thermal bridges (linear psi-values at junctions)
- Airtightness (n50 value if blower door test available)

### 3. HVAC systems evaluation

For REH:
- **Heating (Nic):** system type, nominal efficiency, aux energy
- **Cooling (Nvc):** system type, EER, aux energy
- **DHW (Nac):** system type, efficiency, storage losses, solar contribution

For RECS:
- **IEE (Indicador de Eficiencia Energetica):** kWh/m2.year by end-use
- **HVAC central systems:** COP/EER, distribution losses, control systems
- **Lighting power density:** W/m2 vs reference, control type
- **Elevators, pumps, other technical systems**

### 4. Renewable energy assessment

Check compliance with minimum renewable contribution:
- **Solar thermal:** mandatory for DHW in new builds (DL 118/2013, Art. 27)
  - Exception: if technically unfeasible (shading, orientation, structural)
  - Minimum: Esolar >= 50% of DHW needs (REH)
- **Photovoltaic:** contribution to Eren,p (primary energy from renewables)
- **Heat pumps:** renewable fraction per EN 14825 (SPF > 2.5)
- **Biomass:** if used, efficiency and PM emissions compliance

### 5. Calculate energy indicators

For REH:
```
Ntc = (Nic x fi,c + Nvc x fv,c + Nac x fa,c) / Nt
```
Where:
- Nic = heating needs (kWh/m2.year)
- Nvc = cooling needs (kWh/m2.year)
- Nac = DHW needs (kWh/m2.year)
- Nt = reference total primary energy
- R_Ntc = Ntc/Nt ratio determines energy class

| Class | R_Ntc range |
|---|---|
| A+ | <= 0.25 |
| A  | 0.26 - 0.50 |
| B  | 0.51 - 0.75 |
| B- | 0.76 - 1.00 |
| C  | 1.01 - 1.50 |
| D  | 1.51 - 2.00 |
| E  | 2.01 - 2.50 |
| F  | > 2.50 |

### 6. Improvement recommendations

Rank by cost-benefit (ROI / payback years):

1. **Quick wins (payback <3 years):** LED lighting, DHW timer, smart thermostat, draught sealing
2. **Envelope improvements (3-8 years):** ETICS, roof insulation, window replacement
3. **Systems upgrade (5-12 years):** heat pump, solar thermal, condensing boiler
4. **Major investment (8-20 years):** PV system, MVHR, full NZEB retrofit

Each recommendation includes:
- Estimated cost (EUR)
- Energy savings (kWh/year)
- Class improvement potential
- Applicable incentives (Fundo Ambiental, PRR, IFRRU 2020)

## Output template

```markdown
---
project: <project-name>
date: YYYY-MM-DD
type: energy-certification-prep
building_type: residential|commercial
regulation: REH|RECS
climate_zone: I1-V2
current_class: <X>
target_class: <Y>
tags: [energia, SCE, certificacao, <project>]
---

# Preparacao Certificacao Energetica — <Project Name>

## 1. Dados do Edificio
- **Tipo:** Residencial / Comercial
- **Localizacao:** <municipio>, zona climatica <Ix-Vy>
- **Area util (Ap):** <X> m2
- **N. pisos:** <X>
- **Fator de forma (Ff):** <X>
- **Ano de construcao:** <X>

## 2. Envolvente
| Elemento | Composicao | U actual (W/m2.K) | U ref | Conforme? |
|---|---|---|---|---|
| Paredes ext. | ... | ... | ... | Sim/Nao |
| Cobertura | ... | ... | ... | Sim/Nao |
| Pavimento | ... | ... | ... | Sim/Nao |
| Vaos envidracados | ... | ... | ... | Sim/Nao |

### Pontes termicas
- ...

## 3. Sistemas Tecnicos
| Sistema | Tipo | Eficiencia | Ref. minima | Conforme? |
|---|---|---|---|---|
| Aquecimento | ... | ... | ... | ... |
| Arrefecimento | ... | ... | ... | ... |
| AQS | ... | ... | ... | ... |
| Solar termico | ... | ... | Obrigatorio | ... |

## 4. Indicadores Energeticos
- **Nic:** <X> kWh/m2.ano (ref: <Y>)
- **Nvc:** <X> kWh/m2.ano (ref: <Y>)
- **Nac:** <X> kWh/m2.ano (ref: <Y>)
- **Ntc:** <X> kWh/m2.ano (ref: <Y>)
- **R_Ntc:** <X> → **Classe <Z>**

## 5. Energia Renovavel
- Contribuicao solar termica: <X>%
- Contribuicao fotovoltaica: <X> kWh/ano
- Total renovavel: <X>%

## 6. Recomendacoes de Melhoria
| # | Medida | Custo est. | Poupanca/ano | Payback | Melhoria classe |
|---|---|---|---|---|---|
| 1 | ... | ... | ... | ... | ... |

## 7. Proximos Passos
- [ ] Contactar PQ (Perito Qualificado) via portal ADENE
- [ ] Preparar documentacao (plantas, memorias descritivas)
- [ ] Agendar visita tecnica
```

## Save location

`C:\Users\barda\OneDrive\Documents\VCHOME segundo cerebro\05 - Claude - IA\Outputs\YYYY-MM-DD - <Project> - Certificacao Energetica SCE.md`

## Red Flags
- Never skip the building envelope analysis (walls, roof, floor, windows) — the envelope determines 60-80% of the energy class, and optimizing systems without fixing the envelope is like heating a house with open windows
- Never ignore the solar thermal obligation for new builds and major rehabilitations — DL 118/2013 Art. 27 mandates solar contribution to DHW, and non-compliance blocks the certificado energetico and therefore the autorizacao de utilizacao
- Always check REH vs RECS applicability before starting any calculation — residential and commercial buildings use completely different methodologies (Ntc vs IEE), and applying the wrong framework invalidates the entire analysis
- Never estimate U-values from generic tables without verifying actual wall/roof composition — Portuguese buildings from different decades have wildly different constructions (tijolo simples, tijolo duplo, betao, pedra) and a wrong U-value cascades through every energy indicator
- Never present an energy class prediction as a guarantee — only a PQ (Perito Qualificado) registered with ADENE can issue the official SCE certificate, and site conditions may differ from design assumptions
- Always account for thermal bridges at pillar-wall, beam-slab, and window-wall junctions — in Portuguese construction (especially pre-2006 buildings without ETICS), thermal bridges can account for 10-30% of total heat losses and single-handedly drop the energy class by one or two levels

## References

- **ADENE portal:** https://www.adene.pt
- **SCE portal:** https://www.sce.pt
- **PQ search:** https://www.sce.pt/pesquisa-de-tecnicos/
- **DL 118/2013:** https://dre.pt/dre/detalhe/decreto-lei/118-2013-499237
- **Despacho 15793-F/2013:** Climate zone definitions by municipality

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Identificação do edifício e quadro regulatório correto
- [ ] Tipo de edifício declarado (REH residencial vs RECS comercial/serviços) com justificação explícita
- [ ] Situação clara: obra nova / grande reabilitação / existente (venda/arrendamento) / voluntário
- [ ] Zona climática atribuída por município real (ex: Lisboa = I1-V2, Bragança = I3-V1)
- [ ] Regulamentação aplicável citada: DL 118/2013, Portaria 349-B ou 349-D, DL 101-D/2020
- ❌ NOT delivery-ready: "Edifício em zona I2, regulamentação aplicável a definir"
- ✅ Delivery-ready: "Moradia em Braga (I2-V2), REH aplicável — DL 118/2013 + Portaria 349-B/2013; obra nova obriga a classe mínima B- e NZEB desde jan 2021"

### Gate 2 — Análise da envolvente com valores U verificáveis
- [ ] U-value declarado para cada elemento (paredes, cobertura, pavimento, vãos envidraçados)
- [ ] Comparação explícita com limites máximos da zona climática (tabela I1/I2/I3)
- [ ] Pontes térmicas identificadas (lineares ψ W/m.K) e tratamento indicado
- [ ] Conformidade ou não-conformidade assinalada por elemento com delta numérico
- ❌ NOT delivery-ready: "Paredes com isolamento adequado para a zona climática"
- ✅ Delivery-ready: "Parede exterior ETICS 6cm EPS: U = 0.38 W/m²K — conforme I2 (máx 0.40); cobertura XPS 8cm: U = 0.32 W/m²K — conforme (máx 0.35); janelas PVC duplo 4-16-4 Argon: Uw = 1.9 W/m²K, gT = 0.37 — conforme I2 (máx 2.40)"

### Gate 3 — Indicadores energéticos REH/RECS calculados
- [ ] Para REH: Nic, Nvc, Nac declarados em kWh/m².ano com valores de referência Ni, Nv, Na
- [ ] R_Ntc calculado (Ntc/Nt) e classe resultante identificada na tabela de classes A+→F
- [ ] Para RECS: IEE por uso final (AVAC, iluminação, AQS, outros) em kWh/m².ano
- [ ] Contribuição de renováveis (Eren,p) declarada e impacto no R_Ntc quantificado
- ❌ NOT delivery-ready: "Classe energética estimada B, sujeita a confirmação por perito"
- ✅ Delivery-ready: "Nic = 48 kWh/m²·ano (Ni ref = 62); Nvc = 6 kWh/m²·ano; Nac = 18 kWh/m²·ano; Ntc = 89 kWh/m²·ano → R_Ntc = 0.81 → Classe B-; solar térmico contribui Esolar = 1.240 kWh/ano (54% da AQS)"

### Gate 4 — Sistemas AVAC e AQS com eficiências declaradas
- [ ] Sistema de aquecimento: tipo, potência nominal, COP/EER ou rendimento η declarado
- [ ] Sistema de arrefecimento: tipo, EER nominal, classe EU Energy Label se aplicável
- [ ] AQS: sistema declarado + cumprimento solar térmico obrigatório (DL 118/2013, Art. 27)
- [ ] Exceção solar justificada tecnicamente se aplicável (sombreamento, orientação, estrutura)
- ❌ NOT delivery-ready: "Bomba de calor ar-ar eficiente; solar térmico a considerar"
- ✅ Delivery-ready: "Bomba de calor ar-água Daikin Altherma 3 8kW: COP 4.1 (A55/W35); arrefecimento EER 3.2; AQS: termoacumulador 200L + coletores Vulcano FKC-2 (2×2m²) — Esolar = 1.180 kWh/ano = 52% AQS — cumpre Art. 27"

### Gate 5 — Recomendações de melhoria com ROI e incentivos reais
- [ ] Mínimo 3 medidas de melhoria com custo estimado (€) e poupança (kWh/ano) declarados
- [ ] Payback calculado em anos com fórmula custo/poupança×preço energia
- [ ] Melhoria de classe potencial indicada por medida (ex: C→B-)
- [ ] Incentivos aplicáveis citados com nome correto: Fundo Ambiental, PRR, IFRRU 2020, IRS dedução 30%
- ❌ NOT delivery-ready: "Isolamento da cobertura melhora eficiência e tem apoios disponíveis"
- ✅ Delivery-ready: "ETICS fachada 8cm EPS: custo ~€8.500, poupança 2.100 kWh/ano (€294/ano a €0.14/kWh), payback 29 anos sem apoio → 18 anos com Fundo Ambiental (35% fundo perdido); melhoria de classe D→C confirmada por redução Nic de 98→61 kWh/m²·ano"

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets por preencher
- [ ] Frontmatter YAML sem campos `<placeholder>` por preencher
- [ ] Nome do projeto, município, Ap (m²), n.º de pisos todos preenchidos com valores reais
- [ ] Zona climática correta para o município declarado (não genérica)
- [ ] Classe atual e classe alvo numéricas/letras reais (não `<X>` e `<Y>`)
- ❌ NOT delivery-ready: `project: <project-name>`, `climate_zone: I1-V2`, `current_class: <X>`
- ✅ Delivery-ready: `project: vivenda-cascais-2024`, `climate_zone: I1-V2`, `current_class: D`, `target_class: B-`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / memória / dados do cliente
- 🟡 **assumed** — plausível mas necessita confirmação do cliente antes da entrega
- 🟢 **projection** — previsão por design (não verificável até certificação emitida)

Output checklist upfront mostra ao leitor exactamente o que é trust-as-is vs. precisa de verify. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready:
> "Parede exterior U=0.38 W/m².K, classe B-, Ntc/Nt=0.82, payback ETICS 4 anos."
> *(zero labels — cliente assume tudo verificado; se zona climática ou composição da parede estiver errada, toda a análise colapsa)*

✅ Delivery-ready:
> - 🔵 **verified** — Município: Braga → zona climática I2/V2 (Despacho 15793-F/2013)
> - 🟡 **assumed** — Espessura isolamento ETICS: 6 cm (não confirmada em telas finais; assumida com base na descrição verbal)
> - 🟡 **assumed** — Sistema AQS: esquentador a gás η=0.87 (cliente mencionou "gás", modelo não confirmado)
> - 🟢 **projection** — Classe energética estimada pós-melhoria: B (R_Ntc ≈ 0.68); sujeita a cálculo formal REH pelo perito qualificado
> - 🟢 **projection** — Payback ETICS + janelas duplas: ~6 anos (baseado em preços médios mercado PT 2024; orçamento real pode variar ±30%)

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — composição real da envolvente validada em telas/visita
- [ ] All 🟡 items confirmed — equipamentos HVAC e AQS com fichas técnicas (COP/EER/η reais)
- [ ] All 🔵 sources cited — zona climática, U-values de referência com portaria aplicável
- [ ] All 🟢 projections labeled as such ao cliente — classe estimada ≠ classe certificada; apenas perito SCE emite certificado válido

## Fully-worked A-tier example (delivery-ready reference)

```markdown
---
project: vivenda-cascais-2024
date: 2025-06-15
type: energy-certification-prep
building_type: residential
regulation: REH
climate_zone: I1-V2
current_class: D
target_class: B-
tags: [energia, SCE, certificacao, REH, Cascais, vivenda]
---

# Preparação Certificação Energética — Vivenda Cascais 2024

## 1. Dados do Edifício
- **Tipo:** Residencial unifamiliar — REH (Portaria 349-B/2013)
- **Situação:** Existente — remodelação major (>25% envolvente) → obriga classe mínima B-
- **Localização:** Cascais, Lisboa — zona climática I1 (inverno) / V2 (verão)
- **Área útil (Ap):** 187 m²
- **N.º de pisos:** 2 (r/c + 1.º andar)
- **Fator de forma (Ff):** 0.68 m⁻¹
- **Orientação fachada principal:** Sul (azimute 175°)

## 2. Análise da Envolvente

| Elemento | Composição | U calculado | U máx I1 | Conformidade |
|---|---|---|---|---|
| Parede exterior | Tijolo 11 + caixa-de-ar 4cm + ETICS 8cm EPS | 0.34 W/m²K | 0.50 | ✅ Conforme |
| Cobertura inclinada | Desvão ventilado + XPS 10cm sob laje | 0.28 W/m²K | 0.40 | ✅ Conforme |
| Pavimento térreo | Laje + XPS 5cm + betonilha | 0.37 W/m²K | 0.40 | ✅ Conforme |
| Vãos envidraçados | PVC 5 câmaras + 4-16-4 Argon Low-E | Uw = 1.6, gT = 0.37 | 2.80 | ✅ Conforme |
| Pontes térmicas | Caixa de estore: ψ = 0.30 W/m·K | — | — | ⚠️ Tratamento recomendado |

**Permeabilidade ao ar:** n50 = 3.2 h⁻¹ (blower door realizado em 12/05/2025)

## 3. Sistemas AVAC e AQS

- **Aquecimento:** Bomba de calor ar-água Daikin Altherma 3 R 8kW — COP = 4.08 (A7/W35)
- **Arrefecimento:** Mesmo circuito, modo reversível — EER = 3.2 (Eurovent 2024)
- **AQS:** Termoacumulador 200L + 2× coletores Vulcano FKC-2W (4 m² total, orientação Sul, inclinação 32°)
  - Esolar calculado = 1.340 kWh/ano = **56% das necessidades de AQS** — ✅ cumpre Art. 27 DL 118/2013
- **Ventilação:** Natural por abertura de fachada; grelhas de admissão em sala e quartos

## 4. Indicadores Energéticos REH

| Indicador | Valor calculado | Valor referência | Rácio |
|---|---|---|---|
| Nic (aquecimento) | 43 kWh/m²·ano | Ni = 66 kWh/m²·ano | 0.65 ✅ |
| Nvc (arrefecimento) | 5 kWh/m²·ano | Nv = 16 kWh/m²·ano | 0.31 ✅ |
| Nac (AQS) | 19 kWh/m²·ano | Na = 26 kWh/m²·ano | 0.73 ✅ |
| **Ntc (primária total)** | **76 kWh/m²·ano** | **Nt = 94 kWh/m²·ano** | — |
| **R_Ntc = Ntc/Nt** | — | — | **0.81 → Classe B-** ✅ |

Eren,p (renováveis): 1.340 kWh/ano solar térmico + 720 kWh/ano fração renovável BC (SPF 3.2 > 2.5)

## 5. Recomendações de Melhoria (para atingir classe B ou superior)

| # | Medida | Custo est. | Poupança/ano | Payback bruto | Payback c/ apoio | Melhoria de classe |
|---|---|---|---|---|---|---|
| 1 | Estores inteligentes + termostat Tado | €420 | €85/ano | 5 anos | — | +0.04 R_Ntc |
| 2 | Tratamento caixa de estore (ψ: 0.30→0.10) | €1.200 | €140/ano | 8.6 anos | 6 anos (Fundo Ambiental 30%) | B- → B |
| 3 | PV 3 kWp (12 painéis 250W) telhado Sul | €5.400 | €520/ano | 10.4 anos | 7.2 anos (IRS dedução 30% + PRR) | B → A |
| 4 | MVHR Zehnder ComfoAir Q350 | €4.800 | €310/ano | 15.5 anos | 11 anos (IFRRU 2020) | +0.06 R_Ntc |

**Classe atual pós-obra:** B- (R_Ntc = 0.81) — cumpre mínimo legal para grande reabilitação
**Classe potencial (medidas 1+2+3):** A (R_Ntc estimado 0.48)

## 6. Próximos Passos
1. Submissão a perito qualificado SCE para emissão de certificado (prazo médio: 15 dias úteis)
2. Registo no Portal SCE (www.sce.pt) — taxa: €65 (residencial até 250 m²)
3. Validade do certificado: **10 anos** (DL 118/2013, Art. 8.º)
4. Candidatura Fundo Ambiental aberta até 31/12/2025 — submissão recomendada antes de setembro
```

---

## Output anti-patterns

- Zona climática genérica ("I2-V2 típico") sem verificação do município real do projeto
- U-values declarados sem composição construtiva que os sustente (ex: "parede isolada U=0.35" sem espessura/material)
- R_Ntc calculado mas classe energética omitida ou invertida (confundir Ntc com Nt)
- Solar térmico descrito como "previsto" sem área de coletores, orientação e Esolar calculado — Art. 27 fica sem verificação
- Recomendações sem custo (€) e poupança (kWh/ano) — não é possível calcular payback nem comparar incentivos
- Incentivos citados com nomes errados ou desatualizados (ex: "POSEUR" encerrado; usar Fundo Ambiental, PRR, IFRRU 2020)
- Frontmatter com `<placeholders>` entregue ao cliente — revela template não preenchido
- Confundir REH com RECS para edifícios mistos sem justificação da dominante regulatória
- Classe "estimada sujeita a perito" sem R_Ntc numérico — impede decisão do cliente sobre investimento
- Omitir validade do certificado (10 anos) e referência ao Portal SCE para registo obrigatório
