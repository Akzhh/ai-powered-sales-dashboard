# pyrefly: ignore [missing-import]
from flask import Blueprint
import os
import sys
import logging
from flask import jsonify, request

# Removed sys.path modification to avoid ModuleNotFoundError on Vercel

from _services.config import SECRET_KEY, CORS_ORIGINS
from _services.database import get_latest_model_metadata
from _services.auth_service import require_auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

predict_bp = Blueprint("predict", __name__)


@predict_bp.route('/api/predict', methods=['POST'])
@predict_bp.route('/predict', methods=['POST'])
@require_auth
def predict():
    data = request.get_json() or {}
    month = data.get('month')

    if month is None:
        return jsonify({'error': 'Month is required'}), 400

    try:
        m = int(month)
        if m <= 0:
            return jsonify({'error': 'Month must be greater than 0'}), 400

        # Lazy import of forecast/predict_sales to prevent early sklearn/pandas import
        from _services.forecast import predict_sales
        prediction = predict_sales(m)
        return jsonify({
            'month': m,
            'predicted_sales': prediction
        })
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@predict_bp.route('/api/model/info', methods=['GET'])
@predict_bp.route('/model/info', methods=['GET'])
@require_auth
def model_info():
    try:
        metadata = get_latest_model_metadata()
        if metadata:
            return jsonify(metadata)
        else:
            return jsonify({
                "accuracy": 0.0,
                "algorithm": "Linear Regression (Not trained yet)",
                "training_date": "N/A",
                "dataset_size": 0
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


