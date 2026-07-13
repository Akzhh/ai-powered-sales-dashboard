# pyrefly: ignore [missing-import]
from flask import Blueprint
import os
import sys
import logging
from flask import jsonify

# Add the root api directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _services.config import SECRET_KEY, CORS_ORIGINS
import _services.database as database
from _services.auth_service import require_auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route('/api/stats', methods=['GET'])
@dashboard_bp.route('/stats', methods=['GET'])
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


