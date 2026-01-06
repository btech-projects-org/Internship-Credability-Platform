# Dataset Validation Integration

## Overview

The Internship Credibility Platform now validates user-submitted internship data against verified datasets from HuggingFace and Kaggle, in addition to the existing web-based verification methods.

## Architecture

### Three-Layer Validation System

1. **Dataset Validation (25% weight)**
   - Checks against verified companies database (HuggingFace/Kaggle/Local)
   - Detects known scam companies
   - Pattern matching for common scam indicators

2. **Web-Based Verification (35% + 25% weight)**
   - Company online presence verification
   - Website SSL/HTTPS validation
   - Scam report detection
   - Offer quality assessment

3. **Sentiment Analysis (15% weight)**
   - NLP-based tone analysis of job description
   - Detects suspicious language patterns

## Setup Instructions

### 1. Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
# HuggingFace API (for dataset access)
HUGGINGFACE_API_KEY=your_token_here

# Kaggle API (for internship scam datasets)
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_api_key

# Google Custom Search (existing)
GOOGLE_CSE_API_KEY=your_key
GOOGLE_CSE_ENGINE_ID=your_engine_id
```

### 2. Get API Keys

#### HuggingFace Token
1. Sign up at https://huggingface.co
2. Go to Settings → Access Tokens
3. Create a new token with read access

#### Kaggle API Key
1. Sign up at https://kaggle.com
2. Go to Settings → API
3. Click "Create New API Token" (downloads kaggle.json)
4. Copy username and key from kaggle.json

### 3. Local Datasets

The system includes built-in local datasets for offline validation:

- `backend/data/legitimate_companies.json` - Verified companies list
- `backend/data/scam_companies.json` - Known scam companies
- `backend/data/scam_patterns.json` - Common scam indicators and patterns

These load automatically without requiring API keys.

## How It Works

### Validation Flow

```
User Submits Data
    ↓
[Company Name, Email, Job Description]
    ↓
1. Dataset Validation (HuggingFace/Kaggle/Local)
   - Is company in legitimate database? (+0.3 score)
   - Is company in scam database? (-0.4 score)
   - Do patterns match scam indicators? (-0.05 to -0.3 score)
   - Is email from temp service? (-0.2 score)
    ↓
2. Web-Based Verification (existing)
   - Search for scam reports
   - Verify website validity
   - Check online presence
    ↓
3. Sentiment Analysis
   - Analyze job description tone
   - Detect suspicious language
    ↓
Final Score = (Dataset * 0.25) + (Web * 0.35) + (Quality * 0.25) + (Sentiment * 0.15)
```

### Example Validation Results

```json
{
  "credibility_score": 0.78,
  "credibility_level": "LIKELY_LEGITIMATE",
  "dataset_validation": {
    "checks_performed": [
      "legitimate_company_check",
      "scam_pattern_check",
      "email_domain_check"
    ],
    "warnings": [
      "✓ Google found in verified companies dataset"
    ],
    "matching_patterns": []
  },
  "recommendations": [
    "✓ Google found in verified companies dataset",
    "Company has accessible website",
    "Website uses HTTPS"
  ]
}
```

## Supported Datasets

### HuggingFace Datasets
- `datasets/legitimate_companies` - Verified company database
- `datasets/internship_scams` - Known scam patterns and indicators

### Kaggle Datasets
- `mrisdal/internship-scams` - Comprehensive internship scam analysis
- Custom verified company datasets

### Local JSON Datasets
- Legitimate companies list
- Known scam companies
- Scam pattern indicators

## API Response Enhancement

The `/api/analyze` endpoint now returns:

```json
{
  "credibility_score": 0.75,
  "breakdown": {
    "dataset_score": 0.8,
    "company_verification_score": 0.7,
    "offer_quality_score": 0.6,
    "sentiment_score": 0.5
  },
  "dataset_validation": {
    "checks_performed": ["legitimate_company_check", "scam_pattern_check"],
    "warnings": ["Company found in verified database"],
    "matching_patterns": []
  }
}
```

## Performance Notes

- Dataset validation adds ~100-500ms to analysis (async loading)
- Results are cached in memory for subsequent requests
- Local datasets load instantly; API-based datasets load on first request

## Troubleshooting

### "HUGGINGFACE_API_KEY not set"
- This is optional. System will use local datasets.
- To enable, set HUGGINGFACE_API_KEY in .env

### "KAGGLE credentials not set"
- This is optional. System will use local datasets.
- To enable, download kaggle.json from Kaggle API settings

### Datasets not loading
- Check backend/data/ directory exists
- Verify JSON file format is valid
- Check API keys are correctly set in .env

## Future Enhancements

- [ ] Real-time dataset updates via scheduled sync
- [ ] Custom company whitelist/blacklist management
- [ ] Machine learning for pattern detection
- [ ] Community-contributed scam reports
- [ ] Integration with employment verification APIs
