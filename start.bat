@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo Run setup.bat first.
  pause
  exit /b 1
)
if not exist node_modules\vite\bin\vite.js (
  echo Run setup.bat first.
  pause
  exit /b 1
)
start "DevTool Finder API" /D "%~dp0" cmd /k "call .venv\Scripts\activate.bat && python -m backend"
start "DevTool Finder Web" /D "%~dp0" cmd /k "npm run dev"
timeout /t 3 /nobreak >nul
start http://127.0.0.1:5173
