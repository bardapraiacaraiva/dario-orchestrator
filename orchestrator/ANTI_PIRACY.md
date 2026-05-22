# DARIO Anti-Piracy Stack — Defence in Depth (Onda 7 + 8 + 9)

This document is the operator's quick-reference for the layered enforcement
shipped with DARIO. None of these layers is bulletproof on its own; together
they raise the cost of bypass from "30 seconds" to "expert + several hours".

## Layer 1 — Local 3-layer fingerprint (Onda 7)

Three independent persistence locations for the trial activation marker:

1. `~/.claude/orchestrator/.trial_fingerprint` — visible, signed JSON.
2. `~/.dario-trial-{sha256(MASTER_SECRET+machine_id)[:16]}.bin` — obfuscated
   filename, hidden in $HOME.
3. `HKCU\Software\DARIO\TrialState` — Windows registry (winreg).

Deleting any subset → the remaining layers refuse re-init. Deleting *all*
layers IS allowed but represents an installer-level reset (e.g. fresh OS).

**Mitigates:** casual `rm license.json` bypass.

**Files:** `license_manager.py`.

## Layer 2 — License server (Onda 8)

Optional server-side enforcement. When env var `DARIO_LICENSE_SERVER` is set:

- `init_trial` posts `{machine_id}` to `/trial/activate`. The server's record
  of `first_init_at` is immutable; subsequent activations return the same
  record. Wiping all 3 local layers does NOT reset the server clock.
- `check_license` posts `{machine_id, token, client_first_init_at}` to
  `/trial/validate` once per hour. Server returns `valid=false,
  rollback_detected=true` if local and server timestamps diverge by more
  than the tolerance (default 1h).
- VIP customers get a permanent record via `/vip/activate`.

**Mitigates:** local file wipe, VM snapshot rollback, local clock tamper.

**Files:** `license_server/`, `license_client.py`, `license_manager.py`.

## Layer 3 — Certificate pinning (Onda 9 #1)

When the orchestrator talks to the license server over HTTPS, the leaf
certificate's SPKI SHA-256 must match `DARIO_LICENSE_CERT_PIN`. DNS hijacks
or MITM with a different cert fail closed *before* the HTTP request goes
out.

### Setup (operator)

```bash
# 1. Generate the server pin once after deploy:
python -m license_client --print-pin https://license.dario.io
# → prints 64-char hex

# 2. Distribute that hex to every install:
export DARIO_LICENSE_CERT_PIN=4f1c...c1d4

# 3. (optional) Verify a live server matches the pin:
python -m license_client --verify-pin https://license.dario.io
```

The pin survives normal cert renewals as long as the key pair is kept
across renewals — rotate the pin only when you intentionally regenerate
the private key.

**Mitigates:** DNS hijacking, MITM, fake servers spoofing your domain.

**Files:** `license_client.py` (`fetch_server_pin`, `_verify_pin_or_raise`).

## Layer 4 — Cython compilation (Onda 9 #2)

The three license-critical Python files can be compiled to native extension
modules (`.pyd` on Windows, `.so` on Linux) by:

```bash
cd ~/.claude/orchestrator
python build_obfuscated.py
# → license_client.cp313-win_amd64.pyd  (or matching .so)
# → license_manager.cp313-win_amd64.pyd
# → license_server/app.cp313-win_amd64.pyd

# Distribution mode — drop the .py originals after compile:
python build_obfuscated.py --remove-py
```

A casual user opening `license_manager.py` in a text editor sees a binary
blob instead of plaintext Python with `if 'machine_id' in ...`. A determined
attacker with cython-disasm + ghidra can still recover most logic.

**Prereqs:**
- Windows: Microsoft Visual C++ Build Tools 14+
- Linux:   `gcc` + `python3-dev`
- macOS:   `xcode-select --install`

If you don't have a local C toolchain, build in CI (GitHub Actions has
gcc on `ubuntu-latest`) and publish the wheels.

