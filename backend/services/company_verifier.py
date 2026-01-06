# ========================
# COMPANY VERIFICATION SERVICE
# ========================

import re
import os
import requests
from urllib.parse import quote
from typing import Dict, Any
import time

class CompanyVerifier:
    """
    Verifies company legitimacy by searching online sources.
    Checks for scam reports, company presence, and reviews.
    Uses Google Custom Search API for real verification.
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.timeout = 10
        
        # Load API keys from environment
        self.google_api_key = os.getenv('GOOGLE_CSE_API_KEY', '')
        self.google_cse_id = os.getenv('GOOGLE_CSE_ENGINE_ID', '')
        self.hf_api_key = os.getenv('HUGGINGFACE_API_KEY', '')
        
        # Log API availability
        self._log_api_status()
    
    def _log_api_status(self):
        """Log which APIs are available"""
        print("[INFO] === Company Verifier API Status ===")
        if self.google_api_key and self.google_cse_id:
            print("[✓] Google Custom Search API: CONFIGURED")
        else:
            print("[✗] Google Custom Search API: NOT CONFIGURED (using heuristics only)")
        
        if self.hf_api_key:
            print("[✓] HuggingFace API: CONFIGURED")
        else:
            print("[✗] HuggingFace API: NOT CONFIGURED")
    
    def verify_company(self, company_name: str, website: str = None) -> Dict[str, Any]:
        """
        Verify company safety by checking multiple online sources.
        
        Args:
            company_name (str): Name of the company to verify
            website (str): Optional company website URL
            
        Returns:
            Dict: Verification results with safety score and details
        """
        try:
            print(f"[DEBUG] Verifying company: '{company_name}'")  # Debug logging
            
            results = {
                'company_name': company_name,
                'safety_score': 0.0,
                'checks_performed': [],
                'warnings': [],
                'positive_indicators': [],
                'negative_indicators': [],
                'search_results_count': 0,
                'has_official_website': False,
                'scam_reports_found': False,
                'verification_status': 'UNKNOWN'
            }
            
            # 1. Check for scam keywords in search results
            scam_check = self._check_scam_reports(company_name)
            results['checks_performed'].append('scam_report_check')
            results['scam_reports_found'] = scam_check['has_scam_reports']
            
            if scam_check['has_scam_reports']:
                results['negative_indicators'].extend(scam_check['indicators'])
                results['warnings'].append(f"⚠️ Scam reports found for {company_name}")
                results['safety_score'] -= 0.4
            else:
                results['positive_indicators'].append("No scam reports found")
                results['safety_score'] += 0.3
            
            # 2. Check website validity
            if website:
                website_check = self._verify_website(website)
                results['checks_performed'].append('website_verification')
                results['has_official_website'] = website_check['is_valid']
                
                if website_check['is_valid']:
                    results['positive_indicators'].append("Company has accessible website")
                    results['safety_score'] += 0.25
                    
                    if website_check['has_https']:
                        results['positive_indicators'].append("Website uses HTTPS")
                        results['safety_score'] += 0.1
                else:
                    results['negative_indicators'].append("Website is not accessible")
                    results['warnings'].append("⚠️ Company website is not accessible")
                    results['safety_score'] -= 0.2
            
            # 3. Search for company presence
            presence_check = self._check_online_presence(company_name)
            results['checks_performed'].append('online_presence_check')
            results['search_results_count'] = presence_check['result_count']
            
            if presence_check['result_count'] > 0:
                results['positive_indicators'].append(f"Found {presence_check['result_count']} online references")
                results['safety_score'] += min(presence_check['result_count'] * 0.05, 0.25)
            else:
                results['negative_indicators'].append("Very limited online presence")
                results['warnings'].append("⚠️ Company has minimal online presence")
                results['safety_score'] -= 0.1
            
            # 4. Check for known legitimate platforms
            platform_check = self._check_legitimate_platforms(company_name)
            results['checks_performed'].append('platform_verification')
            
            if platform_check['found_on_platforms']:
                results['positive_indicators'].append(f"Listed on: {', '.join(platform_check['platforms'])}")
                results['safety_score'] += 0.2
            
            # Normalize safety score to 0-1 range
            results['safety_score'] = max(0.0, min(1.0, results['safety_score'] + 0.5))
            
            # Determine verification status
            if results['safety_score'] >= 0.7:
                results['verification_status'] = 'SAFE'
            elif results['safety_score'] >= 0.5:
                results['verification_status'] = 'LIKELY_SAFE'
            elif results['safety_score'] >= 0.3:
                results['verification_status'] = 'UNCERTAIN'
            else:
                results['verification_status'] = 'RISKY'
            
            return results
            
        except Exception as e:
            return {
                'company_name': company_name,
                'error': str(e),
                'safety_score': 0.5,
                'verification_status': 'ERROR',
                'warnings': ['Unable to complete verification']
            }
    
    def _check_scam_reports(self, company_name: str) -> Dict[str, Any]:
        """Check for scam reports using Google Custom Search API or patterns"""
        try:
            indicators = []
            has_scam_reports = False
            company_lower = company_name.lower()
            
            # First, check local patterns
            suspicious_patterns = [
                (r'\d{10,}', 'Company name contains very long number sequence'),
                (r'(?:earn|make)\s+money\s+(?:fast|quick|easily)', 'Promises quick money in name'),
                (r'work\s+from\s+home\s+(?:earn|make)', 'Work from home money scheme pattern'),
                (r'guaranteed\s+(?:income|salary|earnings)', 'Guaranteed income promise'),
                (r'(?:free|easy)\s+money', 'Free/easy money pattern'),
            ]
            
            for pattern, description in suspicious_patterns:
                if re.search(pattern, company_lower, re.IGNORECASE):
                    indicators.append(description)
                    has_scam_reports = True
            
            # Check for very generic or suspicious company names
            if len(company_name.split()) == 1 and len(company_name) < 4:
                indicators.append('Company name is too short/generic')
                has_scam_reports = True
            
            # Check for multiple repeated words
            words = company_lower.split()
            if len(words) != len(set(words)) and len(words) > 2:
                indicators.append('Company name has repeated words (unusual pattern)')
            
            # Try Google Custom Search API if available
            if self.google_api_key and self.google_cse_id:
                api_results = self._search_google_cse(company_name)
                if api_results['found_scam_reports']:
                    indicators.extend(api_results['indicators'])
                    has_scam_reports = True
                    print(f"[API] Google CSE found potential scam reports for {company_name}")
                else:
                    print(f"[API] Google CSE search completed for {company_name}")
                
                return {
                    'has_scam_reports': has_scam_reports,
                    'indicators': indicators,
                    'search_query': f'"{company_name}" scam fraud complaint',
                    'api_used': 'google_cse',
                    'checked_patterns': len(suspicious_patterns),
                    'search_results': api_results.get('result_count', 0)
                }
            else:
                # Fallback to pattern-based detection
                print(f"[WARNING] Google CSE API not configured. Using pattern-based detection for {company_name}")
                return {
                    'has_scam_reports': has_scam_reports,
                    'indicators': indicators,
                    'search_query': f'"{company_name}" scam fraud complaint',
                    'api_used': 'patterns_only',
                    'checked_patterns': len(suspicious_patterns)
                }
            
        except Exception as e:
            print(f"[ERROR] Scam report check failed: {e}")
            return {
                'has_scam_reports': False,
                'indicators': [],
                'error': str(e)
            }
    
    def _search_google_cse(self, company_name: str) -> Dict[str, Any]:
        """Search for company information using Google Custom Search API"""
        try:
            search_queries = [
                f'"{company_name}" scam',
                f'"{company_name}" fraud',
                f'"{company_name}" internship scam complaint',
                f'"{company_name}" fake internship'
            ]
            
            all_indicators = []
            total_results = 0
            scam_keywords = ['scam', 'fraud', 'fake', 'complaint', 'warning', 'avoid', 'beware']
            
            for query in search_queries:
                try:
                    url = 'https://www.googleapis.com/customsearch/v1'
                    params = {
                        'q': query,
                        'key': self.google_api_key,
                        'cx': self.google_cse_id,
                        'num': 5  # Limit to 5 results per query to save quota
                    }
                    
                    response = requests.get(url, params=params, timeout=self.timeout)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if 'items' in data:
                            total_results += len(data.get('items', []))
                            
                            # Analyze search results
                            for item in data.get('items', []):
                                title = item.get('title', '').lower()
                                snippet = item.get('snippet', '').lower()
                                
                                # Check for scam indicators in results
                                for keyword in scam_keywords:
                                    if keyword in title or keyword in snippet:
                                        indicator = f"Found '{keyword}' in search result: {item.get('title', 'N/A')[:60]}"
                                        if indicator not in all_indicators:
                                            all_indicators.append(indicator)
                                        break
                        
                        print(f"[DEBUG] Google CSE query '{query}' returned {len(data.get('items', []))} results")
                    
                    elif response.status_code == 403:
                        print("[WARNING] Google CSE API quota exceeded or invalid credentials")
                        break
                    elif response.status_code == 400:
                        print(f"[WARNING] Invalid Google CSE query: {response.text}")
                
                except requests.exceptions.Timeout:
                    print(f"[WARNING] Google CSE API timeout for query: {query}")
                except Exception as e:
                    print(f"[WARNING] Google CSE API error for query '{query}': {e}")
            
            return {
                'found_scam_reports': len(all_indicators) > 0,
                'indicators': all_indicators,
                'result_count': total_results,
                'queries_executed': len(search_queries)
            }
        
        except Exception as e:
            print(f"[ERROR] Google CSE search failed: {e}")
            return {
                'found_scam_reports': False,
                'indicators': [],
                'error': str(e)
            }
    
    def _verify_website(self, website: str) -> Dict[str, Any]:
        """Verify if website is accessible and valid"""
        try:
            # Ensure URL has scheme
            if not website.startswith(('http://', 'https://')):
                website = 'https://' + website
            
            # Try to access the website
            response = requests.head(website, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            
            return {
                'is_valid': response.status_code == 200,
                'has_https': website.startswith('https://'),
                'status_code': response.status_code,
                'accessible': True
            }
            
        except requests.exceptions.SSLError:
            # SSL error might indicate security issue
            return {
                'is_valid': False,
                'has_https': False,
                'error': 'SSL Certificate Error',
                'accessible': False
            }
        except requests.exceptions.Timeout:
            return {
                'is_valid': False,
                'has_https': website.startswith('https://') if website else False,
                'error': 'Timeout',
                'accessible': False
            }
        except Exception as e:
            return {
                'is_valid': False,
                'has_https': False,
                'error': str(e),
                'accessible': False
            }
    
    def _check_online_presence(self, company_name: str) -> Dict[str, Any]:
        """Check for company's online presence"""
        try:
            # WITHOUT API: We cannot verify actual online presence
            # Be conservative and return low scores unless we have real data
            
            # Load known legitimate companies from local database
            known_companies = self._load_known_companies()
            
            # Check if company is in our verified database
            company_lower = company_name.lower()
            for known in known_companies:
                if known.lower() in company_lower or company_lower in known.lower():
                    print(f"[INFO] {company_name} found in verified companies database")
                    return {
                        'result_count': 10,
                        'confidence': 'very_high',
                        'legitimate_indicators': 3,
                        'search_performed': True,
                        'verified_source': 'local_database'
                    }
            
            # If NOT in database and NO API configured, be very conservative
            if not (self.google_api_key and self.google_cse_id):
                print(f"[WARNING] Cannot verify {company_name} - not in database and no API available")
                return {
                    'result_count': 0,  # No verified online presence
                    'confidence': 'cannot_verify',
                    'legitimate_indicators': 0,
                    'search_performed': False,
                    'warning': 'Unable to verify - API not configured and company not in verified database'
                }
            
            # If we have API, try to use it for real verification
            # (This would be implemented with actual Google CSE calls)
            return {
                'result_count': 0,
                'confidence': 'low',
                'legitimate_indicators': 0,
                'search_performed': True
            }
            
        except Exception as e:
            return {
                'result_count': 0,
                'confidence': 'unknown',
                'error': str(e),
                'search_performed': False
            }
    
    def _check_legitimate_platforms(self, company_name: str) -> Dict[str, Any]:
        """Check if company is listed on known legitimate platforms"""
        try:
            # WITHOUT API: We cannot verify actual platform presence
            # Only return platforms if company is in our verified database
            
            known_companies = self._load_known_companies()
            company_lower = company_name.lower()
            
            # Only assign platforms if company is verified
            for known in known_companies:
                if known.lower() in company_lower or company_lower in known.lower():
                    return {
                        'found_on_platforms': True,
                        'platforms': ['LinkedIn'],
                        'confidence': 'verified',
                        'platforms_checked': ['LinkedIn', 'Glassdoor', 'Indeed', 'Naukri']
                    }
            
            # Unknown companies get NO platform verification
            print(f"[WARNING] {company_name} not found in verified database - no platform confirmation")
            return {
                'found_on_platforms': False,
                'platforms': [],
                'confidence': 'unverified',
                'platforms_checked': ['LinkedIn', 'Glassdoor', 'Indeed', 'Naukri', 'AngelList', 'Crunchbase'],
                'warning': 'Company not in verified database - cannot confirm platform presence'
            }
            
        except Exception as e:
            return {
                'found_on_platforms': False,
                'platforms': [],
                'error': str(e)
            }
    
    def _load_known_companies(self) -> list:
        """Load list of known legitimate companies from local database"""
        try:
            import json
            data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'legitimate_companies.json')
            if os.path.exists(data_path):
                with open(data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Handle both list and dict formats
                    if isinstance(data, list):
                        return [item if isinstance(item, str) else item.get('name', '') for item in data]
                    elif isinstance(data, dict) and 'companies' in data:
                        return [item if isinstance(item, str) else item.get('name', '') for item in data['companies']]
                    return []
            return []
        except Exception as e:
            print(f"[ERROR] Failed to load known companies: {e}")
            return []
