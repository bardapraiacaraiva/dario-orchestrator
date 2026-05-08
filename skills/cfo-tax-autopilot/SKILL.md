---
name: cfo-tax-autopilot
description: >
  Piloto automatico fiscal PT — verifica calendario AT, gera alertas antes de deadlines,
  produz checklists de preparacao por obrigacao. Integra com heartbeat para verificacao
  automatica. IVA trimestral, IRC PPC, DMR mensal, DRI SS, SAF-T, IES, Modelo 22.
  Use quando: proximas obrigacoes fiscais, calendario AT, quanto tempo para IVA,
  o que preparar para IRC, alertas tax, fecho fiscal, deadlines AT.
tools: Read, Bash, Write, Edit
version: 1.0
---

# CFO Tax Autopilot — Piloto Automatico Fiscal PT

## Proposito

Garantir que **nenhuma obrigação fiscal é esquecida**. O sistema:
- Verifica automaticamente o calendário fiscal a cada heartbeat pulse
- Gera alertas 30/7/1 dias antes de cada deadline
- Produz checklists específicas de preparação por tipo de obrigação
- Marca obrigações como submitted/paid após confirmação humana
- Calcula penalidades potenciais se deadline for ultrapassado

## Comandos

| Comando | Descricao |
|---------|-----------|
| `/cfo-tax-autopilot` | Vista geral — todas as obrigações + semáforo |
| `/cfo-tax-autopilot next` | Próxima obrigação + checklist de preparação |
| `/cfo-tax-autopilot [id]` | Detalhe de uma obrigação específica |
| `/cfo-tax-autopilot overdue` | Obrigações em atraso |
| `/cfo-tax-autopilot month [MM]` | Obrigações de um mês específico |
| `/cfo-tax-autopilot submit [id]` | Marcar obrigação como submetida |
| `/cfo-tax-autopilot checklist [tipo]` | Checklist genérica por tipo (iva/irc/dmr/ss/saft) |

## Workflow

### Phase 1: LOAD CALENDAR

1. Ler `~/.claude/orchestrator/finance/tax_calendar.yaml`
2. Calcular para cada obrigação:
   - `days_until = deadline - today`
   - `status_color`: verde (>30d), amarelo (8-30d), laranja (1-7d), vermelho (overdue)
   - `is_recurring`: se tem `recurrence: monthly`, calcular próximo deadline

3. Para obrigações recorrentes (DMR, DRI, SS, SAF-T):
   ```python
   # Calcular próximo deadline
   if today.day <= deadline_day:
       next_deadline = date(today.year, today.month, deadline_day)
   else:
       next_month = today.month + 1 if today.month < 12 else 1
       next_year = today.year if today.month < 12 else today.year + 1
       next_deadline = date(next_year, next_month, deadline_day)
   ```

### Phase 2: ALERT GENERATION

| Dias até deadline | Nivel | Accao |
|-------------------|-------|-------|
| > 30 dias | INFO | Sem alerta — tudo ok |
| 8-30 dias | AVISO | Lembrete + checklist de preparação |
| 1-7 dias | URGENTE | Alerta forte + checklist detalhada + status de preparação |
| 0 dias | HOJE | DEADLINE HOJE — verificar se foi submetido |
| < 0 dias | OVERDUE | ATRASO — coima potencial + accão imediata |

### Phase 3: CHECKLISTS POR OBRIGAÇÃO

#### IVA Trimestral (Declaração Periódica)
```
Deadline: dia 15 do 2º mês após trimestre
Penalidade: Coima 150€ - 3.750€ + juros compensatórios

Checklist preparação (começar 15 dias antes):
- [ ] Verificar todas as facturas emitidas no trimestre (e-Fatura)
- [ ] Verificar todas as facturas recebidas (dedução IVA)
- [ ] Conciliar SAF-T mensal com registos contabilísticos
- [ ] Verificar operações intra-comunitárias (VIES)
- [ ] Calcular IVA a entregar: IVA liquidado - IVA dedutível
- [ ] Se IVA a recuperar: verificar se pede reembolso ou reporta
- [ ] Preencher Declaração Periódica no Portal das Finanças
- [ ] Validar campos: base tributável, IVA liquidado, IVA dedutível
- [ ] SUBMETER (requer aprovação humana)
- [ ] Guardar comprovativo de submissão
- [ ] Pagar até ao deadline (se IVA a entregar)
```

