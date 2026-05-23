---
name: diva-smart-home
description: Smart home / domotica specification — needs assessment by room, protocol selection (KNX, Zigbee, Wi-Fi, Matter), subsystem design (lighting, blinds, HVAC, security, audio, irrigation), pre-installation requirements, brand recommendations, integration platforms, and cost estimation by tier. Triggers on "domotica", "smart home", "casa inteligente", "automacao casa", "KNX", "home assistant", "Loxone".
license: MIT
---

# DIVA Skill — Smart Home / Domotica Specification

Designs complete smart home specifications for residential and small commercial projects in Portugal. Covers protocol selection, subsystem architecture, pre-installation cabling/infrastructure requirements, brand/product recommendations, integration platform selection, and tiered cost estimation.

## When to activate

- New construction where domotica is planned from the start
- Renovation with smart home retrofit
- Client asks for home automation recommendations
- Architect/designer needs domotica spec for project documentation
- Electrician/installer needs pre-installation requirements
- Client wants cost comparison between automation tiers

Do NOT use for:
- Industrial automation (SCADA, PLC systems)
- Building management systems for large commercial (>2000m2) — refer to BMS specialists
- Pure IT/networking without automation context

## Protocol comparison (reference)

| Protocol | Wiring | Reliability | Cost | Scalability | Best for |
|---|---|---|---|---|---|
| KNX | Dedicated bus (TP) | Excellent | High | Excellent | Premium new-build, commercial |
| Zigbee 3.0 | Wireless (mesh) | Good | Low | Good | Retrofit, medium budgets |
| Z-Wave | Wireless (mesh) | Good | Medium | Good | Retrofit, strong ecosystem |
| Wi-Fi | Existing network | Fair | Low | Limited | Entry-level, simple setups |
| Matter | Wireless (Thread/Wi-Fi) | Good | Medium | Excellent | Future-proof, multi-vendor |
| Loxone Tree | Dedicated bus | Excellent | High | Excellent | Integrated premium solution |
| DALI-2 | Dedicated bus | Excellent | Medium | Good | Lighting-only subsystems |

## Workflow

### 1. Needs assessment by room

For each room/zone, evaluate:
- **Lighting:** scenes, dimming, color temperature, circadian
- **Blinds/shutters:** motorized, sun-tracking, wind sensors
- **HVAC:** zone control, floor heating valves, split AC integration
- **Security:** motion sensors, door/window contacts, cameras, alarm
- **Audio/video:** multi-room audio, intercom, media distribution
- **Irrigation:** garden zones, weather-based scheduling, soil moisture
- **Appliances:** smart plugs, energy monitoring, EV charger integration
- **Access control:** smart locks, video doorbell, gate automation

Template per room:
```
| Room | Lighting | Blinds | HVAC | Security | Audio | Special |
|---|---|---|---|---|---|---|
| Sala | Dim+CCT, 3 scenes | 2x motorized | AC zone | Motion | Sonos | Fireplace relay |
| Cozinha | On/off, under-cabinet | 1x motorized | AC zone | Smoke+gas | — | Appliance monitoring |
| Suite | Dim+CCT, wake-up | 2x motorized | Floor heating | Motion | Sonos | Bedside USB |
```

### 2. Protocol selection

Decision matrix based on:
- **New build vs retrofit:** new build = wired preferred; retrofit = wireless
- **Budget tier:** basic = Wi-Fi/Zigbee; medium = Zigbee/Matter; premium = KNX/Loxone
- **Number of devices:** <30 = Wi-Fi OK; 30-100 = Zigbee/Z-Wave; >100 = KNX/Loxone
- **Client technical skill:** DIY = Home Assistant + Zigbee; turnkey = Loxone/Control4
- **Future-proofing priority:** Matter for maximum vendor independence
- **Reliability requirements:** mission-critical (security, HVAC) = wired always

Recommendation pattern:
- **Backbone:** KNX or Loxone Tree for lighting, blinds, HVAC (wired, reliable)
- **Sensors:** Zigbee or Thread for motion, temperature, humidity (wireless, battery)
- **Integration:** Home Assistant or Loxone Miniserver as central brain
- **Voice:** Apple HomeKit / Google Home / Alexa as user interface layer

### 3. Pre-installation requirements

This section is CRITICAL — must be defined before construction/renovation begins:

