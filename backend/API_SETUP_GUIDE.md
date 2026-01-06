# API Configuration Guide

## Overview
The Internship Credibility Platform uses multiple APIs for comprehensive verification. This guide shows how to configure each API.

## APIs Used

### 1. Google Custom Search Engine (Required for best results)
**Purpose:** Search the web for scam reports about companies

**Steps to Configure:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "Custom Search API":
   - Search for "Custom Search API" in the search bar
   - Click on it and press "ENABLE"
4. Create API credentials:
   - Go to "Credentials" in left menu
   - Click "Create Credentials" → "API Key"
   - Copy the API Key
5. Set up Custom Search Engine:
   - Go to [Custom Search Engine](https://programmablesearchengine.google.com/)
   - Click "Create" to create a new search engine
   - Give it a name and select "Search the entire web"
   - Once created, copy the Search Engine ID (CX)

**Add to .env:**
```
GOOGLE_CSE_API_KEY=your_api_key_from_step_4
GOOGLE_CSE_ENGINE_ID=your_cx_from_step_5
```

**Free Tier:** 100 queries per day

---

### 2. HuggingFace API (Optional - for dataset validation)
**Purpose:** Access verified company databases and scam patterns

**Steps to Configure:**

1. Sign up at [HuggingFace](https://huggingface.co)
2. Go to Settings → Access Tokens
3. Click "New token"
4. Name it (e.g., "Internship Checker")
5. Set role to "read"
6. Copy the token

**Add to .env:**
```
HUGGINGFACE_API_KEY=hf_your_token_here
```

**Free Tier:** Unlimited (with rate limits)

---

### 3. Kaggle API (Optional - for verified internship datasets)
**Purpose:** Access verified internship and company datasets

**Steps to Configure:**

1. Sign up at [Kaggle](https://kaggle.com)
2. Go to Settings → API
3. Click "Create New API Token"
4. A file `kaggle.json` will download
5. Open it and copy the username and key

**Add to .env:**
```
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_key
```

**Free Tier:** Limited downloads per day

---

## Creating .env File

1. Copy `.env.example` to `.env`:
   ```bash
   cp backend/.env.example backend/.env
   ```

2. Edit `backend/.env` and fill in your API keys:
   ```bash
   GOOGLE_CSE_API_KEY=your_key
   GOOGLE_CSE_ENGINE_ID=your_cx
   HUGGINGFACE_API_KEY=your_hf_token
   KAGGLE_USERNAME=your_username
   KAGGLE_KEY=your_key
   ```

3. Save and restart the Flask server

---

## Verification

### Check if APIs are Loaded

When you start the Flask server, you should see:

```
[INFO] === Company Verifier API Status ===
[✓] Google Custom Search API: CONFIGURED
[✓] HuggingFace API: CONFIGURED
[✓] Dataset Validator: INITIALIZED with 23 legitimate companies
```

Or if not configured:

```
[INFO] === Company Verifier API Status ===
[✗] Google Custom Search API: NOT CONFIGURED (using heuristics only)
[✗] HuggingFace API: NOT CONFIGURED
[✓] Dataset Validator: INITIALIZED with local datasets
```

---

## Fallback Behavior

The system is designed to work without APIs:

- **Without Google CSE:** Uses pattern-based scam detection (built-in rules)
- **Without HuggingFace:** Uses local JSON datasets (`backend/data/`)
- **Without Kaggle:** Uses local JSON datasets (`backend/data/`)

### Local Datasets Included:
- `legitimate_companies.json` - 23 verified major companies
- `scam_companies.json` - Known scam company names
- `scam_patterns.json` - 10 common scam indicators

---

## API Rate Limits & Costs

| API | Free Tier | Cost | Impact |
|-----|-----------|------|--------|
| Google CSE | 100/day | $5/1000 queries above free | Required for best verification |
| HuggingFace | Unlimited | Free | Optional, improves dataset validation |
| Kaggle | Rate limited | Free | Optional, improves company verification |

---

## Environment Variables Reference

```env
# ========================
# ENVIRONMENT CONFIGURATION
# ========================

# Google Custom Search Engine (for company search)
GOOGLE_CSE_API_KEY=your_google_cse_api_key_here
GOOGLE_CSE_ENGINE_ID=your_google_cse_engine_id_here

# HuggingFace API (for dataset validation)
HUGGINGFACE_API_KEY=your_huggingface_api_token_here

# Kaggle API (for verified internship/company datasets)
KAGGLE_USERNAME=your_kaggle_username_here
KAGGLE_KEY=your_kaggle_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=False
```

---

## Troubleshooting

### "Google CSE API: NOT CONFIGURED"
- Check if `.env` file exists in `backend/` directory
- Verify API key and Engine ID are correct
- Check for typos in variable names

### "API quota exceeded"
- Google CSE: Limited to 100 free queries/day
- Wait for quota reset (midnight Pacific Time)
- Consider upgrading to paid tier

### "Invalid Credentials"
- Verify credentials are copied correctly
- Check for extra whitespace in `.env`
- Ensure API is enabled in Google Cloud Console

---

## Next Steps

1. Configure at least Google CSE for real scam report searching
2. (Optional) Add HuggingFace for enhanced dataset validation
3. (Optional) Add Kaggle for internship-specific datasets
4. Restart Flask server: `python backend/app.py`
5. Test with sample company name
