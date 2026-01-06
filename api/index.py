# ========================
# VERCEL SERVERLESS FUNCTION
# ========================

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', 'config', 'secrets.env'))

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Register blueprints
from routes.credibility_routes import credibility_bp
from routes.sentiment_routes import sentiment_bp

app.register_blueprint(credibility_bp, url_prefix='/api')
app.register_blueprint(sentiment_bp, url_prefix='/api')

@app.route('/api/health')
def health_check():
    return {'status': 'healthy', 'service': 'Internship Credibility API'}, 200

# Vercel serverless function handler
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()

# Export the app for Vercel
app = app
