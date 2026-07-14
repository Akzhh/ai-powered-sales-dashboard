import os
import re
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "models" / "sales_model.pkl"
MODEL_JSON_PATH = BASE_DIR / "models" / "sales_model.json"

# Secret Keys
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is missing. It is required for secure authentication.")

JWT_SECRET = os.environ.get("JWT_SECRET") or SECRET_KEY

# Environment Validation
FLASK_ENV = os.environ.get("FLASK_ENV", "production")

# Database Validation
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing. It is required for database connectivity.")

# CORS Origins
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    re.compile(r"^https://.*\.vercel\.app$")
]
if os.environ.get("ALLOWED_ORIGINS"):
    CORS_ORIGINS.extend(os.environ.get("ALLOWED_ORIGINS").split(","))
