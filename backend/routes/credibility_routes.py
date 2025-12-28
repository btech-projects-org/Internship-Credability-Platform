# ========================
# CREDIBILITY PREDICTION ROUTES
# ========================

from flask import Blueprint, request, jsonify
from services.credibility_engine import CredibilityEngine
from services.url_feature_extractor import URLFeatureExtractor
from services.info_parser import InternshipInfoParser
from services.company_verifier import CompanyVerifier

credibility_bp = Blueprint('credibility', __name__)
engine = None
url_extractor = None
info_parser = None
company_verifier = None

def _ensure_initialized():
    """Lazy initialize services on first request"""
    global engine, url_extractor, info_parser, company_verifier
    if engine is None:
        engine = CredibilityEngine()
    if url_extractor is None:
        url_extractor = URLFeatureExtractor()
    if info_parser is None:
        info_parser = InternshipInfoParser()
    if company_verifier is None:
        company_verifier = CompanyVerifier()

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
        
        # Validate input
        if 'rawInternshipInfo' not in data or not data['rawInternshipInfo'].strip():
            return jsonify({'error': 'Missing or empty rawInternshipInfo field'}), 400
        
        # Parse the raw information
        raw_text = data['rawInternshipInfo']
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
        
        # Validate input
        if 'companyName' not in data or not data['companyName'].strip():
            return jsonify({'error': 'Missing or empty companyName field'}), 400
        
        company_name = data['companyName']
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
        
        # Validate required fields
        required_fields = ['companyName', 'contactEmail']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Delegate to credibility engine
        result = engine.analyze(data)
        
        return jsonify(result), 200
        
    except Exception as e:
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
