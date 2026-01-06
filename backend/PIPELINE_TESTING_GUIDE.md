# Pipeline Validation Testing Guide

## Overview

This testing suite validates that user-submitted internship data flows correctly through all validation pipelines:

1. **Dataset Validation Pipeline** - Checks against HuggingFace and Kaggle datasets
2. **Company Verification Pipeline** - Verifies company legitimacy
3. **Sentiment Analysis Pipeline** - Analyzes job description tone
4. **Offer Quality Assessment Pipeline** - Evaluates offer completeness and professionalism
5. **Red Flag Detection Pipeline** - Identifies suspicious patterns
6. **Final Scoring Pipeline** - Calculates credibility score and recommendation

## Test Cases Included

### Case 1: Legitimate Company (Google)
- **Status**: ✓ Expected to be HIGH_CREDIBILITY
- **Company**: Google LLC
- **Email**: careers@google.com
- **Key Features**:
  - Professional job description
  - Realistic compensation
  - Clear company history
  - Legitimate contact
- **Expected Pipeline Results**:
  - ✓ Dataset: Company found in legitimate database
  - ✓ Company Verification: Positive indicators
  - ✓ Sentiment: Professional positive tone
  - ✓ Offer Quality: High (detailed requirements, benefits)
  - ✓ Red Flags: None
  - **Expected Score**: 85-95%

### Case 2: Clear Scam (QuickMoneyHub)
- **Status**: ✗ Expected to be VERY_LOW_CREDIBILITY
- **Company**: QuickMoneyHub Fast Earnings Inc
- **Email**: admin@quickmoneyhub.tempmail.com
- **Key Red Flags**:
  - Promises guaranteed income
  - Temporary email (tempmail.com)
  - Upfront payment required
  - Unrealistic earnings claims
  - Suspicious company name pattern
  - Pressure tactics ("Limited spots!")
- **Expected Pipeline Results**:
  - ✗ Dataset: Company in scam companies list + pattern matching
  - ✗ Company Verification: Multiple negative indicators
  - ✗ Sentiment: Suspicious language detected
  - ✗ Offer Quality: Unrealistic promises
  - ✗ Red Flags: Multiple critical flags (payment, scam patterns)
  - **Expected Score**: 5-15%

### Case 3: Legitimate Startup (TechVision)
- **Status**: ✓ Expected to be MEDIUM-HIGH_CREDIBILITY
- **Company**: TechVision Solutions Private Limited
- **Email**: internships@techvision.co.in
- **Key Features**:
  - Real company description
  - Realistic stipend (₹20,000/month)
  - Professional structure
  - Detailed selection process
  - Legitimate contact details
- **Expected Pipeline Results**:
  - ✓ Dataset: Legitimate business indicators
  - ✓ Company Verification: Positive references
  - ✓ Sentiment: Professional tone
  - ✓ Offer Quality: Good (clear process, realistic terms)
  - ✓ Red Flags: Minimal
  - **Expected Score**: 70-80%

### Case 4: Suspicious International Program (Payment Required)
- **Status**: ⚠ Expected to be LOW_CREDIBILITY (potential scam)
- **Company**: GlobalTech Internship Network
- **Email**: recruitment@globaltech-network.org
- **Red Flags**:
  - Upfront payment required ($450)
  - "30-day money back guarantee minus $50 admin fee"
  - Pressure tactics ("48-hour window")
  - Generic roles
  - International visa promises
- **Expected Pipeline Results**:
  - ✗ Dataset: Scam pattern matches (fees, visa promises)
  - ✗ Company Verification: Suspicious elements
  - ✗ Sentiment: Pressure tactics detected
  - ✗ Offer Quality: Questionable structure
  - ✗ Red Flags: Payment requirement, visa guarantees
  - **Expected Score**: 20-30%

### Case 5: Borderline Legitimate (Small Startup)
- **Status**: ⚠ Expected to be MEDIUM_CREDIBILITY
- **Company**: DataDriven Analytics Services
- **Email**: hr@datadriven-analytics.com
- **Key Features**:
  - Smaller company
  - Realistic stipend (₹15,000/month)
  - Some professional details
  - Legitimate contact details
  - No upfront payment
- **Expected Pipeline Results**:
  - ~ Dataset: Limited company information
  - ~ Company Verification: Few indicators
  - ~ Sentiment: Neutral to slightly positive
  - ~ Offer Quality: Moderate
  - ~ Red Flags: Few but some concerns
  - **Expected Score**: 55-70%

---

## How to Run Tests

### Prerequisites

```bash
# Ensure Flask server is running
cd backend
python app.py
# Server should start on http://localhost:5000
```

### Run All Tests

```bash
# From backend directory
python tests/run_pipeline_tests.py
```

### Expected Output

```
================================================================================
INTERNSHIP CREDIBILITY VALIDATION PIPELINE TEST
================================================================================
Test Start Time: 2026-01-06 10:30:45
Backend URL: http://localhost:5000
================================================================================

================================================================================
TEST CASE: CASE_1_LEGITIMATE_GOOGLE
================================================================================
Description: Legitimate internship from Google
Company: Google LLC
Email: careers@google.com
...

[PIPELINE] Sending request to backend API...

[PIPELINE] Analyzing response from all validation pipelines...

✓ DATASET VALIDATION PIPELINE EXECUTED
  - Checks: ['legitimate_company_check']
  - Warnings: 1
  - Patterns Found: 0

✓ COMPANY VERIFICATION PIPELINE EXECUTED
  - Warnings: 0
  - Positive Indicators: 3

✓ SENTIMENT ANALYSIS PIPELINE EXECUTED
  - Sentiment Score: 0.85

✓ OFFER QUALITY ASSESSMENT PIPELINE EXECUTED
  - Offer Quality Score: 0.92

✓ RED FLAG DETECTION PIPELINE EXECUTED
  - Red Flags Found: 0

✓ FINAL SCORING PIPELINE EXECUTED
  - Final Credibility Score: 88.50%
  - Credibility Level: LIKELY_LEGITIMATE

✓ RECOMMENDATIONS PIPELINE EXECUTED
  - Generated 2 recommendations
```

