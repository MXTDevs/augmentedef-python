@echo off
REM Check if Python 3.11 is installed using the py launcher
py -3.11 --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3.11 is required but not found.
    echo Please install Python 3.11 from https://www.python.org/downloads/ and try again.
    pause
    exit /b 1
)

echo Python 3.11 found.

echo Checking for virtual environment...
IF EXIST venv (
    echo Virtual environment found. Activating...
    call venv\Scripts\activate
) ELSE (
    echo Virtual environment not found. Creating one with Python 3.11...
    py -3.11 -m venv venv
    call venv\Scripts\activate
    echo Installing dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
)

echo Launching the app...
python main.py
pause

