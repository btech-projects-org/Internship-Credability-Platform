@echo off
REM ========================
REM QUICK START GUIDE
REM ========================
REM Run this batch file to display setup instructions

cls
color 0A

echo.
echo ========================================
echo  INTERNSHIP CREDIBILITY CHECK
echo  Quick Start Guide
echo ========================================
echo.

echo [1] FOR END USERS (Just want to run it)
echo ───────────────────────────────────────
echo.
echo     Download: CredibilityCheck.exe
echo     Run:      Double-click it
echo     Done!     App starts automatically
echo.
echo.

echo [2] FOR DEVELOPERS (Want to build or modify)
echo ───────────────────────────────────────────
echo.
echo     OPTION A: Build Standalone .exe
echo     ─────────────────────────────
echo       1. Run: build.bat
echo       2. Wait 5-10 minutes
echo       3. Output: dist\CredibilityCheck.exe
echo       4. Test: Run dist\CredibilityCheck.exe
echo.
echo     OPTION B: Develop Locally
echo     ────────────────────────
echo       1. Install deps:  pip install -r backend\requirements.txt
echo       2. Start server:  cd backend ^&^& python app.py
echo       3. Open browser:  http://localhost:5000
echo       4. Edit code and refresh browser
echo.
echo.

echo [3] DOCUMENTATION
echo ──────────────────
echo.
echo     README.md                  - Overview ^& quick reference
echo     DEPLOYMENT.md              - Complete deployment guide
echo     documentation/project_overview.html - Full architecture
echo.
echo ========================================
echo.

pause
