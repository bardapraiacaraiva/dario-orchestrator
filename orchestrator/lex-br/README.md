# LEX-BR — Agente Especialista em Direito Brasileiro

**Versão:** v1.0.0 (2026-05-19)
**Parent agent:** dario-ceo (DARIO Orchestrator v11.1.2+)
**Jurisdição:** Brasil
**Idioma:** PT-BR formal

---

## O que é

LEX-BR é o **primeiro agente de IA jurídica BR-native** do mercado. Não é um plugin adaptado — é uma arquitectura completa com:

- **15 skills BR-native** cobrindo todas as áreas do Direito Brasileiro
- **8 conectores MCP** (3 ja implementados) para plataformas brasileiras
- **Compliance OAB Provimento 205/2021** built-in (não opcional)
- **LGPD operator marker** automático em todos os outputs
- **HMAC-signed VIP keys** para licenciamento seguro
- Construído sobre **DARIO Orchestrator v11.1.2+** (216+ testes de base, agora 242+)

## As 15 Skills

| Skill | Foco | Templates |
|---|---|---|
| `lex-civil` | Código Civil 2002, responsabilidade civil, obrigações | 30 |
| `lex-commercial` | Contratos B2B, distribuição, franquia | 25 |
| `lex-corporate` | Lei 6.404/76 (S.A.), M&A, governance | 20 |
| `lex-trabalhista` | CLT, Reforma 13.467/17, Justiça do Trabalho | 40 |
| `lex-tributario` | CTN, Reforma EC 132/2023, CARF, STF/STJ | 30 |
| `lex-lgpd` | LGPD, ANPD, DPO, RIPD, DSR | 15 |
| `lex-regulatorio` | BACEN, CVM, ANVISA, ANATEL, ANEEL, ANP, ANS | 20 |
| `lex-ai-governance` | Marco Legal IA PL 2338/2023, LGPD+IA | 10 |
| `lex-ip` | INPI, Lei 9.279/96, software, autoral | 15 |
| `lex-litigation` | CPC/2015, peças processuais, recursos | 50 |
| `lex-consumidor` | CDC Lei 8.078/90, e-commerce, recall | 20 |
| `lex-administrativo` | NLLC 14.133/21, licitações, TCU | 25 |
| `lex-imobiliario` | Locação, compra e venda, condomínio | 15 |
| `lex-familia` | Divórcio, alimentos, guarda, sucessões | 20 |
| `lex-criminal` | CP, CPP, Anticrime, defesa criminal | 25 |

**Total: 360 templates curados** (validação por consultor advogado em progresso).

## Compliance Layer (Built-in, não opcional)

### 1. OAB Provimento 205/2021 Gate
- Outputs destinados a tribunal/cliente/contraparte requerem `revisao_humana_confirmada: true`
- Sem revisão → output **BLOQUEADO** (não sai do sistema)
- Audit trail: cada output regista o advogado responsável (OAB nº)

### 2. LGPD Operator Marker
Rodapé automático em todos os outputs:
```
Documento gerado com assistência de DARIO/LEX-BR (operador LGPD).
Controlador: [Escritório]. DPO: [contacto]. ZDR active.
Sigilo profissional mantido (Provimento OAB 205/2021 + Art. 36 EOAB).
```

### 3. ZDR Enforcement
Inputs com **dados sensíveis** (CPF, RG, número de processo, dados clínicos, dados financeiros) requerem Zero Data Retention activo.

### 4. Cite Checker
Toda referência a artigo/lei/súmula passa por validador:
- Existência (não inventada pelo modelo)
- Não-revogada
- Aplicabilidade

### 5. Privilege Marker
Outputs do tipo `estrategia_processual`, `parecer_juridico`, `comunicacao_cliente` ganham banner:
```
SIGILOSO — PRIVILÉGIO CLIENTE-ADVOGADO
Art. 36 EOAB + Art. 154 CP
```

### 6. Audit Trail OAB-Compatible
Log imutável em `memory/compliance_log/YYYY-MM-DD.yaml`:
- Timestamp UTC
- Skill invocada
- Cliente (hash anonimizado)
- Output_type + hash do output (integrity)
- Revisor (OAB nº)
- Flags compliance (cite_check, ZDR, privilege)

## MCP Connectors (3 implementados + 5 planeados)

### Implementados (v1.0.0)
- **mcp-jusbrasil** — jurisprudência STF/STJ/TJs (modo STUB sem API key, LIVE com `JUSBRASIL_API_KEY`)
- **mcp-cnj-datajud** — metadados processuais oficiais CNJ (token público compartilhado)
- **mcp-stf** — RSS decisões + Súmulas Vinculantes + Repercussão Geral

### Planeados (v1.1.0)
- mcp-diario-oficial — DOU + diários estaduais
- mcp-anpd — sanções LGPD + orientações
- mcp-receita-federal — eCAC + CNPJ
- mcp-advbox — gestão processual
- mcp-projuris — gestão processual

**Open-source strategy:** Todos os MCP servers vão ser publicados em `github.com/dario-legal-br/*` para captura de comunidade.

## Pricing Tiers

| Tier | Preço | Para | Inclui |
|---|---|---|---|
| **Trial** | Grátis 7d | Avaliação | 15 skills + 3 MCP + 50 peças (acesso completo) |
| **LEX-BR Solo** | R$ 297/mês | Advogado individual | 15 skills + 3 MCP + 50 peças/mês |
| **LEX-BR Office** | R$ 997/mês | Escritório <10 advs | + 5 MCP + 200 peças + multi-client memory + DMS |
| **LEX-BR Enterprise** | R$ 4-12K/mês | Escritório/Dept. jurídico | + 8 MCP + ilimitado + multi-tenant + DPA Anthropic + SLA 4h |

