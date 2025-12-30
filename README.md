# Internship Credibility Checker

**Automated AI/ML system to verify internship offer authenticity and assess credibility**

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.12.3-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements & Dependencies](#requirements--dependencies)
- [Installation & Setup](#installation--setup)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

USE Python 3.11  version

### Windows (Easiest)
```bash
# 1. Navigate to backend
cd backend

# 2. Double-click START.bat (or run in terminal)
python run.py

# 3. Open browser
http://localhost:5000
```

### Linux/Mac
```bash
# 1. Navigate to backend
cd backend

# 2. Run startup script
bash START.sh

# 3. Open browser
http://localhost:5000
```

### Manual Installation
```bash
# 1. Install dependencies
cd backend
pip install -r requirement1.txt

# 2. Run Flask app
python app.py

# 3. Open browser
http://localhost:5000
```

**⏱️ First run auto-installs all dependencies (5-10 minutes)**

---

## ✨ Features

- ✅ **Parse Internship Details** — Extract company, position, salary, duration from raw text
- ✅ **Credibility Analysis** — AI-powered scoring (0-100%)
- ✅ **Red Flag Detection** — Detect fraud indicators (fake salary, domain, payment requests)
- ✅ **Company Verification** — Auto-lookup company legitimacy via web search
- ✅ **Sentiment Analysis** — Analyze job description tone using DistilBERT
- ✅ **URL Analysis** — Check domain age, registrar, SSL certificate patterns
- ✅ **Offer Quality Scoring** — Evaluate completeness (responsibilities, requirements, benefits)
- ✅ **Email Domain Matching** — Verify email domain consistency with company website
- ✅ **Zero-Setup Deploy** — Run directly from GitHub, auto-installs all packages
- ✅ **REST API** — Integrate with other applications

---

## 📁 Project Structure

```
internship-credibility-frontend/
│
├── backend/                           # Flask REST API
│   ├── app.py                        # Main Flask application
│   ├── auto_install.py               # Auto-dependency installer
│   ├── run.py                        # Startup script
│   ├── START.bat                     # Windows startup (double-click)
│   ├── START.sh                      # Linux/Mac startup script
│   ├── requirement1.txt              # Package list (pip-compatible)
│   ├── QUICK_START.md                # Setup instructions
│   │
│   ├── routes/                       # API endpoints
│   │   ├── credibility_routes.py    # /api/predict, /api/parse
│   │   └── sentiment_routes.py      # /api/sentiment
│   │
│   ├── services/                     # Core business logic
│   │   ├── credibility_engine.py    # Main scoring logic
│   │   ├── sentiment_analyzer.py    # DistilBERT sentiment
│   │   ├── company_verifier.py      # Company legitimacy check
│   │   ├── info_parser.py           # Parse raw internship text
│   │   ├── url_feature_extractor.py # Domain analysis
│   │   └── company_search.py        # Web search for company
│   │
│   ├── models/                       # ML models
│   │   ├── random_forest_inference.py # RandomForest predictor
│   │   ├── text_cnn_inference.py    # Text CNN model
│   │   └── generate_stubs.py        # Model generation
│   │
│   ├── preprocessing/                # Data preprocessing
│   │   ├── text_cleaner.py          # Text normalization
│   │   ├── feature_scaler.py        # Feature scaling
│   │   └── tokenizer.py             # Text tokenization
│   │
│   └── config/                       # Configuration
│       └── secrets.env               # Environment variables
│
├── frontend/                          # Web UI
│   ├── index.html                    # Home page
│   ├── pages/                        # Page templates
│   │   ├── check.html               # Credibility checker
│   │   ├── result.html              # Results display
│   │   ├── analysis.html            # Analysis page
│   │   ├── about.html               # About page
│   │   └── contact.html             # Contact page
│   │
│   ├── css/                          # Stylesheets
│   │   ├── main.css                 # Main styles
│   │   ├── animations.css           # Animations
│   │   └── components.css           # Component styles
│   │
│   ├── js/                           # JavaScript
│   │   ├── analysis/                # Analysis scripts
│   │   ├── core/                    # Core utilities
│   │   ├── utils/                   # Utility functions
│   │   └── config/                  # Configuration
│   │
│   ├── assets/                       # Images, videos
│   └── scripts/                      # Setup scripts
│
├── api/                              # Vercel serverless
│   └── index.py                     # WSGI handler
│
├── documentation/                    # Project docs
│   └── project_overview.html        # Full architecture
│
├── README.md                         # This file
├── DEPLOYMENT.md                     # Deployment guide
├── REQUIREMENTS_VERIFICATION.md      # Package verification
├── DEPENDENCIES_ANALYSIS.md          # Complete dependency docs
├── QUICK_REFERENCE.txt               # Quick lookup
└── .gitignore                        # Git ignore rules

```

---

## 📦 Requirements & Dependencies

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **Python** | 3.10 | 3.12.3 |
| **OS** | Windows 10, Linux, macOS | Windows 11, Ubuntu 22+, macOS 13+ |
| **Disk Space** | 2 GB | 5 GB |
| **RAM** | 4 GB | 8 GB |
| **Internet** | Optional* | For company lookup feature |

*Optional: Only needed for company verification via web search

### All 17 Required Packages

| Package | Version | Purpose |
|---------|---------|---------|
| **Flask** | 3.0.0 | REST API framework |
| **flask-cors** | 4.0.0 | Cross-origin requests |
| **Werkzeug** | 3.0.1 | WSGI utilities |
| **python-dotenv** | 1.0.0 | Environment config |
| **numpy** | 1.26.2 | Numerical computing |
| **pandas** | 2.1.4 | Data analysis |
| **scikit-learn** | 1.3.2 | ML algorithms (RandomForest) |
| **joblib** | 1.3.2 | Model serialization |
| **transformers** | 4.36.2 | DistilBERT NLP model |
| **huggingface-hub** | 0.20.1 | Model downloads |
| **torch** | 2.2.0 | PyTorch backend |
| **nltk** | 3.8.1 | Text preprocessing |
| **requests** | 2.31.0 | HTTP requests |
| **tldextract** | 5.1.1 | Domain extraction |
| **url-normalize** | 1.4.3 | URL normalization |
| **beautifulsoup4** | 4.12.2 | HTML parsing |
| **lxml** | 4.9.4 | XML/HTML backend |

---

## 🛠️ Installation & Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/internship-credibility-frontend.git
cd internship-credibility-frontend
```

### Step 2: Auto-Install Dependencies

**Option A: Windows (Easiest)**
```bash
cd backend
START.bat
```

**Option B: Linux/Mac**
```bash
cd backend
bash START.sh
```

**Option C: Manual Install**
```bash
cd backend
pip install -r requirement1.txt
```

### Step 3: Verify Installation

```bash
# Check Python version
python --version

# Check pip
pip --version

# List installed packages
pip list | grep -E "Flask|transformers|scikit-learn|torch"
```

---

## ▶️ Running the Project

### Sequential Commands (From Fresh Clone)

```bash
# 1. Navigate to project
cd internship-credibility-frontend

# 2. Navigate to backend
cd backend

# 3. View available Python versions (Windows)
python --version

# 4. Install all required packages
pip install -r requirement1.txt

# 5. Verify critical imports
python -c "from flask import Flask; from transformers import pipeline; print('✓ Ready')"

# 6. Start the Flask application
python run.py
```

### Quick Start Methods

**Method 1: Automatic (Recommended)**
```bash
cd backend
python run.py
```
*Automatically checks and installs missing packages*

**Method 2: Windows Batch Script**
```bash
cd backend
START.bat
```
*Or double-click `START.bat` in File Explorer*

**Method 3: Linux/Mac Script**
```bash
cd backend
bash START.sh
```

**Method 4: Direct Flask**
```bash
cd backend
python app.py
```

### Expected Output

```
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Access the Application

- **Frontend:** http://localhost:5000
- **API Health:** http://localhost:5000/health

---

## 🔌 API Documentation

### 1. Health Check
```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "service": "Internship Credibility API",
  "status": "healthy"
}
```

### 2. Parse Internship Info
```bash
curl -X POST http://localhost:5000/api/parse_internship_info \
  -H "Content-Type: application/json" \
  -d '{"rawInternshipInfo": "Your job description text here"}'
```

### 3. Get Credibility Score
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "Job description text",
    "companyName": "Company Name",
    "companyWebsite": "company.com"
  }'
```

**Response:**
```json
{
  "credibility_score": 85.36,
  "credibility_level": "HIGH",
  "breakdown": {
    "company_verification_score": 100,
    "offer_quality_score": 85,
    "sentiment_score": 99,
    "email_match_score": 0
  },
  "red_flags": {},
  "recommendations": [...]
}
```

### 4. Sentiment Analysis
```bash
curl -X POST http://localhost:5000/api/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "Text to analyze"}'
```

---

## 🏗️ Architecture

### Technology Stack

| Layer | Technology |
|-------|-----------|
| **Web Framework** | Flask 3.0.0 |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **ML/NLP** | PyTorch, Transformers (DistilBERT) |
| **ML Models** | scikit-learn RandomForest |
| **Data Processing** | NumPy, Pandas |
| **Web Scraping** | BeautifulSoup4, Requests |
| **Deployment** | Vercel (Serverless) + Local Flask |

### Core Components

```
User Input
    ↓
Frontend (HTML/JS)
    ↓
Flask Routes (/api/predict, /api/parse_internship_info)
    ↓
CredibilityEngine
    ├── SentimentAnalyzer (DistilBERT)
    ├── CompanyVerifier (Web search)
    ├── URLFeatureExtractor (Domain analysis)
    ├── OfferQualityScorer (Text analysis)
    ├── EmailMatcher (Domain matching)
    └── RandomForestModel (ML prediction)
    ↓
Score & Recommendations
    ↓
Frontend Display
    ↓
User Sees Results (Credibility %, Red Flags, Recommendations)
```

### Scoring Breakdown

| Component | Weight | Purpose |
|-----------|--------|---------|
| **Company Verification** | 40% | Verify company legitimacy |
| **Offer Quality** | 30% | Evaluate completeness and professionalism |
| **Sentiment Analysis** | 20% | Detect suspicious language patterns |
| **Email Match** | 10% | Verify email domain consistency |

---

## 🐛 Troubleshooting

### "Python not found"
```bash
# Install Python 3.12+ from https://www.python.org
# Make sure to check "Add Python to PATH"
python --version
```

### "Module not found"
```bash
cd backend
pip install -r requirement1.txt
```

### "Port 5000 already in use"
```bash
# Kill process using port 5000

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :5000
kill -9 <PID>
```

### "Permission denied" (Linux/Mac)
```bash
chmod +x backend/START.sh
bash backend/START.sh
```

### "Certificate verification failed"
```bash
# Pip SSL issue:
pip install --trusted-host pypi.python.org --trusted-host pypi.org \
  --trusted-host files.pythonhosted.org -r requirement1.txt
```

### "No module named 'transformers'"
```bash
# Pre-download the DistilBERT model:
python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')"
```

### Verify Installation
```bash
python -c "
from flask import Flask
from transformers import pipeline
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import requests
print('✓ All imports successful - ready to run!')
"
```

---

## 📚 Additional Documentation

| File | Purpose |
|------|---------|
| **README.md** | This file - overview & quick start |
| **QUICK_START.md** | Detailed setup instructions |
| **DEPLOYMENT.md** | Production deployment guide |
| **REQUIREMENTS_VERIFICATION.md** | Package verification & status |
| **DEPENDENCIES_ANALYSIS.md** | Complete dependency documentation |
| **QUICK_REFERENCE.txt** | Quick package lookup |
| **documentation/project_overview.html** | Full architecture documentation |

---

## 🔐 Security & Privacy

- ✅ **No Data Collection** — Everything runs locally
- ✅ **Open Source** — Full code transparency
- ✅ **No Login Required** — Anonymous usage
- ✅ **No Cloud Upload** — All processing local
- ✅ **Optional Features** — Company lookup can be disabled

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

---

## 📞 Support

For issues, questions, or suggestions:

- **Documentation**: See `documentation/project_overview.html`
- **Setup Help**: Read `QUICK_START.md`
- **Deployment**: Check `DEPLOYMENT.md`
- **Issues**: [GitHub Issues](https://github.com/yourusername/issues)

---

**Made with ❤️ for internship seekers**

Last Updated: December 30, 2025