**Electrical panel:**
- Dedicated DIN-rail space for automation (minimum 2 rows = 24 modules)
- Separate circuits per zone for dimming (no shared neutrals)
- UPS for automation controller (min 600VA)
- Surge protection (SPD Type 2) on automation bus

**Cabling (new build):**
- Cat6A to every room (minimum 2 points per room + 1 per camera position)
- KNX bus cable (2x2x0.8mm LSZH) if KNX selected — star topology from panel
- Speaker cable (2x2.5mm OFC) to ceiling positions for multi-room audio
- Conduit to blinds motor positions (leave pull-wire if motor not yet chosen)
- Conduit to garden for irrigation valves and sensors
- Central patch panel location (technical closet, ventilated)
- HDMI/fiber conduit between AV positions (living room, cinema room)

**Network:**
- Managed PoE switch (for cameras, access points, wired devices)
- Dedicated VLAN for IoT devices (security isolation)
- Wi-Fi access points: ceiling-mounted, PoE, minimum 1 per 60m2
- Internet uplink: minimum 100Mbps for remote access and cameras

**Power:**
- Dedicated 16A circuit for automation rack
- Smart meter or CT clamp for whole-house energy monitoring
- Pre-wire for EV charger if garage present (32A single/three-phase)

### 4. Subsystem specification

For each subsystem, specify:
- Devices (make, model, quantity)
- Protocol connection
- Automation rules (triggers, conditions, actions)
- Fallback behavior (what happens if controller fails)

Key automations to include:
- **Welcome home:** exterior lights on, hallway lights 50%, HVAC to comfort, disarm alarm
- **Good night:** all lights off (except night lights), blinds close, alarm arm (night mode), HVAC setback
- **Away mode:** lights simulate presence, HVAC economy, alarm arm (full), cameras active
- **Morning routine:** blinds open gradually, bathroom lights warm, coffee machine on
- **Sun protection:** auto-close blinds when exterior temp >28C and sun angle hits facade
- **Water leak:** shut valve, alert, flash bathroom lights

### 5. Brand recommendations by tier

**Basic (EUR 30-50/m2):**
- Controller: Home Assistant Yellow or Raspberry Pi 5
- Lighting: Shelly Plus Dimmer 0-10V, IKEA TRADFRI
- Blinds: Shelly Plus 2PM
- Sensors: Aqara/Sonoff Zigbee
- Security: Reolink cameras, Aqara sensors
- Audio: Google/Alexa speakers

**Medium (EUR 80-150/m2):**
- Controller: Home Assistant + SkyConnect + Z-Wave stick
- Lighting: Shelly Pro Dimmer, Philips Hue (key rooms)
- Blinds: Somfy io (via Tahoma) or Shelly Pro 2PM
- HVAC: Airzone / Intesis gateway for splits, Tado valves for floor heating
- Security: Hikvision/Dahua PoE cameras, Ajax alarm system
- Audio: Sonos (2-4 zones)
- Energy: Shelly Pro 3EM for monitoring

**Premium (EUR 200-500/m2):**
- Controller: Loxone Miniserver or KNX server (Gira/ABB)
- Lighting: KNX actuators (ABB, Schneider, MDT) or Loxone Tree
- Blinds: KNX blind actuators or Loxone Tree
- HVAC: KNX integration, Loxone Climate Controller
- Security: Loxone Intercom + cameras, or 2N + Milestone
- Audio: Sonos Amp / Bluesound / Loxone Music Server
- Control: Loxone Touch Pure, Gira G1, Basalte Ellie
- Energy: Loxone Modbus energy meter, SolarEdge/Fronius integration
- Extras: Lutron Palladiom shades, Control4 for AV distribution

### 6. Cost estimation

Calculate per tier:
```
Total = Area (m2) x Rate (EUR/m2) + Fixed costs

Fixed costs:
- Controller/server: EUR 500-3000
- Network infrastructure: EUR 1000-3000
- Electrical panel modifications: EUR 500-2000
- Programming/commissioning: EUR 1500-5000
- Design/engineering: EUR 1000-3000
```

Include Portuguese VAT considerations:
- Installation labor: 23% IVA (6% if renovation of dwelling >2 years old)
- Equipment: 23% IVA always

## Output template

