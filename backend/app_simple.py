#!/usr/bin/env python3
"""Minimal Flask app for testing"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'Internship Credibility API'}), 200

@app.route('/test')
def test():
    return jsonify({'message': 'Backend is working'}), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
