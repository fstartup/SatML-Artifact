@echo off
setlocal
cd /d "%~dp0"
set PYTHONPATH=src
python -m scenario_e.runner_e --case E1_bounded_restart
if errorlevel 1 exit /b 1
python -m scenario_e.runner_e --case E2_blast_radius
if errorlevel 1 exit /b 1
python -m scenario_e.runner_e --case E3_evidence_insufficient
if errorlevel 1 exit /b 1
python -m scenario_e.runner_e --case E4_observability_loss
if errorlevel 1 exit /b 1
python -m scenario_e.runner_e --case E5_recovery_failure
if errorlevel 1 exit /b 1
python -m scenario_e.runner_e --case E6_iam_prohibited
if errorlevel 1 exit /b 1
python -m scenario_e.runner_e --case E7_global_routing
if errorlevel 1 exit /b 1
echo SCENARIO E DETERMINISTIC CASES PASSED.
endlocal
