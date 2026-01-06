# ========================
# URL FEATURE EXTRACTOR
# ========================

import re
from urllib.parse import urlparse
import tldextract
from datetime import datetime

class URLFeatureExtractor:
    """
    Purpose: URL-based credibility features
    Allowed: Domain age, entropy, structure analysis
    Forbidden: API routing, model logic
    """
    
    def __init__(self):
        pass
    
    def extract(self, url: str) -> dict:
        """
        Extract all URL-based features
        
        Args:
            url: Company website URL
        
        Returns:
            dict: Extracted features
        """
        features = {}
        
        try:
            parsed = urlparse(url)
            extracted = tldextract.extract(url)
            
            # Basic features
            features['url_length'] = len(url)
            features['domain_length'] = len(extracted.domain)
            features['has_https'] = 1 if parsed.scheme == 'https' else 0
            features['has_www'] = 1 if extracted.subdomain == 'www' else 0
            
            # Domain features
            features['domain'] = extracted.domain
            features['tld'] = extracted.suffix
            features['subdomain'] = extracted.subdomain
            
            # Suspicious patterns
            features['has_ip_address'] = self._has_ip_address(url)
            features['has_at_symbol'] = 1 if '@' in url else 0
            features['has_double_slash'] = 1 if '//' in parsed.path else 0
            features['num_dots'] = url.count('.')
            features['num_hyphens'] = extracted.domain.count('-')
            features['num_underscores'] = extracted.domain.count('_')
            features['num_digits'] = sum(c.isdigit() for c in extracted.domain)
            
            # Entropy (randomness measure)
            features['domain_entropy'] = self._calculate_entropy(extracted.domain)
            
            # Path analysis
            features['path_length'] = len(parsed.path)
            features['num_path_segments'] = len([p for p in parsed.path.split('/') if p])
            
            return features
            
        except Exception as e:
            return {'error': str(e)}
    
    def _has_ip_address(self, url: str) -> int:
        """Check if URL contains IP address"""
        ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        return 1 if re.search(ip_pattern, url) else 0
    
    def _calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of text"""
        if not text:
            return 0.0
        
        import math
        from collections import Counter
        
        counts = Counter(text)
        length = len(text)
        
        entropy = 0.0
        for count in counts.values():
            prob = count / length
            entropy -= prob * math.log2(prob)
        
        return entropy
    
    def is_suspicious_url(self, url: str) -> bool:
        """
        Determine if URL shows suspicious patterns
        
        Args:
            url: URL to check
        
        Returns:
            bool: True if suspicious
        """
        features = self.extract(url)
        
        # Suspicious if:
        # - No HTTPS
        # - Has IP address
        # - High entropy domain
        # - Many hyphens or digits
        
        if not features.get('has_https', 0):
            return True
        if features.get('has_ip_address', 0):
            return True
        if features.get('domain_entropy', 0) > 4.0:
            return True
        if features.get('num_hyphens', 0) > 2:
            return True
        if features.get('num_digits', 0) > 3:
            return True
        
        return False
