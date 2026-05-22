@echo off
REM DARIO Dream Weekly — long-window consolidation (14 days).
REM Schedule: Sundays 04:00 (after daily run)
REM    schtasks /Create /SC WEEKLY /D SUN /TN "DARIO\DreamWeekly" /TR "%USERPROFILE%\.claude\orchestrator\scripts\dream_weekly.bat" /ST 04:00
REM
REM Logs to ~/.claude/orchestrator/dream/cron.log

setlocal
set ORCH=%USERPROFILE%\.claude\orchestrator
set LOG=%ORCH%\dream\cron.log

echo. >> "%LOG%"
echo === DREAM WEEKLY %DATE% %TIME% (window=14d) === >> "%LOG%"

cd /d "%ORCH%"
python -m dream.engine --window 14 >> "%LOG%" 2>&1

if errorlevel 1 (
  echo [FAIL] weekly dream exited with code %errorlevel% >> "%LOG%"
  exit /b %errorlevel%
)

echo [OK] weekly dream completed at %TIME% >> "%LOG%"
endlocal
