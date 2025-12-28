# ========================
# CREDIBILITY ENGINE
# ========================

from services.url_feature_extractor import URLFeatureExtractor
from services.sentiment_analyzer import SentimentAnalyzer
from services.company_verifier import CompanyVerifier
from models.random_forest_inference import RandomForestPredictor
from preprocessing.text_cleaner import TextCleaner

class CredibilityEngine:
    """
    Purpose: Final credibility fusion
    Allowed: Weighting, explainability
    Forbidden: Flask imports, dataset access
    """
    
    def __init__(self):
        self.url_extractor = URLFeatureExtractor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.company_verifier = CompanyVerifier()
        self.rf_predictor = RandomForestPredictor()
        self.text_cleaner = TextCleaner()
    
    def analyze(self, data: dict) -> dict:
        """
        Comprehensive credibility analysis
        
        Args:
            data: Internship data from frontend
        
        Returns:
            dict: Credibility score and breakdown
        """
        try:
            scores = {}
            
            # Check for parsed internship data from new simplified form
            has_parsed_data = 'parsed' in data
            parsed = data.get('parsed', {})
            
            # Get company name for verification
            company_name = data.get('companyName') or parsed.get('companyName')
            website = data.get('companyWebsite') or parsed.get('companyWebsite')
            
            # 0. Company verification (NEW - searches online)
            if company_name:
                try:
                    company_verification = self.company_verifier.verify_company(company_name, website)
                    scores['company_verification_score'] = company_verification.get('safety_score', 0.5)
                    
                    # Store verification details for recommendations
                    verification_warnings = company_verification.get('warnings', [])
                    verification_positive = company_verification.get('positive_indicators', [])
                except Exception as e:
                    scores['company_verification_score'] = 0.5
                    verification_warnings = []
                    verification_positive = []
            else:
                scores['company_verification_score'] = 0.5
                verification_warnings = []
                verification_positive = []
            
            # 1. URL-based features
            if website:
                url_features = self.url_extractor.extract(website)
                scores['url_score'] = self._score_url_features(url_features)
            else:
                scores['url_score'] = 0.6  # Reduced penalty - website might not always be available
            
            # 2. Email domain match
            email = data.get('contactEmail') or parsed.get('contactEmail')
            if email and website:
                scores['email_match_score'] = self._score_email_match(email, website)
            else:
                scores['email_match_score'] = 0.6  # Reduced penalty
            
            # 3. Sentiment analysis of job description
            job_desc = data.get('jobDescription') or parsed.get('jobDescription')
            if job_desc:
                cleaned_text = self.text_cleaner.clean(job_desc)
                sentiment = self.sentiment_analyzer.analyze(cleaned_text)
                scores['sentiment_score'] = self._score_sentiment(sentiment)
            else:
                scores['sentiment_score'] = 0.7  # Neutral/positive for missing data
            
            # 4. Company verification - score based on parsed data quality
            verification_score = 0.0
            if has_parsed_data:
                # Score based on how much data was successfully parsed
                if parsed.get('companyName'): verification_score += 0.25
                if parsed.get('position'): verification_score += 0.25
                if parsed.get('salary'): verification_score += 0.25
                if parsed.get('duration'): verification_score += 0.25
            else:
                # Old checkbox system
                if data.get('hasLinkedIn'): verification_score += 0.3
                if data.get('hasGlassdoor'): verification_score += 0.3
                if data.get('isRegistered'): verification_score += 0.4
            
            scores['verification_score'] = verification_score
            
            # 5. Red flag detection
            red_flags = self._detect_red_flags(data, parsed)
            red_flag_penalty = min(len(red_flags) * 0.25, 1.0)  # INCREASED per-flag penalty from 0.15 to 0.25
            scores['red_flag_penalty'] = red_flag_penalty
            
            # Calculate final weighted score (NEW WEIGHTS including company verification)
            final_score = (
                scores['company_verification_score'] * 0.25 +  # Company verification
                scores['url_score'] * 0.08 +
                scores['email_match_score'] * 0.07 +
                scores['sentiment_score'] * 0.05 +
                scores['verification_score'] * 0.20 +
                (1 - red_flag_penalty) * 0.35  # INCREASED: Red flags are critical
            )
            
            # Ensure score is between 0 and 1
            final_score = max(0.0, min(1.0, final_score))
            
            # Determine credibility level
            level = self._get_credibility_level(final_score)
            
            return {
                'credibility_score': round(final_score * 100, 2),
                'credibility_level': level,
                'breakdown': scores,
                'red_flags': red_flags,
                'company_verification': {
                    'warnings': verification_warnings,
                    'positive_indicators': verification_positive
                },
                'recommendations': self._generate_recommendations(final_score, red_flags, verification_warnings)
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'credibility_score': 0,
                'credibility_level': 'ERROR'
            }
    
    def _score_url_features(self, features: dict) -> float:
        """Score URL features (0-1)"""
        if 'error' in features:
            return 0.3
        
        score = 0.5  # Base score
        
        if features.get('has_https'): score += 0.2
        if not features.get('has_ip_address'): score += 0.1
        if features.get('domain_entropy', 0) < 4.0: score += 0.1
        if features.get('num_hyphens', 0) <= 1: score += 0.05
        if features.get('num_digits', 0) <= 2: score += 0.05
        
        return min(score, 1.0)
    
    def _score_email_match(self, email: str, url: str) -> float:
        """Check if email domain matches website"""
        try:
            email_domain = email.split('@')[1].lower()
            url_domain = url.replace('http://', '').replace('https://', '')
            url_domain = url_domain.replace('www.', '').split('/')[0].lower()
            
            if email_domain in url_domain or url_domain in email_domain:
                return 1.0
            return 0.3
        except:
            return 0.5
    
    def _score_sentiment(self, sentiment: dict) -> float:
        """Convert sentiment to score"""
        if sentiment['label'] == 'POSITIVE':
            return 0.5 + (sentiment['score'] * 0.5)
        elif sentiment['label'] == 'NEGATIVE':
            return 0.5 - (sentiment['score'] * 0.5)
        return 0.5
    
    def _detect_red_flags(self, data: dict, parsed: dict = None) -> dict:
        """Detect red flags in internship offer"""
        flags = {}
        parsed = parsed or {}
        
        # Check from old checkbox system (legacy)
        if data.get('requiresPayment'):
            flags['payment_required'] = 'Requires upfront payment'
        if data.get('requestsBankDetails'):
            flags['personal_info'] = 'Requests bank/personal details'
        if data.get('noContract'):
            flags['no_contract'] = 'No written contract'
        if data.get('pressureToDecide'):
            flags['pressure'] = 'Pressure to decide quickly'
        if data.get('requestsPersonalInfo'):
            flags['personal_info'] = 'Requests excessive personal info'
        
        # Check from parsed red flags (NEW format from info_parser)
        if 'redFlags' in parsed and isinstance(parsed['redFlags'], list):
            for flag_name in parsed['redFlags']:
                flag_descriptions = {
                    'payment_required': 'Requires upfront payment',
                    'personal_info': 'Requests personal/bank details',
                    'no_contract': 'No written contract',
                    'unclear_opportunity': 'Unclear job description',
                    'unrealistic_salary': 'Unrealistic salary claims',
                    'pressure_to_decide': 'High pressure timeline',
                    'vague_communication': 'Vague communication',
                    'unprofessional': 'Unprofessional tone'
                }
                if flag_name in flag_descriptions:
                    flags[flag_name] = flag_descriptions[flag_name]
                else:
                    flags[flag_name] = flag_name  # Default to flag name itself
        
        return flags
    
    def _get_credibility_level(self, score: float) -> str:
        """Map score to credibility level"""
        if score >= 0.8: return 'HIGH'
        if score >= 0.6: return 'MODERATE'
        if score >= 0.4: return 'LOW'
        return 'VERY_LOW'
    
    def _generate_recommendations(self, score: float, red_flags: list, verification_warnings: list = None) -> list:
        """Generate actionable recommendations"""
        recommendations = []
        verification_warnings = verification_warnings or []
        
        # Add company verification warnings first
        if verification_warnings:
            recommendations.extend(verification_warnings)
        
        if score < 0.6:
            recommendations.append('Thoroughly verify company legitimacy')
            recommendations.append('Research company reviews on multiple platforms')
        
        if red_flags:
            recommendations.append('⚠️ Critical: Address all red flags before proceeding')
        
        if 'Requires payment' in red_flags:
            recommendations.append('NEVER pay for internship opportunities')
        
        if 'No written contract' in red_flags:
            recommendations.append('Request formal written contract before starting')
        
        return recommendations
