@echo off
title Custom AI Desktop Agent Setup
echo ==================================================
echo   Setting up Custom AI Desktop Agent for Windows
echo ==================================================

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.10+ first.
    pause
    exit /b
)

echo [1/3] Creating Virtual Environment...
python -m venv venv
call venv\Scripts\activate.bat

echo [2/3] Installing Python dependencies & Playwright...
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium

echo [3/3] Setup complete! Launching Agent...
python main.py
pause
