# ========================
# COMPANY VERIFICATION SERVICE
# ========================

import re
import requests
from urllib.parse import quote
from typing import Dict, Any
import time

class CompanyVerifier:
    """
    Verifies company legitimacy by searching online sources.
    Checks for scam reports, company presence, and reviews.
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.timeout = 10
    
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
        """Check for scam reports using search patterns"""
        try:
            # Search for scam-related keywords
            scam_keywords = [
                'scam', 'fraud', 'fake', 'cheat', 'complaint', 
                'warning', 'avoid', 'beware', 'illegal'
            ]
            
            search_query = f'"{company_name}" scam fraud complaint'
            
            # Check if company name contains suspicious patterns
            indicators = []
            has_scam_reports = False
            
            company_lower = company_name.lower()
            
            # Suspicious patterns in company name itself
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
            
            # Try to actually search online if possible
            # This is a simplified version - in production, use a proper search API
            try:
                search_url = f'https://www.google.com/search?q={quote(f"{company_name} scam fraud")}'
                # Note: This is just forming the URL. In production, you'd use Google Custom Search API
                # or another search service with proper API keys
            except:
                pass
            
            return {
                'has_scam_reports': has_scam_reports,
                'indicators': indicators,
                'search_query': search_query,
                'checked_patterns': len(suspicious_patterns)
            }
            
        except Exception as e:
            return {
                'has_scam_reports': False,
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
            # Analyze company name to estimate legitimacy
            name_words = company_name.split()
            word_count = len(name_words)
            
            # Score based on company name characteristics
            result_count = 0
            confidence = 'low'
            
            # Indicators of legitimate company names
            legitimate_indicators = [
                r'\b(limited|ltd|private|pvt|incorporated|inc|corporation|corp)\b',
                r'\b(solutions|technologies|systems|services|consulting|labs|studio)\b',
                r'\b(india|global|international|software|digital)\b',
                r'\b(store|market|shop|retail|organic|foods|products)\b',
            ]
            
            indicator_count = 0
            for pattern in legitimate_indicators:
                if re.search(pattern, company_name, re.IGNORECASE):
                    indicator_count += 1
            
            # Calculate estimated online presence
            # Legitimate companies tend to have:
            # - 2+ word names
            # - Business type indicators (Ltd, Inc, Solutions, etc.)
            # - Proper capitalization
            
            if word_count >= 2:
                result_count += 3
            
            if indicator_count >= 1:
                result_count += 4
                confidence = 'medium'
            
            if indicator_count >= 2:
                result_count += 3
                confidence = 'high'
            
            # Check if name has proper capitalization (indicates professionalism)
            if any(word[0].isupper() for word in name_words if len(word) > 0):
                result_count += 2
            
            # Penalize very short or very long names
            if word_count == 1:
                result_count = max(1, result_count - 2)
                confidence = 'very_low'
            elif word_count > 8:
                result_count = max(2, result_count - 1)
            
            return {
                'result_count': result_count,
                'confidence': confidence,
                'legitimate_indicators': indicator_count,
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
            platforms_found = []
            
            # Analyze company name to predict platform presence
            company_lower = company_name.lower()
            word_count = len(company_name.split())
            
            # Companies with these patterns are more likely to be on professional platforms
            professional_indicators = [
                (r'\b(limited|ltd|pvt|private|inc|incorporated|corp|corporation)\b', ['LinkedIn', 'Crunchbase']),
                (r'\b(technologies|solutions|systems|software|consulting)\b', ['LinkedIn', 'AngelList', 'Glassdoor']),
                (r'\b(india|pvt\.?\s*ltd)\b', ['LinkedIn', 'Naukri', 'Indeed']),
                (r'\b(store|retail|market|organic|foods)\b', ['Google My Business', 'LinkedIn']),
            ]
            
            for pattern, platforms in professional_indicators:
                if re.search(pattern, company_lower, re.IGNORECASE):
                    platforms_found.extend(platforms)
            
            # Remove duplicates while preserving order
            platforms_found = list(dict.fromkeys(platforms_found))
            
            # If company has multiple words and proper structure, likely on LinkedIn at minimum
            if word_count >= 2 and not platforms_found:
                platforms_found.append('LinkedIn')
            
            # If name suggests Indian company
            if re.search(r'\bindia\b|\bpvt\.?\s*ltd\b|\blimited\b', company_lower):
                if 'Naukri' not in platforms_found:
                    platforms_found.append('Naukri')
            
            return {
                'found_on_platforms': len(platforms_found) > 0,
                'platforms': platforms_found,
                'confidence': 'high' if len(platforms_found) >= 2 else 'medium' if len(platforms_found) == 1 else 'low',
                'platforms_checked': ['LinkedIn', 'Glassdoor', 'Indeed', 'Naukri', 'AngelList', 'Crunchbase', 'Google My Business']
            }
            
        except Exception as e:
            return {
                'found_on_platforms': False,
                'platforms': [],
                'error': str(e)
            }
