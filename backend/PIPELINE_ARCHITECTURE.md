# Pipeline Architecture Diagram

## Complete Validation Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       USER SUBMITS INTERNSHIP DATA                          │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ • Company Name                                                        │  │
│  │ • Contact Email                                                       │  │
│  │ • Job Description (Full text)                                         │  │
│  │ • Position Title                                                      │  │
│  │ • Salary/Stipend                                                      │  │
│  │ • Duration                                                            │  │
│  │ • Website (optional)                                                  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                 [PIPELINE 1] DATASET VALIDATION (25% Weight)               │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Check: Is company in legitimate companies database?            │   │
│  │    • Google: ✓ YES → +0.30 boost                                 │   │
│  │    • TechVision: ~ MAYBE → 0 (small company)                     │   │
│  │    • QuickMoneyHub: ✗ NO → Continue checking                     │   │
│  │                                                                     │   │
│  │ 2. Check: Is company in known scam companies database?            │   │
│  │    • QuickMoneyHub: ✗ YES → -0.40 penalty                        │   │
│  │    • Others: ✓ NO → Continue                                      │   │
│  │                                                                     │   │
│  │ 3. Pattern Matching: Does job description match known scams?      │   │
│  │    Patterns Checked:                                                │   │
│  │    ├─ "guaranteed income"                                           │   │
│  │    ├─ "work from home unlimited"                                    │   │
│  │    ├─ "upfront payment"                                             │   │
│  │    ├─ "no experience needed"                                        │   │
│  │    ├─ "limited positions"                                           │   │
│  │    └─ "apply immediately"                                           │   │
│  │                                                                     │   │
│  │ 4. Email Domain Validation:                                         │   │
│  │    • @google.com: ✓ Legitimate → +0.05 boost                     │   │
│  │    • @tempmail.com: ✗ Temporary → -0.20 penalty                  │   │
│  │    • @company.com: ~ Unknown → 0                                   │   │
│  │                                                                     │   │
│  │ RESULT: Dataset Confidence Score (0.0-1.0)                         │   │
│  └────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│               [PIPELINE 2] COMPANY VERIFICATION (35% Weight)              │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Scam Report Detection (Google Custom Search API)                │   │
│  │    Searches:                                                         │   │
│  │    • "[Company] scam"                                               │   │
│  │    • "[Company] fraud"                                              │   │
│  │    • "[Company] internship scam complaint"                          │   │
│  │    • "[Company] fake internship"                                    │   │
│  │                                                                     │   │
│  │    If found: -0.40 penalty                                          │   │
│  │    If not found: +0.30 boost                                        │   │
│  │                                                                     │   │
│  │ 2. Website Verification:                                            │   │
│  │    ├─ Accessibility check (HTTP 200 response)                       │   │
│  │    ├─ HTTPS verification (SSL certificate)                          │   │
│  │    ├─ Domain reputation                                             │   │
│  │    └─ Response: +0.25 if valid, -0.20 if invalid                   │   │
│  │                                                                     │   │
│  │ 3. Online Presence Check:                                           │   │
│  │    • Search result count                                            │   │
│  │    • Platform listings (LinkedIn, Glassdoor, etc.)                  │   │
│  │    • Response: Up to +0.25 boost                                    │   │
│  │                                                                     │   │
│  │ 4. Company Name Analysis:                                           │   │
│  │    ├─ Length and structure                                          │   │
│  │    ├─ Business type indicators (Ltd, Inc, Solutions)                │   │
│  │    ├─ Capitalization patterns                                       │   │
│  │    └─ Geographic indicators                                         │   │
│  │                                                                     │   │
│  │ RESULT: Company Safety Score (0.0-1.0)                             │   │
│  └────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              [PIPELINE 3] SENTIMENT ANALYSIS (15% Weight)                  │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ Uses: HuggingFace Transformers (distilbert-base-uncased)          │   │
│  │                                                                     │   │
│  │ Analysis: Job description sentiment and tone                        │   │
│  │ ┌─────────────────────────────────────────────────────────┐        │   │
│  │ │ POSITIVE Sentiment (Professional, detailed) → +0.10    │        │   │
│  │ │ Examples:                                               │        │   │
│  │ │ • "Responsibilities: Develop..."                        │        │   │
│  │ │ • "We offer competitive..."                             │        │   │
│  │ │ • "Learn and grow..."                                   │        │   │
│  │ └─────────────────────────────────────────────────────────┘        │   │
│  │                                                                     │   │
│  │ ┌─────────────────────────────────────────────────────────┐        │   │
│  │ │ NEGATIVE Sentiment (Suspicious, pressure) → -0.15      │        │   │
│  │ │ Examples:                                               │        │   │
│  │ │ • "GUARANTEED INCOME"                                   │        │   │
│  │ │ • "LIMITED SPOTS AVAILABLE!!!"                          │        │   │
│  │ │ • "APPLY NOW"                                           │        │   │
│  │ │ • "Wire transfer required"                              │        │   │
│  │ └─────────────────────────────────────────────────────────┘        │   │
│  │                                                                     │   │
│  │ RESULT: Sentiment Score (0.0-1.0) + Confidence                     │   │
│  └────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│          [PIPELINE 4] OFFER QUALITY ASSESSMENT (25% Weight)              │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ Evaluates completeness and professionalism of offer                │   │
│  │                                                                     │   │
│  │ Checks:                                                             │   │
│  │ ├─ Responsibilities section: +0.15                                 │   │
│  │ ├─ Requirements section: +0.15                                     │   │
│  │ ├─ Compensation details: +0.15                                     │   │
│  │ ├─ Benefits/Learning outcomes: +0.15                               │   │
│  │ ├─ Company description: +0.10                                      │   │
│  │ ├─ Application process: +0.10                                      │   │
│  │ ├─ Realistic salary range: +0.10                                   │   │
│  │ └─ Professional tone & formatting: +0.10                           │   │
│  │                                                                     │   │
│  │ Also checks for:                                                    │   │
│  │ ├─ Unusual capitalization (scam indicator)                         │   │
│  │ ├─ Excessive punctuation (scam indicator)                          │   │
│  │ ├─ Unrealistic claims (bonus deductions)                           │   │
│  │ └─ Length indicator (longer = more professional)                   │   │
│  │                                                                     │   │
│  │ RESULT: Offer Quality Score (0.0-1.0)                              │   │
│  └────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                [PIPELINE 5] RED FLAG DETECTION                             │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ Detects specific scam indicators and suspicious patterns           │   │
│  │                                                                     │   │
│  │ CRITICAL FLAGS (Each -0.30 points):                                │   │
│  │ ├─ ⛔ Upfront payment requirement                                   │   │
│  │ ├─ ⛔ Wire transfer for fees                                       │   │
│  │ ├─ ⛔ Bitcoin/cryptocurrency payment                               │   │
│  │ ├─ ⛔ Guaranteed income promise                                    │   │
│  │ └─ ⛔ Training fee requirement                                     │   │
│  │                                                                     │   │
│  │ HIGH SEVERITY FLAGS (Each -0.20 points):                           │   │
│  │ ├─ ⚠ NDA signing before interview                                  │   │
│  │ ├─ ⚠ No salary discussion                                          │   │
│  │ ├─ ⚠ Too-good-to-be-true benefits                                  │   │
│  │ ├─ ⚠ Unprofessional company name                                   │   │
│  │ └─ ⚠ Temporary email domain                                        │   │
│  │                                                                     │   │
│  │ MEDIUM FLAGS (Each -0.10 points):                                  │   │
│  │ ├─ ~ Pressure to apply ("Limited spots")                           │   │
│  │ ├─ ~ Unusual work-from-home promises                               │   │
│  │ ├─ ~ No company website                                            │   │
│  │ └─ ~ Minimal job description                                       │   │
│  │                                                                     │   │
│  │ RESULT: List of detected red flags and severity levels             │   │
│  └────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                  [PIPELINE 6] FINAL SCORING & ANALYSIS                     │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ Calculate Weighted Score:                                           │   │
│  │                                                                     │   │
│  │ Final Score = (Dataset × 0.25) +                                   │   │
│  │               (Company × 0.35) +                                   │   │
│  │               (Quality × 0.25) +                                   │   │
│  │               (Sentiment × 0.15) -                                 │   │
│  │               (Red Flags Penalty)                                   │   │
│  │                                                                     │   │
│  │ Score Range: 0.0 - 1.0 (0% - 100%)                                │   │
│  │                                                                     │   │
│  │ Credibility Level:                                                 │   │
│  │ ┌─────────────────────────────────────────────────────────┐        │   │
│  │ │ 90-100%: VERY_HIGH       ✓✓✓ Verified Legitimate      │        │   │
│  │ │ 70-89%:  LIKELY_LEGIT    ✓✓  Probably Safe            │        │   │
│  │ │ 50-69%:  UNCERTAIN       ~   Requires Investigation   │        │   │
│  │ │ 20-49%:  RISKY           ⚠   Suspicious Elements      │        │   │
│  │ │ 0-19%:   VERY_LOW        ✗✗  Likely Scam             │        │   │
│  │ └─────────────────────────────────────────────────────────┘        │   │
│  │                                                                     │   │
│  │ Generate Recommendations:                                           │   │
│  │ ├─ Based on score level                                            │   │
│  │ ├─ Based on detected red flags                                     │   │
│  │ ├─ Based on company verification results                           │   │
│  │ └─ Based on sentiment and quality analysis                         │   │
│  │                                                                     │   │
│  │ RESULT: Complete credibility assessment with score, level,         │   │
│  │         recommendations, and detailed breakdown                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RETURN RESULTS TO USER                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ {                                                                    │  │
│  │   "credibility_score": 0.885,                                        │  │
│  │   "credibility_level": "LIKELY_LEGITIMATE",                          │  │
│  │   "breakdown": {                                                     │  │
│  │     "dataset_score": 0.80,                                           │  │
│  │     "company_verification_score": 0.90,                              │  │
│  │     "offer_quality_score": 0.92,                                     │  │
│  │     "sentiment_score": 0.85                                          │  │
│  │   },                                                                 │  │
│  │   "dataset_validation": { ... },                                     │  │
│  │   "company_verification": { ... },                                   │  │
│  │   "red_flags": { },                                                  │  │
│  │   "recommendations": [                                               │  │
│  │     "✓ Company found in verified database",                          │  │
│  │     "Professional job description indicates legitimacy",             │  │
│  │     "No red flags detected - Safe to proceed"                        │  │
│  │   ]                                                                  │  │
│  │ }                                                                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Weight Distribution

