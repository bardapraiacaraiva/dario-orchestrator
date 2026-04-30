---
name: adriana-reception
description: "ADRIANA Visitor Management — registration, NDAs, room booking, hospitality, VIP protocols"
version: "1.0"
---

# ADRIANA-RECEPTION: Gestao de Visitantes e Recepcao

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** visitante, recepcao, registo visitas, NDA, reserva sala, hospitalidade, VIP, fornecedor visita, cliente visita, entrega, correio, portaria
**Trigger words (EN):** visitor, reception, visitor registration, NDA, room booking, hospitality, VIP protocol, guest, front desk, lobby, delivery, mail

Activar quando o utilizador precisa de:
- Registar visitantes
- Preparar recepcao de clientes ou fornecedores
- Gerir NDAs para visitantes
- Reservar salas para reunioes externas
- Definir protocolos VIP
- Gerir entregas e correspondencia

## Workflow Passo-a-Passo

### 1. Pre-Visita: Preparacao

**Checklist de preparacao (24h antes):**
- [ ] Visitante confirmado (nome, empresa, hora chegada)
- [ ] Sala reservada e preparada
- [ ] Anfitriao notificado
- [ ] NDA preparado (se necessario)
- [ ] Equipamento sala verificado (projector, wifi, etc.)
- [ ] Recepcao informada (nome visitante, anfitriao, horario)
- [ ] Parking reservado (se disponivel)
- [ ] Badge/cartao visitante preparado
- [ ] Hospitality: agua, cafe, materiais (conforme protocolo)

### 2. Registo de Visitantes

```markdown
# Registo de Visita
**Ref:** VIS-YYYY-MM-DD-NNN
**Data:** YYYY-MM-DD

## Visitante
| Campo | Valor |
|-------|-------|
| Nome completo | [Nome] |
| Empresa | [Empresa] |
| Contacto | [Telefone/email] |
| Documento ID | [Tipo + ultimos 4 digitos] |
| Hora entrada | HH:MM |
| Hora saida | HH:MM |
| Anfitriao | [Nome colaborador] |
| Motivo visita | [Reuniao / Entrega / Manutencao / Auditoria] |
| NDA assinado | [Sim/Nao/N.A.] |
| Badge # | [Numero] |
| Acompanhado | [Sim — por quem] |
| Areas visitadas | [Lista] |

## Notas
[Observacoes relevantes]

---
Assinatura visitante: _______________ Data/Hora: _______________
```

### 3. Protocolos por Tipo de Visitante

#### Visitante Standard (Fornecedor, Candidato, etc.)
| Passo | Accao | Responsavel |
|-------|-------|-------------|
| 1 | Recepcao: identificar e registar | Recepcao |
| 2 | Notificar anfitriao | Recepcao |
| 3 | Entregar badge visitante | Recepcao |
| 4 | Acompanhar ate sala | Recepcao/Anfitriao |
| 5 | Oferecer agua/cafe | Recepcao |
| 6 | Reuniao | Anfitriao |
| 7 | Acompanhar a saida | Anfitriao |
| 8 | Recolher badge | Recepcao |
| 9 | Registar hora saida | Recepcao |

#### Visitante VIP (Cliente importante, Parceiro estrategico, Investidor)
| Passo | Accao | Responsavel |
|-------|-------|-------------|
| 1 | Parking reservado + sinalizacao | Facilities |
| 2 | Recepcao pelo Director/CEO na entrada | Direccao |
| 3 | Registo express (pre-preenchido) | Recepcao |
| 4 | Sala premium preparada (agua, fruta, materiais marca) | Office manager |
| 5 | Apresentacao empresa (se primeira visita) | Direccao |
| 6 | Almoco/jantar (se aplicavel) | Direccao |
| 7 | Follow-up agradecimento em 24h | Anfitriao |

#### Visitante Tecnico (Manutencao, IT, Inspeccao)
| Passo | Accao | Responsavel |
|-------|-------|-------------|
| 1 | Verificar ordem de servico/autorizacao | Recepcao |
| 2 | NDA obrigatorio (se acesso a areas sensiveis) | Recepcao |
| 3 | Acompanhamento obrigatorio | Facilities |
| 4 | Registo de areas acedidas | Facilities |
| 5 | Verificacao de trabalho concluido | Facilities |
| 6 | Registo saida com notas | Recepcao |

### 4. NDA para Visitantes

