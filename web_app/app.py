import os
import re
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
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
@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'service': 'AI Sales Forecasting Dashboard API',
        'version': '2.0.0'
    })


# API 404 handler
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404


# Startup warmup
def warmup():
    logger.info("Initializing database...")
    init_db()
    logger.info("Caching machine learning model...")
    ModelLoader.load_model()
    logger.info("Warmup complete. API is ready.")


# Perform warmup under app context on startup
with app.app_context():
    warmup()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
