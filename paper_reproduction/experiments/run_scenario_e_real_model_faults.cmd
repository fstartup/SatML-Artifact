@echo off
REM First-wave Scenario E real-model fault injection: F3 and F8 only.
REM Run one command at a time. Synthetic environment only.
REM Maximum first-wave budget: 8 model calls (2 turns x 2 faults x 2 models).
python -m scenario_e.real_model_fault_runner --provider foundry_project --model gpt-5-nano --fault F3
python -m scenario_e.real_model_fault_runner --provider foundry_project --model gpt-5-nano --fault F8
python -m scenario_e.real_model_fault_runner --provider foundry_anthropic --model claude-haiku-4-5 --fault F3
python -m scenario_e.real_model_fault_runner --provider foundry_anthropic --model claude-haiku-4-5 --fault F8
