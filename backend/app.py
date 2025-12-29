# ========================
# FLASK APPLICATION BOOTSTRAP
# ========================

from flask import Flask
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Register blueprints
from routes.credibility_routes import credibility_bp
from routes.sentiment_routes import sentiment_bp

app.register_blueprint(credibility_bp, url_prefix='/api')
app.register_blueprint(sentiment_bp, url_prefix='/api')

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'service': 'Internship Credibility API'}, 200

if __name__ == '__main__':
    # Debug off and reloader disabled to prevent double-starts in subprocesses
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
