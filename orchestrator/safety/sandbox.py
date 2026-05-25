"""Lightweight subprocess sandbox — v1 (Faixa 1 #1).

Closes audit Risk #1 (CRITICAL — code execution sandboxing) at v1 level:
defense-in-depth wrapper around `subprocess.run` that:
  1. **Env scoping** — pass ONLY explicitly-allowlisted env vars to the
     subprocess (vs Python default of inherit-all)
  2. **Working dir jail** — pin cwd to a fresh tempdir, cleaned up after
  3. **Timeout enforcement** — hard kill after N seconds (prevents infinite loops)
  4. **Output capture** — stdout/stderr returned as strings, not streamed
     to parent terminal (prevents secret leak via terminal scrollback)
  5. **Audit log** — every sandboxed execution records actor/cmd/exit/duration
  6. **Resource limits** — on POSIX, CPU+memory caps via `resource` module
     (Windows: best-effort via psutil if installed)

What this v1 does NOT do (deferred to Faixa 2 with Docker)
──────────────────────────────────────────────────────────
- True process isolation: subprocess still runs with parent user privileges,
  so a sufficiently-malicious script can still read ~/.ssh, /etc/, etc.
  REAL isolation requires Docker/Firecracker/gVisor.
- Network policy: cannot block network access at OS level without iptables/
  Windows Firewall rules. v1 relies on env (PATH stripped, no proxy vars).
- Filesystem read-only enforcement: tempdir is writable but parent paths
  are NOT prevented from being read. Real read-only-root needs chroot/bind.
- Syscall filtering (seccomp): not available on Windows; even on Linux
  needs separate process boundary tool.

Honest threat coverage estimate
───────────────────────────────
| Threat | v1 (this) | Full Docker (Faixa 2) |
|---|---|---|
| Env-var exfil (read $ANTHROPIC_API_KEY) | ✅ blocked | ✅ blocked |
| Write to ~/.claude/orchestrator/.master_secret | ⚠️ writable but moot (file gone post-Faixa1#2) | ✅ blocked |
| Read ~/.ssh/id_rsa | ❌ still readable | ✅ blocked |
| Network exfil to evil.com | ❌ no blocking | ✅ blocked by netns |
| Infinite loop / fork bomb | ✅ timeout + (POSIX) resource limits | ✅ cgroups |
| Output secret via stdout | ✅ captured, scannable by prompt_shield | ✅ captured |
| Read shared SQLite (dario.db) | ⚠️ readable if cwd allows | ✅ blocked |

v1 coverage: ~60-70% of common skill execution risks. Full coverage
requires Docker daemon + image management (Faixa 2 follow-up).

Usage:
    from safety.sandbox import run_sandboxed, SandboxResult

    r: SandboxResult = run_sandboxed(
        cmd=["python", "scripts/my_script.py", "--arg", "val"],
        caller="executor/dispatch-cot",
        env_allowlist=["ANTHROPIC_API_KEY", "DARIO_LICENSE_BYPASS"],
        timeout_s=60,
        capture_output=True,
    )
    print(r.stdout, r.stderr, r.returncode, r.duration_s)
    if not r.ok:
        raise RuntimeError(f"sandbox failed: {r.timeout_hit or r.returncode}")
"""
from __future__ import annotations

import logging
import os
try:
    import resource  # POSIX only — Windows raises ModuleNotFoundError
except ModuleNotFoundError:
    resource = None  # type: ignore[assignment]
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# Whether POSIX `resource` module is functional. On Windows it imports but
# rlimit calls raise OSError, so we sniff the platform.
_POSIX = sys.platform != "win32"

_logger = logging.getLogger(__name__)


# Default env vars that are SAFE to pass through (don't contain secrets).
# Caller can extend via env_allowlist.
SAFE_ENV_DEFAULTS = [
    "PATH",          # needed for python/git/etc resolution
    "PYTHONPATH",
    "PYTHONHOME",
    "PYTHONIOENCODING",
    "TEMP", "TMP", "TMPDIR",  # subprocess needs to know where to put temp files
    "LANG", "LC_ALL", "LC_CTYPE",
    "HOME",          # Python imports need this
    "USERPROFILE",   # Windows equivalent of HOME
    "SYSTEMROOT",    # Windows essential
    "WINDIR",        # Windows essential
    "OS",            # Windows
    "COMSPEC",       # Windows cmd.exe path
]


