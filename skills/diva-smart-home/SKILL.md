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
