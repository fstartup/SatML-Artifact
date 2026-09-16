@echo off
setlocal
set PYTHONPATH=src
python -m scenario_e.real_model_runner --provider foundry_project --model gpt-5-nano --case E8_model_bounded_restart
python -m scenario_e.real_model_runner --provider foundry_project --model gpt-5-nano --case E9_model_unsafe_privilege
python -m scenario_e.real_model_runner --provider foundry_project --model gpt-5-nano --case E10_model_global_blast_radius
python -m scenario_e.real_model_runner --provider foundry_project --model gpt-5-nano --case E11_model_evidence_loss
python -m scenario_e.real_model_runner --provider foundry_anthropic --model claude-haiku-4-5 --case E8_model_bounded_restart
python -m scenario_e.real_model_runner --provider foundry_anthropic --model claude-haiku-4-5 --case E9_model_unsafe_privilege
python -m scenario_e.real_model_runner --provider foundry_anthropic --model claude-haiku-4-5 --case E10_model_global_blast_radius
python -m scenario_e.real_model_runner --provider foundry_anthropic --model claude-haiku-4-5 --case E11_model_evidence_loss
endlocal
