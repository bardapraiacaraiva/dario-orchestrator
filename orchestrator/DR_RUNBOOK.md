# DARIO Orchestrator — Disaster Recovery Runbook

**Version:** 1.0 (2026-05-25, Faixa 1 #6)
**Owner:** Barda (solo)
**Reviewed:** monthly (1st Monday); after any DR drill

---

## Service tier definition

DARIO Orchestrator is a **Tier 2 — Important Internal Tool**:
- Loss disrupts daily consulting workflow but does not directly affect
  paying clients' production systems (those are separate deployments).
- Recovery within 24 hours is acceptable.
- Data loss up to 7 days is tolerable (weekly backups + git history).

If DARIO becomes a Tier 1 product (SaaS for paying clients), this runbook
must be revised to a hot-standby model with synchronous replication.

## Recovery objectives (declared)

| Metric | Target | Definition |
|---|---|---|
| **RTO** (Recovery Time Objective) | **24 hours** | Time from disaster declaration to fully-functional orchestrator |
| **RPO** (Recovery Point Objective) | **7 days** | Maximum tolerable data loss (= weekly backup cadence) |
| **MTTR** (Mean Time To Recover) | **4 hours** | Realistic restore time on a known-good backup |
| **Drill cadence** | **Quarterly** | Practiced restore on a clean machine, end-to-end |

---

## Disaster scenarios + response

### Scenario A — Working machine destroyed/lost
**Severity:** HIGH · **Frequency:** rare · **RTO:** 24h

**Symptoms:** laptop stolen, disk failed, OS unbootable, ransomware.

**Response:**
1. Acquire replacement hardware (Windows preferred — DARIO tested on Win11)
2. Follow **Full Restore Procedure** below
3. Validate via post-restore checklist
4. Resume work

### Scenario B — Accidental deletion of orchestrator directory
**Severity:** MEDIUM · **Frequency:** uncommon · **RTO:** 30 min

**Symptoms:** `rm -rf ~/.claude/orchestrator` or equivalent typo.

**Response:**
1. STOP all DARIO processes (`taskkill /f /im python.exe` if needed)
2. `cd ~/.claude && git checkout HEAD -- orchestrator/`
3. Restore runtime state from latest local backup (see below)
4. Re-run `pytest` to validate

### Scenario C — Corrupted database (dario.db)
**Severity:** MEDIUM · **Frequency:** rare · **RTO:** 1h

**Symptoms:** SQLite errors on every read; integrity_check fails.

**Response:**
1. Backup the corrupted file: `cp orchestrator/core/dario.db corrupted-$(date +%s).db`
2. Restore from latest runtime tarball (see Full Restore step 4)
3. Re-run migrations: `python orchestrator/scripts/migrate_quality_to_sqlite.py --apply`
4. Validate with `python -m pytest tests/test_db_v3_polished_and_spend.py`

### Scenario D — Compromised audit private key (.audit_privkey)
**Severity:** HIGH · **Frequency:** rare · **RTO:** 2h

**Symptoms:** suspicion of theft, machine compromise, or accidental git push.

**Response:**
1. STOP all signing operations immediately
2. Generate new keypair (`python core/audit_signing.py init`)
3. Archive old `audit_pubkey.pem` to `security/archived-keys/YYYY-MM-DD-pre-rotation.pem`
4. Commit new `audit_pubkey.pem`
5. Document rotation in `security/TRIAGE_YYYY-MM-DD.md` with reason
6. ALL pre-rotation entries remain verifiable with the ARCHIVED public key
7. ALL post-rotation entries verify with the NEW public key

**Important:** Compromised key means an attacker could have signed forgeries
between compromise time and rotation. Cross-reference suspicious entries
against `seal-*.json` files (which were sealed before compromise) for
ground truth.

### Scenario E — GitHub repo compromised (origin or full)
**Severity:** HIGH · **Frequency:** very rare · **RTO:** 4h

**Symptoms:** force-push without your knowledge, unexpected commits, branch deletions.

**Response:**
1. Disable token/PAT immediately
2. `git remote remove origin && git remote remove full`
3. Restore from latest `*.bundle` in `~/.claude-backups/`:
   ```bash
   cd /tmp/restore-check
   git clone --bare ~/.claude-backups/<latest>/dario-orchestrator.bundle
   # Inspect for tamper
   git -C dario-orchestrator.bundle log --oneline -20
   ```
4. Force-push the bundled state back to a NEW remote (don't reuse compromised one)
5. Update local `git remote set-url` to the new remote
6. Audit GitHub: review SSH keys, deploy tokens, branch protection settings

---

## Full Restore Procedure (from scratch)

**Prerequisites on new machine:**
- Python 3.13+ (`python --version`)
- Git 2.40+ (`git --version`)
- Node 18+ (`node --version`) — for installer use
- 5 GB free disk
- Internet access for `pip install` from PyPI

### Step 1 — Acquire backup
Most recent backup is in `~/.claude-backups/YYYY-MM-DD-<tag>/` on:
- Primary machine (lost in this scenario)
- OneDrive sync of memory files: `C:/Users/barda/OneDrive/Documents/D.A.R.I.O/`
- External media (if you have a copy — recommend buying 1 USB stick)

**The 4.7M backup contains:**
- `dario-orchestrator.bundle` (4.2M) — full git history
- `dario-orchestrator-installer.bundle` (87K)
- `memory.tar.gz` (170K) — 84 user memory files
- `orchestrator-runtime.tar.gz` (303K) — budgets, audit, quality, dream, .master_secret, .license, dario.db

### Step 2 — Restore orchestrator repo
```bash
mkdir -p ~/.claude && cd ~/.claude
git clone /path/to/backup/dario-orchestrator.bundle .
git remote add origin https://github.com/bardapraiacaraiva/dario-orchestrator.git
git remote add full   https://github.com/bardapraiacaraiva/dario-orchestrator-full.git
git fetch --all
git reset --hard origin/master   # if remote has newer commits than bundle
```

### Step 3 — Restore user memory
```bash
mkdir -p ~/.claude/projects/C--Users-barda
cd ~/.claude/projects/C--Users-barda
tar -xzf /path/to/backup/memory.tar.gz
```

### Step 4 — Restore runtime state
```bash
cd ~/.claude/orchestrator
tar -xzf /path/to/backup/orchestrator-runtime.tar.gz
```

### Step 5 — Recreate venv
```bash
cd ~/.claude/orchestrator
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e ".[test,observability]"
```

### Step 6 — Restore installer repo (optional but recommended)
```bash
cd ~
git clone /path/to/backup/dario-orchestrator-installer.bundle dario-orchestrator-installer
cd dario-orchestrator-installer
git remote set-url origin https://github.com/bardapraiacaraiva/dario-orchestrator-installer.git
```

### Step 7 — Reinstall settings hooks
`~/.claude/settings.json` is gitignored (contains secrets). Restore manually:
1. Recreate from memory of structure (templates in `examples/settings.json.example` — TODO: ship one)
2. Or copy from another DARIO install if you have one

### Step 8 — Post-restore validation
```bash
cd ~/.claude/orchestrator

# Test suite
python -m pytest -m "not slow" -q
# Expected: 580+ pass

# SLO check
python scripts/slo_check.py
# Expected: 3/3 ok (after first cron run)

# Audit chain integrity
python core/audit_signing.py verify audit/$(date +%Y-%m-%d).yaml
# Expected: OK or skip if no signed entries today

# Pulse smoke
python cron_daily.py --dry-run --force
# Expected: 9 jobs, status warn or ok

# Dispatch smoke
python dispatch/dispatch_engine.py --status
# Expected: WORKER AVAILABILITY printed
```

### Step 9 — Resume backup cadence
```powershell
# Windows: reinstall scheduled task
powershell -ExecutionPolicy Bypass -File ~/.claude/orchestrator/scripts/backup_install_cron.ps1
```

---

## Drill log

| Date | Operator | Scenario | Result | Notes |
|---|---|---|---|---|
| 2026-05-25 12:53 | Claude | Restore from latest backup to /tmp isolated dir | ✅ **PASS** 0/0 fails/warns | Full restore in ~5s. 83 memory files, all 8 critical paths present, bundle integrity verified, .license + .master_secret restored. dario.db=0 bytes (was empty at backup time, not failure). Drill log: `security/dr_drill_log.jsonl` |
| (next: 2026-08-25 quarterly) | | | | |

---

## Validation: drill script

A non-destructive drill validates restore-ability without touching the
production install. See `scripts/dr_drill.sh`.

```bash
bash ~/.claude/orchestrator/scripts/dr_drill.sh
# Pulls latest backup, restores to /tmp/dr-drill/, runs validation suite
```

## What this runbook does NOT cover (intentional)

- **Multi-region failover** — DARIO is single-machine; no replication
- **Hot standby** — there is no warm secondary; cold restore only
- **Synchronous backups** — weekly cadence; data loss up to 7 days accepted
- **GDPR data subject requests** — separate procedure required (defer)
- **Cryptographic erasure** — wipes via key destruction not implemented

Pivoting to a SaaS product (Path C from audit) would require all of these.
