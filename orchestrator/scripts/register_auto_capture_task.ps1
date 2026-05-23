# DARIO Auto-Capture — register hourly Windows Scheduled Task.
# Run once to install. Re-run to update.

$TaskName = "DARIO-AutoCapture"
$BatchFile = "$env:USERPROFILE\.claude\orchestrator\scripts\auto_capture_hourly.bat"

# Delete existing task if present
$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Removing existing task: $TaskName"
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Define action (run the batch file)
$action = New-ScheduledTaskAction -Execute $BatchFile

# Trigger: hourly, starting 5 min from now
$startTime = (Get-Date).AddMinutes(5)
$trigger = New-ScheduledTaskTrigger -Once -At $startTime `
    -RepetitionInterval (New-TimeSpan -Hours 1)

# Settings: run whether user logged on, don't stop if on battery, etc.
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5)

# Register the task
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "DARIO auto-capture: scan Obsidian Outputs/ folder hourly, score new deliverables via score_real_output.py (limit 5/run, max 5 cents/run). Logs to ~/.claude/orchestrator/logs/auto_capture.log"

Write-Host ""
Write-Host "OK -- Task registered:"
Write-Host "  Name:     $TaskName"
Write-Host "  Trigger:  hourly starting $startTime"
Write-Host "  Action:   $BatchFile"
Write-Host "  Log:      $env:USERPROFILE\.claude\orchestrator\logs\auto_capture.log"
Write-Host ""
Write-Host "Verify with: schtasks /Query /TN $TaskName /FO LIST /V"
Write-Host "Force run now: schtasks /Run /TN $TaskName"
Write-Host "Delete later: schtasks /Delete /TN $TaskName /F"