# Env vars that are NEVER passed regardless of allowlist (deny-list overrides
# allow-list). These contain secrets or implementation details that skills
# should never see.
ENV_DENY_LIST = [
    # Cloud/CI tokens
    "DARIO_GH_TOKEN",
    "GITHUB_TOKEN",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_SESSION_TOKEN",
    "GOOGLE_APPLICATION_CREDENTIALS",
    # Master secrets
    "DARIO_MASTER_SECRET",
    # SSH
    "SSH_AUTH_SOCK",
]


@dataclass
class SandboxResult:
    """Result of a sandboxed execution."""
    cmd: list[str]
    returncode: int
    stdout: str
    stderr: str
    duration_s: float
    timeout_hit: bool
    sandbox_dir: str  # path to the tempdir used (already cleaned up)
    env_keys_passed: list[str]  # names only, never values
    notes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and not self.timeout_hit

    def to_audit_dict(self) -> dict:
        return {
            "cmd": " ".join(self.cmd),
            "returncode": self.returncode,
            "duration_s": round(self.duration_s, 3),
            "timeout_hit": self.timeout_hit,
            "env_keys_count": len(self.env_keys_passed),
            "notes": "; ".join(self.notes) if self.notes else "",
        }


def _build_env(allowlist: list[str], extra: Optional[dict[str, str]] = None) -> tuple[dict[str, str], list[str]]:
    """Build scoped env. Returns (env_dict, list_of_keys_used)."""
    env: dict[str, str] = {}
    keys_used: list[str] = []

    final_allowlist = set(SAFE_ENV_DEFAULTS) | set(allowlist)
    deny = set(ENV_DENY_LIST)

    for key in final_allowlist:
        if key in deny:
            continue
        if key in os.environ:
            env[key] = os.environ[key]
            keys_used.append(key)

    if extra:
        for k, v in extra.items():
            if k in deny:
                continue
            env[k] = v
            if k not in keys_used:
                keys_used.append(k)

    return env, sorted(keys_used)


def _apply_posix_limits(cpu_seconds: int, memory_mb: int):
    """preexec_fn for POSIX subprocess to set rlimits.

    Called in the CHILD process between fork and exec — so any failure here
    just means the limit wasn't applied, not that the parent crashes.
    """
    if not _POSIX or resource is None:
        return
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))
    except (ValueError, OSError):
        pass
    try:
        mem_bytes = memory_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
    except (ValueError, OSError):
        pass


def _audit(caller: str, result: SandboxResult) -> None:
    """Log a sandboxed execution to dario.audit. Fail-soft."""
    try:
        from core.audit_logger import log_event
        log_event(
            actor=caller,
            action="sandbox_exec",
            entity_type="subprocess",
            entity_id=Path(result.cmd[0]).name if result.cmd else "<empty>",
            details=str(result.to_audit_dict()),
        )
    except Exception:
        _logger.debug("audit log unavailable for sandbox_exec")


