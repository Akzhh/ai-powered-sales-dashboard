import os
import sys
import re
import logging
from flask import Flask, jsonify
from flask_cors import CORS

# Add the 'api' directory to sys.path so we can import shared local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.dirname(current_dir)
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

from services.database import init_db
from services.model_loader import ModelLoader
from routes.prediction import prediction_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Flask App Setup
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ai-sales-forecasting-dashboard-secret-key-2026')

# Enable CORS for React dev server, production domains, and any Vercel deployments
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    re.compile(r"^https://.*\.vercel\.app$")
]
if os.environ.get("ALLOWED_ORIGINS"):
    cors_origins.extend(os.environ.get("ALLOWED_ORIGINS").split(","))

CORS(app, supports_credentials=True, origins=cors_origins)

# Register only the prediction blueprint
app.register_blueprint(prediction_bp)

# Health check specifically for prediction service
@app.route('/api/predict/health')
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Prediction Serverless Function running successfully'
    })

# API 404 handler
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

# Perform warmup lazily to avoid crashing during Vercel build
warmup_done = False

@app.before_request
def do_warmup():
    global warmup_done
    if not warmup_done:
        warmup_done = True
        try:
            logger.info("Initializing database connection for predict function...")
            init_db()
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")

        try:
            logger.info("Caching machine learning model...")
            ModelLoader.load_model()
        except Exception as e:
            logger.error(f"Model caching failed: {e}")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
