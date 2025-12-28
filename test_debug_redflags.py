"""Debug red flag penalty calculation"""

import sys
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from services.info_parser import InternshipInfoParser
from services.credibility_engine import CredibilityEngine

test_scam = """Make Money Fast - Work From Home!

₹ 50,000 - 100,000 /month
Remote
Immediate Start

URGENT! Limited positions available!
Complete simple tasks on your computer.
Payment required upfront: Rs5,000
No experience needed!
Click here to apply and earn money today!"""

parser = InternshipInfoParser()
parsed = parser.parse(test_scam)

print("Parsed red flags:", parsed['redFlags'])

engine = CredibilityEngine()

# Manually check red flag detection
red_flags = engine._detect_red_flags({'parsed': parsed}, parsed)
print("Detected red flags in engine:", red_flags)
print("Number of red flags:", len(red_flags))

# Full analysis
result = engine.analyze({'parsed': parsed, 'resumeText': ''})

print("\nFinal result:")
print(f"  Score: {result['credibility_score']}%")
print(f"  Red flags from result: {result.get('red_flags', [])}")
print(f"  Breakdown red_flag_penalty: {result['breakdown'].get('red_flag_penalty', 'N/A')}")