```
Dataset Validation      ████████░░░░░░░░░░░░░ 25%
Company Verification   ███████████░░░░░░░░░░░░ 35%
Offer Quality          ████████░░░░░░░░░░░░░░░ 25%
Sentiment Analysis     ███░░░░░░░░░░░░░░░░░░░░ 15%
                       ─────────────────────────────
                       100% Total
```

## Test Case Examples

### Test 1: Google (Expected: 85-95%)
```
Dataset:     0.95 (✓ in legitimate DB)
Company:     0.90 (✓ high online presence)
Quality:     0.92 (✓ detailed offer)
Sentiment:   0.85 (✓ professional tone)
Red Flags:   None (-0.00)
─────────────────────────
Final:       0.885 = 88.5% LIKELY_LEGITIMATE ✓
```

### Test 2: QuickMoneyHub (Expected: 5-15%)
```
Dataset:     0.10 (✗ scam pattern match)
Company:     0.05 (✗ suspicious name)
Quality:     0.15 (✗ unrealistic promises)
Sentiment:   0.20 (✗ pressure language)
Red Flags:   -0.50 (✓ multiple critical)
─────────────────────────
Final:       0.10 = 10% VERY_LOW ✗
```

### Test 3: TechVision (Expected: 70-80%)
```
Dataset:     0.70 (~ limited info)
Company:     0.75 (~ small company)
Quality:     0.80 (✓ good structure)
Sentiment:   0.75 (✓ professional)
Red Flags:   -0.05 (~ few minor)
─────────────────────────
Final:       0.75 = 75% LIKELY_LEGITIMATE ✓
```

---

## Data Flow Summary

1. **Input** → User submits data
2. **Dataset** → Check databases, patterns, emails
3. **Company** → Verify legitimacy, search scam reports
4. **Sentiment** → Analyze tone and language
5. **Quality** → Evaluate offer professionalism
6. **Red Flags** → Detect specific scam indicators
7. **Score** → Calculate weighted final score
8. **Output** → Return credibility assessment

All pipelines execute in parallel when possible, with comprehensive logging at each stage.
