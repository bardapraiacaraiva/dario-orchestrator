@echo off
REM DARIO Auto-Capture — Hourly wrapper for Windows Task Scheduler.
REM Runs the auto_capture_obsidian.py with safe limits (max 5 new per hour, ~$0.05/h max).
REM Logs to ~/.claude/orchestrator/logs/auto_capture.log

set ORCH=%USERPROFILE%\.claude\orchestrator
set LOG=%ORCH%\logs\auto_capture.log
set PY=C:\Python313\python.exe

REM Ensure log dir exists
if not exist "%ORCH%\logs" mkdir "%ORCH%\logs"

REM Append timestamp + run
echo. >> "%LOG%"
echo === %DATE% %TIME% === >> "%LOG%"
cd /d "%ORCH%"
"%PY%" scripts\auto_capture_obsidian.py --limit 5 >> "%LOG%" 2>&1

REM Exit cleanly
exit /b 0
