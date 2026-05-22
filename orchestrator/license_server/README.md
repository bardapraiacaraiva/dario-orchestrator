# DARIO License Server

Server-side trial enforcement with anti-snapshot rollback detection.
Closes the last bypass gap from the Onda 7 audit.

## Quick start (local dev)

```bash
# 1. Generate a server secret (KEEP THIS SAFE — anyone with it can forge tokens)
export LICENSE_SERVER_SECRET=$(python -c 'import secrets; print(secrets.token_hex(32))')

# 2. Run the server
cd ~/.claude/orchestrator
python -m license_server.app --host 0.0.0.0 --port 8430

# 3. On every DARIO install, point clients at it
export DARIO_LICENSE_SERVER=http://localhost:8430

# 4. Initialise trial (will now bind to the server)
python license_manager.py --init-trial
```

## Endpoints

| Method | Path | Body | Returns |
|---|---|---|---|
| GET  | `/health` | — | `{status: "ok"}` |
| POST | `/trial/activate` | `{machine_id}` | `TrialResponse` (idempotent) |
| POST | `/trial/validate` | `{machine_id, token, client_first_init_at?}` | `ValidationResponse` |
| POST | `/vip/activate` | `{machine_id, vip_key}` | `TrialResponse` (tier upgraded) |

`TrialResponse` includes `token` (HMAC-signed) which the client stores in
`license.json` and replays on every subsequent `validate` call.

## Anti-snapshot rollback

`/trial/validate` accepts an optional `client_first_init_at`. The server
compares this to its own immutable `first_init_at` for the machine_id:

- Within ±1 hour (configurable via `LICENSE_ROLLBACK_TOLERANCE_HOURS`) — pass.
- Drift larger than tolerance — `rollback_detected=True`, `valid=false`.

This catches:
- VM snapshot restored to before the original trial activation
- Local system clock manipulated to "rewind" the trial
- Any tampering with the local `activated_at` field

## Production deployment

### Option A — VPS / bare metal

```bash
# 1. Provision the host with python 3.13 + uv
# 2. Clone the repo somewhere (e.g. /opt/dario-license-server)
# 3. Create a systemd unit:
cat > /etc/systemd/system/dario-license.service <<'EOF'
[Unit]
Description=DARIO License Server
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/dario-license-server
Environment=LICENSE_SERVER_SECRET=PASTE_64_HEX_CHARS_HERE
Environment=LICENSE_SERVER_DB=/var/lib/dario/license.db
ExecStart=/usr/bin/python3 -m license_server.app --host 0.0.0.0 --port 8430
Restart=on-failure
User=dario

[Install]
WantedBy=multi-user.target
EOF
systemctl enable --now dario-license
```

### Option B — Docker

```dockerfile
# Dockerfile (place inside license_server/)
FROM python:3.13-slim
WORKDIR /app
COPY . /app/orchestrator
WORKDIR /app/orchestrator
RUN pip install --no-cache-dir fastapi uvicorn pydantic
EXPOSE 8430
ENV LICENSE_SERVER_DB=/data/license.db
VOLUME /data
CMD ["python", "-m", "license_server.app", "--host", "0.0.0.0", "--port", "8430"]
```

```bash
docker build -t dario-license -f license_server/Dockerfile .
docker run -d --name dario-license \
    -p 8430:8430 \
    -e LICENSE_SERVER_SECRET=$(openssl rand -hex 32) \
    -v dario-license-data:/data \
    dario-license
```

### Option C — Cloud (Fly.io / Railway / Render)

Same Dockerfile; deploy via your platform's UI or CLI. Make sure:

1. `LICENSE_SERVER_SECRET` is set in the platform's secret manager.
2. The SQLite DB volume is persistent (use the platform's persistent disk).
3. Front the service with HTTPS — clients send tokens that act as bearer
   credentials, so plaintext HTTP would be a leak.

## Configuration

| Env var | Default | Purpose |
|---|---|---|
| `LICENSE_SERVER_SECRET` | — (required, ≥32 chars) | HMAC signing key for tokens |
| `LICENSE_SERVER_DB` | `~/.dario-license-server.db` | SQLite path |
| `LICENSE_TRIAL_DAYS` | `7` | Trial duration |
| `LICENSE_ROLLBACK_TOLERANCE_HOURS` | `1` | Snapshot detection tolerance |

## Backup + restore

The single SQLite file at `LICENSE_SERVER_DB` is the entire source of truth.

```bash
# Backup
sqlite3 /var/lib/dario/license.db ".backup '/backups/license-$(date +%F).db'"

# Restore
cp /backups/license-2026-05-22.db /var/lib/dario/license.db
systemctl restart dario-license
```

For higher scale (>10k machines/day) swap SQLite for Postgres — the schema
in `db.py` is portable, you only have to change the connect string.

## Auditing

Every activation, validation, rollback, and upgrade writes to the
`audit_log` table with timestamps. Query it:

```bash
sqlite3 /var/lib/dario/license.db \
    "SELECT server_ts, machine_id, event, payload
     FROM audit_log
     WHERE machine_id = 'TARGET_MACHINE_ID'
     ORDER BY server_ts DESC LIMIT 50;"
```

## Threat model

| Attack | Defense | Effectiveness |
|---|---|---|
| Delete `license.json` + `.trial_fingerprint` | Server-side record persists | ✅ Hard bypass |
| Tamper local `activated_at` to past | Token signature mismatch | ✅ Detected |
| Tamper local `activated_at` to future | Rollback detection via `client_first_init_at` mismatch | ✅ Detected |
| VM snapshot rollback | Server's monotonic `last_seen_at` + heartbeat count | ✅ Detected on next /validate |
| Change `MachineGuid` (Windows registry) | Looks like new machine → new trial | ⚠️ Possible, requires admin |
| OS reinstall | Looks like new machine → new trial | ⚠️ Legitimate but costly |
| Steal `LICENSE_SERVER_SECRET` | Forge tokens for any machine_id | ⚠️ Game over — rotate secret |
| MITM on plaintext HTTP | Steal/replay tokens | ⚠️ Use HTTPS in production |
| Server outage | Client falls back to offline 3-layer (Onda 7) | ✅ Degrades gracefully |

## See also

- `license_manager.py` — client integration (init_trial + check_license)
- `license_client.py` — thin HTTP client
- `tests/test_license_server.py` — 17 end-to-end tests
- `memory/license_3layer_2026_05_22.md` — Onda 7 local 3-layer defense