```markdown
---
project: <project-name>
date: YYYY-MM-DD
type: smart-home-spec
protocol: KNX|Zigbee|Loxone|Mixed
tier: basic|medium|premium
area_m2: <X>
estimated_cost: <EUR X>
tags: [domotica, smart-home, <protocol>, <project>]
---

# Especificacao Domotica — <Project Name>

## 1. Resumo Executivo
- **Area:** <X> m2, <N> divisoes
- **Tier:** <Basic/Medium/Premium>
- **Protocolo principal:** <X>
- **Plataforma integracao:** <X>
- **Orcamento estimado:** EUR <X> (s/ IVA)

## 2. Necessidades por Divisao
| Divisao | Iluminacao | Estores | HVAC | Seguranca | Audio | Especial |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |

## 3. Arquitectura do Sistema
### Protocolo e topologia
- ...

### Controlador central
- ...

### Rede
- ...

## 4. Pre-Instalacao (para electricista/empreiteiro)
### Quadro electrico
- ...

### Cablagem
- ...

### Infraestrutura de rede
- ...

## 5. Lista de Equipamento
| # | Equipamento | Marca/Modelo | Qtd | Preco unit. | Total |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

**Subtotal equipamento:** EUR <X>
**Instalacao e programacao:** EUR <X>
**Total (s/ IVA):** EUR <X>
**IVA (23%):** EUR <X>
**Total (c/ IVA):** EUR <X>

## 6. Cenarios de Automacao
| Cenario | Trigger | Accoes |
|---|---|---|
| Bem-vindo | Porta entrada abre | Luzes hall 50%, AVAC conforto, alarme desarmar |
| Boa noite | Botao cabeceira | Luzes off, estores fecham, alarme noite |
| ... | ... | ... |

## 7. Fallback e Fiabilidade
- Comportamento sem controlador: ...
- UPS: ...
- Manutencao recomendada: ...

## 8. Proximos Passos
- [ ] Aprovar especificacao com cliente
- [ ] Enviar req. pre-instalacao ao electricista
- [ ] Encomendar equipamento (lead times: X semanas)
- [ ] Agendar programacao/comissionamento
```

## Save location

`C:\Users\barda\OneDrive\Documents\VCHOME segundo cerebro\05 - Claude - IA\Outputs\YYYY-MM-DD - <Project> - Especificacao Domotica.md`

## Red flags — don't do this

- Do NOT recommend Wi-Fi-only for >20 devices — network congestion and reliability issues
- Do NOT skip pre-installation cabling spec — retrofitting conduits after construction is 5-10x more expensive
- Do NOT mix KNX and Loxone Tree on the same bus — they are incompatible physical layers
- Do NOT forget fallback behavior — smart home must work with manual switches even if controller fails
- Do NOT ignore Portuguese electrical standards (RTIEBT) — all work must comply
- Do NOT specify outdoor cameras without checking RGPD/CNPD requirements for recording public spaces
- Do NOT undersize the electrical panel — automation adds 12-48 DIN modules depending on tier
- Do NOT assume all ISPs support port forwarding for remote access — recommend Tailscale/WireGuard VPN instead

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Needs assessment completo por divisão

- [ ] Tabela de divisões preenchida com TODAS as divisões do projeto (não "Sala/Quarto genérico")
- [ ] Cada subsistema (lighting, blinds, HVAC, security, audio, special) avaliado por divisão — células vazias só com "—" intencional
- [ ] Cenas de iluminação nomeadas explicitamente (ex: "Jantar", "Filme", "Leitura") — não "3 scenes"
- [ ] Equipamentos especiais identificados (lareira, piscina, portão, carregador EV)

❌ NOT delivery-ready: `| Suite | Dim+CCT | Motorized | Floor heating | Motion | — | — |`
✅ Delivery-ready: `| Suite Principal | Dim+CCT 2700-5000K, cenas: Acordar/Relaxar/Leitura | 2x motor SOMFY RS100 io, sun-tracking sul | Termostato chão Danfoss CF-SG, 2 zonas | PIR Aqara MS-S02, contacto janela | Sonos Era 100 (embutido) | Tomadas USB-C x4 cabeceira |`

---

### Gate 2 — Protocolo justificado com dados do projeto

