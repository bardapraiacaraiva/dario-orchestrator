---
name: diva-bim
description: "BIM integration for architecture and construction projects. Generates Revit/ArchiCAD-compatible specifications: room data sheets, door/window schedules, material schedules, finish schedules, equipment lists, and IFC-ready structured data. Export formats for BIM coordination. Triggers on \"BIM\", \"Revit\", \"ArchiCAD\", \"IFC\", \"room data sheet\", \"mapa de vaos\", \"mapa de acabamentos\", \"schedule\", \"LOD\", \"clash detection\", \"especialidades\"."
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# DIVA BIM — Building Information Modeling Integration

Generate structured specification data exportable to Revit, ArchiCAD, and other BIM platforms. Bridges DIVA's design decisions with BIM-ready documentation.

## When to activate

Invoke `/diva-bim` when:
- User needs room data sheets for BIM model
- User needs door/window schedules (mapa de vaos)
- User needs material/finish schedules (mapa de acabamentos)
- User needs equipment schedules
- User needs IFC-compatible structured output
- User wants to coordinate specialties (clash detection prep)
- User asks about LOD levels for a project phase

## Workflow

### 1. Determine BIM output needed

| Request | Output Type | Format |
|---|---|---|
| "mapa de vaos" | Door & Window Schedule | CSV/JSON |
| "mapa de acabamentos" | Finish Schedule | CSV/JSON |
| "room data sheet" | Room Data Sheets | Markdown/CSV |
| "lista de equipamentos" | Equipment Schedule | CSV |
| "coordenacao especialidades" | Specialty Coordination Matrix | Markdown |
| "preparar para Revit" | Multiple schedules + parameters | CSV bundle |

### 2. Generate — Room Data Sheets

Template per room for BIM model:

```csv
Room_ID,Room_Name,Floor,Area_m2,Height_m,Floor_Finish,Wall_Finish,Ceiling_Finish,Ceiling_Height_m,Lighting_Lux,HVAC_Type,HVAC_BTU,Electrical_Points,Data_Points,Water_Points,Special_Requirements,RGEU_Min_Area,RGEU_Compliant
R.0.01,Hall Entrada,0,4.5,2.70,Calcario Moca polido,Estuque pintado branco RAL 9010,Gesso cartonado pintado,2.50,150,Split,9000,3,1,0,Videoporteiro,3.0,SIM
R.0.02,Sala Estar+Jantar,0,28.0,2.70,Soalho carvalho eng. natural,Estuque pintado Farrow&Ball Pointing,Gesso cartonado pintado,2.50,300,Piso radiante,n/a,12,4,0,Cortinas motorizadas,18.0,SIM
R.0.03,Cozinha,0,14.0,2.70,Porcelanato Marazzi Grande 120x60,Azulejo artesanal Aleluia atras bancada + pintura,Gesso cartonado hidrofugo,2.40,500,Extracao+Split,12000,14,2,4,Extracao 400m3/h,6.0,SIM
R.0.04,WC Social,0,3.0,2.70,Micro-cimento cinza,Micro-cimento + espelho,Gesso cartonado hidrofugo,2.40,200,Extracao,n/a,4,0,3,Ventilacao mecanica,1.5,SIM
R.1.01,Suite Principal,1,16.0,2.70,Soalho carvalho eng.,Estuque pintado,Gesso cartonado,2.50,200,Split,12000,8,2,0,Blackout motorizado,10.5,SIM
R.1.02,WC Suite,1,6.5,2.70,Marmore Estremoz branco,Marmore ate 1.20m + pintura,Gesso cartonado hidrofugo,2.40,300,Extracao+toalheiro,n/a,5,0,4,Piso radiante WC,3.5,SIM
R.1.03,Quarto 2,1,12.0,2.70,Soalho carvalho eng.,Estuque pintado,Gesso cartonado,2.50,200,Split,9000,6,2,0,,9.0,SIM
R.1.04,Quarto 3,1,10.0,2.70,Soalho carvalho eng.,Estuque pintado,Gesso cartonado,2.50,200,Split,9000,5,1,0,,9.0,SIM
R.1.05,WC Comum,1,4.5,2.70,Ceramica Revigres 60x60,Ceramica ate 2.10m,Gesso cartonado hidrofugo,2.40,200,Extracao,n/a,4,0,3,,3.5,SIM
```

### 3. Generate — Door & Window Schedule (Mapa de Vaos)

