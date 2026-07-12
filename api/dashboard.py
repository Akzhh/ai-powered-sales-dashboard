import os
import sys
import re
import logging
from flask import Flask, jsonify
from flask_cors import CORS

# Add the root api directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import services.database as database
from services.auth_service import require_auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ai-sales-forecasting-dashboard-secret-key-2026')

# Enable CORS
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    re.compile(r"^https://.*\.vercel\.app$")
]
if os.environ.get("ALLOWED_ORIGINS"):
    cors_origins.extend(os.environ.get("ALLOWED_ORIGINS").split(","))
CORS(app, supports_credentials=True, origins=cors_origins)

@app.route('/api/stats', methods=['GET'])
@app.route('/stats', methods=['GET'])
@require_auth
def get_stats():
    try:
        rows = database.view_sales()
        total_sales = sum(float(r[6]) for r in rows)
        total_profit = sum(float(r[7]) for r in rows)
        total_orders = len(rows)
        return jsonify({
            'total_sales': round(total_sales, 2),
            'total_profit': round(total_profit, 2),
            'total_orders': total_orders
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
