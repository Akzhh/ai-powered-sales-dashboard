import os
import re
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "models" / "sales_model.pkl"
MODEL_JSON_PATH = BASE_DIR / "models" / "sales_model.json"

# Secret Keys
SECRET_KEY = os.environ.get('SECRET_KEY', 'ai-sales-forecasting-dashboard-secret-key-2026')
JWT_SECRET = os.environ.get("JWT_SECRET") or SECRET_KEY

# Database
DATABASE_URL = os.environ.get("DATABASE_URL")

# CORS Origins
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    re.compile(r"^https://.*\.vercel\.app$")
]
if os.environ.get("ALLOWED_ORIGINS"):
    CORS_ORIGINS.extend(os.environ.get("ALLOWED_ORIGINS").split(","))
