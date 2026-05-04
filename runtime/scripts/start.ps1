# DARIO Orchestrator Runtime — Start Script
$ErrorActionPreference = "SilentlyContinue"

# Check if already running
$running = Get-NetTCPConnection -LocalPort 8421 -State Listen 2>$null
if ($running) {
    Write-Host "DARIO Runtime already running on port 8421" -ForegroundColor Yellow
    exit 0
}

# Start in background
$proc = Start-Process -FilePath "C:\dario-orch\.venv\Scripts\python.exe" `
    -ArgumentList "C:\dario-orch\run.py" `
    -WorkingDirectory "C:\dario-orch" `
    -WindowStyle Hidden `
    -PassThru

Write-Host "DARIO Runtime started (PID: $($proc.Id)) on port 8421" -ForegroundColor Green