**Mitigates:** static analysis via `cat`, `grep`, `strings`. Slows down
casual disassembly significantly.

**Files:** `build_obfuscated.py` (generates `setup_obfuscated.py`).

## Layer 5 — Signed binaries (Onda 9 #3)

Bundle the orchestrator + license CLI into a single executable with
PyInstaller, then sign it with your code-signing certificate:

```bash
# Build
cd ~/.claude/orchestrator
pyinstaller scripts/dario_license.spec --clean --noconfirm

# Sign (Windows, cert in store)
python scripts/sign_bundle.py dist/dario-license.exe \
    --cert-subject "CN=Your Company Name"

# Sign (Windows, .pfx file)
DARIO_CERT_PFX_PASSWORD=secret python scripts/sign_bundle.py \
    dist/dario-license.exe --pfx ./cert.pfx

# Sign (macOS)
python scripts/sign_bundle.py dist/dario-license \
    --cert-identity "Developer ID Application: Your Co (TEAMID)"
```

Signed executables:
- Bypass Windows SmartScreen + macOS Gatekeeper warnings.
- Lose their signature on modification — Windows refuses to launch
  tampered binaries with the original publisher identity.

**Cert acquisition:**
- Windows: Sectigo, DigiCert, SSL.com — €150–€400/year for OV; €200–€700/year
  for EV (recommended for SmartScreen reputation).
- macOS: Apple Developer Program — $99/year.

**Mitigates:** end-user UX (no scary warnings), tampering detection.

**Files:** `scripts/dario_license.spec`, `scripts/sign_bundle.py`.

## Threat model summary

| Attack | Mitigated by | Cost to bypass |
|---|---|---|
| `rm license.json` | Layer 1 (3 layers) | 5 sec → still blocked |
| `rm` all 3 local layers | Layer 2 (server) | needs admin + DNS skill |
| VM snapshot rollback | Layer 2 (heartbeats + rollback detection) | needs snapshot reset every check |
| DNS hijack the server URL | Layer 3 (cert pin) | needs to compromise pin distribution |
| Disassemble `license_manager.py` | Layer 4 (Cython) | needs C reverse engineering |
| Run a tampered `.exe` | Layer 5 (code signing) | needs to break or buy a cert chain |
| Steal `MASTER_SECRET` | Operational (rotate it) | one-shot — rotate to recover |
| Steal `LICENSE_SERVER_SECRET` | Operational (rotate it) | one-shot — rotate + reissue tokens |

## What we still recommend (not in this repo)

- **Commercial obfuscator** like PyArmor 8+ — better than Cython for hiding
  control flow.
- **Hardware fingerprinting via TPM** — extends machine_id to be hardware-
  bound (Windows 11 Pro+ only).
- **Server-side rate limiting** — protect `/trial/activate` from automated
  machine_id enumeration.
- **Audit log review** — `audit_log` table in the server records every
  request. Periodic review surfaces fleet anomalies.

## Operational checklist

- [ ] Generate a 32-byte `MASTER_SECRET`. Store in env or `.master_secret`.
- [ ] Generate a 32-byte `LICENSE_SERVER_SECRET`. Store in deployment secrets.
- [ ] Deploy the license server (VPS + systemd, or Docker, or Fly.io).
- [ ] Capture the server pin with `python -m license_client --print-pin URL`.
- [ ] Distribute `DARIO_LICENSE_SERVER` + `DARIO_LICENSE_CERT_PIN` in your
      installer.
- [ ] Buy a code-signing cert (Windows OV ≈ €150/yr, macOS Apple Dev $99/yr).
- [ ] Set up CI to build + sign on every release tag.
- [ ] Rotate `MASTER_SECRET` and `LICENSE_SERVER_SECRET` on a schedule
      (e.g. yearly) — note this invalidates all existing VIP keys.
