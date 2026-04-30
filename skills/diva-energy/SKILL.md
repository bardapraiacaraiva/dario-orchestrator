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
