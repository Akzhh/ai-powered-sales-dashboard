import os
import sys
import re
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add the current directory to sys.path so we can import local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from services.database import init_db
from services.model_loader import ModelLoader

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

# Import blueprints
from routes.auth import auth_bp
from routes.sales import sales_bp
from routes.prediction import prediction_bp
from routes.upload import upload_bp
from routes.exports import exports_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(prediction_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(exports_bp)


# Health check endpoint
@app.route('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Backend running successfully'
    })


# API 404 handler
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404


# Startup warmup
def warmup():
    try:
        logger.info("Initializing database...")
        init_db()
    except Exception as e:
        logger.error(f"Database initialization failed (maybe DATABASE_URL is not set): {e}")

    try:
        logger.info("Caching machine learning model...")
        ModelLoader.load_model()
    except Exception as e:
        logger.error(f"Model caching failed: {e}")
    logger.info("Warmup complete. API is ready.")

# Perform warmup lazily to avoid crashing during Vercel build
warmup_done = False

@app.before_request
def do_warmup():
    global warmup_done
    if not warmup_done:
        warmup_done = True
        warmup()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
