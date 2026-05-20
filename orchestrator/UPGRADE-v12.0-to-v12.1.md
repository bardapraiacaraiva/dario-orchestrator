# Upgrade DARIO Orchestrator v12.0 → v12.1

**Date:** 2026-05-20
**Target audience:** VIP customers que já têm v12.0 instalado localmente
**Estimated time:** 5-10 min
**Reversibility:** Sim (rollback via git reset)

---

## TL;DR (3 comandos)

Se tens `~/.claude/orchestrator/` clonado do VIP repo `dario-orchestrator-full`:

```bash
cd ~/.claude/orchestrator
git pull full master
python scripts/upgrade_v12_1.py
```

Faz tudo automaticamente. Read this doc só se quiseres entender o que mudou OU se algo falhar.

---

## O que vem em v12.1

### Novos squads / skills (62 skills nesta release)

| Skill family | Quantidade | Propósito |
|---|---|---|
| `a360-director` | 1 | Diagnostic routing 6-fase para A360 squad |
| `prometheus-*` | 8 | Meta-evolution squad (Wave 1: 5 sensors + Wave 2: 3 decay detectors) |
| `dream` | 1 | Slash command para Memory & Dreaming subsystem |
| Community skills | 23 | accessibility, banana, builder-*, framer-motion-animator, gsap, etc. |
| Outros | 29 | scroll-animations, shadcn-ui, supabase, tailwindcss, threejs, etc. |

### Novos artefactos

| Categoria | Files | Localização |
|---|---|---|
| A360 templates estruturais | 4 | `skills/a360-{modelo,validacao,nicho,oferta}/templates/` |
| A360 examples anonimizados | 2 | `skills/a360-{modelo,nicho}/examples/` |
| Founder Bundle config | 1 | `orchestrator/bundles/founder.yaml` |
| PROMETHEUS KB files | 3 | `orchestrator/prometheus/findings/` (deprecations_kb, version_baselines, fact_sources) |
| PROMETHEUS state files | 5 | `orchestrator/prometheus/state/` (last_run, etc.) |
| Scripts de operação | 3 | `prometheus_cron.py`, `prometheus_decay_scan.py`, `prometheus_wave3_reminder.py` |

### Mudanças em arquivos existentes

- `company.yaml` — +260 linhas (agents_meta_evolution + workers_prometheus + workers_a360 + squads_* + dispatch_* + governance)
- `skill_chains.yaml` — +7 chains (6 A360 + 1 prometheus_weekly_scan)
- `12 skills a360-*` — frontmatter upgrade v12.0 standard (+license, +parent_agent, +compliance)
- `2 skills oraculo-*` — fix histórica references (Claude 3 Sonnet + GPT-3.5 strikethrough)

### Cognitive layer (já estava em v12.0, agora oficial)

- 18 modules (Sprints 1-4 + U11-U18, 216/216 tests)
- Memory & Dreaming subsystem (4 camadas + 4 fases)
- `dream_cli.py` + `/dream` slash command
- Daily cron 03:00 BRT (já configurado em v12.0, manter)

---

## Upgrade automatizado (recomendado)

### 1. Backup primeiro

```bash
cd ~/.claude/orchestrator
# Backup do estado actual antes do pull
zip -r ~/dario-orchestrator-pre-v12.1.zip . -x "__pycache__/*" "*.pyc" ".git/*"
```

Ou via PowerShell (Windows):
```powershell
Compress-Archive -Path "$env:USERPROFILE\.claude\orchestrator\*" -DestinationPath "$env:USERPROFILE\dario-orchestrator-pre-v12.1.zip" -CompressionLevel Optimal
```

### 2. Pull

```bash
cd ~/.claude/orchestrator
git fetch full
git pull full master
```

**Conflitos esperados:** Se tens mudanças locais não-committed em `company.yaml`, `skill_chains.yaml`, ou skills tocados pelo upgrade, vais ver merge conflicts. Resolve manualmente OR stash primeiro:
```bash
git stash --include-untracked
git pull full master
git stash pop
```

### 3. Run migration script

```bash
cd ~/.claude/orchestrator
python scripts/upgrade_v12_1.py
```

O script faz:
- ✅ Cria `orchestrator/prometheus/` directory structure se não existe
- ✅ Inicializa state YAML files vazios (last_run, last_seen_releases, etc.)
- ✅ Adiciona ao `~/.claude/.gitignore` os state files se ainda não estão
- ✅ Cria scheduled task "PROMETHEUS Weekly" (Sunday 22h00 BRT) se não existe
- ✅ Cria scheduled task "PROMETHEUS Wave 3 Reminder" (one-shot 2026-06-17) se não existe
- ✅ Valida que cron_daily continua activo (Memory & Dreaming)
- ✅ Re-indexa skills novas na RAG (se RAG engine estiver running)
- ✅ Verifica integridade pos-upgrade

