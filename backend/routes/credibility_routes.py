# ========================
# CREDIBILITY PREDICTION ROUTES
# ========================

from flask import Blueprint, request, jsonify
from services.credibility_engine import CredibilityEngine
from services.url_feature_extractor import URLFeatureExtractor
from services.info_parser import InternshipInfoParser
from services.company_verifier import CompanyVerifier
from services.company_search import CompanySearcher
import re

credibility_bp = Blueprint('credibility', __name__)
engine = None
url_extractor = None
info_parser = None
company_verifier = None
company_searcher = None

def _ensure_initialized():
    """Lazy initialize services on first request"""
    global engine, url_extractor, info_parser, company_verifier, company_searcher
    if engine is None:
        engine = CredibilityEngine()
    if url_extractor is None:
        url_extractor = URLFeatureExtractor()
    if info_parser is None:
        info_parser = InternshipInfoParser()
    if company_verifier is None:
        company_verifier = CompanyVerifier()
    if company_searcher is None:
        company_searcher = CompanySearcher()


@credibility_bp.route('/find_company_website', methods=['POST'])
def find_company_website():
    """
    Endpoint: /api/find_company_website
    Purpose: Find likely official website for a company using Google CSE
    Input: companyName (required)
    Output: best-guess website URL
    """
    _ensure_initialized()
    try:
        data = request.get_json()
        if not data or 'companyName' not in data:
            return jsonify({'error': 'Missing companyName field'}), 400

        company_name = data['companyName']
        if not company_name or not str(company_name).strip():
            return jsonify({'error': 'Company name cannot be empty'}), 400

        website = company_searcher.search_company(company_name)

        if not website:
            return jsonify({'success': False, 'message': 'No website found'}), 200

        return jsonify({'success': True, 'website': website}), 200

    except Exception as e:
        return jsonify({'error': f'Failed to find company website: {str(e)}'}), 500

@credibility_bp.route('/parse_internship_info', methods=['POST'])
def parse_internship_info():
    """
    Endpoint: /api/parse_internship_info
    Purpose: Parse raw internship information and extract structured data
    Input: rawInternshipInfo (raw text)
    Output: Structured internship data (company name, email, position, salary, red flags, etc.)
    """
    _ensure_initialized()
    try:
        data = request.get_json()
        
        # Validate input exists
        if 'rawInternshipInfo' not in data:
            return jsonify({'error': 'Missing rawInternshipInfo field'}), 400
        
        raw_text = data['rawInternshipInfo']
        
        # Allow any non-empty input - parser will extract what it can
        if not raw_text or not str(raw_text).strip():
            return jsonify({'error': 'Please provide internship information'}), 400
        
        # Parse the raw information (parser returns empty fields if nothing found)
        parsed_data = info_parser.parse(raw_text)
        
        return jsonify({
            'success': True,
            'parsed': parsed_data,
            'message': 'Information parsed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to parse internship info: {str(e)}'}), 500

