# LEX-BR Memory Structure

```
memory/
├── playbooks/              # Padrões por cliente (memória do escritório)
│   └── {cliente_hash}/
│       └── playbook.yaml   # estilo, escalation rules, jurisdição predominante
│
├── precedentes/            # Cache de jurisprudência por área
│   ├── trabalhista/
│   ├── civil/
│   └── ...
│
├── peticoes_templates/     # Templates editáveis por skill
│   ├── lex-civil/          # 30 templates
│   ├── lex-trabalhista/    # 40 templates
│   └── ...
│
└── compliance_log/         # Audit OAB-compatible (imutável)
    └── YYYY-MM-DD.yaml
```

## Sample playbook structure

```yaml
client_hash: client-abc123
escritorio_nome: "XYZ Advocacia"
dpo_contact: dpo@xyz-adv.com.br
oab_responsavel: "OAB/SP 123456"

areas_principais:
  - trabalhista
  - empresarial
  - lgpd

clientes_tipo:
  - PME (10-100 funcionários)
  - Profissionais liberais
  - E-commerce

style_guide:
  formalidade: alta
  uso_estrangeirismos: vedado
  citacao_jurisprudencia: completa (com link)
  citacao_doutrina: opcional

escalation_rules:
  baixa_complexidade: associado_junior
  media_complexidade: associado_senior
  alta_complexidade: socio_responsavel
  caso_estrategico: comitê_juridico

valores_estrategicos:
  acima_de_R$_1M: comitê_aprovação
  novos_contratos: revisão_dupla
  litigio_acima_R$_500K: sócio_responsável
```
