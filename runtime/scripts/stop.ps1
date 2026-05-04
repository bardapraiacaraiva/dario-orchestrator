# DARIO Orchestrator Runtime — Stop Script
$ErrorActionPreference = "SilentlyContinue"

$conn = Get-NetTCPConnection -LocalPort 8421 -State Listen 2>$null
if ($conn) {
    $pid = $conn.OwningProcess
    Stop-Process -Id $pid -Force
    Write-Host "DARIO Runtime stopped (PID: $pid)" -ForegroundColor Yellow
} else {
    Write-Host "DARIO Runtime not running" -ForegroundColor Gray
}