```csv
ID,Type,Floor,Room_From,Room_To,Width_mm,Height_mm,Material,Finish,Glass,Hardware,Fire_Rating,Acoustic_dB,Threshold,Notes
P.01,Porta entrada,0,Exterior,Hall,1000,2100,Madeira macica carvalho,Verniz natural,Visor 200x200,Fechadura seguranca 3 pontos,EI30,42,Soleira aluminio,Porta seguranca
P.02,Porta interior,0,Hall,Sala,900,2100,MDF lacado,Branco RAL 9010,Nao,Magnetica+puxador inox,Nao,32,Nao,Batente oculto
P.03,Porta correr,0,Sala,Cozinha,1200,2100,Vidro temperado 10mm,Transparente,Sim full,Sistema embutido Eclisse,Nao,28,Nao,Embutida na parede
P.04,Porta WC,0,Corredor,WC Social,700,2100,MDF lacado,Branco RAL 9010,Nao,Trinco+indicador ocupado,Nao,32,Nao,Ventilacao grelha inferior
J.01,Janela fixa+batente,0,Sala,Exterior,2400,2200,Aluminio Cortizo COR-70,Lacado RAL 7016,Duplo low-E 6/16Ar/6,Oscilo-batente Roto,Nao,38,Peitoril pedra,Uw=1.4
J.02,Janela batente,0,Cozinha,Exterior,1200,1200,Aluminio Cortizo COR-70,Lacado RAL 7016,Duplo 6/16Ar/6,Oscilo-batente Roto,Nao,36,Peitoril pedra,Uw=1.4
J.03,Porta varanda,1,Suite,Varanda,1800,2200,Aluminio Cortizo COR-70,Lacado RAL 7016,Duplo low-E 6/16Ar/6,Levante-correr,Nao,38,Soleira nivelada,Uw=1.3
```

### 4. Generate — Material/Finish Schedule (Mapa de Acabamentos)

```csv
Code,Material,Manufacturer,Reference,Colour,Finish,Application,Thickness_mm,Price_EUR_m2,Lead_Time_weeks,Rooms_Applied
PAV.01,Soalho eng. carvalho,Jular,Oak Classic 190mm,Natural,Oleo Osmo,Pavimento,15,65,4,"R.0.02,R.1.01,R.1.03,R.1.04"
PAV.02,Calcario Moca,Solancis,Moca Creme 60x60,Creme,Amaciado,Pavimento,20,85,3,"R.0.01"
PAV.03,Porcelanato,Marazzi,Grande Marble Look 120x60,Statuario,Polido,Pavimento,9,55,3,"R.0.03"
PAV.04,Micro-cimento,Topciment,Sttandard,RAL 7038 cinza,Selante poliuretano,Pavimento+paredes WC,3,95,2,"R.0.04"
PAV.05,Marmore Estremoz,Marmetal,Branco Estremoz 60x30,Branco veio cinza,Polido,Pavimento+paredes,20,120,4,"R.1.02"
REV.01,Estuque tradicional,Aplicador local,Cal+areia fina,Branco,Pintura CIN Cinacryl,Paredes,15,28,1,"R.0.01-R.1.04"
REV.02,Azulejo artesanal,Aleluia Ceramicas,Heritage 15x15,Branco craquele,Vidrado,Parede cozinha,8,45,3,"R.0.03"
REV.03,Ceramica parede,Revigres,Touch 30x60,Cinza claro,Matt,Paredes WC,9,32,2,"R.1.05"
TEC.01,Gesso cartonado,Knauf,Standard 12.5mm,Branco,Pintura,Tectos,12.5,22,1,"Todos"
TEC.02,Gesso cartonado hidrofugo,Knauf,Moisture 12.5mm,Branco,Pintura anti-humidade,Tectos WC/cozinha,12.5,26,1,"R.0.03,R.0.04,R.1.02,R.1.05"
```

### 5. Generate — Equipment Schedule

