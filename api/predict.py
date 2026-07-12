import os
import sys
import re
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add the root api directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.config import SECRET_KEY, CORS_ORIGINS
from services.database import get_latest_model_metadata
from services.auth_service import require_auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Enable CORS
CORS(app, supports_credentials=True, origins=CORS_ORIGINS)

@app.route('/api/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
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
        from services.forecast import predict_sales
        prediction = predict_sales(m)
        return jsonify({
            'month': m,
            'predicted_sales': prediction
        })
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/model/info', methods=['GET'])
@app.route('/model/info', methods=['GET'])
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