@credibility_bp.route('/verify_company', methods=['POST'])
def verify_company():
    """
    Endpoint: /api/verify_company
    Purpose: Verify company safety by searching online
    Input: companyName (required), website (optional)
    Output: Safety score, warnings, indicators, verification status
    """
    _ensure_initialized()
    try:
        data = request.get_json()
        
        # Validate input exists
        if 'companyName' not in data:
            return jsonify({'error': 'Missing companyName field'}), 400
        
        company_name = data['companyName']
        
        if not company_name or not str(company_name).strip():
            return jsonify({'error': 'Company name cannot be empty'}), 400
        
        website = data.get('website', data.get('companyWebsite', None))
        
        # Verify the company
        verification_result = company_verifier.verify_company(company_name, website)
        
        return jsonify({
            'success': True,
            'verification': verification_result,
            'message': 'Company verification completed'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to verify company: {str(e)}'}), 500

@credibility_bp.route('/predict', methods=['POST'])
def predict_credibility():
    """
    Endpoint: /api/predict
    Purpose: Predict internship credibility
    Allowed: Input validation, service calls
    Forbidden: Feature extraction, model logic
    """
    _ensure_initialized()
    try:
        data = request.get_json()
        
        print(f"\n[DEBUG] === PREDICT ENDPOINT ===")
        print(f"[DEBUG] Received keys: {list(data.keys())}")
        
        # Ensure jobDescription is populated
        if not data.get('jobDescription') and data.get('rawInternshipInfo'):
            print(f"[DEBUG] No jobDescription, using rawInternshipInfo")
            data['jobDescription'] = data['rawInternshipInfo']
        
        job_desc_len = len(data.get('jobDescription', ''))
        print(f"[DEBUG] jobDescription length: {job_desc_len}")
        
        # Pass data directly to engine for analysis
        # Engine will return 0% if any critical fields are missing
        
        # Delegate to credibility engine
        result = engine.analyze(data)
        
        print(f"[DEBUG] === BEFORE JSONIFY ===")
        print(f"[DEBUG] Result keys: {list(result.keys())}")
        print(f"[DEBUG] Breakdown keys: {list(result.get('breakdown', {}).keys())}")
        print(f"[DEBUG] offer_quality_score in result['breakdown']: {'offer_quality_score' in result.get('breakdown', {})}")
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        return jsonify({'error': str(e)}), 500


@credibility_bp.route('/extract_url_features', methods=['POST'])
def extract_url_features():
    """
    Endpoint: /api/extract_url_features
    Purpose: Extract URL-based features
    Allowed: URL validation, feature delegation
    Forbidden: Feature computation logic
    """
    try:
        data = request.get_json()
        
        if 'url' not in data:
            return jsonify({'error': 'Missing URL'}), 400
        
        features = url_extractor.extract(data['url'])
        
        return jsonify(features), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@credibility_bp.route('/debug_sentiment', methods=['POST'])
def debug_sentiment():
    """Debug endpoint to trace sentiment calculation"""
    _ensure_initialized()
    try:
        data = request.get_json()
        job_desc = data.get('jobDescription', '')
        
        print(f"\n[DEBUG] === SENTIMENT DEBUG ===")
        print(f"[DEBUG] Job desc length: {len(job_desc)}")
        print(f"[DEBUG] Job desc preview: {job_desc[:100]}...")
        
        # Clean text
        cleaned = engine.text_cleaner.clean(job_desc)
        print(f"[DEBUG] Cleaned length: {len(cleaned)}")
        print(f"[DEBUG] Cleaned preview: {cleaned[:100]}...")
        
        # Analyze sentiment
        sentiment = engine.sentiment_analyzer.analyze(cleaned)
        print(f"[DEBUG] Sentiment result: {sentiment}")
        
        # Score it
        sentiment_score = engine._score_sentiment(sentiment)
        print(f"[DEBUG] Sentiment score (0-1): {sentiment_score}")
        print(f"[DEBUG] Display (%): {sentiment_score * 100}%")
        
        return jsonify({
            'jobDescLength': len(job_desc),
            'cleanedLength': len(cleaned),
            'sentiment': sentiment,
            'sentimentScore': sentiment_score,
            'displayPercent': round(sentiment_score * 100, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
def test_sentiment():
    """Test endpoint to check sentiment analysis"""
    _ensure_initialized()
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        from services.sentiment_analyzer import SentimentAnalyzer
        from preprocessing.text_cleaner import TextCleaner
        
        analyzer = SentimentAnalyzer()
        cleaner = TextCleaner()
        
        cleaned = cleaner.clean(text)
        sentiment = analyzer.analyze(cleaned)
        
        # Calculate score like in credibility engine
        if 'error' in sentiment or 'label' not in sentiment:
            score = 0.6
        elif sentiment['label'] == 'POSITIVE':
            score = 0.5 + (sentiment['score'] * 0.5)
        elif sentiment['label'] == 'NEGATIVE':
            score = max(0.0, 0.5 - (sentiment['score'] * 0.5))
        else:
            score = 0.6
        
        return jsonify({
            'original_length': len(text),
            'cleaned_text': cleaned,
            'cleaned_length': len(cleaned),
            'sentiment': sentiment,
            'calculated_score': score,
            'display_percentage': round(score * 100, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
