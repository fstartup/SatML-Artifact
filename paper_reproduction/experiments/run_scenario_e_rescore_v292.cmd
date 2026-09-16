@echo off
setlocal
python experiments\src\scenario_e\rescore_real_model.py --input "%~1"
endlocal