---

## Understanding Pipeline Results

### Dataset Validation Pipeline
```python
{
  "dataset_validation": {
    "checks_performed": ["legitimate_company_check", "scam_pattern_check"],
    "warnings": ["✓ Company found in verified database"],
    "matching_patterns": []
  }
}
```
**What it does**: 
- Checks if company is in legitimate companies database
- Checks if company is in known scam database
- Matches job description against scam patterns
- Scores contribution: 25%

### Company Verification Pipeline
```python
{
  "company_verification": {
    "warnings": [],
    "positive_indicators": [
      "No scam reports found",
      "Company has accessible website",
      "Website uses HTTPS"
    ]
  }
}
```
**What it does**:
- Searches for scam reports (Google CSE)
- Verifies website accessibility
- Checks for HTTPS
- Finds online presence
- Scores contribution: 35%

### Sentiment Analysis Pipeline
```python
{
  "breakdown": {
    "sentiment_score": 0.85,
    "sentiment_label": "POSITIVE",
    "sentiment_confidence": 0.92
  }
}
```
**What it does**:
- Analyzes tone of job description using NLP
- Detects positive vs suspicious language
- Scores contribution: 15%

### Offer Quality Assessment Pipeline
```python
{
  "breakdown": {
    "offer_quality_score": 0.92
  }
}
```
**What it does**:
- Evaluates completeness of offer details
- Checks for professional structure
- Verifies realistic compensation
- Scores contribution: 25%

### Red Flag Detection Pipeline
```python
{
  "red_flags": {
    "upfront_payment": "Upfront payment requirement detected",
    "guaranteed_income": "Unrealistic earnings guarantee"
  }
}
```
**What it does**:
- Detects common scam patterns
- Identifies suspicious requirements
- Flags unrealistic promises
- Returns: List of detected flags

### Final Scoring Pipeline
```python
{
  "credibility_score": 0.885,
  "credibility_level": "LIKELY_LEGITIMATE"
}
```
**Formula**:
```
Score = (Dataset × 0.25) + (Company × 0.35) + (Quality × 0.25) + (Sentiment × 0.15)
```

**Levels**:
- `VERY_HIGH` (90-100%): Verified legitimate
- `LIKELY_LEGITIMATE` (70-89%): Probably safe
- `UNCERTAIN` (50-69%): Requires investigation
- `RISKY` (20-49%): Suspicious elements
- `VERY_LOW` (0-19%): Likely scam

---

## Expected Test Results Summary

| Test Case | Expected Score | Expected Level | All Pipelines | Status |
|-----------|----------------|----------------|---------------|--------|
| Google (Legitimate) | 85-95% | LIKELY_LEGITIMATE | ✓ All 6 | PASS |
| QuickMoneyHub (Scam) | 5-15% | VERY_LOW | ✓ All 6 | PASS |
| TechVision (Startup) | 70-80% | LIKELY_LEGITIMATE | ✓ All 6 | PASS |
| GlobalTech (Suspicious) | 20-30% | RISKY | ✓ All 6 | PASS |
| DataDriven (Borderline) | 55-70% | UNCERTAIN | ✓ All 6 | PASS |

---

## Troubleshooting

### "Could not connect to backend"
```bash
# Check if Flask is running
cd backend
python app.py
# Should see: Running on http://localhost:5000
```

### "HTTP 500: Internal Server Error"
- Check backend logs for errors
- Verify all imports are available
- Check if .env file is configured correctly

### "API responded with 400"
- Check request data format
- Verify all required fields are present:
  - companyName
  - jobDescription
  - contactEmail (optional)

### Test script not found
```bash
# Ensure you're in the correct directory
cd backend
python tests/run_pipeline_tests.py
```

---

## Interpreting Results

### High Score (85%+) - LIKELY_LEGITIMATE
- Company verified in datasets
- Professional job description
- No red flags detected
- Realistic compensation

### Medium Score (50-70%) - UNCERTAIN
- Some verification challenges
- Limited company information
- Minor suspicious indicators
- Requires user investigation

### Low Score (20-50%) - RISKY
- Multiple suspicious elements
- Red flags detected
- Poor company verification
- Unrealistic promises

### Very Low Score (0-20%) - VERY_LOW
- Clear scam indicators
- Multiple red flags
- Confirmed in scam databases
- Strong recommendation against

---

## Next Steps

After running tests:

1. **Review Results**: Check `test_results.json` for detailed output
2. **Verify Pipelines**: Ensure all 6 pipelines executed
3. **Check Scores**: Compare with expected results
4. **Test Variations**: Try custom test cases
5. **Deploy**: If all tests pass, deploy to production

---

## Custom Testing

To add your own test cases, edit `test_datasets.py`:

```python
test_cases["your_test_name"] = {
    "description": "Your test description",
    "companyName": "Company Name",
    "contactEmail": "email@company.com",
    "position": "Job Title",
    "salary": "Compensation",
    "duration": "Duration",
    "jobDescription": "Full job description",
    "website": "https://company.com"
}
```

Then run:
```bash
python tests/run_pipeline_tests.py
```
