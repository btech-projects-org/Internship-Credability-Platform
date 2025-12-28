#!/usr/bin/env python3
"""Quick backend health check"""
import urllib.request
import json
import time
import sys

time.sleep(2)  # Wait for server to start

try:
    response = urllib.request.urlopen('http://localhost:5000/health', timeout=5)
    data = json.loads(response.read().decode())
    print(f"✓ Backend responding: {data}")
    sys.exit(0)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
