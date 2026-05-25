# Install DARIO Weekly Backup as a Windows Scheduled Task.
# Runs every Sunday at 03:30 (after dream cron at 03:00).
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File backup_install_cron.ps1
#
# Uninstall:
#   Unregister-ScheduledTask -TaskName "DARIO Weekly Backup" -Confirm:$false

$TaskName = "DARIO Weekly Backup"
$ScriptPath = "$env:USERPROFILE\.claude\orchestrator\scripts\backup_weekly.sh"
$LogPath = "$env:USERPROFILE\.claude-backups\backup_cron.log"

# Find bash.exe (Git Bash)
$BashPath = $null
$candidates = @(
    "C:\Program Files\Git\bin\bash.exe",
    "C:\Program Files\Git\usr\bin\bash.exe",
    "$env:ProgramFiles\Git\bin\bash.exe"
)
foreach ($c in $candidates) {
    if (Test-Path $c) { $BashPath = $c; break }
}
if (-not $BashPath) {
    Write-Error "bash.exe not found. Install Git for Windows or pass -BashPath."
    exit 1
}

Write-Host "Installing scheduled task '$TaskName'..."
Write-Host "  bash: $BashPath"
Write-Host "  script: $ScriptPath"
Write-Host "  log: $LogPath"

if (-not (Test-Path "$env:USERPROFILE\.claude-backups")) {
    New-Item -ItemType Directory -Path "$env:USERPROFILE\.claude-backups" -Force | Out-Null
}

# Remove existing task if present
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

$action = New-ScheduledTaskAction `
    -Execute $BashPath `
    -Argument "-c `"'$ScriptPath' >> '$LogPath' 2>&1`""

$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 3:30am

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -DontStopOnIdleEnd `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30) `
    -RestartCount 1 `
    -RestartInterval (New-TimeSpan -Minutes 5)

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Weekly automated backup of DARIO orchestrator (Risk recommendation #5, 2026-05-25)" `
    -User $env:USERNAME

Write-Host ""
Write-Host "Installed successfully. Next run: Sunday 03:30."
Write-Host ""
Write-Host "Manual trigger (test): Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "Check log: Get-Content '$LogPath' -Tail 50"
Write-Host "Uninstall: Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false"
