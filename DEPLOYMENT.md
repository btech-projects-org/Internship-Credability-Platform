# INTERNSHIP CREDIBILITY CHECK - DEPLOYMENT GUIDE

## Overview

This document explains how to:
1. **Developers**: Build the standalone `.exe` executable
2. **End Users**: Run the application with zero setup

---

## Architecture: PyInstaller Single Executable

The application is packaged as a **single `.exe` file** that includes:
- Python 3.12 runtime (embedded)
- All dependencies (Flask, ML libraries, etc.)
- Complete backend (Flask API)
- Complete frontend (HTML/CSS/JS)
- All required data files

**No installation, no configuration, no manual setup required.**

---

## For Developers: Building the Executable

### Prerequisites
- **Windows 10/11** (64-bit)
- **Python 3.12+** (download from python.org)
- **~3 GB disk space** for build process

### Step 1: Prepare Dependencies (One-time)

Generate stub models if needed:
```bash
cd backend/models
python generate_stubs.py
cd ../..
```

This creates placeholder trained models for demo purposes.
(In production, replace with actual trained models.)

### Step 2: Run Build Script

```bash
build.bat
```

**What it does:**
1. Checks Python installation
2. Installs PyInstaller and project dependencies
3. Builds `dist/CredibilityCheck.exe`

**Expected output:**
```
========================================
  BUILD SUCCESS
========================================

Output: dist/CredibilityCheck.exe

Next steps:
  1. Test: Run dist\CredibilityCheck.exe
  2. Distribute: Copy dist\CredibilityCheck.exe to end users
```

**Build time:** 2-10 minutes (depends on system speed)

### Step 3: Test the Build

```bash
dist/CredibilityCheck.exe
```

Expected behavior:
- Console window opens showing server startup
- Browser automatically opens to the frontend
- Server runs indefinitely until you press Ctrl+C

### Step 4: Distribute

Copy `dist/CredibilityCheck.exe` to end users via:
- Email
- File sharing (Google Drive, Dropbox, OneDrive)
- USB drive
- Website download

---

## For End Users: Running the Application

### System Requirements
- **Windows 10/11** (64-bit)
- **No Python installation needed**
- **No additional software needed**
- **~500 MB free disk space** (for .exe file)

### To Run

**Option 1: Double-click**
```
Double-click: CredibilityCheck.exe
```

**Option 2: Command line**
```bash
CredibilityCheck.exe
```

### Expected Behavior

1. **Console window opens** with server startup message
2. **Browser automatically opens** to the application
3. **Web interface loads** in your default browser
4. **Use the application** to check internship credibility

### To Stop

Press **Ctrl+C** in the console window, or close the console.

---

## Project Structure

```
internship-credibility-frontend/
├── launcher.py                 # Entry point for executable
├── build.bat                   # Build script (run once)
├── CredibilityCheck.spec       # PyInstaller configuration
├── README.md                   # This file
│
├── backend/
│   ├── app.py                  # Flask application
│   ├── requirements.txt         # Pinned dependencies
│   ├── models/
│   │   ├── generate_stubs.py   # Stub model generator
│   │   ├── saved/              # Pre-trained models (bundled in exe)
│   │   │   ├── random_forest.pkl
│   │   │   └── text_cnn.h5
│   │   ├── random_forest_inference.py
│   │   └── text_cnn_inference.py
│   ├── routes/                 # API endpoints
│   ├── services/               # Core business logic
│   └── preprocessing/          # Data pipelines
│
├── frontend/
│   ├── pages/                  # HTML pages (check, analysis, result, etc.)
│   ├── js/                     # JavaScript logic
│   ├── css/                    # Stylesheets
│   └── assets/                 # Images, videos
│
└── documentation/
    └── project_overview.html   # Full project documentation
```

---

## API Endpoints

The Flask backend runs on **http://localhost:5000** and exposes:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/parse_internship_info` | POST | Extract structured data from raw text |
| `/api/predict` | POST | Analyze credibility (scores + breakdown) |
| `/api/find_company_website` | POST | Lookup official company website (Google CSE) |
| `/api/verify_company` | POST | Verify company indicators |
| `/api/extract_url_features` | POST | Analyze URL for red flags |
| `/health` | GET | Health check |

