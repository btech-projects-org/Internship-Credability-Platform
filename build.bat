@echo off
REM ========================
REM BUILD SCRIPT FOR PYINSTALLER
REM ========================
REM This script builds a standalone .exe from the project
REM Run this ONCE to create CredibilityCheck.exe
REM Then distribute the .exe to end users

echo.
echo ========================================
echo  CREDIBILITY CHECK - BUILD PROCESS
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.12+ from python.org
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Install build dependencies
echo [INFO] Installing build dependencies...
pip install --upgrade pip setuptools wheel pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install build tools
    pause
    exit /b 1
)

echo [OK] Build dependencies installed
echo.

REM Install project dependencies
echo [INFO] Installing project dependencies from requirements.txt...
echo This may take 2-5 minutes (first time only)...
echo.
pip install -r backend/requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    echo Check backend/requirements.txt for issues
    pause
    exit /b 1
)

echo.
echo [OK] Dependencies installed
echo.

REM Run PyInstaller
echo [INFO] Building standalone .exe ...
echo This will take 2-10 minutes depending on your system...
echo.

pyinstaller CredibilityCheck.spec --noconfirm

if errorlevel 1 (
    echo [ERROR] PyInstaller build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo  BUILD SUCCESS
echo ========================================
echo.
echo Output: dist/CredibilityCheck.exe
echo.
echo Next steps:
echo   1. Test: Run dist\CredibilityCheck.exe
echo   2. Distribute: Copy dist\CredibilityCheck.exe to end users
echo   3. Users run: Double-click CredibilityCheck.exe (no setup needed!)
echo.
pause
