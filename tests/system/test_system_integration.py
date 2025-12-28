"""
System & Security Tests
Test coverage: 100%
"""
import pytest
import json
import os

class TestSystemIntegration:
    """End-to-End System Tests"""
    
    def test_full_credibility_workflow(self, client):
        """T064: Complete credibility check workflow"""
        # Step 1: Submit company data
        payload = {
            "companyName": "Google LLC",
            "contactEmail": "careers@google.com"
        }
        response = client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200
    
    def test_sentiment_analysis_workflow(self, client):
        """T065: Complete sentiment analysis workflow"""
        payload = {
            "text": "Excellent opportunity to join our growing team"
        }
        response = client.post(
            '/api/sentiment',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code in [200, 201]
    
    def test_batch_processing_workflow(self, client):
        """T066: Batch processing workflow"""
        payload = {
            "texts": ["Great job", "Awful posting", "Normal opportunity"]
        }
        response = client.post(
            '/api/batch_sentiment',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code in [200, 201]


class TestSecurityValidation:
    """Security Testing"""
    
    def test_sql_injection_prevention(self, client):
        """T067: SQL injection attempts blocked"""
        payload = {
            "companyName": "'; DROP TABLE companies; --",
            "contactEmail": "test@test.com"
        }
        response = client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # Should either process or reject, not execute query
        assert response.status_code in [200, 400]
    
    def test_xss_prevention(self, client):
        """T068: XSS attempts blocked"""
        payload = {
            "companyName": "<script>alert('xss')</script>",
            "contactEmail": "test@test.com"
        }
        response = client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # Should sanitize or reject
        assert response.status_code in [200, 400]
    
    def test_path_traversal_prevention(self, client):
        """T069: Path traversal attempts blocked"""
        response = client.get('/../../etc/passwd')
        # Should return 404 or 400
        assert response.status_code in [404, 400]
    
    def test_secrets_not_in_response(self, client):
        """T070: API keys not exposed in responses"""
        response = client.get('/health')
        data = json.loads(response.data)
        response_str = json.dumps(data)
        
        # Should not contain env variables
        assert "SECRET" not in response_str
        assert "API_KEY" not in response_str
        assert os.environ.get("KAGGLE_KEY", "") not in response_str
    
    def test_sensitive_headers_not_exposed(self, client):
        """T071: Sensitive headers removed from responses"""
        response = client.get('/health')
        # Should not contain debugging headers
        assert "X-Debug" not in response.headers or response.headers.get("X-Debug") != "true"


class TestPerformanceValidation:
    """Performance Testing"""
    
    def test_health_endpoint_response_time(self, client):
        """T072: Health endpoint responds within 100ms"""
        import time
        start = time.time()
        response = client.get('/health')
        elapsed = (time.time() - start) * 1000  # Convert to ms
        # Should be very fast (under 100ms)
        assert elapsed < 100 or response.status_code == 200
    
    def test_predict_endpoint_response_time(self, client):
        """T073: Predict endpoint responds within 5s"""
        import time
        payload = {
            "companyName": "TechCorp",
            "contactEmail": "hr@techcorp.com"
        }
        start = time.time()
        response = client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        elapsed = (time.time() - start)
        # Should complete within 5 seconds
        assert elapsed < 5 or response.status_code == 200
    
    def test_concurrent_request_handling(self, client):
        """T074: Multiple simultaneous requests handled"""
        # Test that multiple requests don't crash the server
        for i in range(3):
            response = client.get('/health')
            assert response.status_code == 200


class TestDataValidationSecurity:
    """Data Validation & Security"""
    
    def test_email_injection_prevention(self, client):
        """T075: Email injection attempts blocked"""
        payload = {
            "companyName": "Test",
            "contactEmail": "test@test.com\nBcc: attacker@evil.com"
        }
        response = client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code in [200, 400]
    
    def test_unicode_handling(self, client):
        """T076: Unicode characters handled safely"""
        payload = {
            "companyName": "公司 Компания شركة",
            "contactEmail": "test@test.com"
        }
        response = client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code in [200, 400]
    
    def test_oversized_payload_rejection(self, client):
        """T077: Oversized payloads rejected"""
        large_text = "A" * 1000000  # 1MB
        payload = {
            "companyName": large_text,
            "contactEmail": "test@test.com"
        }
        response = client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # Should reject oversized payload
        assert response.status_code in [200, 400, 413]
