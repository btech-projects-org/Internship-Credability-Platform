"""Test system with multiple different inputs"""

import sys
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from services.info_parser import InternshipInfoParser
from services.credibility_engine import CredibilityEngine

# Test Case 1: Legitimate company (MastersHelp)
test1 = """Operations
MastersHelp

Actively hiring
MastersHelp
₹ 7,500 - 10,000 /month
Secunderabad, Hyderabad
3 Months
About MastersHelp:
MastersHelp is an initiative providing free study abroad support.
Activity on Internshala: Hiring since: December 2024; Opportunities posted: 29; Candidates hired: 603."""

# Test Case 2: Legitimate company (The Affordable Organic Store)
test2 = """Supply Chain Management (SCM)
The Affordable Organic Store

Actively hiring
The Affordable Organic Store
₹ 20,000 /month
Hyderabad, Kompally
6 Months
About The Affordable Organic Store
The Affordable Organic Store is committed to providing high-quality organic products.
Selected intern responsibilities: Managing inventory, Coordinating suppliers, Analyzing metrics."""

# Test Case 3: Suspicious posting (Generic, no company details)
test3 = """Make Money Fast - Work From Home!

₹ 50,000 - 100,000 /month
Remote
Immediate Start

URGENT! Limited positions available!
Complete simple tasks on your computer.
Payment required upfront: ₹5,000
No experience needed!
Click here to apply and earn money today!"""

# Test Case 4: Another legitimate (Google-like description)
test4 = """Software Engineer - Intern
Google India
Remote
Start: Immediately
Duration: 3 months
Stipend: ₹ 50,000/month

About Google:
Google is a multinational technology company specializing in search engines and cloud computing.
You will work on real projects with experienced mentors.
Requirements: Good communication skills, Problem-solving ability, Basic programming knowledge."""

test_cases = [
    ("Test 1: MastersHelp (Legitimate)", test1),
    ("Test 2: Affordable Organic Store (Legitimate)", test2),
    ("Test 3: Generic Scam (Suspicious)", test3),
    ("Test 4: Google-like (Legitimate Tech)", test4)
]

parser = InternshipInfoParser()
engine = CredibilityEngine()

for title, test_text in test_cases:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    
    # Parse
    parsed = parser.parse(test_text)
    print(f"\nPARSED DATA:")
    print(f"   Company: {parsed['companyName']}")
    salary_safe = parsed['salary'].replace('₹', 'Rs')
    print(f"   Salary: {salary_safe}")
    print(f"   Duration: {parsed['duration']}")
    print(f"   Red Flags: {parsed['redFlags'] or 'None'}")
    
    # Analyze
    result = engine.analyze({
        'parsed': parsed,
        'resumeText': ''
    })
    
    print(f"\nCREDIBILITY SCORE: {result['credibility_score']}%")
    print(f"   Level: {result['credibility_level']}")
    print(f"\nBREAKDOWN:")
    for key, value in result.get('breakdown', {}).items():
        if isinstance(value, float):
            print(f"   {key}: {value:.2f}")
        else:
            print(f"   {key}: {value}")
    
    if result.get('red_flags'):
        print(f"\nRED FLAGS:")
        for flag, details in result['red_flags'].items():
            print(f"   - {flag}: {details}")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print("\nExpected Results:")
print("  Test 1 & 2 & 4: HIGH (70-85%)")
print("  Test 3: VERY_LOW (20-40%)")