#### IRC (Modelo 22 / PPC)
```
Modelo 22 Deadline: último dia útil de Maio
PPC Deadlines: Julho (30%), Setembro (30%), Dezembro (40%)
Penalidade: Coima 150€ - 3.750€ + juros compensatórios

Checklist Modelo 22 (começar em Abril):
- [ ] Fechar contabilidade do exercício anterior
- [ ] Calcular resultado contabilístico (SNC)
- [ ] Identificar variações patrimoniais positivas/negativas
- [ ] Calcular correcções fiscais (gastos não aceites)
- [ ] Aplicar benefícios fiscais (SIFIDE, RFAI, etc.)
- [ ] Calcular matéria colectável
- [ ] Aplicar taxa IRC (21% geral, 17% PME primeiros 50K)
- [ ] Calcular derrama municipal (até 1.5%)
- [ ] Calcular tributação autónoma
- [ ] Deduzir PPC, retenções na fonte, PAC
- [ ] Preencher Modelo 22 no Portal das Finanças
- [ ] SUBMETER (requer aprovação humana)
- [ ] Pagar IRC apurado até deadline do Modelo 22

Checklist PPC:
- [ ] Verificar IRC do ano anterior (base cálculo)
- [ ] 1ª prestação: 30% do IRC anterior (Julho)
- [ ] 2ª prestação: 30% do IRC anterior (Setembro)
- [ ] 3ª prestação: 40% do IRC anterior (Dezembro)
- [ ] Guardar comprovativos de pagamento
```

#### DMR (Declaração Mensal de Remunerações)
```
Deadline: dia 10 do mês seguinte
Penalidade: Coima 50€ - 25.000€

Checklist (começar dia 1 do mês seguinte):
- [ ] Processar salários do mês
- [ ] Calcular retenções IRS por trabalhador
- [ ] Calcular contribuições SS (23.75% entidade + 11% trabalhador)
- [ ] Verificar subsídio alimentação (isento até 6€/dia em cartão, 4.77€ numerário)
- [ ] Incluir retenções sobre recibos verdes (se aplicável)
- [ ] Preencher DMR no Portal das Finanças
- [ ] SUBMETER até dia 10
```

#### DRI (Declaração de Remunerações SS)
```
Deadline: dia 10 do mês seguinte
Penalidade: Juros de mora 3% + coima

Checklist:
- [ ] Extrair dados salariais do mês
- [ ] Verificar TSU aplicável por trabalhador
- [ ] Verificar trabalhadores independentes (se economicamente dependentes)
- [ ] Submeter DRI na Segurança Social Directa
- [ ] PAGAR contribuições até dia 20
```

#### SAF-T Mensal
```
Deadline: dia 12 do mês seguinte
Penalidade: Coima 200€ - 10.000€

Checklist:
- [ ] Extrair SAF-T do software de facturação
- [ ] Validar ficheiro com validador AT
- [ ] Verificar: todas as facturas, notas crédito, recibos incluídos
- [ ] Verificar: numeração sequencial sem falhas
- [ ] Comunicar via Portal das Finanças (e-Fatura)
- [ ] Guardar comprovativo
```

#### IES (Informação Empresarial Simplificada)
```
Deadline: 15 de Julho
Penalidade: Coima + impossibilidade de obter certidão

Checklist (começar em Junho):
- [ ] Fechar contabilidade do exercício anterior (se não feito)
- [ ] Preencher Anexo A (informação contabilística — SNC)
- [ ] Preencher outros anexos aplicáveis
- [ ] Validar coerência com Modelo 22 já submetido
- [ ] SUBMETER no Portal das Finanças
```

