#!/bin/bash
# DARIO Orchestrator — VPS Deploy Pack
# =====================================
# Deploys the DARIO runtime to a VPS with HTTPS, systemd, and nginx.
#
# Usage:
#   bash deploy_pack.sh --server user@ip --domain dario.yourdomain.com
#   bash deploy_pack.sh --local           # Local setup only (no SSH)
#   bash deploy_pack.sh --check           # Check if deployment is healthy
#
# Prerequisites on VPS:
#   - Ubuntu 22.04+ or Debian 12+
#   - Python 3.11+
#   - nginx
#   - certbot

set -euo pipefail

ORCH_DIR="$HOME/.claude/orchestrator"
RUNTIME_PORT=8422
DOMAIN=""
SERVER=""
LOCAL=false
CHECK_ONLY=false

usage() {
    echo "Usage: $0 [--server user@ip] [--domain domain.com] [--local] [--check]"
    exit 1
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --server) SERVER="$2"; shift 2 ;;
        --domain) DOMAIN="$2"; shift 2 ;;
        --local) LOCAL=true; shift ;;
        --check) CHECK_ONLY=true; shift ;;
        *) usage ;;
    esac
done

# === CHECK MODE ===
if $CHECK_ONLY; then
    echo "=== DARIO Deploy Health Check ==="
    if curl -sf http://localhost:$RUNTIME_PORT/health > /dev/null 2>&1; then
        HEALTH=$(curl -s http://localhost:$RUNTIME_PORT/health)
        echo "  Runtime: LIVE on port $RUNTIME_PORT"
        echo "  Health: $HEALTH"
    else
        echo "  Runtime: DOWN"
    fi
    if systemctl is-active --quiet dario-runtime 2>/dev/null; then
        echo "  Service: ACTIVE"
    else
        echo "  Service: NOT INSTALLED or INACTIVE"
    fi
    if command -v nginx &> /dev/null && nginx -t 2>/dev/null; then
        echo "  Nginx: OK"
    fi
    exit 0
fi

echo "=== DARIO Orchestrator Deploy Pack ==="
echo "  Runtime port: $RUNTIME_PORT"
echo "  Domain: ${DOMAIN:-localhost}"
echo "  Mode: $(if $LOCAL; then echo 'local'; else echo 'remote'; fi)"

# === GENERATE SYSTEMD SERVICE ===
cat > /tmp/dario-runtime.service << EOF
[Unit]
Description=DARIO Orchestrator Runtime
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$ORCH_DIR
ExecStart=$(which python3 || which python) $ORCH_DIR/runtime.py --port $RUNTIME_PORT --host 127.0.0.1
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

echo "  Generated systemd service"

# === GENERATE NGINX CONFIG ===
if [ -n "$DOMAIN" ]; then
cat > /tmp/dario-nginx.conf << EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:$RUNTIME_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 120s;
        proxy_connect_timeout 10s;
    }

    location /events {
        proxy_pass http://127.0.0.1:$RUNTIME_PORT/events;
        proxy_set_header Connection '';
        proxy_http_version 1.1;
        chunked_transfer_encoding off;
        proxy_buffering off;
        proxy_cache off;
    }
}
EOF
echo "  Generated nginx config for $DOMAIN"
fi

# === LOCAL INSTALL ===
if $LOCAL; then
    echo ""
    echo "=== Local Install ==="
    sudo cp /tmp/dario-runtime.service /etc/systemd/system/ 2>/dev/null || echo "  [skip] systemd (no sudo)"
    sudo systemctl daemon-reload 2>/dev/null || true
    sudo systemctl enable dario-runtime 2>/dev/null || true
    sudo systemctl start dario-runtime 2>/dev/null || true

    if [ -n "$DOMAIN" ]; then
        sudo cp /tmp/dario-nginx.conf /etc/nginx/sites-available/dario 2>/dev/null || echo "  [skip] nginx (no sudo)"
        sudo ln -sf /etc/nginx/sites-available/dario /etc/nginx/sites-enabled/ 2>/dev/null || true
        sudo nginx -t 2>/dev/null && sudo systemctl reload nginx 2>/dev/null || true
        echo "  Run: sudo certbot --nginx -d $DOMAIN"
    fi

    echo ""
    echo "=== Done ==="
    echo "  Service: systemctl status dario-runtime"
    echo "  Health: curl http://localhost:$RUNTIME_PORT/health"
    if [ -n "$DOMAIN" ]; then
        echo "  URL: https://$DOMAIN"
    fi
    exit 0
fi

# === REMOTE DEPLOY ===
if [ -z "$SERVER" ]; then
    echo "ERROR: --server required for remote deploy"
    usage
fi

echo ""
echo "=== Remote Deploy to $SERVER ==="

# Create tarball of orchestrator
echo "  Packing orchestrator..."
TARBALL="/tmp/dario-deploy.tar.gz"
tar -czf "$TARBALL" \
    -C "$HOME/.claude" \
    orchestrator/ \
    --exclude='orchestrator/__pycache__' \
    --exclude='orchestrator/.pytest_cache' \
    --exclude='orchestrator/orchestrator.db' \
    --exclude='orchestrator/evolution/checkpoints' \
    --exclude='orchestrator/evolution/journal'

echo "  Tarball: $(du -h $TARBALL | cut -f1)"

# Upload
echo "  Uploading to $SERVER..."
scp "$TARBALL" /tmp/dario-runtime.service "$SERVER:/tmp/"
if [ -n "$DOMAIN" ]; then
    scp /tmp/dario-nginx.conf "$SERVER:/tmp/"
fi

# Install remotely
echo "  Installing..."
ssh "$SERVER" << 'REMOTE_SCRIPT'
set -e
mkdir -p ~/.claude
cd ~/.claude
tar -xzf /tmp/dario-deploy.tar.gz

# Python deps
pip install fastapi uvicorn pyyaml --quiet 2>/dev/null || pip3 install fastapi uvicorn pyyaml --quiet

# Systemd
sudo cp /tmp/dario-runtime.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dario-runtime
sudo systemctl restart dario-runtime

# Nginx (if config exists)
if [ -f /tmp/dario-nginx.conf ]; then
    sudo cp /tmp/dario-nginx.conf /etc/nginx/sites-available/dario
    sudo ln -sf /etc/nginx/sites-available/dario /etc/nginx/sites-enabled/
    sudo nginx -t && sudo systemctl reload nginx
fi

echo "DEPLOY COMPLETE"
REMOTE_SCRIPT

echo ""
echo "=== Deploy Complete ==="
echo "  Health: ssh $SERVER 'curl -s http://localhost:$RUNTIME_PORT/health'"
if [ -n "$DOMAIN" ]; then
    echo "  HTTPS: ssh $SERVER 'sudo certbot --nginx -d $DOMAIN'"
    echo "  URL: https://$DOMAIN"
fi

# Cleanup
rm -f "$TARBALL" /tmp/dario-runtime.service /tmp/dario-nginx.conf
