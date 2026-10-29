@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Create it with: py -m venv .venv
    exit /b 1
)
cd server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
