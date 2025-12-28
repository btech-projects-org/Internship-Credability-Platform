# ========================
# SENTIMENT ANALYSIS ROUTES
# ========================

from flask import Blueprint, request, jsonify
from services.sentiment_analyzer import SentimentAnalyzer

sentiment_bp = Blueprint('sentiment', __name__)
analyzer = None

def _ensure_initialized():
    """Lazy initialize analyzer on first request"""
    global analyzer
    if analyzer is None:
        analyzer = SentimentAnalyzer()

@sentiment_bp.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    """
    Endpoint: /api/sentiment
    Purpose: Analyze text sentiment
    Allowed: Delegate to sentiment service
    Forbidden: Scoring logic, model inference
    """
    _ensure_initialized()
    try:
        data = request.get_json()
        
        if 'text' not in data:
            return jsonify({'error': 'Missing text field'}), 400
        
        result = analyzer.analyze(data['text'])
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@sentiment_bp.route('/batch_sentiment', methods=['POST'])
def batch_sentiment():
    """
    Endpoint: /api/batch_sentiment
    Purpose: Batch sentiment analysis
    Allowed: Batch processing delegation
    Forbidden: Direct model usage
    """
    _ensure_initialized()
    try:
        data = request.get_json()
        
        if 'texts' not in data or not isinstance(data['texts'], list):
            return jsonify({'error': 'Missing or invalid texts array'}), 400
        
        results = analyzer.batch_analyze(data['texts'])
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