---

## Configuration

### Environment Variables (Optional)

If you have Google Custom Search API credentials, add to `backend/config/secrets.env`:

```env
GOOGLE_CSE_API_KEY=your_api_key_here
GOOGLE_CSE_CX=your_search_engine_id_here
```

These enable the auto-lookup feature for company websites.

---

## Troubleshooting

### Problem: .exe doesn't run
**Solution:** Ensure you're on Windows 10/11 (64-bit) and have 500 MB free space.

### Problem: Port 5000 already in use
**Solution:** Close other applications using port 5000, or edit `launcher.py` line ~90 to use a different port.

### Problem: Browser doesn't auto-open
**Solution:** Manually open your browser and go to `http://localhost:5000`

### Problem: Antivirus flags the .exe
**Solution:** This is normal for bundled executables. The `.exe` is safe (open-source code). Whitelist it in your antivirus settings.

### Problem: Models not loading (always returns 0.5 score)
**Solution:** This means stub models are in use. For production:
1. Train actual ML models (Random Forest + Text CNN)
2. Save to `backend/models/saved/`
3. Rebuild the executable with `build.bat`

---

## For Production Deployment

### Replace Stub Models

1. Train your actual Random Forest and Text CNN models
2. Save to:
   - `backend/models/saved/random_forest.pkl`
   - `backend/models/saved/text_cnn.h5` + tokenizer
3. Rebuild: `build.bat`
4. Test: Run the new `.exe`
5. Distribute the new `.exe`

### Custom Configuration

Edit `launcher.py` to:
- Change port (line 90)
- Add logging
- Pre-load environment variables
- Auto-start on system boot (Windows Task Scheduler)

### Cloud Deployment

For cloud deployment (AWS, Azure, Heroku):
- Use `backend/app.py` directly
- Create Docker image with `Dockerfile`
- Use `gunicorn` instead of Flask development server
- Set environment variables in cloud console

---

## Development Workflow

For developers modifying the code:

### Test Without Rebuilding

1. Install dependencies (one-time):
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Run Flask directly:
   ```bash
   cd backend
   python app.py
   ```

3. Open frontend: `http://localhost:5000` (or double-click `frontend/pages/index.html`)

4. Make changes to `.py` or `.html` files

5. Test in browser (refresh page for JS/CSS changes)

### Rebuild .exe After Changes

```bash
build.bat
```

This ensures all code changes are included in the executable.

---

## File Manifest (What's Included in .exe)

| Component | Bundled | Location in .exe |
|-----------|---------|------------------|
| Python 3.12 | ✓ | Internal runtime |
| Flask | ✓ | Embedded dependencies |
| scikit-learn | ✓ | Embedded dependencies |
| Transformers | ✓ | Embedded dependencies |
| PyTorch | ✓ | Embedded dependencies |
| Frontend HTML/CSS/JS | ✓ | `frontend/` |
| Backend code | ✓ | `backend/` |
| Models (stub) | ✓ | `backend/models/saved/` |
| Documentation | ✓ | `documentation/` |

---

## License & Support

- **License**: [Your license here]
- **Source Code**: Available at repository root
- **Documentation**: See `documentation/project_overview.html`
- **Support**: [Your support contact here]

---

## Version Info

- **Build Date**: 2025-12-29
- **Python Version**: 3.12
- **Flask Version**: 3.0.0
- **PyInstaller Version**: 6.4.0
- **Target OS**: Windows 10/11 (64-bit)

---

## Summary

### For End Users:
```
1. Download CredibilityCheck.exe
2. Double-click it
3. Done! App runs with zero setup
```

### For Developers:
```
1. Clone repository
2. Run: build.bat
3. Distribute: dist/CredibilityCheck.exe
4. Maintain: Update code, rebuild, redistribute
```

---

**Made with ❤️ for seamless, zero-setup deployment.**