```csv
ID,Equipment,Brand,Model,Dimensions_mm,Power_W,Water,Gas,Drain,Room,Notes
EQ.01,Placa inducao,Bosch,PXE875DC1E,816x527,7400,Nao,Nao,Nao,R.0.03,Encastrar bancada
EQ.02,Forno,Bosch,HBG675BS1,595x595x548,3600,Nao,Nao,Nao,R.0.03,Coluna forno
EQ.03,Micro-ondas,Bosch,BFL634GS1,595x382x320,900,Nao,Nao,Nao,R.0.03,Encastrar coluna
EQ.04,Frigorifico,Liebherr,ICBNd 5183,560x1770x550,n/a,Nao,Nao,Nao,R.0.03,Encastrar
EQ.05,Maq lavar louca,Bosch,SMV4HCX48E,600x815x550,2400,Sim,Nao,Sim,R.0.03,Integrada
EQ.06,Maq lavar roupa,Bosch,WIW28542EU,600x820x590,2300,Sim,Nao,Sim,Lavandaria,Encastrar
EQ.07,Exaustor,Elica,Hidden 60cm,600x280x300,250,Nao,Nao,Nao,R.0.03,Encastrar movel
EQ.08,Bomba calor AQS,Ariston,Nuos Plus 250,550x1834,270,Sim,Nao,Sim,Tecnica,250L
EQ.09,Split AC sala,Daikin,Stylish FTXA35BW,798x295x189,1030,Nao,Nao,Sim,R.0.02,Unidade interior
EQ.10,Unidade exterior,Daikin,RXA35A,765x550x285,1210,Nao,Nao,Nao,Exterior,Multi-split
```

### 6. Generate — LOD Specification by Phase

| Fase Projecto | LOD | Conteudo BIM | Uso |
|---|---|---|---|
| Estudo Previo | 100 | Volumes, areas brutas, orientacao | Viabilidade, primeira estimativa |
| Ante-Projecto | 200 | Geometria aproximada, materiais genericos | Orcamento preliminar, camara |
| Projecto Execucao | 300 | Dimensoes exactas, materiais especificos, schedules | Orcamento definitivo, consulta |
| Coordenacao | 350 | MEP integrado, clash detection, furacao | Coordenacao especialidades |
| Preparacao Obra | 400 | Detalhe construtivo, pecas fabricacao | Encomendas, producao |
| Telas Finais | 500 | As-built, desvios registados | Gestao edificio, FM |

### 7. Generate — Specialty Coordination Matrix

```csv
Specialty,Software,File_Format,Coordinator,Delivery_Phase,Clash_Check_With
Arquitectura,Revit/ArchiCAD,IFC/RVT,Arquitecto,LOD 300,"Estrutura,MEP"
Estrutura,Revit Structure/Tekla,IFC,Eng. Estruturas,LOD 300,"Arquitectura,MEP"
AVAC,Revit MEP/AutoCAD,IFC/DWG,Eng. Mecanica,LOD 350,"Estrutura,Electricidade,Canalizacao"
Electricidade,Revit MEP/AutoCAD,IFC/DWG,Eng. Electrotecnica,LOD 350,"Estrutura,AVAC,Canalizacao"
Canalizacao,Revit MEP/AutoCAD,IFC/DWG,Eng. Civil,LOD 350,"Estrutura,AVAC,Electricidade"
ITED,AutoCAD,DWG,Eng. Telecomunicacoes,LOD 300,"Electricidade"
Gas,AutoCAD,DWG,Eng. Mecanica,LOD 300,"Canalizacao,AVAC"
SCIE,AutoCAD,DWG,Eng. SCIE,LOD 200,"Arquitectura"
```

## Export Formats

| Target Software | Format | How to Import |
|---|---|---|
| Revit | CSV → Schedules | Create shared parameters, import CSV |
| ArchiCAD | CSV/JSON → Properties | Interactive Schedule import |
| Solibri | IFC | Open model, run clash rules |
| Navisworks | IFC/NWC | Append models, run clash detection |
| Excel | CSV | Direct open |
| PlanRadar | CSV/JSON | `/diva-planradar` integration |

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - [Projecto] - BIM [Schedule Type].csv`

## Red Flags
- Never export a BIM model or schedule without running clash detection first — undetected clashes between MEP and structure are the number one cause of rework on Portuguese construction sites, costing weeks and thousands of euros
- Never skip room data validation against RGEU minimum dimensions (areas, ceiling heights, ventilation) — a model that passes BIM coordination but fails RGEU review gets rejected by the camara municipal
- Always include IFC classification (IFC 2x3 or IFC4) on every exported element — Portuguese specialty engineers use different BIM software (Revit, ArchiCAD, Tekla, AutoCAD) and IFC is the only reliable interoperability format
- Never assume software compatibility between project team members — always confirm file format support before exchanging models, and provide IFC as fallback for every deliverable
- Always use mm as the base unit for all BIM dimensions — mixing cm or m causes scaling errors that propagate silently across linked models and only surface during construction
- Never generate LOD 400/500 specifications without verified construction drawings — high-detail BIM data based on preliminary design creates false confidence and leads to costly fabrication errors
