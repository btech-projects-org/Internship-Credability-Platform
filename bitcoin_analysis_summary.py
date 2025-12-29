#!/usr/bin/env python3
"""Summary of Bitcoin India internship parsing improvements"""
import sys
sys.path.insert(0, 'backend')

from services.info_parser import InternshipInfoParser
from services.credibility_engine import CredibilityEngine

# Real Bitcoin India internship data from Internshala
bitcoin_data = """HR Administration
BITCOIN INDIA SOFTWARE SERVICES PRIVATE LIMITED
Start Date
Immediately
Duration
2 Months
Stipend
₹ 5,000 - 8,000 /month
Apply By
19 May' 24
Internshala's Advice
Show your interest in HR & build a solid profile by adding relevant skills, education, projects & experience to increase your job opportunities at Internshala.
Today's best opportunity
₹ 50,000/month salary + incentives
Profile
1. Preparing and processing payroll for employees
2. Updating employee records with new hire information and/or changes in employment status
3. Maintaining current HR files and databases
4. Answering employee questions about benefits (for example, vacation days and sick time)
5. Completing termination paperwork and assisting with exit interviews
6. Processing all employment verification requests
7. Assisting with the recruitment process by posting job openings and conducting phone screens or interviews with applicants
8. Scheduling meetings and interviews as requested by the hiring manager
Who can apply
Certain candidates need to be from the below-mentioned cities.
Activity on Internshala
Hiring since March 2024
131 opportunities posted
46 candidates hired
About the company
Activity on Internshala
Hiring since March 2024
131 opportunities posted
46 candidates hired
BITCOIN INDIA SOFTWARE SERVICES PRIVATE LIMITED is a cryptocurrency exchange and trading platform based in India."""

print("=" * 80)
print("BITCOIN INDIA INTERNSHIP - CREDIBILITY ANALYSIS")
print("=" * 80)
print()

# Step 1: Parse the data
parser = InternshipInfoParser()
parsed = parser.parse(bitcoin_data)

print("STEP 1: DATA PARSING")
print("-" * 80)
print(f"Company Name: {parsed.get('companyName', 'N/A')}")
print(f"Position: {parsed.get('position', 'N/A')}")
print(f"Contact Email: {parsed.get('contactEmail', 'N/A')}")
print(f"Salary: {parsed.get('salary', 'N/A')}")
print(f"Duration: {parsed.get('duration', 'N/A')}")
print(f"Job Description Length: {len(parsed.get('jobDescription', ''))} characters")
print(f"Red Flags Detected: {parsed.get('redFlags', [])}")
print()

# Step 2: Analyze credibility
engine = CredibilityEngine()
result = engine.analyze({'parsed': parsed})

print("STEP 2: CREDIBILITY ANALYSIS")
print("-" * 80)
print(f"Overall Score: {result.get('credibility_score', 0)}%")
print(f"Credibility Level: {result.get('credibility_level', 'UNKNOWN')}")
print()

# Step 3: Score breakdown
breakdown = result.get('breakdown', {})
print("Score Breakdown:")
print(f"  - Company Verification: {breakdown.get('company_verification_score', 0):.2f}")
print(f"  - URL Score: {breakdown.get('url_score', 0):.2f}")
print(f"  - Email Match: {breakdown.get('email_match_score', 0):.2f}")
print(f"  - Sentiment: {breakdown.get('sentiment_score', 0):.2f}")
print(f"  - Verification: {breakdown.get('verification_score', 0):.2f}")
print(f"  - Red Flag Penalty: {breakdown.get('red_flag_penalty', 0):.2f}")
print()

# Step 4: Recommendations
recs = result.get('recommendations', [])
if recs:
    print("Recommendations:")
    for rec in recs[:3]:  # Show first 3 recommendations
        print(f"  - {rec}")
print()

print("=" * 80)
print("RESULT: Bitcoin India internship analysis COMPLETED SUCCESSFULLY!")
print("=" * 80)