```markdown
# Acordo de Confidencialidade — Visitante

**Data:** YYYY-MM-DD
**Visitante:** [Nome completo]
**Empresa:** [Empresa]
**Anfitriao:** [Nome], [Empresa anfitria]

Pelo presente, o Visitante compromete-se a:

1. Manter confidencial toda a informacao observada, recebida ou a que
   tenha acesso durante a visita as instalacoes de [Empresa].

2. Nao fotografar, filmar ou gravar nas instalacoes sem autorizacao
   expressa e por escrito.

3. Nao reproduzir, copiar ou transmitir qualquer informacao ou material
   a que tenha acesso.

4. Devolver qualquer material entregue no final da visita.

Este acordo vigora por um periodo de [2] anos a contar da data da visita.

Assinatura visitante: _______________
Data: _______________
```

### 5. Gestao de Correspondencia e Entregas

**Processo de recepcao:**
```
ENTREGA → REGISTO → NOTIFICACAO DESTINATARIO → LEVANTAMENTO → ARQUIVO
```

**Registo de entregas:**
| Data/Hora | Remetente | Destinatario | Tipo | Estado | Levantamento |
|-----------|-----------|-------------|------|--------|-------------|
| DD/MM HH:MM | [Empresa] | [Nome] | Encomenda | Entregue | DD/MM HH:MM |
| DD/MM HH:MM | [Empresa] | [Nome] | Carta reg. | Pendente | — |

### 6. Gestao de Salas para Visitas Externas

**Matriz de salas para visitantes:**
| Sala | Capacidade | Nivel | Equipamento | Uso recomendado |
|------|-----------|-------|-------------|-----------------|
| Sala Cliente | 6 | Premium | TV 55", webcam, whiteboard | Clientes VIP |
| Sala Reuniao A | 8 | Standard | Projector, whiteboard | Reunioes gerais |
| Sala Reuniao B | 4 | Standard | TV, webcam | Calls com visitantes |
| Sala Entrevista | 2 | Basico | Mesa, cadeiras | Entrevistas, 1:1 |

**Preparacao sala (30min antes):**
- [ ] Mesa limpa e arrumada
- [ ] Equipamento testado (ligar, testar conectividade)
- [ ] Agua e copos disponiveis
- [ ] Material de escrita (bloco + caneta)
- [ ] Wifi: credenciais de visitante impresso/disponivel
- [ ] Temperatura adequada (ajustar AC)
- [ ] Material de marketing (se aplicavel)

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana reception register [visitante]` | Registar visitante |
| `adriana reception prepare [data] [hora]` | Preparar recepcao |
| `adriana reception nda [visitante]` | Gerar NDA para visitante |
| `adriana reception vip [visitante]` | Activar protocolo VIP |
| `adriana reception deliveries` | Lista entregas pendentes |
| `adriana reception log [periodo]` | Historico de visitas |
| `adriana reception room [sala] [data]` | Reservar sala |

## Template de Output

```markdown
## Registo Visitas — [Periodo]

### Resumo
- Total visitas: X
- Visitas VIP: X
- NDAs assinados: X
- Media duração visita: Xh

### Visitantes Frequentes
| Visitante | Empresa | Visitas | Ultimo |
|-----------|---------|---------|--------|
| [Nome] | [Empresa] | X | DD/MM |

### Entregas
- Recebidas: X
- Pendentes levantamento: X
- Tempo medio levantamento: Xh

### Utilizacao Salas
| Sala | Bookings | Taxa ocupacao |
|------|----------|---------------|
| [Sala] | X | XX% |
```

## Red Flags

- Visitante sem registo (seguranca e RGPD)
- Visitante nao acompanhado em areas restritas
- NDA nao assinado quando necessario
- Badge de visitante nao devolvido
- Sala nao preparada para reuniao com cliente
- Entregas nao notificadas ao destinatario
- Dados de visitantes retidos alem do necessario (RGPD)
- Sem procedimento para emergencia com visitante nas instalacoes
- WiFi de visitante com acesso a rede interna

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-facilities** | Salas, equipamento, controlo acesso |
| **adriana-calendar** | Reservas de sala no calendario |
| **adriana-meetings** | Reunioes com visitantes externos |
| **adriana-docs** | NDAs geridos como documentos |
| **adriana-archive** | Registo de visitas — retencao RGPD |
| **adriana-policies** | Politica de visitantes |
| **adriana-sop** | SOP de recepcao |
| **dario-legal** | NDAs e conformidade |
| **risco-rgpd** | Dados pessoais de visitantes |

## Contexto Portugal

- RGPD: dados de visitantes sao dados pessoais — base legal: interesse legitimo (seguranca)
- Retencao: dados de visitantes max 30 dias (a menos que necessidade legal)
- Videovigilancia: informar visitantes (placa visivel na entrada)
- Lei 34/2013: seguranca privada — se empresa de seguranca, verificar licenca
- SHST: visitantes cobertos pelo plano de emergencia interno
- NDA: valido sob lei portuguesa sem necessidade de reconhecimento notarial
