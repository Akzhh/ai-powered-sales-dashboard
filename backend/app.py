import os
import logging
from flask import Flask
from flask_cors import CORS
from pathlib import Path
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
BASE_DIR = Path(__file__).resolve().parent
TMP_DIR = BASE_DIR / "tmp"
TMP_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ai-sales-forecasting-dashboard-secret-key-2026')

# Configure session cookie settings for cross-origin authentication in production
if os.environ.get('ENV') == 'production' or os.environ.get('DATABASE_URL'):
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True

# Enable CORS for React dev server and production frontend domain(s)
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
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


# Startup warmup
def warmup():
    logger.info("Initializing database...")
    init_db()
    logger.info("Caching machine learning model...")
    ModelLoader.load_model()


# Perform warmup under app context on startup
with app.app_context():
    warmup()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