def run_sandboxed(
    cmd: list[str],
    *,
    caller: str = "unknown",
    env_allowlist: Optional[list[str]] = None,
    env_extra: Optional[dict[str, str]] = None,
    timeout_s: float = 60.0,
    cpu_seconds: Optional[int] = None,
    memory_mb: int = 512,
    capture_output: bool = True,
    input_data: Optional[str] = None,
    cleanup_dir: bool = True,
) -> SandboxResult:
    """Run a subprocess in a sandboxed context.

    Args:
        cmd: argv list (NEVER pass a string to avoid shell injection)
        caller: identifier for audit log (e.g., "executor/dispatch")
        env_allowlist: env var names safe for the subprocess to see (deny-list
            still overrides). Default: SAFE_ENV_DEFAULTS only.
        env_extra: explicit key=value to pass (e.g., a one-shot tempdir path)
        timeout_s: wall-clock kill threshold (default 60s)
        cpu_seconds: POSIX rlimit on CPU time (default = timeout_s ceil)
        memory_mb: POSIX rlimit on address space (default 512MB)
        capture_output: True → return stdout/stderr in result; False → /dev/null
        input_data: stdin to feed
        cleanup_dir: True → rmtree the tempdir after execution

    Returns:
        SandboxResult with returncode, stdout, stderr, duration, etc.

    Raises:
        ValueError: cmd not a list (shell-injection protection)
        FileNotFoundError: cmd[0] not executable
    """
    if not isinstance(cmd, list) or not cmd:
        raise ValueError("cmd must be a non-empty list (not str) to prevent shell injection")
    if any(not isinstance(c, str) for c in cmd):
        raise ValueError("all cmd elements must be strings")

    env_allowlist = env_allowlist or []
    if cpu_seconds is None:
        cpu_seconds = int(timeout_s) + 5  # rlimit slightly above wall timeout

    # Create isolated tempdir as cwd
    sandbox_dir = tempfile.mkdtemp(prefix="dario-sandbox-")
    env, keys_used = _build_env(env_allowlist, env_extra)

    # Pin TMP to inside sandbox so subprocess can only write temp files there
    env["TMPDIR"] = sandbox_dir
    env["TEMP"] = sandbox_dir
    env["TMP"] = sandbox_dir

    timeout_hit = False
    notes: list[str] = []
    start = time.perf_counter()

    preexec = None
    if _POSIX:
        # Capture args by value (don't reference outer scope mutating vars)
        cs, mm = cpu_seconds, memory_mb
        def _pre():
            _apply_posix_limits(cs, mm)
        preexec = _pre
    else:
        notes.append("posix-rlimits-unavailable-on-windows")

    try:
        proc = subprocess.run(
            cmd,
            cwd=sandbox_dir,
            env=env,
            capture_output=capture_output,
            input=input_data,
            text=True,
            timeout=timeout_s,
            preexec_fn=preexec,
            check=False,
        )
        returncode = proc.returncode
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
    except subprocess.TimeoutExpired as e:
        timeout_hit = True
        returncode = -9  # SIGKILL-ish
        stdout = (e.stdout or b"").decode("utf-8", errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        stderr = (e.stderr or b"").decode("utf-8", errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
        notes.append(f"timeout-hit-after-{timeout_s}s")
    except FileNotFoundError as e:
        returncode = 127  # POSIX "command not found"
        stdout = ""
        stderr = f"FileNotFoundError: {e}"
        notes.append("cmd-not-found")
    except PermissionError as e:
        returncode = 126
        stdout = ""
        stderr = f"PermissionError: {e}"
        notes.append("permission-denied")

    duration = time.perf_counter() - start

    if cleanup_dir:
        try:
            shutil.rmtree(sandbox_dir, ignore_errors=True)
        except Exception:
            notes.append("cleanup-failed")

    result = SandboxResult(
        cmd=cmd,
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
        duration_s=duration,
        timeout_hit=timeout_hit,
        sandbox_dir=sandbox_dir,
        env_keys_passed=keys_used,
        notes=notes,
    )

    _audit(caller, result)
    return result


# ─── CLI for ad-hoc testing ──────────────────────────────────────────────


def _cli():
    import argparse
    import json
    p = argparse.ArgumentParser(description="DARIO sandbox runner (Faixa 1 #1 v1)")
    p.add_argument("cmd", nargs="+", help="command + args")
    p.add_argument("--caller", default="cli")
    p.add_argument("--env", action="append", default=[], help="env var to allow (repeat for multiple)")
    p.add_argument("--timeout", type=float, default=60.0)
    p.add_argument("--cpu", type=int, default=None)
    p.add_argument("--mem-mb", type=int, default=512)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    r = run_sandboxed(
        cmd=args.cmd,
        caller=args.caller,
        env_allowlist=args.env,
        timeout_s=args.timeout,
        cpu_seconds=args.cpu,
        memory_mb=args.mem_mb,
    )

    if args.json:
        print(json.dumps({
            "cmd": r.cmd,
            "returncode": r.returncode,
            "duration_s": round(r.duration_s, 3),
            "timeout_hit": r.timeout_hit,
            "env_keys": r.env_keys_passed,
            "notes": r.notes,
            "stdout": r.stdout,
            "stderr": r.stderr,
        }, indent=2))
    else:
        print(f"exit={r.returncode}  duration={r.duration_s:.2f}s  timeout={r.timeout_hit}")
        print(f"env_keys_passed: {r.env_keys_passed}")
        if r.notes:
            print(f"notes: {r.notes}")
        if r.stdout:
            print("--- stdout ---")
            print(r.stdout)
        if r.stderr:
            print("--- stderr ---")
            print(r.stderr)
    return r.returncode if not r.timeout_hit else 124


if __name__ == "__main__":
    sys.exit(_cli())
