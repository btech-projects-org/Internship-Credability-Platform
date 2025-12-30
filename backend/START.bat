@echo off
REM ===================================================
REM STARTUP SCRIPT FOR WINDOWS
REM Automatically installs dependencies and starts API
REM ===================================================

setlocal enabledelayedexpansion

echo.
echo ===================================================
echo INTERNSHIP CREDIBILITY CHECKER - BACKEND
echo ===================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.12+ from https://www.python.org
    pause
    exit /b 1
)

echo Python found!
echo.

REM Run the Flask app with auto-install
echo Starting backend server with auto-dependency installation...
echo.

python run.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start server
    echo.
    echo Try manual installation:
    echo   pip install -r requirement1.txt
    echo   python app.py
    pause
    exit /b 1
)

pause