- [ ] Decisão de protocolo explicada com referência explícita ao projeto (nova construção vs. retrofit, m², nº estimado de dispositivos)
- [ ] Híbridos justificados (ex: "backbone KNX + sensores Zigbee porque retrofit parcial")
- [ ] Plataforma de integração escolhida e versão indicada (ex: Home Assistant OS 2024.11 / Loxone Miniserver Gen 2)
- [ ] Limitações conhecidas do protocolo escolhido mencionadas (ex: "Wi-Fi limitado a <30 dispositivos — expansão futura requer migração")

❌ NOT delivery-ready: `Recomendamos KNX para este projeto premium.`
✅ Delivery-ready: `Moradia Cuidai — 280m², nova construção, estimativa 87 pontos de controlo → KNX TP backbone (Schneider MTN) + Zigbee 3.0 para sensores de presença (Aqara hub local) + Home Assistant OS 2024.11 como camada de integração. Matter Thread reservado para expansão 2025+.`

---

### Gate 3 — Pré-instalação específica e acionável

- [ ] Lista de cabos com especificação técnica real (secção, tipo, norma) — não genérica
- [ ] Posições de cablagem identificadas por divisão/ponto (ex: "Cat6A × 2 pontos sala, 1 ponto câmara hall")
- [ ] Dimensionamento do quadro elétrico indicado (nº módulos DIN reservados, UPS VA, VLAN IoT)
- [ ] Notas "deixar vazio agora / instalar depois" marcadas explicitamente para decisões adiadas

❌ NOT delivery-ready: `Passar cabo de rede em todas as divisões e preparar para estores motorizados.`
✅ Delivery-ready: `Vivenda Sintra — Quadro técnico: 2 calhas DIN livres (24 módulos) para automação KNX, UPS Salicru SPS 700VA, SPD Hager MN125. Cablagem: Cat6A Legrand 2×/divisão + 1×câmara (hall, garagem, jardim N/S), bus KNX LSZH 2×2×0.8mm estrela a partir de quadro, speaker OFC 2×2.5mm para tetos sala+suite, conduit ∅20mm a motores estores (pull-wire instalado). EV: circuito 32A trifásico garagem pré-instalado.`

---

### Gate 4 — Especificação de subsistema com automações concretas

- [ ] Pelo menos 4 automações-chave descritas (trigger → condição → ação) — não só nomeadas
- [ ] Comportamento de fallback definido para falha do controlador
- [ ] Marcas e modelos reais indicados (não "actuador KNX genérico")
- [ ] Regras de segurança/alarme separadas de conforto (criticidade diferente)

❌ NOT delivery-ready: `Modo Boa Noite: luzes apagam, estores fecham, alarme ativa.`
✅ Delivery-ready: `Modo Boa Noite (trigger: botão hall ou 23h30 se presença detetada): 1) Luzes todas OFF exceto corredor 5% cálido (Philips Hue Gradient, 2200K); 2) Estores SOMFY todas as suites fecham 100%; 3) Termostato Danfoss recua para 17°C; 4) DSC Neo arma em modo perímetro (zonas internas inativas). Fallback KNX: botão físico Schneider E/S atua direto sem Miniserver.`

---

### Gate 5 — Estimativa de custo por tier com itemização real

- [ ] Três tiers apresentados (Basic / Smart / Premium) com intervalo de preço em € para o projeto específico
- [ ] Custo de mão-de-obra e programação separado do material
- [ ] Componentes mais caros itemizados (não apenas total)
- [ ] Nota clara sobre IVA e exclusões (obra civil, pintura, rede elétrica base)

❌ NOT delivery-ready: `Tier Premium: €25.000 - €50.000 dependendo do projeto.`
✅ Delivery-ready: `Moradia Atrium Cascais 220m² — Tier Smart (Zigbee + HA): material €8.400 (Hub Sonoff iHost €89, 24× actuador Aqara €38/un, 12× dimmer Aqara €45/un, 8× motor Zemismart €65/un, NAS Synology DS223 €320) + mão-de-obra + programação €3.200 = **Total ~€11.600 + IVA 23%**. Exclui quadro elétrico base, obra civil e pintura.`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder

- [ ] Zero ocorrências de `<nome>`, `<morada>`, `<protocolo>`, `<marca>`, `[INSERIR]` ou equivalentes no output final
- [ ] Nome do cliente/projeto aparece no título e em pelo menos 2 secções
- [ ] Endereço ou tipologia real da habitação mencionados (ex: "T4 nova construção Comporta", "V3 retrofit Cascais")
- [ ] Data de entrega do documento e versão indicadas no cabeçalho

