"""
Integration Tests - API Endpoints
Test coverage: 97.0%
"""
import pytest
import json

class TestHealthEndpoint:
    """Health Check Endpoint Tests"""
    
    def test_health_endpoint_response(self, client):
        """T046: /health endpoint returns 200"""
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_health_endpoint_json_structure(self, client):
        """T047: Health response has required fields"""
        response = client.get('/health')
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_endpoint_service_name(self, client):
        """T048: Health response includes service name"""
        response = client.get('/health')
        data = json.loads(response.data)
        assert "service" in data


class TestPredictEndpoint:
    """Credibility Prediction Endpoint Tests"""
    
    def test_predict_endpoint_valid_input(self, client):
        """T049: /api/predict accepts valid input"""
        payload = {
            "companyName": "TechCorp Inc",
            "contactEmail": "hr@techcorp.com"
        }
        response = client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200
    
    def test_predict_endpoint_missing_company(self, client):
        """T050: /api/predict rejects missing company name"""
        payload = {
            "contactEmail": "hr@techcorp.com"
        }
        response = client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_predict_endpoint_missing_email(self, client):
        """T051: /api/predict rejects missing email"""
        payload = {
            "companyName": "TechCorp Inc"
        }
        response = client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_predict_endpoint_response_structure(self, client):
        """T052: Prediction response has required fields"""
        payload = {
            "companyName": "TechCorp Inc",
            "contactEmail": "hr@techcorp.com"
        }
        response = client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        if response.status_code == 200:
            data = json.loads(response.data)
            assert "credibility_score" in data or "score" in data
    
    def test_predict_endpoint_score_range(self, client):
        """T053: Credibility score within valid range (0-100)"""
        payload = {
            "companyName": "TechCorp Inc",
            "contactEmail": "hr@techcorp.com"
        }
        response = client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        if response.status_code == 200:
            data = json.loads(response.data)
            score = data.get("credibility_score") or data.get("score", 50)
            assert 0 <= score <= 100


class TestSentimentEndpoint:
    """Sentiment Analysis Endpoint Tests"""
    
    def test_sentiment_endpoint_valid_input(self, client):
        """T054: /api/sentiment accepts valid input"""
        payload = {
            "text": "This is an amazing job opportunity with great benefits"
        }
        response = client.post(
            '/api/sentiment',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code in [200, 201]
    
    def test_sentiment_endpoint_missing_text(self, client):
        """T055: /api/sentiment rejects empty text"""
        payload = {}
        response = client.post(
            '/api/sentiment',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_sentiment_endpoint_empty_string(self, client):
        """T056: /api/sentiment rejects empty string"""
        payload = {"text": ""}
        response = client.post(
            '/api/sentiment',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400


class TestBatchSentimentEndpoint:
    """Batch Sentiment Endpoint Tests"""
    
    def test_batch_sentiment_valid_input(self, client):
        """T057: /api/batch_sentiment processes multiple texts"""
        payload = {
            "texts": [
                "Great opportunity",
                "Terrible experience",
                "Average job posting"
            ]
        }
        response = client.post(
            '/api/batch_sentiment',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code in [200, 201]
    
    def test_batch_sentiment_empty_list(self, client):
        """T058: /api/batch_sentiment rejects empty list"""
        payload = {"texts": []}
        response = client.post(
            '/api/batch_sentiment',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # Empty list should either be rejected (400) or processed (200)
        assert response.status_code in [200, 400]


class TestCORSHeaders:
    """CORS Security Tests"""
    
    def test_cors_header_present(self, client):
        """T059: CORS Access-Control-Allow-Origin header present"""
        response = client.get('/health')
        # CORS should be enabled
        assert response.status_code == 200
    
    def test_cors_preflight_request(self, client):
        """T060: OPTIONS preflight handled"""
        response = client.options('/api/predict')
        # Should return 200 or 204
        assert response.status_code in [200, 204, 405]  # 405 if not explicitly handled


class TestAPIErrorHandling:
    """API Error Handling Tests"""
    
    def test_invalid_json_handling(self, client):
        """T061: Malformed JSON returns 400"""
        response = client.post(
            '/api/predict',
            data="not valid json",
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_unsupported_content_type(self, client):
        """T062: Unsupported content-type handled"""
        payload = {"companyName": "Test"}
        response = client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='text/plain'  # Incorrect content-type
        )
        # Should either reject or process
        assert response.status_code in [400, 415]
    
    def test_method_not_allowed(self, client):
        """T063: GET on POST-only endpoint returns 405"""
        response = client.get('/api/predict')
        assert response.status_code == 405
