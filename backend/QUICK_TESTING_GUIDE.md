# Quick Start: Pipeline Testing

## Run Tests in 3 Steps

### Step 1: Start Flask Server
```bash
cd backend
python app.py
# Should show: Running on http://localhost:5000
```

### Step 2: Run Test Suite (in new terminal)
```bash
cd backend
python tests/run_pipeline_tests.py
```

### Step 3: View Results
- Console output shows immediate results
- `backend/tests/test_results.json` contains detailed data

---

## What Gets Tested

Each test case validates that user data flows through **6 validation pipelines**:

```
User Input
    ↓
[1] Dataset Validation (25%)
    ├─ Check legitimate company database
    ├─ Check scam company list
    └─ Pattern matching for red flags
    ↓
[2] Company Verification (35%)
    ├─ Web search for scam reports
    ├─ Website verification
    └─ Online presence check
    ↓
[3] Sentiment Analysis (15%)
    ├─ NLP tone analysis
    └─ Suspicious language detection
    ↓
[4] Offer Quality Assessment (25%)
    ├─ Detail completeness check
    └─ Professionalism evaluation
    ↓
[5] Red Flag Detection
    ├─ Payment requirements
    ├─ Unrealistic promises
    └─ Suspicious patterns
    ↓
[6] Final Scoring
    └─ Calculate credibility score (0-100%)
```

---

## 5 Test Cases Included

| # | Case | Company | Expected | Status |
|---|------|---------|----------|--------|
| 1 | Legitimate | Google LLC | 85-95% | ✓ Should PASS |
| 2 | Scam | QuickMoneyHub | 5-15% | ✓ Should PASS |
| 3 | Startup | TechVision | 70-80% | ✓ Should PASS |
| 4 | Suspicious | GlobalTech | 20-30% | ✓ Should PASS |
| 5 | Borderline | DataDriven | 55-70% | ✓ Should PASS |

---

## Expected Output Example

```
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

Status: ✓ SUCCESS
```

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `ConnectionError` | Flask not running: `python app.py` |
| `HTTP 500` | Check imports and .env file |
| `Timeout` | Flask taking too long, check logs |
| Tests not found | Run from `backend/` directory |

---

## Test Case Breakdown

### Test 1: Google (Expected High Score)
✓ Legitimate company in database
✓ Professional job description
✓ Realistic compensation
✓ No red flags
→ **Expected**: 85-95% LIKELY_LEGITIMATE

### Test 2: QuickMoneyHub (Expected Very Low Score)
✗ Scam pattern in company name
✗ Temporary email (tempmail)
✗ Unrealistic earnings
✗ Upfront payment required
→ **Expected**: 5-15% VERY_LOW

### Test 3: TechVision (Expected Good Score)
✓ Real company structure
✓ Realistic stipend
✓ Clear process
✓ Professional contact
→ **Expected**: 70-80% LIKELY_LEGITIMATE

### Test 4: GlobalTech (Expected Low Score)
✗ Upfront fees required
✗ Pressure tactics
✗ Generic promises
✗ Visa sponsorship claim
→ **Expected**: 20-30% RISKY

### Test 5: DataDriven (Expected Medium Score)
~ Limited information
~ Realistic terms
~ Some professional elements
~ Unknown company
→ **Expected**: 55-70% UNCERTAIN

---

## Verify All Pipelines Executed

Check console output for these lines (one for each test):
```
✓ DATASET VALIDATION PIPELINE EXECUTED
✓ COMPANY VERIFICATION PIPELINE EXECUTED
✓ SENTIMENT ANALYSIS PIPELINE EXECUTED
✓ OFFER QUALITY ASSESSMENT PIPELINE EXECUTED
✓ RED FLAG DETECTION PIPELINE EXECUTED
✓ FINAL SCORING PIPELINE EXECUTED
✓ RECOMMENDATIONS PIPELINE EXECUTED (bonus)
```

If any are missing, check backend logs for errors.

---

## Results File

After running tests, check: `backend/tests/test_results.json`

Contains:
- Complete API responses
- Pipeline execution details
- Scores and levels
- All warnings and flags
- Execution errors (if any)

---

## Next Steps

1. ✓ Run the tests
2. ✓ Verify all pipelines execute
3. ✓ Check scores match expectations
4. ✓ Review results in test_results.json
5. → Deploy with confidence

---

## Need More Details?

See: `PIPELINE_TESTING_GUIDE.md` for comprehensive documentation