### 4. Restart se RAG engine estava activo

```bash
# Stop RAG engine (Ctrl+C se foreground OR kill via task manager)
# Start novo
cd /c/dario-rag/engine
.venv/Scripts/python.exe main.py &
```

---

## Upgrade manual (se preferir controlo total)

### Step 1: Verifica estado antes

```bash
cd ~/.claude/orchestrator
git status
git log --oneline -5
```

Confirma que estás em `2991040` (v12.0) ou commit posterior.

### Step 2: Pull e revisa diff

```bash
git fetch full
git log --oneline full/master ^master  # commits novos
git diff master full/master --stat       # impact summary
```

### Step 3: Resolve conflitos manualmente se houver

```bash
git merge full/master
# Resolve qualquer conflito
git add <resolved files>
git commit
```

### Step 4: Inicializa PROMETHEUS state manualmente

Se não rodaste `upgrade_v12_1.py`, faz manualmente:

```bash
mkdir -p ~/.claude/orchestrator/prometheus/{state,digests,findings,experiments}
```

Os state files YAML são auto-criados na primeira execução de `prometheus_cron.py`. KB files JÁ vêm no pull.

### Step 5: Configura Task Scheduler (Windows)

```powershell
# Weekly cron PROMETHEUS Wave 1 + Wave 2
schtasks /create /tn "PROMETHEUS Weekly" /sc weekly /d SUN /st 22:00 `
  /tr '"C:\dario-rag\engine\.venv\Scripts\python.exe" "C:\dario-rag\scripts\prometheus_cron.py"' /f

# One-shot reminder para Wave 3 review em 2026-06-17
schtasks /create /tn "PROMETHEUS Wave 3 Reminder" /sc once /sd 17/06/2026 /st 09:00 `
  /tr '"C:\dario-rag\engine\.venv\Scripts\python.exe" "C:\dario-rag\scripts\prometheus_wave3_reminder.py"' /f
```

**Notas:**
- `/rl HIGHEST` requer admin. Sem ele, task corre só em login interactive (OK para desktop pessoal).
- Adapta paths se tens RAG noutro local que não `C:\dario-rag\`.

### Step 6: Verifica RAG ingest dos novos skills

```bash
cd /c/dario-rag
.venv/Scripts/python.exe scripts/bulk_ingest_skills.py
```

Output esperado: ~9 skills novos ingeridos + ~543 já existentes (hash-skip).

### Step 7: Smoke test

```bash
cd ~/.claude/orchestrator
python prometheus_decay_scan.py  # deve mostrar 0-2 findings
```

E confirma cron tasks:
```powershell
schtasks /query /tn "PROMETHEUS Weekly" /fo LIST
schtasks /query /tn "PROMETHEUS Wave 3 Reminder" /fo LIST
```

---

## Rollback (se necessário)

```bash
cd ~/.claude/orchestrator
git reset --hard 2991040    # volta para v12.0
git clean -fd               # remove arquivos novos não-tracked
```

**Atenção:** rollback APAGA findings/state de PROMETHEUS criados pós-upgrade. Faz backup desses antes:
```bash
cp -r prometheus/findings prometheus/findings.backup
```

E delete scheduled tasks se quiseres:
```powershell
schtasks /delete /tn "PROMETHEUS Weekly" /f
schtasks /delete /tn "PROMETHEUS Wave 3 Reminder" /f
```

---

## What's NOT changed

- ✅ Tua `.master_secret` continua intacto (gitignored)
- ✅ Tua licença VIP continua válida (não há mudança no `license_manager.py` que afecte runtime)
- ✅ Tasks activos em `tasks/active/` preservados
- ✅ Memory entries em `memory/` preservados (episodic, semantic, procedural)
- ✅ Quality scores em `quality/` preservados
- ✅ Synaptic weights preservados

---

## What's expected to take time on first run

| Operation | Tempo | Razão |
|---|---|---|
| `git pull full master` | ~30s | 58 files, ~7MB delta |
| `upgrade_v12_1.py` | ~1 min | Setup + scheduled tasks + RAG re-ingest |
| First `prometheus_cron.py` (auto-trigger Domingo 22h) | ~30s | 4 external sensors + 1 decay scan |
| First weekly digest narrative (próxima sessão Claude) | ~1-2 min | Reads raw findings + produces 5 .md digests |

---

## Suporte

Se algo falhar:
1. Read logs em `~/.claude/orchestrator/prometheus/cron.log` + `decay_scan.log`
2. Check `git status` para conflitos
3. Read `MANUAL.md` para arquitectura geral
4. Email: barda@automationsolutionai.com

---

## Cross-references

- README.md (overview geral)
- MANUAL.md (operação detalhada)
- COGNITIVE-AUDIT-v11.1.md (cognitive layer arquitectura)
- `scripts/upgrade_v12_1.py` (este upgrade runner)
- `prometheus/README.md` (squad meta-evolution)
