#!/usr/bin/env python3
"""Backend smoke tests.
- Imports key modules
- Exercises /health and API routes via Flask test client
"""
import json
import sys
from pathlib import Path

# Ensure project root (backend) on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app

# Sample payload for predict
PREDICT_PAYLOAD = {
    "companyName": "Acme Corp",
    "contactEmail": "hr@acme.com",
    "companyWebsite": "https://acme.com",
    "jobDescription": "We offer a great internship with learning opportunities.",
    "hasLinkedIn": True,
    "hasGlassdoor": False,
    "isRegistered": True,
    "requiresPayment": False,
    "requestsBankDetails": False,
    "noContract": False,
    "pressureToDecide": False,
    "requestsPersonalInfo": False
}


def test_health(client):
    resp = client.get('/health')
    assert resp.status_code == 200, resp.data


def test_predict(client):
    resp = client.post('/api/predict', data=json.dumps(PREDICT_PAYLOAD), content_type='application/json')
    assert resp.status_code == 200, resp.data
    body = resp.get_json()
    assert 'credibility_score' in body


def test_sentiment(client):
    payload = {"text": "This internship looks promising and well-structured."}
    resp = client.post('/api/sentiment', data=json.dumps(payload), content_type='application/json')
    assert resp.status_code == 200, resp.data
    body = resp.get_json()
    assert 'label' in body


def test_batch_sentiment(client):
    payload = {"texts": ["Good place", "Bad experience"]}
    resp = client.post('/api/batch_sentiment', data=json.dumps(payload), content_type='application/json')
    assert resp.status_code == 200, resp.data


def run_all():
    with app.test_client() as client:
        test_health(client)
        test_predict(client)
        test_sentiment(client)
        test_batch_sentiment(client)
    print("Smoke tests passed")


if __name__ == '__main__':
    run_all()
