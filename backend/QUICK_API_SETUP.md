# Quick Start: API Configuration

## TL;DR - Get Started in 5 Minutes

### 1. Copy .env Template
```bash
cd backend
cp .env.example .env
```

### 2. Add Google CSE Keys (Recommended)
Get from: https://console.cloud.google.com/ and https://programmablesearchengine.google.com/

Edit `backend/.env`:
```
GOOGLE_CSE_API_KEY=AIzaSy... (from Google Cloud)
GOOGLE_CSE_ENGINE_ID=1234567... (from Custom Search)
```

### 3. Restart Flask
```bash
python backend/app.py
```

### 4. Verify
You should see:
```
[INFO] === Company Verifier API Status ===
[✓] Google Custom Search API: CONFIGURED
```

---

## What Each API Does

| API | Purpose | Required? | Setup Time |
|-----|---------|-----------|-----------|
| **Google CSE** | Real web search for scam reports | No* | 10 min |
| **HuggingFace** | Dataset validation | No | 5 min |
| **Kaggle** | Verified internship datasets | No | 10 min |

*Google CSE recommended for best results. Without it, uses pattern detection.

---

## .env Configuration

```env
# Google Custom Search (for company web searches)
GOOGLE_CSE_API_KEY=your_key
GOOGLE_CSE_ENGINE_ID=your_engine_id

# HuggingFace (for company databases)
HUGGINGFACE_API_KEY=your_token

# Kaggle (for internship datasets)
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_api_key
```

---

## No API? No Problem!

The system works without any API keys:
- Uses local scam company database
- Uses pattern-based fraud detection
- Shows warning when APIs not configured
- Full fallback to offline operation

---

## Full Setup Guide

See: `API_SETUP_GUIDE.md` for detailed instructions

## Integration Details

See: `API_INTEGRATION_SUMMARY.md` for technical overview
