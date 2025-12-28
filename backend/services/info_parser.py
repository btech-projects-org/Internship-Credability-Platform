# ========================
# INTERNSHIP INFORMATION PARSER
# ========================

import re
from typing import Dict, Any

class InternshipInfoParser:
    """
    Parses raw internship information text and extracts structured data.
    Uses NLP patterns and keyword matching to identify key information.
    """
    
    def __init__(self):
        self.patterns = {
            'email': r'[\w\.-]+@[\w\.-]+\.\w+',
            'url': r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)',
            'phone': r'\+?1?\d{9,15}',
            'currency': r'(?:Rs|₹|\$|€|£)\s*[\d,]+(?:\.\d{2})?',
        }
    
    def parse(self, raw_text: str) -> Dict[str, Any]:
        """
        Parse raw internship information and return structured data.
        
        Args:
            raw_text (str): Raw internship information provided by user
            
        Returns:
            Dict: Structured information with extracted fields
        """
        # Extract company name
        company_name = self._extract_company_name(raw_text)
        print(f"[DEBUG] Extracted company name: '{company_name}'")  # Debug logging
        
        parsed_data = {
            'companyName': company_name,
            'companyWebsite': self._extract_website(raw_text),
            'contactEmail': self._extract_email(raw_text),
            'position': self._extract_position(raw_text),
            'salary': self._extract_salary(raw_text),
            'duration': self._extract_duration(raw_text),
            'workType': self._extract_work_type(raw_text),
            'redFlags': self._extract_red_flags(raw_text),
            'jobDescription': raw_text,  # Store full text as job description for analysis
            'rawText': raw_text
        }
        
        return parsed_data
    
    def _extract_company_name(self, text: str) -> str:
        """Extract company name from text - intelligent detection"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return "Unknown Company"
        
        # Strategy 1: Look for explicit company/organization keywords
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ['company:', 'organization:', 'firm:', 'employer:']):
                # Extract text after the keyword
                parts = re.split(r'[:–-]', line, 1)
                if len(parts) > 1:
                    extracted = parts[1].strip()
                    if extracted:
                        return extracted
        
        # Strategy 2: Check for lines that appear multiple times (strong indicator)
        # Company names are often repeated multiple times in job postings
        text_lower = text.lower()
        repeated_candidates = []
        
        for line in lines[:15]:  # Check first 15 lines
            # Skip common non-company patterns
            if re.match(r'^(about|start date|duration|stipend|salary|position|role|internship|location|apply|actively|hiring)', line, re.IGNORECASE):
                continue
            
            # Skip very short lines
            if len(line) < 3:
                continue
            
            # Skip purely numeric lines
            if re.match(r'^[\d\s,/-]+$', line):
                continue
            
            # Skip lines with lots of currency/numbers
            if re.search(r'[₹$€£]\s*[\d,]+|per\s+month|per\s+annum', line, re.IGNORECASE):
                continue
            
            # Count occurrences (case-insensitive)
            occurrences = text_lower.count(line.lower())
            
            # If appears 2+ times, it's likely the company name
            if occurrences >= 2:
                repeated_candidates.append((line, occurrences))
        
        if repeated_candidates:
            # Sort by frequency (descending)
            repeated_candidates.sort(key=lambda x: -x[1])
            return repeated_candidates[0][0]
        
        # Strategy 3: Look for lines with business indicators
        for line in lines[:12]:
            # Skip common patterns
            if re.match(r'^(about|start date|duration|stipend|salary|position|role|internship|location|apply|actively|hiring)', line, re.IGNORECASE):
                continue
            
            word_count = len(line.split())
            
            # 1-3 word proper-cased names are good candidates
            if 1 <= word_count <= 3:
                # Check if properly capitalized (good indicator of company name)
                if any(word[0].isupper() for word in line.split()):
                    # Not pure lowercase
                    if line != line.lower():
                        return line
        
        # Strategy 4: Look for "About [Company]" section
        for line in lines:
            match = re.match(r'^about\s+(?:the\s+)?(.+?)(?:\s*:|$)', line, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                if company and len(company) > 2:
                    return company
        
        # Strategy 5: First line that looks like a proper name
        for line in lines[:5]:
            # Must be capitalized and not a label
            if line[0].isupper() and not re.match(r'^(role|position|location|duration|stipend):', line, re.IGNORECASE):
                if len(line) > 2:
                    return line
        
        # Final fallback: first substantial line
        for line in lines:
            if len(line) > 5 and not line.isdigit():
                return line
        
        return "Unknown Company"
    
    def _extract_website(self, text: str) -> str:
        """Extract website URL from text"""
        urls = re.findall(self.patterns['url'], text)
        if urls:
            return urls[0]
        return ""
    
    def _extract_email(self, text: str) -> str:
        """Extract email address from text"""
        emails = re.findall(self.patterns['email'], text)
        if emails:
            return emails[0]
        return ""
    
    def _extract_position(self, text: str) -> str:
        """Extract job position from text"""
        text_lower = text.lower()
        
        # Look for position-related keywords
        position_keywords = ['position', 'role', 'designation', 'title', 'job', 'internship']
        
        for keyword in position_keywords:
            pattern = rf'{keyword}[:\s\-–]+([^\n]+)'
            match = re.search(pattern, text_lower)
            if match:
                # Extract from original text to preserve case
                idx = text.lower().find(match.group(1))
                return text[idx:idx+len(match.group(1))].strip()
        
        # Look for common position titles
        position_patterns = [
            r'([\w\s]+(?:developer|engineer|analyst|designer|manager|coordinator|executive|trainee|associate))',
        ]
        
        for pattern in position_patterns:
            match = re.search(pattern, text_lower)
            if match:
                idx = text.lower().find(match.group(1))
                return text[idx:idx+len(match.group(1))].strip()
        
        return ""
    
    def _extract_salary(self, text: str) -> str:
        """Extract salary/stipend information from text"""
        text_lower = text.lower()
        
        # Look for salary keywords
        salary_keywords = ['salary', 'stipend', 'compensation', 'remuneration', 'payment', 'per month', 'pm', 'per annum', 'pa']
        
        for keyword in salary_keywords:
            pattern = rf'{keyword}[:\s\-–]+([\w\s₹$€£,\.]+)'
            match = re.search(pattern, text_lower)
            if match:
                idx = text.lower().find(match.group(1))
                salary_text = text[idx:idx+len(match.group(1))].strip()
                if salary_text:
                    return salary_text
        
        # Look for currency amounts
        currencies = re.findall(self.patterns['currency'], text)
        if currencies:
            return currencies[0]
        
        return ""
    
    def _extract_duration(self, text: str) -> str:
        """Extract internship duration from text"""
        text_lower = text.lower()
        
        # Look for duration keywords
        duration_pattern = r'(\d+\s*(?:weeks?|months?|years?))'
        matches = re.findall(duration_pattern, text_lower)
        if matches:
            return matches[0]
        
        # Look for specific phrases
        duration_keywords = ['duration', 'period', 'length', 'timeline']
        for keyword in duration_keywords:
            pattern = rf'{keyword}[:\s\-–]+([^\n]+)'
            match = re.search(pattern, text_lower)
            if match:
                idx = text.lower().find(match.group(1))
                return text[idx:idx+len(match.group(1))].strip()
        
        return ""
    
    def _extract_work_type(self, text: str) -> str:
        """Extract work type (remote, hybrid, onsite) from text"""
        text_lower = text.lower()
        
        work_types = {
            'remote': ['remote', 'work from home', 'wfh', 'online'],
            'hybrid': ['hybrid', 'mixed', 'flexible'],
            'onsite': ['onsite', 'office', 'in-office', 'on-site']
        }
        
        for work_type, keywords in work_types.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return work_type
        
        return ""
    
    def _extract_red_flags(self, text: str) -> list:
        """Extract potential red flags from the text"""
        red_flags = []
        text_lower = text.lower()
        
        # Red flag patterns - more specific to avoid false positives
        # Use regex with word boundaries to avoid matching legitimate phrases
        suspicious_patterns = {
            'payment_required': [
                r'\brequires\s+payment\b',
                r'registration\s+fee',
                r'upfront\s+(?:cost|payment|fee)',
                r'pay\s+to\s+(?:apply|join|start)',
                r'deposit\s+required',
                r'upfront\s+investment',
                r'₹\s*\d+\s*(?:fee|cost|payment)'
            ],
            'personal_info': [
                r'bank\s+(?:account|details)',
                r'aadhar',
                r'\bpan\b',
                r'passport',
                r'ssn',
                r'credit\s+card'
            ],
            'unrealistic_salary': [
                r'earn\s+(?:fast|quick|money)',
                r'quick\s+(?:money|cash|earnings)',
                r'passive\s+income',
                r'make\s+money\s+fast',
                r'guaranteed\s+(?:income|earnings)',
                r'\b(?:50000|100000|unlimited)\s+(?:per\s+month|monthly)\b'
            ],
            'pressure_to_decide': [
                r'(?:only|just|just\s+)\d+\s+(?:spots|positions|seats)\s+(?:left|available)',
                r'(?:immediate|urgent)\s+(?:decision|action|hiring)',
                r'decide\s+(?:now|today|immediately)',
                r'(?:limited|urgent)\s+(?:opportunity|positions)'
            ],
            'vague_communication': [
                r'(?:no\s+)?(?:experience|skills?)\s+(?:required|needed)',
                r'simple\s+tasks',
                r'work\s+from\s+(?:home|anywhere)',
                r'(?:complete|just)\s+(?:simple|easy)\s+tasks'
            ],
            'no_contract': [
                r'(?:no|without)\s+(?:written\s+)?contract',
                r'verbal\s+agreement\s+(?:only)?',
                r'informal\s+arrangement',
            ],
            'unprofessional': [
                r'!!+',  # Multiple exclamation marks
                r'\bclick\s+here\b',
                r'apply\s+(?:now|today|here)',
            ]
        }
        
        for flag_type, patterns in suspicious_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    red_flags.append(flag_type)
                    break
        
        return list(set(red_flags))  # Remove duplicates
