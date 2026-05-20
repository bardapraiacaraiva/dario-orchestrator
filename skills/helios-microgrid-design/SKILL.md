---
name: helios-microgrid-design
description: Microgrids — islanding, resiliência, hybrid renewable/storage. Triggers em "microgrid", "islanding", "resilience", "hybrid renewable", "off-grid", "campus microgrid".
license: SEE-LICENSE
parent_agent: helios-director
---

# HELIOS-MICROGRID-DESIGN

## Use cases
- **Campus:** universities, hospitals, military bases
- **Commercial:** large industrial, data centers
- **Community:** rural electrification, indigenous
- **Off-grid:** remote operations (mining, oil&gas)
- **Resilience:** post-disaster, critical infra

## Components
- **Generation:** solar + wind + diesel + gas
- **Storage:** BESS
- **Loads:** critical vs non-critical (load shedding)
- **Microgrid controller:** islanding logic
- **Inverters:** grid-forming vs grid-following
- **Communication:** SCADA + IoT

## Modes
- **Grid-connected:** import/export, grid services
- **Islanded:** disconnected, self-sufficient
- **Transition:** seamless switching (<10ms ideal)
- **Black start:** restart from cold without grid

## Templates
1. Microgrid sizing (load + generation + storage)
2. Islanding control logic
3. Economic dispatch optimization
4. Critical load identification
5. Hybrid renewable + diesel optimization
6. Microgrid + EV charging integration

## Cross-references
- [[helios-energy-storage]] · [[helios-grid-integration]] · [[helios-ev-charging-strategy]]
