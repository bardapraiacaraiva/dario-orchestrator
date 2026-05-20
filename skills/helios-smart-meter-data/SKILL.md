---
name: helios-smart-meter-data
description: Smart meter data analytics — consumo patterns, M&V, AMI, energy disaggregation. Triggers em "smart meter", "AMI", "M&V", "energy disaggregation", "consumption analytics", "PRODIST 9".
license: SEE-LICENSE
parent_agent: helios-director
---

# HELIOS-SMART-METER-DATA

## Tipos meter
- **AMI (Advanced Metering Infrastructure):** smart, bidirecional, communications
- **AMR (Automated Meter Reading):** one-way
- **Time-of-Use (ToU):** rate por hora
- **Demand meter:** medida kW peak

## Analytics use cases
- **Energy disaggregation:** identify HVAC, lighting, refrigeration consumo
- **Anomaly detection:** detect leaks, equipment failure
- **Load forecasting:** ML para demand
- **Customer segmentation:** behavioral patterns
- **Energy efficiency audit:** identify savings opportunities

## Stack
- **Itron, Landis+Gyr:** meter hardware
- **Honeywell Smart Energy:** AMI head-end
- **Bidgely, Sense:** disaggregation
- **Datapool BR:** energy analytics
- **OpenEEmeter:** open-source M&V

## Templates
1. AMI deployment plan
2. M&V Protocol IPMVP-compliant
3. Energy disaggregation pipeline
4. Anomaly detection rules
5. Customer-facing energy report
6. Load forecasting model (LSTM)

## Cross-references
- [[helios-energy-efficiency-iso50001]] · [[demeter-realtime-streaming]] · [[demeter-predictive]]