❌ NOT delivery-ready: `Especificação Smart Home para <Cliente> — <tipologia> em <localidade>.`
✅ Delivery-ready: `**Especificação Domotica — Vivenda LUSOconta, V4 Nova Construção, Comporta** | Versão 1.0 | Janeiro 2025 | Preparado por DIVA para João Ferreira`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Especificação Domotica — Moradia Cuidai, V4 Nova Construção, Cascais
**Versão 1.2 | Fevereiro 2025 | DIVA Smart Home Specification**
Cliente: Cuidai Residências | Contacto: Ana Lopes | Entrega obra: Setembro 2025

---

## Needs Assessment por Divisão

| Divisão | Iluminação | Estores | HVAC | Segurança | Áudio | Especial |
|---|---|---|---|---|---|---|
| Hall Entrada | On/off 3000K, deteção presença | — | — | PIR + contacto porta | — | Vídeo porteiro |
| Sala Estar | Dim+CCT 2700-5000K, cenas: Jantar/Filme/Leitura/Festa | 3× motor sul + 1× motor poente | Zona AC + FCU | PIR Aqara | Sonos Era 300 (2×) | Controlo lareira bioetanol |
| Cozinha | On/off + sob-armário CCT | 1× motor | Zona AC | Detetor fumo+gás | — | Monitorização consumo eletrodomésticos |
| Suite Principal | Dim+CCT, cenas: Acordar/Relaxar/Noite | 2× motor blackout | Piso radiante 2 zonas + AC | PIR + contacto janela | Sonos Era 100 (embutido teto) | Tomadas USB-C × 4 cabeceiras |
| Suite 2 | Dim+CCT, cenas: Acordar/Relaxar | 2× motor | Piso radiante 1 zona | PIR + contacto janela | Sonos Era 100 | — |
| Escritório | Dim+CCT, cena: Foco circadiano | 1× motor | AC zona | — | — | KVM + monitor retractil |
| Garagem | On/off deteção presença | — | Ventilação CO | PIR + sensor CO | — | Carregador EV 22kW |
| Jardim/Ext. | Caminhos + destaque vegetação | — | — | 4× câmara PoE | — | Irrigação 6 zonas |

---

## Protocolo Selecionado

**Projeto:** V4, 310m², nova construção, estimativa 112 pontos de controlo
→ **Backbone KNX TP** (Schneider Electric MTN series) para iluminação, estores, HVAC
→ **Zigbee 3.0** (Aqara Hub M3, local processing) para sensores de presença, temperatura, humidade, contactos
→ **DALI-2** para circuitos iluminação técnica cozinha e escritório
→ **Plataforma:** Home Assistant OS 2025.1 em NAS Synology DS923+ (redundância RAID-1)
→ **UI:** Apple HomeKit (família) + painel wall Schneider Touch Multitouch KNX (hall, sala, suite)
→ **Limitação conhecida:** Zigbee limitado a ~100 dispositivos neste hub — sensores jardim via Zigbee 2º hub

---

## Pré-Instalação (Entregar ao Empreiteiro até Março 2025)

**Quadro Elétrico Técnico (cave):**
- Reservar 3 calhas DIN (36 módulos) para automação KNX
- UPS Salicru SPS.One 1000VA para controlador + NAS
- SPD Hager MN125 na saída bus KNX
- Circuito dedicado 16A para rack automação

**Cablagem obrigatória antes de fechar paredes:**
- Cat6A Legrand (U/FTP) × 2 pontos por divisão + 1 ponto por câmara (hall ext N/S, garagem, jardim)
- Bus KNX LSZH 2×2×0.8mm — topologia estrela a partir do quadro técnico cave
- Speaker OFC 2×2.5mm para posições teto: sala (4 pontos), suite 1 (2), suite 2 (2), exterior (2)
- Conduit ∅20mm a cada motor de estore com pull-wire instalado (motor decidido fase 2)
- HDMI 2.1 + fibra OM3 entre sala e armário AV (distância ~8m)
- Conduit ∅32mm para eletroválvulas irrigação jardim (6 zonas, central a norte)
- Circuito 32A trifásico garagem para carregador EV (Schneider EVlink Pro AC 22kW)