### Phase 4: HEARTBEAT INTEGRATION

A cada pulse do heartbeat, o tax autopilot:

```python
# Integração no heartbeat step
import datetime

def check_tax_deadlines():
    """Chamado a cada heartbeat pulse"""
    calendar = load_yaml('finance/tax_calendar.yaml')
    today = datetime.date.today()
    alerts = []

    for obligation in calendar['obligations']:
        if obligation.get('recurrence') == 'monthly':
            # Calcular próximo deadline
            deadline = next_monthly_deadline(obligation['deadline_day'], today)
        else:
            deadline = parse_date(obligation['deadline'])

        days = (deadline - today).days

        if days < 0 and obligation['status'] != 'submitted':
            alerts.append({
                'id': obligation['id'],
                'level': 'OVERDUE',
                'name': obligation['name'],
                'days': abs(days),
                'penalty': get_penalty(obligation['id'])
            })
        elif days <= 7:
            alerts.append({
                'id': obligation['id'],
                'level': 'URGENT',
                'name': obligation['name'],
                'days': days
            })
        elif days <= 30:
            alerts.append({
                'id': obligation['id'],
                'level': 'WARNING',
                'name': obligation['name'],
                'days': days
            })

    return alerts
```

### Phase 5: OUTPUT

```markdown
## Tax Autopilot — [Data]

### Semaforo Fiscal
| Obrigacao | Deadline | Dias | Status | Preparacao |
|-----------|----------|------|--------|------------|
| [nome] | [data] | Xd | [cor] | [X/Y items done] |

### Proxima Obrigacao: [nome]
**Deadline:** [data] ([X dias])
**Penalidade se falhar:** [coima]

#### Checklist de Preparacao
- [ ] Step 1
- [ ] Step 2
- ...
- [ ] SUBMETER (requer aprovacao humana)

### Alertas
- [OVERDUE] [nome] — X dias em atraso. Coima potencial: EUR X
- [URGENTE] [nome] — X dias restantes. Iniciar preparacao AGORA.
- [AVISO] [nome] — X dias restantes. Agendar preparacao.

### Resumo Anual
| Obrigacao | Jan | Fev | Mar | ... | Dez |
|-----------|-----|-----|-----|-----|-----|
| DMR | OK | OK | OK | ... | — |
| DRI/SS | OK | OK | OK | ... | — |
| SAF-T | OK | OK | OK | ... | — |
| IVA Q1 | — | — | — | ... | — |
| IRC PPC | — | — | — | ... | — |
```

## Estado Management

Quando o utilizador confirma submissão:
```yaml
# Actualizar tax_calendar.yaml
- id: iva_q1
  status: submitted        # pending → submitted
  submitted_at: "2026-05-14"
  submitted_by: "barda"
  receipt_ref: "AT-2026-XXXXX"
```

Quando o utilizador confirma pagamento:
```yaml
- id: iva_q1
  status: paid             # submitted → paid
  paid_at: "2026-05-15"
  paid_amount: 1234.56
  payment_ref: "MB-XXXXX"
```

## Red Flags

| # | Red Flag | Consequencia |
|---|----------|-------------|
| 1 | Deadline ultrapassado sem submissão | Coima automatica AT |
| 2 | SAF-T com falhas na sequência | Rejeição + coima |
| 3 | DMR submetida sem incluir freelancers | Correcção obrigatória + coima |
| 4 | IVA calculado sem verificar intra-EU | Liquidação adicional |
| 5 | IRC sem tributação autónoma | Inspecção AT |
| 6 | PPC não pago no prazo | Juros compensatórios |
| 7 | IES inconsistente com Modelo 22 | Alerta AT para verificação |
| 8 | Obrigação marcada submitted sem comprovativo | Risco de disputa com AT |
