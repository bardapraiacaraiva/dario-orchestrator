$TaskName = "DARIO\DreamWeekly"
$ScriptPath = Join-Path $env:USERPROFILE ".claude\orchestrator\scripts\dream_weekly.bat"

schtasks /Query /TN $TaskName 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
    schtasks /Delete /TN $TaskName /F | Out-Null
}

schtasks /Create /SC WEEKLY /D SUN /TN $TaskName /TR "`"$ScriptPath`"" /ST 04:00 /F
