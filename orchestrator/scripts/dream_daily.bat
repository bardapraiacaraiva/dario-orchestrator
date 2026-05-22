@echo off
REM DARIO Dream — daily consolidation cron.
REM Schedule via Task Scheduler: daily 03:00 AM
REM    schtasks /Create /SC DAILY /TN "DARIO\DreamDaily" /TR "%USERPROFILE%\.claude\orchestrator\scripts\dream_daily.bat" /ST 03:00
REM
REM Logs to ~/.claude/orchestrator/dream/cron.log

setlocal
set ORCH=%USERPROFILE%\.claude\orchestrator
set LOG=%ORCH%\dream\cron.log

echo. >> "%LOG%"
echo === DREAM RUN %DATE% %TIME% === >> "%LOG%"

cd /d "%ORCH%"
python -m dream.engine --window 7 >> "%LOG%" 2>&1

if errorlevel 1 (
  echo [FAIL] dream exited with code %errorlevel% >> "%LOG%"
  exit /b %errorlevel%
)

echo [OK] dream completed at %TIME% >> "%LOG%"
endlocal
