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
        
        # Pass data directly to engine for analysis
        # Engine will return 0% if any critical fields are missing
        
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
