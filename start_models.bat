@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe py -3.12 -m venv .venv
if errorlevel 1 goto fail
.venv\Scripts\python.exe -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 goto fail
.venv\Scripts\python.exe -m pip install -r requirements-models.txt
if errorlevel 1 goto fail
.venv\Scripts\python.exe scripts\download_models.py
if errorlevel 1 goto fail
set LLM_BACKEND=transformers
set SEMANTIC_SEARCH=1
start "" http://127.0.0.1:8000
.venv\Scripts\python.exe app.py
exit /b
:fail
echo Setup failed. Confirm Python 3.12 is installed and internet access is available.
pause
exit /b 1
