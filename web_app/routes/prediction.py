from flask import Blueprint, request, jsonify
from services.forecast import predict_sales
from services.database import get_latest_model_metadata, get_dataset_rows
from services.auth_service import require_auth

prediction_bp = Blueprint('prediction', __name__)


@prediction_bp.route('/api/predict', methods=['POST'])
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

        prediction = predict_sales(m)
        return jsonify({
            'month': m,
            'predicted_sales': prediction
        })
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@prediction_bp.route('/api/model/info', methods=['GET'])
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


@prediction_bp.route('/api/dataset', methods=['GET'])
@require_auth
def get_dataset():
    """Return dataset rows from the database (uploaded via CSV)."""
    try:
        data = get_dataset_rows()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
