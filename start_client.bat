@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Create it with: py -m venv .venv
    exit /b 1
)
python -m client.main
