# QUICK START GUIDE - Auto-Installation Setup

## Overview
The project is now configured to automatically install all required dependencies when you first run it. No virtual environment setup needed!

---

## Quick Start (Windows)

### Option 1: Double-Click (Easiest)
1. Navigate to `backend/` folder
2. Double-click **START.bat**
3. Wait for dependencies to install (first run only)
4. Server will start at http://localhost:5000

### Option 2: Command Line
```cmd
cd backend
python run.py
```

---

## Quick Start (Linux/Mac)

### Option 1: Shell Script
```bash
cd backend
bash START.sh
```

### Option 2: Command Line
```bash
cd backend
python3 run.py
```

---

## What Happens on First Run

1. **Auto-Install Triggers** → Detects missing packages
2. **Installs Dependencies** → Runs `pip install -r requirement1.txt`
3. **Verifies Installation** → Checks critical imports
4. **Starts Server** → Flask API runs on http://localhost:5000

All automatic - no user action needed!

---

## Files Created for Auto-Installation

| File | Purpose |
|------|---------|
| **auto_install.py** | Automatic dependency checker & installer |
| **run.py** | Python startup script with auto-install |
| **START.bat** | Windows batch file (double-click to run) |
| **START.sh** | Linux/Mac shell script |
| **app.py** | Modified to call auto_install on startup |
| **requirement1.txt** | Package list for pip install |

---

## First-Time Setup (from Fresh GitHub Download)

### Windows
```
1. Download/Clone project
2. Open CMD/PowerShell
3. cd backend
4. python run.py
   (or double-click START.bat)
5. Wait for install... (may take 5-10 minutes)
6. Server runs at http://localhost:5000
```

### Linux/Mac
```
1. Download/Clone project
2. Open Terminal
3. cd backend
4. bash START.sh
   (or python3 run.py)
5. Wait for install... (may take 5-10 minutes)
6. Server runs at http://localhost:5000
```

---

## Manual Installation (If Needed)

If auto-install fails for any reason:

```cmd
cd backend
pip install -r requirement1.txt
python app.py
```

---

## All 17 Packages Auto-Installed

```
Flask==3.0.0
flask-cors==4.0.0
Werkzeug==3.0.1
python-dotenv==1.0.0
numpy==1.26.2
pandas==2.1.4
scikit-learn==1.3.2
joblib==1.3.2
transformers==4.36.2
huggingface-hub==0.20.1
torch==2.2.0
nltk==3.8.1
requests==2.31.0
tldextract==5.1.1
url-normalize==1.4.3
beautifulsoup4==4.12.2
lxml==4.9.4
```

---

## Verify Installation

```cmd
# Check if server is running
curl http://localhost:5000/health

# Expected response:
# {"service":"Internship Credibility API","status":"healthy"}
```

---

## Troubleshooting

### "Python not found"
- Install Python 3.12+ from https://www.python.org
- Make sure to check "Add Python to PATH" during installation

### "Permission denied" (Linux/Mac)
```bash
chmod +x backend/START.sh
bash backend/START.sh
```

### "Pip not found"
```bash
python -m pip install --upgrade pip
python run.py
```

### Manual Fallback
If all else fails, manually install and run:
```cmd
cd backend
pip install -r requirement1.txt
python app.py
```

---

## Features

✓ **Auto-Install** - No virtual environment needed  
✓ **Zero Setup** - Download and run  
✓ **Cross-Platform** - Works on Windows, Linux, Mac  
✓ **Error Handling** - Graceful fallback to manual install  
✓ **Progress Feedback** - Shows installation progress  

---

**Ready to use! Just run START.bat (Windows) or bash START.sh (Linux/Mac)**

Generated: December 30, 2025