**Rede:**
- Ubiquiti UniFi Switch Pro 24 PoE (400W) no rack cave
- VLAN 10 (IoT isolada), VLAN 20 (câmeras), VLAN 30 (automação KNX/IP)
- Access Points: UniFi U6-Pro × 3 (piso 0, piso 1, exterior) — ceiling mount, Cat6A PoE
- Uplink mínimo 300Mbps (NOS Empresas recomendado)

---

## Automações Principais

**Chegar a Casa** (trigger: geofence 500m OU reconhecimento matrícula câmara portão):
Condição: modo Away ativo → portão abre, hall 70% 3000K, sala 40% 3000K, HVAC retoma conforto (21°C), alarme DSC Neo desarma, Sonos retoma playlist habitual a 25%.

**Boa Noite** (trigger: botão hall "moon" OU 23h30 se presença sala):
Luzes ALL OFF exceto corredor 8% 2200K (Schneider MTN630619) → estores suites fecham 100% blackout → Danfoss CF2+ recua 17°C pisos → DSC Neo arma perímetro. Fallback: botão físico KNX atua direto sem HA.

**Proteção Solar** (trigger: radiação > 600W/m² sensor exterior E hora solar entre 10h-18h):
Estores sala e suites descem para 40% (posição lâminas orientadas) → suspende se vento > 40km/h (anemómetro ELSNER P03/3-RS485).

**Irrigação Inteligente** (trigger: diário 6h30):
Condição: precipitação prevista < 3mm (API IPMA) AND humidade solo < 45% (sensor Xiaomi HHCCJCY10) → abre eletroválvulas Rain Bird por zona (6×8min), registo em HA Energy.

---

## Estimativa de Custo — Moradia Cuidai

| Componente | Qtd | Preço Unit. | Total |
|---|---|---|---|
| KNX Schneider MTN actuadores (iluminação + estores) | 18 | €185 | €3.330 |
| KNX Schneider MTN paineis tácteis | 5 | €420 | €2.100 |
| Motores estore SOMFY RS100 io | 9 | €145 | €1.305 |
| Sensores Zigbee Aqara (PIR, contactos, temp) | 28 | €35 | €980 |
| Sonos Era 100/300 + Sub Mini | 6 | €280 avg | €1.680 |
| NAS Synology DS923+ + 2×HDD 4TB | 1 | €680 | €680 |
| UniFi Switch + APs + câmaras PoE G4 | 1 lot | €1.450 | €1.450 |
| DSC Neo alarme (central + sensores) | 1 lot | €890 | €890 |
| Rain Bird irrigação (central + 6 válvulas) | 1 lot | €380 | €380 |
| Carregador EV Schneider 22kW | 1 | €650 | €650 |
| **Material total** | | | **€13.445** |
| Programação HA + KNX + comissionamento | | | €4.200 |
| **TOTAL + IVA 23%** | | | **~€21.800** |

*Exclui: quadro elétrico base, obra civil, pintura, instalação elétrica convencional.*
*Tier Basic (só Zigbee + HA, sem KNX): ~€9.200 + IVA*
```

---

## Output anti-patterns

- **Protocolo sem justificação de projeto** — recomendar KNX sem referir m², nº dispositivos ou nova construção vs. retrofit
- **Tabela de divisões com dados genéricos** — "Quarto 1 / Dim / Motorized / AC" sem nomes de cenas, marcas ou especificações técnicas
- **Pré-instalação sem especificação de cabo** — "passar rede e KNX" sem secção, norma ou topologia
- **Automações só nomeadas** — listar "Modo Férias" sem trigger → condição → ação → fallback
- **Custo em banda larga vaga** — "€15k–€40k dependendo do projeto" sem itemização de componentes principais
- **Angle-brackets no output final** — `<localidade>`, `<protocolo escolhido>`, `[INSERIR MARCA]` chegam ao cliente
- **Fallback de falha de controlador omitido** — especificação que não responde "o que acontece se o Home Assistant reiniciar?"
- **IVA e exclusões não declarados** — cliente interpreta custo de material como preço final chave-na-mão
- **Marcas placeholder** — "actuador KNX de uma marca reconhecida" em vez de Schneider MTN / ABB i-bus / Gira
- **Cablagem de áudio/AV esquecida** — especificação que planeia multi-room audio sem speaker cable nas paredes
