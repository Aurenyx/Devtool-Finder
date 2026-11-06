@echo off
setlocal
cd /d "%~dp0"
if not exist .tmp mkdir .tmp
set "TEMP=%CD%\.tmp"
set "TMP=%CD%\.tmp"
set "PYTHONUTF8=1"
if not exist .venv\Scripts\python.exe python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
if not exist node_modules\vite\bin\vite.js npm install
echo.
echo Setup complete. Run start.bat to launch DevTool Finder.
pause
