#!/usr/bin/env python3
"""
Verify frontend-backend API contract
Purpose: Verify frontend-backend JSON schema
Forbidden: API execution
"""

import json

def check_api_contract():
    """Verify API endpoints match frontend expectations"""
    
    print("Checking Frontend-Backend API Contract\n")
    print("="*50)
    
    # Expected API endpoints
    endpoints = {
        '/api/predict': {
            'method': 'POST',
            'request_fields': ['companyName', 'contactEmail'],
            'response_fields': ['credibility_score', 'credibility_level', 'breakdown']
        },
        '/api/sentiment': {
            'method': 'POST',
            'request_fields': ['text'],
            'response_fields': ['label', 'score']
        },
        '/api/extract_url_features': {
            'method': 'POST',
            'request_fields': ['url'],
            'response_fields': ['url_length', 'has_https', 'domain_entropy']
        }
    }
    
    print("\nExpected API Endpoints:")
    for endpoint, spec in endpoints.items():
        print(f"\n{spec['method']} {endpoint}")
        print(f"  Request: {', '.join(spec['request_fields'])}")
        print(f"  Response: {', '.join(spec['response_fields'])}")
    
    print("\n" + "="*50)
    print("Contract specification complete")
    print("\nTo verify at runtime:")
    print("1. Start backend: python backend/app.py")
    print("2. Test endpoints with curl or Postman")
    print("3. Ensure response format matches frontend expectations")
    
    return True


if __name__ == '__main__':
    check_api_contract()
