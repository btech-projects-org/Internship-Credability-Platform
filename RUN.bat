@echo off
REM ========================
REM SETUP AND RUN WRAPPER
REM ========================
REM Windows batch wrapper for setup_and_run.py
REM User double-clicks this file to start the application

echo.
echo Checking Python installation...
python --version >nul 2>&1

if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Solution: Install Python 3.12+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
echo.
echo Starting automated setup and backend...
echo.

python "%~dp0setup_and_run.py"

if errorlevel 1 (
    echo.
    echo [ERROR] Setup or backend startup failed
    echo Check the error message above
    echo.
    pause
    exit /b 1
)

pause
