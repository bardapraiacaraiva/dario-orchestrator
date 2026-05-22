# Install DARIO Dream as a daily Windows scheduled task.
# Run from PowerShell (admin not required for current user).

$TaskName = "DARIO\DreamDaily"
$ScriptPath = Join-Path $env:USERPROFILE ".claude\orchestrator\scripts\dream_daily.bat"
$StartTime = "03:00"

if (-not (Test-Path $ScriptPath)) {
    Write-Error "Script not found: $ScriptPath"
    exit 1
}

# Remove existing task if present
schtasks /Query /TN $TaskName 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
    schtasks /Delete /TN $TaskName /F | Out-Null
    Write-Host "Removed existing task $TaskName"
}

# Create new daily task at 03:00
$result = schtasks /Create /SC DAILY /TN $TaskName /TR "`"$ScriptPath`"" /ST $StartTime /F
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Scheduled DARIO Dream daily at $StartTime"
    Write-Host "     Inspect: schtasks /Query /TN `"$TaskName`" /V /FO LIST"
    Write-Host "     Run now: schtasks /Run /TN `"$TaskName`""
    Write-Host "     Logs:    $env:USERPROFILE\.claude\orchestrator\dream\cron.log"
} else {
    Write-Error "Failed to create task"
    exit 1
}