## Quick Start — 2 opções de instalação

### Opção A — Installer dedicado LEX-BR (recomendado para advogados)

```bash
npx github:bardapraiacaraiva/lex-br-installer
```

Descarrega APENAS o subset jurídico:
- 15 skills BR-native
- 3 MCP servers (JusBrasil, CNJ DataJud, STF)
- 6 módulos compliance (OAB + LGPD + ZDR + cite + privilege + audit)
- License manager + guard

**Vantagem:** branding LEX-BR puro, menor footprint, focado em advocacia.

### Opção B — Installer DARIO completo (super-product)

```bash
npx github:bardapraiacaraiva/dario-orchestrator-installer
```

Descarrega TUDO:
- LEX-BR (idem opção A)
- + 269 skills DARIO (marketing, SEO, dev, design, contabilidade PT)
- + 28 skills DIVA (arquitectura, design de interiores, obras)
- + 18 cognitive modules + 6 operational modules

**Vantagem:** suite completa. Útil se escritório também precisa de marketing/social media/web dev.

### Após instalar (qualquer opção)

### Install
```bash
npx github:bardapraiacaraiva/dario-orchestrator-installer
```

### Activar VIP key
```bash
python ~/.claude/orchestrator/license_manager.py --activate DARIO-XXXX-XXXX-XXXX-LXS
```
(LXS = Solo, LXO = Office, LXE = Enterprise)

### Trial 7d
```bash
python ~/.claude/orchestrator/license_manager.py --init-trial
```

### Configurar escritório (LGPD marker)
```bash
python ~/.claude/orchestrator/lex-br/compliance/lgpd_marker.py \
  --configure --escritorio "XYZ Adv" --dpo dpo@xyz.com.br
```

### Usar skill
```
/lex-trabalhista:reclamacao_inicial <descrição do caso>
```

## Estrutura de directórios

```
~/.claude/orchestrator/lex-br/
├── manifesto.yaml              # Identity + values + coverage + roadmap
├── README.md                   # Este arquivo
├── compliance/                 # 6 módulos compliance
│   ├── __init__.py
│   ├── oab_205_gate.py
│   ├── lgpd_marker.py
│   ├── zdr_check.py
│   ├── cite_checker.py
│   ├── privilege_marker.py
│   └── audit_oab.py
├── memory/                     # Memory subsystem
│   ├── playbooks/{cliente}/
│   ├── precedentes/{area}/
│   ├── peticoes_templates/{skill}/  # 360+ templates
│   └── compliance_log/{date}.yaml
└── mcp_servers/                # 3 implementados + 5 planeados
    ├── jusbrasil/server.py
    ├── cnj_datajud/server.py
    ├── stf/server.py
    └── ...

~/.claude/skills/
├── lex-civil/SKILL.md
├── lex-commercial/SKILL.md
└── ... (15 total)
```

## Diferenciação Competitiva

| Player | Oferece | Gap |
|---|---|---|
| **Claude genérico (Anthropic)** | LLM + plugins genéricos | Sem BR-native, sem MCP BR, sem compliance OAB |
| **JusBrasil** | Dados jurisprudência | Sem IA, sem geração de peças |
| **ADV Box / Projuris** | Gestão processual | Sem IA, sem análise |
| **CP Pro / Lexter** | LegalGPT BR / LegalTech BR | Single-shot, sem orquestração, sem MCP, sem auto-learning |
| **LEX-BR** | **15 skills BR + 3-8 MCP + compliance built-in + orquestração + auto-learning** | **Único no mercado BR** |

## Roadmap

- **v1.0.0** (2026-05-19) — Foundation + 15 skills + 3 MCP + compliance ✓
- **v1.1.0** — 5 MCP restantes + 360 templates curados por consultor
- **v1.2.0** — Beta com 5 advogados reais + iteração
- **v1.3.0** — Production launch + Stripe BR + marketing AB2L
- **v2.0.0** — SaaS hospedado (alternativa ao local install)

## Limitações conhecidas

- **Jurisprudência live** requer `JUSBRASIL_API_KEY` (modo STUB sem)
- **Templates** ainda não validados por advogado consultor (planeado v1.1)
- **Trial bypass two-step** (delete .trial_fingerprint + license.json juntos) — documentado, requer server-side para fix completo
- **TST/TRTs específicos** não estão em mcp-jusbrasil stub (apenas STJ/STF mock)

## Compliance disclaimers

> LEX-BR é assistente de IA, não substitui assessoria jurídica. Todas as análises e peças requerem revisão por advogado inscrito na OAB. Provimento OAB 205/2021 art. 6º: o advogado é único responsável pelo conteúdo final.

## Suporte

- **Issues:** github.com/bardapraiacaraiva/dario-orchestrator/issues (tag `lex-br`)
- **VIP support (Office/Enterprise):** WhatsApp dedicado + Slack channel
- **Comunidade:** AB2L + grupo Erik Navarro "A Nova Elite da Advocacia"

## Related docs

- Manifesto: `~/.claude/orchestrator/lex-br/manifesto.yaml`
- Audit técnico inicial: `Obsidian: 2026-05-19 - LEX-BR Agent - Auditoria PDF + Proposta Tecnica.md`
- Companion: DARIO Orchestrator README + COGNITIVE-AUDIT-v11.1.md
